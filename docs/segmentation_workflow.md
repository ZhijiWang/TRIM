# Source Segmentation Workflow

## Purpose

Source segmentation gives TRIM a stable evidential layer before annotation. It turns passages into auditable textual units that coders and reviewers can cite, compare, and revisit.

## Two Connected Layers

The workflow links two forms of structure:

- `source_segments.csv` records passages, locations, translations or paraphrases, and review notes;
- TRIM annotations record evidence nodes, source-facing evidence anchors, normalized anchor nodes, function labels, and threshold-rationale fields.

`case_id` links the two layers. `segment_id` gives each passage a stable reference that can appear in `evidence_anchor` and `rationale_note`.

```text
source passages → auditable segments → TRIM annotation → validation, comparison, graph export
```

## Recommended Fields

- `segment_id`: stable identifier for the source segment;
- `case_id`: TRIM case identifier;
- `source`: source text or corpus;
- `language`: source language;
- `segment_order`: local order within the case;
- `original_text`: concise source anchor or passage label;
- `translation_or_paraphrase`: short translation, paraphrase, or content note;
- `location_note`: source location or testimony section;
- `segment_note`: brief note supporting review.

## Workflow

1. Segment the source passages.
2. Assign stable segment IDs.
3. Create one or more evidence nodes for each annotation.
4. Link `evidence_anchor` to the relevant segment IDs.
5. Assign `anchor_node` as the normalized analytic centre of the selected evidence.
6. Run `trim validate`.
7. Run `trim report`.
8. Run `trim compare`.
9. Run `trim graph`.
10. Use the linked outputs for review and intercoder analysis.

Evidence nodes may draw on one or several source segments. Their construction remains part of the interpretive act, while the segment layer preserves the textual basis from which that act proceeds.

## Demonstration

The demonstration file includes three *In a Grove* cases:

| segment_id | case_id | source | segment note |
| --- | --- | --- | --- |
| `GROVE_TAJOMARU_01` | `GROVE_TAJOMARU` | In a Grove | Tajōmaru testimony section. |
| `GROVE_MASAGO_01` | `GROVE_MASAGO` | In a Grove | Masago testimony section. |
| `GROVE_TAKEHIRO_01` | `GROVE_TAKEHIRO` | In a Grove | Takehiro testimony section. |

`examples/run_trim_with_source_segments.py` links these segments to the demonstration annotations and writes validation, comparison, report, and graph outputs.

## Analytic Role

Segmentation supports auditability, textual return, and intercoder review. Validation checks the annotation schema; scholarly adjudication evaluates the interpretation built from those segments.
