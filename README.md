# Governance Framework Demo Consumer

This repository is a neutral demo consumer for the public DevSecOps Governance Framework.

It shows how an application repository can consume:

- `joku-dev/devsecops-governance-framework/.github/workflows/devsecops-baseline-l1-v1.1.3.yml@l1-baseline-v1.1.3`
- `joku-dev/devsecops-governance-framework/.github/workflows/architecture-baseline-l1-v0.1.0.yml@architecture-baseline-l1-v0.1.0`

The demo intentionally starts in `report-only` mode. This keeps the first onboarding run useful for review without requiring branch protection or production-grade evidence on day one.

## What This Repository Contains

| Path | Purpose |
| --- | --- |
| `.github/workflows/devsecops-baseline.yml` | Builds a small source artifact, generates minimal evidence and calls the public DevSecOps L1 baseline. |
| `.github/workflows/architecture-governance.yml` | Calls the public Architecture L1 baseline. |
| `.governance/architecture/` | Draft architecture evidence examples consumed by the architecture collector. |
| `docs/` | Minimal architecture and deployment documentation referenced by evidence. |
| `src/demo_app/` | Tiny example application. |
| `tests/` | Minimal unit test. |

## Expected Workflow Result

The first run should produce:

- `application-evidence`
- `devsecops-pipeline-evidence`
- `governance-run-input`
- `architecture-governance-evidence`

Findings are acceptable while the repository is in `report-only` mode. A team should switch to blocking mode only after evidence generation and branch protection are stable.

## Local Test

```bash
python3 -m unittest discover -s tests
```

## Adoption Source

This repository was created from the public adoption package:

```text
https://github.com/joku-dev/devsecops-governance-framework/tree/main/adoption-package
```
