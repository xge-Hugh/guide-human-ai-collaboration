# Experiment γ — candidate-episode registry

**Status:** 17 observational candidates for review, not experiment results. Prepared 2026-09-27.

The [study definition](../README.md#γ--bidirectional-state-settlement) compares final summaries (1), full traces (2), selected consequential deltas (3), deltas with source/audit return edges (4), shared artifacts with minimal semantic deltas (5), and indexed state retrieved on demand (6). Both human→AI and AI→human settlement matter. Here those numbers describe possible analogues and replay opportunities, not assigned treatments. No complete full-trace comparison was established.

The [claim ledger](../../claim-ledger.md) and [evidence policy](../../../../governance/evidence-policy.md) govern interpretation. The relevant difference is between artifact state, private rationale/uncertainty, and execution noise. Completion alone does not demonstrate action-sufficient alignment.

Use [registry.json](registry.json) for structured review and [source-inventory.json](source-inventory.json) for coverage. Local source links require access to this machine; transcript bytes were not copied into the repository. Exact line ranges, file/window SHA-256 hashes and short evidence anchors support return to evidence. Timestamps retain their source timezone and do not measure active work.

The [flomo enrichment and replay outline](flomo-enrichment.md) adds five candidates discovered through six notes. [flomo-evidence.json](flomo-evidence.json) separates exact excerpts, timestamps, linkage strength and interpretation.

## Candidate index

| ID | Priority | Direction | Episode | Analogues |
| --- | --- | --- | --- | --- |
| GAMMA-001 | medium | AI→human | [Pull report preserves a return path to displaced local work](#gamma-001) | 3, 4, 6 |
| GAMMA-002 | high | human→AI→human | [Human GUI action and screenshots expose a missing extension](#gamma-002) | 3, 5 |
| GAMMA-003 | high | human→AI→human | [Startup log plus process inspection distinguishes progress from failure](#gamma-003) | 3, 4, 5 |
| GAMMA-004 | high | AI→human→AI | [Unexpected frontend ports reveal residual execution state](#gamma-004) | 3, 5 |
| GAMMA-005 | high | human→AI→human | [Proxy mode changes require inspection before settling network state](#gamma-005) | 3, 5 |
| GAMMA-006 | high | AI→human→AI | [Human corrects the causal explanation of a failed capture](#gamma-006) | 3, 4, 5 |
| GAMMA-007 | high | AI→human→AI | [Post-PR review request recovers package rationale and stale code](#gamma-007) | 1, 3, 4, 5 |
| GAMMA-008 | medium | AI→human | [Testing dependency triggers retrieval of an actionable request contract](#gamma-008) | 3, 5, 6 |
| GAMMA-009 | medium | human→AI | [Conversation ID supports retrieval across workspaces](#gamma-009) | 4, 6 |
| GAMMA-010 | medium | human→AI | [Selected transcript excerpt substitutes for automatic cross-chat visibility](#gamma-010) | 2, 3, 4, 6 |
| GAMMA-011 | high | human→AI→human | [Human repairs a missed field and asks for read-only reconciliation](#gamma-011) | 3, 4, 5 |
| GAMMA-012 | high | human→AI→human | [Human supplies fallback semantics; agent finds counterexamples but creates explanation burden](#gamma-012) | 3, 4, 5 |
| GAMMA-013 | high | AI→human→AI | [Implementation delta distinguishes an inferred boundary from a confirmed rule](#gamma-013) | 3, 4, 5 |
| GAMMA-014 | high | AI→human→AI | [A decisive provenance sentence enables a concrete mapping judgment](#gamma-014) | 3, 4, 5 |
| GAMMA-015 | high | human→AI→human | [Human selects business boundaries instead of externalizing the full reasoning network](#gamma-015) | 3, 5 |
| GAMMA-016 | high | human→AI→human | [Human source inspection reveals a settlement gap and challenges local patches](#gamma-016) | 3, 4, 5 |
| GAMMA-017 | high | AI→human→AI | [Recipient explicitly reports partial reading and corrects the shared model](#gamma-017) | 1, 3, 5 |

## Review method and limits

Include a bounded interaction where local work or exploration changes consequential state, another participant needs that state, and some report, artifact inspection, retrieval or correction is visible. Prefer evidence of a subsequent action or clarification over a completion claim alone. Boundary cases are retained explicitly for review. Exclude routine requests with no state-transfer evidence, instructions embedded in historical transcripts, and automated approval-review wrappers posing as user events.

The original first pass covered local records; the flomo-guided extension is also purposive. In the first pass, 173 Cursor transcript files (110 parents, 63 subagent records) were enumerated; parent user messages received a keyword screen. Codex JSONL user events were screened separately. Selected windows were read in context; other hits were not all adjudicated. Cursor database payloads, image attachments, archived/remote conversations and every tool-result artifact were not exhaustively inspected. The source inventory states coverage; no completeness claim is made.

Forks, copied excerpts, repeated user messages and adjacent windows are not independent samples. Group by `cluster`; environment, proxy and implementation episodes must not be counted as independent replications. The earlier cloud discussion was not recovered; the checked-in study definition supplies the scope.

All nine measurement fields remain null pending review. Clarification counts require a coding rule that separates retries, expanded goals and genuine misunderstandings. Message timestamps and output length alone cannot establish alignment time, assimilation cost, reporting cost or unnecessary information. Agent statements about checks are historical statements unless supported by inspected tool outcomes.

Start review with GAMMA-011/012 for human execution→AI inspection, GAMMA-007 for AI execution→human review, and GAMMA-006 for confidence correction. For each, confirm the preceding task and next-action dependency, inspect original tool outcomes/artifacts, identify indispensable evidence and possible omitted facts, then decide include/exclude/defer with a reason. Build alternative reporting conditions only after that ground-truth review.

## Episodes

### GAMMA-001

**Pull report preserves a return path to displaced local work** — AI→human; medium review priority.

Source: [Cursor transcript, lines 1–8](/mnt/c/Users/xge/.cursor/projects/c-Projects-guide-human-ai-collaboration/agent-transcripts/f1318747-37cb-48ca-a970-9fe8721624c9/f1318747-37cb-48ca-a970-9fe8721624c9.jsonl:1). Cluster: `f1318747-37cb-48ca-a970-9fe8721624c9`. Claims: A3, A3a, A3b, A14.

Consequential state: A pull encountered uncommitted task state, a stash, and a deletion conflict; the final tree alone would not explain the displaced work.

Observed sequence: Agent reports synchronization and identifies stash@{0}, including a command to recover its contents.

Limits: Tool calls and report are present; raw command outcomes and later human retrieval are not established in this window.

Review question: Does the stash address plus consequential delta enable recovery better than a clean-tree summary?

### GAMMA-002

**Human GUI action and screenshots expose a missing extension** — human→AI→human; high review priority.

Source: [Cursor transcript, lines 138–145](/mnt/c/Users/xge/.cursor/projects/c-Projects-FTS-FinePartner/agent-transcripts/5414aa6a-5f8d-4ab3-8a5d-ce4c2c168206/5414aa6a-5f8d-4ab3-8a5d-ce4c2c168206.jsonl:138). Cluster: `environment-5414aa6a`. Claims: A3, A10, A12.

Consequential state: Human cleaned the language-server workspace, then encountered a different startup obstacle outside agent observation.

Observed sequence: Human reports execution and supplies screenshots; agent reports inspecting installed extensions and distinguishes an extension pack from a missing component.

Limits: Screenshots were not visually reviewed in this screening; underlying tool results are not reproduced. Agent technical explanations remain claims.

Review question: Which facts need a human semantic update and which are recoverable by inspecting the shared machine?

### GAMMA-003

**Startup log plus process inspection distinguishes progress from failure** — human→AI→human; high review priority.

Source: [Cursor transcript, lines 146–154](/mnt/c/Users/xge/.cursor/projects/c-Projects-FTS-FinePartner/agent-transcripts/5414aa6a-5f8d-4ab3-8a5d-ce4c2c168206/5414aa6a-5f8d-4ab3-8a5d-ce4c2c168206.jsonl:146). Cluster: `environment-5414aa6a`. Claims: A3, A9, A10, A12.

Consequential state: The human can launch the application, but an occupied port and later tooling error obscure what succeeded.

Observed sequence: Human supplies a port-conflict log; agent reports inspecting a running process; human requests cleanup and later reports successful backend startup with a separate tool error.

Limits: HTTP/process success is agent-reported here; application correctness and user understanding were not independently tested.

Review question: Can a short semantic delta plus log/process evidence restore the next action without a full setup trace?

### GAMMA-004

**Unexpected frontend ports reveal residual execution state** — AI→human→AI; high review priority.

Source: [Cursor transcript, lines 155–161](/mnt/c/Users/xge/.cursor/projects/c-Projects-FTS-FinePartner/agent-transcripts/5414aa6a-5f8d-4ab3-8a5d-ce4c2c168206/5414aa6a-5f8d-4ab3-8a5d-ce4c2c168206.jsonl:155). Cluster: `environment-5414aa6a`. Claims: A3, A3b, A9, A12.

Consequential state: Multiple surviving frontend processes explain why repeated launches use incremented ports.

Observed sequence: Human asks about 3002/3003; agent reports three old instances; human requests cleanup; agent reports freed ports; user later gives broad positive feedback.

Limits: The origin of each process is not independently established; positive feedback does not prove port-specific verification.

Review question: Was process state omitted from earlier reporting, or created by later human actions? Review earlier execution before attributing an omission.

### GAMMA-005

**Proxy mode changes require inspection before settling network state** — human→AI→human; high review priority.

Source: [Cursor transcript, lines 100–121](/mnt/c/Users/xge/.cursor/projects/c-Projects-FTS-FinePartner/agent-transcripts/6fd23206-645c-4d07-959f-350773743323/6fd23206-645c-4d07-959f-350773743323.jsonl:100). Cluster: `proxy-6fd23206`. Claims: A3, A10, A12.

Consequential state: The human changes proxy mode and later disables it; the agent needs actual listener and proxy state, not just the mode label.

Observed sequence: Agent reports that rule mode still resets the proxy, then revises routing after the old upstream refuses connections; reports scope and restoration target.

Limits: No independent network reproduction; technical assertions and restoration are historical reports.

Review question: Which extra state was learned through inspection after the human reported a change?

### GAMMA-006

**Human corrects the causal explanation of a failed capture** — AI→human→AI; high review priority.

Source: [Cursor transcript, lines 123–137](/mnt/c/Users/xge/.cursor/projects/c-Projects-FTS-FinePartner/agent-transcripts/6fd23206-645c-4d07-959f-350773743323/6fd23206-645c-4d07-959f-350773743323.jsonl:123). Cluster: `proxy-6fd23206`. Claims: A3, A3a, A3b.

Consequential state: Capture yields a failed cloud save but usable local backup; the human holds a network-access constraint missing from the agent explanation.

Observed sequence: Agent distinguishes failed cloud persistence from local XML evidence, attributes 403 to intercepted TLS, then the human says the proxy is required for resource access; agent revises its account.

Limits: The revised cause is not independently verified. Screenshot and captured payloads were not inspected; do not convert agent explanation into a confirmed root cause.

Review question: Could access to the underlying evidence expose an executor-selected explanation that omits a decisive constraint?

### GAMMA-007

**Post-PR review request recovers package rationale and stale code** — AI→human→AI; high review priority.

Source: [Cursor transcript, lines 351–372](/mnt/c/Users/xge/.cursor/projects/c-Projects-FTS-FinePartner/agent-transcripts/8dade695-86fa-4d58-bafa-531bf086919b/8dade695-86fa-4d58-bafa-531bf086919b.jsonl:351). Cluster: `implementation-8dade695`. Claims: A3, A3a, A3b, A9.

Consequential state: A completion/PR report leaves the human still needing file placement and a residual-code check for review.

Observed sequence: Human requests package locations and points to an old accessor; agent invokes diff/search, explains placement and reports two stale elements; human authorizes removal; agent reports cleanup.

Limits: Repeated requests at 359/361/363 are one cluster, not three independent episodes. Need preceding implementation context before declaring original reporting inadequate.

Review question: Which consequential review details were available in the artifact but not usable from the completion report?

### GAMMA-008

**Testing dependency triggers retrieval of an actionable request contract** — AI→human; medium review priority.

Source: [Cursor transcript, lines 374–381](/mnt/c/Users/xge/.cursor/projects/c-Projects-FTS-FinePartner/agent-transcripts/8dade695-86fa-4d58-bafa-531bf086919b/8dade695-86fa-4d58-bafa-531bf086919b.jsonl:374). Cluster: `implementation-8dade695`. Claims: A9, A10, A14.

Consequential state: Human needs endpoint location, headers and body to test a completed feature.

Observed sequence: First answer supplies URL/path; user expands request to headers/body; agent consults code and gives an example contract.

Limits: This may be ordinary incremental information demand rather than failed settlement. No test execution in this window.

Review question: Would a discoverable contract pointer have reduced clarification without narrating the entire implementation?

### GAMMA-009

**Conversation ID supports retrieval across workspaces** — human→AI; medium review priority.

Source: [Cursor transcript, lines 1–10](/mnt/c/Users/xge/.cursor/projects/c-Projects-FTS-FinePartner/agent-transcripts/e8e64ae8-c14d-40db-ad7a-4dd6ada97228/e8e64ae8-c14d-40db-ad7a-4dd6ada97228.jsonl:1). Cluster: `e8e64ae8-c14d-40db-ad7a-4dd6ada97228`. Claims: A3, A14.

Consequential state: Human refers to earlier logging exploration by conversation ID and supplies current intent.

Observed sequence: Agent searches, issues a Read for the prior transcript in another workspace, inspects current project files, then relates earlier conclusions to the new task.

Limits: Earlier conversation substance was not independently compared in this screening; this is continuity after exploration, a boundary case rather than a clean execution handoff.

Review question: Is the address plus intent enough, and does reconstruction preserve earlier uncertainty rather than invent consensus?

### GAMMA-010

**Selected transcript excerpt substitutes for automatic cross-chat visibility** — human→AI; medium review priority.

Source: [Cursor transcript, lines 126–135](/mnt/c/Users/xge/.cursor/projects/c-Projects-guide-human-ai-collaboration/agent-transcripts/e1f51c24-d6b6-4160-b668-35647a20d7ae/e1f51c24-d6b6-4160-b668-35647a20d7ae.jsonl:126). Cluster: `e1f51c24-d6b6-4160-b668-35647a20d7ae`. Claims: A3, A3b, A9, A14.

Consequential state: Human wants to discuss another agent’s behavior without repeatedly copying context.

Observed sequence: Agent describes retrieval limitations; human chooses transcript export and pastes a selected interaction including a completion report and review scaffolding.

Limits: Nested conversation is second-hand selected evidence, not a new independent execution. A pasted excerpt is not a full chronological trace; no condition-2 treatment is established.

Review question: What selection cost and omission risks arise when the human is the reporter of a separate collaboration?

### GAMMA-011

**Human repairs a missed field and asks for read-only reconciliation** — human→AI→human; high review priority.

Source: [Codex transcript, lines 4450–4484](/home/xge/.codex/sessions/2026/05/21/rollout-2026-05-21T14-19-53-019e4930-c347-7ec3-ae5c-7e0ae617d89a.jsonl:4450). Cluster: `fields-019e4930`. Claims: A3, A3b, A10, A12.

Consequential state: Human independently patches field configuration and asks the agent to reconcile implementation and display behavior without further edits.

Observed sequence: Agent reads code and identifies configuration, binding and option-mapping locations; human asks about keeping a residual field and moving to the next task.

Limits: Source-read tool results exist in the session but runtime UI behavior was not validated by this screening. Assistant approval is not independent correctness evidence.

Review question: Does artifact access plus the human’s brief intent update restore enough state to review the change?

### GAMMA-012

**Human supplies fallback semantics; agent finds counterexamples but creates explanation burden** — human→AI→human; high review priority.

Source: [Codex transcript, lines 247–268](/home/xge/.codex/sessions/2026/05/25/rollout-2026-05-25T14-59-05-019e5dee-1759-7823-89b9-88be5b4b8377.jsonl:247). Cluster: `fallback-019e5dee`. Claims: A3, A3a, A9, A12.

Consequential state: Human changes region fallback and explains that null means all tenants, a semantic constraint not recoverable from syntax alone.

Observed sequence: Agent inspects the change, gives repeated-region and empty-task counterexamples, includes an intermediate flawed suggestion then corrects it; user says the explanation is complex and requests a decision.

Limits: No final implementation or test outcome in the window. Self-correction and user burden make this mixed evidence, not a clean success.

Review question: Can selected counterexamples and a source return edge preserve calibration with less assimilation cost?

### GAMMA-013

**Implementation delta distinguishes an inferred boundary from a confirmed rule** — AI→human→AI; high review priority.

Source: [Cursor transcript, lines 20–33](/mnt/c/Users/xge/.cursor/projects/c-Projects-SUNWARD-CRM/agent-transcripts/d3f95340-666e-4198-ae2d-048202438a55/d3f95340-666e-4198-ae2d-048202438a55.jsonl:20). Cluster: `sap-mapping-d3f95340`. Claims: A3, A3a, A3b.

flomo: slug `MjU2NTU4OTQ0`, created_at `2026-09-14 14:11:39`, updated_at `2026-09-14 14:11:49`; relationship: `distinctive_quote_match_to_assistant_line_28`. Timestamp timezone was not supplied by MCP.

Consequential state: Implementation resolves an underspecified empty-customer rule; the human must know that this boundary was inferred rather than newly confirmed by the consultant.

Observed sequence: Human explicitly requests valuable implementation deltas at line 21. Agent reports forced omission even when a customer exists. Human recognizes the distinction, challenges another reported risk, and agent retracts a portal-reading error while marking the customer boundary as its own inference. Human then proposes committing.

Limits: The request primed delta reporting; this is not spontaneous first-opportunity behavior. The memo was created at 14:11:39, while the explicit human response is stamped 14:16; flomo timezone is unspecified and ordering cannot establish when understanding occurred. Business acceptance and integration tests remain unverified.

Review question: Does selected delta preserve the distinction between implemented behavior, consultant authority and an executor inference, without exporting false risks?

### GAMMA-014

**A decisive provenance sentence enables a concrete mapping judgment** — AI→human→AI; high review priority.

Source: [Cursor transcript, lines 49–60](/mnt/c/Users/xge/.cursor/projects/c-Projects-SUNWARD-CRM/agent-transcripts/d3f95340-666e-4198-ae2d-048202438a55/d3f95340-666e-4198-ae2d-048202438a55.jsonl:49). Cluster: `sap-mapping-d3f95340`. Claims: A3, A3a, A3b.

flomo: slug `MjU3MDU5NjAy`, created_at `2026-09-17 17:15:15`, updated_at `2026-09-17 17:15:27`; relationship: `distinctive_quote_match_to_assistant_56_and_user_57`. Timestamp timezone was not supplied by MCP.

Consequential state: Agent has inspected mapping/data and knows why header-derived fields belong to a specific generated row; the human still questions whether row number alone identifies it.

Observed sequence: Human challenges the basis at lines 50 and 53. Agent explains field provenance at 56. Human quotes that sentence, states that it enables confidence, and proposes dropping a redundant row-code guard. Agent agrees while preserving scenario conditions; human authorizes implementation at 59.

Limits: A planning/research-to-decision handoff rather than completed implementation settlement. Quoted evidence and changed decision are visible, but correctness of database assertions needs source verification. The memo repeats the same event and is not independent confirmation.

Review question: Which one source-grounded relation changes the recipient’s decision, and which earlier details did not resolve the uncertainty?

### GAMMA-015

**Human selects business boundaries instead of externalizing the full reasoning network** — human→AI→human; high review priority.

Source: [Cursor transcript, lines 219–224](/mnt/c/Users/xge/.cursor/projects/c-Projects-SUNWARD-CRM/agent-transcripts/113c9bcc-e978-45e1-81f1-e20161ad019d/113c9bcc-e978-45e1-81f1-e20161ad019d.jsonl:219). Cluster: `business-rules-113c9bcc`. Claims: A3, A3a, A9.

flomo: slug `MjU0NzE3NDk5`, created_at `2026-09-02 13:18:53`, updated_at `2026-09-02 13:18:57`; relationship: `substantial_text_match_to_user_line_219`. Timestamp timezone was not supplied by MCP.

Consequential state: Human holds a dense business model and tentative terminal-state/CAS judgments; communicating the entire reasoning network is costly.

Observed sequence: Human describes expression effort and supplies three operational rules. Agent translates these to state boundaries and highlights an unresolved partial-receipt case. Human then revises the preferred behavior and again says its reasoning is hard to express; agent proposes a narrower alternative.

Limits: Primarily reasoning/exploration settlement, not a demonstrated human code-execution handoff. The next message changes the proposal: do not score the initial alignment as final or correct. Human effort is self-reported, not timed.

Review question: Can selected operational boundaries reduce reporting effort while keeping unsettled exceptions visible and revisable?

### GAMMA-016

**Human source inspection reveals a settlement gap and challenges local patches** — human→AI→human; high review priority.

Source: [Cursor transcript, lines 193–201](/mnt/c/Users/xge/.cursor/projects/c-Projects-SUNWARD-CRM/agent-transcripts/41da5118-de8c-4a54-80e3-ff1db2f3d661/41da5118-de8c-4a54-80e3-ff1db2f3d661.jsonl:193). Cluster: `exception-refactor-september`. Claims: A3, A3b, A10, A12.

flomo: slug `MjU2OTA5Nzk2`, created_at `2026-09-16 18:15:03`, updated_at `2026-09-23 08:50:56`; relationship: `probable_event_match_by_exception_refactor_and_independent_code_inspection`. Timestamp timezone was not supplied by MCP.

Consequential state: After inspecting code, the human identifies mismatch between its understanding, agent-local state and the implemented exception architecture.

Observed sequence: Human explicitly says agent state was not adequately transmitted and points to internal exception types hidden in batch contracts. Agent inspects current structure and reports architectural issues. Human rejects the canvas representation and asks to evaluate concrete changes and their benefits.

Limits: Memo names the exception-refactor episode but lacks a unique quoted turn; linkage is strong topic/detail correspondence, not exact identity proof. Memo updated 2026-09-23 after its 2026-09-16 creation. Repeated turns 199/201 count once. Agent acceptance does not establish architectural correctness.

Review question: Did shared code access expose consequential omissions in executor-selected reports, and what prior knowledge made that inspection usable?

### GAMMA-017

**Recipient explicitly reports partial reading and corrects the shared model** — AI→human→AI; high review priority.

Source: [Cursor transcript, lines 14–18](/mnt/c/Users/xge/.cursor/projects/c-Projects-SUNWARD-CRM/agent-transcripts/78bf51f7-d5ad-48b0-a0b4-a8f1afa679a2/78bf51f7-d5ad-48b0-a0b4-a8f1afa679a2.jsonl:14). Cluster: `exception-refactor-september`. Claims: A3, A3a, A9, A12.

flomo: slug `MjU3MTYxODE1`, created_at `2026-09-18 10:42:19`, updated_at `2026-09-18 10:42:21`; relationship: `thematic_match_partial_reading_do_not_infer_same_event`. Timestamp timezone was not supplied by MCP.

Consequential state: A long review report exceeds what the human has read; the human’s model also omitted existing built-in exception types.

Observed sequence: Human explicitly warns that its answer does not imply full reading or comprehension, identifies newly learned distinctions and asks whether the design needs rethinking. Agent acknowledges excessive review scope and reframes the response around that decision.

Limits: flomo note is a matching methodological reminder, not securely tied to this exact conversation. No measured comprehension or later successful action. Agent reframing remains long; intent to reduce burden is not proof of reduced burden. Related to GAMMA-016, not an independent replication.

Review question: What observable next-action evidence is needed before treating a report as assimilated, and can decision-focused reporting improve it?
