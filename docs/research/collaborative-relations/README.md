# Collaborative relations research

- **Status**: active research program; contents are `candidate / research`, not specification authority.
- **Started**: 2026-09-12

This program studies the relational structure of human-AI collaboration: asymmetry, dependence and shared failure sources, responsibility and delegation, participant-local state, self/other models, allocation, representation, verification, and longitudinal capability.

It began as an inquiry into human-AI asymmetry and expanded after the inquiry showed that asymmetry is important but insufficient as a complete theory of collaboration.

## Evidence and authority boundary

This program follows [`../../governance/evidence-policy.md`](../../governance/evidence-policy.md). Field observations, external research, project studies, design hypotheses and normative choices remain distinct.

Nothing here automatically changes the current specification, guidance, live Skills, carrier behavior, or existing authority/responsibility commitments.

## Candidate architecture

```text
UPPER CONSTRAINTS
purpose · authority · responsibility · risk acceptance
evidence/source boundaries · epistemic integrity
                         │
                         ▼
TASK + RELATIONAL STATE
risk · reversibility · decomposability · observability
asymmetry A(t) · dependence/correlation C(t)
participant-local state · self/other models
                         │
                         ▼
COORDINATION ECONOMICS
allocation · verification · state-transfer cost
representation fitness · capability trajectory
                         │
                         ▼
INTERACTION MECHANISMS / CARRIER
exposure · timing · delegation · probes · shared substrate
representation mediation · evidence return · tools / UI
                         │
                         ▼
OUTCOME + STATE TRANSITION
result · calibration · understanding · reliance · capability
search diversity · evidence access · coordination cost
                         │
                         └──────────────► next relational state
```

This diagram is a research representation, not a mandatory runtime state machine.

### Responsibility, delegation and asymmetry are reciprocal

Let `R(t)` be responsibility/authority arrangement, `D(t)` delegated cognition/action, and `A(t)` consequential asymmetry. Responsibility defines capability/evidence demand and therefore which asymmetries matter. Delegation changes who acts, observes evidence and practices cognition, thereby changing later information and capability. Observed mismatch can then justify changing support, delegation, expertise or responsibility arrangement, subject to higher normative/legal constraints.

`R(t) ↔ A(t) ↔ D(t)` is therefore a constrained feedback system rather than a one-way hierarchy.

A current-project boundary remains: increased AI capability or work volume does not automatically grant additional authority or transfer human responsibility.

### Relational state is broader than asymmetry

Candidate asymmetry dimensions are:

- **epistemic access**: one participant has evidence/context/tool feedback/private intent the other lacks;
- **capability / error structure**: task-relevant competence or failure-distribution differences under current tools/support;
- **resource / operational differences**: attention, memory, speed, persistence, search/generation scale, tool or action affordance;
- **consequence exposure**: different exposure to downstream consequences, which interacts with but does not itself create legitimate authority.

Collaboration also depends on `C(t)`, the **dependence / correlation structure**: shared sources, assumptions, framing, search trajectories, information contamination and error correlation. Two equally capable participants can provide very different review value depending on whether their errors are correlated.

A negative-control rule follows: if removing human-AI asymmetry from a case leaves a rule's rationale intact, that rule should not be explained primarily through asymmetry.

## Distributed participant state

For a human `H` and AI `A`, distinguish six first-order referents:

```text
effective task-relevant states
    S_H*      human effective state
    S_A*      AI effective state

self-models
    M_H(H)    human model of own state
    M_A(A)    AI model of own state

partner-models
    M_H(A)    human model of AI state
    M_A(H)    AI model of human state
```

`S_H*` and `S_A*` are partially latent effective states, not metaphysical “true selves.” They can only be inferred through task-relevant evidence such as behavior, predictions, artifacts, tests, corrections and transfer.

A participant may therefore mis-model both the partner and themselves. Collaboration can sometimes improve self-calibration as well as mutual understanding.

Higher-order recursion such as “what I think you think I think” is not tracked by default; add it only when it changes a consequential prediction.

## Shared substrate and state coordination

Let `E(t)` denote authorized external task state such as files, diffs, tests, tables, plans, logs, source documents or visual interfaces. Shared visibility does not imply shared meaning. Each participant reconstructs usable state through its own tools, competence, task model and representation affordances.

General loop:

```text
participant-local state
→ externalization / observable action
→ representation / shared evidence
→ participant-specific perception + inference
→ reconstructed local state
→ grounding / correction / next action
```

This applies to ordinary dialogue as well as delegated execution.

When one participant performs local work, new state can be decomposed provisionally as `Δartifact + Δprivate + Δephemeral`: externally recoverable evidence; private reasoning/uncertainty/intent; and low-value local noise. The system should not automatically require the executor to narrate all three.

## Coordination economics

Raw execution capability is insufficient for task allocation. A provisional analytical decomposition is:

```text
total collaboration cost
= execution cost
+ specification / delegation cost
+ externalization cost
+ recipient acquisition / assimilation cost
+ verification cost
+ switching / waiting cost
+ expected error / recovery cost
+ relevant longitudinal capability effect
```

This is not a runtime numerical formula. Cheap production does not imply cheap state transfer.

## Participant-relative representation fitness

Informationally similar representations can impose different acquisition, inference and verification costs. Representation fitness is therefore participant-, task-, operation-, tool- and context-relative.

Candidate dimensions include fidelity, operational affordance, current accessibility, responsibility relevance, representational competence, developmental value, joint coordination cost, and provenance/return path.

The easiest representation now is not always the best long-term representation. If competence with a domain representation is itself needed for recurring responsibility, mediation may rationally fade over time. The reverse boundary also matters: participants should not be forced to learn a native representation merely because it exists when retained responsibility can be substantively exercised through another reliable representation.

## Four current design discriminators

1. **Responsibility relevance of delegation** — does the delegated cognitive operation overlap capability needed for current/foreseeable responsibility?
2. **Value of independent participant signal** — does preserving a sufficiently independent signal improve judgment enough to justify its cost?
3. **Selector / verification reliability** — can consequential evidence be distinguished from noise, and are omissions discoverable?
4. **Cross-participant state-transfer cost** — after local work, how expensive is it to make consequential state usable by the participant who needs it?

These variables explain why the same apparent asymmetry can rationally produce opposite mechanisms.

## Epistemic integrity versus disclosure strategy

Epistemic integrity constrains fabrication, unsupported certainty, false evidence claims and knowingly misleading omission. It does **not** require exhaustive immediate disclosure. Honest collaboration may still use selective sequencing, probes, delayed explanation, compression of low-value noise, or deliberate preservation of harmless divergence.

Honesty also does not solve mutual opacity: participants can genuinely misjudge what the other already knows or what they themselves understand.

## Longitudinal objective

```text
initial relational state
→ allocation / exposure / representation / delegation
→ cognition + action + evidence
→ learning / anchoring / dependence / search correlation
→ new capability and information distribution
→ next relational state
```

The objective is not to minimize asymmetry or maximize human participation. A stronger candidate objective is:

> Maintain or create a relational state whose asymmetries, dependencies, evidence access and capabilities remain compatible with the desired responsibility structure and future collaboration goals at proportionate joint cost.

## Current falsifiable claim families

The inquiry has produced candidate claims that should be allowed to lose:

- responsibility-relative capability demand;
- pre-exposure independence only when independent signal has value;
- delegated-action epistemic delta and selective settlement;
- selector reliability as a condition on selective reporting;
- responsibility-capability mismatch cannot be repaired by nominal approval alone;
- repeated responsibility-relevant substitution can alter future capability;
- stable high-AI delegation can remain healthy when responsibility-relevant capability/evidence is adequate;
- verification bandwidth can limit nominal human oversight;
- state-transfer cost can change optimal task allocation even at equal execution capability;
- shared observability can substitute for some explicit narration;
- participant-relative representation routing can reduce coordination cost;
- responsibility-relevant representational competence may justify fading mediation.

These claims should be tested against competing designs rather than treated as mutually reinforcing slogans.

## Candidate studies

- **α — responsibility-relevant delegation**: compare substitution, scaffolded responsibility-relevant engagement, and stable delegation of genuinely irrelevant low-level work; measure immediate output and later judgment/transfer.
- **β — independent-signal value**: compare AI-first, minimal human judgment first, and conditional exposure while stratifying human/AI competence, error overlap, risk and verification cost.
- **γ — state settlement**: compare final summary, full trace, selective delta, selective delta plus audit return, and shared artifact access; run in both AI-executes and human-executes directions.
- **δ — adaptive representation trajectory**: compare permanent familiar translation, native representation immediately, mediated native representation with fading support, and representation chosen only for immediate efficiency.

## Explicit non-claims

This program does not currently claim that all collaboration problems are asymmetry problems; latent participant state is directly observable; full common-ground convergence is desirable; more transparency is always better; human-first reasoning is universally superior; repeated AI delegation necessarily causes capability decline; raw/native representations are always superior; the same representation is optimal for human and AI; or this architecture is ready to replace the current specification model.

## Relations to neighboring programs

- [`../cognitive-coordination/`](../cognitive-coordination/README.md): task models, cognitive allocation, strategic exposure, reconstruction and related mechanisms.
- [`../runtime-capability/`](../runtime-capability/README.md): context, retrieval, Skills and external state as runtime capability infrastructure.
- [`../temporal-coordination/`](../temporal-coordination/README.md): waiting, suspension, recovery and interaction timing.
- [`../assurance/`](../assurance/README.md): runtime assurance and carrier reliability.

This program asks which relational conditions make those mechanisms valuable, unnecessary or harmful, and how interaction changes the relational state for future work.
