#!/usr/bin/python3
"""Exercise real Git changes and review invalidation through the CLI."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / 'tools/reconcile.py'


class ReconcileTest(unittest.TestCase):
  def test_changes_require_review_and_pending_stays_incomplete(self):
    with tempfile.TemporaryDirectory() as tmp:
      root = Path(tmp) / 'local'
      upstream = Path(tmp) / 'upstream'
      root.mkdir()
      upstream.mkdir()
      def git(*args):
        return subprocess.run(['git', '-C', str(upstream), *args], check=True, capture_output=True)
      git('init', '-b', 'master')
      git('config', 'user.email', 'test@example.invalid')
      git('config', 'user.name', 'Test')
      recipe = upstream / 'pkgbuilds/demo'
      recipe.mkdir(parents=True)
      (recipe / 'PKGBUILD').write_text('pkgver=1\n')
      git('add', '.')
      git('commit', '-m', 'initial')
      (root / 'catalog.tsv').write_text('upstream_name\tstatus\tnote\ndemo\tpending\tNeeds a port\n')
      (root / 'packages').mkdir()
      def run(*args, code=0):
        result = subprocess.run(['python3', str(TOOL), '--root', str(root), '--upstream', str(upstream), '--ref', 'HEAD', *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result.stdout
      run('check', code=1)
      run('review', 'demo', '--reason', 'Reviewed; port remains blocked')
      run('check')
      run('check', '--complete', code=1)
      # Auxiliary upstream files must invalidate a review even without a version bump.
      (recipe / 'fix.patch').write_text('a necessary patch\n')
      git('add', '.')
      git('commit', '-m', 'patch')
      run('check', code=1)
      run('review', 'demo', '--reason', 'Reviewed patch; blocker remains')
      local = root / 'packages/demo'
      local.mkdir()
      (local / 'demo.spec').write_text('Version: 1\n')
      run('check', code=1)
      run('review', 'demo', '--reason', 'Reviewed local port work')
      # New recipes cannot disappear from the report behind the old snapshot.
      new = upstream / 'pkgbuilds/new'
      new.mkdir()
      (new / 'PKGBUILD').write_text('pkgver=1\n')
      git('add', '.')
      git('commit', '-m', 'new recipe')
      report = json.loads(run('check', '--json', code=1))
      self.assertTrue(any(i['package'] == 'new' for i in report['issues']))
      git('rm', '-r', 'pkgbuilds/new', 'pkgbuilds/demo')
      git('commit', '-m', 'retire recipes')
      self.assertIn('absent upstream', run('check', code=1))
      run('review', 'demo', '--retain-removed', '--reason', 'Fedora still needs this port')
      run('check')
      (root / 'catalog.tsv').write_text('upstream_name\tstatus\tnote\ndemo\tretired\tRemoved upstream\n')
      (local / 'demo.spec').unlink()
      local.rmdir()
      run('review', 'demo', '--reason', 'Retired and removed the local recipe')
      run('check')
      recipe.mkdir(parents=True)
      (recipe / 'PKGBUILD').write_text('pkgver=2\n')
      git('add', '.')
      git('commit', '-m', 'restore recipe')
      self.assertIn('reassess retirement', run('check', code=1))


if __name__ == '__main__':
  unittest.main()
