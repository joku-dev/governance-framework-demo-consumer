# Deployment

This demo repository does not deploy a production service.

The deployment evidence is intentionally minimal and documents that:

- the repository can be packaged as a source artifact,
- the governance workflows can evaluate that artifact,
- runtime operations evidence remains draft until a real service is deployed.

The CI workflow provides the current operational evidence boundary: build,
test, scan, artifact upload, and architecture-governance execution are
observable in GitHub Actions logs. No production health endpoint, dashboard,
runtime metric, or rollback execution exists for this repository.

CI additionally produces `demo-runtime-diagnostics`: measured outcomes and durations
for successful and rejected calls to the local Python demo function. See the
[open operation-readiness action](OPERATION_READINESS_ACTION.md). This is a
non-deployed runtime diagnostic and does not supply production metrics or alerts.
