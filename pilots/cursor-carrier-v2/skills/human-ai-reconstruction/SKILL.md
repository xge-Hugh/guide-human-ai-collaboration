---
name: human-ai-reconstruction
description: Use when reactivating prior reasoning or adding a small reconstruction cue could materially reduce observable reacquisition or integration cost. Strong signals include explicit forgetting or loss of context, return after interruption or side branch, a distant dependency needed for current reasoning, multiple revisions whose causal spine may be hard to reacquire, or long/dense/branched assistant-generated context where one small cue would reconnect the current answer to earlier reasoning. Infer reconstruction risk from observable interaction structure, not private forgetting. Do not activate merely because time elapsed or the conversation is long when the needed relation is already locally clear. A valid treatment may be only one embedded causal sentence; do not require a visible Context card or full summary.
---

# Human–AI Reconstruction

Help prior task reasoning become usable again with the smallest useful cue. This is not an AI-memory protocol and not a requirement to restore the entire conversation.

This Skill may support ordinary long-form collaboration, not only explicit “I forgot” recovery events.

## 1. Infer reconstruction risk, not private forgetting

The AI cannot directly observe whether the human currently remembers or understands a prior model.

Do not say or imply that the human forgot merely because context is long, dense, branched, or distant.

You may, however, observe that the interaction now requires reactivating a relation established far earlier, has accumulated several model revisions, or contains enough assistant-generated material that a small bridge cue would reduce reacquisition cost.

If the human explicitly says they forgot, lost context, or no longer understand prior reasoning, accept that report and reconstruct. Do not test whether they “really” forgot.

## 2. Identify the relation that must become usable

Ask internally:

> What prior relationship must become usable now for the current explanation, prediction, inspection, judgment, or decision to make sense?

Do not default to replaying the transcript or summarizing the entire task.

If the relation is already locally explicit, no reconstruction may be needed even in a very long conversation.

## 3. Recover from traceable sources

Use the current conversation, code, documents, confirmed decisions, evidence, revision traces, and explicit commitments.

The reconstruction view is derived from those sources. It is not a new source of truth.

When an old cue may be stale, check the current authoritative or directly verifiable source before relying on it.

## 4. Select the minimum sufficient reconstruction set

Choose the smallest set of cues that lets the human regenerate enough of the reasoning to continue.

Candidate cue types include:

- purpose or invariant;
- causal bridge;
- checkpoint;
- open loop or return edge;
- confirmed commitment;
- unresolved divergence;
- consequential model change;
- direct evidence;
- relevant unknown;
- proposal.

These are a vocabulary, not a fixed schema.

Prefer cues that restore many useful relationships with little reading.

The set may be one sentence or empty.

## 5. Embed cues when that is cheaper than a separate surface

When the current response already needs to explain something, prefer embedding the reconstruction cue naturally.

For example, instead of emitting a separate context block, reconnect the new point to the prior causal spine:

```text
Earlier we separated ETag from the business marker:
ETag blocks stale concurrent writes; the invoice/status marker prevents the same event from being applied again later.
```

This is reconstruction even though it is not a visible “recovery mode.”

## 6. Preserve semantic and epistemic status

Do not reconstruct:

- an AI proposal as a shared commitment;
- a superseded plan as the current next step;
- an inference as confirmed fact;
- a previous summary as stronger than its source;
- past agreement when consequential divergence remained.

Reconstruction restores a reasoning path so the model can be judged again; it does not make old beliefs current merely because they were once stored.

## 7. Render for rapid reacquisition

Use the least elaborate representation that exposes the needed relationship.

- One cue: usually one natural sentence.
- Two or three heterogeneous cues: short scan-friendly text with semantic anchors.
- Truly parallel comparison dimensions: a compact table if that reduces integration cost.
- Real dependency or branch structure: a richer representation only when the structure itself matters.

Do not generate a Context card merely because this Skill activated.

## 8. Preserve a cheap return cue when an open loop is observable

When collaboration visibly creates an interruption, side branch, unresolved commitment, important model revision, or return edge whose loss would create meaningful reconstruction cost, preserve one small cue if doing so is cheap.

Do not continuously maintain a hidden model of what the human probably remembers.

Do not build a task-state database or persistent reconstruction file unless later observed failure justifies that mechanism.

## 9. Re-establish grounding only when needed

If reconstruction is sufficient and the next action is low-risk or readily reversible, continue.

If a consequential judgment still depends on whether the reconstructed relation is actually usable, obtain one proportionate task-specific externalization or invoke the model-coordination treatment.

Do not require reproduction of the whole model.

## 10. Return to the original task

Reconstruction is support for continuity, not a new workflow phase.

Keep the surface temporary, correctable, and subordinate to its sources.
