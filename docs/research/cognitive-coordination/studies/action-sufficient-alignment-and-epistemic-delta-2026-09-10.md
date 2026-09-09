# Action-sufficient alignment and epistemic-delta settlement — field-derived candidate

- **Date**: 2026-09-10
- **Status**: `field observation + candidate mechanism`; not current spec, not validated guidance, and not authorization to modify the live Skill or Cursor carrier
- **Program**: cognitive coordination
- **Related**: [`../model.md`](../model.md), [`../evidence-review.md`](../evidence-review.md), [`../../../spec/domains/software-development.md`](../../../spec/domains/software-development.md), [`../../../spec/evaluation.md`](../../../spec/evaluation.md), [`../../../guidance/interaction.md`](../../../guidance/interaction.md), Issue #33

## 1. Why record this

Two ordinary work episodes exposed a shared constraint that is easy to miss when collaboration is evaluated mainly by AI output quality.

1. **Good AI analysis did not automatically create usable human understanding.** The AI analyzed Excel/business material and complex designer requirements, found contradictions, and raised many of the same questions the human later formed independently. Yet the AI's detailed textual explanation initially made the task feel more complicated. After the human inspected the source documents and graphical interface directly, cross-checked relationships, and constructed their own questions, the task model became simpler and usable.
2. **Good pre-implementation grounding did not guarantee good post-implementation epistemic state.** Human and AI had already aligned on business invariants, implementation form, idempotency mapping, and other code-shaping constraints. The AI then implemented independently. During execution a compile failed and was repaired; another error was judged unrelated; a date-format issue had not been discussed; metadata validation was not performed through the expected MCP path and old code was reused. The final report largely restated the agreed implementation and exposed little of this new information. Only an accidental glimpse of the compile failure and subsequent human probing surfaced the broader delta.

The second episode is **not** evidence that every transient failure must be reported. A compile error that is locally repaired, understood, and leaves no consequential uncertainty may be routine execution noise. The relevant problem is the selection rule for what becomes visible after delegated work.

These observations connect to existing project concerns about strategic exposure, productive divergence, cognitive allocation, grounding, evidence contact, responsibility-related capability, and Issue #33's private-state coordination problem.

## 2. Candidate premise: internal models are private, partial, and dynamically divergent

Human and AI cannot directly inspect each other's internal task models. Dialogue, artifacts, tool outputs, behavior, examples, tests, and other externalizations provide evidence about those models, but do not make them identical.

This yields two complementary constraints:

- **non-transferability**: AI-side processing or understanding does not automatically become human-side understanding; when the human must judge, steer, verify, explain, accept risk, or continue reasoning, sufficient human-side task structure still has to be constructed;
- **non-convergence requirement**: healthy collaboration does not require complete internal model convergence. Some divergence can remain harmless, delegated, cheaply testable, or positively useful for independent review and alternative hypotheses.

Therefore the coordination target should not be `make both models identical`. It should be `make consequential differences sufficiently observable for the next action and responsibility boundary`.

## 3. Candidate mechanism A: action-sufficient alignment

**Action-sufficient alignment** means that human and AI have enough shared or mutually legible structure to take the next consequential action without requiring complete model convergence.

The alignment target is local to an action boundary. It may include, depending on the task:

- purpose and business semantics;
- invariants and constraints;
- observable behavior / contract;
- authority, delegation, and risk-acceptance boundary;
- acceptance / validation evidence;
- assumptions whose divergence would materially reshape downstream work.

Residual divergence can remain when it is reasonably:

- non-consequential to the next action;
- inside an explicitly delegated solution space;
- cheap to detect and repair later;
- bounded by reversibility, modularity, tests, previews, diffs, staging, or other strong feedback;
- deliberately preserved for exploration, creativity, or independent review.

Further grounding is more justified when a plausible unresolved divergence could materially change a hard-to-reverse action, acceptance criterion, responsibility boundary, evidence interpretation, or downstream dependency.

A qualitative marginal test is:

```text
continue grounding when
expected value of exposing one more consequential difference
    >
coordination cost of doing so
```

Potential value grows with the probability of a hidden consequential divergence, its impact, and the cost/difficulty of discovering and repairing it later. Coordination cost includes communication, human assimilation, delay, attention switching, anchoring/fixation, and lost productive independence.

This is **not** a runtime score or mandatory checklist.

### Important implication: verification can substitute for some pre-action consensus

When mismatch is cheap to observe and reverse, a better strategy may be to reduce the cost of residual divergence rather than discuss more before acting.

For example:

```text
more pre-action grounding
        OR
more reversible / observable / testable next action
        ↓
reduced expected divergence loss
```

This means previews, tests, diffs, prototypes, reversible commits, and staging environments can function as cognitive-coordination mechanisms, not only engineering conveniences.

## 4. Candidate mechanism B: epistemic-delta settlement

Action-sufficient alignment is temporary. Delegation itself creates new asymmetry because the acting party encounters evidence, tool feedback, failures, local decisions, substitutions, and unknowns that the other party did not observe.

Let the last sufficiently grounded shared state be `S0`. During delegated work, AI state may become:

```text
S_AI1 = S0 + Δ
```

while the human remains closer to:

```text
S_H1 ≈ S0
```

A useful post-delegation report should therefore preferentially settle the **consequential portion of Δ**, rather than mainly restate `S0` or narrate every low-value execution event.

**Epistemic-delta settlement** is the candidate operation of selectively returning new information acquired during delegated work when that information can materially change the human's model of:

- whether the result satisfies the agreed intent;
- what evidence supports the result;
- what validation was performed, skipped, weakened, substituted, or failed;
- what assumptions or constraints were added or reinterpreted;
- what anomalies, unexplained results, or residual uncertainties remain;
- what consequential implementation choices were made inside or near the delegation boundary;
- what the human should inspect, test, accept, reject, monitor, or re-ground next.

The desired property is **high information gain relative to the last grounded shared state**, not maximum report length and not maximum execution transparency.

### Negative cases

Epistemic-delta settlement does **not** imply:

- report every compile failure, retry, warning, or locally repaired typo;
- dump raw logs for the human to triage;
- treat any intermediate error as a risk escalation;
- repeat the already agreed plan in greater detail;
- assume a clean final result erases materially different evidence paths;
- force the human to audit all low-level AI work.

A transient failure can remain compressed away when it is understood, locally resolved, does not weaken the final evidence, does not reveal a broader assumption mismatch, and does not change what the responsible human should believe or do.

Conversely, apparently successful execution can still require exposure when the evidence path changed. For example, reusing old code instead of performing an expected metadata validation may matter even if compilation succeeds, because it changes the basis for confidence.

## 5. Relationship between the two mechanisms

The two mechanisms form a temporal coordination loop:

```text
partial private models
        ↓
action-sufficient alignment
        ↓
delegated action / independent cognition
        ↓
new private evidence and local decisions
        ↓
selective epistemic-delta settlement
        ↓
re-ground only affected dependencies
        ↓
next action-sufficient alignment
```

This avoids two symmetric failures:

- **over-transfer**: AI gives a complete finished representation that imposes high assimilation cost and bypasses useful human model construction;
- **under-transfer**: AI compresses away new evidence, deviations, or uncertainty required for meaningful human judgment and responsibility.

The candidate objective is selective transfer: preserve distinctions whose loss would change judgment while compressing low-value execution noise.

## 6. Relation to existing project concepts

### Strategic exposure / substrate contact

The field case supports the existing concern that AI-compressed summaries can remove anomalies and direct evidence needed for human calibration. Epistemic-delta settlement is one possible temporal selection rule for *which* new substrate evidence deserves return after delegation.

### Productive divergence / mutual model legibility

Action-sufficient alignment narrows the stopping condition: do not pursue model identity; pursue enough legibility around consequential action boundaries. Remaining divergence may be deliberately preserved when it is bounded and useful.

### Cognitive allocation

Both mechanisms are cost-sensitive. More exposure is not automatically better. The unit of optimization is total coordination value, including human assimilation burden, verification cost, expected mismatch/rework, and loss from hidden uncertainty.

### Issue #33: exposure ↔ inquiry ↔ inference

Issue #33 asks how to coordinate private participant state without always inferring, always asking, or requiring continuous human self-report. The current candidate adds an action-boundary interpretation:

> choose the cheapest coordination operation that reduces expected consequential divergence enough to support the next action.

That operation may be inference, one direct question, one discriminating example, a direct evidence slice, a test, a diff, a reversible implementation, or explicit preservation of uncertainty.

### Responsibility and epistemic access

A particularly important failure state is:

```text
AI information advantage increases
human responsibility remains
human evidence visibility decreases
```

This can create nominal human authority without sufficient epistemic access to exercise it. The project should therefore distinguish delegation of execution/cognition from delegation of responsibility and risk acceptance.

## 7. Field-derived predictions for later validation

These are candidate predictions, not current requirements.

1. A useful post-delegation report has higher information gain relative to the last grounded state than a report that mainly restates the agreed implementation.
2. Reporting every transient event increases cognitive cost without proportional improvement; selective delta reporting should outperform raw execution narration.
3. Skipped, substituted, weakened, or materially different validation paths are more likely to matter than locally repaired execution noise because they change the evidence basis for confidence.
4. Cheap observability and reversibility should reduce the amount of pre-action conversational grounding required for low/medium-risk implementation choices.
5. When a late delta exposes an earlier model mismatch, only dependent judgments should be selectively revalidated rather than restarting the whole conversation.
6. Human responsibility without visibility into consequential evidence deltas should predict poorer calibration even when final AI task output is technically correct.
7. Reports optimized only for polished final-state summaries may systematically hide the highest-value collaborative information: anomalies, evidence substitutions, boundary decisions, and residual unknowns.

## 8. Evidence boundary and non-overfitting rule

Current support is limited to:

- two field observations from real human–AI work;
- derivation from existing project semantics;
- compatibility with current cognitive-coordination candidates and software review/retrospective requirements.

This does **not** establish that `action-sufficient alignment` or `epistemic-delta settlement` are optimal terms, independent mechanisms, or generally valid across domains.

Do not promote them to current spec or live carrier solely from this record. Future field evidence should be used to test whether these constructs improve discrimination over existing concepts such as grounding, strategic exposure, evidence contact, productive divergence, cognitive allocation, and selective revalidation. If they merely rename existing behavior without changing prediction or design, collapse them back into the simpler model.
