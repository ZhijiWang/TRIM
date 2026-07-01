# TRIM-HAA assistance provenance

Assistance provenance is a sidecar. It describes how a record was produced and what AI output was visible. It does not replace the raw annotation record.

## Required relationships

- `HUMAN_PRE` is locked before AI exposure.
- `AI_RECORD` is produced independently with a frozen prompt/configuration.
- `HUMAN_POST_AI` references the locked `HUMAN_PRE`.
- `HUMAN_SECOND_PASS_CONTROL` references the locked `HUMAN_PRE` and records rereading without AI.

## Model metadata

For every `ai_independent` record, record:

- model provider;
- model name;
- provider version or date label;
- prompt template ID;
- prompt hash;
- model run ID;
- retry count;
- regenerated-output flag;
- sampling settings where available.

Do not fabricate provider-side version, random seed, or internals. If only a date label is available, record the date and report the limitation.

## Prompt hashing

`prompt_hash` is generated from exact prompt text. `system_prompt_hash` is recorded only when the system prompt is available to the researcher. Hidden chain-of-thought must not be collected.

## Exposure fields

`ai_output_exposed` records what was shown:

- `none`
- `label_only`
- `evidence_only`
- `label_and_evidence`
- `rationale_only`
- `full_core_record`
- `full_core_and_depth`

`exposure_order` records whether the participant worked human-first, AI-first, or in a control second pass.

## Change flags

Changed-field flags are descriptive consistency fields. They should match raw pre/post differences and should not classify behaviour as bias or error.

