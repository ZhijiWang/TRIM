# Friction Locus Coding Manual v0.1
Manual version: `friction_locus_manual_v0_1`  
Status: `AUTHORITATIVE_FOR_PROTOCOL_REVIEW`  
Effective date: 2026-07-02  
Repository commit: `TO_BE_REPLACED_BY_FINAL_COMMIT`  
Manual hash: `TO_BE_RECORDED_IN_MANIFEST`
## 1. Scope and claim boundary
This is a provisional audit vocabulary for small-N, interpretation-intensive annotation. It is designed to make evidence selection, counterfactual tests, uncertainty, alternative pathways, and procedural disagreement reviewable. It is not an exhaustive ontology of interpretation, not a natural-kind claim, and not empirical validation. Agreement under this manual demonstrates procedural comparability under stated conditions, not ontological truth. The manual does not make one coder a gold standard. The categories identify the dominant procedural locus of unresolved interpretive friction: the point at which conversion from selected evidence to interpretation becomes unstable.
## 2. Core concepts
- **evidence**: Textual material selected by a coder as supporting the proposed interpretation. Evidence must be cited by stable evidence ID when records are produced.
- **function/label**: The submitted primary interpretive claim or label whose evidential support is being audited.
- **warrant**: A source, sign, speaker, medium, result, or relation that licenses movement from evidence to interpretation.
- **operation**: A visible act of interpretation, testimony, consultation, recognition, confession, translation, classification, or self-reading that converts evidence into function.
- **relation**: A conflict, ranking, qualification, interaction, or suspension among warrants.
- **perspective**: The speaker, witness role, focalization, standpoint, or testimonial position through which evidence is presented or made functional.
- **temporal layer**: A later, retrospective, fulfilled, reused, or historically readable layer that changes the function of earlier evidence.
- **boundary**: The scope of the case, interpretive unit, category, speaker, episode, or application field.
- **context**: A bridge beyond the local anchor that is needed to license the interpretation.
- **dominant friction locus**: The single primary procedural place where evidence-to-interpretation conversion is most unstable after counterfactual tests.
- **unresolved**: A permitted final state when the record cannot responsibly choose a dominant locus.
- **alternative pathway**: A complete or partial interpretive route that remains plausible and is preserved rather than silently discarded.
- **escalation**: A governance status used when the record needs review, cannot force a final category, or proposes a review-required value.

## 3. Global coding sequence
1. identify focal interpretive decision.
2. identify selected evidence.
3. state proposed primary interpretation.
4. retain plausible alternatives.
5. identify where conversion from evidence to interpretation becomes unstable.
6. apply relevant counterfactual tests.
7. choose dominant friction locus.
8. record uncertainty.
9. escalate where required.

## 4. Evidence-before-locus rule

Coders must record selected evidence and a concise rationale before assigning `friction_locus`. The friction locus is not a substitute for the primary label or interpretation; it audits where the evidence-to-interpretation conversion becomes procedurally unstable.
## 5. One dominant locus rule

Each record requires exactly one primary friction locus or `unresolved`. Secondary loci may be described in rationale or decision path only when the schema permits; they are not arbitrary multi-label outputs. If two loci remain tied after counterfactual testing, the record must escalate or use `unresolved` rather than forcing a false precision.
## 6. Eight category sections
### `cue_function`
- **Category ID**: `cue_function`
- **One-sentence definition**: The cue family itself remains the dominant procedural locus after more specific operation, warrant, relation, perspective, temporal, boundary, and context loci have been excluded.
- **Analytic question**: Is the unresolved conversion produced by what kind of cue this is, rather than by who uses it, how it is used, or how warrants relate?
- **Use when**:
  - The record turns on the function of a cue type such as omen, testimony, prophecy, sign, inscription, confession, or token.
  - No more specific locus explains the instability.
  - The cue family remains unstable even after evidence, speaker, operation, warrant, time, boundary, and context checks.
- **Do not use when**:
  - Do not use when a visible interpretive act converts the evidence; use operation_function.
  - Do not use when a specific source or sign is granted authority; use warrant_attribution.
  - Do not use as a default for difficult cases.
- **Use another value when**:
  - Use operation_function when the act of reading, confessing, consulting, recognizing, or interpreting does the work.
  - Use warrant_attribution when the issue is whether one source, sign, or medium has standing.
  - Use context_inference when the local cue is stable but needs an external bridge.
- **Positive indicators**:
  - A cue type is named but its procedural role remains unsettled after other checks.
  - Different cue-family readings would change the primary interpretation.
- **Exclusion indicators**:
  - A named cue appears only as topic vocabulary.
  - The cue is stable and the problem is authority, relation, operation, or context.
- **Confusable with**: `operation_function`, `warrant_attribution`
- **Mandatory counterfactual test**:
  - `CF_CUE_FUNCTION_PRIMARY`: If the same local content arrived through a different cue family, would the proposed interpretation change while speaker, operation, warrant, time, boundary, and context stayed stable?
  - `CF_PAIR_CUE_FUNCTION__OPERATION_FUNCTION`: Ask whether the problem is what this cue type does here, or what an act of interpretation, consultation, confession, recognition, or self-reading does.
- **Decision consequence**: Use only with care; if accepted, the record says the unresolved converter is cue-family function itself.
- **Escalation condition**: Escalate when cue_function is proposed but another specific locus remains plausible at equal or higher confidence.
- **Positive example**: Artificial example: a packet contains a sealed red mark whose genre is unspecified. The record cannot decide whether the mark functions as warning, authorization, or ritual token, and no speaker, operation, or warrant relation resolves it.
- **Near-miss example**: Artificial near miss: a judge reads a seal aloud and declares it valid. The visible act of reading and validating is operation_function or warrant_attribution, not cue_function.
- **Provenance note**: Definition inherits the active lineage table and protocol boundaries; operational rules are v0.1 synthesis from lineage, predicted-confusion tests, protocol schema, and legacy manual distinctions.

### `warrant_attribution`
- **Category ID**: `warrant_attribution`
- **One-sentence definition**: One source, medium, speaker, sign, or result is granted warranting force for the primary interpretation.
- **Analytic question**: Does the decision turn on whether one item is allowed to count as a warrant?
- **Use when**:
  - A single source, speaker, medium, sign, result, or textual item receives authority.
  - Removing that item’s standing would change the interpretation.
  - The problem is attribution of warranting force, not interaction among multiple warrants.
- **Do not use when**:
  - Do not use when multiple warrants must be ranked or reconciled; use warrant_relation.
  - Do not use when the visible operation itself converts evidence; use operation_function.
  - Do not use when standpoint controls the function; use perspective_assignment.
- **Use another value when**:
  - Use warrant_relation when the dominant instability is conflict or ranking among two or more warrants.
  - Use operation_function when a reading, confession, consultation, recognition, or self-reading performs the conversion.
  - Use perspective_assignment when changing the speaker or witness role changes the interpretation.
- **Positive indicators**:
  - One sign is treated as decisive evidence.
  - One speaker’s report is granted standing over available alternatives.
- **Exclusion indicators**:
  - Several sources interact and none singly carries the decision.
  - The source’s authority is already stable and the remaining question is how it is handled.
- **Confusable with**: `warrant_relation`, `operation_function`, `cue_function`
- **Mandatory counterfactual test**:
  - `CF_WARRANT_ATTRIBUTION_PRIMARY`: If this single source, speaker, medium, sign, or result lost warranting standing, would the proposed interpretation lose its support?
  - `CF_PAIR_CUE_FUNCTION__WARRANT_ATTRIBUTION`: Ask whether the cue type itself is underdetermined after excluding more specific loci, or whether one source, sign, medium, speaker, or result is granted standing.
- **Decision consequence**: The final record should cite the warrant-bearing item and explain why its standing matters.
- **Escalation condition**: Escalate when the record cannot decide whether one warrant has standing or multiple warrants are interacting.
- **Positive example**: Artificial example: a witness note is treated as reliable enough to identify the speaker’s intention, and the interpretation would collapse if the note were not granted standing.
- **Near-miss example**: Artificial near miss: two witness notes contradict each other and the record depends on ranking them. That is warrant_relation.
- **Provenance note**: Definition inherits the active lineage table and protocol boundaries; operational rules are v0.1 synthesis from lineage, predicted-confusion tests, protocol schema, and legacy manual distinctions.

### `warrant_relation`
- **Category ID**: `warrant_relation`
- **One-sentence definition**: Conflict, ranking, qualification, suspension, or interaction among multiple warrants is the dominant procedural locus.
- **Analytic question**: Does the interpretation depend on how two or more warrants interact?
- **Use when**:
  - Multiple warrants point in different or mutually qualifying directions.
  - The record ranks, reconciles, suspends, or combines warrants.
  - Removing the relation among warrants would change the interpretation.
- **Do not use when**:
  - Do not use merely because records disagree.
  - Do not use when one source alone is granted standing; use warrant_attribution.
  - Do not use when temporal reclassification is dominant; use temporal_layering.
- **Use another value when**:
  - Use warrant_attribution for one source receiving standing.
  - Use temporal_layering when later framing changes earlier evidence.
  - Use perspective_assignment when standpoint rather than cross-warrant relation determines the function.
- **Positive indicators**:
  - Two reports conflict and the record depends on which is prioritized.
  - A sign is qualified by a later statement within the same packet.
- **Exclusion indicators**:
  - Only one warrant is operative.
  - The relation is incidental and another locus performs conversion.
- **Confusable with**: `warrant_attribution`, `operation_function`, `temporal_layering`, `perspective_assignment`, `boundary_setting`, `context_inference`
- **Mandatory counterfactual test**:
  - `CF_WARRANT_RELATION_PRIMARY`: If the same warrants no longer conflicted, ranked, qualified, or interacted, would the primary interpretation change?
  - `CF_PAIR_WARRANT_ATTRIBUTION__WARRANT_RELATION`: Count the warrants: if the annotation depends on how more than one warrant interacts, use warrant_relation; if one source receives authority, use warrant_attribution.
- **Decision consequence**: The record should name the warrants and the relation among them.
- **Escalation condition**: Escalate when the record cannot decide whether warrant interaction or perspective, time, operation, or boundary is dominant.
- **Positive example**: Artificial example: one note promises release while a later order cancels it; the interpretation turns on the relation between promise and cancellation.
- **Near-miss example**: Artificial near miss: a single order is simply treated as authoritative. That is warrant_attribution.
- **Provenance note**: Definition inherits the active lineage table and protocol boundaries; operational rules are v0.1 synthesis from lineage, predicted-confusion tests, protocol schema, and legacy manual distinctions.

### `operation_function`
- **Category ID**: `operation_function`
- **One-sentence definition**: A visible interpretive, testimonial, consultative, recognitional, or self-reading operation converts evidence into the primary interpretation.
- **Analytic question**: Does an act performed in or by the record do the converting work?
- **Use when**:
  - The evidence becomes meaningful because someone interprets, recognizes, confesses, testifies, consults, translates, classifies, or self-reads.
  - The operation is visible in the packet and not merely inferred as background.
  - Changing or removing the operation would change the interpretation.
- **Do not use when**:
  - Do not use when the operation only grants standing to one warrant; consider warrant_attribution.
  - Do not use when a later time layer reclassifies earlier evidence; use temporal_layering.
  - Do not use for any action; the action must perform interpretive conversion.
- **Use another value when**:
  - Use warrant_attribution when authority assigned to a source is dominant.
  - Use warrant_relation when the operation primarily ranks or relates multiple warrants.
  - Use perspective_assignment when the speaker or standpoint controls the function.
- **Positive indicators**:
  - A character interprets a sign and that act supplies the function.
  - A confession changes how earlier evidence is read.
- **Exclusion indicators**:
  - The act is physical but not interpretive.
  - The operation is mentioned but not needed for the decision.
- **Confusable with**: `cue_function`, `warrant_attribution`, `warrant_relation`, `temporal_layering`, `perspective_assignment`
- **Mandatory counterfactual test**:
  - `CF_OPERATION_FUNCTION_PRIMARY`: If the visible operation were removed but the same evidence remained, would the proposed interpretation still follow?
  - `CF_PAIR_CUE_FUNCTION__OPERATION_FUNCTION`: Ask whether the problem is what this cue type does here, or what an act of interpretation, consultation, confession, recognition, or self-reading does.
- **Decision consequence**: The record should cite the operation and specify what conversion it performs.
- **Escalation condition**: Escalate when operation and warrant attribution or temporal layering are equally plausible.
- **Positive example**: Artificial example: a messenger deciphers a mark and the decision depends on that deciphering rather than on the mark alone.
- **Near-miss example**: Artificial near miss: the mark is accepted because it bears an official seal; that is warrant_attribution.
- **Provenance note**: Definition inherits the active lineage table and protocol boundaries; operational rules are v0.1 synthesis from lineage, predicted-confusion tests, protocol schema, and legacy manual distinctions.

### `boundary_setting`
- **Category ID**: `boundary_setting`
- **One-sentence definition**: Instability over the relevant case, interpretive unit, category boundary, speaker boundary, or scope of application is dominant.
- **Analytic question**: Would changing the boundary of the unit or category change the interpretation?
- **Use when**:
  - The record depends on where the case begins or ends.
  - A speaker, category, episode, or scope boundary is unstable.
  - Different reasonable boundaries would produce different interpretations.
- **Do not use when**:
  - Do not use when the unit is stable and the issue is a missing contextual bridge; use context_inference.
  - Do not use for any segmentation note that does not affect the decision.
  - Do not use when warrants within a stable boundary interact; use warrant_relation.
- **Use another value when**:
  - Use context_inference when the unit is stable but external context is needed.
  - Use warrant_relation when the boundary is stable and warrants interact.
  - Use perspective_assignment when a speaker or focalizer boundary specifically controls standpoint.
- **Positive indicators**:
  - The interpretation changes depending on whether a quoted sentence belongs to one speaker or another.
  - The relevant episode boundary is uncertain and affects the label.
- **Exclusion indicators**:
  - The packet boundary is merely administrative.
  - The boundary question is resolved before coding and no longer affects the decision.
- **Confusable with**: `warrant_relation`, `context_inference`
- **Mandatory counterfactual test**:
  - `CF_BOUNDARY_SETTING_PRIMARY`: If the interpretive unit, category scope, or speaker boundary were fixed differently, would the proposed interpretation change?
  - `CF_PAIR_BOUNDARY_SETTING__WARRANT_RELATION`: Ask whether changing the boundary of the annotation would change the result; if the boundary is stable but warrants interact, use warrant_relation.
- **Decision consequence**: The record should identify the unstable boundary and explain the chosen scope.
- **Escalation condition**: Escalate when the boundary cannot be fixed without evidence outside the packet.
- **Positive example**: Artificial example: a two-line notice may belong either to the speaker’s statement or to a narrator’s aside, and the interpretation changes with that boundary.
- **Near-miss example**: Artificial near miss: a stable paragraph needs historical background to interpret a term. That is context_inference.
- **Provenance note**: Definition inherits the active lineage table and protocol boundaries; operational rules are v0.1 synthesis from lineage, predicted-confusion tests, protocol schema, and legacy manual distinctions.

### `temporal_layering`
- **Category ID**: `temporal_layering`
- **One-sentence definition**: Later fulfilment, retrospective framing, historical readability, or reuse across time changes the function of earlier evidence.
- **Analytic question**: Does a later or retrospective layer reclassify what earlier evidence does?
- **Use when**:
  - A later event changes how earlier evidence functions.
  - The record depends on retrospective framing or later readability.
  - The same evidence has one local role and another later role.
- **Do not use when**:
  - Do not use merely because events happen in sequence.
  - Do not use when a local recognition act performs the conversion; use operation_function.
  - Do not use when multiple warrants conflict without time-layered reclassification; use warrant_relation.
- **Use another value when**:
  - Use operation_function when a visible local act converts evidence.
  - Use warrant_relation when conflict among warrants is dominant.
  - Use context_inference when historical background is external rather than a textual time layer.
- **Positive indicators**:
  - An early promise becomes evidence of irony only after a later reversal.
  - A later fulfilment recasts an earlier sign.
- **Exclusion indicators**:
  - Chronology is present but not interpretively active.
  - A later fact is just another warrant in a conflict.
- **Confusable with**: `warrant_relation`, `operation_function`, `context_inference`
- **Mandatory counterfactual test**:
  - `CF_TEMPORAL_LAYERING_PRIMARY`: If the later or retrospective layer were removed, would the earlier evidence keep the same function?
  - `CF_PAIR_WARRANT_RELATION__TEMPORAL_LAYERING`: If removing cross-warrant conflict removes the function, prefer warrant_relation; if removing the later temporal frame removes it, prefer temporal_layering.
- **Decision consequence**: The record should name the earlier evidence and the later layer that reclassifies it.
- **Escalation condition**: Escalate when the record cannot decide whether time layering or local operation is dominant.
- **Positive example**: Artificial example: a harmless greeting becomes evidence of threat only after a later reply reveals prior knowledge.
- **Near-miss example**: Artificial near miss: two simultaneous statements conflict. That is warrant_relation.
- **Provenance note**: Definition inherits the active lineage table and protocol boundaries; operational rules are v0.1 synthesis from lineage, predicted-confusion tests, protocol schema, and legacy manual distinctions.

### `perspective_assignment`
- **Category ID**: `perspective_assignment`
- **One-sentence definition**: Whose perspective, witness role, testimonial position, focalization, or narrative standpoint determines the function.
- **Analytic question**: Would changing the speaker, witness position, or standpoint change the interpretation?
- **Use when**:
  - The function depends on who sees, speaks, reports, remembers, or frames the evidence.
  - A witness role or focalizer controls the force of the record.
  - Changing standpoint would change the primary interpretation.
- **Do not use when**:
  - Do not use merely because a speaker is present.
  - Do not use when multiple accounts interact as warrants; use warrant_relation.
  - Do not use when a confession or testimony matters as an operation; use operation_function.
- **Use another value when**:
  - Use warrant_relation when the issue is conflict among several accounts.
  - Use operation_function when the act of confessing, testifying, or recognizing performs conversion.
  - Use warrant_attribution when one speaker is simply granted authority.
- **Positive indicators**:
  - The same statement functions differently because it is internal focalization rather than public report.
  - A witness role changes whether evidence counts as observation or rumor.
- **Exclusion indicators**:
  - Speaker identity is stable and not interpretively consequential.
  - The perspective is only one warrant among multiple ranked warrants.
- **Confusable with**: `warrant_relation`, `operation_function`, `warrant_attribution`
- **Mandatory counterfactual test**:
  - `CF_PERSPECTIVE_ASSIGNMENT_PRIMARY`: If the same words or observations came from a different standpoint or witness role, would the proposed interpretation change?
  - `CF_PAIR_WARRANT_RELATION__PERSPECTIVE_ASSIGNMENT`: Ask whether incompatibility among multiple warrants determines the function, or whether changing the speaker/testimonial position would change the annotation.
- **Decision consequence**: The record should identify the controlling standpoint and its effect.
- **Escalation condition**: Escalate when perspective control and warrant relation remain inseparable.
- **Positive example**: Artificial example: a line appears certain when read as narrator report but doubtful when read as a frightened witness’s memory.
- **Near-miss example**: Artificial near miss: two witnesses disagree and the record ranks their accounts. That is warrant_relation.
- **Provenance note**: Definition inherits the active lineage table and protocol boundaries; operational rules are v0.1 synthesis from lineage, predicted-confusion tests, protocol schema, and legacy manual distinctions.

### `context_inference`
- **Category ID**: `context_inference`
- **One-sentence definition**: A contextual bridge beyond the local anchor is the dominant obstacle to evidence-to-interpretation conversion.
- **Analytic question**: Is the local evidence stable but insufficient without a contextual bridge?
- **Use when**:
  - The packet evidence needs social, genre, institutional, historical, or discourse context to support the interpretation.
  - The local unit is stable but the needed bridge is not fully inside it.
  - More specific loci have been excluded.
- **Do not use when**:
  - Do not use as a residual bucket for difficulty.
  - Do not use when a time layer in the packet does the work; use temporal_layering.
  - Do not use when local warrants interact; use warrant_relation.
- **Use another value when**:
  - Use boundary_setting when the relevant unit or scope itself is unstable.
  - Use temporal_layering when later textual framing reclassifies earlier evidence.
  - Use warrant_relation when interacting local warrants carry the decision.
- **Positive indicators**:
  - A local phrase needs an institutional convention to explain its function.
  - A stable sentence requires genre context to justify the label.
- **Exclusion indicators**:
  - The context is available locally as a warrant relation.
  - The missing bridge is caused by unclear packet boundaries.
- **Confusable with**: `boundary_setting`, `temporal_layering`, `warrant_relation`
- **Mandatory counterfactual test**:
  - `CF_CONTEXT_INFERENCE_PRIMARY`: If the contextual bridge beyond the local anchor were unavailable, would the proposed interpretation no longer be licensed?
  - `CF_PAIR_BOUNDARY_SETTING__CONTEXT_INFERENCE`: Ask whether the relevant unit/scope is unstable, or whether the unit is stable but needs external contextual inference to support conversion.
- **Decision consequence**: The record should name the contextual bridge and mark uncertainty when it is not fully supplied by the packet.
- **Escalation condition**: Escalate when the required bridge is external to the packet and cannot be responsibly supplied.
- **Positive example**: Artificial example: a phrase can function as a legal release only if a recorded institutional convention is accepted as context.
- **Near-miss example**: Artificial near miss: the local passage contains two explicit rules that conflict. That is warrant_relation.
- **Provenance note**: Definition inherits the active lineage table and protocol boundaries; operational rules are v0.1 synthesis from lineage, predicted-confusion tests, protocol schema, and legacy manual distinctions.

## 7. Pairwise disambiguation
### `cue_function -> operation_function`
- **Why confusion is expected**: A cue type such as prophecy, testimony, or divination may be mistaken for the visible act performed with it.
- **Decisive question**: Which side of `cue_function -> operation_function` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: Ask whether the problem is what this cue type does here, or what an act of interpretation, consultation, confession, recognition, or self-reading does.
- **Directional error risk**: Reserved cue_function may be overused when operation_function is the more specific locus. Directionality: directional.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `cue_function -> warrant_attribution`
- **Why confusion is expected**: A cue family may be confused with the source or medium receiving warranting force.
- **Decisive question**: Which side of `cue_function -> warrant_attribution` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: Ask whether the cue type itself is underdetermined after excluding more specific loci, or whether one source, sign, medium, speaker, or result is granted standing.
- **Directional error risk**: Reserved cue_function may be overused when warrant_attribution is the more specific locus. Directionality: directional.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `warrant_attribution -> warrant_relation`
- **Why confusion is expected**: A single source granted authority may be confused with an interaction among multiple warrants.
- **Decisive question**: Which side of `warrant_attribution -> warrant_relation` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: Count the warrants: if the annotation depends on how more than one warrant interacts, use warrant_relation; if one source receives authority, use warrant_attribution.
- **Directional error risk**: One-warrant cases may be overcoded as warrant_relation when contextual complexity is present. Directionality: symmetric.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `warrant_attribution -> operation_function`
- **Why confusion is expected**: Authority is often assigned through an interpretive act, so granting standing may be confused with visible operation.
- **Decisive question**: Which side of `warrant_attribution -> operation_function` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: If evidence becomes usable as a warrant through the operation, prefer warrant_attribution; if evidence already has standing and the function depends on handling it, prefer operation_function.
- **Directional error risk**: Warrant attribution may be overcoded as operation_function when interpretation is visibly present. Directionality: symmetric.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `warrant_relation -> temporal_layering`
- **Why confusion is expected**: Cross-warrant conflict may coexist with retrospective framing or later readability.
- **Decisive question**: Which side of `warrant_relation -> temporal_layering` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: If removing cross-warrant conflict removes the function, prefer warrant_relation; if removing the later temporal frame removes it, prefer temporal_layering.
- **Directional error risk**: Warrant conflicts in retrospectively framed cases may be mistaken for temporal_layering, or temporal effects may be flattened into warrant_relation. Directionality: symmetric.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `warrant_relation -> perspective_assignment`
- **Why confusion is expected**: Incompatible testimony or standpoint can look like conflict among warrants or like perspective control.
- **Decisive question**: Which side of `warrant_relation -> perspective_assignment` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: Ask whether incompatibility among multiple warrants determines the function, or whether changing the speaker/testimonial position would change the annotation.
- **Directional error risk**: Perspective-governed testimony may be overcoded as warrant_relation when multiple accounts are visible. Directionality: symmetric.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `operation_function -> warrant_relation`
- **Why confusion is expected**: An operation can matter because it performs conversion or because it creates, exposes, ranks, or intensifies relations among warrants.
- **Decisive question**: Which side of `operation_function -> warrant_relation` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: If the operation itself performs the conversion, prefer operation_function; if it mainly relates multiple warrants, prefer warrant_relation.
- **Directional error risk**: Operations that rank warrants may be overcoded as operation_function when warrant_relation is dominant. Directionality: symmetric.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `operation_function -> temporal_layering`
- **Why confusion is expected**: Recognition or fulfilment can be treated as a local operation or as later reclassification of earlier evidence.
- **Decisive question**: Which side of `operation_function -> temporal_layering` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: If the local operation produces the function, prefer operation_function; if a later moment reclassifies earlier evidence, prefer temporal_layering.
- **Directional error risk**: Later reclassification may be overcoded as operation_function when a recognition scene is visible. Directionality: symmetric.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `boundary_setting -> warrant_relation`
- **Why confusion is expected**: A scope or unit boundary may be confused with the relation among warrants inside a stable unit.
- **Decisive question**: Which side of `boundary_setting -> warrant_relation` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: Ask whether changing the boundary of the annotation would change the result; if the boundary is stable but warrants interact, use warrant_relation.
- **Directional error risk**: Boundary_setting may be underused when coders move directly to warrant_relation inside an unstable unit. Directionality: directional.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `boundary_setting -> context_inference`
- **Why confusion is expected**: A missing boundary may be confused with a missing contextual bridge.
- **Decisive question**: Which side of `boundary_setting -> context_inference` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: Ask whether the relevant unit/scope is unstable, or whether the unit is stable but needs external contextual inference to support conversion.
- **Directional error risk**: Boundary problems may be absorbed into context_inference as a residual explanation. Directionality: directional.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `temporal_layering -> warrant_relation`
- **Why confusion is expected**: Later fulfilment, retrospective readability, or reuse may coexist with local warrant conflict.
- **Decisive question**: Which side of `temporal_layering -> warrant_relation` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: If removing the later temporal frame removes the function, prefer temporal_layering; if removing cross-warrant conflict removes it, prefer warrant_relation.
- **Directional error risk**: Temporal_layering may be undercoded when later readability appears alongside multiple warrants. Directionality: symmetric.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `temporal_layering -> operation_function`
- **Why confusion is expected**: A visible recognition or fulfilment scene can look like a local operation.
- **Decisive question**: Which side of `temporal_layering -> operation_function` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: If the function is produced by local operation, prefer operation_function; if a later moment reclassifies earlier evidence, prefer temporal_layering.
- **Directional error risk**: Temporal effects may be overcoded as operation_function when the text includes a visible recognition act. Directionality: symmetric.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `perspective_assignment -> warrant_relation`
- **Why confusion is expected**: Perspective, witness role, or testimonial position may be confused with incompatibility among multiple accounts as warrants.
- **Decisive question**: Which side of `perspective_assignment -> warrant_relation` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: Ask whether changing the speaker/testimonial position would change the annotation; if incompatibility among multiple warrants is dominant, use warrant_relation.
- **Directional error risk**: Perspective_assignment may be undercoded when multiple accounts make warrant conflict salient. Directionality: symmetric.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `perspective_assignment -> operation_function`
- **Why confusion is expected**: Confession or testimony can be treated as a visible operation or as standpoint-governed perspective.
- **Decisive question**: Which side of `perspective_assignment -> operation_function` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: Ask whether the function depends on the act of confessing/testifying or on whose perspective/testimonial role controls the annotation.
- **Directional error risk**: Perspective-governed testimony may be overcoded as operation_function when the speech act is prominent. Directionality: symmetric.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `context_inference -> temporal_layering`
- **Why confusion is expected**: Historical readability or later framing may be mistaken for external contextual inference.
- **Decisive question**: Which side of `context_inference -> temporal_layering` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: Ask whether later readability is the decisive feature; if yes, use temporal_layering rather than context_inference.
- **Directional error risk**: Context_inference may be overused when temporal_layering provides the more specific explanation. Directionality: directional.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

### `context_inference -> warrant_relation`
- **Why confusion is expected**: External or background context may be confused with interaction among warrants within the text.
- **Decisive question**: Which side of `context_inference -> warrant_relation` performs the evidence-to-interpretation conversion?
- **Counterfactual test**: Ask whether the local text contains interacting warrants; if yes, use warrant_relation. Use context_inference only when the missing contextual bridge is dominant.
- **Directional error risk**: Context_inference may be overused as a residual category for difficult warrant interactions. Directionality: directional.
- **Unresolved condition**: If the test supports both sides or neither side with adequate evidence, escalate or use `unresolved`.

## 8. Decision tree

### Human-readable numbered decision tree
1. `DT1`: Are selected evidence and focal interpretive decision recorded? If yes: `DT2`. If no: `ESCALATE_INSUFFICIENT_EVIDENCE`.
2. `DT2`: Is evidence-to-interpretation conversion sufficiently licensed? If yes: `DT3`. If no: `UNRESOLVED`.
3. `DT3`: Does an unstable unit, speaker boundary, category boundary, or scope boundary control the decision? If yes: `boundary_setting`. If no: `DT4`.
4. `DT4`: Does a later, retrospective, or reuse layer reclassify earlier evidence? If yes: `temporal_layering`. If no: `DT5`.
5. `DT5`: Does standpoint, focalization, witness role, or testimonial position control the function? If yes: `perspective_assignment`. If no: `DT6`.
6. `DT6`: Does a visible interpretive, testimonial, consultative, recognitional, or self-reading operation perform the conversion? If yes: `operation_function`. If no: `DT7`.
7. `DT7`: Does one source, medium, speaker, sign, or result receive warranting force? If yes: `DT7A`. If no: `DT8`.
8. `DT7A`: Do multiple warrants have to be ranked, reconciled, qualified, suspended, or related? If yes: `warrant_relation`. If no: `warrant_attribution`.
9. `DT8`: Do multiple local warrants interact as the dominant problem? If yes: `warrant_relation`. If no: `DT9`.
10. `DT9`: Is the cue family itself still the unresolved converter after more specific loci are excluded? If yes: `cue_function`. If no: `DT10`.
11. `DT10`: Is a contextual bridge beyond the local anchor required after more specific loci are excluded? If yes: `context_inference`. If no: `UNRESOLVED`.
12. `ESCALATE_INSUFFICIENT_EVIDENCE`: terminal `unresolved`; escalation_required = true.
13. `UNRESOLVED`: terminal `unresolved`; escalation_required = true.

### Machine-readable representation

See `docs/manuals/friction_locus_manual_v0_1.json`, field `decision_tree.nodes`.
## 9. Reserved/review-required policy

`cue_function`, `boundary_setting`, and `context_inference` are operationally review-sensitive because the active lineage table records them as reserved, awaiting positive out-of-sample testing, or vulnerable to residual use. A model may propose them, but if the manual or protocol marks the proposal as review-required, the operational status becomes `requires_human_review` and the final operational label remains `unresolved`. No model may autonomously approve a review-required category. Later review must create a separate record and never overwrite the original proposed record.
## 10. Counterfactual-test protocol

Counterfactual tests are mandatory when a category is proposed, when a predicted-confusion pair is relevant, when uncertainty is medium or high, or when an alternative pathway is retained. Each test records `test_id`, `question`, `answer`, `cited_evidence`, `effect_on_decision`, and `confidence`. Allowed answer states are `supports_category`, `supports_other_category`, `inconclusive`, and `not_applicable`, with pairwise tests also allowing `supports_left` and `supports_right`. If tests conflict, escalate or use `unresolved`; do not force a dominant locus.
## 11. Uncertainty and alternatives

Uncertainty level, alternative pathway, unresolved locus, and escalation are separate fields. A low-uncertainty record may still retain an alternative if the packet supports it. A high-uncertainty record may still choose a locus if evidence and counterfactual tests support a dominant procedural locus. `unresolved` means no responsible dominant locus is chosen. Escalation means review is required or a governance rule prevents final classification.
## 12. Worked examples

All examples in this section are artificial minimal examples. They are training/manual examples and are therefore ineligible for held-out testing.
### Example for `cue_function`
- **Evidence**: Artificial example: a packet contains a sealed red mark whose genre is unspecified. The record cannot decide whether the mark functions as warning, authorization, or ritual token, and no speaker, operation, or warrant relation resolves it.
- **Primary interpretation**: The example is coded as `cue_function`.
- **Alternative**: A near-miss value is considered and preserved in rationale.
- **Relevant tests**: `CF_CUE_FUNCTION_PRIMARY`.
- **Decision path**: evidence recorded; alternative retained; counterfactual test applied; dominant locus `cue_function` selected.
- **Friction locus**: `cue_function`.
- **Uncertainty**: medium for training purposes.
- **Escalation status**: not required unless the test is inconclusive.

### Example for `warrant_attribution`
- **Evidence**: Artificial example: a witness note is treated as reliable enough to identify the speaker’s intention, and the interpretation would collapse if the note were not granted standing.
- **Primary interpretation**: The example is coded as `warrant_attribution`.
- **Alternative**: A near-miss value is considered and preserved in rationale.
- **Relevant tests**: `CF_WARRANT_ATTRIBUTION_PRIMARY`.
- **Decision path**: evidence recorded; alternative retained; counterfactual test applied; dominant locus `warrant_attribution` selected.
- **Friction locus**: `warrant_attribution`.
- **Uncertainty**: medium for training purposes.
- **Escalation status**: not required unless the test is inconclusive.

### Example for `warrant_relation`
- **Evidence**: Artificial example: one note promises release while a later order cancels it; the interpretation turns on the relation between promise and cancellation.
- **Primary interpretation**: The example is coded as `warrant_relation`.
- **Alternative**: A near-miss value is considered and preserved in rationale.
- **Relevant tests**: `CF_WARRANT_RELATION_PRIMARY`.
- **Decision path**: evidence recorded; alternative retained; counterfactual test applied; dominant locus `warrant_relation` selected.
- **Friction locus**: `warrant_relation`.
- **Uncertainty**: medium for training purposes.
- **Escalation status**: not required unless the test is inconclusive.

### Example for `operation_function`
- **Evidence**: Artificial example: a messenger deciphers a mark and the decision depends on that deciphering rather than on the mark alone.
- **Primary interpretation**: The example is coded as `operation_function`.
- **Alternative**: A near-miss value is considered and preserved in rationale.
- **Relevant tests**: `CF_OPERATION_FUNCTION_PRIMARY`.
- **Decision path**: evidence recorded; alternative retained; counterfactual test applied; dominant locus `operation_function` selected.
- **Friction locus**: `operation_function`.
- **Uncertainty**: medium for training purposes.
- **Escalation status**: not required unless the test is inconclusive.

### Example for `boundary_setting`
- **Evidence**: Artificial example: a two-line notice may belong either to the speaker’s statement or to a narrator’s aside, and the interpretation changes with that boundary.
- **Primary interpretation**: The example is coded as `boundary_setting`.
- **Alternative**: A near-miss value is considered and preserved in rationale.
- **Relevant tests**: `CF_BOUNDARY_SETTING_PRIMARY`.
- **Decision path**: evidence recorded; alternative retained; counterfactual test applied; dominant locus `boundary_setting` selected.
- **Friction locus**: `boundary_setting`.
- **Uncertainty**: medium for training purposes.
- **Escalation status**: not required unless the test is inconclusive.

### Example for `temporal_layering`
- **Evidence**: Artificial example: a harmless greeting becomes evidence of threat only after a later reply reveals prior knowledge.
- **Primary interpretation**: The example is coded as `temporal_layering`.
- **Alternative**: A near-miss value is considered and preserved in rationale.
- **Relevant tests**: `CF_TEMPORAL_LAYERING_PRIMARY`.
- **Decision path**: evidence recorded; alternative retained; counterfactual test applied; dominant locus `temporal_layering` selected.
- **Friction locus**: `temporal_layering`.
- **Uncertainty**: medium for training purposes.
- **Escalation status**: not required unless the test is inconclusive.

### Example for `perspective_assignment`
- **Evidence**: Artificial example: a line appears certain when read as narrator report but doubtful when read as a frightened witness’s memory.
- **Primary interpretation**: The example is coded as `perspective_assignment`.
- **Alternative**: A near-miss value is considered and preserved in rationale.
- **Relevant tests**: `CF_PERSPECTIVE_ASSIGNMENT_PRIMARY`.
- **Decision path**: evidence recorded; alternative retained; counterfactual test applied; dominant locus `perspective_assignment` selected.
- **Friction locus**: `perspective_assignment`.
- **Uncertainty**: medium for training purposes.
- **Escalation status**: not required unless the test is inconclusive.

### Example for `context_inference`
- **Evidence**: Artificial example: a phrase can function as a legal release only if a recorded institutional convention is accepted as context.
- **Primary interpretation**: The example is coded as `context_inference`.
- **Alternative**: A near-miss value is considered and preserved in rationale.
- **Relevant tests**: `CF_CONTEXT_INFERENCE_PRIMARY`.
- **Decision path**: evidence recorded; alternative retained; counterfactual test applied; dominant locus `context_inference` selected.
- **Friction locus**: `context_inference`.
- **Uncertainty**: medium for training purposes.
- **Escalation status**: not required unless the test is inconclusive.

## 13. Non-examples and failure modes

- Choosing a locus from topic words alone.
- Treating disagreement as automatically a warrant relation.
- Using context_inference as a residual bucket.
- Confusing narrative time with temporal_layering.
- Confusing speaker presence with perspective_assignment.
- Confusing an interpretive act with warrant attribution.
- Forcing cue_function when another specific locus applies.
- Using final-label disagreement as the locus itself.

## 14. Versioning and freeze rule

Manual version: `friction_locus_manual_v0_1`. Effective date: 2026-07-02. Repository commit and SHA-256 hash are recorded in `docs/manuals/friction_locus_manual_manifest.json` after file creation. Later changes require a new version. Records coded under an older version are never silently migrated. Empirical coding must cite the exact manual commit and hash.
