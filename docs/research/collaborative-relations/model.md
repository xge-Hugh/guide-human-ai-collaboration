# Collaborative relations — candidate model

- **Status**: `candidate / research model`; not specification authority.
- **Program**: collaborative relations.
- **Purpose**: describe task-relevant relations among human and AI participants that change the value of allocation, verification, representation, exposure, retrieval, and capability-development choices.

This file extracts the conceptual model that was initially consolidated into the program README. It does not add a new normative requirement and does not imply that every dimension must be tracked at runtime.

## 1. Why asymmetry is not the whole relational model

The inquiry began with human–AI collaborative asymmetry: under a given task, time, tool state, information state, and support condition, what consequential differences exist between participants?

A useful task-relative description is:

```text
under context C,
for function F,
at time t,
given information / tools / support S,
participants H and A differ along dimension D
```

However, participant differences alone do not determine complementarity or review value. Two participants can have similar aggregate capability while making different errors, or very different capability while sharing the same blind spot.

The relational model therefore separates several questions that must not be collapsed.

## 2. Relational-state dimensions

### 2.1 Participant comparison: asymmetry, symmetry, similarity

This axis asks how participants compare along a task-relevant dimension.

Candidate dimensions include:

- **epistemic access** — evidence, context, tool feedback, private intent, or local execution state available to one participant but not the other;
- **capability / error structure** — effective task competence and failure tendencies under current tools and support;
- **resource / operational structure** — attention, memory, speed, persistence, search/generation scale, tool access, or action affordances;
- **consequence exposure** — different exposure to downstream consequences; this interacts with responsibility but does not by itself create legitimate authority.

`asymmetry` and `symmetry / similarity` belong to this same comparison axis. Asymmetry is not a permanent participant property; it is task-, context-, time-, tool-, and support-relative.

### 2.2 Joint dependence / correlation structure

This is a different axis. It asks how the participants' information, assumptions, search paths, judgments, and errors are jointly coupled.

Relevant mechanisms can include:

- shared evidence sources or external substrate;
- shared assumptions or conventions;
- framing dependence caused by one participant seeing the other's proposal first;
- search-path correlation;
- error correlation;
- information contamination or copied intermediate conclusions.

Shared sources or substrate can **cause** dependence, but are not identical to dependence. Participants can interpret one source differently, and they can become correlated without literally sharing an artifact.

This distinction matters for complementarity. Similar capability with low error correlation can produce useful independent review; similar capability with highly correlated errors may add little assurance. Conversely, a weaker participant can still provide high-value review if they possess an independent signal for a consequential failure class.

### 2.3 Distributed epistemic state

Human and AI do not automatically share task-relevant state. For a dyad `H` and `A`, distinguish six first-order referents:

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

`S_H*` and `S_A*` are partially latent effective states, not metaphysical "true selves". They are inferred through task-relevant evidence such as behavior, predictions, artifacts, tests, corrections, and transfer.

A participant can therefore mis-model the partner and also mis-model themselves. Collaboration can sometimes improve self-calibration as well as mutual understanding.

Higher-order recursion such as "what I think you think I think" is excluded by default. Add another order only when it changes a consequential prediction.

### 2.4 Responsibility / authority structure

Responsibility and authority are related to, but not reducible to, capability comparison.

A current project invariant remains:

> Increased AI capability or work volume does not automatically grant additional authority or transfer human responsibility.

Responsibility creates contextual capability and evidence demands. Those demands determine which participant differences and evidence paths are consequential.

### 2.5 Interaction / allocation structure

Collaboration architecture determines who explores, decides, executes, verifies, receives evidence, and maintains continuity. It also changes future relational state.

Let:

```text
R(t) = responsibility / authority arrangement
D(t) = delegated cognition and action
A(t) = consequential participant asymmetries
```

Then, provisionally:

```text
R(t)
→ defines capability / evidence demand
→ changes which A(t) matters
→ influences D(t)

D(t)
→ changes practice, local evidence, anchoring, and information access
→ changes participant state and A(t+1)

A(t+1)
→ may justify revised support or delegation
→ can sometimes motivate reconsideration of R(t+1)
  subject to normative / legal / value constraints
```

Responsibility, delegation, and asymmetry are therefore a constrained feedback system, not a one-way hierarchy.

## 3. Shared substrate and state coordination

Let `E(t)` denote authorized external task state such as files, diffs, tests, tables, plans, logs, source documents, issue state, or visual interfaces.

```text
participant-local state
→ externalization / observable action
→ representation / shared evidence
→ participant-specific perception + inference
→ reconstructed local state
→ grounding / correction / next action
```

Shared visibility does not imply shared meaning.

When one participant performs local work, a useful provisional decomposition is:

```text
Δlocal = Δartifact + Δprivate + Δephemeral
```

- `Δartifact`: recoverable from external evidence;
- `Δprivate`: rationale, uncertainty, surprise, rejected alternatives, intent, or suspicion not fully encoded in artifacts;
- `Δephemeral`: low-value execution noise.

The executor should not automatically narrate all three. Consequential state can instead be replicated, exposed, indexed/addressable, retrieved on demand, or safely left local depending on responsibility and next-action dependencies.

## 4. Coordination economics

Raw execution capability is insufficient for allocation. A provisional analytical decomposition is:

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

This is not a runtime numerical formula. Cheap production does not imply cheap coordination or cheap verification.

Current design discriminators include:

1. **responsibility relevance of delegation** — does delegated cognition overlap capability needed for current or foreseeable responsibility?
2. **value of independent participant signal** — does preserving sufficiently independent cognition improve judgment enough to justify its cost?
3. **selector / verification reliability** — can consequential evidence be distinguished from noise, and can omissions be detected or audited?
4. **cross-participant state-coordination cost** — how expensive is it to make consequential local state usable or retrievable by whoever needs it?
5. **reasoning / recognition dependency** — must knowledge participate directly in downstream reasoning, or merely be recognized and retrieved when relevant?

These are candidate discriminators, not fixed runtime questionnaire fields.

## 5. Representation and cognitive proximity

Informationally similar representations can impose different acquisition, inference, assimilation, and verification costs on different participants.

Representation fitness is therefore participant-, task-, operation-, tool-, context-, and responsibility-relative. Candidate considerations include:

- fidelity and provenance;
- operational affordance;
- current accessibility;
- representational competence;
- responsibility relevance;
- developmental value;
- joint coordination cost;
- return path to richer or authoritative evidence.

The easiest representation now is not always the best long-term representation. If competence with a domain representation is itself required for recurring responsibility, mediation may rationally fade. Conversely, a participant should not be forced to internalize a native representation merely because it exists when responsibility can be substantively exercised through another reliable representation.

The related candidate construct **cognitive placement** is developed separately in [`studies/cognitive-placement-bridge-2026-09-15.md`](studies/cognitive-placement-bridge-2026-09-15.md). It treats "internal / external" as insufficient and asks how cognitively close a structure must be when a dependency arises.

## 6. Epistemic integrity versus disclosure strategy

Epistemic integrity constrains fabrication, unsupported certainty, false evidence claims, and knowingly misleading omission. It does **not** require exhaustive immediate disclosure.

Honest coordination may still use selective sequencing, probes, delayed explanation, compression of low-value noise, preservation of useful divergence, or addressable evidence rather than full replication.

Honesty does not solve mutual opacity: participants can genuinely misjudge what the other knows or what they themselves understand.

## 7. Longitudinal objective

Collaboration does not merely respond to relational state; it produces future relational state.

```text
initial relational state
→ allocation / exposure / representation / delegation
→ cognition + action + evidence
→ learning / anchoring / dependence / search correlation
→ new capability and information distribution
→ next relational state
```

A current candidate objective is:

> Maintain or create a relational state whose participant differences, dependencies, evidence access, capabilities, and coordination structure remain compatible with the desired responsibility structure and future collaboration goals at proportionate joint cost.

This does not imply minimizing asymmetry, maximizing symmetry, maximizing human participation, or maximizing AI delegation.

## 8. Explicit non-claims

This model does not currently claim that:

- all collaboration problems are asymmetry problems;
- asymmetry and dependence/correlation are conceptual opposites;
- shared substrate implies shared meaning or fully correlated errors;
- latent participant state is directly observable;
- full common-ground convergence is desirable;
- more transparency is always better;
- human-first reasoning is universally superior;
- repeated AI delegation necessarily causes capability decline;
- raw/native representations are always superior;
- the same representation or knowledge placement is optimal for human and AI;
- this research model is ready to replace the current specification model.

## 9. Evidence and evolution

Falsifiable claims derived from this model are maintained in [`claim-ledger.md`](claim-ledger.md). Candidate studies that discriminate among competing explanations are maintained in [`studies/README.md`](studies/README.md).

A failed claim should narrow or revise the relevant part of this model rather than being absorbed as another post-hoc explanation.