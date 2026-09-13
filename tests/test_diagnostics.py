import unittest
from demo_app.diagnostics import collect_diagnostics


class DiagnosticTests(unittest.TestCase):
    def test_real_function_success_and_rejection(self):
        report = collect_diagnostics(commit_id="a" * 40, run_id="local")
        self.assertEqual(report["status"], "pass")
        self.assertEqual([c["id"] for c in report["checks"]],
                         ["valid_release", "empty_name", "empty_version"])
        self.assertTrue(all(c["duration_ns"] >= 0 for c in report["checks"]))

    def test_unexpected_runtime_failure_is_visible(self):
        def broken(*args):
            raise RuntimeError("unavailable")
        report = collect_diagnostics(commit_id="a" * 40, run_id="local", operation=broken)
        self.assertEqual(report["status"], "fail")
        self.assertTrue(all(c["status"] == "fail" for c in report["checks"]))
        self.assertEqual(report["checks"][0]["observed_error_type"], "RuntimeError")

    def test_failure_to_reject_invalid_input_is_visible(self):
        def permissive(name, version):
            return {"name": name, "version": version, "status": "demo"}
        report = collect_diagnostics(commit_id="a" * 40, run_id="local", operation=permissive)
        self.assertEqual([c["status"] for c in report["checks"]], ["pass", "fail", "fail"])

    def test_wrong_success_payload_is_visible(self):
        report = collect_diagnostics(commit_id="a" * 40, run_id="local", operation=lambda *a: {})
        self.assertEqual(report["status"], "fail")
