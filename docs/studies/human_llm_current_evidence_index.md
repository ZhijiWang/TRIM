# Design B Human-LLM Pilot: Current Evidence Index

Status: current navigation overlay. This page does not replace or rehash any
historical record and does not change a study gate.

## Provider and runtime evidence lineage

| Layer | Record | Interpretation |
|---|---|---|
| Historical provider planning v0.1 | `data/studies/human_llm_pilot/provider_model_account_verification.json` | Immutable record of the earlier blocked state. It remains valid historical evidence and is not overwritten. |
| Historical runtime draft | `data/studies/human_llm_pilot/runtime_settings_draft.json` | Immutable blocked draft; not a runtime freeze. |
| Current provider metadata audit v0.2 | `data/studies/human_llm_pilot/provider_model_account_verification_v0_2.json` | Current metadata-audit evidence. Result: `BLOCKED_NO_CREDENTIAL_AVAILABLE`; no metadata request or inference occurred. |
| Current runtime capability audit v0.1 | `data/studies/human_llm_pilot/runtime_capability_audit_v0_1.json` | Documents candidates only. Runtime remains blocked pending separately authorized synthetic no-source inference verification. |

The gate-status manifest remains the historical machine-readable gate snapshot
created with the blocked preparation layer. This overlay supplies current
evidence navigation without rewriting that hashed or historical record.

## Current decisions

- provider/model/account: `BLOCKED`
- runtime: `BLOCKED_PENDING_SYNTHETIC_NO_SOURCE_INFERENCE_VERIFICATION`
- pricing: `BLOCKED_PENDING_POINT_IN_TIME_PRICING_FREEZE`
- final authorization: `BLOCKED`
- human coding: `BLOCKED`
- model execution: `BLOCKED`
- overall: `EXECUTION_BLOCKED`

The v0.2 metadata audit found no local credential, made no network request,
called no inference endpoint, transmitted no prompt or private content, and did
not inspect a controlled packet. A future credential-enabled metadata rerun and
any later synthetic inference verification require separate reviewed tasks.
