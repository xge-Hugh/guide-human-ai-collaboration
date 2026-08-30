---
name: human-ai-evidence-assurance
description: Evaluate claims, evidence, provenance, conflicts, independence, and validation boundaries when a decision or review depends on what is actually established. Use for source conflict, high-impact verification, independent review, anomalous evidence, substantive model revision after new evidence, or assurance design. Skip simple factual questions and low-risk tasks whose evidence boundary is already clear.
---

# Human-AI Evidence and Assurance

Use this Skill when the collaboration needs to determine what a claim is supported by, what remains unknown, or how much assurance an action deserves.

## Runtime behavior

1. **State the actual claim.** Distinguish observation, inference, causal explanation, value judgment, recommendation, and unknown.

2. **Match evidence to the relevant failure mode.** Ask what the evidence can discriminate or rule out. Test count, fluent explanation, confidence, or final task success do not substitute for evidence at the failing boundary.

3. **Preserve provenance.** A summary, table, task view, generated plan, or AI explanation is a derived representation. When it bears on consequential judgment, keep a path to the relevant source and identify material transformation or omission.

4. **Resolve conflicts semantically.** First determine whether two statements truly conflict or differ by scope, abstraction, time, or wording. Check verifiable facts directly. Escalate only the unresolved difference that changes direction, responsibility, risk, or action.

5. **Evaluate independence relative to the target failure source.** A different reviewer, model, agent, session, or phrasing is not enough by itself. Identify which information, assumptions, reasoning context, method, or evidence-generation path must be separated.

6. **Make bearing model revision observable.** If new evidence materially changes a prior judgment, briefly settle:
   - prior judgment;
   - new evidence;
   - revised conclusion;
   - what remains valid or unknown;
   - what changes next.
   Do not turn minor wording edits into meta-analysis.

7. **Use anomalous direct evidence proportionally.** A low-frequency trace, failure, or source fragment deserves attention when it can change the claim or risk model. Do not dump raw material when a smaller discriminating slice is enough.

8. **Keep assurance claims bounded.** Distinguish carrier structure, runtime behavior, execution assurance, task outcome, and human capability evidence. Passing one layer does not prove the others.

## Review behavior

Before calling a review independent, identify the failure source it is intended to control and the actual separation used. Before treating a test suite as sufficient, identify which consequential failures it can and cannot expose.

Stop when the decision-relevant claim has sufficient evidence for the current risk, has been explicitly bounded as unknown, or has been routed to a stronger validation path.
