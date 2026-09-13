#!/usr/bin/env python3
"""Write measured demo diagnostics as report-only evidence."""
import argparse
import json
from pathlib import Path

from demo_app.diagnostics import collect_diagnostics

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--commit", required=True)
parser.add_argument("--run-id", required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
report = collect_diagnostics(commit_id=args.commit, run_id=args.run_id)
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print("Demo runtime diagnostics (report-only): " + report["status"])
