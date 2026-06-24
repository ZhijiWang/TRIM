# TRIM Coding Manual v0.2: `friction_locus`

## Purpose

`friction_locus` identifies the point where the evidence-to-function conversion requires its main interpretive work. Each annotation receives one dominant locus. Secondary difficulties remain visible in `rationale_note` or `alternative_signature`.

Interpretive friction arises through the relation among textual evidence, the analytic task, the project's function vocabulary, and the coder's stated rationale. The field therefore records a situated judgement about where the conversion becomes most difficult to sustain.

Allowed values:

- `cue_function`
- `warrant_attribution`
- `warrant_relation`
- `operation_function`
- `boundary_setting`
- `temporal_layering`
- `perspective_assignment`
- `context_inference`

The ten-case corpus demonstrates five values. `boundary_setting` and `context_inference` have operational definitions and await positive out-of-sample cases. `cue_function` remains provisional until out-of-sample work establishes a stable decision rule.

## Selection Sequence

When several loci appear plausible, ask three questions:

1. Which candidate, if removed, would make the function hardest to sustain?
2. Which candidate most directly mediates the anchor-to-function conversion?
3. Which candidate explains the conversion with the fewest additional assumptions?

The selected value names the dominant threshold. A case that remains unresolved receives `uncertainty_flag=high`, an `alternative_signature` where possible, and a rationale note explaining both pathways.

### Dominant-threshold rule

`friction_locus` records the single point that most directly explains the evidence-to-function conversion. Use the counterfactual, proximity, and explanatory-sufficiency tests together:

- **Counterfactual test:** removing which candidate locus would make the function label hardest to sustain?
- **Proximity test:** which candidate most directly mediates the anchor-to-function conversion?
- **Explanatory-sufficiency test:** which candidate explains the conversion with the fewest additional assumptions?

If these tests still leave two viable loci, set `uncertainty_flag=high`, record the competing pathway in `alternative_signature` when possible, and explain the unresolved threshold in `rationale_note`.

## `cue_function`

### Definition

Use `cue_function` when the cue type itself creates the main interpretive problem: what divination, prophecy, testimony, confession, or another cue family is doing in the case.

### Selection conditions

Choose this value when:

- uncertainty centres on the function of the cue type;
- no more specific locus captures the conversion;
- project review confirms that the cue family itself remains the main threshold.

A visible interpretive act points toward `operation_function`. Authority granted to a source points toward `warrant_attribution`. Interaction among several warrants points toward `warrant_relation`.

### Current status

The demonstration corpus contains no positive `cue_function` case. The three *Macbeth* scenes show why: a shared cue family can produce different loci at the level of warrant, operation, and temporal layering.

## `warrant_attribution`

### Definition

Use `warrant_attribution` when one source, sign, speaker, medium, or result receives enough authority to support the function.

### Selection conditions

Choose this value when:

- one source carries the decisive warrant;
- the central question concerns whether that source can sustain the function;
- the annotation depends on granted authority.

A relation among several warrants points toward `warrant_relation`. A visible interpretive act points toward `operation_function`. Later fulfilment that reorganizes earlier evidence points toward `temporal_layering`.

### Demonstrated cases

- `ZZ_MIN_1`: Xin Liao's interpretation gives the milfoil result warranting force.
- `MAC_1_3`: confirmation by Ross and Angus gives the witches' words practical authority.

## `warrant_relation`

### Definition

Use `warrant_relation` when the main difficulty lies in how two or more warrants interact.

### Selection conditions

Choose this value when:

- several warrants conflict, rank, qualify, suspend, or contradict one another;
- the function depends on their relation;
- no single warrant explains the conversion on its own.

A single source receiving authority points toward `warrant_attribution`. A decisive testimonial standpoint points toward `perspective_assignment`. A later time layer that changes earlier evidence points toward `temporal_layering`.

### Demonstrated cases

- `ZZ_XI_4`: turtle-shell and milfoil results, ranking speech, and textual material remain in conflict.
- `GROVE_TAKEHIRO`: posthumous testimony enters an incompatible testimonial field and deepens the difficulty of adjudication.

## `operation_function`

### Definition

Use `operation_function` when a visible act of interpretation, consultation, confession, recognition, or self-reading converts evidence into function.

### Selection conditions

Choose this value when:

- the observable operation is the decisive converter;
- the cue matters through what an actor does with it;
- the function emerges from interpretation in action.

Authority granted to one source points toward `warrant_attribution`. Interaction among several warrants points toward `warrant_relation`. Later fulfilment that reclassifies earlier evidence points toward `temporal_layering`.

### Demonstrated cases

- `ZZ_XIANG_7`: Meng Xianzi's ritual-timing explanation converts failed divination into procedural intelligibility.
- `MAC_4_1`: Macbeth converts equivocal prophecy into operational security.
- `GROVE_TAJOMARU`: confession becomes self-justifying self-display.

## `boundary_setting`

### Definition

Use `boundary_setting` when the main interpretive work lies in deciding where the case, category, frame, or applicable scope begins and ends.

### Selection conditions

Choose this value when:

- changing the annotation boundary changes the function;
- scope determines which evidence, speaker, warrant, or frame belongs to the case;
- the principal judgement concerns inclusion and exclusion.

A stable unit containing conflicting warrants points toward `warrant_relation`. A missing contextual bridge points toward `context_inference`.

### Current status

The value awaits a positive out-of-sample demonstration. `ZZ_XI_4` provides a useful contrast: its unit contains several elements, yet the dominant issue is the relation among warrants inside that unit.

## `temporal_layering`

### Definition

Use `temporal_layering` when story time, discourse time, later fulfilment, retrospective framing, or reuse across time changes the function of earlier evidence.

### Selection conditions

Choose this value when:

- a later moment makes an earlier sign readable differently;
- prospective and retrospective positions interact;
- fulfilment or historical uptake changes the status of the original evidence.

A relation among warrants at one level points toward `warrant_relation`. A visible operation whose force does not depend on later time points toward `operation_function`.

### Demonstrated cases

- `ZZ_ZHUANG_22`: the sign remains active across projected descent and later historical readability.
- `MAC_5_8`: Macduff's disclosure reclassifies Macbeth's earlier assurance as an equivocal trap.

## `perspective_assignment`

### Definition

Use `perspective_assignment` when the main difficulty lies in whose standpoint, testimonial role, or narrative position determines the function.

### Selection conditions

Choose this value when:

- the annotation depends on the speaker's position;
- shame, accusation, self-defence, victimhood, or self-blame shapes the function;
- changing the testimonial standpoint would change the result.

Conflict among several accounts as warrants points toward `warrant_relation`. A confession treated mainly as an act points toward `operation_function`.

### Demonstrated case

- `GROVE_MASAGO`: victim-position, shame, accusation, and self-blame qualify one another, making testimonial position decisive.

## `context_inference`

### Definition

Use `context_inference` when the main threshold is the contextual bridge required to connect the immediate textual anchor to the function.

### Selection conditions

Choose this value when:

- the local passage cannot sustain the function without a specific contextual inference;
- the missing bridge, rather than the contextual evidence itself, is the dominant obstacle;
- the rationale identifies that bridge explicitly.

Ordinary use of narrative, historical, ritual, or scholarly context belongs in `epistemic_support`. A problem of unit scope points toward `boundary_setting`.

### Current status

The value awaits a positive out-of-sample demonstration. Its use should identify the precise contextual bridge and explain why the function depends on it.

## Key Distinctions

### `friction_locus` and `rationale_mechanism`

`friction_locus` identifies where the conversion becomes difficult. `rationale_mechanism` identifies what that threshold does as evidence becomes functional. A case may have the same locus with different mechanisms, or the same mechanism produced through different loci. For example, `ZZ_XI_4` and `GROVE_TAKEHIRO` both use `warrant_relation`, but their mechanisms differ because one extends deliberation while the other contradicts and suspends adjudication.

### `friction_locus` and `epistemic_support`

`friction_locus` identifies where the conversion requires added inferential work. `epistemic_support` identifies what carries the judgement across that threshold. Narrative or historical context can support an annotation whose locus remains `warrant_relation`, `temporal_layering`, or another more specific value.

### `warrant_attribution` and `warrant_relation`

`warrant_attribution` centres one source receiving warranting force. `warrant_relation` centres the interaction among several warrants. Min 1 and Macbeth Act 1.3 illustrate attribution; Xi 4 and Takehiro illustrate relation.

### `operation_function` and `warrant_attribution`

Choose `operation_function` when evidence already has standing and the decisive question is what a visible operation does with it. Choose `warrant_attribution` when the operation grants standing to a source, medium, speaker, or result.

Xiang 7 uses `operation_function` because the failed divination already counts as the relevant result and Meng Xianzi transforms its meaning. Min 1 uses `warrant_attribution` because Xin Liao's interpretation makes the result usable as warrant.

Counterfactual test: if the evidence already counts as relevant before the operation, and the function depends on how the operation handles it, prefer `operation_function`. If the evidence becomes usable as warrant through the operation that grants it standing, prefer `warrant_attribution`.

### `operation_function` and `warrant_relation`

Choose `operation_function` when the visible act performs the conversion. Choose `warrant_relation` when the act matters because it creates, ranks, or intensifies a relation among warrants. In Xi 4, the ranking speech matters through the hierarchy it creates between turtle-shell and milfoil results.

Counterfactual test: if the operation itself performs the conversion, prefer `operation_function`. If the operation mainly matters because it relates multiple warrants to one another, prefer `warrant_relation`.

### `cue_function` and `operation_function`

Choose `cue_function` when the evidentiary cue type itself leaves the function underdetermined. Choose `operation_function` when a visible action such as interpretation, confession, consultation, recognition, or self-reading converts evidence into function. Macbeth Act 4.1 uses `operation_function` because Macbeth's self-reading of the apparitions drives the conversion.

### `warrant_relation` and `temporal_layering`

Choose `warrant_relation` when local conflict among warrants produces the function. Choose `temporal_layering` when later fulfilment, historical readability, or retrospective framing reclassifies earlier evidence. Xi 4 centres cross-warrant conflict; Zhuang 22 centres time-layered uptake.

Counterfactual test: if removing the cross-warrant conflict removes the function, prefer `warrant_relation`. If removing the later temporal frame or later readability removes the function, prefer `temporal_layering`.

### `operation_function` and `temporal_layering`

Choose `operation_function` when a local act converts the evidence. Choose `temporal_layering` when a later moment changes the status of earlier evidence. Macbeth Act 5.8 centres the later fulfilment that reclassifies the earlier prophecy.

Counterfactual test: if the function is produced by the local operation itself, prefer `operation_function`. If the operation registers a later temporal reclassification of earlier evidence, prefer `temporal_layering`.

### `perspective_assignment` and `warrant_relation`

Choose `perspective_assignment` when one testimonial standpoint determines the function. Choose `warrant_relation` when incompatibility among several accounts determines the function. Masago illustrates perspective; Takehiro illustrates warrant relation.

### Compound and contested cases

`friction_locus` itself is not compound. When a record contains a compound `rationale_mechanism`, choose the locus that explains the primary mechanism and use `rationale_note` to describe how the secondary mechanism modifies the conversion. When two loci remain genuinely viable, preserve the second pathway through `alternative_signature` rather than combining loci in one field.

When `alternative_signature` is recorded, the rationale note should document the competing pathway clearly enough for review. The validator applies the language-neutral alternative-signature rationale threshold described in the codebook; the threshold is a minimum reviewability safeguard, not a quality score.

## Decision Tree

Use this sequence when several loci remain plausible:

1. Does the annotation unit or case boundary determine the result? → `boundary_setting`.
2. Does speaker position or testimonial standpoint determine the function? → `perspective_assignment`.
3. Do several warrants interact, conflict, rank, qualify, or suspend one another? → `warrant_relation`.
4. Does later fulfilment, retrospective framing, or historical readability reclassify earlier evidence? → `temporal_layering`.
5. Does one source, medium, speaker, or result receive warranting standing? → `warrant_attribution`.
6. Does a visible operation locally convert evidence into function? → `operation_function`.
7. Does a missing contextual bridge remain the dominant obstacle after the more specific loci have been considered? → `context_inference`.
8. When the cue type itself remains the dominant unresolved problem, consider provisional `cue_function` through project review.

Apply the counterfactual, proximity, and explanatory-sufficiency tests to the leading candidates. A remaining tie receives high uncertainty, an alternative signature where possible, and contested review.

## Reporting

Report the selected locus together with its evidence basis, mechanism, support, discourse position, temporal orientation, and uncertainty. Reliability analysis should preserve both exact agreement and the case-level location of disagreement.
