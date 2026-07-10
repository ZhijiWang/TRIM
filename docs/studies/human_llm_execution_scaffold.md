# Human–LLM no-call execution scaffold

Status: `EXECUTION_BLOCKED`

This scaffold prepares deterministic local machinery for the frozen Design B human–LLM pilot. It is not an execution authorization, runtime-settings freeze, provider client, account check, human-coding start, or model run. The implementation has no live provider transport and does not read credentials.

## Architecture

The scaffold lives under `src/trim_haa/llm/`, following the repository's existing Python package rather than creating a parallel `trim` package.

- `hashing.py` defines compact, key-sorted UTF-8 JSON serialization; prefixed SHA-256 byte hashes; record hashing with `record_hash` excluded; and record-hash verification.
- `frozen_reference.py` can read only six explicitly allowlisted public PR #18 metadata/schema paths from the pinned Git object `eac65f27bbe302a17e5f508ac1d516178e917aea`. It rejects every controlled source-packet path and has no fetch or network fallback.
- `gates.py` normalizes the public gate manifest. Restricted rights and controlled-access statuses are sufficient for preparation, but not execution.
- `request_preservation.py` constructs and preserves only a fixed synthetic, provider-neutral placeholder representation.
- `response_preservation.py` preserves raw synthetic bytes in controlled test storage, hashes those bytes, then parses and validates the preserved copy.
- `openai_adapter.py` contains a blocked planning adapter. It imports no SDK or network client and has no enabled execution path.
- `dry_run.py` validates public freeze metadata, the 25 non-blocked rights records, controlled-packet approval, blocked execution gates, and the checked-in metadata-only plan.

The planned provider is OpenAI and the candidate identifier is `gpt-5.4-mini`. Account availability remains unverified. The API surface and structured-output mode are candidate representations only; every account- or runtime-sensitive parameter remains `pending_account_verification` or `pending_provider_verification`.

## Public and controlled data separation

Public request envelopes contain identifiers, statuses, hashes, and controlled references only. Their schema has `additionalProperties: false` and provides no properties for raw prompts, source text, private packet content, copyrighted excerpts, model-visible source content, or credentials.

Public response envelopes contain preservation, parsing, validation, retry, error-class, and hash metadata only. There is no property for raw response content or parsed payload content. Raw synthetic fixtures are written only to caller-selected controlled test paths such as a temporary directory.

No checked-in request body contains a selected source, frozen assembled prompt, private packet text, or source-derived fixture. The checked-in dry-run report contains metadata and hashes only.

## Request preservation lifecycle

The implemented synthetic lifecycle is:

1. accept only the fixed synthetic case identifier and invented placeholder;
2. serialize the provider-neutral representation as canonical UTF-8 JSON;
3. preserve the exact bytes in caller-designated controlled storage;
4. compute the request byte hash;
5. create the public request envelope after preservation;
6. set `transmission_authorized: false`, `transmitted: false`, and provider request ID to null;
7. stop before the blocked adapter.

A future source-bearing request must not be constructed until controlled access, packet hash verification, access logging, account/runtime verification, pricing, and authorization gates have independently passed.

## Response preservation lifecycle

Synthetic response tests use manually written, non-literary fixtures. The lifecycle is:

1. preserve exact raw bytes in controlled test storage;
2. hash the preserved raw bytes;
3. read back and verify the preserved hash;
4. parse the preserved bytes;
5. validate parsed JSON against the frozen PR #18 model-authored response schema;
6. retain only non-sensitive status, hash, and schema-error-location summaries in the public envelope.

Invalid JSON, unknown categories, missing fields, malformed evidence/confidence fields, and extra properties fail without copying response content into public metadata.

## Gate enforcement

The normalized preparation decision accepts:

- rights evidence: `PASSED_WITH_DOWNSTREAM_GATES_BLOCKED`;
- controlled private-packet handling: `PASSED_WITH_CONTROLLED_ACCESS_ONLY`.

Those statuses do not authorize packet inspection or execution. The current blockers are:

- provider/model/account account availability;
- runtime settings;
- pricing;
- final authorization;
- human coding;
- model execution.

The adapter also refuses absent provider-transmission authorization, a draft runtime record, unverified account availability, forbidden public fields, incomplete request preservation, absent private-packet access authorization, absent source packet hash, and absent request byte hash. Even a hypothetical all-pass input reaches a final no-network refusal because no live implementation exists in this PR. There is no bypass flag or environment-variable override.

## Dry-run and network prohibition

Run:

```text
python scripts/dry_run_human_llm_execution.py
```

The successful terminal status is:

```text
DRY_RUN_VALID_EXECUTION_BLOCKED
```

Success means only that public metadata is internally consistent and execution is correctly blocked. The command constructs no provider request, reads no private packet, performs no human coding, calls no provider, transmits nothing, receives no response, and generates no output.

Tests disable sockets and environment lookup, restrict subprocess use during the dry-run to local `git show` reads of the public allowlist, and confirm that provider SDK/client construction, provider CLIs, and HTTP access are not used. OpenAI is not a dependency.

## Validation

`scripts/validate_human_llm_execution_scaffold.py` verifies the blocked draft and plan, strict envelopes, canonical hashes, no-call adapter, dry-run outcome, pinned public freeze hashes, selected-case/order invariants, unchanged PR #18 artifact paths, unchanged authoritative manual, unchanged package version, unchanged Core/provenance boundaries, and synthetic-fixture content restrictions.

This validator supplements and does not weaken `scripts/validate_human_llm_rights_gate.py`.

## Future activation sequence

The only permitted future sequence is:

1. independently audit the no-call scaffold;
2. verify account model listing in a separate authorized task;
3. verify and freeze runtime settings;
4. verify structured-output compatibility;
5. capture pricing close to authorized execution;
6. obtain final execution authorization;
7. verify controlled packet hashes and create access logs;
8. authorize human coding, if separately approved;
9. authorize model execution;
10. authorize provider transmission and execute.

Steps 7–10 are not currently authorized. Any failure or missing evidence keeps execution blocked.
