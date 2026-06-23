# TRIM Codebook v0.2.0

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

Interpretive friction is a locatable difficulty in the warranted conversion
from textual evidence to an analytic function under an explicit interpretive
scheme. It is relational rather than a context-free property embedded in a
text. It arises through the relation among textual evidence, the analytic task,
the project's function vocabulary, and the coder's stated rationale. TRIM
preserves that difficulty as evidence-constrained, locatable, reviewable, and
comparable.

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

`friction_locus` and `epistemic_support` answer different questions:

- `friction_locus` records where the conversion is blocked or requires added
  inferential work.
- `epistemic_support` records what evidence or support the coder uses to cross
  that threshold.

Do not assign `context_inference` merely because contextual evidence is used.
Assign it only when the absence of a contextual bridge is itself the dominant
obstacle to evidence-to-function conversion.

## Structured Free-Text / Project-Specific Fields

| Field | Status | Standard annotation requirement |
| --- | --- | --- |
| `function_label` | project-specific free text | required |
| `cue_family` | project-specific free text | optional |
| `broad_function_family` | project-specific free text | optional |
| `case_type` | project-specific free text | optional |
| `language` | project-specific free text | optional |
| `source` | project-specific free text | required |
| `evidence_anchor` | project-specific free text | required |
| `evidence_nodes` | structured list / delimited text | at least one non-empty node required |
| `anchor_node` | project-specific free text | required |
| `rationale_note` | project-specific free text | required |

`function_label` is defined by the research project using TRIM rather than by a
global package vocabulary.

### Evidence and Anchor Fields

- `evidence_anchor` is the source-facing locatable span, quotation, passage
  label, or segment reference used to return to the text.
- `evidence_nodes` decomposes the selected evidence into one or more non-empty
  human-defined units that contribute to the anchor.
- `anchor_node` is the normalized analytic label around which those evidence
  nodes are organized.

TRIM does not define an anchor-only standard mode. Valid standard annotations
must supply all three fields. `evidence_anchor` and `anchor_node` may be closely
related, but they must not be treated as automatic substitutes: one preserves
source location, while the other supplies the analytic node label used in graph
construction.

## `friction_locus` Closed Set

- `cue_function`
- `warrant_attribution`
- `warrant_relation`
- `operation_function`
- `boundary_setting`
- `temporal_layering`
- `perspective_assignment`
- `context_inference`

## `friction_locus` Demonstration Status

| Status | Values |
| --- | --- |
| Active and demonstrated in the ten-case corpus | `warrant_attribution`, `warrant_relation`, `operation_function`, `temporal_layering`, `perspective_assignment` |
| Operational but awaiting positive out-of-sample testing | `boundary_setting`, `context_inference` |
| Provisional reserved value | `cue_function` |

`cue_function` should not be treated as empirically established in reliability
reporting until it is supported by positive out-of-sample cases and a stable
decision rule. `boundary_setting` and `context_inference` have operational
definitions but no positive demonstration cases; their stability remains to be
tested.

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

The vocabulary is intentionally cross-dimensional. Values may name logical
relations, interpretive operations, epistemic effects, or temporal effects. The
primary value records the dominant conversion, while an optional secondary
value records a consequential modification. Order therefore matters for the
primary/secondary distinction even when compound-aware intercoder analysis also
compares the values as sets.

## Compound `epistemic_support` Rule

`epistemic_support` may contain one value, or two values joined by `+`. Values
must be in the controlled set. More than two values, empty values, and
duplicate compound values are rejected by validation.

## Dominant Threshold Rule

Each annotation records one dominant threshold-rationale signature. The selected
`friction_locus` should identify the dominant converter from evidence to
function. Secondary difficulties can be recorded in `rationale_note` or, for a
contested reading, in `alternative_signature`.

When more than one locus is plausible, apply these tests:

1. **Counterfactual test:** which candidate locus, if removed, would make the
   function label hardest to sustain?
2. **Proximity test:** which locus most directly mediates the
   anchor-to-function conversion?
3. **Explanatory sufficiency test:** which locus explains the conversion with
   the fewest additional assumptions?

If the tests do not resolve the case, set `uncertainty_flag=high`, provide an
`alternative_signature` whenever possible, explain the unresolved choice in
`rationale_note`, and route the annotation to contested review.

Short `rationale_note` values generate a review warning:

```text
rationale_note is too short to support review; minimum recommended length is 30 characters.
```

The warning marks records that would benefit from fuller review documentation.

## Contested Annotation Workflow

TRIM operationalizes the recording-and-review workflow for contested thresholds.
If `alternative_signature` is present, it must parse and validate as a complete
six-field signature, and `rationale_note` must contain at least 60 characters.
This language-neutral character threshold is only a minimal documentation
safeguard; it is not evidence of interpretive quality. No English or
language-specific keywords are required.

TRIM also prepares human-review fields for the demarcation criterion:

- locatable?
- rationale-coherent?
- resists simple refinement?

Adjudication is carried out through the human scholarly review workflow.

## Expressivity And Pilot Reliability Work

The current demonstration corpus establishes expressivity and traceability.
The repository provides infrastructure for a three-case software demonstration
and a possible ten-case preliminary usability pilot. These can test whether the
manuals and workflow are usable and show where disagreements occur. They cannot
establish domain-general reliability, stable population-level agreement, or
universal reproducibility. A properly designed reliability evaluation remains
future work.

## Validator Review Boundary

The validator checks whether annotations conform to the schema. It supports
review by ensuring that required fields, controlled values, compound signatures,
and contested-case documentation are present and comparable. Interpretive
adjudication is carried out through the human review workflow.

The validator checks:

- required fields;
- at least one non-empty evidence node;
- controlled vocabulary conformance;
- compound value shape;
- well-formed friction signatures;
- language-neutral contested-case documentation length;
- cross-case comparability.
