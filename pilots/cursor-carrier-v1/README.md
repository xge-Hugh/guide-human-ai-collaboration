# Cursor Human–AI Collaboration Carrier v1.1

> Status: **experimental pilot carrier** for Issue #31. This directory is not a normative source and does not replace `docs/spec/`.
>
> Revision: **2026-09-16 research-informed pilot**. Research baseline: remote `main` at `62d3b6dff2f5112f35513cfc63fa18f06075347b`, verified on 2026-09-16. The directory remains `cursor-carrier-v1` for installation continuity.
>
> Primary host: **Cursor Agent (Chat)**.
>
> Purpose: field-test a small executable projection of current project semantics plus selected cognitive-coordination candidates during ordinary cross-project work.

## Architecture

```text
Cursor User Rule
  ├─ K1 collaboration-state integrity
  ├─ K2 epistemic integrity
  ├─ K3 substantive human responsibility
  └─ proportionality / no-op boundary

conditionally discovered Agent Skills
  ├─ human-ai-model-coordination
  │    ├─ action-sufficient alignment / discrimination
  │    ├─ selective cross-level epistemic probing
  │    ├─ strategic substrate contact / concept connections
  │    ├─ consequential post-delegation delta
  │    ├─ revision / selective revalidation
  │    └─ productive divergence
  │
  └─ human-ai-reconstruction
       ├─ minimum sufficient reconstruction set
       ├─ human-facing reactivation / usable reasoning and retrieval cues
       └─ optional low-cost return cue at observable open loops
```

The split is based on runtime activation conditions, not on a desire to maximize Skill count.

- **Model coordination** activates when a consequential model relation or evidence basis needs repair, including changes discovered during delegation, or when a live task supports a useful concept connection. Ordinary completion reporting stays in the kernel; it does not require loading a Skill.
- **Human reconstruction** activates when previously established reasoning must become usable again, or when an observable interruption/open loop makes a cheap return cue valuable.
- Either Skill may be inactive. No intervention is a valid outcome.

## Files

- `cursor-user-rule.md` — exact source for the user-level resident kernel.
- `skills/human-ai-model-coordination/SKILL.md` — conditional E1 treatment, including E2/E4 operations.
- `skills/human-ai-reconstruction/SKILL.md` — conditional E3 human reconstruction treatment.
- `evals/cases.json` — discriminating activation and behavior cases for manual review or later runner adaptation.
- [`field-evaluation.md`](field-evaluation.md) — optional observation record, comparison procedure, and research return path.

## Semantic sources

This carrier was re-derived from current project material rather than patched from the previous Skill:

- `docs/spec/norms.md`
- `docs/spec/model.md`
- `docs/spec/adaptation.md`
- `docs/spec/evaluation.md`
- `docs/spec/failure-models.md`
- `docs/governance/evidence-policy.md`
- `docs/research/cognitive-coordination/model.md`
- `docs/research/cognitive-coordination/studies/cross-level-epistemic-probing-replay-2026-08-30.md`
- `docs/research/cognitive-coordination/studies/reconstruction-surface-cloud-review-2026-08-27.md`
- Issue #31 and the recovered implementation-authorization failure recorded in project feedback.

Research candidates remain candidates when made executable here. Carrier structure does not promote them to normative truth. This revision implements the user-requested experimental update; the studies alone did not authorize deployment or establish effectiveness.

## Research-to-carrier decisions

| Research source | Pilot treatment | Discriminating observation |
| --- | --- | --- |
| [Action-sufficient alignment and epistemic delta](../../docs/research/cognitive-coordination/studies/action-sufficient-alignment-and-epistemic-delta-2026-09-10.md) | Stop grounding at the relevant action boundary; report consequential new evidence after delegation | Fewer redundant questions without hidden assumptions or validation substitutions |
| [Progressive schema formation](../../docs/research/cognitive-coordination/studies/progressive-schema-formation-through-strategic-exposure-2026-09-11.md) | Brief task-grounded seeds; respond to human connections; restore partial concepts through live evidence | Later recognition, prediction, or useful reuse versus distraction or false confidence |
| [Collaborative relations model](../../docs/research/collaborative-relations/model.md) and [claim ledger](../../docs/research/collaborative-relations/claim-ledger.md) | Consider responsibility, independent signal, selector reliability, and recipient review cost | Inspectable omissions, meaningful review, and reduced compensatory labor; A2–A5, A8–A13 |
| [Cognitive placement](../../docs/research/collaborative-relations/studies/cognitive-placement-bridge-2026-09-15.md) | Small resident recognition cues; restore reasoning when a link is insufficient; retrieve volatile details | Missed/false routing, lookup cost, stale evidence, and recovery when retrieval fails; A14–A17 |
| [Static context carrier gap](../../docs/research/runtime-capability/design-diagnoses/static-context-carrier-gap.md) | Retain two Skills; add targeted canonical return paths and record loading conditions | Distinguish available instructions, actual loading, behavior, and human correction |

The relational dimensions are design discriminators, not runtime profile fields or a required questionnaire. This revision does not implement a universal memory architecture or assume the static-carrier reliability gap has been solved. Temporal waiting/rejoin mechanisms remain separate research probes; this carrier does not add a scheduler.

For a task that needs deeper project-specific interpretation, optionally read only the relevant source above from an available checkout. The Skills also include pinned source links for installations outside this repository. Record such orientation separately from automatic Skill loading. Do not read the whole corpus before routine tasks or claim unavailable sources were consulted.

## Install in Cursor

### 1. Install the resident User Rule

In Cursor:

1. Open **Customize** in the sidebar.
2. Open **Rules**.
3. Add the contents of `cursor-user-rule.md` as a **User Rule**.

User Rules apply to Cursor Agent Chat across projects and sync with the Cursor account.

### 2. Install the two user-level Skills

Copy these two directories:

```text
pilots/cursor-carrier-v1/skills/human-ai-model-coordination
pilots/cursor-carrier-v1/skills/human-ai-reconstruction
```

into:

```text
~/.cursor/skills/
```

Result:

```text
~/.cursor/skills/
  human-ai-model-coordination/
    SKILL.md
  human-ai-reconstruction/
    SKILL.md
```

Cursor discovers user-level Skills from the local machine and decides relevance from each Skill description and current context.

After installation, check **Customize → Skills** and confirm both Skills are discoverable.

For an existing v1 installation, replace the existing User Rule and both same-named Skill directories; do not append a second rule or install duplicate Skills. Record the installed source commit and any local edits, plus the host/model where available. Keep the previous version if a field comparison or rollback is needed. Repository edits alone do not update Cursor's stored User Rule or local installations.

## Host boundaries

This pilot deliberately accepts the following Cursor constraints:

- User Rules affect **Agent Chat**, not Cursor Tab or Inline Edit.
- Rule precedence is **Team Rules → Project Rules → User Rules**. A conflicting higher-precedence rule may override this experimental kernel.
- User-level Skills under `~/.cursor/skills/` are local to the machine where Agent runs. They are not automatically copied to Cloud Agents, remote SSH Agent sessions, or other workers.
- Skill routing is model-mediated. A Skill can under-trigger or over-trigger; routing quality is part of the experiment.
- The carrier cannot directly observe a human's private cognitive state or reliably infer unreported interruptions.

These are host limitations, not silently repaired assurance guarantees.

## Deliberate exclusions

Version 1 does **not** add:

- hooks or pre-tool enforcement;
- subagents or independent reviewer agents;
- MCP services;
- a task-state database;
- a new AI memory system;
- automatic interruption detection;
- physiological or behavioral monitoring;
- a fixed reconstruction schema;
- a software-development phase model;
- mandatory learning mode, quizzes, or questionnaires;
- a router Skill above the two conditional Skills.

Additions should be justified by an observed failure or a specific experimental question.

## Field evaluation

Prioritize first-opportunity behavior rather than final outcome alone.

Use [`field-evaluation.md`](field-evaluation.md) to record high-value observations when they naturally occur. Writing cases is not running them; no runtime or field results are claimed by this revision. Record:

- `pass` — intended behavior occurred at the first appropriate opportunity;
- `recovered` — human/external correction was needed before the behavior recovered;
- `fail` — the relevant failure remained;
- `not_observed` — no discriminating situation occurred.

Especially watch for:

- human compensatory labor;
- unnecessary questions or confirmation rituals;
- implicit inference about human understanding, memory, or capability;
- Skill under-routing or over-routing;
- model probes that do not change a meaningful judgment;
- useful versus noisy substrate contact;
- reconstruction that reduces rereading/re-explanation;
- stale cues or proposal/commitment confusion;
- correct no-intervention cases.

Do not infer carrier reliability, cognitive-model truth, human capability growth, or cross-host generality from one successful task.

## Deployment/source relationship

The repository copy is the **versioned experimental source**.

The Cursor User Rule and `~/.cursor/skills/` copies are runtime installations. When recording a field observation, retain enough information to identify which repository revision the installed carrier came from.

This avoids turning the local Cursor installation into an independent source of truth.
