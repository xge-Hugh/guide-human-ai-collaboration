---
name: human-ai-reconstruction
description: Use when the human explicitly reports losing, forgetting, or no longer understanding prior task reasoning; when collaboration visibly returns to an interrupted task or branch; when a previously established relationship is required for the next consequential judgment but is no longer sufficiently observable; or when an unresolved commitment, consequential model revision, important divergence, or evidence basis must be reactivated. Also use when an observable interruption or branch creates a high-value return edge that is cheap to preserve. Do not use merely because time elapsed, the conversation is long, the task is complex, or the AI guesses the human may have forgotten.
---

# Human–AI Reconstruction

Help the human regain a usable task model after cognitive discontinuity. This is not an AI-memory protocol and not a requirement to restore the entire conversation.

## 1. Do not mind-read

The AI cannot directly observe whether the human currently remembers or understands a prior model.

Do not infer forgetting from silence, elapsed time, conversational style, or task complexity alone.

If the human explicitly says they forgot, lost context, or do not understand the previous reasoning, accept that report and reconstruct. Do not test whether they “really” forgot.

If reconstruction need is not observable and does not affect a consequential judgment, do nothing.

## 2. Identify the next meaningful judgment

Ask internally:

> What relationship must become usable again for the human to explain, predict, inspect, judge, or decide what comes next?

Do not default to replaying the transcript or summarizing the entire task.

## 3. Recover from traceable sources

Use the current conversation, code, documents, confirmed decisions, evidence, revision traces, and explicit commitments.

The reconstruction view is derived from those sources. It is not a new source of truth.

When an old cue may be stale, check the current authoritative or directly verifiable source before relying on it.

## 4. Select the minimum sufficient reconstruction set

Choose the smallest set of cues that lets the human regenerate enough of the reasoning to judge:

- whether the current model still applies;
- what materially changed;
- what remains unresolved;
- whether the next meaningful action is justified.

The set may be empty.

Candidate cue types include:

- purpose or invariant;
- checkpoint;
- open loop or return edge;
- confirmed commitment;
- unresolved divergence;
- consequential model change;
- direct evidence;
- relevant unknown;
- proposal.

These are a vocabulary, not a fixed schema or required card.

Prefer cues that restore many useful relationships with little reading.

Distinguish a recognition cue from usable reasoning. A remembered label may only identify which source to retrieve. When subsequent reasoning repeatedly depends on a relationship, restore that causal structure or keep a useful diagram/example visible; a link alone may be insufficient. Exact, infrequent details can stay in a reliably retrievable source.

Include enough orientation to recognize when retrieval is needed and a concrete return path when a cue depends on external evidence. If access is unavailable, say what remains unverified and recover what the task needs through available evidence; never imply that a link was inspected. Recheck volatile facts at use time.

## 5. Preserve semantic and epistemic status

Do not reconstruct:

- an AI proposal as a shared commitment;
- a superseded plan as the current next step;
- an inference as confirmed fact;
- a previous summary as stronger than its source;
- past agreement when consequential divergence remained.

Reconstruction restores a reasoning path so the model can be judged again; it does not make old beliefs current merely because they were once stored.

## 6. Render for rapid reacquisition

Use the least elaborate representation that exposes the needed relationship.

- One cue: usually one natural sentence.
- Two or three heterogeneous cues: short scan-friendly text with semantic anchors.
- Truly parallel comparison dimensions: a compact table if that reduces integration cost.
- Real dependency or branch structure: a richer representation only when the structure itself matters.

Do not generate a Context card merely because this Skill activated.

Do not require the human to read the full conversation log when a smaller reconstruction surface can restore the needed model.

## 7. Preserve a cheap return cue only when the open loop is observable

When the collaboration visibly creates an interruption, side branch, unresolved commitment, or return edge whose loss would create meaningful reconstruction cost, preserve one small cue if doing so is cheap.

Do not continuously maintain a hidden model of what the human probably remembers.

Do not build a task-state database or persistent reconstruction file unless a later observed failure justifies that mechanism.

## 8. Re-establish grounding only when consequential

If the human reports that reconstruction is sufficient and the next action is low-risk or readily reversible, continue.

If a consequential judgment still depends on whether the reconstructed relation is actually usable, obtain one proportionate task-specific externalization or invoke the model-coordination treatment.

Do not require reproduction of the whole model. If a partial concept is reactivated by a new anomaly, connect the old cue to current evidence and revise it as needed; do not merely repeat the old explanation or treat recognition as mastery.

## 9. Return to the original task

Reconstruction is support for re-entry, not a new workflow phase.

Keep the surface temporary, correctable, and subordinate to its sources.

## Research return path

These procedures are experimental. If a boundary needs deeper interpretation, consult the [candidate source](https://github.com/xge-Hugh/guide-human-ai-collaboration/blob/62d3b6dff2f5112f35513cfc63fa18f06075347b/docs/research/collaborative-relations/studies/cognitive-placement-bridge-2026-09-15.md) and its related material, when accessible. This pinned source explains provenance, not current task state. Do not load it for routine use or treat retrieval failure as evidence.
