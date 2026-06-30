# Schema and Validator Changes for Unreleased 0.2.0

This note records the validation changes introduced before the first formal 0.2.0 release.

## Evidence and Anchor Structure

Standard annotations now include one or more evidence nodes, a source-facing `evidence_anchor`, and a normalized `anchor_node`.

The demonstration records already use this structure. Blank second-coder templates become valid after their evidence, anchor, signature, and rationale fields are completed.

Graph conversion now preserves the full evidence-to-anchor pathway. Projects adopting this source version should retain both the source reference and the analytic anchor label.

## Contested Rationale Structure

An `alternative_signature` activates two checks: the alternative pathway parses as a complete signature, and `rationale_note` contains at least 60 characters.

The length threshold provides a language-neutral minimum for review documentation. Interpretive quality remains part of scholarly assessment.

## Command-Line Status

`trim validate` writes the CSV report and returns `0` for valid or warnings-only input and `1` when errors are present. `--always-zero` supports report-only workflows.

## v0.2.1 Pilot-Informed Additions

v0.2.1 adds pilot-facing fields while preserving v0.2.0 compatibility:

- `primary_evidence_segment_ids`
- `context_segment_ids`
- `evidence_highlight`
- `language_access_mode`
- `case_scope`
- `shared_context_ids`
- `cross_case_context_permitted`
- `required_context_segments`

For v0.2.1 retest records, `primary_evidence_segment_ids` is required and must
contain one to three segment IDs. `context_segment_ids` is optional. A segment
cannot be both primary and context in the same record. When known segment IDs
are supplied to the validator, unknown IDs are errors.

Legacy v0.2.0 records with `evidence_nodes` remain loadable and valid. Graph
conversion uses `evidence_nodes` when present. If `evidence_nodes` is absent and
`primary_evidence_segment_ids` is present, graph conversion creates evidence
nodes from the primary segment IDs and stores context IDs in anchor metadata.

The repository's v0.2.1 retest closes the project-specific `function_label`
vocabulary to eight substantive labels plus `no_fit`. This is a project-level
pilot rule, not a claim that all future TRIM projects must use the same
function list.

`case_scope=multi_passage_single_case` records a formal case that contains
separated passages from the same work without using cross-case context. It
requires empty `shared_context_ids`, empty `required_context_segments`, and
`cross_case_context_permitted=no`.

Question logs now have a structured validation path for self-resolved
questions:

- `question_type`
- `provisional_resolution`
- `did_question_change_code`
- `blocking_or_nonblocking`
- `requires_manual_revision`

Low uncertainty with a complete `alternative_signature` produces a warning
because the v0.2.0 pilot showed that complete alternatives should normally
trigger at least medium uncertainty.

## Shared-Context Registry

v0.2.1 retest scope is represented by a separate registry file,
`data/retest_v0_2_1_shared_context_registry.csv`, rather than by free-text
manifest notes alone. The registry schema is:

- `shared_context_id`
- `description`
- `member_case_ids`
- `permitted_segment_ids`

The validator checks this registry against the retest manifest. Every
`shared_context_id` used by a case must exist in the registry. Every member case
must exist in the manifest. Every registry entry must contain at least two
member cases; singleton distributed passages should use
`case_scope=multi_passage_single_case` instead. Every permitted segment must
exist in a manifest `segment_ids` field and belong to a member case.
`required_context_segments` must exist and belong to the declared shared-context group. Annotation
`primary_evidence_segment_ids` are limited to local case segments, while
`context_segment_ids` may include local segments and permitted shared-context
segments.

For v0.2.0 compatibility, legacy annotations are not required to provide a
registry. v0.2.1 records that use shared-context fields should pass
`manifest_metadata` and `shared_context_registry` to `validate_record` or
`validate_dataframe`; the package builder does this for the public retest
materials.

## v0.2.2 Deployment Patch

v0.2.2 preserves schema support for `cue_family` and
`broad_function_family` for older datasets and researcher-facing descriptive
metadata, but removes both fields from the v0.2.2 coder-facing retest template.
They are optional, not coder-generated v0.2.2 fields, and should not be included
in v0.2.2 field-level agreement calculations.

v0.2.2 also adds the cross-file warning
`QUESTION_CHANGED_CODE_BUT_LOW_UNCERTAINTY`. Use
`validate_question_annotation_consistency` after returned annotations and
question logs are both available. The warning is emitted when an interpretive or
definitional question changed the code, but the final annotation uses
`uncertainty_flag=low` and no complete `alternative_signature`. This warning
does not automatically change the annotation and does not require an alternative
signature merely because a question occurred.
