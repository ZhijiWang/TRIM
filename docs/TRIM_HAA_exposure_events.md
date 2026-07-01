# TRIM-HAA exposure events

The current prototype supports one AI exposure per human-post record through provenance fields:

- `exposed_ai_annotation_id`;
- `exposed_model_run_id`.

It also defines an exposure-event table for future multiple-exposure support.

## Exposure-event fields

- `exposure_event_id`
- `human_post_annotation_id`
- `human_pre_annotation_id`
- `ai_annotation_id`
- `model_run_id`
- `case_id`
- `exposure_sequence`
- `output_components_shown`
- `exposure_timestamp`
- `interface_condition`
- `notes`

## Validation

Exposure events must point to:

- an existing human-post record;
- the correct human-pre parent;
- an existing `ai_independent` record;
- the same case;
- the AI record's model-run ID.

Multiple exposure events for one human-post record are allowed as a future design path, but currently produce a warning because prototype reports assume one primary exposed AI record.

