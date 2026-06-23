# Source Segmentation Workflow

## Purpose

TRIM can be used after source passages have been segmented into auditable
textual units. Source segmentation gives coders and reviewers a stable evidence
layer before TRIM annotation.

## Two-Layer Workflow

The source-segment layer and the TRIM annotation layer remain separate:

- `source_segments.csv` records source passages, locations,
  translations/paraphrases, and notes.
- TRIM annotation records evidence nodes, source-facing evidence anchor,
  normalized anchor node, `friction_locus`,
  `rationale_mechanism`, `function_label`, and `rationale_note`.
- `case_id` links the source-segment layer and the TRIM annotation layer.
- `segment_id` can be cited inside `evidence_anchor` or `rationale_note`.

This structure supports the workflow:

```text
source passages → auditable segments → TRIM annotation → validation, comparison, graph export
```

## Recommended Fields

- `segment_id`: stable identifier for the source segment.
- `case_id`: TRIM case identifier linked to the annotation row.
- `source`: source text or corpus.
- `language`: source language.
- `segment_order`: local order within the case.
- `original_text`: concise source anchor or passage label.
- `translation_or_paraphrase`: short translation, paraphrase, or content note.
- `location_note`: source location or testimony section.
- `segment_note`: brief note about how the segment supports review.

## Workflow Steps

1. Segment source passages.
2. Assign stable segment IDs.
3. Create at least one explicit `evidence_nodes` value for each standard TRIM
   annotation. Evidence nodes may be derived from one or more source segments,
   but the derivation remains a human coding decision.
4. Link the source-facing `evidence_anchor` to `segment_id` where useful.
5. Assign `anchor_node` as a normalized analytic label rather than duplicating
   the source reference.
6. Run `trim validate`.
7. Run `trim report`.
8. Run `trim compare`.
9. Run `trim graph`.
10. Use linked outputs for review and second-coder work.

## Example

The demonstration source-segment file includes three In a Grove cases:

| segment_id | case_id | source | segment note |
| --- | --- | --- | --- |
| `GROVE_TAJOMARU_01` | `GROVE_TAJOMARU` | In a Grove | Source segment used as evidence anchor for `operation_function / reframes`. |
| `GROVE_MASAGO_01` | `GROVE_MASAGO` | In a Grove | Source segment used as evidence anchor for `perspective_assignment / qualifies`. |
| `GROVE_TAKEHIRO_01` | `GROVE_TAKEHIRO` | In a Grove | Source segment used as evidence anchor for `warrant_relation / contradicts+suspends`. |

The script `examples/run_trim_with_source_segments.py` links these segment IDs
to the existing demonstration annotations, preserves their explicit evidence
nodes and normalized anchor nodes, and writes validation, comparison, report,
and graph outputs.

## Scope

Source segmentation supports auditability and second-coder review. The TRIM
validator continues to validate the annotation schema. Interpretive
adjudication remains part of the human review workflow.
