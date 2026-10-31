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

    def test_committed_inputs_have_stable_fingerprints(self):
        head=submit.git('rev-parse','HEAD')
        inputs=submit.fingerprints(head)
        self.assertIn('helium-browser-bin',inputs)
        self.assertEqual(inputs['omarchy'], inputs['omarchy-settings'])
        self.assertEqual(inputs, submit.fingerprints(head))


if __name__ == '__main__':unittest.main()
