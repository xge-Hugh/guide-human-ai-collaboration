# SR-2 — GAMMA-011

**Decision: defer**. Retain as reciprocal observational case; do not fabricate exact pre/post fixture snapshots.

The human edit and read-only inspection are evidenced, but the exact immediate pre/post artifact boundary is not frozen. Neighboring tool outputs also show restored PAYMENT_TERM_TEXT state outside the named CreateField edit. Earlier/later Git commits cannot isolate which changes occurred in the human interval.

Source IDs resolve through [sources.json](sources.json); `Tn:line` means a 1-based JSONL line, `Gn:line` a 1-based historical blob line. This is reviewer material containing future holdouts.

## Last shared state S0

- **S1** Payment-term UI label should display code(description), while the submitted value is code; user approves binding directly to PAYMENT_TERM while preserving non-KR disabled behavior. Evidence: T2:4414, T2:4422. Status: human-provided and acknowledged design. Who knew: human, AI. Uncertainty: none identified for this bounded proposition
- **S2** Agent says it switched binding and removed PAYMENT_TERM_TEXT from schema/refill, with matching contemporaneous search output. Evidence: T2:4430, T2:4439, T2:4443. Status: observed patch/search plus AI-reported completion. Who knew: AI executed/reported, human received report. Uncertainty: Does not establish complete UI correctness or configuration coverage.

## Episode boundary

- **start:** After agent report T2:4443 and before human report T2:4450; exact edit times unknown
- **end:** Human report T2:4450; first captured read outputs at T2:4458-4461
- **settlement:** T2:4450
- **future:** AI inspection T2:4454 onward is the historical recipient response; later closeout T2:4483 onward is a separate broader J

## Event ledger

| Event | Fact and source | Status / artifact visibility / semantic explanation | Current consequence / L | Judgment rationale and uncertainty |
| --- | --- | --- | --- | --- |
| E1 (execution) | Earlier observed field config has PAYMENT_TERM hidden and PAYMENT_TERM_TEXT visible; later read shows PAYMENT_TERM uses getFieldEditProps and TEXT hidden. [T2:4212, T2:4458] | observed / yes / yes | D_now+ / medium | J2: Visibility and editability determine whether the agreed binding is usable. Before excerpt is 02:29Z; human report is 04:01Z. This is not an exact whole-file immediate before snapshot. |
| E2 (execution) | Human states it repaired the forgotten CreateField config and explicitly requires inspection without edits. [T2:4450] | human-provided / partial / yes | D_now+ / high | J2: Supplies attribution, review intent and a no-write boundary that source code cannot encode. Exact full human diff is not captured. |
| E3 (recipient_inspection) | Recipient reads show ApiSelect binding to PAYMENT_TERM and API option mapping label=paymentName(paymentDesc), value=paymentName. [T2:4459-4460] | observed / yes / no | D_now+ / medium | J2: Direct source evidence distinguishes UI label from submitted value. Historical read results establish snippets, not a runtime UI demonstration. |
| E4 (recipient_inspection) | PAYMENT_TERM_TEXT refill and hidden schema are present in post-human reads even though previous agent patch/search reported removal. [T2:4430, T2:4439, T2:4461, T2:4465] | observed / yes / yes | ambiguous / medium | J2: Unexplained adjacent state change prevents clean single-edit attribution and exact snapshot freezing. Could be human restoration, editor undo or concurrent edits; source review does not choose among them. |
| E5 (future_holdout) | AI says residual hidden field is nonblocking; user asks about retaining it and then broader SO closeout. [T2:4468, T2:4475-4484] | AI-reported / partial / yes | ambiguous / medium | J2: A review opinion and later expanded task do not independently prove correctness or initial evidence sufficiency. Do not replace J2 with later whole-header closeout. |

## Downstream judgment J

Check the human patch without changing code and locate the code(description) display mapping; report what source inspection does and does not establish.

Acceptable justified uncertainty:

- Identify binding/label locations and request a complete historical diff before claiming the full human change is safe.
- Flag restored TEXT entries without guessing who restored them.
- Respect no-write scope; do not silently repair.

Evidence threshold: Exact reviewed source snippets plus an attributable before/after artifact boundary are required for a controlled execution replay; UI/tenant correctness needs additional evidence if claimed.

## Return paths R

- T2:4212 pre excerpt; T2:4458-4465 post inspection outputs with call IDs
- G9/G10 historical bracketing commits, expressly not exact snapshots

## Eligibility gate

1. defensible_S0: met for narrow J2
2. bounded_work_interval: partial: bracketed, exact edit state unresolved
3. current_decision_relevant_delta: met at observed-snippet level
4. concrete_J: met
5. evidence_return_paths: partial: snippet returns, full artifact freeze missing
6. historical_artifact_vs_interpretation: unresolved: exact human delta and restored fields
7. future_turn_leakage_control: designable, but no packet eligible

## What would change the decision

- Recover an exact editor/checkpoint snapshot or attributable full diff spanning the human edit, including adjacent schema/refill files.
- If unavailable, keep observational; a deliberately reconstructed snippet fixture must be labeled reconstruction and separately reviewed.

Recovery searches performed:

- Inspected Codex tool-call/output pairs and preceding binding patch/search.
- Inspected local Git history around May 21–25 and the May 23/24 field-file versions.
- Searched Cursor and VS Code local History entries.json for FtsCustomerOrderCreateField; no matching entry located.

## Limits

- No exact human action trace or immediate whole-file snapshots.
- Assistant approval is not independent correctness evidence.
- No build/UI test rerun; current working tree is not substituted for historical evidence.
