# Cursor Human–AI Collaboration Carrier v1

> Status: **experimental pilot carrier** for Issue #31. This directory is not a normative source and does not replace `docs/spec/`.
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
  │    ├─ externalization / discrimination
  │    ├─ selective cross-level epistemic probing
  │    ├─ strategic substrate contact
  │    ├─ revision / selective revalidation
  │    └─ productive divergence
  │
  └─ human-ai-reconstruction
       ├─ minimum sufficient reconstruction set
       ├─ human-facing reactivation
       └─ optional low-cost return cue at observable open loops
```

The split is based on runtime activation conditions, not on a desire to maximize Skill count.

- **Model coordination** activates when a consequential model relation is uncertain, differently understood, insufficiently externalized, contradicted, or stuck in the current representation.
- **Human reconstruction** activates when previously established reasoning must become usable again, or when an observable interruption/open loop makes a cheap return cue valuable.
- Either Skill may be inactive. No intervention is a valid outcome.

## Files

- `cursor-user-rule.md` — exact source for the user-level resident kernel.
- `skills/human-ai-model-coordination/SKILL.md` — conditional E1 treatment, including E2/E4 operations.
- `skills/human-ai-reconstruction/SKILL.md` — conditional E3 human reconstruction treatment.
- `evals/cases.json` — discriminating activation and behavior cases for manual review or later runner adaptation.

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

Research candidates remain candidates because they are executable here. Carrier structure does not promote them to normative truth.

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

Record high-value observations when they naturally occur:

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
