# End-to-End Evidence Trust Demo

## Demo Goal

This repository demonstrates how an application consumes released governance
baselines and pilots typed Evidence Trust without changing delivery behavior.

The DevSecOps workflow shows this chain:

```text
application source
  -> packaged application artifact
  -> real Trivy filesystem scan
  -> normalized vulnerability evidence
  -> collector capture and SHA-256 verification
  -> provisional 24-hour Freshness evaluation
  -> report-only Evidence Trust record
  -> released DevSecOps L1 governance evaluation
  -> independent central re-verification and viewer projection
```

The architecture workflow independently demonstrates the released
Architecture L1 baseline.

## What To Show

### 1. Consumer Boundaries

Open `.github/workflows/devsecops-baseline.yml` and explain:

- the application repository produces its own evidence
- the governance repository owns schemas, collectors, policies, and baselines
- released baseline `l1-baseline-v1.1.3` remains the governance evaluation
- the collector pilot is pinned to commit `754cfb4`
- everything remains report-only

### 2. Real Scanner Output

Open the `application-evidence` artifact from a GitHub Actions run and compare:

```text
security/trivy-scan.raw.json
security/vulnerability-scan.json
```

The first file is scanner-native Trivy JSON. The second is the small,
repository-normalized format consumed by the collector. Normalization retains
the vulnerability ID, package, installed and fixed versions, status, severity,
scanner identity, production time, and maximum severity.

### 3. Trust Record

Open:

```text
governance/vulnerability-scan-trust.json
```

Highlight:

| Field | Demo meaning |
|---|---|
| `effective_level` | Expected `integrity_verified` after both file digests are recomputed |
| `capture.evidence_type` | `vulnerability_scan` |
| `capture.subjects` | Digests for the normalized scan and packaged application source |
| `capture.observations.finding_count` | Findings reported by the real scan |
| `capture.observations.severity_consistent` | Whether the declared summary matches the normalized findings |
| `capture.observations.subject_binding.mode` | `co_collected` |
| `checks[].finding_effect` | `report_only` |

The useful distinction is that Evidence Trust does not decide whether the
vulnerabilities are acceptable. It answers whether the evidence bytes,
identity, age, and collection context were evaluated.

### 4. Freshness

The collector compares the scan production time with verification time using
the provisional 24-hour policy. A fresh run should show a passing
`freshness_evaluated` check. A stale scan would remain integrity-verified but
receive a report-only Freshness failure.

### 5. Governance Result

Open the `devsecops-pipeline-evidence` artifact and the reusable workflow
summary. Explain that:

- vulnerability findings and Evidence Trust are separate signals
- the released baseline evaluates the normalized governance input
- report-only findings remain visible without failing delivery
- the central viewer projects typed Trust separately from governance results

### 6. Central Projection

In `joku-dev/devsecops-governance-framework`, open the **Typed Evidence
Trust** section of `generated/viewer/status-viewer.html`. The central intake
downloads `application-evidence`, recomputes both subject digests, applies
Freshness again, and records its own verifier identity. It does not trust the
producer assessment without checking the downloaded bytes.

The projection is stored separately in
`status/typed-evidence-results-index.json`; it does not create a governance
pass or replace governance `latest_result`.

## Recommended Live Run

1. Open the repository's **Actions** page.
2. Select **DevSecOps Baseline**.
3. Run the workflow with **Run workflow** on `main`.
4. Follow the `Prepare Evidence` job through scan, normalization, collection,
   and upload.
5. Download `application-evidence`.
6. Show the raw scan, normalized scan, and Trust record in that order.
7. Open the `Central DevSecOps Baseline` job and explain the report-only result.
8. Open the governance viewer's **Typed Evidence Trust** section and compare
   the centrally verified run with the producer record.

A manually dispatched run is diagnostic evidence. It does not claim to be the
official mainline state. The typed-evidence index prefers a `main` push, so a
later manual run does not replace that official central projection.

## Expected Result

The exact number of findings can change when the Trivy database changes. The
stable demo expectations are:

- a real scanner identity, never `placeholder`
- both scan and application artifact have SHA-256 subjects
- `effective_level` is `integrity_verified`
- Freshness is evaluated
- `capture.enforcement` is `report_only`
- the workflow uploads all evidence even when findings exist

Do not promise a fixed vulnerability count in the presentation. The changing
scanner database is itself a useful explanation for the Freshness policy.

## Validated Reference Run

The current centrally verified mainline run of this demo is:

| Field | Value |
|---|---|
| Workflow | `DevSecOps Baseline` |
| Run | `29432884108` |
| Commit | `4ec2b2bd53560e010ebb1c078c4d3bd41b0bfcc6` |
| Event | `push` to `main` |
| Trivy | `v0.70.0`, zero findings in this run |
| Collector status | `collected` |
| Effective Trust level | `integrity_verified` |
| Content digest check | `pass` |
| Freshness check | `pass` |
| Enforcement | `report_only` |

Run URL:

```text
https://github.com/joku-dev/governance-framework-demo-consumer/actions/runs/29432884108
```

Use this run as a stable fallback if a live scan is unavailable during a
presentation. Its zero findings are historical to that run; future scanner
database updates may produce a different finding count.

## Local Validation

Run the application and normalizer tests with:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

For a local collector run, first create or obtain a real Trivy JSON output,
normalize it, and then invoke the collector from a local governance-framework
checkout as described in its vulnerability-scan collector usage guide.

## Current Limitations

- normalization is a consumer-owned adapter, not yet a released governance
  framework adapter
- subject binding is `co_collected`, not scanner-attested
- the collector pilot is pinned to a governance-framework commit rather than a
  released collector package
- automatic producer-to-governance dispatch still requires a configured
  cross-repository intake token; manual central intake is available
- no Trust signal blocks delivery
