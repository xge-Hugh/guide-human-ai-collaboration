# γ-I v2 execution — streaming runtime preflight

Status: **invalid operational attempt; excluded from analysis**. The earlier
automatic approval block was resolved by the user's explicit authorization;
see the [attempt status](attempt-status.json) for the later run failure.

This episode uses the same frozen v1 settlement/scoring inputs and v2 audit layer
as the two earlier preflight episodes. It uses the user-updated `gamma-i-v2` profile:
recipient `deepseek/deepseek-flash`, scorer `qwen3.8-flash`.

## Pre-exposure runtime corrections

Six non-streaming independent-review attempts failed at the transport layer. A
streaming diagnostic completed the same C13 review after 246 seconds with HTTP 200,
finish reason `stop`, and the terminal stream marker. Therefore the gamma runner
now uses streaming on the wire, buffers final content, and persists it only after
the complete response. Partial output never triggers audit-menu exposure. Reasoning
content is not retained. No external tools are provided or executed.

The diagnostic review flagged a conditional D-versus-T consequence-linkage issue.
Its interpretation limits explicitly noted that the frozen scoring plan could
permit treating it as a residual confound. The earlier review prompt had omitted
that plan despite asking the reviewer to apply it. This episode supplies the complete,
unchanged frozen scoring plan and v2 run specification to the independent reviewer.
The provisional review is preserved in the prior episode; it is not silently replaced.

All corrections occurred before any recipient exposure. No settlement surface,
S0, audit payload, oracle, scoring source, or claim interpretation was edited.
Five offline tests passed, including incomplete-stream rejection, rejection of tool
responses, exact audit return, and initial-response persistence before menu exposure.

Both provider connectivity checks passed. C13 and S01 returned independent reviews;
their full responses are preserved. C13 reported no blocking defect. S01 flagged
the known D-versus-T guidance confound as blocking a clean fact-selection comparison.
The pre-exposure [adjudication](preflight/interpretation-adjudication.md) preserves
that flag and applies the frozen scoring plan's narrower mechanics-feasibility
boundary. SH2's exact review request was saved, but its first execution was
interrupted before a response was persisted.

The next SH2 call was rejected twice by automatic approval review. Its stated
reason: the configured external grader would receive frozen packets, audit payloads,
oracle, and scoring material, and general authorization to proceed with the
experiment/provider was not specific enough for that egress. No indirect execution
or alternate destination was used after the rejection. The pending request SHA-256
is `472bf9cdc2d6b21179bae2d14fc1be0e392cb3b425b64aa24b62f1e740131317`;
it matches the previously saved request exactly. Earlier C13/S01 reviews and
connectivity checks were approved and completed. The two rejected attempts did
not send the SH2 request.

At this pause, all nine frozen Git blobs match the v2 manifest, nine initial
prompts and 18 audit payloads are present, five isolation/streaming tests pass,
execution-source snapshots match the current runner, and a private-value scan
found no configured endpoint or credential in run artifacts. Two independent
review responses exist; SH2 has none. There are no recipient records or scores.

The runtime gate remained closed until explicit authorization to
send the frozen packet and reviewer materials to the provider endpoint selected
by the user's `gamma-i-v2` profile, or another permitted route is configured and
verified. Then finish SH2 review, assess its findings, and run the 27 recipients
and separate scorer contexts without changing frozen study inputs.

## Attempt after the approved gate

The gate passed, and two C13 recipient contexts were exposed. In `C13-F-1`, the
recipient selected `C13-R1` and `C13-R5` and repeated each ID while explaining its
choice. The runner wrongly counted four mentions as four selections, returned the
frozen invalid-ID message, and contaminated the subsequent response. The first
record is preserved but excluded. `C13-T-1` saved its initial and selection
responses; its final request was interrupted before a final response was saved.
It too is excluded. No scores were produced and no treatment result is claimed.

This is a runner defect, not a change to the v2 packets, oracle, scoring rules,
or claim interpretation. The exact repeated-ID response is the regression case
for the fixed parser. A separate fresh attempt starts with a new run directory;
no record from this attempt is pooled into its 27-run matrix.
