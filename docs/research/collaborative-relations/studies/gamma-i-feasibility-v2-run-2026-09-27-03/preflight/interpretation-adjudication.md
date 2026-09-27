# Pre-exposure review adjudication: consequence-linkage confound

This adjudication was recorded before any recipient exposure. It does not revise
the packets, oracle, recipient scoring rules, or claim interpretation.

The independent C13 reviewer classified D's additional consequence linkage and
verification guidance as a reportable confound, with no exposure-blocking defect.
The independent S01 reviewer identified the same class of issue but classified it
as blocking a **clean fact-selection/settlement-form interpretation**. It reported
no audit oracle leakage, answer-bearing index labels, or material synthetic-artifact
inconsistency. Its full output remains unchanged in `independent-review-S01.response.json`.

## Controlling frozen rule

PR #41 `scoring.md`, Treatment-leakage check, says:

> After runs, inspect whether selective-delta packets systematically contain extra **consequence linkage** or **verification guidance** absent from the trace condition.
>
> If they do, do not interpret a selective-delta advantage as evidence for fact selection alone. Either:
> - revise packets before confirmatory work, or
> - explicitly factorialize consequence linkage/guidance.

The same scoring plan identifies this as mechanics feasibility, not confirmatory
evidence. The v2 run specification says an issue detected before exposure **may**
create v3; it does not replace the explicit frozen interpretation rule with an
automatic veto on collecting mechanics evidence whenever D has extra guidance.

## Decision

The S01 review's factual observation is retained. Its proposed veto on a clean
fact-selection comparison does not block collection of the authorized mechanics
run with the existing interpretation limit. No clean fact-selection inference will
be made, irrespective of the eventual direction or size of observed differences.
This is the same limitation applied to C13 and required by the frozen scoring plan.

The runner's automatic stop on any reviewer `blocking_defect` boolean is a local
preflight implementation choice, not a frozen scoring rule. Its stop has been
honored: no recipient was exposed. Releasing the gate requires explicit orchestrator
adjudication of the actual finding against the frozen requirements, preserving the
original reviewer flag and this rationale. A blanket favorable re-review is not used.

This decision covers only the identified D-versus-T consequence-linkage/guidance
confound. It does not waive input integrity, exact audit return, index timing,
recipient/scorer isolation, future-holdout leakage, material artifact inconsistency,
or other execution defects. SH2 still requires review before any exposure.

The orchestrator is also the runtime implementer and is not an independent second
reviewer. That dependence and the review disagreement must be reported. Neither
review is a recipient performance result or a change to a consequentiality label.
