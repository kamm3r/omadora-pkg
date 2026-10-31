import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('submit_edge', Path(__file__).resolve().parents[1]/'tools/submit-edge.py')
submit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(submit)


class SubmissionTests(unittest.TestCase):
    def test_only_main_push_can_submit(self):
        submit.validate_context('push', 'refs/heads/main')
        for event, ref in [('pull_request','refs/heads/main'), ('workflow_dispatch','refs/heads/main'), ('push','refs/heads/hyprland-testing')]:
            with self.assertRaises(ValueError):submit.validate_context(event, ref)

    def test_webhook_is_restricted_to_exact_edge_project(self):
        submit.validate_endpoint('https://copr.fedorainfracloud.org/webhooks/github/123/token-value/',123)
        for url in ['https://copr.fedorainfracloud.org/webhooks/github/124/token-value/',
                    'https://evil.test/webhooks/github/123/token-value/',
                    'http://copr.fedorainfracloud.org/webhooks/github/123/token-value/',
                    'https://copr.fedorainfracloud.org/webhooks/github/123/token-value/?redirect=other']:
            with self.assertRaises(ValueError):submit.validate_endpoint(url,123)

    def test_changes_accumulate_since_last_submission(self):
        self.assertEqual(submit.changed_inputs({'a':'old','b':'old'}, {'a':'new','b':'new'}),['a','b'])
        self.assertEqual(submit.changed_inputs({'a':'new','b':'new'}, {'a':'new','b':'new'}),[])

    def test_new_recipe_is_selected_but_retirement_is_not_a_build(self):
        self.assertEqual(submit.changed_inputs({'old':'hash'}, {'new':'hash'}),['new'])

    def test_manual_core_and_blocked_recipes_do_not_block_normal_submissions(self):
        self.assertEqual(submit.automatic_inputs(['omarchy','omarchy-settings','allowed','blocked','new'],
                         {'allowed':'ready','blocked':'pending','new':'not-applicable'}),['allowed'])

    def test_receipt_uses_creation_time_instead_of_artifact_id_or_api_order(self):
        import io
        import json
        import zipfile
        from types import SimpleNamespace
        from unittest.mock import patch
        artifacts = [
            {'id':900,'created_at':'2026-10-31T07:12:00Z','expired':False,'workflow_run':{'id':1},'archive_download_url':'https://example.test/old'},
            {'id':100,'created_at':'2026-10-31T07:19:00Z','expired':False,'workflow_run':{'id':2},'archive_download_url':'https://example.test/new'}]
        def metadata(url, token):
            if '/actions/artifacts?' in url:return {'artifacts':artifacts}
            identifier=int(url.rsplit('/',1)[1])
            return {'event':'push','head_branch':'main','workflow_id':77,'head_sha':str(identifier)*40}
        def download(request, timeout):
            identifier=2 if request.full_url.endswith('/new') else 1
            data=io.BytesIO()
            with zipfile.ZipFile(data,'w') as archive:
                archive.writestr('edge-submission.json',json.dumps({'state':'submitted','head':str(identifier)*40,'fingerprints':{'example':str(identifier)}}))
            return io.BytesIO(data.getvalue())
        with patch.object(submit,'json_get',side_effect=metadata), \
             patch.object(submit.urllib.request,'build_opener',return_value=SimpleNamespace(open=download)), \
             patch.object(submit.subprocess,'run',return_value=SimpleNamespace(returncode=0)):
            receipt=submit.prior_receipt('owner/repo',77,'3'*40,'test-token')
            self.assertEqual(receipt['fingerprints']['example'],'2')

    def test_committed_inputs_have_stable_fingerprints(self):
        head=submit.git('rev-parse','HEAD')
        inputs=submit.fingerprints(head)
        self.assertIn('helium-browser-bin',inputs)
        self.assertEqual(inputs['omarchy'], inputs['omarchy-settings'])
        self.assertEqual(inputs, submit.fingerprints(head))


if __name__ == '__main__':unittest.main()
