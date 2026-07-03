# Human-LLM Pilot Prompt Assembly Specification

Status: `PROMPT_ASSEMBLY_SPECIFIED_EXECUTION_BLOCKED`

This specification defines how model-visible inputs will be assembled for the Design B human-model procedural comparison. It does not authorize execution. Rights review, controlled private-packet handling, account-verified model settings, runtime preservation, and final execution authorization remain blocked.

## Assembly Order

Every model request must be assembled in this exact order:

1. `SYSTEM_PROMPT`
2. `CONDITION_PAYLOAD`
3. `SOURCE_PACKET_ENVELOPE`
4. `MODEL_RESPONSE_SCHEMA`
5. `CASE_AND_RUN_CONTEXT`

No component may be omitted, reordered, or replaced without creating a new prompt bundle version.

## Exact Component Join Rule

The five top-level components are joined with exactly two LF characters between components and exactly one final trailing LF after the last component.

The byte-equivalent rule is:

```python
normalize(SYSTEM_PROMPT).rstrip("\n")
+ "\n\n"
+ normalize(CONDITION_PAYLOAD).rstrip("\n")
+ "\n\n"
+ normalize(SOURCE_PACKET_ENVELOPE).rstrip("\n")
+ "\n\n"
+ normalize(MODEL_RESPONSE_SCHEMA).rstrip("\n")
+ "\n\n"
+ normalize(CASE_AND_RUN_CONTEXT).rstrip("\n")
+ "\n"
```

The final trailing newline is included. `normalize(...)` means decode as UTF-8 and convert CRLF and CR to LF.

## Shared Components

- `SYSTEM_PROMPT`: `prompts/human_llm_pilot/system_prompt.txt`
- `SOURCE_PACKET_ENVELOPE`: `prompts/human_llm_pilot/source_packet_envelope.txt`
- `MODEL_RESPONSE_SCHEMA`: `schemas/human_llm_model_response.schema.json`
- `CASE_AND_RUN_CONTEXT`: `prompts/human_llm_pilot/case_and_run_context.txt`

The source-packet envelope contains a controlled private packet placeholder in this public PR. The exact private source packet must be inserted only after rights and private-packet gates pass.

## Condition Payloads

Condition A uses `prompts/human_llm_pilot/condition_A.txt`.

Condition B uses `prompts/human_llm_pilot/condition_B.txt`.

Condition C uses `prompts/human_llm_pilot/condition_C.txt` plus the complete authoritative JSON manual.

## Condition C Manual Delivery

Condition C does not rely on repository access, browsing, tools, or a path-only reference. The execution harness must inject the full authoritative JSON manual into the assembled prompt.

Manual content source:

- path: `docs/manuals/friction_locus_manual_v0_1.json`
- SHA-256: `797d79fcdb29fc32850c3778c6afb029ac0768207ea33f66d714fe8fa8cb591a`
- encoding: UTF-8
- newline rule: normalize CRLF and CR to LF before hashing or insertion
- serialization rule: inject the file content verbatim after LF normalization
- excluded fields: none
- delimiters: `BEGIN_FULL_MANUAL_JSON` and `END_FULL_MANUAL_JSON`

The Condition C payload is:

1. the LF-normalized content of `prompts/human_llm_pilot/condition_C.txt`;
2. one newline;
3. `BEGIN_FULL_MANUAL_JSON`;
4. one newline;
5. the LF-normalized content of `docs/manuals/friction_locus_manual_v0_1.json`;
6. one newline;
7. `END_FULL_MANUAL_JSON`;
8. one trailing newline.

## Hashing Rules

Component hash: SHA-256 over each source component's UTF-8 bytes after LF normalization.

The assembled condition payload hash is SHA-256 over the exact condition payload after applying the Condition C manual injection rule when applicable.

Assembled prompt template hash: SHA-256 over the assembled prompt while public placeholders remain unchanged.

Assembled prompt instance hash: SHA-256 over the assembled prompt after substituting the controlled source packet and explicitly model-visible variables: case ID, instruction condition, and prompt bundle version. This is the authoritative hash of the exact model-visible input.

Provider request hash: if the API wraps the model-visible prompt into a provider-specific JSON request, preserve a separate provider request hash where available. Do not confuse provider request hash with the model-visible assembled prompt instance hash.

No prompt field may depend on the resulting assembled prompt hash. `assembled_prompt_hash`, source packet hash, provider, model, run ID, runtime settings, retry metadata, and other harness-only metadata are stored outside the model-visible prompt.

Correct sequence:

1. Load each source component.
2. Normalize CRLF and CR to LF.
3. Substitute controlled source packet, case ID, instruction condition, prompt bundle version, and any explicitly model-visible case variables.
4. Assemble the five components using the exact join rule above.
5. Preserve the exact model-visible assembled text.
6. Compute SHA-256 over its UTF-8 bytes.
7. Store the resulting hash outside the prompt.
8. Submit the already-hashed exact text to the provider.
9. Preserve the provider-visible request representation where available.

## Preservation Rule

Before any model call, the harness must preserve:

- exact shared system text;
- exact condition payload;
- exact source-packet text;
- exact model response schema text;
- exact case/run context;
- complete assembled model-visible input;
- complete assembled model-visible input hash;
- provider request hash separately from the model-visible prompt hash where available;
- provider-visible request representation where available.

No model call may occur in this PR.
