# γ-I v2 runner

This study-specific runner reuses `tools.assurance_eval.config` for private provider
configuration and uses a gamma-specific streaming transport for stateless API calls.
The transport buffers final text and exposes it only after a completed response.
It does not use the Assurance recipe, treatments, or scoring rules.
The γ inputs come directly from the Git blobs frozen by PRs #41 and #42.

Stages:

1. `preflight`: offline blob checks, exact section extraction, prompt/payload hashes.
2. `runtime`: non-experimental provider checks and independent packet review.
3. `run`: 27 isolated recipient histories, with initial persistence, index selection,
   exact payload return, and final judgment.
4. `score`: two separate label-blind scorer contexts per completed recipient record.

Example after the provider/profile has been configured and authorized:

```bash
python3 -m tools.gamma_eval runtime \
  --settings /absolute/private/setting.json \
  --profile PROFILE \
  --output PATH_TO_RUN_DIRECTORY
```

Use the same settings/profile/output for `run` and `score`. Credentials and endpoint
values are excluded from artifacts. Model configurations, requests, responses,
usage, retries, and elapsed time are recorded. Existing records are not overwritten.
Failed/incomplete calls must be reviewed before continuation. No automatic scientific
conclusion or overall winner score is produced.

The current parameters use thinking enabled, streaming wire responses, and maximum
output limits of 65,536 tokens for recipients and 32,768 for scorers. These are
runtime choices, not frozen treatment content. Any configuration change must happen
before recipient exposure and be captured by a new successful runtime preflight.
Streaming avoids the non-streaming transport failures observed during preflight;
it does not expose partial recipient judgments or advance the audit sequence early.

Offline boundary tests:

```bash
python3 -m unittest discover -s tests -p test_gamma_eval.py -v
```
