# γ-0A Pilot H2 — full-trace calibration

- **Status**: protocol calibration; not confirmatory evidence.
- **Recipient**: human collaborator.
- **Condition**: γ-I full chronological trace.
- **Precommitment**: hidden oracle text was frozen before exposure; SHA-256 `8b02b8b8d2e35f64bdad3d13c97027b1b4927977808e55c206a246682914a111`.

## Frozen consequential structure

The oracle contained two current-acceptance consequential deltas:

1. **authority/freshness substitution** — after repeated Billing API 429s, 37 records were taken from the previous night's local snapshot without staleness marking or authoritative refresh;
2. **identity/idempotency mismatch** — an existing helper keyed reconciliation by `customer_id + report_date`, while the grounded invariant required distinguishing subscription and billing period; fixture data contained two subscriptions for one customer, and existing tests covered only one subscription per customer.

The oracle marked the repaired millisecond/second parser mismatch and unrelated logging deprecation warning as non-decision-critical for current acceptance.

## Human recipient observation

The recipient:

- correctly identified the authoritative-API fallback as consequential and connected it to the prior invariant against silent authority substitution;
- proposed targeted inquiry into why the fallback occurred, its purpose, and its risks;
- treated the parser mismatch as not necessarily acceptance-blocking but extracted model/learning value from it, generalizing toward explicit contract-assumption validation and stronger external evidence;
- inspected the existing helper from an architectural/reuse perspective but did **not explicitly derive the concrete semantic correctness failure** that `customer_id + report_date` can collapse two subscriptions despite the full trace containing the necessary clues;
- correctly treated generic unit-test success as weak evidence when agreed case coverage was not exposed;
- largely discounted the unrelated warning/build-success tail.

No numeric confidence or explicit final action was supplied, so calibration cannot be scored quantitatively for this pilot.

## Protocol findings

### P1 — full trace can preserve facts while still imposing selector burden

The recipient detected D+1 but missed the more structurally embedded D+2. This is compatible with, but does not establish, the hypothesis that chronological transparency can leave consequentiality inference to the recipient.

### P2 — binary consequential / noise annotation is too coarse

The parser event was non-decision-critical for the immediate acceptance judgment yet carried longitudinal model value for the human. Future oracle annotation should distinguish at least:

- **current-decision consequence**: could this change accept/inspect/repair/escalate now?
- **longitudinal model/capability value**: could this low-cost exposure improve future prediction, contract checking, or delegation?

An event can be low on the first dimension and nonzero on the second.

### P3 — evidence-result statements need coverage semantics

`tests passed` is not equivalent to `the agreed discriminating cases were tested`. γ scoring should distinguish:

- test execution success;
- evidence coverage of the grounded invariant;
- authoritative provenance of the evidence.

### P4 — recipient review scope needs separation

The human naturally reviewed both:
1. **intent/invariant satisfaction**, and
2. **broader engineering quality** such as helper placement, reuse, naming, and architecture.

γ's primary outcome should score (1). Broader engineering-quality observations may be preserved as secondary naturalistic behavior rather than treated as settlement errors.

## Interpretation boundary

One replay cannot compare full trace against selective delta because the same human cannot be reset to an uncontaminated state for the same fixture. H2 is therefore useful for instrument/protocol calibration and for generating hypotheses about selector burden, not for estimating a treatment effect.
