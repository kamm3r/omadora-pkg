#!/usr/bin/env python3
"""Submit changed, tested main-branch recipe inputs to COPR edge only."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile
import io
import time

ROOT = Path(__file__).resolve().parents[1]
OWNER, PROJECT = 'kammer', 'omadora-edge'
API = 'https://copr.fedorainfracloud.org/api_3'
OUTPUT = Path('edge-submission.json')


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()


def json_get(url, token=None):
    headers = {'Accept': 'application/vnd.github+json'} if token else {}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise ValueError(f'Metadata API HTTP {error.code}: {url}') from None


def fingerprints(ref):
    paths = git('ls-tree', '--name-only', ref, 'packages/').splitlines()
    # ls-tree on a directory includes each immediate recipe directory.
    result = {}
    catalog = {row.split('\t')[0]: row.split('\t')[1] for row in git('show', ref + ':catalog.tsv').splitlines()[1:]}
    shared = git('rev-parse', ref + ':.copr/Makefile')
    for path in paths:
        name = path.split('/')[-1]
        if catalog.get(name) not in {'published', 'ready'} or not git('ls-tree', ref, path + '/' + name + '.spec'):
            continue
        result[name] = hashlib.sha256((git('rev-parse', ref + ':' + path) + shared).encode()).hexdigest()
    core = ''.join(git('rev-parse', ref + ':' + path) for path in
                   ['omadora-revision', '.copr/core.mk', 'packaging/rpm/omarchy', 'packaging/rpm/omarchy-settings'])
    for name in ['omarchy', 'omarchy-settings']:
        result[name] = hashlib.sha256((core + shared).encode()).hexdigest()
    return result


def changed_inputs(previous, current):
    return sorted(name for name, value in current.items() if previous.get(name) != value)


def validate_context(event, ref):
    if event != 'push' or ref != 'refs/heads/main':
        raise ValueError('Edge submissions require a successful main push CI run')


def validate_endpoint(url, project_id):
    pattern = rf'https://copr\.fedorainfracloud\.org/webhooks/github/{project_id}/[A-Za-z0-9-]+/'
    if not re.fullmatch(pattern, url):
        raise ValueError('Webhook capability must target the configured edge project')


def prior_receipt(repository, workflow, head, token):
    base = f'https://api.github.com/repos/{repository}'
    artifacts = json_get(base + '/actions/artifacts?name=copr-edge-submission&per_page=100', token)['artifacts']
    for artifact in artifacts:
        if artifact['expired']:
            continue
        run = json_get(base + '/actions/runs/' + str(artifact['workflow_run']['id']), token)
        if run['event'] != 'push' or run['head_branch'] != 'main' or run['workflow_id'] != workflow:
            continue
        request = urllib.request.Request(artifact['archive_download_url'], headers={'Authorization': 'Bearer ' + token})
        # GitHub redirects downloads to a signed URL; strip Authorization on redirects.
        class Redirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
                if redirected:
                    redirected.remove_header('Authorization')
                return redirected
        with urllib.request.build_opener(Redirect()).open(request, timeout=120) as response:
            data = response.read(2 * 1024 * 1024)
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            receipt = json.loads(archive.read('edge-submission.json'))
        if receipt.get('state') != 'submitted' or receipt.get('head') != run['head_sha']:
            continue
        if subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', receipt['head'], head], capture_output=True).returncode:
            if subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', head, receipt['head']], capture_output=True).returncode == 0:
                return {'state': 'outdated'}
            raise ValueError('Submission history diverged; review the release cursor')
        return receipt
    return None


def main():
    validate_context(os.environ['GITHUB_EVENT_NAME'], os.environ['GITHUB_REF'])
    head = os.environ['GITHUB_SHA']
    if git('rev-parse', 'HEAD') != head:
        raise ValueError('Checkout is not the tested commit')
    repo = os.environ['GITHUB_REPOSITORY']
    if repo != 'kamm3r/omadora-pkg':
        raise ValueError('Unexpected repository')
    token = os.environ['GH_TOKEN']
    run = json_get(f'https://api.github.com/repos/{repo}/actions/runs/{os.environ["GITHUB_RUN_ID"]}', token)
    previous = prior_receipt(repo, run['workflow_id'], head, token)
    if previous and previous.get('state') == 'outdated':
        print('A newer tested commit was already submitted; no backward submission')
        return
    before = previous['fingerprints'] if previous else fingerprints((ROOT/'.copr/edge-ci-baseline').read_text().strip())
    current = fingerprints(head)
    names = changed_inputs(before, current)
    catalog = {row.split('\t')[0]: row.split('\t')[1] for row in (ROOT/'catalog.tsv').read_text().splitlines()[1:]}
    names = [name for name in names if name in {'omarchy', 'omarchy-settings'} or catalog.get(name) in {'published', 'ready'}]
    project = json_get(f'{API}/project?ownername={OWNER}&projectname={PROJECT}')
    endpoint = os.environ['COPR_EDGE_WEBHOOK_URL']
    validate_endpoint(endpoint, project['id'])
    packages = json_get(f'{API}/package/list?ownername={OWNER}&projectname={PROJECT}&with_latest_build=true')['items']
    packages = {p['name']: p for p in packages}
    spec = importlib.util.spec_from_file_location('channels', ROOT/'tools/channels.py')
    channels = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(channels)
    metadata = channels.metadata(project['chroot_repos']['fedora-44-x86_64'], enrich=False)
    latest = channels.latest(metadata, check_content=False)
    selected = []
    for name in names:
        package = packages.get(name)
        if not package or not package['auto_rebuild']:
            raise ValueError(f'{name}: edge definition missing or builds are frozen')
        source = package['source_dict']
        if source.get('clone_url') != 'https://github.com/kamm3r/omadora-pkg.git' or source.get('committish') != 'main':
            raise ValueError(f'{name}: unexpected source definition')
        latest_build = package['builds']['latest']
        if latest_build and latest_build['state'] not in channels.TERMINAL:
            raise ValueError(f'{name}: build {latest_build["id"]} is still active; retry after it finishes')
        path = ROOT/'packages'/name/(name+'.spec') if name not in {'omarchy','omarchy-settings'} else ROOT/'packaging/rpm'/name/(name+'.spec')
        output = subprocess.check_output(['rpmspec','-q','--srpm','--define','dist .fc44','--qf','%{NAME}|%{EPOCHNUM}|%{VERSION}|%{RELEASE}',str(path)],text=True).strip()
        rpm_name, epoch, version, release = output.split('|')
        if version == '0':
            raise ValueError('Core submission needs the pinned version/release definitions; use the core release procedure')
        desired = {'name':rpm_name,'evr':{'epoch':epoch,'ver':version,'rel':release}}
        existing = [p for (n,a),p in latest.items() if n == rpm_name and a != 'src']
        if existing and any(channels.compare(desired,p) <= 0 for p in existing):
            raise ValueError(f'{name}: changed recipe must increase epoch/version/release beyond edge')
        selected.append({'name':name,'directory':source.get('subdirectory',''),'previous_build_id':latest_build['id'] if latest_build else None,'version_release':version+'-'+release})
    receipt = {'schema':1,'head':head,'state':'prepared','fingerprints':before.copy(),'builds':{}}
    OUTPUT.write_text(json.dumps(receipt,indent=2)+'\n')
    if selected:
        payload = {'repository':{'clone_url':'https://github.com/kamm3r/omadora-pkg.git'},'ref':'refs/heads/main','after':head,
                   'commits':[{'added':[],'removed':[],'modified':[p['directory']+'/.ci-trigger' for p in selected]}]}
        request = urllib.request.Request(endpoint, data=json.dumps(payload).encode(), headers={
            'Content-Type':'application/json','X-GitHub-Event':'push',
            'X-GitHub-Delivery':f'ci-{os.environ["GITHUB_RUN_ID"]}-{os.environ["GITHUB_RUN_ATTEMPT"]}'})
        try:
            with urllib.request.urlopen(request,timeout=120) as response:
                if response.status != 200:
                    raise ValueError('COPR did not accept the submission')
        except urllib.error.URLError:
            raise ValueError('COPR webhook submission failed; inspect edge before retrying') from None
        for item in selected:
            for attempt in range(5):
                package = json_get(f'{API}/package?ownername={OWNER}&projectname={PROJECT}&package_name={item["name"]}&with_latest_build=true')
                build = package['builds']['latest']
                if build and build['id'] != item['previous_build_id']:
                    receipt['builds'][item['name']] = {'id':build['id'],'version_release':item['version_release'],'state':'submitted','url':f'https://copr.fedorainfracloud.org/coprs/build/{build["id"]}/'}
                    print(item['name'],receipt['builds'][item['name']]['url'])
                    break
                time.sleep(1)
            else:
                raise ValueError(f'{item["name"]}: no new build found after accepted webhook')
    # Retired/blocked recipes are deliberately not marked as submitted.
    for name in current:
        if name not in names or name in receipt['builds']:
            receipt['fingerprints'][name] = current[name]
    receipt['state']='submitted'
    OUTPUT.write_text(json.dumps(receipt,indent=2)+'\n')
    print(f'{len(selected)} tested recipes submitted to edge; submission is not publication verification')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        # Never echo credential-bearing HTTP request URLs.
        print('Edge submission stopped: '+str(error) if not isinstance(error,urllib.error.URLError) else 'Edge submission stopped: network error',file=sys.stderr)
        sys.exit(1)
