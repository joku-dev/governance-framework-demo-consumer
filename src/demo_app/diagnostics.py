"""Measured diagnostics for the local demo function; no deployment health claim."""
from datetime import datetime, timezone
from time import perf_counter_ns

from .service import describe_release


def collect_diagnostics(*, commit_id, run_id, operation=describe_release):
    """Exercise successful calls and input rejection without hiding failures."""
    cases = [("valid_release", "demo-app", "0.1.0", False),
             ("empty_name", "", "0.1.0", True),
             ("empty_version", "demo-app", "", True)]
    checks = []
    for name, app, version, reject in cases:
        started = perf_counter_ns()
        error_type = None
        try:
            result = operation(app, version)
            passed = not reject and result == {
                "name": app, "version": version, "status": "demo"}
        except ValueError:
            passed = reject
            error_type = "ValueError"
        except Exception as error:
            passed = False
            error_type = type(error).__name__
        checks.append({"id": name, "status": "pass" if passed else "fail",
                       "duration_ns": max(0, perf_counter_ns() - started),
                       "observed_error_type": error_type})
    return {"schema_version": "0.1.0", "evidence_type": "demo_runtime_diagnostics",
            "scope": "local Python function in CI; no deployed service",
            "commit_id": commit_id, "run_id": run_id,
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "status": "pass" if all(c["status"] == "pass" for c in checks) else "fail",
            "checks": checks}
