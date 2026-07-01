# TRIM-HAA Core schema

The Core schema is intentionally smaller than legacy TRIM. It is designed for every annotation stage in a human-AI audit study.

## Fields

| Field | Required | Controlled | Notes |
|---|---:|---:|---|
| `annotation_id` | yes | no | Globally unique record ID. |
| `case_id` | yes | no | Source/case ID. |
| `parent_annotation_id` | conditional | no | Empty for independent records; required for post-AI and control records. |
| `actor_id` | yes | no | Pseudonymous human or model actor. |
| `actor_type` | yes | yes | `human`, `model`. |
| `annotation_stage` | yes | yes | `human_pre`, `ai_independent`, `human_post_ai`, `human_second_pass_control`, `adjudicated`. |
| `primary_evidence_segment_ids` | yes | no | Pipe-separated segment IDs. |
| `function_label` | yes | study-specific | Final analytic label. |
| `rationale_mechanism` | yes | study-specific | Lightweight structured justificatory mechanism. |
| `uncertainty_flag` | yes | yes | `low`, `medium`, `high`. |
| `rationale_note` | yes | no | Submitted justificatory record. |
| `alternative_pathway_present` | yes | yes | `yes`, `no`. |
| `alternative_mechanism` | conditional | study-specific | Required when alternative is present. |
| `alternative_note` | conditional | no | Required when alternative is present. |
| `status` | yes | yes | `draft`, `locked`, `superseded`. |

## Design rules

- `annotation_id` must be globally unique.
- Independent records have empty `parent_annotation_id`.
- `human_post_ai` records must reference a locked `human_pre`.
- `human_post_ai` records identify the AI output shown through provenance, not through `parent_annotation_id`.
- `human_second_pass_control` records must reference a locked `human_pre`.
- `ai_independent` records require `actor_type=model`.
- Model records are model-generated justificatory artifacts, not hidden model reasoning.
- `rationale_note` records a submitted justification, not a cognitive trace.
- If `alternative_pathway_present=yes`, `alternative_mechanism` and `alternative_note` are required.

## Substantive burden

The human-facing Core asks for six substantive judgments per case:

1. primary evidence;
2. function label;
3. rationale mechanism;
4. uncertainty;
5. rationale note;
6. alternative present/absent, with details only if present.
