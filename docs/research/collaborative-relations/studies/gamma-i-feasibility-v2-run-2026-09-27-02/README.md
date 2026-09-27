# γ-I v2 runtime preflight — fixture-specific follow-up

**Blocked before recipient exposure: 0/27 runs started.** No scores, treatment
comparisons, or claim updates were produced.

The user updated the private provider configuration and authorized proceeding.
The `gamma-i-v2` profile validated with recipient `deepseek/deepseek-flash` and
scorer `qwen3.8-flash`. API execution was approved. Both configured models returned
READY to the short non-experimental connectivity check, in both preflight episodes.

## Completed checks

- All nine frozen input blobs match the PR #42 manifest; original treatment and
  scoring inputs remain at the PR #41 packet version.
- Nine initial packets and 18 exact audit payloads extracted and hashed.
- Three offline boundary tests passed, including 27 fake-provider histories,
  initial persistence before menu exposure, and exact selected payload ordering.
- Artifact scan found no private endpoint or credential values.

## Runtime failure

The earlier combined independent-review request exhausted three transport attempts.
This follow-up split the independent review by fixture using the same review
criteria and frozen content. C13 again exhausted three transport attempts. No
review response was returned; S01 and SH2 review requests were therefore not sent.

All six failures are recorded as `provider transport failure`. The sanitized error
does not identify whether the underlying cause was timeout, connection termination,
or another transport problem. A successful short request is insufficient evidence
that this route supports the substantive review/scoring workload.

The runtime gate did not pass. No initial settlement was sent to a recipient.
The review-only scorer context was exposed to the review materials as intended;
that is not one of the 27 recipient contexts.

See [status.json](status.json) for the combined error inventory and successful smoke
responses, [offline-preflight.json](offline-preflight.json) for input hashes, and
[execution-code/manifest.json](execution-code/manifest.json) for the execution-source
snapshot. Exact review requests and sanitized errors are under `preflight/`.

## Continuation

Diagnose the configured scorer transport or configure a working scorer route/model.
Then use a new append-only preflight directory and complete the runtime gate before
any recipient exposure. Do not count these infrastructure failures as treatment
failures or change the frozen packets, oracle, scoring rules, or claim interpretations.

The harness was adjusted only before exposure to review fixtures separately. Its
runtime configuration remains thinking enabled, non-streaming, recipient maximum
65,536 tokens and scorer maximum 32,768 tokens. Actual response usage is preserved
for successful calls; failed-request usage is unknown.
