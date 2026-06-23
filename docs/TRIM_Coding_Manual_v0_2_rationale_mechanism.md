# TRIM Coding Manual v0.2: `rationale_mechanism`

## Purpose

`rationale_mechanism` records what the dominant threshold does as evidence becomes functional. It names the conversion itself: supporting, contradicting, overriding, qualifying, reframing, stabilizing, extending, reactivating, suspending, projecting, authorizing, or narrowing.

The vocabulary crosses logical, interpretive, epistemic, and temporal dimensions because the mechanism field describes the action performed by the threshold-rationale relation.

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

## Compound Mechanisms

Each annotation records one main mechanism. A second mechanism may be added with `+` when it captures a consequential modification.

The first value names the dominant conversion. The second records an additional effect. Order therefore matters: `authorizes+reframes` and `reframes+authorizes` share a set but assign a different primary operation.

Intercoder reporting compares raw strings, exact sets, primary mechanisms, any overlap, and Jaccard overlap.

## `supports`

### Definition

Use `supports` when the threshold adds evidential backing to a function while leaving its frame and actionability largely stable.

### Selection logic

Choose this value when evidence strengthens an existing judgement. `authorizes` fits when the evidence grants standing for action. `stabilizes` fits when uncertainty settles into usable judgement. `reframes` fits when the interpretive frame changes.

### Demonstration status

The current corpus contains no primary `supports` case. `MAC_1_3` offers a contrast because confirmation authorizes and reframes the prophecy rather than merely adding backing.

## `contradicts`

### Definition

Use `contradicts` when the mechanism introduces incompatibility between a warrant and another account, expectation, or interpretive path.

### Selection logic

Choose this value when contradiction organizes the function. Add `suspends` when the incompatibility also prevents closure. `qualifies` fits a modification that leaves the claim recognizable. `overrides` fits a case in which one warrant displaces another.

### Demonstrated case

- `GROVE_TAKEHIRO`: posthumous testimony contradicts preceding accounts and, together with `suspends`, keeps adjudication open.

## `overrides`

### Definition

Use `overrides` when one warrant, operation, or judgement displaces another as the operative basis for function.

### Selection logic

Choose this value when replacement is decisive and one pathway remains active after another loses force. `contradicts` fits unresolved incompatibility. `qualifies` fits continued but reduced force. `extends` fits a conflict that remains active.

### Demonstration status

The current corpus contains no primary `overrides` case. `ZZ_XI_4` offers a contrast because competing warrants extend deliberation without producing a complete replacement.

## `qualifies`

### Definition

Use `qualifies` when the mechanism modifies, limits, or complicates a function while keeping its basic frame recognizable.

### Selection logic

Choose this value when the function remains usable but carries internal limits. `reframes` fits a change in interpretive frame. `narrows` fits a reduction in available meanings or uses. `suspends` fits blocked closure.

### Demonstrated case

- `GROVE_MASAGO`: victim-position, shame, accusation, and self-blame qualify one another within the testimony.

## `reframes`

### Definition

Use `reframes` when the mechanism changes the interpretive frame through which evidence becomes functional.

### Selection logic

Choose this value when the same evidence acquires a new kind of significance: confession becomes self-display, prophecy becomes actionable, or earlier assurance becomes a retrospective trap. `qualifies` retains the frame while modifying it. `narrows` reduces possibilities within a frame. `stabilizes` settles evidence into a usable judgement.

### Demonstrated cases

- `MAC_1_3`: confirmation reframes kingship as actionable.
- `MAC_4_1`: Macbeth reframes equivocal conditions as security.
- `MAC_5_8`: fulfilment reframes earlier assurance as a trap.
- `GROVE_TAJOMARU`: confession becomes self-justifying self-display.

## `stabilizes`

### Definition

Use `stabilizes` when the mechanism settles evidence into a usable judgement.

### Selection logic

Choose this value when sequence, standing, or interpretation becomes coherent enough for the function to hold. `extends` fits evidence that remains open. `projects` gives the judgement forward reach. `authorizes` grants standing for action.

### Demonstrated cases

- `ZZ_XIANG_7`: ritual sequence makes failed divination procedurally intelligible.
- `ZZ_MIN_1`: Xin Liao's reading stabilizes the result and, together with `projects`, gives it lineage significance.

## `extends`

### Definition

Use `extends` when the mechanism keeps evidence active, open, prolonged, or unresolved across the local sequence.

### Selection logic

Choose this value when significance continues because closure is delayed or the sign remains available for later uptake. `stabilizes` settles the evidence. `projects` directs it forward. `reactivates` brings previously inactive evidence back into use.

### Demonstrated cases

- `ZZ_XI_4`: competing warrants extend deliberation.
- `ZZ_ZHUANG_22`: the sign remains active across descent and later readability, combined with `projects`.

## `reactivates`

### Definition

Use `reactivates` when earlier or previously settled evidence returns to functional use in a later context.

### Selection logic

Choose this value when the evidence regains force after a period of reduced activity. `extends` fits continuous activity. `projects` moves significance forward from the present. `reframes` changes the meaning of earlier evidence.

### Demonstration status

The current corpus contains no primary `reactivates` case. `ZZ_ZHUANG_22` offers a contrast because the sign remains continuously active across projection and later uptake.

## `suspends`

### Definition

Use `suspends` when the mechanism prevents closure and keeps adjudication unresolved.

### Selection logic

Choose this value when the central effect is blocked resolution. `contradicts` identifies explicit incompatibility. `extends` keeps significance active across time or sequence. `qualifies` limits a function that remains usable.

### Demonstrated case

- `GROVE_TAKEHIRO`: posthumous testimony combines `contradicts+suspends`, adding incompatibility and preventing closure.

## `projects`

### Definition

Use `projects` when the mechanism gives evidence prospective reach.

### Selection logic

Choose this value when a sign, judgement, or interpretation becomes meaningful through future lineage, fulfilment, or outcome. `reactivates` returns earlier evidence to use. `extends` keeps significance open. `stabilizes` settles it in the present.

### Demonstrated cases

- `ZZ_MIN_1`: the stabilized judgement projects lineage significance.
- `ZZ_ZHUANG_22`: the sign extends across time and projects future descent.

## `authorizes`

### Definition

Use `authorizes` when the mechanism gives a function standing for action, uptake, or legitimate use.

### Selection logic

Choose this value when evidence changes what can now be treated as an actionable warrant. `supports` adds backing. `stabilizes` settles judgement. `reframes` changes the interpretive frame.

### Demonstrated case

- `MAC_1_3`: confirmation of Cawdor authorizes the prophecy and reframes kingship as actionable.

## `narrows`

### Definition

Use `narrows` when the mechanism reduces the range of meanings, possibilities, or practical uses available to the evidence.

### Selection logic

Choose this value when ambiguity is converted into a restricted operational reading. `qualifies` limits a claim while preserving several possibilities. `reframes` changes the frame. `stabilizes` settles the judgement without necessarily reducing its range.

### Demonstrated case

- `MAC_4_1`: Macbeth narrows equivocal conditions into a usable sense of security.

## Selection Sequence

When two mechanisms appear plausible, ask:

1. What is the main change between the evidence and the function?
2. Which value names that change most directly?
3. Does a second mechanism record a consequential effect that remains necessary to the explanation?

The first value records the primary conversion. The second value records the additional effect. A case that remains genuinely ambiguous should preserve the competing pathway through `alternative_signature` and `uncertainty_flag`.

## Reporting

Report mechanisms together with locus, evidence, support, discourse level, temporality, and uncertainty. Compound-aware analysis should preserve both the selected set and the primary-secondary order.
