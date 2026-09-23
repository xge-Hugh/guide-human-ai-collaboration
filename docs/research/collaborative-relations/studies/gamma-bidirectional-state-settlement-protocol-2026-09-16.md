# Experiment γ — bidirectional state-settlement protocol

- **Date**: 2026-09-16
- **Status**: `candidate study protocol`; design, not results; not specification authority.
- **Program**: collaborative relations
- **Primary claim targets**: A3, A3a, A3b, A10, A12, A14. γ estimates the state-coordination-cost component relevant to A9 but does not by itself establish an allocation rule.
- **Field basis**: [`../../cognitive-coordination/studies/action-sufficient-alignment-and-epistemic-delta-2026-09-10.md`](../../cognitive-coordination/studies/action-sufficient-alignment-and-epistemic-delta-2026-09-10.md)

## 1. Research question

After one collaborator performs locally asymmetric work and acquires new evidence, decisions, failures, substitutions, or uncertainty, what settlement architecture lets the other collaborator regain **action-sufficient usable state** with the best trade-off among consequential-state fidelity, judgment/calibration, retrieval reliability, and total coordination cost?

The study is bidirectional:

```text
AI executes → human reconstructs / judges
human executes → AI reconstructs / judges
```

The goal is not to prove that more transparency is better. Final summaries, full traces, selective deltas, shared artifacts, and indexed/on-demand retrieval are competing designs.

## 2. Why the original six-way comparison is split

The earlier γ sketch mixed two causal variables:

1. **semantic settlement form** — what the executor proactively communicates;
2. **evidence-access architecture** — what underlying evidence the recipient can inspect or retrieve.

A flat six-way comparison could identify a winning package without showing why it won. γ is therefore staged.

### γ-I — settlement-form test

Hold a canonical audit return path constant and compare:

1. **final-state only** — final result/status plus already-agreed structure; no deliberate execution-delta surface;
2. **full trace** — chronological execution events including routine noise;
3. **selective consequential delta** — only oracle-identified state changes capable of altering downstream belief/action, with concise source pointers.

Pilot H3 showed that a selective-delta surface can accidentally bundle three mechanisms:

- **fact selection** — which new facts are surfaced;
- **consequence linkage** — how those facts connect to a grounded invariant, evidence threshold, or downstream judgment;
- **verification guidance** — what evidence/action could discriminate the remaining uncertainty.

Confirmatory γ-I should hold consequence-linkage and verification affordances as equivalent as possible across conditions, or explicitly factorialize them. Otherwise a selective-delta condition may win because it receives stronger reasoning support rather than because selective settlement itself is superior.

This primarily discriminates A3/A3a.

### γ-II — evidence-access architecture test

Hold the selective semantic delta surface constant and compare:

1. **surface only** — no underlying return edge during the decision task;
2. **direct shared artifacts** — relevant evidence bundle is directly inspectable without a semantic index;
3. **indexed / on-demand retrieval** — recipient receives an index of available evidence and retrieves only what a dependency requires.

This primarily discriminates A3b/A10/A12/A14.

### γ-III — selector stress test

Run only if γ-I shows that selective settlement has useful value. Compare:

1. **oracle-selected delta**;
2. **executor-selected delta without audit return**;
3. **executor-selected delta with audit return**.

Fixtures must contain at least one event that a locally acting executor could plausibly misclassify as non-consequential even though it changes the evidence basis or reveals the executor's own mistaken model. This directly tests the selector problem in A3b.

## 3. Experimental unit: controlled episode replay

The unit is an **episode fixture**, not a live free-form collaboration run.

Each fixture contains:

```text
S0 = last action-sufficient grounded state
E  = complete execution evidence record after S0
F  = final artifact/result state
D_now+ = deltas that can change the current accept/inspect/repair/escalate judgment
D_now0 = events not decision-critical for the current judgment
L      = possible longitudinal model/capability value of an event
J      = downstream judgments/actions that D_now+ should affect
R      = authoritative return paths to supporting evidence
```

The previous binary `D+ / D-` notation proved too coarse in pilot H2. An event can be non-decision-critical now yet still have longitudinal learning/model value. Current-decision consequence and longitudinal value must therefore be annotated separately rather than treating compressed events as cognitively worthless.

The fixture is frozen before settlement packages are generated.

### Why replay first

Replay prevents condition differences from being confounded with different underlying execution histories. A later field phase may test live execution, but the first study should vary settlement while holding the work episode fixed.

## 4. Fixture construction

Start with software-development and structured-analysis episodes because the project already has field observations there. Each fixture should include a mixture of:

- a changed implementation choice inside the delegation boundary;
- a validation path performed as planned;
- a validation path skipped, weakened, or substituted;
- a transient repaired failure that should usually remain compressible;
- an unrelated or low-value warning/noise event;
- a residual uncertainty or assumption whose relevance depends on the next action;
- final artifacts from which some, but not all, state can be reconstructed.

At least one fixture should recreate the structure of the field episode in which compilation failed and was repaired, an expected metadata-validation path was not used, old code was reused, and the polished final report exposed little of the changed evidence path.

At least one fixture should favor shared-artifact inspection, and at least one should make raw artifact inspection costly enough that an index could plausibly help.

## 5. Oracle annotation and anti-circularity

Before producing condition materials, annotate each fixture with:

- every candidate event;
- current-decision classification: `D_now+`, `D_now0`, or ambiguous;
- possible longitudinal model/capability value `L` separately from current-decision consequence;
- why a `D_now+` event can alter a downstream judgment;
- which judgment(s) it affects;
- evidence/source location;
- expected confidence direction if discovered;
- whether it requires semantic explanation beyond artifact inspection;
- evidence-coverage semantics: whether reported validation actually covers the grounded invariant rather than merely reporting that a command/test suite passed.

The acting AI must not be the sole authority for these labels. Where possible, use observable task invariants, tests, source evidence, and predeclared acceptance criteria. Ambiguous annotations remain marked ambiguous rather than forced into `D+` or `D-`.

Scoring rubrics are frozen before recipient runs.

## 6. Recipient task

After receiving the condition-specific settlement surface, the recipient must make consequential follow-up judgments rather than merely recall facts.

Required outputs:

1. **acceptance state** — accept / inspect further / reject or repair / escalate or re-ground;
2. **implementation confidence** — calibrated probability that the result actually satisfies the agreed intent;
3. **acceptance-evidence sufficiency** — whether currently available evidence is sufficient to accept now; this is scored separately from implementation confidence;
4. **evidence model** — what validation was performed, skipped, weakened, substituted, and which grounded cases it actually covered;
5. **dependency update** — which earlier assumptions or downstream decisions, if any, need revalidation;
6. **unknowns** — consequential unresolved uncertainty;
7. **evidence retrieval task** — locate supporting evidence when the condition permits retrieval;
8. **verification policy** — identify what evidence/reviewer/search/action would actually discriminate the live uncertainty and in what order.

Broader engineering-quality observations (architecture, naming, reuse, maintainability) may be recorded as secondary naturalistic behavior, but the primary γ judgment concerns satisfaction of the grounded intent/evidence threshold. This avoids scoring legitimate scope expansion as a settlement failure.

Recipient-directed verification is treated as a candidate coordination operation rather than assumed away:

```text
settlement surface
→ identify threatened invariant / uncertainty
→ choose evidence source, artifact, search, or reviewer
→ inspect / retrieve / ask
→ update confidence and next action
```

The recipient's selector can itself fail. A second reviewer given only a human-curated subset may inherit the human's omissions or framing. When independent review value matters, measure whether the reviewer retains an independent return path to source evidence.

A delayed probe should test whether the recipient can later locate the decisive evidence and reconstruct why confidence changed.

## 7. Outcome measures

Avoid one opaque aggregate score. Report an efficiency frontier across at least:

### Fidelity / judgment

- weighted recall of `D+`;
- false-positive uptake of `D-` as consequential;
- accuracy of accept/inspect/repair/escalate judgment;
- accuracy of validation-path reconstruction;
- correct identification of dependent judgments requiring revalidation;
- missed consequential evidence rate.

### Calibration

- confidence calibration / Brier-style error where outcomes are binary enough to support it;
- high-confidence wrong judgment rate (`false common ground` proxy).

### Coordination cost

- recipient reading / inspection time;
- tokens or information volume consumed;
- clarification turns;
- number and cost of artifact/retrieval actions;
- executor packaging/reporting effort;
- switching / waiting cost when measurable.

### Retrieval / reconstruction

- time to locate decisive evidence;
- unnecessary evidence opened;
- delayed evidence-location success;
- ability to reconstruct why confidence or next action should change;
- quality of the verification policy: whether requested evidence can discriminate the actual live uncertainty;
- dependence of a second reviewer on recipient-selected/framed evidence versus independent source access.

## 8. Bidirectional implementation

### AI → human

The same frozen execution record is rendered into the experimental settlement conditions. Human recipients should not see the same fixture in multiple conditions. Begin with a feasibility pilot; do not generalize from one project participant.

### Human → AI

Use fresh isolated AI contexts with only the condition-permitted information. The AI must not have repository/tool access beyond the experimental return edge. Human-executor fixtures should preserve artifacts plus private semantic notes separately so that artifact-recoverable and semantic-only deltas can be distinguished.

Use repeated independent AI runs per cell rather than treating one stochastic run as stable capability evidence.

## 9. Assignment and contamination control

- use blocked/randomized assignment across fixtures and conditions;
- never show one recipient the same fixture under two conditions;
- balance fixture difficulty across conditions;
- isolate AI recipient contexts;
- do not let scorers see condition labels when human judgment is required;
- use deterministic/rule-based scoring for objective fields when possible;
- treat model/version/tool state as part of the experimental context, not as a permanent property of AI.

The first pilot estimates variance, ceiling/floor effects, fixture validity, and whether recipient capability/methodology creates strong moderator effects. Confirmatory sample size should be chosen only after pilot variance is known rather than invented in advance.

Pilot calibration should also record recipient-side interpretation competence. Full-trace information can be present without the recipient deriving the consequential relation. Possible supports include consequence-linked guidance, verification methodology, or domain/representation competence; these should be modeled as context/moderators rather than silently assuming a universally capable selector/understander.

## 10. Stage-specific predictions and failure conditions

### γ-I

A3a gains support if selective delta preserves or improves consequential reconstruction/judgment while reducing unnecessary information and joint cost relative to full trace and final-state-only surfaces.

A3a is threatened if final-state-only or full trace consistently matches/outperforms selective delta at comparable cost.

A3 is narrowed if final artifacts/final-state surfaces reliably reconstruct all consequential post-execution state with negligible additional cost.

### γ-II

A10/A12 gain support if direct shared artifacts reduce explicit narration/clarification without increasing missed deltas or false confidence.

They are threatened if shared artifacts create equal or greater ambiguity/assimilation burden than semantic settlement.

A14 gains support where indexed/on-demand retrieval matches direct access on judgment while reducing inspection cost for low-reasoning-dependency evidence.

A14 is narrowed if indexed/addressable access systematically misses consequential evidence that direct access surfaces.

### γ-III

A3b gains support if executor-selected delta degrades specifically on self-implicating or hard-to-classify events and an audit return edge recovers recipient performance.

A3b is weakened if executor-only selection remains robust even on seeded selector-risk fixtures and auditability adds no material benefit.

## 11. Stopping / revision rules

- If recipients cannot distinguish consequential from non-consequential events even with oracle materials, repair the fixture before interpreting condition effects.
- If all conditions hit ceiling/floor performance, redesign fixture difficulty.
- If selective delta fails in γ-I, do not proceed as though γ-III only needs a better selector; first reconsider A3a or the representation itself.
- If shared artifacts help only because they reveal information omitted from supposedly equivalent semantic materials, treat that as a fidelity failure, not an access-architecture effect.
- Null and mixed results narrow exact claims; they do not validate or reject the whole collaborative-relations model.

## 12. Pilot deliverables

Before any confirmatory claim:

1. 3–5 frozen episode fixtures with oracle annotations;
2. condition renderers/templates that do not alter underlying evidence;
3. recipient task and frozen scoring rubric;
4. one AI-recipient feasibility run across multiple fixtures/conditions;
5. one human-recipient feasibility pass focused on usability and burden, explicitly treated as N-of-1 field evidence;
6. post-pilot protocol revision noting every change made before confirmatory evaluation.

The first next action is therefore **fixture construction**, not participant recruitment or model scoring.