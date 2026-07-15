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
- no collector result updates the central viewer in this pilot

## Recommended Live Run

1. Open the repository's **Actions** page.
2. Select **DevSecOps Baseline**.
3. Run the workflow with **Run workflow** on `main`.
4. Follow the `Prepare Evidence` job through scan, normalization, collection,
   and upload.
5. Download `application-evidence`.
6. Show the raw scan, normalized scan, and Trust record in that order.
7. Open the `Central DevSecOps Baseline` job and explain the report-only result.

A manually dispatched run is diagnostic evidence. It does not claim to be the
official mainline state and does not automatically update a central
`latest_result`.

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
- typed vulnerability Trust is not yet projected into the central viewer
- no Trust signal blocks delivery
