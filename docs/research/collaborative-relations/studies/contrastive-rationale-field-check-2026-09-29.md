# Contrastive rationale as experiential compensation — field-evidence check

- **Date**: 2026-09-29
- **Status**: focused field-evidence check / candidate mechanism; not validated guidance
- **Parent direction**: [post-delegation human robustness](../post-delegation-human-robustness-2026-09-29.md)
- **External mechanism basis**: [human-human handoff mechanisms](human-human-handoff-mechanisms-2026-09-29.md)
- **Question**: Does the existing project evidence justify treating contrastive rationale as a serious candidate mechanism for compensating some learning lost through delegated AI execution?

## 1. Candidate mechanism

After AI performs substantial delegated implementation, selectively expose one or a few **decision-relevant contrasts** rather than only the final result or a chronological trace.

Candidate shape:

~~~text
goal / invariant
→ plausible competing approach
→ chosen approach
→ discriminating condition / evidence
→ trade-off
→ switch condition for a nearby future case
~~~

The intended outcome is not complete implementation knowledge. It is a reusable decision distinction that can support later human judgment.

## 2. External-evidence reason to take the candidate seriously

Human-human code review has interpersonal functions beyond defect detection, including knowledge transfer, team awareness, alternative-solution generation, rationale exchange, and shared ownership.

Recent think-aloud evidence also shows that reviewers orient around context and rationale before detailed assessment and that review decisions rely on experience-based recognition of relevant distinctions.

Cognitive-apprenticeship research provides a second, independent rationale: workplace learning benefits when expert decision processes are made externally visible through modeling, articulation, reflection, and progressively more autonomous exploration.

These literatures do not validate the H-AI mechanism, but they make it less ad hoc.

## 3. Existing project observation A — progressive schema formation

The strongest existing human-side field evidence is the dependency-injection episode recorded in:

[Progressive schema formation through strategic exposure](../../cognitive-coordination/studies/progressive-schema-formation-through-strategic-exposure-2026-09-11.md).

The human first acquired only a partial concept name and vocabulary around dependency injection. A later lifetime/disposal anomaly reactivated that representation, and active comparison among:

- framework/DI-provided collaborator;
- locally constructed owned resource;
- containing-object lifetime;

helped build a stronger model involving ownership, lifecycle, disposal, pooling/factory behavior, and state retention.

This supports three parts of the present candidate:

1. a compact exposure can have future option value even when current action is already possible;
2. **contrast** among concrete cases can help bind a concept into a stronger relational model;
3. task-grounded reactivation can produce broader future design questions.

### Limitation

This episode was not a post-delegation completion report and did not compare contrastive rationale against other reporting forms.

It therefore supports the learning mechanism in principle, not the exact post-delegation intervention.

## 4. Existing project observation B — final-state reporting is too narrow

The field-derived action-sufficient-alignment / epistemic-delta study recorded a delegated implementation where the final report largely restated the agreed plan while execution had generated new evidence:

- compile failure and repair;
- an unrelated error;
- an ungrounded date-format issue;
- expected metadata validation not performed;
- reuse of old code.

The immediate lesson was state settlement: final success does not reveal changes in the evidence basis.

The new human-robustness framing adds another question:

> Even if all acceptance-relevant deltas had been reported correctly, what implementation judgment would the human have failed to develop by not doing the work?

The historical record does not answer that question directly.

This is important negative evidence: **state settlement and experiential compensation cannot be collapsed into the same reporting objective.**

## 5. Existing project observation C — later review seeks architecture/rationale even after prior explanation

GAMMA-007 / SR-3 concerns a real episode in which the human had already reviewed substantial code, requested explanations of new idempotency classes, and approved a commit. Later, the human still asked where new files were placed and whether package placement was reasonable, and stale code was subsequently inspected/removed.

Source review correctly deferred this as a primary γ-I omission fixture because earlier explanations and the acceptance boundary make a simple "report omitted consequential state" story unjustified.

Under the present question, however, that ambiguity is itself informative:

- human review interest extends beyond immediate functional correctness;
- architecture, placement, reuse, and stale abstractions can matter to the human's continuing model;
- a brief completion report is not the only information channel; earlier explanation and later artifact inspection can jointly carry rationale.

### Limitation

This does not prove that a contrastive completion report would have improved later judgment.

It suggests that **rationale exposure is temporally distributed** and that post-delegation compensation should be evaluated across the collaboration episode, not only in the final report.

## 6. Candidate distinction: rationale exposure versus rationale dumping

The evidence does not support a rule to explain every implementation choice.

The candidate should remain selective.

High-value contrastive rationale is more plausible when:

- the human retains responsibility for nearby future decisions;
- the implementation used a non-obvious strategy among genuinely plausible alternatives;
- the distinction recurs across tasks;
- an invariant was preserved through a mechanism the human is unlikely to infer from the artifact alone;
- the task exposed a boundary condition, trade-off, or failure mode with future option value;
- the exposure can be grounded in a small artifact/example.

Low-value exposure includes:

- arbitrary stylistic choices;
- alternatives invented after the fact to make the explanation look sophisticated;
- implementation trivia with little future reuse;
- long design narration when the human already has the relevant schema.

## 7. Strongest current hypothesis

A narrower hypothesis is better supported than "AI should teach alternatives after every task":

> **When delegated implementation contains a reusable decision boundary that the human would otherwise have encountered through hands-on work, a compact contrastive rationale plus representative evidence may preserve more future judgment value than final-state reporting alone at substantially lower cost than reproducing the implementation experience.**

This is still a candidate causal claim.

## 8. What would materially weaken it

The candidate should be narrowed if prospective field use shows that:

- humans rarely reuse the exposed distinctions in later tasks;
- contrastive rationale mostly increases explanation volume without changing questions, predictions, or delegation;
- the AI frequently invents weak alternatives or misleading trade-offs;
- selected artifact inspection alone yields the same longitudinal value more cheaply;
- humans develop stronger models only through direct hands-on execution, not explanation/contrast;
- the intervention creates false confidence because a compact rationale feels more complete than it is.

## 9. Focused prospective field observation

Do not build a controlled experiment yet.

For future ordinary delegated implementation, only when a high-value contrast naturally arises, allow a small post-execution exposure such as:

~~~text
Decision distinction:
I used A rather than B because condition X holds.

Invariant protected:
Y.

Trade-off:
A is simpler now but couples Z.

Switch condition:
if X changes / Z becomes shared, B becomes more attractive.

Evidence:
one diff/test/source pointer.
~~~

Observe naturally:

- Does the human ask a better follow-up question?
- Does the human inspect the cited artifact?
- Does the distinction reappear in a later task without AI first restating it?
- Does it improve the human's ability to set constraints or challenge a future design?
- Was the exposure ignored or experienced as noise?

Do not require a form after every task. Record only naturally consequential episodes.

## 10. Current judgment

The candidate is **worth field observation but not yet worth a dedicated controlled study**.

Why:

- external human-human literature gives it plausible mechanism support;
- the dependency-injection field episode demonstrates longitudinal value from task-grounded conceptual contrast;
- existing γ/state-settlement episodes show that completion reporting alone is an incomplete model of post-delegation coordination;
- the project does not yet have direct evidence that contrastive completion rationale improves future human judgment.

The cheapest next evidence is therefore prospective daily use in naturally suitable cases, followed by retrospective corpus analysis if repeated reuse or failure appears.
