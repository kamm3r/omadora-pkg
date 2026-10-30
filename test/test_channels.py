#!/usr/bin/env python3
import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('channels', Path(__file__).resolve().parents[1]/'tools/channels.py')
channels = importlib.util.module_from_spec(spec)
spec.loader.exec_module(channels)
CONFIG = channels.read_json(channels.ROOT/'.copr/channels.json')


def package(name='example', version='1.0', release='1.fc44', content='a', epoch='0'):
    return {'name': name, 'arch': 'x86_64', 'evr': {'epoch': epoch, 'ver': version, 'rel': release},
            'checksum': content, 'content': {'header_sha256': content, 'payload_sha256': [content]}, 'requires': []}


class PromotionTests(unittest.TestCase):
    def validate(self, src, dst, source='edge', destination='rc'):
        return channels.validate_transition(CONFIG, source, destination, src, dst)

    def test_forward_moves_only(self):
        for source, destination in [('rc', 'edge'), ('stable', 'rc'), ('edge', 'stable'), ('stable', 'edge')]:
            with self.assertRaisesRegex(ValueError, 'Only edge'):
                self.validate([], [], source, destination)
        self.assertEqual(self.validate([], [], 'rc', 'stable'), [])

    def test_rpm_epoch_tilde_and_numeric_release_order(self):
        for src, dst in [(package(version='1.0~rc1'), package(version='1.0')),
                         (package(version='10', epoch='0'), package(version='1', epoch='1')),
                         (package(release='2.fc44'), package(release='10.fc44'))]:
            with self.assertRaisesRegex(ValueError, 'Downgrade'):
                self.validate([src], [dst])
        self.assertEqual(len(self.validate([package(release='10.fc44')], [package(release='2.fc44')])), 1)

    def test_resigning_same_content_is_not_a_rebuild(self):
        left, right = package(), package()
        right['checksum'] = 'different destination signature'
        self.assertEqual(self.validate([left], [right]), [])
        self.assertEqual(len(channels.latest([left, right])), 1)
        right['content']['header_sha256'] = 'conflicting header'
        with self.assertRaisesRegex(ValueError, 'Ambiguous same-NEVRA'):
            channels.latest([left, right])

    def test_same_version_changed_payload_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'same-version'):
            self.validate([package(content='b')], [package()])

    def test_removal_requires_separate_review(self):
        with self.assertRaisesRegex(ValueError, 'retirement'):
            self.validate([], [package()])

    def test_partial_coordinated_group_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Incomplete coordinated'):
            self.validate([package('omarchy')], [])

    def test_titlebars_must_match_exact_compositor(self):
        src = [package(name) for name in CONFIG['groups'][1]]
        with self.assertRaisesRegex(ValueError, 'exact staged Hyprland'):
            self.validate(src, [])
        src[-1]['requires'] = [{'name': 'hyprland(x86-64)', 'flags': 'EQ', 'epoch': '0', 'ver': '1.0', 'rel': '1.fc44'}]
        self.assertEqual(len(self.validate(src, [])), 4)
        src[-1]['requires'][0]['rel'] = '2.fc44'
        with self.assertRaisesRegex(ValueError, 'exact staged Hyprland'):
            self.validate(src, [])

    def candidate(self):
        instance = channels.Channels.__new__(channels.Channels)
        instance.config = CONFIG
        snapshot = {'project': 'omadora-edge', 'artifacts': [package()], 'definitions': []}
        plan = {'from': 'edge', 'to': 'rc', 'source': snapshot, 'destination': {},
                'changed': [package()], 'config_sha256': channels.digest(CONFIG)}
        plan['sha256'] = channels.digest(plan)
        return instance, plan

    def test_tampered_plan_rejected_before_api(self):
        instance, plan = self.candidate()
        plan['to'] = 'stable'
        with self.assertRaisesRegex(ValueError, 'checksum'):
            instance.apply(plan, {}, '/unused')

    def test_missing_or_unbound_evidence_rejected_before_api(self):
        instance, plan = self.candidate()
        with self.assertRaisesRegex(ValueError, 'bound'):
            instance.apply(plan, {}, '/unused')
        with self.assertRaisesRegex(ValueError, 'automated-tests'):
            instance.apply(plan, {'plan_sha256': plan['sha256']}, '/unused')

    def test_stale_plan_rejected_before_publication(self):
        instance, plan = self.candidate()
        instance.snapshot = lambda channel: {'changed': True}
        evidence = {'plan_sha256': plan['sha256'], 'checks': {'automated-tests': {'result': 'passed', 'details': 'test record'}}}
        with self.assertRaisesRegex(ValueError, 'changed since planning'):
            instance.apply(plan, evidence, '/unused')

    def test_core_versions_must_match(self):
        with self.assertRaisesRegex(ValueError, 'Core packages'):
            self.validate([package('omarchy', version='2'), package('omarchy-settings', version='1')], [])

    def test_apply_and_verify_resigned_artifact(self):
        from types import SimpleNamespace
        instance, plan = self.candidate()
        instance.owner = CONFIG['owner']
        instance.packages = lambda channel: []
        source = plan['source']
        destination = plan['destination']
        calls = []
        instance.client = SimpleNamespace(project_proxy=SimpleNamespace(fork=lambda *a, **k: calls.append(a)))
        instance.snapshot = lambda channel: source if channel == 'edge' else destination
        instance.verify_download = lambda project, artifact: calls.append(('download', project))
        evidence = {'plan_sha256': plan['sha256'], 'checks': {'automated-tests': {'result': 'passed', 'details': 'measured result'}}}
        # Destination must be a complete snapshot for validation.
        destination.update({'project': 'omadora-rc', 'artifacts': []})
        plan['sha256'] = channels.digest({k: v for k, v in plan.items() if k != 'sha256'})
        evidence['plan_sha256'] = plan['sha256']
        with tempfile.TemporaryDirectory() as directory:
            submitted = Path(directory)/'submitted.json'
            instance.apply(plan, evidence, submitted)
            self.assertEqual(channels.read_json(submitted)['state'], 'submission-intent')
            self.assertTrue(any(call[:3] == ('kammer', 'omadora-edge', 'kammer') for call in calls))
            copied = copy.deepcopy(source)
            copied['project'] = 'omadora-rc'
            copied['artifacts'][0]['checksum'] = 'new signature'
            instance.snapshot = lambda channel: source if channel == 'edge' else copied
            verified = Path(directory)/'verified.json'
            instance.verify(channels.read_json(submitted), verified)
            self.assertEqual(channels.read_json(verified)['state'], 'verified')
            copied['artifacts'][0]['content']['header_sha256'] = 'changed header'
            with self.assertRaisesRegex(ValueError, 'altered artifact'):
                instance.verify(channels.read_json(submitted), Path(directory)/'bad.json')

    def test_forked_builds_are_selected_and_partial_copy_is_rejected(self):
        from types import SimpleNamespace as S
        from unittest.mock import patch
        instance = channels.Channels.__new__(channels.Channels)
        instance.config, instance.owner = CONFIG, 'kammer'
        item = S(name='example', source_type='scm', auto_rebuild=False,
                 source_dict={'clone_url': CONFIG['source_repository'], 'committish': 'main'},
                 builds={'latest': {'id': 42, 'state': 'forked'}, 'latest_succeeded': None})
        instance.packages = lambda channel: [item]
        build = S(id=42, state='forked', chroots=[CONFIG['chroot']], source_package={'name': 'example'})
        info = S(chroot_repos={CONFIG['chroot']: 'https://example.test/'})
        instance.client = S(project_proxy=S(get=lambda *a: info), build_proxy=S(get_list=lambda *a: [build]))
        result = b'{"packages":[{"name":"example","epoch":null,"version":"1.0","release":"1.fc44","arch":"x86_64"}]}'
        with patch.object(channels, 'fetch', return_value=result), \
             patch.object(channels, 'metadata', return_value=[package()]), \
             patch.object(channels, 'enrich_artifacts', side_effect=lambda base, artifacts: artifacts):
            self.assertEqual(instance.snapshot('edge')['definitions'][0]['successful'], 42)
        with patch.object(channels, 'fetch', return_value=result), \
             patch.object(channels, 'metadata', return_value=[]):
            with self.assertRaisesRegex(ValueError, 'Latest successful builds'):
                instance.snapshot('edge')

    def test_receipts_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'receipt.json'
            channels.write_json(path, {'state': 'submitted'})
            with self.assertRaises(FileExistsError):
                channels.write_json(path, {'state': 'verified'})


if __name__ == '__main__':
    unittest.main()
