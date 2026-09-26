# Experiment γ — source-review gate after local corpus mining

- **Date**: 2026-09-27
- **Status**: research handoff / source-review gate; not results; not specification authority.
- **Input**: local-agent candidate registry `gamma-candidates-2026-09-27/`.
- **Governing protocol**: `gamma-bidirectional-state-settlement-protocol-2026-09-16.md`.

## 1. Reconciliation with the calibrated protocol

The local-agent replay outline is valuable as corpus discovery, but its six-condition table reflects the older flat γ sketch.

The current calibrated protocol takes precedence:

```text
γ-I   settlement form
      final-state only
      vs full trace
      vs selective consequential delta
      [common audit return path]

γ-II  evidence-access architecture
      surface only
      vs direct shared artifacts
      vs indexed/on-demand retrieval
      [semantic delta held constant]

γ-III selector stress
      oracle-selected
      vs executor-selected without audit
      vs executor-selected with audit
      [conditional on γ-I]
```

Do not construct one six-way "winner" comparison. Source review should first produce fixtures usable by γ-I.

Pilot H3 also showed that selective settlement can accidentally bundle:
- fact selection;
- consequence linkage;
- verification guidance.

A γ-I fixture/renderer must either hold consequence-linkage and verification affordances comparable across conditions or explicitly record them as an additional manipulation.

## 2. First source-review set

### SR-1 — GAMMA-013: implementation delta and provenance boundary
**Direction:** AI executor → human recipient.  
**Use:** primary γ-I candidate.

Why selected:
- bounded implementation handoff;
- explicit request for valuable implementation deltas;
- visible human reaction to provenance/inference distinctions;
- contains a reported concern that was later retracted, useful for calibration.

Important confound:
- delta reporting was explicitly prompted. This case cannot establish spontaneous selector behavior.

Required source review:
1. recover the last shared state before implementation;
2. identify which empty-customer behavior was already grounded versus inferred during implementation;
3. inspect the historical implementation artifact and tool outcomes;
4. preserve the later retracted ticket/navigation concern as a potentially mistaken executor interpretation rather than oracle truth;
5. identify the minimum downstream decision the human needed to make at the settlement point;
6. withhold future corrective turns from replay recipients.

### SR-2 — GAMMA-011: human patch and read-only reconciliation
**Direction:** human executor → AI recipient.  
**Use:** primary reciprocal γ-I candidate.

Why selected:
- actual human artifact modification;
- subsequent AI inspection rather than another implementation pass;
- potentially clean separation between artifact-recoverable state and human semantic intent.

Required source review:
1. freeze the exact historical artifact version before and after the human edit;
2. identify what the human changed and why;
3. separate facts directly recoverable from code from semantic intent supplied only by the human;
4. inspect actual read/search/tool outcomes used by the AI;
5. identify the next review decision and what evidence would justify moving on;
6. do not treat assistant approval as independent correctness evidence.

### SR-3 — GAMMA-007: completion report to review-gap recovery
**Direction:** AI executor → human recipient → AI.  
**Use:** secondary γ-I candidate; possible later γ-II artifact case.

Why selected:
- completion/PR report followed by human requests for package placement and stale-code inspection;
- can test whether final-state reporting omitted state needed for actual review;
- artifacts appear to contain at least some recoverable evidence.

Required source review:
1. recover the original completion report and preceding implementation scope;
2. determine whether the later human questions were already implied by the agreed review responsibility or were genuinely new goals;
3. inspect diff/search evidence for the stale elements;
4. identify which facts were available in artifacts but not usable from the report;
5. exclude repeated requests in the same cluster from independent sample counts.

## 3. Diagnostic / deferred cases

### GAMMA-014 — evidence-selection diagnostic
Keep as a diagnostic case for **consequence linkage / evidence selection**. It is a research-to-decision handoff before completed implementation, so do not count it as a clean post-execution γ fixture unless the experimental question is explicitly broadened.

### GAMMA-016 / GAMMA-017 — linked failure/recovery cluster
Review jointly, not as independent replications. They may be strong field evidence for:
- shared artifact access not guaranteeing understanding;
- human source inspection revealing omitted state;
- long reports exceeding actual recipient assimilation.

Use them to refine moderators and failure modes before turning them into replay fixtures.

### GAMMA-006 — selector-stress candidate
Potentially valuable for γ-III because a causal explanation omitted a human-held constraint. Keep observational until the underlying capture evidence and root cause can be independently reconstructed.

### GAMMA-009 / 010 — addressability boundary
More naturally relevant to γ-II/A14 than γ-I. Defer until settlement-form feasibility is established.

## 4. Source-review fact ledger

For each selected case, produce a ledger before any condition packet is rendered.

```text
case_id
source_snapshot
S0:
  proposition
  evidence that it was shared/grounded
  who knew it
  epistemic status

execution_event:
  event_id
  fact
  source address
  status:
    observed
    human-provided
    AI-reported
    inferred
    consultant/external-confirmed
    disputed
    withdrawn
    unknown
  artifact_visible: yes/no/partial
  semantic explanation needed: yes/no/uncertain

classification:
  D_now+ / D_now0 / ambiguous
  L: none/low/medium/high/unknown
  affected downstream judgment
  rationale
  annotator uncertainty

J:
  bounded next-action judgment
  acceptable justified-uncertainty responses
  evidence threshold

R:
  authoritative return paths
  historical artifact/tool-output addresses
```

Do not convert later agreement, final success, or assistant confidence into ground truth.

## 5. Eligibility gate

A case is **include** only when all of the following are reasonably reconstructable:

1. a defensible pre-work `S0`;
2. a bounded local-work interval;
3. at least one state change whose current-decision relevance can be argued from sources;
4. a concrete downstream judgment `J`;
5. evidence return paths `R`;
6. enough historical source material to distinguish artifact state from interpretation;
7. no future-turn answer leakage in the initial replay packet.

Use **defer** when the phenomenon is promising but one of these is unresolved.  
Use **exclude** when the case depends mainly on retrospective story, unverified agent claims, or a new goal rather than state settlement.

Every include/defer/exclude decision needs a reason.

## 6. First replay after source review: γ-I only

After at least three fixtures pass the source-review gate, run γ-I first.

For each frozen fixture, generate:

1. **final-state-only**;
2. **full chronological trace**;
3. **selective consequential delta**.

All three must have the same permitted audit return path.

The renderer must not use future recipient reactions to optimize condition 3. Freeze the selector output before recipient evaluation.

Because the original human already knows many corpus episodes, do not treat replay to that same human as uncontaminated comparative evidence. Human replay can still test usability. For AI-recipient feasibility, use fresh isolated contexts per fixture/condition and record model/tool state.

## 7. Scoring additions from H1–H3 calibration

Keep separate:

- **implementation confidence**: probability the result actually satisfies intent;
- **acceptance-evidence sufficiency**: whether available evidence is enough to accept now.

Also score:

- recognition of each `D_now+`;
- false elevation of `D_now0`;
- whether the recipient links the fact to the correct threatened invariant;
- quality of the verification policy;
- evidence actually retrieved;
- unjustified confidence;
- source/provenance mistakes;
- recipient information volume and clarification actions.

Record longitudinal value `L` separately. An event can be noncritical now while still helping future model formation.

## 8. What the corpus currently establishes — and does not

The local mining establishes that there are multiple plausible naturally occurring state-settlement episodes across both directions and several mechanisms: reports, artifact inspection, screenshots/logs, retrieval addresses, corrections, and human selective externalization.

It does **not** yet establish comparative treatment effects, prevalence in the full corpus, selector accuracy, action-sufficient alignment time, or support for A3a/A3b/A10/A12/A14.

Those claims remain pending source review and controlled replay.
