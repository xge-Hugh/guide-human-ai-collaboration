# Experiment γ — flomo enrichment and first replay outline

**Status:** observational enrichment and proposed study design, 2026-09-27. No controlled replay has been run and no treatment effect is estimated.

## What flomo contributed

The original registry captured visible handoffs. flomo supplied searchable clues about what the human found consequential, difficult to express, insufficiently communicated, or newly understandable. Searching those clues in local transcripts added GAMMA-013 through GAMMA-017, bringing the registry to 17 candidates. These are five bounded windows, not five independent replications.

The [structured evidence records](flomo-evidence.json) preserve slug, created_at, updated_at, short original excerpt, full-note text hash, interpretation and linkage strength. Full-note text was read through the read-only MCP; it is not copied into this repository. The source service did not supply a timezone. Cursor timestamps explicitly use UTC+8; cross-source timing is therefore provisional.

| flomo source (slug; created_at) | Original excerpt | Research interpretation and link |
| --- | --- | --- |
| `MjU2NTU4OTQ0`; `2026-09-14 14:11:39` | “AI的认知模型也在变化” | GAMMA-013: a distinctive quote matches the implementation report. The transcript distinguishes an inferred boundary from consultant confirmation and includes a separate risk retraction. |
| `MjU3MDU5NjAy`; `2026-09-17 17:15:15` | “才让人类明白问题所在” | GAMMA-014: the human quotes the decisive sentence and proposes a concrete change. This is more informative than a generic acknowledgment, but does not independently validate the mapping. |
| `MjU0NzE3NDk5`; `2026-09-02 13:18:53` | “但是这让我轻松不少” | GAMMA-015: substantially the same text appears in the human chat turn. It reports expression effort and a selective alternative; it is one observation represented twice. |
| `MjU2OTA5Nzk2`; `2026-09-16 18:15:03` | “人自己独立看代码更换表征却能发现很多之前没发现的问题” | GAMMA-016: probable event linkage to exception-refactor inspection. Updated `2026-09-23 08:50:56`, so current text cannot be treated as an unchanged same-day record. |
| `MjU3MTYxODE1`; `2026-09-18 10:42:19` | “ai不要默认人看了自己的全部输出” | GAMMA-017: thematic link to an explicit partial-reading disclosure; not proof that the note describes this exact turn. |
| `MjU2MzQ1MTc3`; `2026-09-13 00:07:46` | “但我知道你读了这篇论文” | GAMMA-009: thematic rationale for addressable knowledge. The note does not corroborate the logging episode or establish successful later retrieval. |

The original excerpts above are the user's recorded text. The interpretation column is this screening's analysis. Neither is a measured treatment result.

## What the extension changes

1. **Prioritize GAMMA-013 for post-execution AI→human settlement.** It contains an explicit request for consequential deltas, the report, human reaction, a challenged risk and a retraction. The explicit request is a prompting confound: this case cannot show that the behavior arises spontaneously.
2. **Retain GAMMA-011 for human execution→AI settlement.** The human actually edits an artifact and requests inspection. GAMMA-015 complements it with self-reported externalization cost, but is reasoning settlement rather than a clean execution counterpart.
3. **Use GAMMA-014 as a diagnostic case for evidence selection.** It shows a specific evidence relation followed by a changed judgment. Since it occurs before implementation, analyze it separately from completed-work handoffs.
4. **Use GAMMA-016/017 as related failure/recovery cases.** Code visibility did not automatically produce shared understanding, and a long report was not fully read. They belong to one exception-refactor family and must not be treated as independent successes.

The flomo summary already present in Cursor transcript `efdacc8f-4ca3-4a96-8db0-3144357c90db` was excluded as corroboration: it derives from the same notes. Repeated turns, copied quotes and flomo/chat copies also remain dependent evidence.

## Source review before packet construction

For GAMMA-013 and GAMMA-011, retrieve the historical artifact version and actual tool outcomes, not just today's code or the assistant's final report. Record:

- the last shared pre-execution state and who knew each decisive fact;
- the bounded local execution and its artifact, private-rationale and uncertainty deltas;
- the recipient's concrete next action and the minimum facts needed for it;
- which facts were observed, inferred, consultant-confirmed, disputed or subsequently withdrawn;
- a source address for every consequential fact, plus unresolved evidence gaps.

Source review must preserve the executor's potentially mistaken interpretation. For example, GAMMA-013's stronger empty-customer behavior was an implementation choice, not a newly confirmed consultant rule. Its ticket-navigation risk was later retracted. A packet that silently turns either into established truth would remove precisely the selection/calibration problem γ should test.

Flomo can identify a candidate fact or perceived difficulty. It cannot reconstruct every unspoken thought, prove what the recipient knew beforehand, or replace the historical artifact. If a required historical source cannot be recovered, keep the case observational or label a reconstruction explicitly; do not manufacture ground truth.

## Proposed bounded replay

Start with two reviewed cases: GAMMA-013 (AI executor, human recipient) and GAMMA-011 (human executor, AI recipient). This is a feasibility pilot, not a powered claim-discrimination study. Keep the two directions separate in reporting.

After source review, construct a common pre-task brief, a reference fact ledger and a fixed next-action probe for each case. The recipient must not see the ledger or future corrective turns before answering. Use all six conditions from the study map; the descriptions below define packet boundaries, not completed packets.

| Condition | Recipient receives | Access boundary |
| --- | --- | --- |
| 1. Final-state summary | What was delivered and its reported status | No additional source access during the initial probe |
| 2. Full chronological trace | The bounded execution record through the settlement point | Exclude future recipient reactions and answer-revealing corrections |
| 3. Selected consequential delta | Executor-selected changes in behavior, rationale and uncertainty | No audit return edge during the initial probe |
| 4. Delta plus audit edge | The same selected delta as condition 3, plus source addresses | Source retrieval permitted and recorded |
| 5. Shared artifact plus minimal delta | Historical artifact access plus what the artifact cannot convey | Record inspection and clarification requests |
| 6. Indexed state | A compact index of available state and where to retrieve it | Retrieval permitted when the next-action dependency is recognized |

The common task, pre-state and historical source pool stay fixed. These conditions intentionally differ in representation and access; word count should be recorded, not forced equal at the expense of treatment meaning. Condition 3 and 4 must use the same selected text to isolate the audit-edge addition. Don't quietly optimize the selected delta using the answer key. Freeze and document executor selection before evaluating recipients; the historical report is a useful first selector baseline.

Possible next-action probes, subject to source verification:

- **GAMMA-013:** explain behavior when a ZCRM02 row contains a customer; separate implemented behavior from confirmed business intent; identify which reported concern requires evidence or clarification before accepting it.
- **GAMMA-011:** identify what the human changed, locate the option-label transformation, and explain whether the inspected state warrants moving to the next review task without unauthorized edits.

Use observable action or a small discriminating explanation, not “do you understand?” alone. First score next-action adequacy; then request a cited evidence location and reconstruction of any confidence change. Future-turn facts stay withheld until the corresponding follow-up stage.

## Measurements and interpretation

Record time to the first answer meeting the reviewed action-sufficiency rubric; decisive facts missed or falsely asserted; material consumed; source lookups; clarification requests; confidence before/after audit; and success locating evidence later. Record executor packet-production effort separately from recipient effort. For humans, add a brief self-report of assimilation burden; for AI, record tool latency, context volume and calls without equating them to human cognitive effort. Words viewed are an exposure proxy, not proof of information consumed or unnecessary information.

Mark action sufficiency as met, recovered after correction, not met, or unobservable, with a reason and evidence. A useful rubric must allow justified uncertainty and requests for missing evidence. Unwarranted confidence in an inferred business rule is not success merely because the final code matches it.

The original human already knows these episodes. Replaying all six conditions to that person on the same case would confound reporting quality with memory and practice. For a mechanics pilot, acknowledge that limitation; for stronger inference, use matched unfamiliar cases or fresh recipients and counterbalance condition allocation. AI-recipient runs require fresh contexts per condition. Do not use an AI proxy as evidence of human assimilation. Keep case clusters together when reporting sample counts, and separate prompted from unprompted reporting.

No alignment times, costs, effect sizes or comparative rankings have been filled in. All registry measurement fields remain null. The next concrete artifact is a source-reviewed case packet and its reference fact ledger; replay execution follows that preparation.
