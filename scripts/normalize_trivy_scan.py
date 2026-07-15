#!/usr/bin/env python3
"""Convert Trivy JSON into the governance collector's normalized scan format."""

from __future__ import annotations

from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
import json


SEVERITY_ORDER = {
    "none": 0,
    "unknown": 1,
    "info": 2,
    "low": 3,
    "medium": 4,
    "high": 5,
    "critical": 6,
}


def parse_timestamp(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("produced_at must be a valid ISO 8601 timestamp") from error
    if parsed.tzinfo is None:
        raise ValueError("produced_at must include a timezone")
    return value


def optional_field(target: dict, name: str, value: object) -> None:
    if value not in (None, ""):
        target[name] = str(value)


def normalize(payload: dict, *, scanner_version: str, produced_at: str, artifact: str) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("Trivy scan must be a JSON object")
    results = payload.get("Results", [])
    if not isinstance(results, list):
        raise ValueError("Trivy Results must be an array")

    findings = []
    for result in results:
        if not isinstance(result, dict):
            raise ValueError("Every Trivy result must be an object")
        vulnerabilities = result.get("Vulnerabilities") or []
        if not isinstance(vulnerabilities, list):
            raise ValueError("Trivy Vulnerabilities must be an array")
        for vulnerability in vulnerabilities:
            if not isinstance(vulnerability, dict):
                raise ValueError("Every Trivy vulnerability must be an object")
            vulnerability_id = vulnerability.get("VulnerabilityID")
            severity = str(vulnerability.get("Severity", "unknown")).lower()
            if not vulnerability_id:
                raise ValueError("Every Trivy vulnerability must have a VulnerabilityID")
            if severity not in SEVERITY_ORDER or severity == "none":
                raise ValueError(f"Unsupported Trivy severity: {severity}")
            finding = {"id": str(vulnerability_id), "severity": severity.upper()}
            optional_field(finding, "package", vulnerability.get("PkgName"))
            optional_field(finding, "installed_version", vulnerability.get("InstalledVersion"))
            optional_field(finding, "fixed_version", vulnerability.get("FixedVersion"))
            optional_field(finding, "status", vulnerability.get("Status"))
            findings.append(finding)

    max_severity = (
        max((finding["severity"].lower() for finding in findings), key=SEVERITY_ORDER.get)
        if findings
        else "none"
    )
    return {
        "schema_version": "1.0.0",
        "scanner": {"name": "trivy", "version": scanner_version},
        "produced_at": parse_timestamp(produced_at),
        "artifact": artifact,
        "max_severity": max_severity,
        "findings": findings,
    }


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Trivy scan must be a JSON object")
    return payload


def main() -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--produced-at", required=True)
    parser.add_argument("--artifact", required=True)
    args = parser.parse_args()

    normalized = normalize(
        load_json(args.input),
        scanner_version=args.scanner_version,
        produced_at=args.produced_at,
        artifact=args.artifact,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(normalized, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
