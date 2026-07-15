from pathlib import Path
import json
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from normalize_trivy_scan import normalize


class NormalizeTrivyScanTests(unittest.TestCase):
    def test_normalizes_findings_and_maximum_severity(self) -> None:
        payload = json.loads((ROOT / "tests" / "fixtures" / "trivy-scan.json").read_text(encoding="utf-8"))

        result = normalize(
            payload,
            scanner_version="v0.70.0",
            produced_at="2026-07-15T16:00:00Z",
            artifact="application-source.tar.gz",
        )

        self.assertEqual(result["scanner"], {"name": "trivy", "version": "v0.70.0"})
        self.assertEqual(result["max_severity"], "critical")
        self.assertEqual(len(result["findings"]), 2)
        self.assertEqual(result["findings"][0]["severity"], "HIGH")
        self.assertEqual(result["findings"][0]["fixed_version"], "1.2.1")

    def test_empty_results_produce_a_real_empty_scan(self) -> None:
        result = normalize(
            {"Results": [{"Target": ".", "Vulnerabilities": None}]},
            scanner_version="v0.70.0",
            produced_at="2026-07-15T16:00:00+00:00",
            artifact="application-source.tar.gz",
        )

        self.assertEqual(result["max_severity"], "none")
        self.assertEqual(result["findings"], [])

    def test_rejects_a_timestamp_without_timezone(self) -> None:
        with self.assertRaisesRegex(ValueError, "timezone"):
            normalize(
                {"Results": []},
                scanner_version="v0.70.0",
                produced_at="2026-07-15T16:00:00",
                artifact="application-source.tar.gz",
            )


if __name__ == "__main__":
    unittest.main()
