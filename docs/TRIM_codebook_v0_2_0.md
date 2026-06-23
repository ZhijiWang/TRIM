# TRIM Codebook v0.2.0

## Purpose

This codebook defines the fields, controlled vocabularies, compound rules, and review sequence used by TRIM. It is the canonical vocabulary reference for the package and accompanying research.

## Core Architecture

```text
Evidence nodes → anchor node → threshold–rationale edge → function node
```

Each annotation records selected evidence, an analytic anchor, a threshold–rationale relation, and a project-defined function. TRIM preserves this route as a reviewable object that can be validated, compared, and represented as a graph.

Interpretive friction marks the point where evidence requires additional warrant before it can sustain a function.

## Controlled Fields

- `friction_locus`
- `rationale_mechanism`
- `epistemic_support`
- `discourse_level`
- `temporal_orientation`
- `uncertainty_flag`

`friction_locus` identifies where the conversion requires its main inferential work. `epistemic_support` identifies the support used to sustain that conversion.

`context_inference` applies when the missing contextual bridge is itself the main threshold. Ordinary contextual evidence belongs in `epistemic_support` or the rationale note.

## Project Fields

Standard annotations contain `function_label`, `source`, `evidence_anchor`, `evidence_nodes`, `anchor_node`, and `rationale_note`. Optional project fields include `cue_family`, `broad_function_family`, `case_type`, and `language`.

`evidence_anchor` preserves textual location. `evidence_nodes` preserve decomposition. `anchor_node` gives the evidence a normalized analytic centre.

## `friction_locus`

Allowed values:

- `cue_function`
- `warrant_attribution`
- `warrant_relation`
- `operation_function`
- `boundary_setting`
- `temporal_layering`
- `perspective_assignment`
- `context_inference`

The ten-case corpus demonstrates `warrant_attribution`, `warrant_relation`, `operation_function`, `temporal_layering`, and `perspective_assignment`. `boundary_setting` and `context_inference` await positive out-of-sample testing. `cue_function` remains provisional until positive cases establish a stable rule.

## `rationale_mechanism`

Allowed values:

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

## `epistemic_support`

Allowed values:

- `textual_anchor`
- `internal_sequence`
- `ritual_sequence`
- `narrative_context`
- `scholarly_apparatus`
- `parallel_case`
- `metadata_context`
- `external_historical_context`
- `coder_inference`

## Other Controlled Values

`discourse_level`: `intradiegetic`, `extradiegetic`, `frame_narrative`, `dramatic_present`, `reported_speech`, `commentarial_discourse`.

`temporal_orientation`: `prospective`, `immediate`, `retrospective`, `recursive`, `suspended`, `prospective-retrospective`.

`uncertainty_flag`: `low`, `medium`, `high`.

## Compound Rules

`rationale_mechanism` and `epistemic_support` may contain one value or two values joined by `+`. For mechanisms, the first value records the main conversion and the second records a consequential modification. Order therefore preserves the primary/secondary distinction.

Validation rejects empty compounds, duplicate values, values outside the controlled set, and compounds longer than two elements.

## Dominant Threshold

Each annotation records one main threshold-rationale signature. When several loci appear plausible, apply three tests:

1. **Counterfactual:** which candidate, if removed, would make the function hardest to sustain?
2. **Proximity:** which candidate most directly mediates the anchor-to-function conversion?
3. **Explanatory sufficiency:** which candidate explains the conversion with the fewest added assumptions?

A case that remains unresolved receives `uncertainty_flag=high`, an `alternative_signature` where possible, and a rationale note explaining the competing pathways.

Rationale notes shorter than 30 characters generate a review warning. An annotation with `alternative_signature` requires a complete valid six-field alternative and a rationale note of at least 60 characters.

## Contested Review

The review asks whether the threshold is locatable, whether the rationale is coherent, and whether the disagreement resists simple refinement. Original annotations remain available alongside adjudicated results.

## Current Stage

The ten-case corpus establishes schema expressivity, traceability, and comparative payoff. The blinded pilot materials establish readiness for independent coding. Later work will test field agreement, comparative replication, provisional loci, and out-of-sample stability.

## Validator Role

The validator checks required fields, evidence-node presence, controlled values, compound shape, signature structure, contested-case documentation, and cross-case comparability. Scholarly review evaluates textual adequacy, interpretation, and adjudication.
