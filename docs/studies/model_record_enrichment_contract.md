# Model Record Enrichment Contract

Status: `ENRICHMENT_CONTRACT_SPECIFIED_EXECUTION_BLOCKED`

The model must return only a model-authored annotation payload conforming to `schemas/human_llm_model_response.schema.json`. The model must not author runtime metadata, hashes, provider metadata, record IDs, timestamps, run IDs, parse status, retry counts, or review linkage fields.

## Before the Call

The execution harness supplies or freezes:

- case ID;
- controlled source packet;
- source packet hash;
- prompt version;
- instruction condition;
- assembled prompt hash;
- run ID;
- provider;
- requested model;
- requested model settings.

## Raw Response Preservation

Immediately after provider response, before parsing or repair, the harness must:

- preserve exact raw response bytes/text;
- compute `raw_output_hash`;
- store provider response metadata when available;
- not alter raw output before hashing.

## Parsing

The harness validates the raw model-authored payload against `schemas/human_llm_model_response.schema.json`.

It records:

- `parse_status`;
- parsing errors;
- whether a mechanical formatting repair was attempted;
- retry count;
- technical failure status.

No substantive field may be silently repaired. At most one formatting repair may be attempted for syntactic JSON wrapping or escaping, and the original raw response remains the object hashed as `raw_output_hash`. Technical retries are distinct from parse repair. A parse failure is represented in the run manifest or failure record without inventing annotation values.

## Enrichment

After raw preservation and parsing, the harness adds:

- `record_type = model_coder_record`;
- `actor_type = model`;
- `case_id`;
- `record_id`;
- `timestamp`;
- `manual_version`;
- `review_of_record_id = null`;
- `review_of_record_hash = null`;
- `run_id`;
- `provider`;
- `model`;
- `model_version_if_known`;
- `prompt_version`;
- `instruction_condition`;
- `source_packet_hash`;
- `raw_output_hash`;
- `parse_status`;
- `retry_count`;
- `technical_failure_status`;
- final `record_hash`.

The final `record_hash` is computed only after enrichment. The enriched record validates against `schemas/human_llm_coder_output.schema.json`.

Review/adjudication records are separate later records. They link to the original proposal by `review_of_record_id` and `review_of_record_hash` and never overwrite the original model proposal.
