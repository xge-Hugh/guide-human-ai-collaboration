# Cursor Human–AI Collaboration Carrier v2

> Status: **experimental exposure revision** derived from field evidence from Cursor carrier v1.
>
> Primary host: **Cursor Agent (Chat)**.
>
> Purpose: test whether the project's cognitive-coordination and reconstruction candidates can actually enter ordinary collaboration often enough to be evaluated, while preserving sparse visible intervention and no-op behavior.

## Why v2 exists

Carrier v1 produced a strong field asymmetry:

- the small resident authority / epistemic kernel appeared behaviorally influential;
- `human-ai-model-coordination` and `human-ai-reconstruction` were rarely discovered unless manually invoked;
- ordinary model-building behavior such as confusion, paraphrase, prediction, causal challenge, and revision often proceeded through native-model behavior without the candidate treatments;
- long, dense assistant-generated reasoning rarely produced reconstruction support unless the human explicitly reported forgetting.

This means v1 has weak **treatment exposure** for the mechanisms it was intended to validate.

That observation is evidence about the carrier and its operationalization. It is not, by itself, negative evidence that the underlying cognitive-coordination or reconstruction hypotheses are ineffective.

v1 remains unchanged as the comparison baseline.

## Experimental change

v2 tests one main hypothesis:

> **Cognitive coordination should be continuously/frequently eligible, while substantive visible intervention remains conditional.**

The carrier therefore separates:

```text
mechanism relevance
!=
Skill activation
!=
visible intervention
```

A cognitive mechanism may shape an ordinary response without producing a question, Context card, quiz, explicit mode switch, or other visible ceremony.

## Architecture

```text
Cursor User Rule
  ├─ collaboration-state integrity
  ├─ epistemic integrity
  ├─ substantive human responsibility
  ├─ cognitive coordination sensitivity     NEW / broadened
  └─ proportionality / no-op boundary

conditionally expanded Agent Skills
  ├─ human-ai-model-coordination
  │    ├─ ordinary model-building signals   BROADENED
  │    ├─ externalization / discrimination
  │    ├─ selective cross-level probing
  │    ├─ strategic substrate contact
  │    ├─ revision / selective revalidation
  │    └─ productive divergence
  │
  └─ human-ai-reconstruction
       ├─ reconstruction-risk inference      BROADENED
       ├─ embedded bridge cues
       ├─ minimum sufficient reconstruction
       └─ return cues at observable open loops
```

The resident layer does **not** contain the full cognitive model. Its role is to prevent the cognitive candidates from disappearing from the causal path merely because no major decision or explicit forgetting event has occurred.

The Skills remain the richer treatment surfaces.

## Observable signals, not mind-reading

v2 distinguishes private human state from observable interaction structure.

The AI still cannot directly know whether the human remembers, understands, is confident, or is capable.

It can observe:

- explicit confusion;
- a paraphrase or restatement offered for checking;
- predictions and consequence checks;
- causal or boundary questions;
- corrections and model revisions;
- competing explanations;
- return to a distant dependency;
- assistant-generated context that has become long, dense, branched, or revision-heavy.

These signals may justify adaptation or a reconstruction cue. They do not justify statements such as “you forgot” unless the human actually reports forgetting.

## Frequent eligibility, sparse intervention

Possible outcomes of the resident sensitivity are:

1. **no-op** — ordinary response is already sufficient;
2. **lightweight shaping** — one restored causal link, distinction, checkpoint, or bridge sentence;
3. **model-coordination Skill** — deeper externalization, discrimination, evidence contact, probe, revision, or selective revalidation;
4. **reconstruction Skill** — explicit or implicit-in-the-response reactivation of prior reasoning.

A Skill activation does not require a visible card or workflow announcement.

A long conversation does not automatically require reconstruction.

## What v2 deliberately does not settle

This revision does not attempt to define:

- a complete taxonomy of reconstruction risk;
- a numeric activation threshold;
- a permanent human cognitive profile;
- a mandatory question cadence;
- a fixed reconstruction schema;
- a final carrier architecture;
- whether these candidate mechanisms should ultimately live in Rules, Skills, hooks, another host primitive, or some combination.

Those remain research questions.

The purpose of v2 is to restore treatment exposure so later field evidence can discriminate them.

## Files

- `cursor-user-rule.md` — resident kernel with cognitive sensitivity.
- `skills/human-ai-model-coordination/SKILL.md` — broader ordinary model-coordination treatment.
- `skills/human-ai-reconstruction/SKILL.md` — reconstruction based on observable reacquisition risk as well as explicit recovery.
- `evals/cases.json` — exposure, no-op, and over-intervention cases.

## Install in Cursor

### 1. Replace the v1 User Rule

In Cursor:

1. Open **Customize → Rules**.
2. Replace the previous carrier-v1 User Rule with the contents of `cursor-user-rule.md`.

Do not keep both v1 and v2 resident rules active at the same time; that would confound the pilot.

### 2. Replace the two v1 Skills

Copy:

```text
pilots/cursor-carrier-v2/skills/human-ai-model-coordination
pilots/cursor-carrier-v2/skills/human-ai-reconstruction
```

over the corresponding directories in:

```text
~/.cursor/skills/
```

The Skill names intentionally remain stable so v2 is a treatment revision rather than a new conceptual taxonomy.

## Field evaluation

The first gate is now **treatment exposure**, not final collaboration quality.

For a natural episode, distinguish:

```text
Was there a coordination/reconstruction opportunity?
        ↓
Did the carrier notice it?
        ↓
Did the relevant mechanism influence behavior?
        ↓
Was the treatment proportionate and faithful?
        ↓
Did it improve the collaboration?
```

Do not collapse these into one pass/fail judgment.

High-value observations include:

- the human expresses confusion but no coordination treatment appears;
- the human paraphrases a model and the AI merely says “yes” instead of calibrating the relationship;
- a small reconstruction cue appears naturally and reduces repeated explanation;
- a Skill activates but produces unnecessary questioning or ceremony;
- long context remains locally clear and correctly receives no reconstruction surface;
- a distant/revised causal dependency is needed and the AI restores it without claiming the human forgot;
- manual Skill invocation produces useful behavior while automatic routing still misses;
- the human must issue compensatory meta-instructions to make the carrier use the cognitive mechanisms.

## Interpretation boundary

v2 can fail in at least two opposite ways:

- **under-exposure** — useful candidate mechanisms still rarely enter the causal path;
- **over-intervention** — broader sensitivity turns ordinary collaboration into questions, summaries, Context cards, or visible methodology.

The desired region is:

> **high opportunity sensitivity + low unnecessary intervention cost**

A successful v2 field result would still not prove the cognitive models correct. It would establish that the carrier is finally capable of delivering enough of the intended treatment for effectiveness questions to become interpretable.
