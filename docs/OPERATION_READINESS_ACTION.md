# Operation-readiness improvement action

Status: **roles and demo evidence scope confirmed; remediation decision and closure pending**.

The architecture run [34778462308](https://github.com/joku-dev/governance-framework-demo-consumer/actions/runs/34778462308)
on commit `7d6a4f67c5e8441e1067405cc2da17218dc256fd` reports two messages
under `operation_readiness`: B5 feedback and P11 observability each score 3,
where the gate requires 4. This is one gate candidate with two source messages.

Technical implementation is maintained by `joku-dev`. The maintainer confirmed
the decision, evidence-approval, closure and role-registry responsibilities for
this consumer, together with the limited CI-local evidence scope. The central
[consumer role record](https://github.com/joku-dev/devsecops-governance-framework/blob/main/model/governance/lifecycle/consumer-operation/roles.json)
records that scoped decision.

The separate consumer implementation was merged in central
[PR #101](https://github.com/joku-dev/devsecops-governance-framework/pull/101).
The maintainer posted the implementation-bound
[personal operating acceptance](https://github.com/joku-dev/devsecops-governance-framework/pull/101#issuecomment-5698945870)
on 16 September 2026. Its verified capture and effective state are published in
the [central consumer lifecycle index](https://github.com/joku-dev/devsecops-governance-framework/blob/main/status/governance-consumer-lifecycle.json).
Individual remediation decisions, progress records and closure still require
their own personal statements under the
[consumer operating guide](https://joku-dev.github.io/devsecops-governance-framework/operations/evidence/consumer-lifecycle-operation/).

## Work and evidence

| Item | Implementation | Recorded scope and remaining step |
|---|---|---|
| Feedback / B5 | This tracked action links the source finding, technical owner, work and closure conditions; feedback evidence references it | Maintainer confirmed the demo evidence boundary; retain the fresh mainline finding and record the separate remediation decision |
| Observability / P11 | CI executes `describe_release` and invalid-input cases, retains outcomes, durations, commit and run in `demo-runtime-diagnostics` | Maintainer accepted CI-local diagnostics for this non-deployed demo; bind actual run artifacts to subsequent remediation progress |

The probe measures real calls to the demo function. It does not demonstrate a
production service, deployed health endpoint, alerting, availability or SLO.
A failed probe is retained as report-only evidence. Unit tests verify that
unexpected failures and missing input rejection remain visible.

## Completion and closure

1. Retain the successful mainline CI run and its diagnostic artifact after merge.
2. Preserve the recorded role/evidence-scope decision and operating acceptance.
   Keep the architecture evidence at `reviewed` until the fresh initial finding
   and separate personal remediation decision are recorded in the central pilot.
3. After approval and an accepted consumer lifecycle profile, update the evidence
   references/status through a separate change and rerun architecture evaluation.
4. Require a fresh mainline `operation_readiness` PASS after completion of both
   work items. Retain the earlier finding and each decision/progress record.
5. Obtain the separate personal closure decision. A green CI, manual run, technical
   PR merge or another gate's PASS does not close this gate finding.

The other 23 architecture messages remain outside this action. No waiver,
blocking mode, baseline change or existing central lifecycle-state mutation is
part of this preparation.
