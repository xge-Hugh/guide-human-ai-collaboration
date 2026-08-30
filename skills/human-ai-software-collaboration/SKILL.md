---
name: human-ai-software-collaboration
description: Guide complex software collaboration across framing, planning, implementation, review, and iteration without turning those concerns into fixed gates. Use when software changes have load-bearing contract, architecture, implementation, or validation dependencies; when implementation authorization matters; or when independent review/evidence must be staged. Skip simple mechanical edits and factual programming questions.
---

# Human-AI Software Collaboration

This Skill specializes the current cross-domain collaboration model for software work. Workflow concerns are dependencies, not a mandatory visible five-stage ritual.

## Runtime behavior

1. **Track the current software concern, not a ceremonial phase.** Useful concerns include framing the task, deliberating/planning, acting/producing, assuring/evaluating, and reflecting/learning. They can overlap and iterate.

2. **Separate discussion depth from implementation commitment.** Task framing or implementation discussion may inspect architecture, code, interfaces, data, or runtime evidence without authorizing a real system change. Do not treat lower-level inspection as permission to implement.

3. **Do not hard-code unresolved load-bearing semantics.** If request contracts, invariants, entity pairing, data-loss behavior, permissions, or other consequential dependencies remain unresolved, avoid implementation choices that silently decide them. Continue safe investigation or preparation that does not depend on those decisions.

4. **Use repository and external precedent selectively.** For unfamiliar, high-risk, or load-bearing design, inspect mature repository patterns, official documentation, or direct evidence when useful. Separate what can be reused, what needs adaptation, and what must remain task-specific.

5. **Preserve short feedback loops.** Prefer changes and evidence that expose wrong direction early. When an upstream purpose, contract, or causal assumption is wrong, return to it rather than accumulating downstream patches.

6. **Settle implementation before independent review.** Summarize actual changes, implementation deviations, available evidence, and validation debt. Implementer self-check is not independent review.

7. **Validate at the actual failure boundary.** Compilation, unit tests, integration tests, real requests, logs, replay, load evidence, or other methods have different evidentiary value. Choose according to the failure mode and risk rather than test quantity.

8. **Keep mechanical work mechanical.** Local renames, formatting, obvious boilerplate, and low-risk reversible edits should not trigger architecture ceremony or human cognitive exercises.

## Authorization boundary

A natural technical next step is a proposal until the human has delegated the relevant scope. High-impact or hard-to-reverse software actions require confirmation proportionate to their consequences.

Stop specialized workflow intervention when the task has become simple, local, reversible, and already grounded.
