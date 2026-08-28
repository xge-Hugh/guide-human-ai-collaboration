# Temporal Coordination Field Observation

> Status: field observation / discovery only. This is not a controlled experiment, not a new collaboration norm, and not a requirement to log every wait.

## 1. Decision this observation may inform

The current candidate model proposes that AI latency can create suspended cognitive commitment, blocked-progression polling, and interaction-state conflicts. A newer field clue distinguishes side chat from a second independent chat and proposes rejoin collision: the main thread becomes actionable while an auxiliary side interaction is still unfinished.

The next project decision is not whether to redesign the UI immediately. It is narrower:

> Are these interaction-state costs recurrent and decision-relevant enough to justify a dedicated cognitive-sidecar or other interaction-substrate mechanism?

If not, keep the insight as a bounded observation and do not add mechanism complexity.

## 2. Observation targets

Only retain events that arise naturally and appear informative.

High-value opportunities include:

- a wait becomes subjectively noticeable and the human starts polling, phone checking, note-taking, or another action;
- a side chat is opened while the main thread is waiting;
- the main thread returns before the side prompt or side response is closed;
- streaming starts while the human is elsewhere and the human has to reconstruct the beginning;
- the human needs to reread or reconstruct the parent thread after an auxiliary explanation;
- a low-friction explanation or chunking affordance would clearly have replaced a longer prompt;
- a side chat materially improves explanation, prediction, judgment, or error detection;
- the human deliberately does nothing or rests and later resumes with unusually low cost;
- an apparently helpful proactive explanation instead increases reading burden or distraction.

Do not manufacture these cases.

## 3. Minimal observation record

When a high-value event occurs, preserve only enough information to discriminate mechanisms:

- task / cognitive context;
- what state the main thread was in;
- what the human did during the gap;
- whether a side chat or independent second chat was involved;
- whether the main thread returned before the auxiliary action closed;
- observable recovery or reconciliation cost;
- whether understanding / prediction / judgment improved;
- what competing explanation remains plausible;
- whether this event changes any project decision.

Avoid continuous screen surveillance, physiological sensing, or personality/capability inference.

## 4. Candidate interpretations

### A. Temporal suspension dominates

The main burden comes from being blocked while not knowing whether to remain engaged or disengage. Side chat is secondary.

Prediction: polling, phone checking, and difficulty settling occur even without auxiliary conversations.

### B. Rejoin collision dominates side-chat cost

Side chat is useful while the main thread is unavailable, but main-thread return before side closure creates the largest burden.

Prediction: side chat is beneficial when it closes before the parent thread resumes, and costly mainly when the two become concurrently actionable.

### C. Understanding support dominates

The human opens side chat primarily because the main interaction does not provide enough chunking, explanation, or reconstruction support.

Prediction: low-friction inline explanation or chunking would reduce side-chat use without reducing judgment quality.

### D. Side chat is mostly benign

Auxiliary interactions usually help and rejoin collisions are rare or easy to resolve.

Prediction: observed burden remains small; no dedicated mechanism is justified.

## 5. What would justify a small prototype

Consider a minimal interaction prototype only if repeated field observations show both:

1. the same failure recurs across more than one task/context; and
2. the failure changes understanding, judgment quality, recovery cost, fatigue, or compensatory human coordination work.

Prefer the lowest-risk prototype first:

- selection-aware micro explanation;
- inline chunk anchor;
- one-line reconstruction cue;
- ephemeral scratchpad tied to the parent locus;
- explicit return-to-main affordance.

Do not start with automatic cognitive-state inference.

## 6. Stop / downgrade rule

Do not continue collecting evidence merely because the topic is interesting.

Downgrade or park the candidate if:

- rejoin collisions are rare;
- side chat provides clear net benefit with little reconciliation burden;
- ordinary reconstruction cues already solve the observed problem;
- observation starts requiring artificial tasks or continuous logging;
- proposed support adds more explanation or UI state than the burden it removes.

The purpose of this field pass is discovery and discrimination, not confirmation.


## 7. Event-contingent "cue now, reflect later" protocol

The observation should not depend on sudden inspiration or memory at the end of the week.

Use a small set of predefined **event triggers**. When one happens naturally, capture only a minimal cue. Do not stop the collaboration to write a full diary entry.

### 7.1 Trigger set

A capture opportunity exists when any of the following becomes consciously noticeable:

- **P — Poll**: an urge to check whether the AI has progressed/completed;
- **M — Monitor**: choosing to watch thinking/status/streaming mainly to stay coupled rather than because a specific evidence-bearing detail is needed;
- **F — Phone / low-friction switch**: reaching for social media/messages/another low-threshold activity during the wait;
- **S — Side chat**: opening or composing an attached side interaction;
- **C — Collision**: the main thread becomes actionable while the side interaction or alternative activity is still cognitively unfinished;
- **R — Release / rest**: deliberately letting go, resting, walking away, or waiting without new input;
- **K — Checkpoint**: deliberately re-entering only at a meaningful review/evidence checkpoint instead of monitoring continuously;
- **X — Unexpected**: another interaction-state event that appears important and is not covered above.

These are observation labels, not diagnoses.

### 7.2 Immediate capture

At the moment of the event, preserve only:

`code + optional 3–10 word cue`

Examples:

- `P — next step blocked`
- `C — main returned before side prompt`
- `R — looked away; no phone`
- `K — reviewed test failure only`

A timestamp may be added automatically by the capture tool, but exact latency measurement is not required for discovery.

The cue should take less cognitive effort than reconstructing the event later. If recording the cue itself feels disruptive, skip it.

### 7.3 Delayed reflection

At a natural task checkpoint or retrospective, expand only the cues that still appear decision-relevant:

1. **What was I waiting for / trying to understand?**
2. **What did I do with my attention?**
3. **What happened when the main thread became actionable again?**
4. **Did this help or hurt understanding, judgment, fatigue, or recovery?**
5. **What competing explanation fits this event?**

Do not fill missing detail from imagination. "Unknown / cannot reconstruct" is valid evidence about observability.

### 7.4 Counterexamples matter

Capture positive cases as well as friction:

- monitoring caught a real error early;
- resting made re-entry easier;
- resting made the human too out-of-loop to judge;
- side chat closed cleanly and substantially improved understanding;
- a checkpoint review preserved judgment without continuous monitoring.

The purpose is to discriminate, not accumulate complaints.

## 8. Promotion path for interaction-substrate candidates

This class of candidate should not be forced through a Skill pilot when the Skill cannot observe or instantiate the mechanism.

A provisional evidence route is:

```text
field clue
→ cloud conceptual / research calibration
→ event-contingent field sampling
→ recurring mechanism + counterexamples
→ lowest-risk interaction/substrate prototype
→ naturalistic within-person comparison / field pilot
→ independent evidence review
→ classify outcome:
     conceptual model / failure model / guidance /
     UI-substrate requirement / norm / parked
```

The prototype is the **pilot carrier**, but for this class it may be an interaction affordance rather than a Skill.

Examples:

- a one-action inline explanation;
- a reconstruction cue after long execution;
- a checkpoint-only review surface;
- an ephemeral sidecar;
- a passive/optional progress or cognitive anchor.

A Skill can still participate when the candidate concerns model behavior, such as when to expose a direct evidence slice. It should not be treated as the mandatory carrier for phenomena that occur while the model is silent or that depend on UI-level branch/rejoin behavior.

## 9. Small within-person discrimination when field clues repeat

If natural observations repeatedly support a specific competing pair, a small self-comparison can reduce reliance on intuition.

For example, on naturally similar low-risk waits:

- **continuous-monitor condition**: watch thinking/progress as normally done;
- **release condition**: deliberately disengage until completion/checkpoint;
- **punctuated-oversight condition**: disengage from execution but re-enter at a selected evidence-bearing checkpoint.

Compare only practical outcomes:

- subjective fatigue / agitation;
- ease of resumption;
- ability to explain what the AI did;
- ability to detect a real issue or ask a discriminating question;
- rereading / reconstruction needed;
- whether the monitoring information actually changed a decision.

This is an N-of-1 discovery method, not population evidence. Do not randomize or manipulate high-risk tasks merely for the study.

## 10. Evidence threshold for the next decision

Move from observation to a prototype only when there is at least:

- recurrence across more than one real task/context;
- at least one meaningful counterexample or boundary case;
- a plausible mechanism that predicts a different design;
- a concrete human cost or judgment benefit that the candidate mechanism could change.

If the only evidence remains "this feels interesting," keep the candidate preserved but do not escalate.
