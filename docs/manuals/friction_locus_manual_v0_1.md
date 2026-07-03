# Friction Locus Coding Manual v0.1

Status: `AUTHORITATIVE_FOR_PROTOCOL_REVIEW`

This manual is structurally complete and coherent for protocol review only. It is not empirically validated, not coder-reliability validated, not an ontology claim, and not authorization to begin coding.

## 1. Scope and Claim Boundary
Structurally complete and coherent for protocol review only; not empirically validated, not coder-reliability validated, not an ontology claim, and not authorization to begin coding.

## 2. Core Concepts
- `proposed_locus`: The substantive locus proposed by the original coder or model record.
- `candidate_loci`: The authoritative structured Stage A record: exactly one state for each of the eight substantive categories.
- `operational_status`: The status assigned after review-policy and dominance checks.
- `final_operational_label`: The label admitted for analysis before any later separate review event.
- `review_policy_applied`: The structured category-specific policy applied to the proposed locus.
- `escalation_required`: Whether the record requires human review or cannot be resolved under the manual.
- `review_of_record_id`: For adjudicator separate records, the original proposal record being reviewed.
- `review_of_record_hash`: For adjudicator separate records, the immutable hash of the original proposal record.
- `original_record_preserved`: Original proposal records are not overwritten by later review records.

## 3. Global Coding Sequence
1. identify focal interpretive decision
2. identify selected evidence
3. state proposed primary interpretation
4. retain plausible alternatives
5. evaluate candidate detection for all eight categories without early termination
6. apply relevant primary and pairwise counterfactual tests
7. resolve dominance without category-order priority
8. record proposed_locus, operational_status, final_operational_label, uncertainty, alternatives, and escalation separately

## 4. Evidence-Before-Locus Rule
Record evidence and rationale before assigning friction_locus. friction_locus is not a substitute for the primary label or interpretation.

## 5. One Dominant Locus Rule
- `primary_required`: exactly_one_substantive_proposed_locus_or_unresolved
- `secondary_loci`: candidate_loci and alternatives may be recorded in decision_path/counterfactual_tests; do not encode multiple final labels
- `tie_policy`: ties trigger unresolved plus escalation

## 6. Eight Category Sections
### `cue_function`
- **Definition**: Cue-family substitution changes the proposed interpretation while evidence content, speaker attachment, standpoint, operation, warrant standing, warrant relation, temporal position, boundary, and contextual bridge remain stable.
- **Analytic question**: Would substituting the cue family while holding the other procedural variables stable change the proposed interpretation?
- **Use when**:
  - At least two plausible cue-family functions can be specified.
  - Cue-family substitution changes the proposed interpretation.
  - Evidence content, speaker attachment, standpoint, operation, warrant standing, warrant relation, temporal position, boundary, and contextual bridge are held stable.
  - The cue family itself, not the mere presence of a cue word, explains the change.
- **Do not use when**:
  - Do not use because a cue word appears in the passage.
  - Do not use when the proposed support depends on elimination of all other categories rather than positive cue-family substitution evidence.
  - Do not use when the claimed change is actually produced by operation, warrant standing, warrant relation, perspective, temporal layer, boundary, or documented contextual bridge.
- **Use another value when**:
  - Use operation_function when a visible interpretive act performs the conversion.
  - Use warrant_attribution when standing is assigned to one source, medium, sign, speaker, or result.
  - Use context_inference when a documented contextual bridge, not cue-family substitution, supplies the conversion.
- **Positive indicators**:
  - Two or more cue-family functions are explicitly specified.
  - Substituting cue family changes the proposed interpretation while other procedural variables remain stable.
  - The rationale explains why the cue family itself changes the interpretation.
- **Exclusion indicators**:
  - The only support is that no other category was supported.
  - The rationale points to a cue word but does not specify cue-family substitution.
  - The manipulation changes operation, standing, perspective, time, boundary, or context along with cue family.
- **Candidate detection question**: Would substituting the cue family while holding the other procedural variables stable change the proposed interpretation?
- **Primary counterfactual**: If cue family were substituted while evidence content, speaker attachment, standpoint, operation, warrant standing, warrant relation, temporal position, boundary, and contextual bridge remained stable, would the proposed interpretation change?
- **Review policy**: status `reserved`, requires human review for model = `True`, final label before review = `unresolved`
- **Provenance note**: Revised by SYN_V0_1_CUE_POSITIVE_CRITERION from lineage-table residual wording into positive cue-family substitution criteria.

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
- **Primary counterfactual**: If this single source, speaker, medium, sign, or result lost warranting standing, would the proposed interpretation lose its support?
- **Review policy**: status `standard`, requires human review for model = `False`, final label before review = `null`
- **Provenance note**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

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
- **Primary counterfactual**: If the same warrants no longer conflicted, ranked, qualified, suspended, or interacted, would the primary interpretation change?
- **Review policy**: status `standard`, requires human review for model = `False`, final label before review = `null`
- **Provenance note**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

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
- **Primary counterfactual**: If the visible operation were removed but the same evidence remained, would the proposed interpretation still follow?
- **Review policy**: status `standard`, requires human review for model = `False`, final label before review = `null`
- **Provenance note**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

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
- **Primary counterfactual**: If the interpretive unit, category scope, or speaker attachment were fixed differently while standpoint stayed constant, would the proposed interpretation change?
- **Review policy**: status `review_sensitive`, requires human review for model = `True`, final label before review = `unresolved`
- **Provenance note**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

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
- **Primary counterfactual**: If the later or retrospective layer were removed, would the earlier evidence keep the same function?
- **Review policy**: status `standard`, requires human review for model = `False`, final label before review = `null`
- **Provenance note**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

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
- **Primary counterfactual**: If the same words or observations came from a different standpoint or witness role with attachment held stable, would the proposed interpretation change?
- **Review policy**: status `standard`, requires human review for model = `False`, final label before review = `null`
- **Provenance note**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

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
- **Primary counterfactual**: If the named contextual bridge were unavailable, would the proposed interpretation no longer be licensed by the local anchor?
- **Review policy**: status `review_sensitive`, requires human review for model = `True`, final label before review = `unresolved`
- **Provenance note**: Active lineage and predicted-confusion sources are inherited where possible; candidate-detection, dominance, and governance details are declared v0.1 synthesis.

## 7. Pairwise Disambiguation
### `cue_function -> operation_function`
- **why_confusion_expected**: A cue type such as prophecy, testimony, or divination may be mistaken for the visible act performed with it.
- **distinction**: Cue-family uncertainty concerns what kind of cue is operating; operation_function concerns a visible act performed with or on the cue.
- **question**: Hold the operation stable and substitute cue family; then hold cue family stable and alter the operation. Which manipulation changes the interpretation?
- **counterfactual_manipulation**: Ask whether the problem is what this cue type does here, or what an act of interpretation, consultation, confession, recognition, or self-reading does.
- **pattern**: cue_function remains plausible only when cue-family substitution changes interpretation with operation and other variables stable; operation_function is supported when altering the operation changes conversion while cue family remains stable.
- **directional_error_risk**: Reserved cue_function may be proposed without positive cue-family substitution evidence.
- **unresolved_condition**: Unresolved if cue family and operation cannot be varied separately.

### `cue_function -> warrant_attribution`
- **why_confusion_expected**: A cue family may be confused with the source or medium receiving warranting force.
- **distinction**: Cue function concerns cue-family role; warrant_attribution concerns one source, sign, speaker, medium, or result receiving standing.
- **question**: Hold warrant standing stable and substitute cue family; then hold cue family stable and change standing. Which manipulation changes the interpretation?
- **counterfactual_manipulation**: Hold warrant standing stable and substitute cue family; then hold cue family stable and change standing.
- **pattern**: cue_function remains plausible only when cue-family substitution changes interpretation with standing stable; warrant_attribution is supported when changing standing changes interpretation while cue family remains stable.
- **directional_error_risk**: Reserved cue_function may be proposed when the record actually turns on warranting standing.
- **unresolved_condition**: Unresolved if cue family and standing cannot be varied separately.

### `warrant_attribution -> warrant_relation`
- **why_confusion_expected**: A single source granted authority may be confused with an interaction among multiple warrants.
- **distinction**: One source receives standing versus two or more warrants interacting, ranking, qualifying, or conflicting.
- **question**: Count the operative warrants: would removing interaction among warrants change the interpretation?
- **counterfactual_manipulation**: Count the warrants: if the annotation depends on how more than one warrant interacts, use warrant_relation; if one source receives authority, use warrant_attribution.
- **pattern**: One decisive warrant supports warrant_attribution; interacting warrants support warrant_relation.
- **directional_error_risk**: One-warrant cases may be overcoded as warrant_relation when contextual complexity is present.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `warrant_attribution -> operation_function`
- **why_confusion_expected**: Authority is often assigned through an interpretive act, so granting standing may be confused with visible operation.
- **distinction**: Authority assigned to one source versus a visible operation performing conversion.
- **question**: Two-way test: remove warranting standing while preserving the operation; then remove the operation while granting standing in advance. Which removal blocks the specific interpretation?
- **counterfactual_manipulation**: Standing-removal and operation-removal are both required.
- **pattern**: If removing the operation leaves accepted evidence but no specific interpretation, operation_function is dominant; if removing standing makes the evidence unusable even with the operation, warrant_attribution is necessary but may be prerequisite rather than dominant.
- **directional_error_risk**: Warrant attribution may be overcoded as operation_function when interpretation is visibly present.
- **unresolved_condition**: Unresolved if the record cannot distinguish standing from the visible operation.

### `warrant_relation -> temporal_layering`
- **why_confusion_expected**: Cross-warrant conflict may coexist with retrospective framing or later readability.
- **distinction**: Local warrants interacting versus a later or retrospective layer reclassifying earlier evidence.
- **question**: Does removing cross-warrant interaction or removing the later temporal frame change the interpretation more directly?
- **counterfactual_manipulation**: If removing cross-warrant conflict removes the function, prefer warrant_relation; if removing the later temporal frame removes it, prefer temporal_layering.
- **pattern**: Interaction decisive supports warrant_relation; later/reuse frame decisive supports temporal_layering.
- **directional_error_risk**: Warrant conflicts in retrospectively framed cases may be mistaken for temporal_layering, or temporal effects may be flattened into warrant_relation.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `warrant_relation -> perspective_assignment`
- **why_confusion_expected**: Incompatible testimony or standpoint can look like conflict among warrants or like perspective control.
- **distinction**: Two or more accounts interact, conflict, rank, or qualify each other versus one standpoint’s position changing function.
- **question**: If standpoint is held constant, does warrant interaction still drive the decision; if warrant relation is held constant, does changing standpoint change function?
- **counterfactual_manipulation**: Ask whether incompatibility among multiple warrants determines the function, or whether changing the speaker/testimonial position would change the annotation.
- **pattern**: Account interaction supports warrant_relation; standpoint change supports perspective_assignment.
- **directional_error_risk**: Perspective-governed testimony may be overcoded as warrant_relation when multiple accounts are visible.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `operation_function -> warrant_relation`
- **why_confusion_expected**: An operation can matter because it performs conversion or because it creates, exposes, ranks, or intensifies relations among warrants.
- **distinction**: Operation performs conversion versus operation mainly creates or ranks relations among warrants.
- **question**: If the operation is removed but warrant relation remains, does the function persist; if the warrant relation is removed but operation remains, does the function persist?
- **counterfactual_manipulation**: If the operation itself performs the conversion, prefer operation_function; if it mainly relates multiple warrants, prefer warrant_relation.
- **pattern**: Operation decisive supports operation_function; relation decisive supports warrant_relation.
- **directional_error_risk**: Operations that rank warrants may be overcoded as operation_function when warrant_relation is dominant.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `operation_function -> temporal_layering`
- **why_confusion_expected**: Recognition or fulfilment can be treated as a local operation or as later reclassification of earlier evidence.
- **distinction**: Visible act converts evidence versus later time position or retrospective framing reclassifies evidence.
- **question**: If the later time position remains but the interpretive act is removed, does reclassification still occur; if the act remains but later framing is removed, does reclassification still occur?
- **counterfactual_manipulation**: If the local operation produces the function, prefer operation_function; if a later moment reclassifies earlier evidence, prefer temporal_layering.
- **pattern**: Act-removal decisive supports operation_function; later-frame removal decisive supports temporal_layering; both necessary without dominance means unresolved.
- **directional_error_risk**: Later reclassification may be overcoded as operation_function when a recognition scene is visible.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `boundary_setting -> warrant_relation`
- **why_confusion_expected**: A scope or unit boundary may be confused with the relation among warrants inside a stable unit.
- **distinction**: Changing unit, attachment, or scope changes result versus warrants interact inside a stable unit.
- **question**: Hold warrant content constant and alter unit/scope; then hold unit/scope constant and alter warrant relation. Which change controls?
- **counterfactual_manipulation**: Ask whether changing the boundary of the annotation would change the result; if the boundary is stable but warrants interact, use warrant_relation.
- **pattern**: Boundary change decisive supports boundary_setting; warrant interaction decisive supports warrant_relation.
- **directional_error_risk**: Boundary_setting may be underused when coders move directly to warrant_relation inside an unstable unit.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `boundary_setting -> context_inference`
- **why_confusion_expected**: A missing boundary may be confused with a missing contextual bridge.
- **distinction**: Changing the unit or scope changes the result versus unit is stable and a named contextual bridge is required.
- **question**: If unit/scope is fixed differently does result change; if unit is stable, can a named contextual bridge be cited as necessary?
- **counterfactual_manipulation**: Ask whether the relevant unit/scope is unstable, or whether the unit is stable but needs external contextual inference to support conversion.
- **pattern**: Unit/scope change supports boundary_setting; stable unit plus named bridge supports context_inference.
- **directional_error_risk**: Boundary problems may be absorbed into context_inference as a residual explanation.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `temporal_layering -> warrant_relation`
- **why_confusion_expected**: Later fulfilment, retrospective readability, or reuse may coexist with local warrant conflict.
- **distinction**: Later/reuse layer reclassifies earlier evidence versus local warrant interaction.
- **question**: Does removing the later layer or removing warrant interaction change the decision more directly?
- **counterfactual_manipulation**: If removing the later temporal frame removes the function, prefer temporal_layering; if removing cross-warrant conflict removes it, prefer warrant_relation.
- **pattern**: Later layer decisive supports temporal_layering; interaction decisive supports warrant_relation.
- **directional_error_risk**: Temporal_layering may be undercoded when later readability appears alongside multiple warrants.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `temporal_layering -> operation_function`
- **why_confusion_expected**: A visible recognition or fulfilment scene can look like a local operation.
- **distinction**: Temporal reclassification versus visible local operation.
- **question**: If the act remains but later framing is removed, and if later framing remains but the act is removed, which removal changes the decision?
- **counterfactual_manipulation**: If the function is produced by local operation, prefer operation_function; if a later moment reclassifies earlier evidence, prefer temporal_layering.
- **pattern**: Later-frame removal decisive supports temporal_layering; act removal decisive supports operation_function.
- **directional_error_risk**: Temporal effects may be overcoded as operation_function when the text includes a visible recognition act.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `perspective_assignment -> warrant_relation`
- **why_confusion_expected**: Perspective, witness role, or testimonial position may be confused with incompatibility among multiple accounts as warrants.
- **distinction**: One standpoint’s position changes function versus two or more accounts interact, conflict, rank, or qualify each other.
- **question**: Does changing standpoint alone change function, or does the relation among accounts do the work?
- **counterfactual_manipulation**: Ask whether changing the speaker/testimonial position would change the annotation; if incompatibility among multiple warrants is dominant, use warrant_relation.
- **pattern**: Standpoint decisive supports perspective_assignment; account interaction decisive supports warrant_relation.
- **directional_error_risk**: Perspective_assignment may be undercoded when multiple accounts make warrant conflict salient.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `perspective_assignment -> operation_function`
- **why_confusion_expected**: Confession or testimony can be treated as a visible operation or as standpoint-governed perspective.
- **distinction**: Standpoint controls interpretation versus a speech/reading/confession/testimony act performs conversion.
- **question**: If the act remains but standpoint changes, and if standpoint remains but act is removed, which manipulation controls?
- **counterfactual_manipulation**: Ask whether the function depends on the act of confessing/testifying or on whose perspective/testimonial role controls the annotation.
- **pattern**: Standpoint change supports perspective_assignment; act removal supports operation_function.
- **directional_error_risk**: Perspective-governed testimony may be overcoded as operation_function when the speech act is prominent.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `context_inference -> temporal_layering`
- **why_confusion_expected**: Historical readability or later framing may be mistaken for external contextual inference.
- **distinction**: External or non-local contextual bridge versus later/reuse layer in the text.
- **question**: Is the needed bridge documented as context outside the local anchor, or is reclassification produced by a later textual layer?
- **counterfactual_manipulation**: Ask whether later readability is the decisive feature; if yes, use temporal_layering rather than context_inference.
- **pattern**: Named external/non-local bridge supports context_inference; later textual layer supports temporal_layering.
- **directional_error_risk**: Context_inference may be overused when temporal_layering provides the more specific explanation.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `context_inference -> warrant_relation`
- **why_confusion_expected**: External or background context may be confused with interaction among warrants within the text.
- **distinction**: External or non-local bridge licenses conversion versus locally available warrants interact.
- **question**: Can locally available warrants explain conversion without the contextual bridge?
- **counterfactual_manipulation**: Ask whether the local text contains interacting warrants; if yes, use warrant_relation. Use context_inference only when the missing contextual bridge is dominant.
- **pattern**: If local interaction suffices, warrant_relation wins; if a named bridge is necessary and permitted, context_inference wins.
- **directional_error_risk**: Context_inference may be overused as a residual category for difficult warrant interactions.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `boundary_setting -> perspective_assignment`
- **why_confusion_expected**: Added in v0.1 repair because audit identified this distinction as operationally necessary.
- **distinction**: Uncertain attachment, scope, or unit boundary versus stable attachment with standpoint, focalization, witness role, or epistemic position changing interpretation.
- **question**: Hold standpoint constant and alter unit or speaker attachment; then hold attachment constant and alter standpoint. Which manipulation changes the result?
- **counterfactual_manipulation**: Hold standpoint constant and alter unit or speaker attachment; then hold attachment constant and alter standpoint. Which manipulation changes the result?
- **pattern**: Attachment/scope change supports boundary_setting; standpoint change with stable attachment supports perspective_assignment.
- **directional_error_risk**: Unresolved or wrong-locus risk if attachment, standpoint, and authority are not separated.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

### `perspective_assignment -> warrant_attribution`
- **why_confusion_expected**: Added in v0.1 repair because audit identified this distinction as operationally necessary.
- **distinction**: Standpoint or witness position controls interpretation versus one speaker or source receives standing or authority.
- **question**: If the same source retains authority but standpoint changes, does interpretation change; if standpoint stays constant but authority is withdrawn, does support fail?
- **counterfactual_manipulation**: If the same source retains authority but standpoint changes, does interpretation change; if standpoint stays constant but authority is withdrawn, does support fail?
- **pattern**: Standpoint change supports perspective_assignment; authority withdrawal supports warrant_attribution.
- **directional_error_risk**: Unresolved or wrong-locus risk if attachment, standpoint, and authority are not separated.
- **unresolved_condition**: If observable manipulations support both sides, neither side, or require unavailable evidence, set final_operational_label to unresolved and set escalation_required true.

## 8. Decision Tree
Stage A evaluates all eight categories and stores the result in `candidate_loci`. Array order is not category priority. Stage B resolves dominance from the supported-candidate set, counterfactual tests, and review-policy application.

- `no_supported_candidate`: {'escalation_required': True, 'final_operational_label': 'unresolved', 'operational_status': 'unresolved', 'proposed_locus': 'unresolved', 'reason': 'No candidate locus received candidate_supported.'}
- `one_supported_candidate`: Apply that category primary counterfactual test. If supported, retain as proposed_locus and apply review policy. If inconclusive or contradictory, final_operational_label unresolved and escalation_required true.
- `two_supported_candidates`: Apply relevant pairwise disambiguation test and both removal/substitution counterfactuals where relevant. Choose dominant locus only when one side is better supported; otherwise unresolved with escalation.
- `more_than_two_supported_candidates`: Apply pairwise tests needed to compare plausible candidates. Do not use tournament ordering. If no stable dominant locus emerges, unresolved with escalation.
- `review_sensitive_or_reserved_proposal`: Apply category-specific review policy. Model proposals requiring review preserve proposed_locus but set operational_status requires_human_review, final_operational_label unresolved, escalation_required true.
- `conflicting_counterfactual_tests`: {'escalation_required': True, 'final_operational_label': 'unresolved', 'operational_status': 'unresolved'}

## 9. Reserved/Review-Required Policy
`cue_function` is reserved. `boundary_setting` and `context_inference` are review-sensitive. Model proposals of these categories require human review, unresolved final label before review, and escalation. Later review never overwrites the original proposed record.

## 10. Counterfactual-Test Protocol
- `allowed_answer_states`: ['candidate_supported', 'candidate_not_supported', 'insufficient_evidence', 'not_applicable', 'supports_left', 'supports_right', 'supports_both', 'supports_neither', 'inconclusive']
- `conflict_policy`: Conflicting tests produce final_operational_label unresolved and escalation_required true.
- `fields`: ['test_id', 'question', 'answer', 'cited_evidence', 'effect_on_decision', 'confidence']
- `mandatory_when`: ['category is candidate_supported', 'two or more categories are candidate_supported', 'review policy is triggered', 'uncertainty is medium or high', 'alternative pathway is retained']

## 11. Uncertainty and Alternatives
Uncertainty level, alternative pathway, unresolved locus, and escalation are distinct fields and must not be collapsed.

## 12. Worked Examples
### `WEX_RESOLVED_WARRANT_ATTRIBUTION` (resolved)
- **record_id**: WEX_RESOLVED_WARRANT_ATTRIBUTION_REC
- **record_hash**: b4a6501695499e7efe0788c248ce44a9bfca774ef5e38279219c491666ce0a74
- **actor_event_type**: human_proposal
- **analyst_role**: researcher_analyst
- **review_of_record_id**: null
- **review_of_record_hash**: null
- **focal_interpretive_decision**: Does the notice carry procedural standing?
- **proposed_primary_interpretation**: The notice functions because official standing is attributed to that source.
- **proposed_locus**: warrant_attribution
- **operational_status**: accepted_for_analysis
- **final_operational_label**: warrant_attribution
- **escalation_required**: False
- **escalation_reason**: none
- **review_policy_applied**: {'category': 'warrant_attribution', 'status': 'standard', 'trigger': ['warrant_attribution_proposal'], 'requires_human_review': False, 'final_label_before_review': null}
- **primary_counterfactual_test**: If source standing were removed while the words remained, would the interpretation still follow?
- **primary_test_answer**: supports_category: without standing, the notice no longer performs the function.
- **pairwise_counterfactual_test**: No second supported candidate required pairwise dominance testing.
- **pairwise_test_answer**: not_applicable
- **effect_on_decision**: Choose warrant_attribution.
- **decision_path**: ['candidate_loci recorded for all eight categories', 'only warrant_attribution candidate_supported', 'standard review policy permits accepted_for_analysis']
- **original_record_preserved**: True
- **provenance**: artificial minimal example; not PR #18 material
- **candidate_loci**:
  - `cue_function`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support cue_function.
  - `warrant_attribution`: `candidate_supported`; evidence=['EX_ATTR_01']; confidence=`medium`; rationale=Positive counterfactual support recorded for warrant_attribution.
  - `warrant_relation`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support warrant_relation.
  - `operation_function`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support operation_function.
  - `boundary_setting`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support boundary_setting.
  - `temporal_layering`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support temporal_layering.
  - `perspective_assignment`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support perspective_assignment.
  - `context_inference`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support context_inference.

### `WEX_PAIR_OPERATION_ATTRIBUTION` (pairwise)
- **record_id**: WEX_PAIR_OPERATION_ATTRIBUTION_REC
- **record_hash**: 84be5d7bef78ec4cc1381089d5a551f14c92825845b8ca62a08cdde94d556ff9
- **actor_event_type**: human_proposal
- **analyst_role**: researcher_analyst
- **review_of_record_id**: null
- **review_of_record_hash**: null
- **focal_interpretive_decision**: Does the symbol sequence function as the command OPEN?
- **proposed_primary_interpretation**: The sequence yields the command because a visible decoding operation is applied to an already admitted source.
- **proposed_locus**: operation_function
- **operational_status**: accepted_for_analysis
- **final_operational_label**: operation_function
- **escalation_required**: False
- **escalation_reason**: none
- **review_policy_applied**: {'category': 'operation_function', 'status': 'standard', 'trigger': ['operation_function_proposal'], 'requires_human_review': False, 'final_label_before_review': null}
- **primary_counterfactual_test**: If the decoding operation were removed while codebook standing remained accepted, would the specific command still be available?
- **primary_test_answer**: supports_category: the codebook remains valid evidence, but without decoding the command OPEN is unavailable.
- **pairwise_counterfactual_test**: Two-way test: remove source standing while preserving decoding; then remove decoding while granting standing in advance.
- **pairwise_test_answer**: standing-removal result: the source becomes unusable even if the operation is known. operation-removal result: the source remains accepted but the specific command is unavailable. Operation is dominant because standing is a prerequisite while decoding performs the actual evidence-to-interpretation conversion.
- **effect_on_decision**: Choose operation_function while recording warrant_attribution as supported but prerequisite.
- **decision_path**: ['candidate_loci recorded for all eight categories', 'operation_function and warrant_attribution candidate_supported', 'two-way pairwise counterfactual applied', 'operation performs conversion after standing is granted', 'standard review policy permits accepted_for_analysis']
- **original_record_preserved**: True
- **provenance**: artificial minimal example; not PR #18 material
- **candidate_loci**:
  - `cue_function`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support cue_function.
  - `warrant_attribution`: `candidate_supported`; evidence=['EX_PAIR_01']; confidence=`medium`; rationale=Positive counterfactual support recorded for warrant_attribution.
  - `warrant_relation`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support warrant_relation.
  - `operation_function`: `candidate_supported`; evidence=['EX_PAIR_01']; confidence=`medium`; rationale=Positive counterfactual support recorded for operation_function.
  - `boundary_setting`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support boundary_setting.
  - `temporal_layering`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support temporal_layering.
  - `perspective_assignment`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support perspective_assignment.
  - `context_inference`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support context_inference.

### `WEX_REVIEW_REQUIRED_CUE_FUNCTION_MODEL` (review_required)
- **record_id**: WEX_REVIEW_REQUIRED_CUE_FUNCTION_MODEL_REC
- **record_hash**: cd59bc7a41f9177f50aa754cdd298925f172103c8e9db11c246080de9543a036
- **actor_event_type**: model_proposal
- **analyst_role**: researcher_analyst
- **review_of_record_id**: null
- **review_of_record_hash**: null
- **focal_interpretive_decision**: Does cue family itself change how the warning functions?
- **proposed_primary_interpretation**: The warning changes function when its cue family is substituted under otherwise stable variables.
- **proposed_locus**: cue_function
- **operational_status**: requires_human_review
- **final_operational_label**: unresolved
- **escalation_required**: True
- **escalation_reason**: reserved category proposed by model
- **review_policy_applied**: {'category': 'cue_function', 'status': 'reserved', 'trigger': ['cue_function_proposal'], 'requires_human_review': True, 'final_label_before_review': 'unresolved'}
- **primary_counterfactual_test**: If cue family were substituted while evidence content, speaker attachment, standpoint, operation, warrant standing, warrant relation, temporal position, boundary, and contextual bridge remained stable, would the proposed interpretation change?
- **primary_test_answer**: supports_category: cue-family substitution changes the proposed interpretation while other variables are held stable.
- **pairwise_counterfactual_test**: Compare cue-family substitution against operation and warrant-standing manipulations.
- **pairwise_test_answer**: supports_cue_function but review policy applies because cue_function is reserved.
- **effect_on_decision**: Preserve proposed_locus cue_function but final label remains unresolved before separate review.
- **decision_path**: ['candidate_loci recorded for all eight categories', 'positive cue-family substitution evidence supports cue_function', 'reserved category proposed by model', 'requires_human_review; final unresolved before review']
- **original_record_preserved**: True
- **provenance**: artificial minimal example; not PR #18 material
- **candidate_loci**:
  - `cue_function`: `candidate_supported`; evidence=['EX_CUE_01']; confidence=`medium`; rationale=Positive counterfactual support recorded for cue_function.
  - `warrant_attribution`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support warrant_attribution.
  - `warrant_relation`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support warrant_relation.
  - `operation_function`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support operation_function.
  - `boundary_setting`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support boundary_setting.
  - `temporal_layering`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support temporal_layering.
  - `perspective_assignment`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support perspective_assignment.
  - `context_inference`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support context_inference.

### `WEX_UNRESOLVED_NO_CANDIDATE` (unresolved)
- **record_id**: WEX_UNRESOLVED_NO_CANDIDATE_REC
- **record_hash**: a2b93d094c1ec01932dfa10279e3a19c718452b4a74b1404b24ecc295e203c60
- **actor_event_type**: human_proposal
- **analyst_role**: researcher_analyst
- **review_of_record_id**: null
- **review_of_record_hash**: null
- **focal_interpretive_decision**: Can a dominant procedural locus be identified?
- **proposed_primary_interpretation**: No stable primary interpretation is available from the recorded evidence.
- **proposed_locus**: unresolved
- **operational_status**: unresolved
- **final_operational_label**: unresolved
- **escalation_required**: True
- **escalation_reason**: insufficient evidence for candidate detection
- **review_policy_applied**: {'category': None, 'status': 'not_applicable', 'trigger': ['unresolved_no_policy'], 'requires_human_review': False, 'final_label_before_review': null}
- **primary_counterfactual_test**: Is there enough recorded evidence and rationale to identify and compare plausible procedural loci?
- **primary_test_answer**: insufficient_evidence for all eight candidate entries.
- **pairwise_counterfactual_test**: No supported candidates are available for pairwise testing.
- **pairwise_test_answer**: not_applicable
- **effect_on_decision**: Final operational label remains unresolved and escalates for insufficient evidence.
- **decision_path**: ['candidate_loci recorded for all eight categories', 'no candidate_supported entries', 'ESCALATE_INSUFFICIENT_EVIDENCE', 'final unresolved']
- **original_record_preserved**: True
- **provenance**: artificial minimal example; not PR #18 material
- **candidate_loci**:
  - `cue_function`: `insufficient_evidence`; evidence=[]; confidence=`not_applicable`; rationale=Evidence is insufficient to evaluate cue_function.
  - `warrant_attribution`: `insufficient_evidence`; evidence=[]; confidence=`not_applicable`; rationale=Evidence is insufficient to evaluate warrant_attribution.
  - `warrant_relation`: `insufficient_evidence`; evidence=[]; confidence=`not_applicable`; rationale=Evidence is insufficient to evaluate warrant_relation.
  - `operation_function`: `insufficient_evidence`; evidence=[]; confidence=`not_applicable`; rationale=Evidence is insufficient to evaluate operation_function.
  - `boundary_setting`: `insufficient_evidence`; evidence=[]; confidence=`not_applicable`; rationale=Evidence is insufficient to evaluate boundary_setting.
  - `temporal_layering`: `insufficient_evidence`; evidence=[]; confidence=`not_applicable`; rationale=Evidence is insufficient to evaluate temporal_layering.
  - `perspective_assignment`: `insufficient_evidence`; evidence=[]; confidence=`not_applicable`; rationale=Evidence is insufficient to evaluate perspective_assignment.
  - `context_inference`: `insufficient_evidence`; evidence=[]; confidence=`not_applicable`; rationale=Evidence is insufficient to evaluate context_inference.

### `WEX_CONFLICTING_OPERATION_TEMPORAL` (conflicting_tests)
- **record_id**: WEX_CONFLICTING_OPERATION_TEMPORAL_REC
- **record_hash**: 77f33d715b6acc5e74e3cbd97b3fbfc7f5d9cca513bc12e5656ccd7d5a457d3a
- **actor_event_type**: human_proposal
- **analyst_role**: researcher_analyst
- **review_of_record_id**: null
- **review_of_record_hash**: null
- **focal_interpretive_decision**: Does the interpretation turn on the recognition act or the later temporal layer?
- **proposed_primary_interpretation**: Both the operation and the later layer appear to control the interpretation.
- **proposed_locus**: unresolved
- **operational_status**: unresolved
- **final_operational_label**: unresolved
- **escalation_required**: True
- **escalation_reason**: conflicting counterfactual tests
- **review_policy_applied**: {'category': None, 'status': 'not_applicable', 'trigger': ['unresolved_no_policy'], 'requires_human_review': False, 'final_label_before_review': null}
- **primary_counterfactual_test**: If the visible recognition operation were removed, would the interpretation still follow?
- **primary_test_answer**: supports_category, but temporal-layer test also supports a different category.
- **pairwise_counterfactual_test**: Separate operation removal from later-layer removal.
- **pairwise_test_answer**: inconclusive: the packet cannot vary act and later frame separately.
- **effect_on_decision**: Conflicting tests require unresolved final label and escalation.
- **decision_path**: ['candidate_loci recorded for all eight categories', 'operation_function and temporal_layering candidate_supported', 'pairwise test cannot separate act from later frame', 'conflicting tests terminal', 'final unresolved with escalation']
- **original_record_preserved**: True
- **provenance**: artificial minimal example; not PR #18 material
- **candidate_loci**:
  - `cue_function`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support cue_function.
  - `warrant_attribution`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support warrant_attribution.
  - `warrant_relation`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support warrant_relation.
  - `operation_function`: `candidate_supported`; evidence=['EX_CONFLICT_01']; confidence=`medium`; rationale=Positive counterfactual support recorded for operation_function.
  - `boundary_setting`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support boundary_setting.
  - `temporal_layering`: `candidate_supported`; evidence=['EX_CONFLICT_01']; confidence=`medium`; rationale=Positive counterfactual support recorded for temporal_layering.
  - `perspective_assignment`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support perspective_assignment.
  - `context_inference`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support context_inference.

### `WEX_REVIEW_RECORD_FOR_CUE_FUNCTION` (linked_review_record)
- **record_id**: WEX_REVIEW_RECORD_FOR_CUE_FUNCTION_REC
- **record_hash**: 0bef883e9f280f6c782700d9059af55357baa09553185dd407cabeee5acb2bb7
- **actor_event_type**: adjudicator_review
- **analyst_role**: adjudicator_separate_record
- **review_of_record_id**: WEX_REVIEW_REQUIRED_CUE_FUNCTION_MODEL_REC
- **review_of_record_hash**: sha256:cd59bc7a41f9177f50aa754cdd298925f172103c8e9db11c246080de9543a036
- **focal_interpretive_decision**: Separate review of the reserved cue_function proposal.
- **proposed_primary_interpretation**: The original model proposal is reviewed without overwriting it.
- **proposed_locus**: cue_function
- **operational_status**: requires_human_review
- **final_operational_label**: unresolved
- **escalation_required**: True
- **escalation_reason**: reserved category review retained unresolved
- **review_policy_applied**: {'category': 'cue_function', 'status': 'reserved', 'trigger': ['cue_function_proposal'], 'requires_human_review': True, 'final_label_before_review': 'unresolved'}
- **primary_counterfactual_test**: If cue family were substituted while evidence content, speaker attachment, standpoint, operation, warrant standing, warrant relation, temporal position, boundary, and contextual bridge remained stable, would the proposed interpretation change?
- **primary_test_answer**: review_outcome: retained unresolved pending additional protocol decision.
- **pairwise_counterfactual_test**: Review record cites original candidate and pairwise tests rather than mutating them.
- **pairwise_test_answer**: Original proposed_locus remains cue_function in the preserved proposal record.
- **effect_on_decision**: Review record preserves original proposal and records separate final review outcome.
- **decision_path**: ['linked to original proposal record_id and record_hash', 'original proposed_locus preserved', 'separate review event records final decision', 'original record not overwritten']
- **original_record_preserved**: True
- **provenance**: artificial minimal example; not PR #18 material
- **candidate_loci**:
  - `cue_function`: `candidate_supported`; evidence=['EX_CUE_01']; confidence=`medium`; rationale=Positive counterfactual support recorded for cue_function.
  - `warrant_attribution`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support warrant_attribution.
  - `warrant_relation`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support warrant_relation.
  - `operation_function`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support operation_function.
  - `boundary_setting`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support boundary_setting.
  - `temporal_layering`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support temporal_layering.
  - `perspective_assignment`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support perspective_assignment.
  - `context_inference`: `candidate_not_supported`; evidence=[]; confidence=`medium`; rationale=Counterfactual test did not support context_inference.

## 13. Non-Examples and Failure Modes
- choosing a locus from topic words alone
- treating disagreement as automatically a warrant relation
- using context_inference as a residual bucket
- confusing narrative time with temporal_layering
- confusing speaker presence with perspective_assignment
- confusing an interpretive act with warrant attribution
- using cue_function because no other category was supported
- using final-label disagreement as the locus itself

## 14. Versioning and Freeze Rule
Manual version: `friction_locus_manual_v0_1`. Status: `AUTHORITATIVE_FOR_PROTOCOL_REVIEW`. Hashes are recorded in `docs/manuals/friction_locus_manual_manifest.json`. Later changes require a new version or documented revision. Records coded under an older version are never silently migrated.
