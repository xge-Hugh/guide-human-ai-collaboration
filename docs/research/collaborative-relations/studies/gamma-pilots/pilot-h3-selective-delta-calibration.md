# γ-0A Pilot H3 — selective-delta calibration

- **Status**: protocol calibration; not confirmatory evidence.
- **Recipient**: human collaborator.
- **Condition**: γ-I selective consequential delta.
- **Precommitment**: hidden oracle was frozen before exposure; SHA-256 `b9ff491f1f5efe428da46f9336bf6ad866f20d2bbd698d44dce728c2f42676e3`.

## Frozen oracle summary

Current-decision consequential deltas:

1. a legacy provider event lacked `provider_event_id`; executor invented `sha256(payload)` as fallback identity without re-grounding, changing deduplication semantics;
2. existing persistence uniqueness used only `provider_event_id`, violating the agreed `tenant_id + provider_event_id` identity and lacking the agreed cross-tenant same-ID test.

Current-decision noncritical events included a repaired compile issue and unrelated linter warning. The missing-ID provider edge also carried longitudinal model value for future contract checks.

## Human recipient observation

The recipient:

- identified both surfaced findings as conflicting with the grounded invariants;
- assigned implementation confidence of about 60%;
- treated evidence as insufficient for acceptance;
- proposed inspecting the sandbox sample and its authority, re-grounding missing-ID behavior, and deciding explicitly whether to reject/error or adopt an authoritative fallback;
- recognized the persistence-identity problem and considered whether the database/index design must change;
- generalized beyond passive receipt of the report into an active verification strategy: inspect diffs/shared artifacts, ask for a reading order, use another AI/expert for review, or search unfamiliar concepts;
- emphasized a sense of control from choosing evidence to inspect and actively constructing questions.

## Calibration findings

### P1 — selective delta reduced immediate selection burden in this fixture

Both current-decision deltas were recognized without the recipient having to infer them from unrelated chronological noise. This is compatible with A3a but is not a treatment estimate because H2/H3 use different fixtures.

### P2 — selective delta representation currently bundles two mechanisms

The H3 surface did not only select facts. It also linked each fact to the violated invariant and, implicitly or explicitly, to what should be checked before acceptance.

Future γ-I must distinguish:

- **delta fact selection**: which new facts are surfaced;
- **consequence linkage**: why a fact matters to the grounded intent/evidence threshold;
- **verification guidance**: what evidence/action could resolve the uncertainty.

Otherwise a selective-delta condition may win because it receives stronger reasoning support, not because selection itself is superior.

### P3 — recipient-directed verification is a distinct coordination operation

After receiving a settlement surface, the human forms an evidence-acquisition policy:

```text
settlement surface
→ identify uncertainty / threatened invariant
→ choose evidence source or reviewer
→ inspect / query / search
→ update confidence and next action
```

This should be measured as part of γ rather than assuming settlement is complete when information is delivered.

Candidate observable properties include:

- whether the recipient asks for evidence that can actually discriminate the live uncertainty;
- unnecessary evidence opened;
- time/actions to reach a justified decision;
- whether a requested second reviewer receives enough independent source access.

### P4 — the selector problem is symmetric

Executor-side selection can omit consequential evidence, but recipient-side selection can also create a bottleneck. If the human forwards only a self-selected subset to another AI/expert, the reviewer may inherit the human's omission or framing.

Therefore independent review value depends on the reviewer's return path to source evidence, not only on the recipient's curated summary.

### P5 — recipient capability is a moderator, not background noise

H2 suggested that full trace can contain enough information while the recipient still fails to derive the consequential relation. H3 and the human reflection suggest at least three possible supports:

- consequence-linked semantic guidance;
- better verification methodology / prompting questions;
- domain/representation competence developed over time.

γ should measure these as context/moderators rather than assume a generic fully competent selector/understander.

## Interpretation boundary

H3 does not establish selective-delta superiority. It supports protocol refinement and provides a contrastive observation against H2. A clean causal comparison still requires different recipients (or uncontaminated fixture assignment) across conditions with equivalent consequence-linkage and verification affordances.
