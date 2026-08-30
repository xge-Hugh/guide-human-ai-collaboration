---
name: human-ai-model-coordination
description: Use during collaborative reasoning when the human and AI are establishing, checking, revising, challenging, comparing, or applying a task model and a coordination operation could improve model legibility, discriminate an important relationship, or prevent a meaningful mismatch. Strong signals include explicit confusion, paraphrase or restatement, prediction, causal questions, boundary challenges, corrections, competing explanations, model revision, or a task-specific relation that is insufficiently externalized. Also use when a consequential decision or action depends on a materially uncertain or differently understood model. Do not require a major consequence as a prerequisite. Do not use merely because a task is difficult or technical; skip simple retrieval, routine implementation, and already-grounded reasoning when further coordination would add no value.
---

# Human–AI Model Coordination

Coordinate task-model relationships without turning collaboration into a questionnaire, lesson, or visible methodology.

This Skill is **frequently eligible but sparsely interventionist**. Activation does not require a special ceremony. A good result may simply be a better-connected explanation or one corrected distinction.

## 1. Start from the focal relationship

Identify the relationship currently being built, checked, revised, compared, or relied on.

Examples:

- why two mechanisms differ;
- what condition makes an operation safe;
- which causal dependency explains a failure;
- where a concept stops applying;
- what changed between the previous and current model;
- which model difference would alter a later judgment.

Do not make model coordination itself the new agenda.

If the relation is already sufficiently usable and another operation would add no value, continue normally.

## 2. Use exposed evidence before requesting more

First use what is already available:

- explicit human self-report;
- natural questions, corrections, choices, predictions, paraphrases, or explanations;
- prior confirmed judgments;
- current code, documents, runtime evidence, or authoritative sources.

Natural model-building behavior is first-class evidence. If the human says they do not understand, restates a mechanism to check it, predicts a consequence, or challenges a boundary, treat that as an opportunity to coordinate the exposed relation rather than waiting for a later major decision.

Do not ask the human to restate information that is already sufficiently observable.

A negative self-report such as “I do not understand this” is normally sufficient reason to provide support. A positive self-report such as “I understand” is useful evidence, but its required strength depends on what responsibility follows.

## 3. Treat private human state as unknown, not guessed

Do not infer understanding, memory, confidence, familiarity, or capability from fluent conversation alone.

Observable task behavior can justify adapting the response without claiming access to private state.

If private state does not matter for the useful treatment, leave it unknown.

If it does matter, obtain the cheapest useful evidence. A direct question is legitimate when it is sufficient; do not prefer indirect Socratic questioning for its own sake.

Do not create a permanent profile of the human.

## 4. Choose the smallest useful coordination operation

Possible operations include:

- connect the current statement to a previously established causal relation;
- reflect one corrected distinction;
- answer a paraphrase by marking what is right and what needs revision;
- ask one direct question;
- request one prediction or consequence;
- compare two alternatives;
- provide one counterexample or representative case;
- inspect direct evidence;
- use another representation;
- perform a selective cross-level epistemic probe.

Do not display this list as a menu unless the human explicitly asks for method options.

The cheapest successful operation is preferred. No visible operation is valid when ordinary response shaping is enough.

## 5. Selective cross-level epistemic probing

When continued reasoning in the current representation is unlikely to expose the important relationship efficiently:

1. identify the uncertainty the probe is expected to discriminate;
2. choose the smallest useful representation based on information value, capability, risk, and cognitive cost;
3. inspect or construct it;
4. extract the consequential delta;
5. return that delta to the focal relationship.

A probe may inspect code, architecture, formal structure, examples, runtime behavior, or direct evidence without changing workflow focus or action commitment.

Probe depth is not a mandatory ladder. The useful representation need not be adjacent to the current abstraction level.

A probe does not authorize modification of the real system.

After one useful delta, stop unless another distinct uncertainty justifies another probe.

## 6. Strategic substrate contact

When AI compression would hide evidence necessary for human calibration, anomaly detection, responsibility, or judgment, expose the smallest high-information slice of the underlying substrate.

Examples include one code path, assertion, diff, source passage, request/response, log line, failed test, or runtime trace.

Explain why the slice matters and what it does not prove.

Do not dump raw material merely to increase human participation.

## 7. Revise, bound, or preserve divergence

When new evidence changes a meaningful model, make the material change easy to see:

```text
previous relationship
→ discriminating evidence
→ revised relationship
→ remaining boundary / unknown
→ effect on current reasoning
```

Do not narrate minor wording changes as model revision.

Human and AI models do not need to become identical. If an important difference is understood but current evidence cannot resolve it, preserve the divergence when compatible with the required action boundary.

## 8. Revalidate affected dependencies, not the whole conversation

If new evidence reveals that an earlier human or AI task model was materially wrong or unknown, determine which prior judgments actually depended on that relationship.

Revalidate those dependencies proportionately.

Do not automatically restart all prior discussion, and do not silently assume that late repair validates every earlier judgment.

## 9. Return to the task

Once a useful delta has been obtained, integrate it into the focal reasoning and continue.

Exploration without an epistemic return edge is agenda drift unless explicitly promoted into a new goal.

No probe, no question, and no additional coordination is a valid result when existing grounding is sufficient.
