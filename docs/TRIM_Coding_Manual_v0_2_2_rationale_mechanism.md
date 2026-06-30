# TRIM Coding Manual v0.2.2: `rationale_mechanism`

## Purpose

`rationale_mechanism` records what the dominant threshold does as evidence
becomes functional. It names the conversion, not the source genre and not the
function label.

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

One value is required. A second value may be joined with `+` when it captures a
consequential modification. The first value is dominant.

## Dominant-Mechanism Rule

Ask:

1. What is the main change between the primary evidence and the analytic
   function?
2. Which mechanism names that change most directly?
3. Does a secondary mechanism alter the explanation enough to record?

Do not use compounds as a list of every plausible effect. Use the second value
only when it changes how the primary mechanism should be read.

## Pilot-Informed Distinctions

### `stabilizes`, `authorizes`, and `extends`

Use `stabilizes` when the threshold settles evidence into usable judgement.

Use `authorizes` when the threshold gives evidence action-guiding standing,
legitimacy, or uptake.

Use `extends` when the threshold keeps deliberation, warrant conflict, or
significance active rather than closing it.

Actor action does not automatically mean `authorizes`. If the action occurs
while unresolved warrant conflict remains central, `extends` may be the better
mechanism. If the evidence becomes locally coherent without becoming a new
basis for action, `stabilizes` may be better.

### `authorizes` and `reframes`

Confirmation may make a source actionable and also change the frame through
which a future claim is read. Use a compound only when both effects are needed.
If one coder records attribution/authorization and another records
relation/authorization for a complete pathway, this may be substantive pathway
variation rather than error.

### `qualifies` and `reframes`

Use `qualifies` when the function remains recognizable but is limited,
complicated, or internally tensioned.

Use `reframes` when the interpretive frame itself changes. A testimony can
shift from apparent disclosure into self-presentation; a sign can shift from
warning into practical confidence; a fulfilled condition can reclassify a prior
assurance.

### `contradicts` and `suspends`

Use `contradicts` when a warrant or account is incompatible with another claim.
Use `suspends` when closure is blocked. The two often combine, but the primary
value should name the effect that most directly carries the function.

### `projects`, `extends`, and `reactivates`

Use `projects` when evidence is given forward reach.

Use `extends` when significance remains active or unresolved across a sequence.

Use `reactivates` when earlier or previously settled evidence returns to use in
a later context.

## Mechanism and Evidence Selection

The mechanism must be supportable from the one to three primary evidence
segments. Context segments can explain why the primary evidence matters, but the
mechanism should not depend on marking every supplied segment as primary.

If the mechanism seems to require more than three segments, identify where the
actual conversion turns. Place surrounding sequence in `context_segment_ids` and
explain the dependency in `rationale_note`.

## Mechanism and Uncertainty

Low uncertainty is appropriate only when one complete pathway is clearly
preferable and no fully specified competing signature remains viable.

Medium uncertainty is appropriate when a preferred mechanism remains better but
a complete alternative mechanism or locus-mechanism pathway is reasonably
defensible.

High uncertainty is appropriate when supplied evidence or rules cannot stabilize
the mechanism choice without further evidence or manual revision.

Do not equate source ambiguity with coder uncertainty automatically. The field
records confidence in the annotation choice.

## Decision Tree

1. Does the threshold settle evidence into usable judgement? -> `stabilizes`.
2. Does it give evidence action-guiding standing? -> `authorizes`.
3. Does it keep deliberation, significance, or warrant conflict active? ->
   `extends`.
4. Does it change the interpretive frame? -> `reframes`.
5. Does it reduce available meanings or practical uses? -> `narrows`.
6. Does it modify a function while preserving the frame? -> `qualifies`.
7. Does it introduce incompatibility? -> `contradicts`.
8. Does it prevent closure? -> `suspends`.
9. Does it send significance forward? -> `projects`.
10. Does earlier settled evidence return to use? -> `reactivates`.
11. Does one warrant displace another? -> `overrides`.
12. Does it add backing without action-guiding standing? -> `supports`.

This ordering is a coding aid. If the selected value feels forced, record the
reasoning and any complete alternative pathway.

