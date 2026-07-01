# TRIM Coding Manual v0.2.1: `friction_locus`

## Purpose

`friction_locus` identifies where the evidence-to-function conversion requires
its main interpretive work. Select one dominant locus. Preserve secondary or
legitimately competing pathways in `rationale_note` and, when complete, in
`alternative_signature`.

v0.2.1 revises the v0.2.0 manual only where the locked pilot and adjudication
showed instability.

Allowed values:

- `cue_function`
- `warrant_attribution`
- `warrant_relation`
- `operation_function`
- `boundary_setting`
- `temporal_layering`
- `perspective_assignment`
- `context_inference`

## Selection Sequence

1. Identify the project-defined analytic function.
2. Mark one to three primary evidence segments.
3. Ask which candidate locus most directly mediates those segments into the
   function.
4. Use the counterfactual, proximity, and explanatory-sufficiency tests.
5. If two complete pathways remain defensible, choose the preferred pathway,
   set uncertainty at least medium, and record the other as
   `alternative_signature`.

## Analytic Function Versus Actor Action

Default rule:

```text
Code the project-defined analytic function of the evidence-to-function
conversion. Actor uptake counts as the function only when action-guiding
standing is the central analytic role, not merely because an actor makes a
decision.
```

Actor action is evidence. It is not automatically the analytic function. A
character can act while the text still leaves the central conversion in
stabilization, extended deliberation, temporal layering, or warrant relation.

Boundary test:

- If the actor's uptake gives the evidence action-guiding standing and that
  standing is the main analytic role, authorization may dominate.
- If the actor acts while unresolved warrant conflict remains the reason the
  case matters, do not let the action erase extended deliberation.
- If the actor's reading makes a local sign coherent without making a new
  action legitimate, stabilization may dominate.

## Locus Definitions

### `cue_function`

Use when the cue type itself creates the main interpretive problem and no more
specific locus captures the conversion. Treat this value as provisional unless
the case genuinely turns on what the cue family is doing.

### `warrant_attribution`

Use when one source, sign, speaker, medium, or result gains standing. The
central question is whether that source can sustain the function.

Contrast with `warrant_relation`: if the function depends on how two or more
warrants interact, conflict, confirm, rank, or qualify one another, relation is
likely dominant.

Special rule for confirmation cases: confirmation may both grant standing to
one warrant and change the relation between a confirmed and an unconfirmed
claim. If both complete pathways are defensible, preserve both rather than
forcing one into error.

### `warrant_relation`

Use when the function depends on interaction among two or more warrants. The
relation may be conflict, rank, confirmation, contradiction, suspension, or
mutual qualification.

Do not choose this value merely because several segments are present. Choose it
when no single warrant explains the conversion by itself.

### `operation_function`

Use when a visible act of interpretation, consultation, confession, recognition,
or self-reading performs the conversion.

The operation must be doing the work. If the same operation would produce a
different function from another speaker position, test `perspective_assignment`.
If the operation chiefly grants standing to one source, test
`warrant_attribution`.

### `boundary_setting`

Use when deciding the case boundary, frame, or scope changes the function.
v0.2.1 source packets should make scope explicit, so this value should not be
used to compensate for hidden packet ambiguity.

### `temporal_layering`

Use when later fulfilment, retrospective framing, story time, discourse time, or
reuse across time changes how earlier evidence functions.

Do not confuse this with `temporal_orientation`, which records the direction of
the completed interpretation.

### `perspective_assignment`

Use when the function depends on whose standpoint, role, shame, self-defence,
accusation, or self-presentation determines the conversion.

Counterfactual test: if the same confession, recognition, or report from a
different standpoint would materially change the function, perspective is
likely dominant. A complete operation-focused alternative may still be
legitimate.

### `context_inference`

Use when the coder must supply a contextual bridge not already performed
explicitly in the local passage.

Do not use `context_inference` merely because context helps. Ordinary
contextual support belongs in `epistemic_support`. If a textual actor visibly
performs the conversion, prefer `operation_function` unless another more
specific locus dominates.

Tests:

- Positive: the local passage gives a sign, but the function depends on a
  contextual rule that no actor states or applies.
- Near miss: an actor states the contextual rule and applies it to the sign.
  This normally points to `operation_function`.
- Counterfactual: remove the external bridge. If the function collapses while
  the local operation remains, `context_inference` may dominate.
- Explicit-textual-operation exclusion: if the passage itself visibly performs
  the conversion, do not select `context_inference` only because that conversion
  uses context.

## Boundary Pairs

### Authorization, Stabilization, Extended Deliberation

Choose authorization only when action-guiding standing is the analytic role.
Choose stabilization when uncertainty or disorder is settled into usable
judgement. Choose extended deliberation when competing warrants remain active.

Actor decision is not enough by itself. Ask what the evidence-to-function
conversion does at the level of the research project.

### `warrant_attribution` / `warrant_relation`

Attribution: one source gains standing.

Relation: two or more warrants interact and the interaction carries the
function.

When confirmation both grants standing and reorganizes a warrant relation, mark
medium uncertainty or higher and preserve a complete alternative signature if
both pathways remain defensible.

### `operation_function` / `perspective_assignment`

Operation: the act performs the conversion.

Perspective: the standpoint makes the act function as it does.

The same confession can be read through the act of confessing or through the
speaker's self-presentation. Treat complete alternatives as substantive pathway
variation when both are textually grounded.

### `reported_speech` / `frame_narrative`

This pair is recorded in `discourse_level`, but it affects locus decisions in
testimony cases. If a local testimony carries the conversion, local speech may
dominate. If the outer arrangement among testimonies changes the function,
frame-level reasoning may dominate. Record the non-dominant level in the
rationale when relevant.

## Decision Tree

1. Does case scope or inclusion determine the result? -> `boundary_setting`.
2. Does speaker standpoint determine the function? -> `perspective_assignment`.
3. Do multiple warrants interact in a way no single warrant can explain? ->
   `warrant_relation`.
4. Does a later time layer reclassify earlier evidence? -> `temporal_layering`.
5. Does one source gain standing? -> `warrant_attribution`.
6. Does a visible operation perform the conversion? -> `operation_function`.
7. Is an unstated contextual bridge the main threshold? -> `context_inference`.
8. Does the cue type itself remain the unresolved problem? -> `cue_function`.

The tree is a guide, not an answer key. Use it with primary evidence segments,
the function boundary rule, and uncertainty calibration.

