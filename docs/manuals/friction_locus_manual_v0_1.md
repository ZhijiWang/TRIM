# Friction Locus Coding Manual v0.1

Manual version: `friction_locus_manual_v0_1`  
Status: `DRAFT_INCOMPLETE`
Effective date: 2026-07-02

## 1. Scope and claim boundary

This draft is a provisional audit vocabulary for small-N, interpretation-intensive annotation. It is designed to make evidence selection, counterfactual tests, uncertainty, alternative pathways, and procedural disagreement reviewable. It is not an exhaustive ontology of interpretation, not a natural-category claim, and not empirical validation. Agreement under this manual would demonstrate procedural comparability under stated conditions, not ontological truth. The manual does not make one coder a gold standard. The categories identify the dominant procedural locus of unresolved interpretive friction: the point at which conversion from selected evidence to interpretation becomes unstable.

## 2. Core concepts

- **evidence**: Text selected as support and cited by stable evidence ID.
- **function/label**: The primary interpretive claim or label being audited.
- **warrant**: A source, sign, speaker, medium, result, or relation licensing movement from evidence to interpretation.
- **operation**: A visible interpretive, testimonial, consultative, recognitional, classificatory, or self-reading act.
- **relation**: Conflict, ranking, qualification, interaction, or suspension among warrants.
- **perspective**: Speaker, witness role, focalization, testimonial position, or epistemic standpoint.
- **temporal layer**: Later, retrospective, reuse, fulfilment, or historical-readability layer affecting earlier evidence.
- **boundary**: Case, unit, category, speaker-attachment, episode, or scope boundary.
- **context**: A named bridge beyond the local anchor, with documented source and protocol permission.
- **dominant friction locus**: The best-supported procedural locus after candidate detection and dominance resolution.
- **unresolved**: A final state when no responsible dominant locus can be selected.
- **alternative pathway**: A plausible route preserved rather than silently discarded.
- **escalation**: A governance flag for review, insufficient evidence, conflict, or review-policy trigger.

## 3. Global coding sequence

1. identify focal interpretive decision.
2. identify selected evidence.
3. state proposed primary interpretation.
4. retain plausible alternatives.
5. evaluate candidate detection for all eight categories without early termination.
6. apply relevant primary and pairwise counterfactual tests.
7. resolve dominance without category-order priority.
8. record proposed_locus, operational_status, final_operational_label, uncertainty, alternatives, and escalation separately.

## 4. Evidence-before-locus rule

Coders must record selected evidence and rationale before assigning `friction_locus`. The question is: is there enough recorded evidence and rationale to identify and compare plausible procedural loci? This is separate from whether the primary interpretation is fully justified. A fully licensed interpretation can still have a friction locus; an underlicensed interpretation may still reveal where friction would occur.

## 5. One dominant locus rule

Each record requires exactly one substantive `proposed_locus` or `unresolved`. Candidate loci may be recorded for comparison, but they are not arbitrary multi-label final outputs. If tests leave two or more loci tied, contradictory, or insufficiently supported, use `unresolved` for `final_operational_label` and set `escalation_required = true`.

## 6. Governance fields

- **proposed_locus**: The substantive locus proposed by the coder or model before governance review.
- **operational_status**: Status for analysis use: accepted_for_analysis, requires_human_review, unresolved, or not_supplied.
- **final_operational_label**: The label admitted for analysis after applying review policy. This may be unresolved even when proposed_locus is substantive.
- **escalation_required**: Boolean review flag.
- **review_policy**: Category-specific governance rule applied to proposed_locus.
- **original_record_preserved**: The original proposal remains unchanged; later review creates a separate review record.

Governance rules:
- Human proposal, model proposal, and post-review decision are distinct events.
- A model proposal never autonomously approves a review-required value.
- For model-proposed review-required categories preserve proposed_locus, set operational_status requires_human_review, set final_operational_label unresolved, set escalation_required true, and create any later review as a separate record.
- unresolved as final_operational_label is distinct from a substantive proposed_locus.

## 7. Category review policies

- `cue_function`: status `reserved`; human proposal allowed = `true`; model proposal allowed = `true`; model review required = `true`; final label before review = `unresolved`. Basis: Lineage table calls cue_function a provisional reserved value with no positive demo example.
- `warrant_attribution`: status `standard`; human proposal allowed = `true`; model proposal allowed = `true`; model review required = `false`; final label before review = `None`. Basis: Lineage table says prior positive examples and relatively clear lineage.
- `warrant_relation`: status `standard`; human proposal allowed = `true`; model proposal allowed = `true`; model review required = `false`; final label before review = `None`. Basis: Lineage table says prior positive examples and defensible relation to argumentation theory.
- `operation_function`: status `standard`; human proposal allowed = `true`; model proposal allowed = `true`; model review required = `false`; final label before review = `None`. Basis: Lineage table says prior positive examples and teachable rule.
- `boundary_setting`: status `review_sensitive`; human proposal allowed = `true`; model proposal allowed = `true`; model review required = `true`; final label before review = `unresolved`. Basis: Lineage table calls boundary_setting an operational value awaiting positive out-of-sample testing.
- `temporal_layering`: status `standard`; human proposal allowed = `true`; model proposal allowed = `true`; model review required = `false`; final label before review = `None`. Basis: Lineage table says prior positive examples and clear lineage.
- `perspective_assignment`: status `standard`; human proposal allowed = `true`; model proposal allowed = `true`; model review required = `false`; final label before review = `None`. Basis: Lineage table says prior positive examples and defensible lineage.
- `context_inference`: status `review_sensitive`; human proposal allowed = `true`; model proposal allowed = `true`; model review required = `true`; final label before review = `unresolved`. Basis: Lineage table calls context_inference awaiting positive out-of-sample testing and vulnerable to residual use.

## 8. Eight category sections

### `cue_function`
- **Definition**: The cue family itself remains the dominant procedural locus after more specific loci have been tested and excluded.
- **Analytic question**: Is the unresolved conversion produced by what kind of cue this is rather than by who uses it, how it is used, how warrants relate, or what context is needed?
- **Use when**:
  - The cue type, such as omen, testimony, prophecy, sign, inscription, confession, or token, is itself unstable as a converter.
  - All more specific candidate loci have been evaluated and do not better explain the friction.
  - Changing the cue family while holding evidence content, standpoint, operation, warrant, time, boundary, and context stable would change the interpretation.
- **Do not use when**:
  - Do not use because a cue word appears in the passage.
  - Do not use when a visible interpretive act performs the conversion; use operation_function.
  - Do not use when one source, speaker, sign, or medium receives standing; use warrant_attribution.
- **Use another value when**:
  - Use operation_function when the act of reading, recognizing, consulting, confessing, testifying, or interpreting performs conversion.
  - Use warrant_attribution when the issue is whether one source, sign, speaker, medium, or result has standing.
  - Use context_inference when a named contextual bridge, not cue family, licenses the conversion.
- **Positive indicators**:
  - A cue family has more than one plausible procedural role.
  - A substitution of cue family changes the interpretation while other variables are held constant.
- **Exclusion indicators**:
  - A more specific locus remains supported.
  - The cue is only topic vocabulary.
- **Candidate detection question**: Does cue-family function itself remain a plausible source of procedural friction after more specific loci are evaluated?
- **Primary counterfactual**: `CF_CUE_FUNCTION_PRIMARY`: If the same local content arrived through a different cue family, with speaker, operation, warrant, time, boundary, and context held stable, would the proposed interpretation change?
- **Confusable with**: `operation_function`, `warrant_attribution`
- **Review policy**: `reserved`; model review required = `true`.
- **Escalation condition**: Escalate if primary or pairwise counterfactual tests are inconclusive, contradictory, unsupported by evidence, or trigger the category review policy.
- **Provenance**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

### `warrant_attribution`
- **Definition**: One source, medium, speaker, sign, or result is granted warranting force for the primary interpretation.
- **Analytic question**: Does the decision turn on whether one item is allowed to count as a warrant?
- **Use when**:
  - A single source, speaker, medium, sign, result, or textual item receives standing.
  - Removing that item’s standing would change the interpretation.
  - The dominant issue is attribution of warranting force rather than interaction among multiple warrants.
- **Do not use when**:
  - Do not use when multiple warrants must be ranked or reconciled; use warrant_relation.
  - Do not use when the visible operation itself converts evidence; use operation_function.
  - Do not use when standpoint controls the function; use perspective_assignment.
- **Use another value when**:
  - Use warrant_relation when two or more warrants interact.
  - Use operation_function when a visible interpretive or testimonial operation performs conversion.
  - Use perspective_assignment when witness position or focalization controls the interpretation.
- **Positive indicators**:
  - One speaker or sign is treated as decisive.
  - One medium or source is granted authority over alternatives.
- **Exclusion indicators**:
  - Several sources interact and none singly carries the decision.
  - The source’s standing is stable and another locus explains conversion.
- **Candidate detection question**: Does one source, speaker, medium, sign, or result plausibly receive warranting force?
- **Primary counterfactual**: `CF_WARRANT_ATTRIBUTION_PRIMARY`: If this single source, speaker, medium, sign, or result lost warranting standing, would the proposed interpretation lose its support?
- **Confusable with**: `warrant_relation`, `operation_function`, `cue_function`, `perspective_assignment`
- **Review policy**: `standard`; model review required = `false`.
- **Escalation condition**: Escalate if primary or pairwise counterfactual tests are inconclusive, contradictory, unsupported by evidence, or trigger the category review policy.
- **Provenance**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

### `warrant_relation`
- **Definition**: Conflict, ranking, qualification, suspension, or interaction among multiple warrants is the dominant procedural locus.
- **Analytic question**: Does the interpretation depend on how two or more warrants interact?
- **Use when**:
  - Multiple local warrants point in different or mutually qualifying directions.
  - The record ranks, reconciles, suspends, combines, or contrasts warrants.
  - Removing the relation among warrants would change the interpretation.
- **Do not use when**:
  - Do not use merely because records disagree.
  - Do not use when one source alone is granted standing; use warrant_attribution.
  - Do not use when later framing reclassifies earlier evidence; use temporal_layering.
- **Use another value when**:
  - Use warrant_attribution for one source receiving standing.
  - Use temporal_layering when later or retrospective framing changes earlier evidence.
  - Use perspective_assignment when standpoint, not cross-warrant relation, controls the function.
- **Positive indicators**:
  - Two accounts conflict and the record depends on their relation.
  - One warrant qualifies or suspends another.
- **Exclusion indicators**:
  - Only one warrant is operative.
  - The relation is incidental and another locus performs conversion.
- **Candidate detection question**: Do two or more local warrants plausibly interact, conflict, rank, qualify, or suspend each other?
- **Primary counterfactual**: `CF_WARRANT_RELATION_PRIMARY`: If the same warrants no longer conflicted, ranked, qualified, suspended, or interacted, would the primary interpretation change?
- **Confusable with**: `warrant_attribution`, `operation_function`, `temporal_layering`, `perspective_assignment`, `boundary_setting`, `context_inference`
- **Review policy**: `standard`; model review required = `false`.
- **Escalation condition**: Escalate if primary or pairwise counterfactual tests are inconclusive, contradictory, unsupported by evidence, or trigger the category review policy.
- **Provenance**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

### `operation_function`
- **Definition**: A visible interpretive, testimonial, consultative, recognitional, or self-reading operation converts evidence into the primary interpretation.
- **Analytic question**: Does an act performed in or by the record do the converting work?
- **Use when**:
  - Someone interprets, recognizes, confesses, testifies, consults, translates, classifies, or self-reads in a way that converts evidence.
  - The operation is visible in the source packet.
  - Removing the operation would change the interpretation.
- **Do not use when**:
  - Do not use for any action; the action must perform interpretive conversion.
  - Do not use when the operation only grants standing to one warrant; consider warrant_attribution.
  - Do not use when later framing does the reclassification; use temporal_layering.
- **Use another value when**:
  - Use warrant_attribution when authority assigned to one source is dominant.
  - Use warrant_relation when the operation primarily ranks or relates multiple warrants.
  - Use perspective_assignment when speaker position or standpoint controls the function.
- **Positive indicators**:
  - A character interprets a sign and that act supplies the function.
  - A confession or recognition changes how evidence is read.
- **Exclusion indicators**:
  - The act is physical but not interpretive.
  - The operation is mentioned but not needed for the decision.
- **Candidate detection question**: Does a visible interpretive, testimonial, consultative, recognitional, or self-reading operation plausibly perform conversion?
- **Primary counterfactual**: `CF_OPERATION_FUNCTION_PRIMARY`: If the visible operation were removed but the same evidence remained, would the proposed interpretation still follow?
- **Confusable with**: `cue_function`, `warrant_attribution`, `warrant_relation`, `temporal_layering`, `perspective_assignment`
- **Review policy**: `standard`; model review required = `false`.
- **Escalation condition**: Escalate if primary or pairwise counterfactual tests are inconclusive, contradictory, unsupported by evidence, or trigger the category review policy.
- **Provenance**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

### `boundary_setting`
- **Definition**: Instability over the relevant case, interpretive unit, category boundary, speaker attachment, or scope of application is dominant.
- **Analytic question**: Would changing the unit, attachment, or scope boundary change the interpretation?
- **Use when**:
  - The record depends on where the case begins or ends.
  - Speaker attachment, quotation attachment, category scope, or episode scope is unstable.
  - Different reasonable boundaries would produce different interpretations.
- **Do not use when**:
  - Do not use when the unit is stable and a contextual bridge is needed; use context_inference.
  - Do not use for administrative segmentation that does not affect the decision.
  - Do not use when standpoint is stable but perspective controls the function; use perspective_assignment.
- **Use another value when**:
  - Use perspective_assignment when attachment is stable but standpoint, focalization, or witness role changes interpretation.
  - Use context_inference when unit/scope is stable but a named contextual bridge is required.
  - Use warrant_relation when locally available warrants interact inside a stable boundary.
- **Positive indicators**:
  - Changing quotation attachment changes the interpretation.
  - Changing the case boundary changes which evidence counts.
- **Exclusion indicators**:
  - The boundary is fixed before coding and no longer affects the decision.
  - A stable boundary leaves a perspective or warrant issue as dominant.
- **Candidate detection question**: Does uncertain unit, scope, category, episode, or speaker attachment plausibly control the result?
- **Primary counterfactual**: `CF_BOUNDARY_SETTING_PRIMARY`: If the interpretive unit, category scope, or speaker attachment were fixed differently while standpoint stayed constant, would the proposed interpretation change?
- **Confusable with**: `warrant_relation`, `context_inference`, `perspective_assignment`
- **Review policy**: `review_sensitive`; model review required = `true`.
- **Escalation condition**: Escalate if primary or pairwise counterfactual tests are inconclusive, contradictory, unsupported by evidence, or trigger the category review policy.
- **Provenance**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

### `temporal_layering`
- **Definition**: Later fulfilment, retrospective framing, historical readability, or reuse across time changes the function of earlier evidence.
- **Analytic question**: Does a later or retrospective layer reclassify what earlier evidence does?
- **Use when**:
  - A later event changes how earlier evidence functions.
  - The record depends on retrospective framing or later readability.
  - The same evidence has one local role and another later role.
- **Do not use when**:
  - Do not use merely because events happen in sequence.
  - Do not use when a local recognition act performs conversion; use operation_function.
  - Do not use when multiple warrants conflict without time-layered reclassification; use warrant_relation.
- **Use another value when**:
  - Use operation_function when a visible local act converts evidence.
  - Use warrant_relation when conflict among warrants is dominant.
  - Use context_inference when historical background is external rather than a textual time layer.
- **Positive indicators**:
  - A later fulfilment recasts an earlier sign.
  - A retrospective frame changes earlier evidence from incidental to functional.
- **Exclusion indicators**:
  - Chronology is present but not interpretively active.
  - A later fact is simply another warrant in a conflict.
- **Candidate detection question**: Does a later, retrospective, reuse, fulfilment, or historical-readability layer plausibly reclassify earlier evidence?
- **Primary counterfactual**: `CF_TEMPORAL_LAYERING_PRIMARY`: If the later or retrospective layer were removed, would the earlier evidence keep the same function?
- **Confusable with**: `warrant_relation`, `operation_function`, `context_inference`
- **Review policy**: `standard`; model review required = `false`.
- **Escalation condition**: Escalate if primary or pairwise counterfactual tests are inconclusive, contradictory, unsupported by evidence, or trigger the category review policy.
- **Provenance**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

### `perspective_assignment`
- **Definition**: Whose perspective, witness role, testimonial position, focalization, or epistemic standpoint determines the function.
- **Analytic question**: Would changing the speaker, witness position, or standpoint change the interpretation?
- **Use when**:
  - The function depends on who sees, speaks, remembers, reports, or frames the evidence.
  - Attachment is stable, but standpoint or epistemic position changes interpretation.
  - Changing standpoint would change the primary interpretation.
- **Do not use when**:
  - Do not use merely because a speaker is present.
  - Do not use when attachment or unit boundary is unstable; use boundary_setting.
  - Do not use when multiple accounts interact as warrants; use warrant_relation.
- **Use another value when**:
  - Use boundary_setting for uncertain attachment, scope, or unit boundary.
  - Use warrant_attribution when one speaker or source receives standing or authority.
  - Use warrant_relation when two or more accounts interact, conflict, rank, or qualify each other.
- **Positive indicators**:
  - The same statement functions differently because it is internal focalization rather than public report.
  - A witness role changes whether evidence counts as observation or rumor.
- **Exclusion indicators**:
  - Speaker identity is stable and not consequential.
  - The perspective is only one warrant among multiple ranked warrants.
- **Candidate detection question**: Does stable attachment plus standpoint, focalization, witness role, or epistemic position plausibly control interpretation?
- **Primary counterfactual**: `CF_PERSPECTIVE_ASSIGNMENT_PRIMARY`: If the same words or observations came from a different standpoint or witness role with attachment held stable, would the proposed interpretation change?
- **Confusable with**: `warrant_relation`, `operation_function`, `warrant_attribution`, `boundary_setting`
- **Review policy**: `standard`; model review required = `false`.
- **Escalation condition**: Escalate if primary or pairwise counterfactual tests are inconclusive, contradictory, unsupported by evidence, or trigger the category review policy.
- **Provenance**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

### `context_inference`
- **Definition**: A named contextual bridge beyond the local anchor is the dominant positive support needed for evidence-to-interpretation conversion.
- **Analytic question**: Is the local evidence stable but insufficient without a cited contextual bridge permitted by the protocol?
- **Use when**:
  - A specific contextual bridge is named and cited.
  - The bridge type is social, genre, institutional, historical, discourse, or another declared type.
  - The record explains why local evidence is insufficient without the bridge and why the bridge is context rather than a new warrant.
- **Do not use when**:
  - Do not use solely because no other category fits.
  - Do not use without naming the contextual bridge and where it is documented.
  - Do not use when locally available warrants interact; use warrant_relation.
- **Use another value when**:
  - Use boundary_setting when the relevant unit or scope itself is unstable.
  - Use temporal_layering when later textual framing reclassifies earlier evidence.
  - Use warrant_relation when local warrants carry the decision through interaction.
- **Positive indicators**:
  - A genre convention is cited and needed to license conversion.
  - An institutional rule documented inside the packet or protocol-approved context bridges local evidence to interpretation.
- **Exclusion indicators**:
  - The bridge cannot be cited.
  - The bridge is actually a local warrant.
  - The bridge is outside the packet and the protocol does not permit its use.
- **Candidate detection question**: Is there positive evidence for a named contextual bridge that is necessary, cited, typed, and protocol-permitted?
- **Primary counterfactual**: `CF_CONTEXT_INFERENCE_PRIMARY`: If the named contextual bridge were unavailable, would the proposed interpretation no longer be licensed by the local anchor?
- **Confusable with**: `boundary_setting`, `temporal_layering`, `warrant_relation`
- **Context positive-evidence requirements**:
  - bridge_name
  - bridge_type
  - where_bridge_is_documented
  - why_local_evidence_is_insufficient_without_it
  - why_bridge_is_context_rather_than_new_warrant
  - inside_or_outside_packet
  - protocol_permission
  - confidence
  - Selection by elimination alone is not allowed.
- **Review policy**: `review_sensitive`; model review required = `true`.
- **Escalation condition**: Escalate if primary or pairwise counterfactual tests are inconclusive, contradictory, unsupported by evidence, or trigger the category review policy.
- **Provenance**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

## 9. Candidate detection and dominance resolution

Stage A evaluates all eight candidate checks and produces a candidate set. Candidate-check order has no priority and must not determine the outcome. Stage B resolves dominance from the candidate set: no candidate reaches unresolved with escalation; one candidate requires the primary counterfactual; two candidates require pairwise disambiguation; more than two candidates require only the pairwise tests needed to compare plausible candidates and must not force a tournament winner; conflicting tests reach unresolved with escalation; review-sensitive or reserved proposals apply category-specific review policy.

## 10. Pairwise disambiguation

### `cue_function -> operation_function`
- **Why confusion is expected**: A cue type such as prophecy, testimony, or divination may be mistaken for the visible act performed with it.
- **Exact observable distinction**: Cue-family uncertainty concerns what kind of cue is operating; operation_function concerns a visible act performed with or on the cue.
- **Decisive question**: Holding cue content constant, does removing the act of interpreting/consulting/recognizing remove the conversion?
- **Counterfactual manipulation**: Ask whether the problem is what this cue type does here, or what an act of interpretation, consultation, confession, recognition, or self-reading does.
- **Expected answer pattern**: If removing the act removes conversion, operation_function wins; if changing cue family while the act stays constant changes conversion, cue_function remains plausible.
- **Directional error risk**: Reserved cue_function may be overused when operation_function is the more specific locus.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `cue_function -> warrant_attribution`
- **Why confusion is expected**: A cue family may be confused with the source or medium receiving warranting force.
- **Exact observable distinction**: Cue function concerns cue-family role; warrant_attribution concerns one source, sign, speaker, medium, or result receiving standing.
- **Decisive question**: Holding cue family constant, does loss of warranting standing remove support?
- **Counterfactual manipulation**: Ask whether the cue type itself is underdetermined after excluding more specific loci, or whether one source, sign, medium, speaker, or result is granted standing.
- **Expected answer pattern**: If standing is decisive, warrant_attribution wins; if standing is stable and cue family remains unstable, cue_function remains plausible.
- **Directional error risk**: Reserved cue_function may be overused when warrant_attribution is the more specific locus.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `warrant_attribution -> warrant_relation`
- **Why confusion is expected**: A single source granted authority may be confused with an interaction among multiple warrants.
- **Exact observable distinction**: One source receives standing versus two or more warrants interacting, ranking, qualifying, or conflicting.
- **Decisive question**: Count the operative warrants: would removing interaction among warrants change the interpretation?
- **Counterfactual manipulation**: Count the warrants: if the annotation depends on how more than one warrant interacts, use warrant_relation; if one source receives authority, use warrant_attribution.
- **Expected answer pattern**: One decisive warrant supports warrant_attribution; interacting warrants support warrant_relation.
- **Directional error risk**: One-warrant cases may be overcoded as warrant_relation when contextual complexity is present.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `warrant_attribution -> operation_function`
- **Why confusion is expected**: Authority is often assigned through an interpretive act, so granting standing may be confused with visible operation.
- **Exact observable distinction**: Authority assigned to one source versus a visible operation performing conversion.
- **Decisive question**: Apply two manipulations: remove warranting standing while preserving the operation; then remove the operation while granting standing in advance.
- **Counterfactual manipulation**: If evidence becomes usable as a warrant through the operation, prefer warrant_attribution; if evidence already has standing and the function depends on handling it, prefer operation_function.
- **Expected answer pattern**: If standing removal is decisive, warrant_attribution wins; if operation removal is decisive, operation_function wins; if both are necessary and neither dominates, unresolved.
- **Directional error risk**: Warrant attribution may be overcoded as operation_function when interpretation is visibly present.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `warrant_relation -> temporal_layering`
- **Why confusion is expected**: Cross-warrant conflict may coexist with retrospective framing or later readability.
- **Exact observable distinction**: Local warrants interacting versus a later or retrospective layer reclassifying earlier evidence.
- **Decisive question**: Does removing cross-warrant interaction or removing the later temporal frame change the interpretation more directly?
- **Counterfactual manipulation**: If removing cross-warrant conflict removes the function, prefer warrant_relation; if removing the later temporal frame removes it, prefer temporal_layering.
- **Expected answer pattern**: Interaction decisive supports warrant_relation; later/reuse frame decisive supports temporal_layering.
- **Directional error risk**: Warrant conflicts in retrospectively framed cases may be mistaken for temporal_layering, or temporal effects may be flattened into warrant_relation.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `warrant_relation -> perspective_assignment`
- **Why confusion is expected**: Incompatible testimony or standpoint can look like conflict among warrants or like perspective control.
- **Exact observable distinction**: Two or more accounts interact, conflict, rank, or qualify each other versus one standpoint’s position changing function.
- **Decisive question**: If standpoint is held constant, does warrant interaction still drive the decision; if warrant relation is held constant, does changing standpoint change function?
- **Counterfactual manipulation**: Ask whether incompatibility among multiple warrants determines the function, or whether changing the speaker/testimonial position would change the annotation.
- **Expected answer pattern**: Account interaction supports warrant_relation; standpoint change supports perspective_assignment.
- **Directional error risk**: Perspective-governed testimony may be overcoded as warrant_relation when multiple accounts are visible.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `operation_function -> warrant_relation`
- **Why confusion is expected**: An operation can matter because it performs conversion or because it creates, exposes, ranks, or intensifies relations among warrants.
- **Exact observable distinction**: Operation performs conversion versus operation mainly creates or ranks relations among warrants.
- **Decisive question**: If the operation is removed but warrant relation remains, does the function persist; if the warrant relation is removed but operation remains, does the function persist?
- **Counterfactual manipulation**: If the operation itself performs the conversion, prefer operation_function; if it mainly relates multiple warrants, prefer warrant_relation.
- **Expected answer pattern**: Operation decisive supports operation_function; relation decisive supports warrant_relation.
- **Directional error risk**: Operations that rank warrants may be overcoded as operation_function when warrant_relation is dominant.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `operation_function -> temporal_layering`
- **Why confusion is expected**: Recognition or fulfilment can be treated as a local operation or as later reclassification of earlier evidence.
- **Exact observable distinction**: Visible act converts evidence versus later time position or retrospective framing reclassifies evidence.
- **Decisive question**: If the later time position remains but the interpretive act is removed, does reclassification still occur; if the act remains but later framing is removed, does reclassification still occur?
- **Counterfactual manipulation**: If the local operation produces the function, prefer operation_function; if a later moment reclassifies earlier evidence, prefer temporal_layering.
- **Expected answer pattern**: Act-removal decisive supports operation_function; later-frame removal decisive supports temporal_layering; both necessary without dominance means unresolved.
- **Directional error risk**: Later reclassification may be overcoded as operation_function when a recognition scene is visible.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `boundary_setting -> warrant_relation`
- **Why confusion is expected**: A scope or unit boundary may be confused with the relation among warrants inside a stable unit.
- **Exact observable distinction**: Changing unit, attachment, or scope changes result versus warrants interact inside a stable unit.
- **Decisive question**: Hold warrant content constant and alter unit/scope; then hold unit/scope constant and alter warrant relation. Which change controls?
- **Counterfactual manipulation**: Ask whether changing the boundary of the annotation would change the result; if the boundary is stable but warrants interact, use warrant_relation.
- **Expected answer pattern**: Boundary change decisive supports boundary_setting; warrant interaction decisive supports warrant_relation.
- **Directional error risk**: Boundary_setting may be underused when coders move directly to warrant_relation inside an unstable unit.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `boundary_setting -> context_inference`
- **Why confusion is expected**: A missing boundary may be confused with a missing contextual bridge.
- **Exact observable distinction**: Changing the unit or scope changes the result versus unit is stable and a named contextual bridge is required.
- **Decisive question**: If unit/scope is fixed differently does result change; if unit is stable, can a named contextual bridge be cited as necessary?
- **Counterfactual manipulation**: Ask whether the relevant unit/scope is unstable, or whether the unit is stable but needs external contextual inference to support conversion.
- **Expected answer pattern**: Unit/scope change supports boundary_setting; stable unit plus named bridge supports context_inference.
- **Directional error risk**: Boundary problems may be absorbed into context_inference as a residual explanation.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `temporal_layering -> warrant_relation`
- **Why confusion is expected**: Later fulfilment, retrospective readability, or reuse may coexist with local warrant conflict.
- **Exact observable distinction**: Later/reuse layer reclassifies earlier evidence versus local warrant interaction.
- **Decisive question**: Does removing the later layer or removing warrant interaction change the decision more directly?
- **Counterfactual manipulation**: If removing the later temporal frame removes the function, prefer temporal_layering; if removing cross-warrant conflict removes it, prefer warrant_relation.
- **Expected answer pattern**: Later layer decisive supports temporal_layering; interaction decisive supports warrant_relation.
- **Directional error risk**: Temporal_layering may be undercoded when later readability appears alongside multiple warrants.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `temporal_layering -> operation_function`
- **Why confusion is expected**: A visible recognition or fulfilment scene can look like a local operation.
- **Exact observable distinction**: Temporal reclassification versus visible local operation.
- **Decisive question**: If the act remains but later framing is removed, and if later framing remains but the act is removed, which removal changes the decision?
- **Counterfactual manipulation**: If the function is produced by local operation, prefer operation_function; if a later moment reclassifies earlier evidence, prefer temporal_layering.
- **Expected answer pattern**: Later-frame removal decisive supports temporal_layering; act removal decisive supports operation_function.
- **Directional error risk**: Temporal effects may be overcoded as operation_function when the text includes a visible recognition act.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `perspective_assignment -> warrant_relation`
- **Why confusion is expected**: Perspective, witness role, or testimonial position may be confused with incompatibility among multiple accounts as warrants.
- **Exact observable distinction**: One standpoint’s position changes function versus two or more accounts interact, conflict, rank, or qualify each other.
- **Decisive question**: Does changing standpoint alone change function, or does the relation among accounts do the work?
- **Counterfactual manipulation**: Ask whether changing the speaker/testimonial position would change the annotation; if incompatibility among multiple warrants is dominant, use warrant_relation.
- **Expected answer pattern**: Standpoint decisive supports perspective_assignment; account interaction decisive supports warrant_relation.
- **Directional error risk**: Perspective_assignment may be undercoded when multiple accounts make warrant conflict salient.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `perspective_assignment -> operation_function`
- **Why confusion is expected**: Confession or testimony can be treated as a visible operation or as standpoint-governed perspective.
- **Exact observable distinction**: Standpoint controls interpretation versus a speech/reading/confession/testimony act performs conversion.
- **Decisive question**: If the act remains but standpoint changes, and if standpoint remains but act is removed, which manipulation controls?
- **Counterfactual manipulation**: Ask whether the function depends on the act of confessing/testifying or on whose perspective/testimonial role controls the annotation.
- **Expected answer pattern**: Standpoint change supports perspective_assignment; act removal supports operation_function.
- **Directional error risk**: Perspective-governed testimony may be overcoded as operation_function when the speech act is prominent.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `context_inference -> temporal_layering`
- **Why confusion is expected**: Historical readability or later framing may be mistaken for external contextual inference.
- **Exact observable distinction**: External or non-local contextual bridge versus later/reuse layer in the text.
- **Decisive question**: Is the needed bridge documented as context outside the local anchor, or is reclassification produced by a later textual layer?
- **Counterfactual manipulation**: Ask whether later readability is the decisive feature; if yes, use temporal_layering rather than context_inference.
- **Expected answer pattern**: Named external/non-local bridge supports context_inference; later textual layer supports temporal_layering.
- **Directional error risk**: Context_inference may be overused when temporal_layering provides the more specific explanation.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `context_inference -> warrant_relation`
- **Why confusion is expected**: External or background context may be confused with interaction among warrants within the text.
- **Exact observable distinction**: External or non-local bridge licenses conversion versus locally available warrants interact.
- **Decisive question**: Can locally available warrants explain conversion without the contextual bridge?
- **Counterfactual manipulation**: Ask whether the local text contains interacting warrants; if yes, use warrant_relation. Use context_inference only when the missing contextual bridge is dominant.
- **Expected answer pattern**: If local interaction suffices, warrant_relation wins; if a named bridge is necessary and permitted, context_inference wins.
- **Directional error risk**: Context_inference may be overused as a residual category for difficult warrant interactions.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `boundary_setting -> perspective_assignment`
- **Why confusion is expected**: Added in v0.1 repair because audit identified this distinction as operationally necessary.
- **Exact observable distinction**: Uncertain attachment, scope, or unit boundary versus stable attachment with standpoint, focalization, witness role, or epistemic position changing interpretation.
- **Decisive question**: Hold standpoint constant and alter unit or speaker attachment; then hold attachment constant and alter standpoint. Which manipulation changes the result?
- **Counterfactual manipulation**: Hold standpoint constant and alter unit or speaker attachment; then hold attachment constant and alter standpoint. Which manipulation changes the result?
- **Expected answer pattern**: Attachment/scope change supports boundary_setting; standpoint change with stable attachment supports perspective_assignment.
- **Directional error risk**: Unresolved or wrong-locus risk if attachment, standpoint, and authority are not separated.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `perspective_assignment -> warrant_attribution`
- **Why confusion is expected**: Added in v0.1 repair because audit identified this distinction as operationally necessary.
- **Exact observable distinction**: Standpoint or witness position controls interpretation versus one speaker or source receives standing or authority.
- **Decisive question**: If the same source retains authority but standpoint changes, does interpretation change; if standpoint stays constant but authority is withdrawn, does support fail?
- **Counterfactual manipulation**: If the same source retains authority but standpoint changes, does interpretation change; if standpoint stays constant but authority is withdrawn, does support fail?
- **Expected answer pattern**: Standpoint change supports perspective_assignment; authority withdrawal supports warrant_attribution.
- **Directional error risk**: Unresolved or wrong-locus risk if attachment, standpoint, and authority are not separated.
- **Unresolved condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

## 11. Counterfactual-test protocol

Counterfactual tests are mandatory when a category is supported, when two or more categories are supported, when review policy is triggered, when uncertainty is medium or high, or when an alternative pathway is retained. Each test records `test_id`, `question`, `answer`, `cited_evidence`, `effect_on_decision`, and `confidence`. Conflicting tests produce `final_operational_label = unresolved` and `escalation_required = true`.

## 12. Uncertainty and alternatives

Uncertainty level, alternative pathway, unresolved locus, and escalation are distinct. A low-uncertainty record may retain an alternative. A high-uncertainty record may still propose a locus if tests support dominance. `unresolved` is a final-label state, not the same as a substantive proposed locus.

## 13. Worked examples

All examples are artificial minimal examples. They are training/manual examples and are ineligible for held-out testing.

### `WEX_RESOLVED_WARRANT_ATTRIBUTION` (resolved)
- **training_manual_status**: training_manual_example_ineligible_for_held_out_testing
- **actor_event_type**: human_proposal
- **focal_interpretive_decision**: Does the notice function as authorization?
- **proposed_primary_interpretation**: The notice functions as authorization.
- **candidate_loci**: ['warrant_attribution']
- **alternative_pathway**: It could be a mere informational notice if the signature had no standing.
- **primary_counterfactual_test**: If this single source, speaker, medium, sign, or result lost warranting standing, would the proposed interpretation lose its support?
- **primary_test_answer**: supports_category: without the clerk signature standing, authorization is unsupported.
- **cited_evidence**: ['EX_RES_01']
- **pairwise_counterfactual_test**: not_applicable: only one candidate supported.
- **pairwise_test_answer**: not_applicable
- **confidence**: high
- **effect_on_decision**: Retain warrant_attribution as dominant.
- **proposed_locus**: warrant_attribution
- **operational_status**: accepted_for_analysis
- **final_operational_label**: warrant_attribution
- **uncertainty**: low
- **escalation_required**: False
- **original_record_preserved**: True
- **decision_path**: ['candidate_detection:warrant_attribution supported', 'primary_counterfactual supports category', 'standard review policy permits accepted_for_analysis']
- **provenance**: artificial minimal example; not PR #18 material
- **selected_evidence**: [{'evidence_id': 'EX_RES_01', 'text': 'Artificial packet: A notice bears a named clerk signature, and the local rule says clerk signatures authorize entry.'}]
- **review_policy_applied**: {'status': 'standard', 'trigger': ['single source, medium, speaker, sign, or result receives warranting force'], 'human_proposal_allowed': True, 'model_proposal_allowed': True, 'requires_human_review_for_model': False, 'final_label_before_review': None, 'source_basis': 'Lineage table says prior positive examples and relatively clear lineage.'}

### `WEX_PAIR_OPERATION_ATTRIBUTION` (pairwise)
- **training_manual_status**: training_manual_example_ineligible_for_held_out_testing
- **actor_event_type**: human_proposal
- **focal_interpretive_decision**: Does the token function as an order?
- **proposed_primary_interpretation**: The token functions as an order because the clerk interprets it aloud.
- **candidate_loci**: ['operation_function', 'warrant_attribution']
- **alternative_pathway**: The clerk could be treated as an authority whose standing alone makes the token count.
- **primary_counterfactual_test**: If the visible operation were removed but the same evidence remained, would the proposed interpretation still follow?
- **primary_test_answer**: supports_category: without the reading act, the token does not become an order.
- **cited_evidence**: ['EX_PAIR_01']
- **pairwise_counterfactual_test**: Apply two manipulations: remove warranting standing while preserving the operation; then remove the operation while granting standing in advance.
- **pairwise_test_answer**: supports_operation_function: removing warranting standing while preserving the reading still leaves the act as conversion in the packet; removing the operation while granting standing in advance removes the observed conversion.
- **confidence**: medium
- **effect_on_decision**: Choose operation_function over warrant_attribution.
- **proposed_locus**: operation_function
- **operational_status**: accepted_for_analysis
- **final_operational_label**: operation_function
- **uncertainty**: medium
- **escalation_required**: False
- **original_record_preserved**: True
- **decision_path**: ['candidate_detection supports operation_function and warrant_attribution', 'two-candidate pairwise test applied', 'operation removal more decisive', 'standard review policy']
- **provenance**: artificial minimal example; not PR #18 material
- **selected_evidence**: [{'evidence_id': 'EX_PAIR_01', 'text': 'Artificial packet: A clerk reads an unsigned token aloud and declares its meaning under a rule already accepted by all parties.'}]
- **review_policy_applied**: {'status': 'standard', 'trigger': ['visible operation converts evidence to function'], 'human_proposal_allowed': True, 'model_proposal_allowed': True, 'requires_human_review_for_model': False, 'final_label_before_review': None, 'source_basis': 'Lineage table says prior positive examples and teachable rule.'}

### `WEX_REVIEW_REQUIRED_CUE_FUNCTION_MODEL` (review_required)
- **training_manual_status**: training_manual_example_ineligible_for_held_out_testing
- **actor_event_type**: model_proposal
- **focal_interpretive_decision**: Does the blue mark function as warning or authorization?
- **proposed_primary_interpretation**: The mark functions as a cue whose family is unresolved.
- **candidate_loci**: ['cue_function']
- **alternative_pathway**: The mark might be a sign with warranting standing if a rule of authority were present, but no such rule is cited.
- **primary_counterfactual_test**: If the same local content arrived through a different cue family, with speaker, operation, warrant, time, boundary, and context held stable, would the proposed interpretation change?
- **primary_test_answer**: supports_category but review policy applies: changing cue family would change interpretation, yet cue_function is reserved.
- **cited_evidence**: ['EX_REV_01']
- **pairwise_counterfactual_test**: not_applicable: no more specific candidate supported.
- **pairwise_test_answer**: not_applicable
- **confidence**: medium
- **effect_on_decision**: Preserve proposed_locus cue_function but do not admit it as final without review.
- **proposed_locus**: cue_function
- **operational_status**: requires_human_review
- **final_operational_label**: unresolved
- **uncertainty**: medium
- **escalation_required**: True
- **original_record_preserved**: True
- **decision_path**: ['candidate_detection supports cue_function only', 'primary counterfactual supports cue_function', 'reserved category proposed by model', 'requires_human_review; final unresolved']
- **provenance**: artificial minimal example; not PR #18 material
- **selected_evidence**: [{'evidence_id': 'EX_REV_01', 'text': 'Artificial packet: An unexplained blue mark appears; no speaker, operation, warrant relation, time layer, boundary issue, perspective, or contextual bridge is supported.'}]
- **review_policy_applied**: {'status': 'reserved', 'trigger': ['cue family remains plausible after all more specific loci are tested', 'proposal is made by a model record', 'counterfactual tests do not support another specific locus'], 'human_proposal_allowed': True, 'model_proposal_allowed': True, 'requires_human_review_for_model': True, 'final_label_before_review': 'unresolved', 'source_basis': 'Lineage table calls cue_function a provisional reserved value with no positive demo example.'}

### `WEX_UNRESOLVED_NO_CANDIDATE` (unresolved)
- **training_manual_status**: training_manual_example_ineligible_for_held_out_testing
- **actor_event_type**: human_proposal
- **focal_interpretive_decision**: Cannot be identified from the record.
- **proposed_primary_interpretation**: No responsible primary interpretation is supplied.
- **candidate_loci**: ['none_supported']
- **alternative_pathway**: No complete alternative can be evaluated because evidence and rationale are insufficient.
- **primary_counterfactual_test**: Is there enough recorded evidence and rationale to identify and compare plausible procedural loci?
- **primary_test_answer**: insufficient_evidence
- **cited_evidence**: ['EX_UNR_01']
- **pairwise_counterfactual_test**: not_applicable: no candidate set.
- **pairwise_test_answer**: not_applicable
- **confidence**: low
- **effect_on_decision**: Use unresolved and escalate for insufficient evidence.
- **proposed_locus**: unresolved
- **operational_status**: unresolved
- **final_operational_label**: unresolved
- **uncertainty**: high
- **escalation_required**: True
- **original_record_preserved**: True
- **decision_path**: ['evidence sufficiency question failed', 'ESCALATE_INSUFFICIENT_EVIDENCE', 'final unresolved']
- **provenance**: artificial minimal example; not PR #18 material
- **selected_evidence**: [{'evidence_id': 'EX_UNR_01', 'text': 'Artificial packet: A sentence is fragmentary and the rationale gives no stable interpretive decision.'}]
- **review_policy_applied**: {'status': 'not_applicable'}

### `WEX_CONFLICTING_OPERATION_TEMPORAL` (conflicting_tests)
- **training_manual_status**: training_manual_example_ineligible_for_held_out_testing
- **actor_event_type**: human_proposal
- **focal_interpretive_decision**: Does the earlier phrase function as a promise?
- **proposed_primary_interpretation**: The earlier phrase may function as a promise.
- **candidate_loci**: ['operation_function', 'temporal_layering']
- **alternative_pathway**: The promise reading could be produced by the announcement as an operation or by the later temporal position as reclassification.
- **primary_counterfactual_test**: If the visible operation were removed but the same evidence remained, would the proposed interpretation still follow?
- **primary_test_answer**: supports_category: removing the announcement act weakens conversion.
- **cited_evidence**: ['EX_CON_01']
- **pairwise_counterfactual_test**: If the later time position remains but the interpretive act is removed, does reclassification still occur; if the act remains but later framing is removed, does reclassification still occur?
- **pairwise_test_answer**: conflicting: later framing and recognition act are not separable in the artificial packet.
- **confidence**: low
- **effect_on_decision**: Do not force a winner; use unresolved and escalate.
- **proposed_locus**: unresolved
- **operational_status**: unresolved
- **final_operational_label**: unresolved
- **uncertainty**: high
- **escalation_required**: True
- **original_record_preserved**: True
- **decision_path**: ['candidate_detection supports operation_function and temporal_layering', 'pairwise test cannot separate act from later frame', 'conflicting tests terminal', 'final unresolved with escalation']
- **provenance**: artificial minimal example; not PR #18 material
- **selected_evidence**: [{'evidence_id': 'EX_CON_01', 'text': 'Artificial packet: A reader later announces that an earlier phrase was a promise, and the announcement itself is also the only visible act of recognition.'}]
- **review_policy_applied**: {'status': 'not_applicable'}

## 14. Non-examples and failure modes

- Choosing a locus from topic words alone.
- Treating disagreement as automatically a warrant relation.
- Using context_inference as a residual bucket.
- Selecting context_inference solely because no other category fits.
- Confusing narrative time with temporal_layering.
- Confusing speaker presence with perspective_assignment.
- Confusing uncertain speaker attachment with perspective_assignment.
- Confusing an interpretive act with warrant attribution.
- Forcing cue_function when another specific locus applies.
- Using final-label disagreement as the locus itself.

## 15. Versioning and freeze rule

Manual version: `friction_locus_manual_v0_1`. Status: `DRAFT_INCOMPLETE`. Hashes are recorded in `docs/manuals/friction_locus_manual_manifest.json`. Later changes require recomputing affected hashes. Records coded under an older version are never silently migrated. No pre-merge file claims to contain a future merge commit.
