# Provider and Runtime Capability Audit

This versioned audit is a metadata-only preparation layer for the frozen OpenAI candidate `gpt-5.4-mini`. It does not replace the historical blocked records, freeze runtime settings, authorize provider transmission, or perform inference.

## Audit result

On 2026-07-13, `OPENAI_API_KEY` was not available in the local audit environment. The credential value was never read, printed, logged, hashed, serialized, or committed. Because no credential was present:

- no provider network request was made;
- exact-model account access was not verified;
- `/v1/responses` and Chat Completions were not called;
- no prompt, response schema, source text, or private content was transmitted;
- no controlled packet was accessed;
- no inference, human coding, or empirical work occurred.

The account result is `BLOCKED_NO_CREDENTIAL_AVAILABLE`. The existing provider/model/account gate therefore remains `BLOCKED`.

## Metadata boundary

The only live request supported by the audit command is an authenticated `GET /v1/models/{model}` retrieval pinned to `gpt-5.4-mini`. OpenAI documents this endpoint as returning basic model information such as identifier, owner, and permissioning. The audit allowlists only the exact returned model identifier and the provider-owned value `openai`; other owner values are suppressed to avoid recording organization or project identifiers. See the [Models API reference](https://platform.openai.com/docs/api-reference/models/object).

Run a future credential-enabled metadata check from a controlled local source checkout with:

```console
python scripts/audit_openai_model_metadata.py
```

The command checks only whether `OPENAI_API_KEY` is present and, when present, retrieves only the frozen candidate's metadata. Its output contains allowlisted, redacted metadata only. Updating a checked-in verification record after a successful rerun requires a separate reviewed change.

## Runtime candidates, not frozen settings

The runtime audit records the following candidate policy without claiming account/runtime support:

- Responses API;
- `text.format` with `type: json_schema` and `strict: true`;
- `store: false`;
- background mode disabled;
- no conversation state, files, tools, or web search;
- no parallel provider calls;
- request preservation before transmission;
- raw response preservation before parsing.

OpenAI documents the Structured Outputs request shape, but exact behavior for the frozen candidate remains unverified without a separately authorized no-source synthetic inference test. Temperature, `top_p`, seed, reasoning effort, maximum output tokens, timeout, and retry settings are not frozen by this audit. See [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs).

## Data-handling boundary

OpenAI's public data-control documentation says API data is not used for training unless the account opts in, and that abuse-monitoring and application-state retention can apply. `store: false` is the candidate request policy, but it does not by itself prove Zero Data Retention. Organization/project retention controls were not inspected, so Zero Data Retention is explicitly unverified. See [Data controls in the OpenAI platform](https://platform.openai.com/docs/models/default-usage-policies-by-endpoint).

## Remaining gates

- provider/model/account: `BLOCKED` because no credential was available for exact-model metadata retrieval;
- runtime: `BLOCKED_PENDING_SYNTHETIC_NO_SOURCE_INFERENCE_VERIFICATION`;
- pricing: `BLOCKED_PENDING_POINT_IN_TIME_PRICING_FREEZE`;
- final authorization: `BLOCKED`;
- human coding: `BLOCKED`;
- model execution: `BLOCKED`;
- overall: `EXECUTION_BLOCKED`.

The frozen candidate is not replaced by newer models. OpenAI publicly identifies GPT-5.4 mini as an API model, but public availability does not establish access for this account. See [Introducing GPT-5.4 mini and nano](https://openai.com/index/introducing-gpt-5-4-mini-and-nano/).
