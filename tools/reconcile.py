#!/usr/bin/python3
"""Account for upstream recipe changes without executing PKGBUILDs."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {'published', 'ready', 'pending', 'not-applicable', 'retired'}


def git(repo, *args):
  return subprocess.check_output(['git', '-C', str(repo), *args])


def digest(files):
  h = hashlib.sha256()
  for name, data in sorted(files):
    h.update(name.encode() + b'\0' + len(data).to_bytes(8, 'big') + data)
  return h.hexdigest()


def upstream(repo, ref):
  commit = git(repo, 'rev-parse', '--verify', ref + '^{commit}').decode().strip()
  paths = git(repo, 'ls-tree', '-r', '--name-only', '-z', commit, '--', 'pkgbuilds').decode().split('\0')
  grouped = {}
  for path in filter(None, paths):
    parts = path.split('/')
    if len(parts) >= 3:
      grouped.setdefault(parts[1], []).append(path)
  return commit, {
    name: digest((p, git(repo, 'show', f'{commit}:{p}')) for p in paths)
    for name, paths in grouped.items() if f'pkgbuilds/{name}/PKGBUILD' in paths
  }


def catalog(root):
  rows = {}
  with (root / 'catalog.tsv').open() as f:
    for row in csv.DictReader(f, delimiter='\t'):
      name = row['upstream_name']
      if name in rows:
        raise ValueError(f'duplicate catalog entry: {name}')
      if row['status'] not in STATUSES or not row['note'].strip():
        raise ValueError(f'invalid status or missing explanation: {name}')
      rows[name] = row
  return rows


def local_digest(root, name, row):
  files = [('catalog', json.dumps(row, sort_keys=True).encode())]
  directory = root / 'packages' / name
  if name in {'omarchy', 'omarchy-settings'}:
    directory = root / 'packaging' / 'rpm' / name
    files.append(('omadora-revision', (root / 'omadora-revision').read_bytes()))
  if directory.exists():
    files.extend((str(p.relative_to(root)), p.read_bytes()) for p in directory.rglob('*') if p.is_file())
  return digest(files)


def audit(root, recipes, rows, reviews):
  issues = []
  names = set(recipes) | set(rows)
  for name in sorted(names):
    row = rows.get(name)
    if row is None:
      issues.append((name, 'new upstream recipe has no catalog entry'))
      continue
    present = name in recipes
    if present and row['status'] == 'retired':
      issues.append((name, 'retired catalog entry exists upstream again: reassess retirement'))
    if not present and row['status'] != 'retired' and not reviews.get(name, {}).get('retain_removed'):
      issues.append((name, 'absent upstream: retire it or review and record a Fedora exception'))
    recipe = root / 'packages' / name / f'{name}.spec'
    if name in {'omarchy', 'omarchy-settings'}:
      recipe = root / 'packaging' / 'rpm' / name / f'{name}.spec'
    if row['status'] in {'ready', 'published'} and not recipe.is_file():
      # A moved package must have a reviewed external location, not a fake local spec.
      if not reviews.get(name, {}).get('external_recipe'):
        issues.append((name, 'maintained package has no spec or reviewed external recipe'))
    if row['status'] == 'retired' and (root / 'packages' / name).exists():
      issues.append((name, 'retired recipe still exists locally'))
    record = reviews.get(name, {})
    if record.get('upstream_digest') != recipes.get(name) or record.get('local_digest') != local_digest(root, name, row) or not record.get('reason'):
      issues.append((name, 'review required (upstream files, local recipe, or catalog changed)'))
  for directory in sorted((root / 'packages').iterdir()):
    if directory.is_dir() and directory.name not in rows:
      issues.append((directory.name, 'local recipe has no catalog entry'))
  return issues


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--root', type=Path, default=ROOT)
  parser.add_argument('--upstream', type=Path, required=True, help='local upstream Git checkout; fetch it before running')
  parser.add_argument('--ref', default='origin/master', help='upstream commit or ref (default: origin/master)')
  commands = parser.add_subparsers(dest='command', required=True)
  check = commands.add_parser('check', help='report unreviewed changes and unresolved work')
  check.add_argument('--complete', action='store_true', help='also fail for pending or unpublished packages')
  check.add_argument('--json', action='store_true')
  review = commands.add_parser('review', help='record one completed manual recipe review')
  review.add_argument('package')
  review.add_argument('--reason', required=True, help='what was ported, validated, retired, or why it is excluded')
  review.add_argument('--retain-removed', action='store_true', help='explicitly retain a removed upstream recipe for Fedora')
  review.add_argument('--external-recipe', help='repository URL/path for a package maintained elsewhere')
  args = parser.parse_args()
  root = args.root.resolve()
  commit, recipes = upstream(args.upstream, args.ref)
  rows = catalog(root)
  state_path = root / 'upstream-reviews.json'
  state = json.loads(state_path.read_text()) if state_path.exists() else {'schema': 1, 'packages': {}}
  if state.get('schema') != 1:
    raise ValueError('unsupported upstream review schema')
  reviews = state['packages']
  if args.command == 'review':
    name = args.package
    if name not in rows or not args.reason.strip():
      raise ValueError('review requires a catalog entry and a nonempty reason')
    reviews[name] = {
      'upstream_commit': commit,
      'upstream_digest': recipes.get(name),
      'local_digest': local_digest(root, name, rows[name]),
      'reason': args.reason,
    }
    if args.retain_removed:
      reviews[name]['retain_removed'] = True
    if args.external_recipe:
      reviews[name]['external_recipe'] = args.external_recipe
    temp = state_path.with_suffix('.json.tmp')
    temp.write_text(json.dumps(state, indent=2, sort_keys=True) + '\n')
    temp.replace(state_path)
    print(f'Recorded {name} at {commit}')
    return 0
  issues = audit(root, recipes, rows, reviews)
  unresolved = [{'package': n, 'status': r['status'], 'note': r['note']} for n, r in sorted(rows.items()) if r['status'] in {'pending', 'ready'}]
  report = {'upstream_commit': commit, 'upstream_recipes': len(recipes), 'issues': [{'package': n, 'reason': why} for n, why in issues], 'unresolved': unresolved}
  if args.json:
    print(json.dumps(report, indent=2))
  else:
    print(f'Upstream {commit}: {len(recipes)} recipes')
    for n, why in issues:
      print(f'REVIEW {n}: {why}')
    for item in unresolved:
      print(f"{item['status'].upper()} {item['package']}: {item['note']}")
    print(f'{len(issues)} review issues; {len(unresolved)} unresolved packages')
  return int(bool(issues or (args.complete and unresolved)))


if __name__ == '__main__':
  try:
    sys.exit(main())
  except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
    print(f'reconcile: {error}', file=sys.stderr)
    sys.exit(2)
