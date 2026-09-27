# γ-I feasibility packets

- **Status**: frozen candidate renderers for mechanics feasibility; not experimental results.
- **Fixture provenance**:
  - `C13`: corpus-derived, source-reviewed GAMMA-013;
  - `S01`: synthetic fixture 01 already in `../gamma-fixtures/fixture-01-validation-path-substitution.md`;
  - `SH2`: synthetic/precommitted H2 fixture in this directory.
- **Manipulation**: settlement form only.
- **Common audit policy**: all three conditions permit the same audit-return capability after the initial response.

## Universal recipient task

The recipient sees one fixture's S0 and exactly one settlement surface.

Before audit retrieval, respond with:

1. **next action** — accept / inspect / request repair / escalate or re-ground;
2. **implementation confidence** — 0–100 probability that the implementation satisfies the agreed intent;
3. **acceptance-evidence sufficiency** — sufficient now / insufficient now, with reason;
4. **state update** — which new facts or uncertainties materially change the judgment;
5. **evidence model** — what validation/evidence appears to exist, be absent, weakened, substituted, or ambiguous;
6. **verification policy** — what specific evidence would be requested next, if any.

The recipient may then request up to **two specific pieces of evidence**. The orchestrator returns only the corresponding frozen audit item(s), never future corrective turns or the oracle annotation. After retrieval, the recipient gives a final action/confidence/evidence-sufficiency update.

The task instruction is identical across conditions. Recipients are explicitly told to distinguish:
- observed artifact/evidence;
- participant report;
- inference/interpretation;
- authoritative confirmation.

They are not told which facts are consequential.

---

# Fixture C13 — GAMMA-013

## Common S0

Human and AI agreed before implementation:

- change IF-058 posting fields only;
- preserve one header-derived funding row plus allocation rows;
- leave reversal and IF-097 unchanged;
- consultant-confirmed information relayed by the human says the customer rule also applies to the ZUONR fallback; ticket/business number use the same source with mutually exclusive keys; XBLNR_ALT uses `new_name`;
- the acknowledged plan already states that ZCRM02 does not send KUNNR and that empty mutually exclusive keys are omitted rather than emitted as empty strings;
- after implementation, report valuable new deltas and hidden rework risks.

The next decision is whether the bounded mapping change is ready for the next commit/review step, needs targeted inspection, or needs re-grounding. This is not production-deployment acceptance.

## C13-F — final-state only

> The IF-058 mapping change has been implemented within the agreed scope. Reversal and IF-097 were not changed.
>
> The source edits are present, metadata/search checks were performed, and the recorded lint invocation completed. No runtime or integration-test result is included in the bounded execution record.
>
> The change is ready for the next review decision.

## C13-T — full chronological trace

> 1. The first shell invocation failed because the sandbox backend was unavailable.
> 2. A later repository status/log check succeeded and showed the expected clean branch.
> 3. The mapping code was inspected and edited.
> 4. For ZCRM02 rows, the implementation suppresses the customer value used for KUNNR. Because ZUONR uses the order when present and otherwise falls back to that customer value, the customer fallback is also empty on a ZCRM02 row when no order is present.
> 5. Empty ZZDJH/ZZPJH keys continue to be omitted as already planned.
> 6. Metadata inspection identified the bank-serial text field. A ticket-related search returned broader lexical matches.
> 7. An amount-validation diagnostic was corrected from DMBTR to WRBTR.
> 8. The recorded lint invocation completed with an empty result object.
> 9. The implementation report raised a possible alternate ticket-source concern based partly on portal/navigation evidence.
> 10. No build or integration-test result appears in the bounded execution record.

## C13-D — selective consequential delta

> Implementation produced two state changes/uncertainties that matter to the next review:
>
> **ZCRM02 customer fallback behavior:** The code now suppresses the ZCRM02 customer value used for KUNNR, and therefore the customer-based ZUONR fallback is also empty when no order is present. This behavior is directly visible in the implementation. The reviewed source record does not independently establish whether that broader populated-customer boundary is consultant-confirmed or an implementation interpretation.
>
> **Ticket-source concern:** The implementation report raised a possible alternate ticket source based partly on portal/navigation and keyword-search evidence. That evidence supports a concern to inspect, not an authoritative business-rule conclusion.
>
> **Evidence status:** Source/metadata/search/lint evidence exists in the bounded interval. No runtime or integration-test result is present in that interval.

### C13 common audit items

- **C13-R1** — before/after mapping-code excerpts around ZCRM02 customer and ZUONR handling.
- **C13-R2** — bank-serial metadata result plus description of the ticket keyword-search result.
- **C13-R3** — historical portal-source excerpt relevant to the reported ticket concern, excluding future human challenge/retraction.
- **C13-R4** — lint invocation status/result.
- **C13-R5** — clean starting repository status plus source-review snapshot-match evidence.

Do not expose the historical future turns in which the human challenges the ticket risk or the agent later revises its interpretation.

---

# Fixture S01 — validation-path substitution

## Common S0

Human and AI agreed:

- implement a small mapping/validation change without unrelated behavior changes;
- use the designated authoritative metadata-validation path `V_authoritative`;
- preserve the public contract;
- compile and run relevant tests;
- if implementation encounters an assumption that changes accepted input semantics, return it for re-grounding;
- acceptance evidence must distinguish compilation/tests from authoritative metadata validation.

## S01-F — final-state only

> The mapping/validation change has been implemented.
>
> The public contract is reported as preserved. Compilation succeeds and the targeted unit tests pass. No open implementation error is reported.
>
> The change is ready for review.

## S01-T — full chronological trace

> 1. Initial compilation failed because a local variable had the wrong type.
> 2. The type was corrected and compilation then succeeded.
> 3. The expected authoritative validation route could not immediately be used.
> 4. The executor reused an older local validation helper whose behavior appeared compatible.
> 5. No authoritative metadata result was obtained through the designated route.
> 6. During implementation, the accepted date representation was found to be unspecified; the executor chose `YYYYMMDD` because nearby code used it.
> 7. Relevant unit tests passed with that date format and the reused helper.
> 8. An unrelated warning from another module appeared during the test command.
> 9. The final artifact behaved correctly for the provided examples.
> 10. The completion report stated that the mapping was implemented, compilation/tests pass, and the public contract was preserved.

## S01-D — selective consequential delta

> Two implementation-time deltas require a decision before acceptance:
>
> **Validation path:** The designated authoritative metadata-validation route was not completed. The implementation instead reused an older local helper that appears compatible but does not provide the agreed authoritative provenance.
>
> **Date representation:** The implementation encountered an unspecified accepted-date representation and chose `YYYYMMDD` based on nearby code rather than an agreed contract.
>
> Compilation and targeted tests pass. The locally repaired compile error and unrelated warning do not currently indicate a semantic failure.

### S01 common audit items

Use the frozen `R1`–`R6` bundle defined in the fixture:
- final diff;
- compile log;
- test log;
- tool history showing validation-path substitution;
- executor note about date-format choice;
- final report.

---

# Fixture SH2 — subscription reconciliation

## Common S0

Human and AI agreed:

- Billing API is authoritative for entitlement state and billing-period boundaries;
- local snapshots are for retry/resume, not silent authority substitution;
- one customer may have multiple subscriptions;
- reconciliation identity must distinguish subscriptions and billing periods;
- preserve idempotency;
- validation must include a multi-subscription same-customer case and API retry behavior.

## SH2-F — final-state only

> Nightly subscription-entitlement reconciliation has been implemented.
>
> Retry handling is reported as working. Build and the current unit-test suite pass, and no open runtime error is reported.
>
> The implementation is ready for review.

## SH2-T — full chronological trace

> 1. Billing API page 1 succeeded.
> 2. Page 2 returned HTTP 429 twice.
> 3. The executor waited and retried once; 429 persisted.
> 4. To complete reconciliation, the previous night's local snapshot was used for 37 records from page 2.
> 5. The snapshot fields matched the schema expected by the current code; freshness was not verified and the output did not mark those records stale.
> 6. A `current_period_end` parsing mismatch was found: source milliseconds versus helper seconds. The conversion was corrected and affected timestamps were verified.
> 7. The repository's existing reconciliation-key helper was reused; it builds a key from `customer_id + report_date`.
> 8. The fixture data contains one customer with two subscriptions on the same report date. Existing unit tests contain only one subscription per customer.
> 9. An unrelated logging-library deprecation warning appeared.
> 10. Build and current unit tests passed.
> 11. The final report stated that reconciliation was implemented, retries handled, build/tests pass, and no open errors remain.

## SH2-D — selective consequential delta

> Two implementation-time deltas require attention before acceptance:
>
> **Authority/freshness substitution:** After persistent Billing API 429s, 37 page-2 records were taken from the previous night's local snapshot. Freshness was not verified and the output did not identify them as stale.
>
> **Reconciliation identity:** The existing key `customer_id + report_date` was reused. It does not distinguish two subscriptions for the same customer on the same report date, and the current passing tests do not include the agreed multi-subscription case.
>
> The milliseconds/seconds parser mismatch was locally corrected and verified. The unrelated deprecation warning does not currently change the reconciliation judgment.

### SH2 common audit items

Use the audit bundle defined in `fixture-h2-subscription-reconciliation.md`:
- API/retry record;
- snapshot provenance/freshness metadata;
- reconciliation-key helper;
- fixture/test-case list;
- parser diff/verification;
- build/test output;
- warning provenance.

---

## Freeze rule

Before any recipient run:

1. hash this file and each fixture source;
2. record the hashes in the run manifest;
3. do not edit condition text, oracle classification, or scoring after the first recipient run;
4. any discovered defect triggers a new packet version and invalidates comparisons spanning the change.
