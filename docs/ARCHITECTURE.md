# Architecture

The demo application is intentionally small. It contains one Python package and one service function so governance workflows can exercise a realistic repository shape without domain-specific assumptions.

## Components

| Component | Responsibility |
| --- | --- |
| `src/demo_app/service.py` | Provides a small release descriptor function. |
| `tests/test_service.py` | Verifies the demo behavior. |
| GitHub Actions workflows | Produce evidence and call the public governance baselines. |

## Interfaces

The demo has no external runtime interface. The Python function is used only by tests.

## Baseline

The example solution baseline is:

```text
example-solution-baseline
```

## Release compatibility

The demo release is compatible with the `example-solution-baseline` for
report-only evaluation. It has no external runtime interface and therefore
has no migration or data-contract compatibility dependency. The declaration
remains subject to architecture-owner approval before blocking use.

## Resilience and feedback

The application is intentionally stateless. A failed test run can be rerun
from the same commit without recovery of runtime state. Findings from each
architecture run are reviewed as improvement backlog input; production
failover and degraded-mode behavior are out of scope until a deployable
service is introduced.
