# TRIM Coding Manual v0.2: `rationale_mechanism`

## Purpose

`rationale_mechanism` records how the dominant threshold converts evidence into
function. It names the action performed by the threshold-rationale relation:
settling, extending, reframing, qualifying, authorizing, narrowing, projecting,
or otherwise changing how evidence becomes functional.

## Allowed Values

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

## Compound Mechanism Rule

One primary mechanism is required. One optional secondary mechanism may be added
with `+`. Use compound values when the secondary mechanism clarifies temporal,
logical, or perspectival reach. Avoid stacking more than two mechanisms. The
primary mechanism should name the main conversion. The secondary mechanism
should name the important modification.

## `supports`

### Definition

Use `supports` when the threshold adds evidential backing to a function without
making that function actionable or changing its frame.

### Use when

- Evidence strengthens an existing judgement.
- The mechanism is evidential backing rather than authorization.
- The function is helped by the evidence but remains otherwise stable.

### Use another value when

- The evidence makes a function actionable or legitimate. Use `authorizes`.
- The evidence settles uncertainty into usable judgement. Use `stabilizes`.
- The evidence changes the frame. Use `reframes`.

### Positive example from existing demo cases

No current demo annotation uses `supports` as its coded mechanism.

Contrast: Macbeth Act 1.3 uses `authorizes+reframes` because partial
confirmation gives the prophecy warranting force and changes kingship into an
actionable possibility.

### Confusable with

- `authorizes`
- `stabilizes`

### Decision tip

Ask whether the evidence adds backing or grants standing for action. If it adds
backing, use `supports`. If it grants standing, use `authorizes`.

## `contradicts`

### Definition

Use `contradicts` when the mechanism introduces incompatibility between a
warrant and another account, expectation, or interpretive path.

### Use when

- A later or alternative warrant conflicts with another warrant.
- The conversion depends on incompatibility rather than synthesis.
- Contradiction is the main mechanism that makes the function visible.

### Use another value when

- The effect is to prevent closure without direct incompatibility. Use
  `suspends`.
- The effect is to modify or limit a claim. Use `qualifies`.
- One warrant displaces another. Use `overrides`.

### Positive example from existing demo cases

Takehiro's posthumous testimony uses `contradicts+suspends`: posthumous medium
speech introduces an extraordinary warrant that contradicts the preceding
accounts and prevents closure.

### Confusable with

- `suspends`
- `qualifies`
- `overrides`

### Decision tip

Use `contradicts` when incompatibility is explicit enough to organize the
function. Add `suspends` when that incompatibility also blocks closure.

## `overrides`

### Definition

Use `overrides` when one warrant, operation, or threshold displaces another as
the basis for function.

### Use when

- One warrant becomes dominant over a competing warrant.
- A later judgement cancels or displaces a prior one.
- The function depends on replacement rather than coexistence.

### Use another value when

- Warrants remain in conflict without one clearly displacing the other. Use
  `contradicts` or `warrant_relation` with an appropriate mechanism.
- A warrant is ranked but still remains active. Use `extends` or `qualifies`
  where appropriate.

### Positive example from existing demo cases

No current demo annotation uses `overrides` as its coded mechanism.

Contrast: Xi 4 uses `extends` because conflict among turtle result, milfoil
result, ranking speech, and line text keeps deliberation open rather than
allowing one warrant to fully replace the others.

### Confusable with

- `contradicts`
- `qualifies`
- `stabilizes`

### Decision tip

Ask whether one warrant remains as the operative basis after another is
displaced. If so, use `overrides`.

## `qualifies`

### Definition

Use `qualifies` when the mechanism modifies, limits, or complicates a function
without fully changing the frame.

### Use when

- A testimony or warrant takes on a function but remains internally limited.
- The annotation depends on complication rather than full reframing.
- The mechanism narrows the force of a claim without reducing possibilities in
  the manner of `narrows`.

### Use another value when

- The interpretive frame changes. Use `reframes`.
- Equivocal possibilities are reduced into a restricted use. Use `narrows`.
- A claim is blocked from closure. Use `suspends`.

### Positive example from existing demo cases

Masago's testimony uses `qualifies`: victim-position, shame, accusation, and
self-blame qualify one another rather than settling into a single testimonial
role.

### Confusable with

- `reframes`
- `narrows`
- `suspends`

### Decision tip

Use `qualifies` when the function remains recognizable but becomes limited or
complicated.

## `reframes`

### Definition

Use `reframes` when the mechanism changes the interpretive frame through which
evidence becomes functional.

### Use when

- A confession becomes self-display.
- A prophecy becomes an actionable possibility or a retrospective trap.
- The same evidence is treated through a new interpretive frame.

### Use another value when

- The range of possibilities is restricted. Use `narrows`.
- Evidence is settled into usable judgement. Use `stabilizes`.
- A function is modified without frame change. Use `qualifies`.

### Positive example from existing demo cases

Macbeth Act 5.8 uses `reframes`: later fulfilment reclassifies Macbeth's
earlier assurance as an equivocal trap.

Tajōmaru's testimony uses `reframes`: confession is converted from apparent
truth-disclosure into self-justifying self-display.

### Confusable with

- `qualifies`
- `narrows`
- `authorizes`

### Decision tip

Ask whether the evidence is being understood through a different frame. If the
frame changes, use `reframes`.

## `stabilizes`

### Definition

Use `stabilizes` when the mechanism settles evidence into a usable judgement.

### Use when

- A sign, result, or interpretation becomes procedurally intelligible.
- Uncertainty is reduced enough for the annotation's function to hold.
- The function is produced by restoring sequence, standing, or judgement.

### Use another value when

- Evidence remains open or prolonged. Use `extends`.
- The mechanism pushes significance forward. Use `projects`.
- The mechanism authorizes action. Use `authorizes`.

### Positive example from existing demo cases

Xiang 7 uses `stabilizes`: Meng Xianzi's explanation converts failed divination
into procedural intelligibility by restoring ritual sequence.

Min 1 uses `stabilizes+projects`: Xin Liao's auspicious interpretation settles
the Yi-related result while projecting lineage significance forward.

### Confusable with

- `extends`
- `supports`
- `authorizes`

### Decision tip

Use `stabilizes` when the threshold makes the evidence usable by settling its
force.

## `extends`

### Definition

Use `extends` when the mechanism keeps evidence active, open, prolonged, or
unresolved across the local sequence.

### Use when

- Conflict prevents clean closure.
- A sign remains active across later readability.
- The mechanism prolongs significance rather than settling it.

### Use another value when

- The evidence settles into usable judgement. Use `stabilizes`.
- Significance is pushed forward as prediction or expectation. Use `projects`.
- Earlier evidence is brought back into use. Use `reactivates`.

### Positive example from existing demo cases

Xi 4 uses `extends`: conflict among turtle result, milfoil result, ranking
speech, and line text prevents clean closure.

Zhuang 22 uses `extends+projects`: the sign remains active across projected
descent and later historical readability.

### Confusable with

- `stabilizes`
- `projects`
- `reactivates`

### Decision tip

Use `extends` when the threshold keeps evidence active rather than settling it.

## `reactivates`

### Definition

Use `reactivates` when the mechanism brings previously settled or earlier
evidence back into functional use.

### Use when

- A prior sign returns to relevance.
- Earlier evidence gains renewed function in a later context.
- The mechanism depends on renewed activation rather than simple continuation.

### Use another value when

- The sign remains continuously active. Use `extends`.
- Significance is projected forward from the current moment. Use `projects`.
- A later frame reclassifies earlier evidence. Use `reframes` or pair with the
  relevant temporal coding.

### Positive example from existing demo cases

No current demo annotation uses `reactivates` as its coded mechanism.

Contrast: Zhuang 22 uses `extends+projects` because the sign remains active
across projected descent and later readability rather than returning after a
settled interval.

### Confusable with

- `extends`
- `projects`
- `reframes`

### Decision tip

Use `reactivates` when the evidence had become settled or inactive and then
returns to functional use.

## `suspends`

### Definition

Use `suspends` when the mechanism prevents closure.

### Use when

- Conflicting warrants keep the case unresolved.
- The annotation foregrounds blocked adjudication.
- A warrant adds uncertainty rather than settling the function.

### Use another value when

- The mechanism directly introduces incompatibility. Use `contradicts`.
- The mechanism keeps significance open over time. Use `extends`.
- A function is limited but remains usable. Use `qualifies`.

### Positive example from existing demo cases

Takehiro's posthumous testimony uses `contradicts+suspends`: posthumous medium
speech contradicts prior testimony and prevents closure.

### Confusable with

- `contradicts`
- `extends`
- `qualifies`

### Decision tip

Use `suspends` when closure is the issue. Pair with `contradicts` when the
blocked closure comes from incompatibility.

## `projects`

### Definition

Use `projects` when the mechanism pushes significance forward from the current
moment.

### Use when

- A sign supports prospective expectation.
- A result becomes meaningful through future lineage, fulfilment, or outcome.
- The mechanism gives evidence forward reach.

### Use another value when

- Earlier evidence returns to functional use. Use `reactivates`.
- Evidence remains open without clear forward projection. Use `extends`.
- Evidence is settled in the present. Use `stabilizes`.

### Positive example from existing demo cases

Min 1 uses `stabilizes+projects`: the Yi-related result is accepted as a stable
prospective lineage judgement.

Zhuang 22 uses `extends+projects`: the sign remains active across projected
descent and later historical readability.

### Confusable with

- `extends`
- `reactivates`
- `stabilizes`

### Decision tip

Use `projects` when the threshold gives evidence prospective reach.

## `authorizes`

### Definition

Use `authorizes` when the mechanism makes a function actionable, legitimate, or
warranted.

### Use when

- A source or result receives standing that can guide action.
- Evidence authorizes uptake rather than simply supporting an existing claim.
- The threshold changes what can now be treated as usable warrant.

### Use another value when

- Evidence only adds backing. Use `supports`.
- Evidence is settled into judgement. Use `stabilizes`.
- The main effect is frame change. Use `reframes`.

### Positive example from existing demo cases

Macbeth Act 1.3 uses `authorizes+reframes`: confirmation of Cawdor gives the
witches' speech warranting force and reframes kingship as an actionable
possibility.

### Confusable with

- `supports`
- `stabilizes`
- `reframes`

### Decision tip

Use `authorizes` when evidence gains force as warrant for action, legitimacy,
or uptake.

## `narrows`

### Definition

Use `narrows` when the mechanism reduces equivocal, conditional, or plural
possibilities into a more restricted functional use.

### Use when

- A conditional prophecy is treated as practical security.
- An equivocal field is reduced into a narrower action-guiding reading.
- The function depends on restriction rather than broad reframing alone.

### Use another value when

- The evidence is understood through a new frame. Use `reframes`.
- The function is modified or limited without restricting possibilities. Use
  `qualifies`.
- The evidence settles into judgement. Use `stabilizes`.

### Positive example from existing demo cases

Macbeth Act 4.1 uses `reframes+narrows`: Macbeth converts equivocal conditional
prophecy into practical security.

### Confusable with

- `reframes`
- `qualifies`
- `stabilizes`

### Decision tip

Use `narrows` when the main effect is reducing the range of possible meanings
or uses.

## Key Distinctions

### `reframes` vs `narrows`

- `reframes`: changes the interpretive frame through which evidence functions.
- `narrows`: reduces equivocal, conditional, or plural possibilities into a
  more restricted functional use.

Counterfactual test: if the passage changes what the evidence is taken to mean,
use `reframes`. If the passage reduces the range of possible meanings or uses,
use `narrows`.

Macbeth Act 4.1 uses `reframes+narrows` because Macbeth reframes conditional
prophecy as guarantee and narrows equivocation into practical security.

### `supports` vs `authorizes`

- `supports`: adds evidential backing.
- `authorizes`: makes a function actionable, legitimate, or warranted.

Macbeth Act 1.3 uses `authorizes+reframes` because partial confirmation makes
the prophecy usable as warrant and changes kingship into an actionable
possibility.

### `stabilizes` vs `extends`

- `stabilizes`: settles the evidence into a usable judgement.
- `extends`: keeps the evidence active, open, prolonged, or unresolved across
  the local sequence.

Use Xiang 7 and Min 1 for stabilization. Use Xi 4 and Zhuang 22 for extension.

### `projects` vs `reactivates`

- `projects`: pushes significance forward from the current moment.
- `reactivates`: brings a previously settled or earlier sign back into
  functional use.

Use Min 1 and Zhuang 22 for projection. No current demo annotation uses
`reactivates`.

### `contradicts` vs `suspends`

- `contradicts`: introduces incompatibility.
- `suspends`: prevents closure.

Takehiro's posthumous testimony uses `contradicts+suspends`.

### `qualifies` vs `reframes`

- `qualifies`: modifies, limits, or complicates a function without fully
  changing the frame.
- `reframes`: changes the frame through which evidence becomes functional.

Use Masago for `qualifies` and Tajōmaru for `reframes`.

## Decision Tree

Use this sequence when selecting the primary mechanism:

1. Does the threshold settle evidence into usable judgement? → `stabilizes`.
2. Does it keep evidence open or prolonged? → `extends`.
3. Does it make evidence actionable or legitimate? → `authorizes`.
4. Does it change the interpretive frame? → `reframes`.
5. Does it restrict equivocal possibilities? → `narrows`.
6. Does it modify or complicate a function? → `qualifies`.
7. Does it introduce incompatibility? → `contradicts`.
8. Does it prevent closure? → `suspends`.
9. Does it push significance forward? → `projects`.
10. Does it bring earlier settled evidence back into use? → `reactivates`.
11. Does one warrant displace another? → `overrides`.
12. Does it add evidential backing without authorizing action? → `supports`.

This ordering is a coding convention for reliability work and can be tested in
future reliability studies.
