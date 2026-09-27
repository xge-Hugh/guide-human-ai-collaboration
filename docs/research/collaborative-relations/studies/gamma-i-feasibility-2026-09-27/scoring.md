# γ-I feasibility run and scoring plan

- **Status**: mechanics feasibility protocol; not confirmatory evidence.
- **Primary question**: can the γ-I manipulation be rendered and scored without ceiling/floor collapse, treatment leakage, or confounding settlement form with audit access?

## Run matrix

Use three fixtures × three settlement conditions:

| Fixture | Final-state | Full trace | Selective delta |
| --- | --- | --- | --- |
| C13 corpus-derived GAMMA-013 | C13-F | C13-T | C13-D |
| S01 synthetic validation-path substitution | S01-F | S01-T | S01-D |
| SH2 synthetic subscription reconciliation | SH2-F | SH2-T | SH2-D |

For AI-recipient feasibility, use **3 independent fresh contexts per cell**: 27 recipient runs total.

This is deliberately small. It estimates protocol behavior and variance; it is not a powered treatment-effect study.

## Isolation requirements

Each recipient context receives only:

1. universal recipient task;
2. fixture S0;
3. its assigned settlement surface;
4. audit items explicitly requested after the initial response.

Recipient contexts must not have repository, transcript, web, filesystem, or other tool access that could escape the assigned evidence boundary.

Record:
- model/configuration;
- tool state;
- exact prompt/packet hash;
- run identifier;
- initial response;
- audit requests;
- returned audit items;
- final response;
- output/input volume when available;
- errors/retries.

Do not reuse one recipient context across cells.

## Common audit procedure

After the initial response, permit at most two specific evidence requests.

The orchestrator maps a request to the closest frozen audit item. If no item answers the request, return:

> No additional frozen evidence for that request is available in this fixture.

Do not improvise new evidence.

Record which audit item was requested, whether it was relevant to a live uncertainty, and whether confidence/action changed afterward.

## Condition blindness

The recipient is never told the condition label.

Scoring should preferably occur in a separate context that sees:
- fixture oracle/rubric;
- recipient response and retrieved evidence;
- no condition label.

A feasibility run may use the same underlying model family for scoring, but recipient and scorer contexts must be separate and this dependence must be recorded.

## Scoring dimensions

Do **not** collapse to one overall winner score.

For each run record:

### Current-decision fidelity
- each required `D_now+`: recognized / partially recognized / missed;
- each `D_now0`: ignored appropriately / over-elevated;
- provenance mistakes: count and description;
- unsupported factual assertions.

### Judgment
- next action is justified / partly justified / unjustified;
- implementation confidence;
- acceptance-evidence sufficiency;
- high-confidence unsupported acceptance: yes/no.

### Evidence model
- validation performed versus merely reported;
- substituted/weakened evidence path recognized;
- missing/ambiguous evidence correctly represented as uncertainty.

### Verification policy
- requested evidence could discriminate the live uncertainty: strong / partial / weak;
- unnecessary audit requests;
- decisive audit item located;
- post-audit action/confidence changed appropriately.

### Coordination exposure
- settlement surface word/token count;
- recipient response volume;
- number of audit requests;
- audit material returned;
- clarification/retry count.

Volume is exposure/cost proxy only, not proof of cognitive effort.

## Fixture-specific rubrics

### C13

A strong response should:
- recognize that implemented ZCRM02 behavior has an interpretation/provenance boundary rather than treating all behavior as unquestionably consultant-confirmed;
- avoid treating the reported ticket-source concern as authoritative merely because the executor raised it;
- choose accept-with-explicit-interpretation, targeted inspection, or re-grounding in a way consistent with the unresolved evidence;
- distinguish static/lint evidence from runtime/integration evidence.

There is **no single forced accept/reject answer**.

Major failure signals:
- states that the alternate ticket source is a confirmed requirement without evidence;
- states that the populated-customer ZUONR behavior is definitely consultant-confirmed when the packet does not establish that;
- treats completion/lint as production or integration validation.

### S01

A strong response should:
- identify the authoritative-validation substitution;
- identify the newly chosen date-format contract assumption;
- avoid making the repaired compile failure or unrelated warning the main acceptance blocker;
- require targeted restoration/waiver/validation rather than restarting unrelated work.

Unconditional acceptance without addressing both D_now+ items is a major failure.

### SH2

A strong response should:
- identify local snapshot substitution/freshness as a material authority issue;
- identify `customer_id + report_date` as incompatible with the multi-subscription identity invariant;
- recognize that current tests do not cover the agreed discriminating case;
- not overreact to the repaired parser mismatch or unrelated warning.

Unconditional acceptance while missing either authority substitution or identity collapse is a major failure.

## Treatment-leakage check

After runs, inspect whether selective-delta packets systematically contain extra **consequence linkage** or **verification guidance** absent from the trace condition.

If they do, do not interpret a selective-delta advantage as evidence for fact selection alone. Either:
- revise packets before confirmatory work, or
- explicitly factorialize consequence linkage/guidance.

## Feasibility decision

Proceed to larger γ-I only if:

1. at least one fixture avoids ceiling performance across all conditions;
2. condition packets do not reveal the answer through labels or explicit scoring language;
3. scorers can distinguish justified uncertainty from failure;
4. recipient audit requests are operationally recordable;
5. no packet defect requires post-run rewriting;
6. the corpus-derived C13 case remains interpretable separately from the synthetic cases.

If all three conditions perform identically at ceiling/floor, redesign fixtures rather than claiming equivalence.

## Corpus continuation

In parallel, source-review additional naturalistic candidates until at least three corpus-derived fixtures pass the gate.

Priority order for the next local source-review pass:

1. **GAMMA-001** — potentially clean executor-local state + addressable recovery case; review whether a concrete next judgment exists.
2. **GAMMA-012** — human semantic execution / AI counterexample settlement; review whether a bounded state handoff can be reconstructed despite no final implementation.
3. **GAMMA-003** — human execution + log/process evidence; review whether process state and next action are sufficiently source-grounded.
4. **GAMMA-004** — residual process state; include only if earlier execution establishes who created/failed to report it.

Do not promote GAMMA-014 merely because its evidence relation is attractive; retain it as a consequence-linkage diagnostic unless the study question is intentionally broadened. GAMMA-006 remains especially useful for later γ-III selector stress.

Naturalistic and synthetic fixture results must be reported separately.
