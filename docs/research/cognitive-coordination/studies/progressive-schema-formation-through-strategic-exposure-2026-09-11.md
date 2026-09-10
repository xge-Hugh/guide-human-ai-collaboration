# Progressive schema formation through strategic exposure — field-derived candidate

- **Date**: 2026-09-11
- **Status**: `field observation + candidate refinement`; not current spec, not validated guidance, and not authorization to modify the live Skill or Cursor carrier
- **Program**: cognitive coordination
- **Primary relation**: clarifies / extends the candidate meaning of `strategic exposure` and `cognitive allocation`
- **Related**: [`../model.md`](../model.md), [`../evidence-review.md`](../evidence-review.md), [`action-sufficient-alignment-and-epistemic-delta-2026-09-10.md`](action-sufficient-alignment-and-epistemic-delta-2026-09-10.md), [`cross-level-epistemic-probing-replay-2026-08-30.md`](cross-level-epistemic-probing-replay-2026-08-30.md), [`../../runtime-capability/model.md`](../../runtime-capability/model.md), [`../../../spec/norms.md`](../../../spec/norms.md)

## 1. Why record this separately

The previous field-derived study clarified two local coordination problems:

- human and AI do not need complete model convergence before acting; they need **action-sufficient alignment**;
- delegated work creates new asymmetric knowledge, so consequential **epistemic deltas** may need to return to the human before later judgment or responsibility continues.

A subsequent reflection exposed a different temporal question:

> Can an exposure be valuable even when it changes little about the current task, because it improves the human's future representations, schemas, independent judgment, prediction, delegation, or reconstruction?

The current cognitive-coordination model already gives `strategic exposure` some longitudinal meaning: selective contact can help the human form new abstractions from lower-level phenomena, retain calibration against AI summaries, preserve anomaly/boundary recognition, and maintain responsibility-related review capability. `Cognitive allocation` also already includes future responsibility-related capability and reconstruction value.

The field observations below sharpen that latent idea into a candidate account of **progressive schema formation across repeated real work**, without proposing a new mandatory teaching layer.

## 2. Field observation A — a concept can be useful before it is fully understood

In earlier API development, the human repeatedly noticed a few lines being added to `Program.cs` and asked why. AI named the concept as **dependency injection** and discussed terms such as lifecycle, singleton, transient, scoped, and inversion of control.

Looking back, the human does not believe a complete operational model of dependency injection had been formed at that time. The result was closer to:

```text
concrete repeated phenomenon
        ↓
concept name / partial vocabulary
        ↓
weak, incomplete representation
```

Nevertheless, the concept was no longer completely unknown. It had become a recognizable cognitive handle.

Later, during a different project failure involving a class/service that held both a framework/DI-provided collaborator and a locally constructed synchronization/resource object, a disposal/lifetime problem created an anomaly. The human noticed the contrast between:

- an object/reference supplied through dependency injection;
- an object actively constructed and owned inside the class;
- the lifetime of the containing object itself.

That live problem reactivated the earlier partial DI representation. Reasoning then expanded from the immediate defect into questions of object creation, ownership, lifecycle, disposal, pooling/factory behavior, state retention, and how the lifetime of a holder interacts with the lifetime of what it holds.

The important observation is not the specific .NET rule. It is the cognitive transition:

```text
partial earlier concept
        +
new concrete anomaly
        +
active human comparison
        ↓
new relational structure
        ↓
revised / stronger task model
        ↓
broader future predictions and design questions
```

A concept that had previously been little more than a name and fragments of vocabulary later became a retrieval index and bridge for a more powerful representation.

## 3. Candidate refinement: strategic exposure can have longitudinal option value

Strategic exposure should not be limited to information needed to cross the **current** collaboration boundary.

A representation, concept name, principle, anomaly, direct evidence slice, or cross-representation relation may deserve selective exposure when its expected value is mainly **longitudinal**:

- it may seed a concept the human can later recognize;
- it may create a bridge cue for future reconstruction;
- it may help later evidence attach to an existing partial structure rather than remain isolated;
- it may increase future independent prediction, judgment, anomaly detection, or review;
- it may let the human formulate better constraints and delegate AI work with lower coordination cost;
- it may reduce repeated explanation/grounding cost across related tasks;
- it may expand the human's future option set: when to challenge, verify, inspect, delegate, or escalate.

A rough qualitative model is:

```text
expected exposure value
    = current coordination value
    + expected longitudinal model / capability value
    - present cognitive + interruption + opportunity cost
```

This is not a runtime score.

### 3.1 Important implication

`Action-sufficient alignment` is a stopping rule for **current action coordination**, not proof that further cognition has zero value.

Even after enough grounding exists to act safely, a low-cost exposure can still be justified when it has unusually high future model value.

Therefore:

```text
enough to act now
    ≠
no reason to expose anything else
```

The remaining question is whether the additional exposure has sufficient longitudinal value to justify the human attention it consumes.

## 4. Candidate process: seed → reactivate → bind → revise

The field observation suggests a progressive process that need not occur in one session and need not begin with a complete lesson.

### 4.1 Seed / index

AI or the human may first expose only a compact concept name, distinction, or relation.

The human may not yet possess a complete model. The immediate gain may simply be:

- `this phenomenon has a name`;
- `these cases may belong to the same structure`;
- `there is a representation here I may recognize later`.

This is **not** evidence of mastery.

### 4.2 Reactivation

A later task, anomaly, failure, comparison, or repeated pattern can reactivate the partial representation.

Recognition may precede understanding:

```text
"I have seen this concept before"
        ↓
"this current situation may be related"
```

That can reduce the distance between the live problem and a useful higher-level model.

### 4.3 Binding through live evidence

The new task can supply the concrete causal or structural relations missing from the earlier exposure.

The human may compare representations, generate hypotheses, inspect evidence, ask why two objects differ, or predict what should happen under another lifetime/ownership condition.

The important cognitive work may be performed **with** the task environment and AI rather than through passive explanation.

### 4.4 Revision / strengthening

The earlier weak representation is restructured rather than merely repeated. A label that once indexed a few terms can become a model capable of generating new predictions and design questions.

Later encounters can strengthen or revise it again.

This suggests:

```text
name / partial representation
    → later activation
    → task-grounded relation
    → revised model
    → future reuse / transfer
```

rather than:

```text
one complete explanation
    → permanent understanding
```

## 5. Complementary initiative: AI can sow; humans can cultivate; either side can open the path

The candidate should **not** be interpreted as either human-interest-only learning or AI-decided teaching.

Two initiation routes can coexist.

### Route A — AI notices a high-option-value exposure

AI may briefly name or expose a concept when:

- the current case is a clear instance of a stable, transferable structure;
- the human is likely to encounter related decisions again or retains responsibility in that area;
- the concept could materially improve future judgment/delegation rather than merely add trivia;
- the present case provides unusually good grounding;
- the exposure cost is low.

The default should remain conservative: this does not justify turning routine work into unsolicited lessons.

### Route B — human interest externalizes model readiness

Human curiosity can itself be high-value evidence about private cognitive state.

Signals include:

- asking why an apparently routine step exists;
- recognizing a term from an earlier encounter;
- noticing an anomaly or contrast;
- generating an analogy or hypothesis;
- asking whether two representations are connected;
- voluntarily moving beyond the shortest task solution.

These signals do not prove that the branch is worth unlimited time, but they lower the uncertainty about whether the human currently has an active information gap and a representation ready to be enriched.

A reasonable candidate asymmetry is:

> Be conservative about imposing unsolicited learning, but comparatively responsive when the human exposes genuine curiosity or starts constructing a cross-representation connection.

This complements Issue #33's broader question about proactive exposure, AI inquiry, and implicit inference: explicit human curiosity can be treated as first-class evidence rather than forcing AI to infer learning value from scratch.

## 6. Interest is a coordination signal, not the only value function

Human interest should receive meaningful weight because it changes the economics of cognition:

- relevant prior knowledge may already be activated;
- the human has identified a subjective information gap;
- attention and assimilation are already being invested;
- the task representation may provide concrete hooks for encoding.

But interest is not sufficient by itself. A curiosity branch may still be low-value, distracting, or too expensive under current task pressure.

Likewise, lack of expressed curiosity does not prove that an exposure has no future value. A human with no concept name may be unable to ask about a structure they cannot yet represent.

This is why AI-side selective seeding and human-side cultivation can be complementary rather than competing policies.

## 7. Graph-shaped learning rather than mandatory prerequisite order

The field observation also supports a cautious hypothesis about learning shape in long-lived human–AI collaboration.

Human learning during real work may be **jumping / graph-shaped**:

```text
current task
    → unfamiliar term
    → later unrelated-looking anomaly
    → old concept reactivated
    → lower-level ownership/lifetime evidence
    → higher-level design model
```

This need not follow a classroom-style prerequisite sequence.

AI can potentially support this by supplying missing prerequisite structure **on demand** when a jump encounters a real dependency, rather than requiring complete prerequisite coverage before the human follows an active question.

However, this is not evidence that prerequisite structure is unnecessary. Some knowledge dependencies are real; the claim is only that the collaboration path need not mirror a fixed curriculum when local scaffolding can make a valuable jump intelligible.

## 8. Relationship to existing cognitive-coordination constructs

This observation currently looks more like a **refinement and temporal coupling of existing constructs** than a new top-level mechanism.

- **strategic exposure**: exposure can be selected for future model value, not only current judgment;
- **activation**: earlier partial concepts can be reactivated by a later task;
- **cross-representation probing**: anomalies can motivate movement into another representation and return a consequential delta;
- **revision / bounding**: later evidence restructures the earlier model;
- **reconstruction**: a compact name or bridge relation can help regenerate a usable model later;
- **cognitive allocation**: current cognitive cost must be traded against both immediate and longitudinal benefit;
- **productive divergence**: AI does not need to force the human into its full explanatory model at first exposure;
- **runtime capability / longitudinal assurance**: repeated opportunities and later activation matter more than one isolated teaching event.

The project should prefer strengthening these relationships over creating a new ontology unless repeated evidence shows that `progressive schema formation` requires a distinct concept with independent downstream consumers.

## 9. What this candidate does **not** imply

It does not imply:

- teach every concept that might someday be useful;
- maximize human participation or explanation length;
- assume that naming a term produces understanding;
- require the human to follow every curiosity branch;
- treat interest as proof of transfer value;
- preserve permanent psychological profiles of what a person knows;
- force fixed prerequisite ladders or fixed learning curricula;
- infer capability growth from one successful conceptual connection;
- change current spec, Skill behavior, or carrier architecture from this observation alone.

A compact seed that never becomes useful is an acceptable outcome; not every exposure must be justified retrospectively as learning success.

## 10. Discriminating predictions / future field probes

The candidate gains value if future collaboration shows patterns such as:

1. **partial-name reuse** — a concept briefly exposed earlier is spontaneously recognized in a later task and helps the human form a better question or model;
2. **anomaly-triggered reconstruction** — a failure or edge case reactivates prior fragments and leads to a stronger representation than passive re-explanation would have produced;
3. **future coordination reduction** — after a schema becomes usable, later related tasks require less explanation/grounding and the human can give higher-quality constraints or delegation;
4. **better independent prediction** — the human can anticipate a new failure mode or design implication without AI first stating it;
5. **human-interest advantage** — when the human has already exposed curiosity or a self-generated connection, a small AI intervention produces more useful model change than similar unsolicited teaching;
6. **high-value AI seeding** — a compact AI-introduced name/distinction later becomes useful even though it did not materially change the original task.

Evidence that should narrow or reject the candidate includes:

- strategic seeding frequently creates distraction without later reuse;
- partial labels produce persistent misconceptions or false confidence more often than useful retrieval cues;
- AI cannot distinguish high-option-value concepts from trivia without excessive inquiry or profiling;
- learning branches systematically increase collaboration cost more than later savings;
- apparent future transfer depends mainly on explicit full instruction rather than progressive task-grounded reconstruction;
- the same phenomena are fully explained by existing strategic exposure / activation / reconstruction semantics without any useful refinement.

## 11. Governance boundary and next step

Per project governance, this file preserves the field observation, separates it from the candidate causal interpretation, places it in the existing cognitive-coordination inquiry context, and keeps authority below `docs/spec/`.

Current status should therefore remain:

```text
field observation
    ↓ supports / clarifies
candidate refinement of strategic exposure + cognitive allocation
    ↓
future field discrimination / evidence review
    ↓
possible narrowing, collapse into existing constructs, or later promotion through a separate governance decision
```

No carrier or specification change is justified by this file alone.
