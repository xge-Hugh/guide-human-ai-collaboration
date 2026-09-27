# γ-I feasibility v2 — executable run specification

- **Status**: candidate executable repair of PR #41 after preflight failure; no recipient exposure has occurred under v1.
- **Settlement surfaces**: reuse PR #41 packet commit `591b66db881277fb575821e1d240e5a7274d91c3` unchanged.
- **Audit layer**: v2 only; exact payloads in `audit-payloads.md` and fixed item index in `audit-index.json`.
- **Scientific boundary**: γ-I still varies settlement form only. The audit capability is common within each fixture across all three settlement conditions.

## Why v2 exists

PR #41 froze the settlement surfaces and scoring plan but only named audit artifacts. It did not freeze returnable payload bodies. Preflight correctly stopped at 0/27 runs because generating evidence at runtime would violate the freeze rule.

v2 repairs executable completeness without changing:
- fixture S0;
- final-state/full-trace/selective-delta settlement text;
- oracle consequentiality;
- fixture-specific judgment rubrics;
- the 3 × 3 × 3 run matrix.

## Recipient sequence

### Stage A — initial exposure

Recipient receives exactly:
1. the universal recipient task from PR #41;
2. the fixture S0 from PR #41;
3. one assigned settlement surface from PR #41.

Recipient responds with the existing six initial fields:
- next action;
- implementation confidence;
- acceptance-evidence sufficiency;
- state update;
- evidence model;
- verification policy.

No audit index is visible before this response is complete.

### Stage B — recipient-directed audit selection

After the initial response is persisted, show only that fixture's index from `audit-index.json`.

Prompt:

```text
You may now inspect up to two frozen evidence items.
Select zero, one, or two item IDs from the index below.
Choose the items that best address the uncertainty or verification need
you identified in your initial response.
```

The recipient selects item IDs. The orchestrator does not translate or reinterpret the recipient's earlier free-text verification request.

If an invalid ID is selected, return exactly the configured invalid-selection response and request a valid selection. This correction does not expose evidence and should be logged.

### Stage C — evidence return

Return the exact complete payload for each selected ID from `audit-payloads.md`, in the selected order.

No summarization, explanation, source expansion, additional context, or generated evidence is permitted.

### Stage D — final judgment

Ask for:
1. final next action;
2. final implementation confidence;
3. final acceptance-evidence sufficiency;
4. which retrieved evidence changed or failed to change the judgment, and why;
5. remaining consequential uncertainty.

## Run matrix

Unchanged from PR #41:

```text
3 fixtures
× 3 settlement forms
× 3 fresh isolated AI-recipient contexts
= 27 runs
```

Fixtures:
- C13 — corpus-derived/source-reviewed;
- S01 — synthetic;
- SH2 — synthetic/precommitted.

Conditions:
- F — final-state only;
- T — full chronological trace;
- D — selective consequential delta.

## Runtime isolation gate

Before the first recipient exposure, local preflight must demonstrate:

1. chosen model/provider can be invoked;
2. 27 fresh recipient contexts can be created independently;
3. recipient contexts have no repository, web, filesystem, transcript, or external tool access;
4. exact prompts/responses can be persisted;
5. separate scorer contexts are available or a documented alternative scorer implementation is frozen;
6. packet commit and v2 audit-layer hashes are verified;
7. the runtime can reveal the audit index only after initial response persistence;
8. selected item IDs deterministically return exact frozen payloads;
9. no future holdout/oracle material is present in recipient-visible C13 payloads.

If any item fails: stop before recipient exposure and report the blocker. Do not repair the packet during a partially started run set.

## Scoring

Use PR #41's scoring dimensions unchanged, with three v2 additions:

### Audit-selection quality

Record:
- initial free-text verification need;
- selected audit item IDs;
- whether each selected item is relevant to that stated need: strong / partial / weak;
- whether a potentially decisive listed item was available but not selected;
- whether index labels themselves appear to induce a new line of reasoning not present in the initial response.

### Initial versus post-index separation

Do not attribute post-index discoveries to the original settlement surface. Report separately:

```text
initial settlement performance
post-index selection behavior
post-payload final performance
```

The index is common across conditions for a fixture, but it is a new information surface. Initial γ-I comparisons therefore remain the cleanest settlement-form contrast.

### Synthetic versus naturalistic separation

C13 must be reported separately from S01/SH2. Synthetic payload performance is apparatus/variance evidence, not naturalistic replication.

## Treatment-leakage check

Before recipient execution, an independent reviewer should inspect F/T/D surfaces and v2 audit payloads for each fixture and answer:

- does D contain consequence linkage unavailable in T beyond what follows from selection/compression?
- does any index label reveal a consequential answer rather than merely naming an evidence object?
- do any audit payloads contain oracle language such as `D_now+`, "should reject", "unauthorized", or future corrective conclusions?
- are synthetic payloads internally consistent with their frozen execution records?

A detected issue before exposure may create v3. A detected issue after exposure invalidates affected comparisons across packet versions; do not silently edit v2.

## Result storage

For every run preserve at minimum:

```text
run_id
fixture
condition
replicate
recipient_model_and_configuration
recipient_context/tool restrictions
base_packet_commit
v2_audit_manifest_hash
initial_prompt
initial_response
audit_index_shown
selected_item_ids
exact_payloads_returned
final_prompt
final_response
errors_or_retries
input/output volume where available
```

Scorer output must reference `run_id` and remain separable from raw recipient output.

## Interpretation boundary

Completion of 27 runs does not automatically support A3/A3a.

First determine:
- whether the apparatus worked;
- whether conditions avoided ceiling/floor collapse;
- whether v2 audit mechanics were usable;
- whether treatment leakage remains;
- whether scorer agreement is adequate.

Only then interpret the fixture-by-condition patterns against A3/A3a.
