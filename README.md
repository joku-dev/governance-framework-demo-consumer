# Governance Framework Demo Consumer

This repository is a neutral demo consumer for the public DevSecOps Governance Framework.

It shows how an application repository can consume:

- `joku-dev/devsecops-governance-framework/.github/workflows/devsecops-baseline-l1-v1.1.3.yml@l1-baseline-v1.1.3`
- `joku-dev/devsecops-governance-framework/.github/workflows/architecture-baseline-l1-v0.1.0.yml@architecture-baseline-l1-v0.1.0`

It also demonstrates the report-only vulnerability Evidence Trust pilot with
a real Trivy scan, normalized evidence, subject digests, and a 24-hour
Freshness evaluation.

The validated mainline evidence is also centrally re-verified and projected in
the governance framework's separate **Typed Evidence Trust** viewer section.
This projection remains report-only and does not change the consumer's
governance result.

The central **Replay Triage** projection additionally uses the GitHub Actions
artifact digest to distinguish newly produced pipeline evidence from
deterministic normalized report content. Historical replay assessments remain
immutable; remediation is demonstrated by producing and intaking a fresh
mainline artifact.

The demo remains in `report-only` mode, while `main` is protected with required
pull-request review and direct pushes disabled. This keeps findings visible for
review without making the governance workflow block delivery.

## What This Repository Contains

| Path | Purpose |
| --- | --- |
| `.github/workflows/devsecops-baseline.yml` | Builds a small source artifact, generates minimal evidence and calls the public DevSecOps L1 baseline. |
| `.github/workflows/architecture-governance.yml` | Calls the public Architecture L1 baseline. |
| `.governance/architecture/` | Draft architecture evidence examples consumed by the architecture collector. |
| `scripts/normalize_trivy_scan.py` | Converts real Trivy JSON into the collector's normalized vulnerability format. |
| `docs/DEMO.md` | Presenter runbook for the end-to-end Evidence Trust demo. |
| `docs/` | Minimal architecture and deployment documentation referenced by evidence. |
| `src/demo_app/` | Tiny example application. |
| `tests/` | Minimal unit test. |

## Expected Workflow Result

The first run should produce:

- `application-evidence`
- `devsecops-pipeline-evidence`
- `governance-run-input`
- `architecture-governance-evidence`

The `application-evidence` artifact also contains the raw Trivy result, the
normalized vulnerability scan, and `vulnerability-scan-trust.json`.

Findings are acceptable while the repository is in `report-only` mode. A team should switch to blocking mode only after evidence generation and branch protection are stable.

## Local Test

For the September maintenance refresh, see
[Refresh governance evidence](docs/EVIDENCE-REFRESH.md).

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Demo Runbook

Use [`docs/DEMO.md`](docs/DEMO.md) for the live walkthrough, expected Trust
signals, and the distinction between a diagnostic run and official mainline
state.

## Adoption Source

This repository was created from the public adoption package:

```text
https://github.com/joku-dev/devsecops-governance-framework/tree/main/adoption-package
```
