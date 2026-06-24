# TRIM Article Working Notes

## Status and purpose

This is the single authoritative paper-development note for the TRIM article. It consolidates the initial adversarial audit and subsequent Claude/Gemini revisions into one maintained document. It does not modify the TRIM schema, codebook, controlled vocabularies, pilot materials, or software. It records the current novelty audit, evidence status, ablation design, pilot decision rules, and demonstration-corpus strategy.

Do not revise the validation object before the independent pilot. The next schema decision must follow observed evidence.

## Current central claim under test

TRIM’s strongest candidate contribution is not source anchoring, graph export, rationale preservation, disagreement-aware annotation, or the discovery that the same label can rest on different reasons. Each of those has substantial prior precedent.

The claim currently under test is narrower:

> TRIM operationalizes the source-anchored, human-coded conversion from textual evidence to a project-defined interpretive function as a multidimensional, reviewable, and comparable annotation pathway.

The pathway records:

- where the conversion places its greatest interpretive demand (`friction_locus`);
- what the conversion does (`rationale_mechanism`);
- what support sustains it (`epistemic_support`);
- where it operates in discourse (`discourse_level`);
- how it is temporally oriented (`temporal_orientation`);
- how confidently it is maintained (`uncertainty_flag`);
- which viable competing pathway remains available (`alternative_signature`);
- and the prose rationale and source-facing evidence that make the record reviewable.

This claim remains provisional. It survives only if the pilot shows that the structured fields provide information that cannot be recovered adequately from a simpler source-span, function-label, and free-text-memo workflow without substantial secondary recoding.

## Claims already abandoned

The article must not claim that TRIM is:

- the first method to connect evidence, warrant, and interpretation;
- the first structured model of scholarly reasoning;
- the first method to preserve rationales;
- the first framework to reveal same-label/different-reason variation;
- the first disagreement-aware annotation method;
- the first graph representation of interpretation;
- the first source-anchored humanities annotation system;
- the first approach to cross-language annotation divergence;
- or a transparent record of the coder’s actual cognitive process.

TRIM records accountable scholarly commitments: the reasons a coder is prepared to state, defend, compare, and revise. It does not provide psychological ground truth.

# 1. Mandatory closest prior work

## 1.1 LiTEx and within-label explanation variation

LiTEx and related work already establish that:

- shared outcome labels can conceal different reasoning;
- similar or identical evidence spans may be selected for different reasons;
- free-text rationales can be converted into controlled categories;
- and rationale categories can be reliability-tested.

TRIM cannot claim novelty for any of those results.

Its candidate difference is not simply that it uses more fields. The paper must show that the fields form an interpretable conversion structure rather than a larger collection of independent rationale categories.

The pilot must therefore ask whether the joint signature reveals stable relations among locus, mechanism, support, discourse, temporality, uncertainty, and alternatives.

Before submission, verify all bibliographic metadata, taxonomy sizes, percentages, task details, and reliability statistics from primary ACL or publisher records.

## 1.2 Gius and Jacke / CATMA

Gius and Jacke’s work on the hermeneutic profit of annotation is a mandatory humanities-side comparison. Their discussion distinguishes four recurrent sources of annotation disagreement:

- misreading;
- inadequate category definitions;
- categories dependent on prior interpretive analysis;
- textual ambiguity or polysemy.

Broader questions of legitimate interpretive plurality are a consequence and interpretive implication of this discussion, not a fifth category to be attributed to the authors.

CATMA and related digital-hermeneutic workflows already support source-linked, overlapping, contradictory, collaborative, theory-guided, and meta-annotated interpretation.

TRIM therefore must concede that:

- productive disagreement in humanities annotation is not new;
- inspectable interpretive plurality is not new;
- source-linked collaborative literary annotation is not new;
- and annotation rationale or meta-annotation is not new.

TRIM’s remaining distinction is narrower:

> `friction_locus` is assigned prospectively within each independent record, before any observed coder disagreement, to identify the dominant pressure point in a source-anchored evidence-to-project-defined-function conversion.

This difference must be established empirically rather than asserted conceptually.

Verify the exact article title, venue, pagination, CATMA version context, and the relation to SANTA or other shared-task materials from primary sources before article drafting.

## 1.3 Walton critical questions and defeasible argumentation

Walton-style argument schemes and their critical questions are the strongest formal analogue for `friction_locus`. Critical questions identify assumptions or points at which a premise-to-claim inference may be challenged. Toulmin-style modelling and AIF also provide explicit evidence, warrant, qualifier, rebuttal, support, conflict, and alternative-path structures.

TRIM must therefore concede that locating contestable points in a reasoning route is not new.

The defensible migration claim is:

> TRIM adapts the intuition of scheme-specific contestability into a prospective, single-coder, record-internal field for non-propositional humanities evidence-to-function assignments.

The difference lies in the conjunction of:

- non-propositional source material;
- project-defined interpretive functions;
- prospective coding;
- single-record applicability;
- controlled cross-case comparison;
- and later evaluation against disagreement and adjudication.

Identify the most relevant Walton sources and distinguish critical questions from undercutting defeaters, rhetorical stasis, ambiguity taxonomies, and general disagreement-source classifications.

## 1.4 Sources-of-disagreement and ambiguity-locus taxonomies

Annotation-disagreement research already classifies disagreement sources such as:

- genuine ambiguity;
- narrative uncertainty;
- annotator assumptions;
- task framing;
- insufficient context;
- category-definition problems;
- and multiple legitimate readings.

This literature directly threatens any claim that TRIM first identifies where interpretation becomes difficult.

TRIM’s narrower distinction is that `friction_locus` is not merely a post hoc explanation of observed disagreement. It is a prospective field attached to each annotation before coder comparison.

## 1.5 Expert rationale disagreement

Expert-annotation research has already built taxonomies of disagreement in specialist rationales, including legal interpretation. TRIM therefore cannot defend itself by contrasting expert humanities judgement with lay or crowdsourced annotation alone.

Its remaining distinction is prospective: the conversion structure is recorded within every independent annotation rather than only diagnosed after two experts diverge.

## 1.6 Qualitative codebook plus memo

A conventional CAQDAS workflow can already preserve:

- source span;
- function or code;
- memo;
- coder identity;
- uncertainty notes;
- code hierarchies;
- overlap;
- and adjudication.

This is the strongest practical baseline because it is cheaper and familiar to humanities and qualitative researchers.

A sceptical reviewer can compress TRIM to:

> an elaborate qualitative codebook with auxiliary fields and a graph export.

TRIM survives only if its field structure yields comparative results that a free-text memo workflow cannot produce directly without a substantial second round of manual recoding.

## 1.7 CATMA, annotation graphs, provenance, CRMinf, and nanopublications

These infrastructures already provide various combinations of:

- source anchoring;
- layered and overlapping annotations;
- graph structures;
- provenance;
- belief or inference representation;
- agent and activity attribution;
- queryability;
- interoperability;
- and atomic scholarly claims.

TRIM should not be presented as an alternative to general annotation or provenance standards. It is better described as a lightweight, task-specific interpretive annotation profile that could be implemented in CATMA or mapped onto broader provenance and knowledge-representation models.

The candidate contribution is the domain-specific internal structure of the interpretive conversion record, not its storage or serialization technology.

## 1.8 Narrative and drama annotation

Story Workbench, DramaBank, SIG, Drammar, and related projects already operationalize high-level narrative theory into structured, graphable, reliability-tested annotations of events, intentions, goals, agency, affect, temporal relations, and narrative structure.

Theory-driven humanities annotation is not new. TRIM’s object must remain at a different level: not the narrative-world structure alone, but the scholarly warranting route through which textual evidence is assigned a project-defined function.

## 1.9 RST and discourse-relation annotation

RST and related frameworks already model functional relations among text spans and support systematic, controlled, and graph-based discourse analysis.

The distinction cannot be “function versus no function.” It must be:

- text-to-text discourse relation versus text-to-analyst-defined function;
- textual coherence structure versus accountable scholarly function assignment;
- relation classification versus conversion-path modelling.

The article should include at least one example where discourse annotation can represent the source relation but does not capture the project-specific interpretive conversion or its dominant pressure point.

# 2. Current evidence status

## 2.1 What the repository currently demonstrates

The current repository demonstrates:

- schema expressivity;
- software correctness;
- source anchoring;
- graph and table generation;
- author-constructed same-function/different-signature examples;
- contested-case representation;
- pilot-ready documentation;
- and a fully specified independent-coding workflow.

## 2.2 What the repository does not yet demonstrate

The current repository does not yet demonstrate:

- independent field-level reliability;
- independent reproduction of same-function/different-route distinctions;
- added value over span + function + memo;
- stable signature topology across coders;
- prospective prediction of adjudication difficulty;
- or cross-language construct validity.

The current intercoder demonstration contains no paired independent rows for `friction_locus` or `rationale_mechanism`. Therefore it is a workflow demonstration, not reliability evidence.

## 2.3 Correct evidence-level statement

The article must distinguish:

> **Expressivity demonstrated:** the schema can represent multiple conversion pathways.

from:

> **Independent validity not yet demonstrated:** the pilot has not yet shown that another coder can reproduce, distinguish, or use those pathways in a non-arbitrary way.

Author-constructed examples can establish possibility and intelligibility. They cannot establish reproducibility or necessity.

# 3. `friction_locus` claim boundary

## What it is not

`friction_locus` is not:

- a claim that interpretive contestability has never been theorized;
- identical to textual blanks or indeterminacy;
- identical to rhetorical stasis;
- identical to a critical question;
- identical to an undercutting defeater;
- identical to a post hoc source-of-disagreement category;
- or proof of an objectively difficult passage.

## Current defensible definition

> `friction_locus` prospectively records the dominant point at which a coder’s source-anchored conversion from textual evidence to project-defined interpretive function requires its most consequential judgement.

Its candidate distinctiveness lies in the conjunction of five properties:

1. prospective rather than only post hoc;
2. applicable within one coder’s record;
3. tied to evidence-to-function conversion;
4. encoded as a controlled cross-case field;
5. evaluated through later comparison and adjudication.

If the pilot does not show reliable, diagnostic, relational, or predictive value, `friction_locus` should be downgraded from central contribution to optional diagnostic field.

# 4. Ablation design

## Baseline A: outcome only

```text
source span + function label
```

This captures evidence location, final analytic assignment, and function-level agreement, but not reasons, disagreement source, alternative pathway, or field-level reliability.

## Baseline B: conventional interpretive record

```text
source span + function label + free-text rationale memo + confidence
```

This captures evidence, assignment, prose reasoning, broad confidence, and reviewable qualitative interpretation. Structured distinctions can be recovered only through later manual memo coding.

## Full TRIM

```text
source span + function label + structured conversion signature + rationale memo
```

Candidate additional value includes:

- field-level agreement;
- prospective disagreement localization;
- direct cross-case querying;
- compound pathway comparison;
- alternative-signature analysis;
- original/gloss relocation analysis;
- and prediction or diagnosis of adjudication difficulty.

The paper should not merely assert that Full TRIM is richer. It should compare what each design permits researchers to observe and report.

Minimum ablation outputs:

1. function agreement under all three representations;
2. whether same-function cases split into distinct signature patterns;
3. whether memo review independently recovers the same distinctions as the structured fields;
4. time or labour required to recover structured patterns from memos;
5. field-level agreement and confusion pairs;
6. association between uncertainty, alternative signature, and adjudication;
7. original/gloss function alignment versus signature alignment.

# 5. Pilot success and failure conditions

Field-level differential reliability is the most direct success condition, but it is not the only result that could justify the full model.

TRIM passes the deletion test if the pilot produces at least one independently reviewable structural result that is not available directly from span + function + memo without substantial secondary recoding.

## 5.1 Differential field reliability

Examples:

- function agreement is high while mechanism agreement is lower but structured;
- locus agreement differs meaningfully from function agreement;
- disagreement concentrates in theoretically intelligible confusion pairs;
- uncertainty and alternative-signature use are stable enough to interpret.

## 5.2 Stable signature topology

The full signature may form interpretable recurring structures, for example:

```text
warrant_attribution + authorizes + retrospective

temporal_layering + reframes + retrospective

perspective_assignment + qualifies + retrospective
```

Evidence for topology would include:

- recurring locus-mechanism-support combinations;
- clusters that survive close reading;
- genre- or tradition-linked pathway structures;
- same-function cases dividing into stable route families;
- or partially shared routes beneath different function labels.

Merely having more coded variables is insufficient. The joint structure must add interpretable value.

## 5.3 Cross-language relocation

A strong result occurs when original and gloss layers agree at function level but differ systematically in:

- `friction_locus`;
- `rationale_mechanism`;
- epistemic support;
- temporal orientation;
- or alternative pathway.

This would show that outcome-label equivalence can conceal translation-mediated construct movement.

## 5.4 Prospective adjudication prediction or localization

Candidate predictors include:

- particular `friction_locus` values;
- initial uncertainty;
- presence of `alternative_signature`;
- compound mechanisms;
- original/gloss divergence;
- and unusually qualified rationale notes.

The strongest result would show that these fields predict or localize later adjudication difficulty beyond the function label.

## 5.5 Partial-route convergence under function disagreement

Two coders may assign different final functions while agreeing on part of the conversion pathway, such as:

- same locus, different function;
- same mechanism, different function;
- shared epistemic support but different temporal interpretation.

This can reveal common interpretive structure hidden by outcome-level disagreement.

## 5.6 Failure condition

The full model fails the deletion test if:

- fields merely restate the memo;
- coders cannot distinguish locus from mechanism;
- each case produces an idiosyncratic signature with no cross-case value;
- independent coding requires extensive author coaching;
- structured outputs add no interpretable information;
- or all findings can be recovered easily from the simpler memo baseline.

# 6. Demonstration-corpus strategy

The three traditions should not be treated as interchangeable examples. Each carries a distinct burden in the methods argument.

## 6.1 *In a Grove*: intuitive route variation

*In a Grove* provides the most accessible demonstration of:

- one event represented through multiple testimonies;
- broad functional convergence with different warranting routes;
- contradiction, qualification, suspension, and reframing;
- and same-cue or same-event comparison.

Because it naturally concerns perspective and explanation variation, it can be compressed into a literary version of within-label variation and placed directly beside LiTEx or disagreement taxonomies. Use it to make route variation intuitive, but do not let it carry the whole novelty claim.

## 6.2 *Zuo zhuan*: non-propositional, project-defined conversion

The *Zuo zhuan* cases provide the strongest evidence that TRIM extends beyond benchmark rationale categorization and proposition-centred argument mapping.

They involve:

- divinatory results;
- ritual sequence;
- omen interpretation;
- ranked warrants;
- retrospective fulfilment;
- recalled signs;
- projected lineage consequence;
- and narrative uptake.

The source material is not simply a premise supporting a claim. The target function is also not necessarily a proposition asserted in the text. It is a project-defined historiographical or narrative function assigned through scholarly interpretation.

At least one *Zuo zhuan* comparison must show why evidence-to-function conversion cannot be reduced adequately to discourse relation, argument scheme, or rationale category alone.

## 6.3 *Macbeth*: temporal and retrospective conversion

The current demonstration dataset already contains three fully populated *Macbeth* annotations:

- `MAC_1_3`, coded as prospective and centred on partial confirmation, authorization, and reframing;
- `MAC_4_1`, coded as prospective-retrospective and centred on Macbeth’s narrowing of equivocal prophecy into false security;
- `MAC_5_8`, coded as retrospective and centred on later fulfilment reclassifying earlier assurance as an equivocal trap.

The *Macbeth* cases therefore do not exist only as a future plan. They already provide demonstration material for:

- authorization;
- equivocal narrowing;
- retrospective reframing;
- fulfilment changing the force of earlier evidence;
- and temporally distributed conversion.

Their current evidential status is still author-constructed demonstration, not independent validation.

Use *Macbeth* to demonstrate why temporal orientation and mechanism may matter when the same prophetic material changes force across narrative time.

## 6.4 Combined logic

The corpus supports a three-part methods demonstration:

- *In a Grove* makes route variation legible;
- *Zuo zhuan* establishes non-propositional and project-defined conversion;
- *Macbeth* establishes temporally distributed and retrospective conversion.

No single corpus component should be asked to prove the entire method.

# 7. Article-scale outcomes

## Outcome A: full TRIM article

Use only if the pilot shows usable field-level reliability, substantive route variation, at least one queryable structural pattern, and added value beyond memo.

Possible article claim:

> a multidimensional annotation model makes interpretive conversion pathways directly comparable and localizes variation concealed by shared function labels.

## Outcome B: narrower fielded-rationale article

Use if some fields work but the full signature is over-specified.

Possible article claim:

> a small set of structured rationale fields improves the comparison of humanities annotations beyond labels and prose memos.

## Outcome C: friction-locus diagnostic article

Use if `friction_locus` is reliable or predicts adjudication while the remaining signature provides limited added value.

Possible article claim:

> prospective coding of interpretive pressure helps identify and compare difficult evidence-to-function assignments.

## Outcome D: negative or reflective methods article

Use if independent coding exposes serious instability but the failure reveals important limits of formalizing interpretation.

This remains publishable if reported honestly, but it would be a different article.

# 8. Current research questions

## RQ1

How can the warranted movement from source-anchored textual evidence to project-defined interpretive function be represented without reducing interpretation to either an outcome label or unrestricted prose rationale?

## RQ2

What forms of within-function variation become visible when interpretive pathways are compared at the levels of threshold locus, mechanism, epistemic support, discourse position, temporal orientation, uncertainty, and alternatives?

## RQ3

Can independent coders use this representation consistently while preserving substantive disagreement as structured evidence rather than treating it only as error?

## RQ4

Do structured pathway fields provide analytically consequential information beyond a source-span, function-label, and free-text-rationale baseline?

## Cross-language validity question

To what extent are interpretive conversion pathways preserved, softened, introduced, or relocated when source-language passages are mediated through close glosses?

# 9. Current safe contribution statement

> TRIM proposes a source-anchored, multidimensional representation of selected scholarly commitments involved in assigning project-defined interpretive functions to textual evidence. Its distinctiveness is not the discovery of rationale variation, annotation disagreement, contestability, or graph-based provenance. It lies in bringing these concerns into a prospective conversion record whose internal fields can be tested independently for reliability, cross-case structure, adjudication value, and cross-language stability.

The final contribution claim must be selected from the observed pilot result rather than fixed in advance.

# 10. Epistemic boundaries

The article must state that:

- TRIM formalizes selected commitments, not interpretation in full;
- structured fields do not exhaust a reading;
- agreement does not establish interpretive truth;
- disagreement does not automatically establish productive plurality;
- source-language coding remains scholarly interpretation, not absolute ground truth;
- rationale notes may be retrospective rationalizations;
- project-defined functions are not universal ontological facts;
- controlled fields may reflect the assumptions of an interpretive community;
- graphability does not imply causal, logical, or objective necessity;
- and simplification after pilot failure is a valid methodological result.

# 11. Literature verification queue

## Priority 1: closest threats

- LiTEx: primary paper, taxonomy, reliability, same-span/different-reason evidence;
- Agree, Disagree, Explain: final venue and across-label findings;
- Gius and Jacke 2017: exact disagreement model and relation to CATMA/SANTA;
- Walton: argument schemes and critical questions most directly comparable to `friction_locus`;
- expert-rationale disagreement research, including legal interpretation;
- sources-of-disagreement and ambiguity-locus taxonomies.

## Priority 2: infrastructure and humanities annotation

- CATMA and heureCLÉA meta-annotation;
- Annotation Graphs;
- W3C Web Annotation and PROV-O;
- CRMinf and relevant CIDOC-CRM inference/belief classes;
- Story Workbench, DramaBank, SIG, and Drammar;
- RST and enhanced RST signalling;
- nanopublications.

## Priority 3: conceptual analogues

- rhetorical stasis;
- undercutting defeaters;
- literary blanks and indeterminacy;
- interpretive communities;
- annotation perspectivism;
- rationale faithfulness and retrospective rationalization.

For each item, verify exact bibliographic metadata and passage-level support before using it in article prose.

# 12. Stop rule

Do not revise the TRIM schema, codebook, controlled vocabularies, or pilot packet in response to this document.

The current schema is the validation object. Changing it before the blinded pilot would move the object being tested.

The next schema decision must follow observed evidence about:

- independent usability;
- field-level reliability;
- redundancy;
- signature topology;
- cross-language relocation;
- disagreement localization;
- and adjudication difficulty.
