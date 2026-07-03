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

Component hashes are SHA-256 over UTF-8 bytes after LF normalization.

The assembled condition payload hash is SHA-256 over the exact condition payload after applying the Condition C manual injection rule when applicable.

The complete assembled prompt hash is SHA-256 over the exact five-part assembled text in the frozen order above. The template-level assembled prompt hash uses the public placeholders exactly as written. Case-level execution must compute and preserve a separate complete assembled input hash after replacing placeholders with the controlled source packet, case ID, run ID, instruction condition, prompt bundle version, and source packet hash.

## Preservation Rule

Before any model call, the harness must preserve:

- exact shared system text;
- exact condition payload;
- exact source-packet text;
- exact model response schema text;
- exact case/run context;
- complete assembled model-visible input;
- complete assembled model-visible input hash;
- provider-visible request representation where available.

No model call may occur in this PR.
