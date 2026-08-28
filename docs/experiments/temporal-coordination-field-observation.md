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
