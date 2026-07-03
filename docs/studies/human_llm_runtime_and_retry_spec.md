# Human-LLM Runtime and Retry Specification

Status: `RUNTIME_SETTINGS_BLOCKED_PENDING_PROVIDER_ACCOUNT_VERIFICATION`

No study model has been called. This specification records the required runtime behavior without freezing unresolved provider/account settings.

## Session Isolation

Each run must use a fresh stateless session. No prompt caching across conditions may be used unless provider behavior is documented and controlled before execution.

## Provider and Settings

Provider, model ID, account availability, structured-output mode, temperature, top-p, seed behavior, and maximum output tokens remain blocked pending official account verification.

## Response Mode

The intended response is structured JSON conforming to `schemas/human_llm_model_response.schema.json`. Exact API mode remains blocked until provider/model verification.

## Retry and Repair

Distinguish:

- API transport retry;
- provider failure retry;
- malformed JSON repair;
- substantive rerun.

Transport or provider failures may be retried only under the frozen retry policy. Malformed JSON may receive at most one mechanical repair attempt if the raw response is preserved first. Substantive reruns must be recorded as separate attempts and may not silently replace an earlier output.

## Failure Handling

Refusal, truncated output, no response, provider failure, rate limiting, and malformed JSON are recorded separately. They do not license invented annotation values.

## Preservation and Cost Logging

The harness must preserve raw request representation where available, complete assembled prompt text, raw response text, hashes, provider response metadata, token counts where available, and cost logs. Current pricing and account availability must be re-verified immediately before execution.

The assembled prompt instance hash is computed after source-packet and model-visible case variable substitution and before provider submission. It is stored outside the prompt. Provider request hash, if available, is a separate hash of provider-specific request wrapping.
