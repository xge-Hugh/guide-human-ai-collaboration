# Field evaluation for the research-informed pilot

This is an optional research instrument, not a per-task form or automatic telemetry. Capture a useful episode in the existing [feedback stream](../../feedback/README.md); short factual notes are enough. Do not invent observations to fill fields or automatically modify the carrier from its own reflections.

## Minimal observation

```text
Date / task / trace or artifact:
Installed carrier commit (or base commit + local diff), host and model if known:
Opportunity: what observable situation made a behavior relevant?
Guidance: rule present? Skill actually loaded? targeted source read? unknown?
First response / action and its consequence:
Outcome: pass | recovered | fail | not_observed
Correction or compensatory human work, if any:
```

Keep observation separate from explanation. For example, “metadata validation was omitted from the first report and surfaced after a question” is an observation; “the selector failed” is a hypothesis unless loading and selection evidence support it. Record an authorized trace pointer or a small redacted excerpt; avoid copying unrelated private task data.

When available and useful, add:

- which new assumption, evidence substitution, or anomaly became visible, and whether it changed judgment;
- whether evidence was actually accessible, inspected, fresh, and sufficient to detect a mistaken summary;
- time/attention, redundant questions, rereading, retrieval failures, or review burden, measured or explicitly estimated;
- whether guidance was automatic, explicitly invoked, read before the task, or reactivated after a miss;
- prior concept exposure and a later natural recognition, prediction, correction, or transfer, with support conditions;
- a competing explanation and a relevant case ID or research claim, if identifiable.

Unknown loading is `unknown`, not “Skill failed to route.” A task without a discriminating opportunity is `not_observed`. Correct non-intervention at an explicit negative-case opportunity can be `pass`. Correction never converts first-opportunity failure into `pass`.

## Manual replay

Use [cases.json](evals/cases.json) as review criteria, not a completed result set. It is not wired into the assurance runner and has no automatic pass claim.

1. In a fresh session, install the rule and make the two Skills available. Present only the case scenario and any necessary raw artifacts; keep expectations out of the task prompt.
2. Capture the first response and relevant tool/load evidence before any correction. Evaluate the observable expectations and routing separately. A good answer with unknown loading does not establish routing reliability.
3. If correction is needed, retain it and the subsequent behavior. Classify first-opportunity success, recovery, unresolved failure, or lack of a discriminating opportunity.
4. Include negative cases as well as positive ones. For combined cases, check that each treatment contributes without duplicating explanations or creating new approval gates.

For a comparison, use the same task inputs and host/model settings in separate fresh sessions with the pre-update carrier at `62d3b6d` and this revision. Record actual installed commits; vary session order where feasible. Compare task quality, consequential omissions, human correction, and coordination cost. Keep task-first automatic routing and explicit source orientation as separate conditions. Do not expose evaluation expectations to either condition or call the comparison independent when it shares a relevant error source.

## Return to research

| Question | Evidence that could narrow or reject the treatment |
| --- | --- |
| Does action-sufficient alignment reduce cost? | Additional rework or hidden differences outweigh saved discussion |
| Does selective delta improve judgment (A3a/A3b)? | Important omissions survive the audit path, or final summaries perform equally well at comparable cost |
| Does source contact improve review (A4/A11)? | It adds inspection burden without changing discrimination |
| Do concept seeds help later reasoning? | Repeated distraction, false confidence, or no useful reuse across actual later opportunities |
| Does placement fit the task (A14–A17)? | Links fail to support reasoning, cues miss relevant retrieval, or resident guidance creates false activation |
| Does the carrier activate reliably? | Good behavior requires repeated human prompting or explicit orientation despite automatic availability |

Link observations to the [claim ledger](../../docs/research/collaborative-relations/claim-ledger.md) or the relevant cognitive-coordination study when interpreting them. Record supporting, narrowing, non-discriminating, threatening/rejecting, or still-unknown evidence for the particular claim. Keep carrier behavior, task outcome, human capability, and longitudinal transfer distinct. A single successful task or replay cannot validate the model or demonstrate lasting learning.
