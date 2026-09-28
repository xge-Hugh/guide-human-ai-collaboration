# Human-human handoff mechanisms for post-delegation human robustness

- **Date**: 2026-09-29
- **Status**: external-research synthesis / candidate mechanism extraction
- **Program**: collaborative relations
- **Primary question**: What mechanisms in effective human-human delegation, review, handoff, and workplace learning plausibly transfer to human-AI post-delegation coordination?
- **Relation**: follows [post-delegation human robustness](../post-delegation-human-robustness-2026-09-29.md)
- **Evidence boundary**: these literatures concern human-human teams and learners. They provide candidate mechanisms and boundary conditions, not direct validation for human-AI collaboration.

## 1. Why this route is useful

The γ-I AI-recipient replay demonstrated that a controlled apparatus can distinguish information surfaces, but it cannot establish how human recipients understand, assimilate, or learn from delegated work.

Human-human collaboration gives a stronger starting point for human-centered candidate mechanisms because the recipient is actually human. The transfer problem then becomes explicit:

~~~text
human-human mechanism
→ coordination problem it solves
→ assumptions it relies on
→ which assumptions survive H-AI asymmetry?
→ candidate H-AI mechanism
→ field observation / later discrimination
~~~

The goal is not to copy existing formats such as I-PASS or code-review templates into AI reports.

## 2. Mechanism A — orientation before analytical review

Recent think-aloud research on code review modeled review as an early **orientation phase** followed by iterative comprehending, assessing, and deciding. Reviewers first sought expectations, context, and rationale; comprehension of the code was a prerequisite for the decision rather than the endpoint.

Earlier industrial code-review research likewise found that change/code understanding was a central challenge and that review produced benefits beyond defect discovery, including knowledge transfer, team awareness, and alternative solutions.

### Candidate transfer

A post-delegation human review may need an orientation surface before implementation detail:

~~~text
purpose / intended change
+
relevant invariants
+
why this implementation exists
+
scope / boundaries
        ↓
targeted artifact and evidence inspection
~~~

This suggests that a diff or execution trace is often a poor first representation when the recipient has not reconstructed the change story.

### Boundary

Human reviewers often share substantial repository, team, and product context. AI may have accumulated much more local execution context than the human during delegation, increasing the orientation gap.

The mechanism should therefore optimize for **reconstructing the decision frame**, not reproducing all executor context.

## 3. Mechanism B — handoff is closed-loop, not sender-only

Healthcare handoff research provides an unusually explicit receiver-side mechanism.

The I-PASS structure includes:

- severity/current state;
- summary;
- action list;
- situation awareness and contingency planning;
- **synthesis by receiver**: the receiver summarizes what was heard, asks questions, and restates key actions.

AHRQ presents receiver synthesis as part of the handoff rather than optional conversational polish. Multicenter I-PASS evidence has been associated with reductions in medical errors; a recent Making Healthcare Safer review rated evidence for I-PASS more favorably than many alternative structured handoff tools.

Safety-critical shift-handover research also found fewer task errors when written material was supplemented by richer briefing modalities. Face-to-face handover allowed questions and rephrasing that can expose differences in mental models, although the experimental result does not isolate questioning as the sole causal mechanism.

### Candidate transfer

Human-AI settlement should not be modeled only as:

~~~text
AI reports
→ human receives
~~~

A more plausible structure is:

~~~text
AI reports / exposes
        ↓
human reconstructs:
"my understanding is..."
"the unresolved boundary is..."
"the next evidence I need is..."
        ↓
AI confirms, corrects, or points to evidence
~~~

This makes misunderstanding observable.

### Boundary

For ordinary low-risk AI work, mandatory read-back would be costly ritual. Receiver synthesis should be conditional on responsibility, ambiguity, novelty, or consequence.

The human's natural questions may be more informative than a fixed template.

## 4. Mechanism C — transfer future-oriented contingencies, not only current state

I-PASS does not stop at a snapshot. It explicitly includes action ownership and contingency planning: what may happen next and what should be done if it does.

This matters because a recipient does not merely need to know what the outgoing worker did; the recipient must continue the work under uncertainty.

### Candidate transfer

Post-delegation AI reporting may need to distinguish:

~~~text
current state
from
decision-relevant future boundary
~~~

Examples:

- what assumption would invalidate the chosen implementation;
- what condition should trigger revalidation;
- what unresolved risk is safe to defer and until when;
- what future architecture pressure would make another implementation preferable.

This directly supports the candidate "switch condition" component of contrastive abstraction.

### Boundary

Do not turn every task into exhaustive scenario planning. Contingencies should be selected by consequence and plausible dependency on the next responsible action.

## 5. Mechanism D — distributed knowledge can remain distributed if its location is known

Team-cognition research distinguishes two related structures:

- **shared mental models**: sufficiently compatible understanding of task, environment, roles, or strategy;
- **transactive memory systems (TMS)**: differentiated knowledge distributed across members plus shared awareness of who knows what and how to access it.

Research on TMS emphasizes specialization, knowledge-location awareness, and retrieval/coordination rather than requiring every team member to internalize the same content. Studies in organizational and software-team contexts associate TMS with more effective communication, coordination, and knowledge sharing.

### Candidate transfer

This provides an external analogue for the project's distinction:

~~~text
state replication
≠
state addressability
~~~

A human does not need all executor-local details internalized if the collaboration preserves reliable meta-knowledge:

- what kind of evidence exists;
- where it resides;
- what it can establish;
- when it should be retrieved;
- what cannot be reconstructed from artifacts alone.

This suggests a post-delegation target of **shared decision frame + reliable evidence addressability**, not complete state synchronization.

### Boundary under H-AI asymmetry

Human-human TMS often relies on relatively persistent people, expertise reputation, and social credibility. AI runtime identity, memory, model version, and tool access can change between sessions.

Therefore the H-AI analogue may need to anchor knowledge location in **artifacts and provenance**, not merely "the AI knows this."

## 6. Mechanism E — review transfers rationale and alternatives, but retention is fragile

Industrial code-review studies report that review supports knowledge transfer and creation of alternative solutions, not only defect detection. Research at Microsoft also found code review to be a point where design rationale becomes explicit, while later retention and recovery of that rationale were poorly supported.

Recent review research similarly emphasizes that reviewers seek rationale and information outside the diff/tool when the change cannot be understood from code alone.

### Candidate transfer

A high-value AI completion report may need to expose selected design rationale:

~~~text
goal / invariant
→ alternatives that were actually plausible
→ chosen approach
→ decision criterion
→ trade-off
→ switch condition
~~~

This is stronger than narrating the execution trace because it encodes a reusable discrimination structure.

It also suggests that rationale should be made **addressable after the immediate conversation**, because a transient explanation may support current approval but fail longitudinally.

### Boundary

Reporting hypothetical alternatives that were never meaningful can create explanation theater.

The useful target is not "list three alternatives." It is:

> expose the distinctions that materially governed the implementation choice or would govern a future nearby choice.

## 7. Mechanism F — experiential compensation requires visible expert decision structure, not hidden reasoning

Cognitive-apprenticeship research emphasizes making expert cognitive and metacognitive processes visible through methods such as modeling, coaching, scaffolding, articulation, reflection, and exploration. Workplace/clinical studies use these methods to support learning in authentic practice rather than only transmitting declarative instructions.

### Candidate transfer

When AI executes work that the human would otherwise have learned through doing, selective exposure can compensate for part of that lost experience by making **decision structure** visible:

- what feature of the situation mattered;
- what competing strategy was plausible;
- what evidence discriminated them;
- what trade-off was accepted;
- what the human should recognize next time.

This supports the candidate mechanism of contrastive abstraction and the distinction between production execution and capability-maintenance execution.

### Important boundary

Human-AI collaboration should **not** treat access to private model chain-of-thought as the analogue of expert modeling.

The useful transferable object is an externally checkable rationale structure:

~~~text
observable condition
→ decision criterion
→ chosen action
→ evidence / trade-off
~~~

not an unverifiable reconstruction of hidden internal reasoning.

## 8. Cross-domain synthesis

The strongest recurring mechanisms can be organized against the three post-delegation obligations.

| Obligation | Human-human mechanism | Candidate H-AI translation |
| --- | --- | --- |
| Invariant assurance | structured review/handoff, new pair of eyes, standardized critical fields | preserve agreed constraints and expose evidence/provenance for them |
| State settlement | orientation, action list, contingency, receiver synthesis | purpose/invariants → consequential delta → human reconstruction/questions |
| Distributed state | transactive memory / knowledge-location awareness | shared decision frame + artifact/evidence addressability |
| Experiential compensation | rationale exchange, alternative solutions, cognitive apprenticeship | contrastive abstraction + selective native artifact contact |
| Longitudinal continuity | retained review rationale / shared team awareness | persistent source pointers, rationale records, revisitable decision boundaries |

This is not yet a final reporting schema. It is a mechanism inventory.

## 9. Important transfer failures to avoid

### 9.1 Do not equate structure with effectiveness

Structured human handoffs can reduce omissions, but rigid templates can become ritual. H-AI reporting should remain conditional and consequence-sensitive.

### 9.2 Do not require full shared mental models

TMS evidence suggests that differentiated knowledge can be healthy when location and retrieval are reliable.

### 9.3 Do not confuse rationale with persuasion

The executor's explanation is itself a fallible representation. Evidence/provenance and an independent return edge remain necessary when responsibility depends on it.

### 9.4 Do not optimize only immediate acceptance

Human-human review and apprenticeship have learning/awareness functions. A reporting design that maximizes today's acceptance efficiency can still weaken future human judgment capability.

### 9.5 Do not infer human outcomes from AI-recipient replay

AI replay remains useful for apparatus, AI-side reconstruction, and adversarial packet tests, not as evidence that humans assimilate the same representation similarly.

## 10. Candidate post-delegation interaction architecture

A provisional architecture emerging from the literature is:

~~~text
1. ORIENT
   purpose + scope + invariants + decision frame

2. ASSURE
   whether invariants held + evidence/provenance

3. SETTLE
   consequential new state, uncertainty, substitutions, contingencies

4. RECONSTRUCT
   human asks/restates/selects evidence where responsibility warrants

5. EXPOSE SELECTIVELY
   rationale, alternatives, trade-offs, switch conditions,
   representative native artifacts when longitudinal value is high

6. LEAVE ADDRESSABLE
   detailed evidence and rationale that need not be internalized now
~~~

This should **not** be promoted into guidance yet.

The next empirical question is which components have enough marginal value in actual human-AI daily work to justify attention cost.

## 11. Focused next field step

Before another controlled experiment, use the historical project corpus and future daily collaboration to look specifically for episodes where:

- an invariant was preserved but the human still lacked useful implementation understanding;
- rationale/alternative exposure changed a later decision;
- a human receiver synthesis/question exposed a misunderstanding;
- evidence addressability substituted successfully for narration;
- a report was sufficient for immediate acceptance but insufficient for later capability;
- hands-on artifact contact produced a distinction that prose did not.

The first prospective pilot should test **one mechanism at a time**, preferably contrastive rationale or receiver reconstruction, rather than deploying the full six-part architecture.

## Sources

1. Söderberg et al., "Code review as decision-making - building a cognitive model from the questions asked during code review," Empirical Software Engineering, 2025. https://link.springer.com/article/10.1007/s10664-025-10791-2
2. Bacchelli & Bird, "Expectations, Outcomes, and Challenges of Modern Code Review," ICSE 2013 / Microsoft Research. https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/
3. Sutherland & Venolia, "Can Peer Code Reviews be Exploited for Later Information Needs?", ICSE 2009 / Microsoft Research. https://www.microsoft.com/en-us/research/publication/can-peer-code-reviews-be-exploited-for-later-information-needs/
4. AHRQ TeamSTEPPS, "I-PASS." https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/ipass.html
5. Starmer et al., "Changes in Medical Errors after Implementation of a Handoff Program," New England Journal of Medicine, 2014. https://www.nejm.org/doi/full/10.1056/NEJMsa1405556
6. Shekelle et al., "Use of structured handoff protocols for within-hospital unit transitions: a systematic review from Making Healthcare Safer IV," BMJ Quality & Safety, 2025. https://qualitysafety.bmj.com/content/early/2025/04/29/bmjqs-2024-018385
7. Parke, Hobbs & Kanki, "Passing the Baton: An Experimental Study of Shift Handover," NASA/HFES, 2010. https://ntrs.nasa.gov/citations/20110008267
8. Ishikawa et al., "Team implicit coordination based on transactive memory systems," Team Performance Management, 2020. https://www.sciencedirect.com/org/science/article/pii/S1352759220000123
9. Stalmeijer et al., "Cognitive apprenticeship in clinical practice," Advances in Health Sciences Education, 2009. https://link.springer.com/article/10.1007/s10459-008-9136-0
10. Lyons et al., "Cognitive apprenticeship in health sciences education: a qualitative review," Advances in Health Sciences Education, 2017. PubMed: https://pubmed.ncbi.nlm.nih.gov/27544386/
