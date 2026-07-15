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
