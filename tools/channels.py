#!/usr/bin/env python3
"""Frozen whole-project COPR promotion. No builds, reverse moves, or downgrades."""
import argparse
import datetime
import gzip
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
import tempfile
import fcntl
from pathlib import Path
import sys
import struct
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = {'r': 'http://linux.duke.edu/metadata/repo',
      'c': 'http://linux.duke.edu/metadata/common',
      'rpm': 'http://linux.duke.edu/metadata/rpm'}
GOOD = {'succeeded', 'forked'}
TERMINAL = GOOD | {'failed', 'canceled', 'skipped'}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    path = Path(path)
    # Never overwrite an earlier plan, freeze receipt or publication receipt.
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def fetch(url):
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read()


def header_identity(url):
    """Read immutable header/payload digests; COPR replaces only RPM signatures."""
    import rpm
    # Read enough bytes for both RPM headers, without fetching a large payload.
    limit = 1024 * 1024
    for attempt in range(3):
        request = urllib.request.Request(url, headers={'Range': f'bytes=0-{limit-1}'})
        with urllib.request.urlopen(request, timeout=120) as response:
            data = response.read(limit)
        if len(data) < 112 or data[:4] != b'\xed\xab\xee\xdb':
            raise ValueError('Invalid RPM lead: ' + url)
        indexes, size = struct.unpack('>II', data[104:112])
        signature_size = 16 + indexes * 16 + size
        header_start = 96 + ((signature_size + 7) // 8) * 8
        needed = header_start + 16
        if len(data) >= needed:
            indexes, size = struct.unpack('>II', data[header_start+8:header_start+16])
            needed += indexes * 16 + size
        if needed > 64 * 1024 * 1024:
            raise ValueError('RPM header exceeds 64 MiB: ' + url)
        if len(data) < needed:
            limit = needed
            continue
        with tempfile.TemporaryFile() as stream:
            stream.write(data)
            stream.seek(0)
            transaction = rpm.TransactionSet()
            transaction.setVSFlags(rpm.RPMVSF_MASK_NOSIGNATURES)
            header = transaction.hdrFromFdno(stream.fileno())
            result = {'header_sha256': header['sha256header'],
                      'payload_sha256': list(header['payloadsha256'])}
            if not result['header_sha256'] or not result['payload_sha256']:
                raise ValueError('Missing strong RPM content digests')
            return result
    raise ValueError('Cannot read RPM header: ' + url)


def same_content(left, right):
    if 'content' in left and 'content' in right:
        return left['content'] == right['content']
    return left['checksum'] == right['checksum']


def metadata(base, enrich=True):
    repomd = ET.fromstring(fetch(base + 'repodata/repomd.xml'))
    primary = repomd.find("r:data[@type='primary']", NS)
    data = fetch(base + primary.find('r:location', NS).attrib['href'])
    checksum = primary.find('r:checksum', NS)
    if hashlib.new(checksum.attrib['type'], data).hexdigest() != checksum.text:
        raise ValueError('Primary metadata checksum mismatch')
    if data[:2] == b'\x1f\x8b':
        data = gzip.decompress(data)
    result = []
    for package in ET.fromstring(data).findall('c:package', NS):
        arch = package.findtext('c:arch', namespaces=NS)
        # Keep source RPMs too: COPR forks them as well.
        result.append({
            'name': package.findtext('c:name', namespaces=NS), 'arch': arch,
            'evr': package.find('c:version', NS).attrib,
            'checksum_type': package.find('c:checksum', NS).attrib['type'],
            'checksum': package.findtext('c:checksum', namespaces=NS),
            'size': int(package.find('c:size', NS).attrib['package']),
            'location': package.find('c:location', NS).attrib['href'],
            'requires': [entry.attrib for entry in package.findall('c:format/rpm:requires/rpm:entry', NS)]})
    result.sort(key=lambda p: (p['name'], p['arch'], json.dumps(p['evr'], sort_keys=True)))
    return enrich_artifacts(base, result) if enrich else result


def enrich_artifacts(base, artifacts):
    def enrich(package):
        package['content'] = header_identity(base + package['location'])
        return package
    with ThreadPoolExecutor(max_workers=6) as pool:
        return list(pool.map(enrich, artifacts))


def identity(package):
    return package['name'], package['arch']


def evr(package):
    v = package['evr']
    return str(v.get('epoch', '0')), v['ver'], v['rel']


def compare(left, right):
    import rpm
    return rpm.labelCompare(evr(left), evr(right))


def latest(packages):
    result = {}
    for package in packages:
        key = identity(package)
        if key not in result or compare(package, result[key]) > 0:
            result[key] = package
        elif compare(package, result[key]) == 0 and not same_content(package, result[key]):
            raise ValueError(f'Ambiguous same-NEVRA artifacts: {key}')
    return result


def validate_transition(config, source, destination, src, dst):
    if [source, destination] not in config['transitions']:
        raise ValueError('Only edge -> rc and rc -> stable are allowed')
    old, new = latest(dst), latest(src)
    changed = []
    for key, package in new.items():
        previous = old.get(key)
        if previous:
            order = compare(package, previous)
            if order < 0:
                raise ValueError(f'Downgrade rejected: {key}')
            if order == 0:
                if not same_content(package, previous):
                    raise ValueError(f'Changed same-version build rejected: {key}; increase Release')
                continue
        changed.append(package)
    missing = set(old) - set(new)
    if missing:
        raise ValueError(f'Source is missing destination packages; retirement needs a separate review: {sorted(missing)}')
    names = {p['name'] for p in changed if p['arch'] != 'src'}
    binary = {p['name']: p for p in new.values() if p['arch'] not in {'src', 'nosrc'}}
    for group in config['groups']:
        if names.intersection(group) and not set(group).issubset(binary):
            raise ValueError(f'Incomplete coordinated package group: {group}')
    if names.intersection({'omarchy', 'omarchy-settings'}):
        if evr(binary['omarchy']) != evr(binary['omarchy-settings']):
            raise ValueError('Core packages must have the same staged version/release')
    # Validate exact Hyprland dependency from titlebars against the staged runtime.
    if names.intersection({'hyprland', 'omarchy-hyprland-titlebars'}):
        runtime, plugin = binary.get('hyprland'), binary.get('omarchy-hyprland-titlebars')
        if runtime and plugin:
            requirements = [r for r in plugin['requires'] if r['name'].split('(')[0] == 'hyprland' and r.get('flags') == 'EQ']
            if not requirements or any((r.get('epoch', '0'), r.get('ver'), r.get('rel')) != evr(runtime) for r in requirements):
                raise ValueError('Titlebars does not require the exact staged Hyprland release')
    return changed


class Channels:
    def __init__(self, config):
        from copr.v3 import Client
        self.client = Client.create_from_config_file()
        self.config = config
        self.owner = config['owner']

    def project(self, channel):
        return self.config['projects'][channel]

    def packages(self, channel):
        return list(self.client.package_proxy.get_list(self.owner, self.project(channel),
                    with_latest_build=True, with_latest_succeeded_build=True))

    def snapshot(self, channel):
        project = self.project(channel)
        info = self.client.project_proxy.get(self.owner, project)
        if set(info.chroot_repos) != {self.config['chroot']}:
            raise ValueError('Unexpected chroots: whole-project forks require exactly the configured chroot')
        packages = self.packages(channel)
        if any(p.auto_rebuild for p in packages):
            raise ValueError(f'{channel} must be frozen: automatic rebuilds are enabled')
        # Check all retained builds, including an older concurrently running job.
        successful = {}
        for build in self.client.build_proxy.get_list(self.owner, project):
            if build.state not in TERMINAL:
                raise ValueError(f'Build {build.id} is not finished: {build.state}')
            if build.state in GOOD and self.config['chroot'] in build.chroots:
                name = build.source_package['name']
                successful[name] = max(successful.get(name, 0), build.id)
        definitions = []
        for package in packages:
            if package.source_dict.get('clone_url') == self.config['source_repository'] and package.source_dict.get('committish') != self.config['source_ref']:
                raise ValueError(f'{package.name} must explicitly pin the main source branch')
            b = package.builds
            if b['latest'] and b['latest']['state'] == 'failed':
                raise ValueError(f'Latest build of {package.name} failed')
            definitions.append({'name': package.name, 'type': package.source_type,
                                'source': dict(package.source_dict),
                                'latest': b['latest']['id'] if b['latest'] else None,
                                'successful': successful.get(package.name)})
        def outputs(definition):
            if not definition['successful']:
                return []
            url = info.chroot_repos[self.config['chroot']] + f"{definition['successful']:08d}-{definition['name']}/results.json"
            packages = json.loads(fetch(url))['packages']
            return [(p['name'], p['arch'], str(p.get('epoch') or '0'), p['version'], p['release']) for p in packages]
        with ThreadPoolExecutor(max_workers=6) as pool:
            selected = {tuple(p) for group in pool.map(outputs, definitions) for p in group}
        artifacts = metadata(info.chroot_repos[self.config['chroot']], enrich=False)
        visible = {(p['name'], p['arch'], *evr(p)) for p in latest(artifacts).values()}
        if selected != visible:
            raise ValueError('Latest successful builds do not match latest repository RPMs; time-based fork would select unexpected versions. Missing: ' + str(sorted(selected - visible)[:8]) + '; unexpected: ' + str(sorted(visible - selected)[:8]))
        artifacts = enrich_artifacts(info.chroot_repos[self.config['chroot']], artifacts)
        return {'project': project, 'chroot': self.config['chroot'],
                'definitions': sorted(definitions, key=lambda p: p['name']),
                'artifacts': artifacts}

    def freeze(self, channel, output):
        if channel != 'edge':
            raise ValueError('Only edge has automatic builds; rc and stable must stay frozen')
        packages = self.packages(channel)
        enabled = sorted(p.name for p in packages if p.auto_rebuild)
        receipt = {'schema': 1, 'channel': channel, 'project': self.project(channel),
                   'config_sha256': digest(self.config), 'created_at': now(), 'enabled': enabled}
        # Save recovery state before any mutation.
        write_json(output, receipt)
        for name in enabled:
            p = next(p for p in packages if p.name == name)
            self.client.package_proxy.edit(self.owner, self.project(channel), name,
                                          p.source_type, {'webhook_rebuild': False})
        if any(p.auto_rebuild for p in self.packages(channel)):
            raise ValueError('Freeze incomplete; retry manually using the saved receipt')
        print(f'Frozen edge; recovery receipt: {output}')

    def thaw(self, receipt):
        if receipt['channel'] != 'edge' or receipt['project'] != self.project('edge') or receipt['config_sha256'] != digest(self.config):
            raise ValueError('Freeze receipt belongs to a different channel/configuration')
        packages = {p.name: p for p in self.packages('edge')}
        if not set(receipt['enabled']).issubset(packages):
            raise ValueError('A previously enabled package disappeared')
        for name in receipt['enabled']:
            p = packages[name]
            self.client.package_proxy.edit(self.owner, self.project('edge'), name,
                                          p.source_type, {'webhook_rebuild': True})
        enabled = {p.name for p in self.packages('edge') if p.auto_rebuild}
        if enabled != set(receipt['enabled']):
            raise ValueError('Enabled set differs from freeze receipt')
        print('Restored the exact edge automatic-build set')

    def plan(self, source, destination, output):
        if [source, destination] not in self.config['transitions']:
            raise ValueError('Only edge -> rc and rc -> stable are allowed')
        src, dst = self.snapshot(source), self.snapshot(destination)
        changed = validate_transition(self.config, source, destination, src['artifacts'], dst['artifacts'])
        plan = {'schema': 1, 'created_at': now(), 'config_sha256': digest(self.config),
                'from': source, 'to': destination, 'source': src, 'destination': dst, 'changed': changed}
        plan['sha256'] = digest(plan)
        write_json(output, plan)
        print(f"Plan {plan['sha256']}: {len(changed)} changed RPMs; no publication requested")

    def apply(self, plan, evidence, output):
        unsigned = {k: v for k, v in plan.items() if k != 'sha256'}
        if digest(unsigned) != plan['sha256'] or plan['config_sha256'] != digest(self.config):
            raise ValueError('Plan checksum/configuration mismatch')
        if evidence.get('plan_sha256') != plan['sha256']:
            raise ValueError('Test evidence is not bound to this plan')
        for gate in self.config['required_evidence'][plan['to']]:
            record = evidence.get('checks', {}).get(gate, {})
            if record.get('result') != 'passed' or not record.get('details'):
                raise ValueError(f'Missing passing evidence: {gate}')
        src, dst = self.snapshot(plan['from']), self.snapshot(plan['to'])
        if src != plan['source'] or dst != plan['destination']:
            raise ValueError('Channel changed since planning; create and test a fresh plan')
        changed = validate_transition(self.config, plan['from'], plan['to'], src['artifacts'], dst['artifacts'])
        if changed != plan['changed'] or not changed:
            raise ValueError('No changes or inconsistent changed artifact list')
        for package in changed:
            self.verify_download(src['project'], package)
        # Write a durable intent before requesting COPR's asynchronous fork.
        write_json(output, {'schema': 1, 'state': 'submission-intent', 'recorded_at': now(),
                            'plan': plan, 'evidence': evidence})
        # A whole-project fork also copies unchanged NEVRAs. Keep all build records
        # to avoid deleting artifacts still referenced by same-version copies.
        for channel in (plan['from'], plan['to']):
            for package in self.packages(channel):
                self.client.package_proxy.edit(self.owner, self.project(channel), package.name,
                                               package.source_type, {'max_builds': 0})
        self.client.project_proxy.fork(self.owner, src['project'], self.owner, dst['project'], confirm=True)
        print(f'Fork requested; not yet verified. Run verify --receipt {output}')

    def verify_download(self, project, package):
        base = f'https://download.copr.fedorainfracloud.org/results/{self.owner}/{project}/{self.config["chroot"]}/'
        digest = hashlib.new(package['checksum_type'])
        size = 0
        with urllib.request.urlopen(base + package['location'], timeout=120) as response:
            while chunk := response.read(1024 * 1024):
                size += len(chunk)
                digest.update(chunk)
        if size != package['size'] or digest.hexdigest() != package['checksum']:
            raise ValueError(f'Artifact integrity check failed: {package["name"]}')

    def verify(self, receipt, output):
        plan = receipt['plan']
        src = self.snapshot(plan['from'])
        if src != plan['source']:
            raise ValueError('Source changed before verification; keep it frozen and investigate')
        dst = self.snapshot(plan['to'])
        expected = latest(src['artifacts'])
        actual = latest(dst['artifacts'])
        if set(actual) != set(expected):
            raise ValueError('Fork incomplete or unexpected destination package set')
        for key, package in expected.items():
            other = actual[key]
            if evr(package) != evr(other) or not same_content(package, other):
                raise ValueError(f'Fork incomplete or altered artifact: {key}')
        for package in plan['changed']:
            self.verify_download(dst['project'], actual[identity(package)])
        write_json(output, {**receipt, 'state': 'verified', 'verified_at': now(), 'destination_after': dst})
        print(f'Published and verified: {output}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT/'.copr/channels.json')
    commands = parser.add_subparsers(dest='command', required=True)
    freeze = commands.add_parser('freeze')
    freeze.add_argument('channel', choices=['edge'])
    freeze.add_argument('--out', required=True, type=Path)
    thaw = commands.add_parser('thaw')
    thaw.add_argument('--receipt', required=True, type=Path)
    plan = commands.add_parser('plan')
    plan.add_argument('--from', dest='source', required=True, choices=['edge', 'rc', 'stable'])
    plan.add_argument('--to', dest='destination', required=True, choices=['edge', 'rc', 'stable'])
    plan.add_argument('--out', required=True, type=Path)
    apply = commands.add_parser('apply')
    apply.add_argument('--plan', required=True, type=Path)
    apply.add_argument('--evidence', required=True, type=Path)
    apply.add_argument('--out', required=True, type=Path)
    verify = commands.add_parser('verify')
    verify.add_argument('--receipt', required=True, type=Path)
    verify.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    # Serialize local release commands; remote administrators must honor the freeze too.
    lock = (ROOT/'.copr/channel.lock').open('a')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise ValueError('Another local channel command is running')
    channels = Channels(read_json(args.config))
    if args.command == 'freeze': channels.freeze(args.channel, args.out)
    elif args.command == 'thaw': channels.thaw(read_json(args.receipt))
    elif args.command == 'plan': channels.plan(args.source, args.destination, args.out)
    elif args.command == 'apply': channels.apply(read_json(args.plan), read_json(args.evidence), args.out)
    elif args.command == 'verify': channels.verify(read_json(args.receipt), args.out)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as error:
        print(f'Refused: {error}', file=sys.stderr)
        sys.exit(1)
