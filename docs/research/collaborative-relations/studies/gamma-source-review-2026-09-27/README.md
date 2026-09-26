# Experiment γ — first source-review results

**Status:** source review completed for the three assigned cases; provisional research annotations, not experimental results. Reviewed 2026-09-27 against the [source-review gate](../gamma-source-review-gate-2026-09-27.md) and [staged protocol](../gamma-bidirectional-state-settlement-protocol-2026-09-16.md). The local branch was already at merged handoff `339a513`; fetching `origin/main` confirmed no additional commits at the start of this review.

| Assigned case | Decision | Evidence and reason |
| --- | --- | --- |
| [SR-1 / GAMMA-013](sr-1.md) | **Include for γ-I fixture construction** | Historical Git before/after code matches Cursor's cached edit snapshots after explicit text normalization. Shared plan, implementation interval, actual tool results and downstream judgment are recoverable. Business intent remains partly ambiguous; the later retracted concern is not oracle truth. |
| [SR-2 / GAMMA-011](sr-2.md) | **Defer** | Actual historical read outputs substantiate the human-reported patch, but no exact immediate full before/after artifact pair was recovered. Adjacent fields reappear after the agent removed them, so the human delta cannot safely be reduced to one config edit. |
| [SR-3 / GAMMA-007](sr-3.md) | **Defer as a primary γ-I fixture** | Historical artifacts substantiate the stale accessor/constant and cleanup. Earlier human code review and class explanations show this was not a simple uninformed recipient. Whether later package/cleanup requests altered a previously grounded acceptance judgment remains unresolved. |

**Replay gate: not met.** One case passes source-review eligibility; zero condition packets have been frozen or evaluated. The gate requires at least three eligible fixtures before γ-I. No extra cases were promoted simply to reach that threshold.

## What was recovered

- **SR-1:** clean starting HEAD `97965853`, resulting commit `11cd4056`, Cursor edit-cache before/after content, actual shell/metadata outcomes and the recorded lint invocation. Cached source and historical Git blobs agree after removing an optional UTF-8 BOM, normalizing CRLF, and removing trailing newline characters. Raw hashes remain separate; these are not claimed byte-identical.
- **SR-2:** the earlier config excerpt, preceding agent patch/search, post-human read/search results and historical Git versions on either side of the episode. These are stronger than an assistant's approval, but bracketing commits are not an exact human-action snapshot.
- **SR-3:** original implementation/review context, draft-PR head `0c18c93`, historical added-file output, pruned search metadata and cleanup commit `a061e8c`. An independent read-only search of the historical tracked Java files reproduces the stale-symbol pattern. The earlier reported commit `f075582` has the same tree as `0c18c93`; the historical branch output determines which head applies to the PR window.

No business repository was checked out or modified. No live CRM, application, database, Redis or deployment operation was run. Source code was inspected as historical evidence, not retested against today's environment.

## Findings that narrow the first-pass interpretation

**SR-1's customer distinction is only partly new.** The acknowledged pre-work plan already said to omit ZCRM02 `KUNNR`. It also already specified omitting empty mutually exclusive keys. Those cannot be scored as entirely new discoveries just because the final report calls them deltas. The exact behavior for a populated customer and `ZUONR` fallback still matters, as does whether that behavior was inferred or externally confirmed. The user relayed the consultant's answers; this review did not obtain independent consultant confirmation.

**The actual validation evidence has limits.** SR-1's lint record stores `{}`. It establishes an invocation/outcome record, not compilation, integration success or coverage of the disputed business boundary. The metadata result establishes a field name/type; a broad ticket keyword search does not establish an alternate ticket-number mapping. No build/test threshold should be invented as an S0 promise.

**SR-2 has an unresolved edit boundary.** Before the human report, the agent removed `PAYMENT_TERM_TEXT` refill and its search did not show the later entries. After the human report, actual read/search output shows both a refill and hidden schema present again. The human explicitly names the config repair but does not enumerate these adjacent changes. They might reflect restoration, undo or other editing; source review cannot choose an actor or cause without evidence.

**SR-3 is not a proven reporting failure.** The human had previously reviewed most code, requested class-level explanation and approved a commit. The later PR report was brief, but the transcript already contained richer implementation rationale. Stale code is observable and cleanup was real; its importance for maintainability does not automatically make it a missing current-acceptance fact under γ-I. Broad architectural interest and an explicit acceptance criterion are different kinds of evidence.

## Deliverables and verification

- [fact-ledger.json](fact-ledger.json): S0, execution events, source addresses, epistemic status, artifact visibility, semantic-explanation need, `D_now+` / `D_now0` / ambiguous, longitudinal `L`, J, R and all seven gate checks for each case.
- [sources.json](sources.json): 29 source records with transcript hashes, immutable Git commits/blobs, precise Cursor SQLite keys and hashes, plus normalization and historical-search results.
- [evidence-excerpts.md](evidence-excerpts.md): short source excerpts for review without copying full business files or database records into this repository.
- [verify_sources.py](verify_sources.py): repeatable read-only verification. Run `python3 verify_sources.py` on the source machine; use `--metadata-only` when private local sources are unavailable. Metadata-only verification does not re-establish source authenticity.

The ledger and review pages contain future-turn evidence and therefore **must not be used as recipient packets**. In SR-1, the frozen portal source can be part of the common audit path, but the future human question and agent retraction must remain withheld. A later commit may corroborate the artifact only because the pre-settlement cache independently matches it.

Implementation confidence and acceptance-evidence sufficiency remain separate. No recipient confidence, alignment time, cost or condition score is populated. Labels are from one source-review annotator and remain open to independent challenge.

## Next action after this handoff

SR-1 can advance to a frozen source-reviewed fixture, with ambiguous business authority and prompted reporting retained. SR-2 needs an exact historical edit snapshot/diff or must remain observational. SR-3 needs a defensible pre-work acceptance dependency, or a separately declared maintainability/γ-II question. If those cannot be recovered, review replacement candidates under the same gate rather than rewriting history to make them pass.

Once at least three fixtures pass, construct only the γ-I final-state, full-trace and selective-delta forms with the same audit return path. Freeze selection before recipient evaluation and hold consequence linkage and verification affordances comparable, or explicitly declare them as extra manipulations. The older flat six-way outline is retired.
