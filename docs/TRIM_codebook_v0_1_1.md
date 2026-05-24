# TRIM Codebook v0.1.1

## Purpose

This codebook defines the annotation fields, controlled vocabularies, compound
value rules, and review workflow used by TRIM: Threshold–Rationale Interpretive
Modelling.

This codebook is the canonical source for the controlled vocabulary used by the
package and accompanying article.

## Package Scope

TRIM supports well-formed, comparable, and reviewable human annotation. The
package checks controlled vocabulary conformance, parses friction signatures,
generates comparison tables, exports graph representations, and prepares
contested thresholds for scholarly review.

## Core Architecture

```text
Evidence nodes → anchor node → threshold–rationale edge → function node
```

Each annotation records human-selected evidence, an anchor, the
threshold-rationale relation, and a function label. Human coders provide the
interpretive labels; the package validates and compares the resulting
annotations.

## Field Name Note

In article prose, the `discourse_level` field may be described as
"narrative/discourse presentation level." The package field name remains
`discourse_level`.

## Controlled Fields

| Field | Status |
| --- | --- |
| `friction_locus` | controlled |
| `rationale_mechanism` | controlled, compound allowed |
| `epistemic_support` | controlled, compound allowed |
| `discourse_level` | controlled |
| `temporal_orientation` | controlled |
| `uncertainty_flag` | controlled |

## Structured Free-Text / Project-Specific Fields

| Field | Status |
| --- | --- |
| `function_label` | project-specific free text |
| `cue_family` | project-specific free text |
| `broad_function_family` | project-specific free text |
| `case_type` | project-specific free text |
| `language` | project-specific free text |
| `source` | project-specific free text |
| `evidence_anchor` | project-specific free text |
| `evidence_nodes` | project-specific free text |
| `anchor_node` | project-specific free text |
| `rationale_note` | project-specific free text |

`function_label` is defined by the research project using TRIM rather than by a
global package vocabulary.

## `friction_locus` Closed Set

- `cue_function`
- `warrant_attribution`
- `warrant_relation`
- `operation_function`
- `boundary_setting`
- `temporal_layering`
- `perspective_assignment`
- `context_inference`

## `rationale_mechanism` Closed Set

- `supports`
- `contradicts`
- `overrides`
- `qualifies`
- `reframes`
- `stabilizes`
- `extends`
- `reactivates`
- `suspends`
- `projects`
- `authorizes`
- `narrows`

## `epistemic_support` Controlled Values

- `textual_anchor`
- `internal_sequence`
- `ritual_sequence`
- `narrative_context`
- `scholarly_apparatus`
- `parallel_case`
- `metadata_context`
- `external_historical_context`
- `coder_inference`

## `discourse_level` Controlled Values

- `intradiegetic`
- `extradiegetic`
- `frame_narrative`
- `dramatic_present`
- `reported_speech`
- `commentarial_discourse`

## `temporal_orientation` Controlled Values

- `prospective`
- `immediate`
- `retrospective`
- `recursive`
- `suspended`
- `prospective-retrospective`

## `uncertainty_flag` Controlled Values

- `low`
- `medium`
- `high`

## Compound Mechanism Rule

`rationale_mechanism` may contain one value, or two values joined by `+`.
Values must be in the controlled set. More than two values, empty values, and
duplicate compound values are rejected by validation.

## Compound `epistemic_support` Rule

`epistemic_support` may contain one value, or two values joined by `+`. Values
must be in the controlled set. More than two values, empty values, and
duplicate compound values are rejected by validation.

## Dominant Threshold Rule

Each annotation records one dominant threshold-rationale signature. The selected
`friction_locus` should identify the dominant converter from evidence to
function. Secondary difficulties can be recorded in `rationale_note` or, for a
contested reading, in `alternative_signature`.

Short `rationale_note` values generate a review warning:

```text
rationale_note is too short to support review; minimum recommended length is 30 characters.
```

The warning marks records that would benefit from fuller review documentation.

## Contested Annotation Workflow

TRIM operationalizes the recording-and-review workflow for contested thresholds.
It stores `alternative_signature`, requires documentation through
`rationale_note`, and prepares human-review fields for the demarcation
criterion:

- locatable?
- rationale-coherent?
- resists simple refinement?

Adjudication is carried out through the human scholarly review workflow.

## Expressivity And Reliability

The current demonstration corpus establishes expressivity and traceability.
Intercoder reliability is evaluated through independently coded annotations
from two or more coders. The included second-coder CSV is a template for that
future validation stage.

## Validator Review Boundary

The validator checks whether annotations conform to the schema. It supports
review by ensuring that required fields, controlled values, compound signatures,
and contested-case documentation are present and comparable. Interpretive
adjudication is carried out through the human review workflow.

The validator checks:

- required fields;
- controlled vocabulary conformance;
- compound value shape;
- well-formed friction signatures;
- contested-case documentation;
- cross-case comparability.
