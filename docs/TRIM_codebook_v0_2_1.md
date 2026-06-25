# TRIM Codebook v0.2.1

## Purpose

This codebook defines the pilot-informed v0.2.1 annotation fields, controlled
vocabularies, evidence-selection model, and review rules for TRIM:
Threshold-Rationale Interpretive Modelling.

v0.2.1 is a prospective retest design. The v0.2.0 ten-case usability pilot
remains a locked historical record. Neither coder's original annotations are
overwritten or treated as ground truth.

## Core Architecture

```text
Evidence nodes -> anchor node -> threshold-rationale edge -> function node
```

TRIM records a human judgement about how textual evidence becomes an analytic
function. The software validates structure and controlled vocabularies; it does
not adjudicate interpretation.

## Function Labels

For the v0.2.1 retest, `function_label` is a closed project-specific list:

- `immediate_stabilization`
- `extended_deliberation`
- `ambition_trigger_authorization`
- `false_security`
- `retrospective_trap`
- `self_justification`
- `self_defence_self_accusation`
- `epistemic_suspension`
- `no_fit`

Use `no_fit` when none of the eight substantive labels can be supported without
inventing a pathway outside the project vocabulary. Do not use `no_fit` merely
because two substantive labels are hard to choose between; record the preferred
pathway, uncertainty, and any complete alternative signature instead.

### Analytic Function Versus Actor Uptake

Default rule:

```text
Code the project-defined analytic function of the evidence-to-function
conversion. Actor uptake counts as the function only when action-guiding
standing is the central analytic role, not merely because an actor makes a
decision.
```

Actor action does not erase an unresolved narrative, warrant, or deliberative
structure. A character acting on a sign does not automatically make the
function authorization. Ask whether the case is mainly about action-guiding
standing, stabilized intelligibility, or sustained warrant conflict.

- Use `ambition_trigger_authorization` when anticipated or desired outcomes are
  given standing for actor-level uptake or decision-making.
- Use `immediate_stabilization` when evidence is settled into a usable local
  judgement without action-guiding standing becoming the main analytic role.
- Use `extended_deliberation` when competing warrants remain active even if an
  actor selects one path.

Neutral boundary pair:

- A sign is explained so that a local failure becomes intelligible; no actor's
  future course is made newly legitimate. This points toward stabilization.
- A sign is treated as standing for a prospective decision, and that standing is
  the reason the evidence matters analytically. This points toward
  authorization.

## Evidence Fields

v0.2.1 makes evidence selection discriminative.

| Field | Status | Rule |
| --- | --- | --- |
| `primary_evidence_segment_ids` | required for v0.2.1 coding | one to three segment IDs |
| `context_segment_ids` | optional | supporting segments that help interpret the primary evidence |
| `evidence_highlight` | optional | a short within-segment phrase or location note |
| `evidence_nodes` | backward-compatible canonical field | older records may continue to use this text/list field |
| `evidence_anchor` | required | source-facing span, quote, or segment reference |
| `anchor_node` | required | normalized analytic anchor |

Primary evidence is the smallest segment set without which the coded pathway
would no longer be supportable. Contextual support helps explain sequence,
speaker role, source setting, or background but is not itself the main
conversion point.

Sequence can matter without making every segment primary. If more than three
segments appear indispensable, choose the one to three segments where the
conversion actually turns, place the remaining segments in `context_segment_ids`,
and explain the dependency in `rationale_note`. A repeated all-segment strategy
does not satisfy the v0.2.1 evidence-selection task unless the rationale
explains why each selected segment is primary.

Software mapping: when `evidence_nodes` is present, graph conversion uses it as
the canonical evidence-node text. When `evidence_nodes` is absent and
`primary_evidence_segment_ids` is present, graph conversion creates evidence
nodes from the primary segment IDs and stores context IDs in anchor metadata.

## Controlled Signature Fields

| Field | Status |
| --- | --- |
| `friction_locus` | controlled |
| `rationale_mechanism` | controlled, up to two values with `+` |
| `epistemic_support` | controlled, up to two values with `+` |
| `discourse_level` | controlled |
| `temporal_orientation` | controlled |
| `uncertainty_flag` | controlled |

## `friction_locus`

- `cue_function`
- `warrant_attribution`
- `warrant_relation`
- `operation_function`
- `boundary_setting`
- `temporal_layering`
- `perspective_assignment`
- `context_inference`

### `context_inference` Exclusion Rule

Use `context_inference` when the coder must supply a contextual bridge not
already performed explicitly in the local passage. When a textual actor visibly
performs the conversion, prefer `operation_function` unless another more
specific locus dominates. Ordinary contextual support belongs in
`epistemic_support`, not automatically in `context_inference`.

Positive example: the local passage gives a bare sign, while the coder must
bring in a known institutional rule to explain why that sign can carry the
function. The contextual bridge is not performed in the passage.

Near miss: a speaker in the passage states the institutional rule and applies it
to the sign. The local operation is visible, so `operation_function` normally
dominates.

Counterfactual test: if the outside bridge were removed, would the function
collapse while the local operation stayed unchanged? If yes, `context_inference`
may be dominant.

Explicit-textual-operation exclusion test: if a character, narrator, witness,
interpreter, or consultant explicitly turns the evidence into its local
meaning, do not select `context_inference` only because the operation uses
contextual knowledge.

### `warrant_attribution` Versus `warrant_relation`

Use `warrant_attribution` when one source, sign, speaker, medium, or result
gains standing. Use `warrant_relation` when the function depends on interaction
among two or more warrants.

When confirmation both grants standing to one warrant and changes the relation
between confirmed and unconfirmed claims, either pathway may be legitimate if
both complete signatures are defensible. Record the preferred pathway, set
uncertainty at least medium, and preserve the alternative in
`alternative_signature`. Disagreement on this boundary can represent
substantive pathway variation rather than coder error.

### `operation_function` Versus `perspective_assignment`

Use `operation_function` when confession, recognition, interpretation, or
consultation as an act performs the conversion. Use `perspective_assignment`
when the speaker's standpoint, role, shame, self-defence, accusation, or
self-presentation determines the function.

Counterfactual test: if the same act performed from another standpoint would
produce a materially different function, `perspective_assignment` is likely
dominant. A complete act-focused alternative can still remain legitimate and
should be recorded through `alternative_signature`.

## `rationale_mechanism`

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

`rationale_mechanism` may contain one value or two values joined by `+`. The
first value is dominant. The second records a consequential modification.

Authorization requires action-guiding standing. Stabilization settles evidence
into usable judgement. Extension keeps deliberation, warrant conflict, or
significance active.

## `epistemic_support`

- `textual_anchor`
- `internal_sequence`
- `ritual_sequence`
- `narrative_context`
- `scholarly_apparatus`
- `parallel_case`
- `metadata_context`
- `external_historical_context`
- `coder_inference`

`epistemic_support` names what carries the judgement across the threshold. It
does not name where the conversion becomes difficult.

## `discourse_level`

- `intradiegetic`
- `extradiegetic`
- `frame_narrative`
- `dramatic_present`
- `reported_speech`
- `commentarial_discourse`

Code the level at which the evidence-to-function conversion is analytically
operative. Use `reported_speech` when the local speech act itself carries the
conversion. Use `frame_narrative` when the outer arrangement of embedded
accounts changes the function. When both are relevant, choose the dominant level
and record the other in `rationale_note` or `alternative_signature`.

## `temporal_orientation`

- `prospective`
- `immediate`
- `retrospective`
- `recursive`
- `suspended`
- `prospective-retrospective`

`temporal_orientation` describes the direction of the completed interpretation.
It is distinct from `temporal_layering`, which is a friction-locus value.

## `uncertainty_flag`

- `low`: one complete pathway is clearly preferable and no fully specified
  competing signature remains viable.
- `medium`: one pathway is preferable but a complete alternative signature is
  reasonably defensible.
- `high`: evidence or rules cannot stabilize the choice without further
  evidence or revision.

A complete plausible alternative signature should normally trigger at least
medium uncertainty. Textual ambiguity alone does not automatically produce high
coder uncertainty; this field records confidence in the annotation choice, not
how ambiguous the source is in general.

## Alternative Signatures

`alternative_signature` must contain a complete six-field signature:

```text
friction_locus / rationale_mechanism / epistemic_support / discourse_level / temporal_orientation / uncertainty_flag
```

When present, `rationale_note` must explain the competing pathway. v0.2.1
validation warns when `alternative_signature` is paired with low uncertainty.

## Question Log

Record every definitional, interpretive, procedural, or packet-level question,
even when you can provisionally resolve it yourself. Formal coding still
prohibits case-specific coaching before lock.

Required question-log fields:

- `question_id`
- `case_id`
- `question_type`
- `question_text`
- `provisional_resolution`
- `did_question_change_code`
- `blocking_or_nonblocking`
- `requires_manual_revision`
- `coder_id`

## Language Access

v0.2.1 records language access instead of assuming original-language
reproducibility.

- `direct_original_language_access`
- `published_translation`
- `project_authored_close_support`
- `summary_mediated`
- `mixed`

The v0.2.0 pilot is described as a multilingual, translation- and
summary-mediated usability pilot. For v0.2.1, either recruit coders who can read
the source languages directly or explicitly standardize translation-mediated
conditions.

## Shared Context Metadata

v0.2.1 cases must state whether coders may use only a local passage, the entire
work, supplied related cases, or an explicitly defined shared narrative field.

| Field | Values |
| --- | --- |
| `case_scope` | `local_passage`, `complete_work`, `supplied_related_cases`, `shared_narrative_field` |
| `shared_context_ids` | optional delimited IDs |
| `cross_case_context_permitted` | `yes` or `no` |
| `required_context_segments` | optional segment IDs |

If a function depends on accumulated incompatibility or a shared narrative
field, the permission must be explicit.

Shared-context groups are represented in
`data/retest_v0_2_1_shared_context_registry.csv`, with one row per
`shared_context_id`. The registry records a neutral description, member case
IDs, and the segment IDs available to that group. A case with
`cross_case_context_permitted=no` must have empty `shared_context_ids` and
empty `required_context_segments`. A case with `case_scope=supplied_related_cases`
or `case_scope=shared_narrative_field` must name a valid registry entry and use
`cross_case_context_permitted=yes`. Local primary evidence must come from the
case's own `segment_ids`; context evidence may use local segments plus the
segments permitted by the declared shared-context group.

## Backward Compatibility

Existing v0.2.0 annotations remain loadable. Records with `evidence_nodes`
continue to validate under the legacy evidence model unless they opt into
v0.2.1 fields or status. v0.2.1 retest records require
`primary_evidence_segment_ids`, `language_access_mode`, `case_scope`, and
`cross_case_context_permitted`.
