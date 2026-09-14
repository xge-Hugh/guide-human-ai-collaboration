# Cognitive placement bridge — human capability and AI runtime

- **Date**: 2026-09-15
- **Status**: `candidate / cross-program research synthesis`; not current specification, guidance, or carrier architecture
- **Program**: collaborative relations
- **Related**: [`../README.md`](../README.md), [`../../runtime-capability/model.md`](../../runtime-capability/model.md), [`../../cognitive-coordination/model.md`](../../cognitive-coordination/model.md), [`../../cognitive-coordination/studies/progressive-schema-formation-through-strategic-exposure-2026-09-11.md`](../../cognitive-coordination/studies/progressive-schema-formation-through-strategic-exposure-2026-09-11.md), [`../../../spec/model.md`](../../../spec/model.md)

## 1. Why record this

The collaborative-relations inquiry produced a recurring placement question:

> when should task-relevant knowledge be locally usable, when is a compact index enough, when should richer structure be conditionally reconstructed, and when should information remain externally addressable?

The same structural question already appears on the AI side in the runtime-capability program. That program distinguishes parametric capability, context-conditioned capability, and externally persistent capability; treats compact resident cues, Skills and retrieval as different activation surfaces; and identifies a selector bottleneck when the knowledge needed to recognize relevance is hidden behind the trigger that requires that recognition.

On the human side, cognitive-coordination research has independently distinguished strategic exposure, reconstruction, responsibility-related capability, and progressive schema formation. A concept may begin as a weak index, later be reactivated by a live anomaly, and eventually become a reusable task model.

The current synthesis asks whether these are instances of one deeper placement problem without assuming that humans and AI learn through the same mechanism.

## 2. Candidate bridge: cognitive placement

**Cognitive placement** is the problem of deciding where task-relevant structure should reside, in what representation and availability mode, so that recognition, reasoning, verification, retrieval, capability development, and coordination remain effective at proportionate total cost.

This is not a new claim that cognition literally occurs in the same way in humans and AI. It is a proposed common **control problem** across participants and carriers.

A storage-centric distinction such as `internal vs external` is too coarse. An external circuit diagram kept continuously visible may participate in human reasoning with lower friction than a poorly remembered internal fact. Likewise, a compact AI cue already in context may be functionally closer than a richer Skill whose relevance is never recognized.

Therefore the more useful candidate variable is **cognitive proximity**:

> how reliably, quickly, and cheaply a representation can become usable when a dependency arises.

Cognitive proximity can depend on retrieval latency, recognition reliability, representation fitness, interpretation cost, freshness, provenance, tool access, and context/attention interference.

## 3. Availability modes

The inquiry currently distinguishes five useful modes rather than one residency hierarchy.

### 3.1 Locally usable structure

Structure that can participate directly in current reasoning with little reconstruction cost.

Examples:

- human: an operational schema for object lifetime, a currently visible circuit diagram, a well-practiced diagnostic model;
- AI: reliable parametric capability or a sufficiently rich current-context representation.

### 3.2 Resident orientation / index

A compact cue that supports framing, relevance recognition, routing, or remembering that deeper material exists.

Examples:

- human: “dependency injection → lifetime / construction / ownership”;
- AI: a compact resident invariant or recognition cue.

An index is not mastery. Its value may be primarily to reduce the distance to later reconstruction.

### 3.3 Conditionally reactivated structure

A richer representation loaded only after relevance is recognized.

Examples:

- human: notes, worked example, saved decision record, earlier conceptual explanation;
- AI: Skill, retrieved procedure, relevant case, targeted canonical section.

### 3.4 Externally addressable knowledge

Large, exact, infrequent, authoritative, or source-sensitive information that can remain outside active cognition while retaining a reliable retrieval path.

Examples include SDK syntax, detailed reference material, papers, specifications, logs, and canonical project knowledge.

### 3.5 External capability / live state

Information or action that must be obtained from the current environment rather than remembered.

Examples:

- human: calculator, IDE, measuring instrument, live dashboard;
- AI: MCP/tool/service call, repository inspection, current API state, execution environment.

The access surface is not itself the knowledge architecture; it exposes external state or capability.

## 4. Two distinct dependencies

### 4.1 Reasoning dependency

A representation has high **reasoning-dependency depth** when later judgment repeatedly and compositionally requires it to generate, connect, discriminate, predict, or verify downstream conclusions.

Exact SDK syntax is often low in reasoning dependency: it can be looked up at use time. Concepts such as distribution, mutual exclusion, lease ownership, or failure semantics can be high in reasoning dependency when designing a distributed lock.

### 4.2 Recognition dependency

A representation has high **recognition dependency** when some part of it must already be cognitively near in order to notice that deeper retrieval or a different mechanism is relevant.

This creates a selector failure:

```text
need K to recognize that K matters
        ↓
must recognize K matters to retrieve K
        ↓
K remains external and is never retrieved
```

A compact cue/index can therefore be valuable even when the complete knowledge should remain external.

## 5. Candidate placement principles

These are research hypotheses, not current norms.

### P1 — dependency proximity

The more frequently and compositionally a structure participates in consequential reasoning, the lower its effective cognitive distance should usually be.

This does **not** imply that it must be memorized internally. A continuously available external representation can sometimes be cognitively proximal enough.

### P2 — recognition-before-retrieval

When recognition of relevance depends on knowledge that would otherwise be hidden behind the retrieval boundary, preserve enough local orientation to trigger the correct retrieval or escalation path.

### P3 — external-authority advantage

Large, volatile, exact, infrequently used, security-sensitive, or provenance-critical information may be better kept in an authoritative external source even when consequential. Local structure may encode stable relations and the condition for retrieval rather than the transient fact itself.

### P4 — return-edge requirement

Compact indexes, summaries, Skills and derived representations should preserve an appropriate return path to richer or more authoritative evidence when omission, ambiguity, staleness, or responsibility requires it.

### P5 — duplication is conditional

The same knowledge need not be fully replicated across human and AI. Duplication is useful when it lowers consequential latency or failure risk enough to justify maintenance and inconsistency cost. Otherwise addressable specialization can be healthy.

### P6 — placement is longitudinal

Placement can change over time. Human repeated task-grounded exposure may convert an index into a durable usable schema. AI project runtime, absent model-weight change, usually requires external persistence and later reactivation rather than assuming equivalent durable internalization.

## 6. Structural symmetry, mechanism asymmetry

Human and AI both face limited active cognitive resources plus much larger potentially useful external resources. Both therefore face a placement problem:

```text
what stays near the active reasoning loop?
what only needs an index?
what is reconstructed conditionally?
what stays externally retrievable?
```

But their state transitions differ.

### Human side

Repeated retrieval, strategic exposure, live evidence, practice and reconstruction can alter durable future capability. The human may gradually need less mediation, and representation competence itself can become responsibility-relevant.

### AI runtime side

Current context can strongly reorganize behavior without changing model weights. Project-specific knowledge often remains dependent on context construction, retrieval, Skills, external persistent state, or validated guidance. The system must therefore re-establish relevant structure across sessions or long tasks.

Additional asymmetries include different attention limits, fatigue/context interference, externalization cost, retrieval mechanisms, updateability, and evidence access.

The bridge is therefore:

> **same abstract placement/control problem; different participant-specific learning and persistence dynamics.**

## 7. Relation to existing project mechanisms

This synthesis currently looks like a bridge across existing constructs rather than a new top-level mechanism.

- **strategic exposure** changes human cognitive proximity to evidence and potentially future schemas;
- **progressive schema formation** can move a human representation from index → reactivation → task-grounded structure → reusable model;
- **reconstruction** restores usable structure after context decay;
- **cognitive allocation** evaluates whether bringing information closer to active cognition is worth its cost;
- **runtime capability** determines how AI knowledge is activated, routed, retrieved, persisted and re-established;
- **Skill / retrieval architecture** can implement conditional reconstruction, but their effectiveness depends on recognition and selector reliability;
- **shared substrate / representation mediation** can make external information functionally proximal without forcing internal replication.

## 8. Falsifiable claims

### A16 — recognition-proximity requirement

**Claim**: if knowledge is required to recognize when a deeper resource is relevant, fully externalizing that knowledge behind the same relevance-dependent retrieval boundary should increase missed retrieval or misrouting; a compact resident cue/index should improve recognition at lower cost than keeping the full resource resident.

**Weakening / rejection**:

- retrieval-only architectures reliably invoke the correct resource without local recognition structure;
- compact cues create enough false activation or context interference to erase their benefit;
- full residency consistently dominates without material attention/context cost.

### A17 — dependency-sensitive placement

**Claim**: across human and AI collaborators, reasoning-heavy or recognition-heavy structure should benefit from lower cognitive distance, while exact, large, volatile, infrequent or authority-sensitive material should often benefit from external addressability.

**Weakening / rejection**:

- one simple placement strategy reliably dominates after retrieval quality, tools, support, and task type are controlled;
- the proposed dependency classes fail to predict errors, latency, transfer, retrieval behavior, or context cost better than simpler variables such as frequency alone.

## 9. Candidate study ζ — placement signatures

Do not force one identical experiment across human and AI. Test the same predicted task × placement interaction with participant-specific implementations.

### ζ-H: human placement

Conditions:

1. full instruction / high internalization support;
2. usable conceptual schema + external reference;
3. compact concept index + external reference;
4. lookup-only.

### ζ-A: AI placement

Conditions:

1. complete relevant theory resident in context;
2. compact recognition kernel + conditional Skill;
3. compact index + canonical retrieval;
4. external resource only, without resident recognition cue.

### Task classes

- **reference-heavy**: exact syntax, flags, constants;
- **recognition-critical**: the main failure is noticing which theory/resource applies;
- **reasoning-compositional**: concepts are repeatedly required to derive later judgments;
- **volatile/source-sensitive**: current authoritative state should be externally checked rather than remembered.

### Measures

- task quality and latency;
- missed and irrelevant retrieval;
- false routing / false activation;
- verification and error detection;
- context or attention cost;
- later transfer / reconstruction;
- recovery when the external store is unavailable;
- source/provenance errors.

The central prediction is an interaction, not a universal winner.

## 10. Adjacent external evidence

This synthesis is consistent with, but not established by, several external lines of work:

- cognitive-offloading reviews report immediate performance benefits but costs when external access is unexpectedly lost;
- external-representation research argues that artifacts can transform the inferential cost structure rather than merely store information;
- recent agent-memory research separates working context from persistent memory, dynamically manages storage/retrieval, and reports trade-offs between retrieval quality, latency and context efficiency.

These literatures use different tasks and mechanisms and should not be treated as direct validation of the cross-participant bridge.

## 11. Explicit non-claims

This synthesis does not claim that:

- human memory and AI context are mechanistically equivalent;
- all important knowledge should be resident;
- all frequently used knowledge should be memorized;
- external representations are merely storage devices;
- Skills or MCP are themselves the knowledge architecture;
- retrieval can substitute for responsibility-relevant conceptual structure in every task;
- durable human learning can be inferred from successful AI-style context loading;
- the proposed placement principles are ready for specification or carrier promotion.

The intended next step is discriminating study design and field observation, not implementation of a universal memory hierarchy.