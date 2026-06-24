# TRIM Article Working Notes

## Status

This is a paper-development document, not a normative method specification. It records the current novelty audit, the closest prior work, the pilot decision rules, and the ablation design that will determine the eventual scale of the article’s contribution.

Do not use this file to revise the TRIM schema before the independent pilot. The validation object must remain stable until pilot results are available.

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

This claim remains provisional. It survives only if the pilot shows that the structured fields provide information that cannot be recovered adequately from a simpler source-span, function-label, and free-text-memo workflow.

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

# 1. Closest prior work

## 1.1 LiTEx and within-label explanation variation

### Established prior contribution

The LiTEx line of work already turns free-text explanations into a controlled, reliability-tested taxonomy and studies variation concealed by shared outcome labels. It therefore directly occupies the territory of:

- same label, different reasons;
- same or similar evidence spans selected for different reasons;
- rationale categorization;
- rationale-level agreement;
- and systematic analysis of within-label variation.

### Consequence for TRIM

TRIM cannot present within-label reasoning variation as a discovery. Its remaining distinction is that it represents a coordinated, multidimensional conversion pathway for humanities interpretation rather than assigning one or more explanation-strategy categories to benchmark rationales.

### Question the pilot must answer

Does the joint signature reveal stable relations among locus, mechanism, support, discourse, temporality, uncertainty, and alternatives, or is it merely a larger collection of independent rationale categories?

### Bibliographic verification required

Before submission, replace working references with checked ACL Anthology or publisher records and verify all reported percentages, taxonomy sizes, task details, and reliability statistics from the papers themselves.

## 1.2 Gius and Jacke, CATMA, and hermeneutic annotation disagreement

### Established prior contribution

Digital-hermeneutic annotation has already argued that disagreement can be epistemically productive rather than merely erroneous. Gius and Jacke’s work is especially close because it asks when annotation disagreement reflects:

- misreading;
- inadequate category definition;
- dependence on prior analysis;
- textual ambiguity or polysemy;
- and legitimate interpretive plurality.

CATMA and related work already support source-linked, overlapping, contradictory, collaborative, and theory-guided humanities annotation.

### Consequence for TRIM

TRIM cannot claim that it first preserves plurality or makes literary disagreement inspectable. The more specific distinction is prospective and record-internal: each coder identifies the dominant pressure point within the evidence-to-function conversion before comparison with another coder.

### Question the pilot must answer

Does prospective `friction_locus` coding produce useful information beyond post hoc classification of disagreement sources?

### Bibliographic verification required

Verify the exact four-part disagreement classification, article title, venue, pagination, CATMA version context, and the relation to SANTA or other shared-task materials from primary sources.

## 1.3 Walton-style critical questions and defeasible argumentation

### Established prior contribution

Argument schemes already associate inference patterns with critical questions that identify assumptions or conditions under which a premise-to-claim move may be challenged. Toulmin-style modelling and AIF also provide explicit evidence, warrant, qualifier, rebuttal, support, conflict, and alternative-path structures.

### Consequence for TRIM

`friction_locus` is not a new discovery of contestability. Its candidate contribution is an operational migration:

> a prospective, single-coder, record-internal field locating the dominant interpretive pressure in a source-anchored evidence-to-project-defined-function conversion.

The target is not necessarily a proposition, the source need not be an argument, and the function may be narratological, historiographical, ethical, testimonial, mantic, or reception-oriented.

### Question the pilot must answer

Does `friction_locus` behave as a coherent field across non-propositional humanities cases, and does it localize later adjudication difficulty?

### Bibliographic verification required

Identify the most relevant Walton sources on argument schemes and critical questions, and distinguish critical questions from undercutting defeaters, stasis, ambiguity taxonomies, and general disagreement-source classifications.

## 1.4 Expert rationale disagreement

### Established prior contribution

Expert-annotation research has already built taxonomies of disagreement in specialist rationales, including legal interpretation. TRIM therefore cannot defend itself by contrasting expert humanities judgement with lay or crowdsourced annotation alone.

### Remaining distinction

TRIM structures the conversion prospectively within every record rather than only diagnosing divergence after two experts disagree.

### Question the pilot must answer

Do independently completed signatures reveal systematic structure even where coders agree on the final function label?

## 1.5 Qualitative codebook plus memo

### Established prior contribution

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

### Central substitution challenge

A sceptical reviewer can compress TRIM to:

> an elaborate qualitative codebook with auxiliary fields and a graph export.

TRIM survives only if its field structure yields comparative results that a free-text memo workflow cannot produce without a substantial second round of manual recoding.

### Question the pilot must answer

Can the full signature localize disagreement, support field-level reliability, reveal cross-case clusters, or predict adjudication difficulty beyond span + function + memo?

## 1.6 CATMA, annotation graphs, provenance, CRMinf, and nanopublications

### Established prior contribution

These infrastructures already provide various combinations of:

- source anchoring;
- layered and overlapping annotations;
- graph structures;
- provenance;
- belief or inference representation;
- agent and activity attribution;
- queryability;
- interoperability;
- atomic scholarly claims.

### Consequence for TRIM

TRIM should not be presented as an alternative to general annotation or provenance standards. It is better described as a lightweight, task-specific interpretive annotation profile that could be implemented in CATMA or mapped onto broader provenance and knowledge-representation models.

### Remaining distinction

The candidate contribution is the domain-specific internal structure of the interpretive conversion record, not its storage or serialization technology.

## 1.7 Narrative and drama annotation

### Established prior contribution

Story Workbench, DramaBank, SIG, Drammar, and related projects already operationalize high-level narrative theory into structured, graphable, reliability-tested annotations of events, intentions, goals, agency, affect, temporal relations, and narrative structure.

### Consequence for TRIM

Theory-driven humanities annotation is not new. TRIM’s object must remain at a different level: not the narrative-world structure alone, but the scholarly warranting route through which textual evidence is assigned a project-defined function.

### Question the pilot and demonstrations must answer

Can two cases share a narrative or interpretive function while showing consequentially different conversion signatures?

## 1.8 RST and discourse-relation annotation

### Established prior contribution

RST and related frameworks already model functional relations among text spans and support systematic, controlled, and graph-based discourse analysis.

### Consequence for TRIM

The distinction cannot be “function versus no function.” It must be:

- text-to-text discourse relation versus text-to-analyst-defined function;
- textual coherence structure versus accountable scholarly function assignment;
- relation classification versus conversion-path modelling.

### Required demonstration

The article should include at least one example where discourse annotation can represent the source relation but does not capture the project-specific interpretive conversion or its dominant pressure point.

# 2. `friction_locus` claim boundary

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

## Conditions for retaining it as a central contribution

At least one of the following should be observed in the pilot:

- locus agreement differs meaningfully from function agreement;
- locus disagreement localizes adjudication to identifiable conversion stages;
- some locus values are associated with higher uncertainty or alternative-signature use;
- some locus values predict disagreement or adjudication difficulty;
- original/gloss pairs preserve function while relocating locus;
- locus-mechanism combinations form interpretable cross-case clusters.

If none occurs, `friction_locus` should be downgraded from central contribution to optional diagnostic field.

# 3. Ablation design

## Baseline A: outcome only

```text
source span + function label
```

Captures:

- evidence location;
- final analytic assignment;
- function-level agreement.

Cannot directly capture:

- reasons;
- disagreement source;
- alternative pathway;
- field-level reliability.

## Baseline B: conventional interpretive record

```text
source span + function label + free-text rationale memo + confidence
```

Captures:

- evidence;
- final assignment;
- prose reasoning;
- broad confidence;
- reviewable qualitative interpretation.

Can recover structured distinctions only through later manual memo coding.

## Full TRIM

```text
source span + function label + structured conversion signature + rationale memo
```

Candidate additional value:

- field-level agreement;
- prospective disagreement localization;
- direct cross-case querying;
- compound pathway comparison;
- alternative-signature analysis;
- original/gloss relocation analysis;
- prediction or diagnosis of adjudication difficulty.

## Required comparison

The paper should not merely assert that Full TRIM is richer. It should compare what each design permits researchers to observe and report.

### Minimum ablation outputs

1. Function agreement under all three representations.
2. Whether same-function cases split into distinct signature patterns.
3. Whether memo review independently recovers the same distinctions as the structured fields.
4. Time or labour required to recover structured patterns from memos.
5. Field-level agreement and confusion pairs.
6. Association between uncertainty, alternative signature, and adjudication.
7. Original/gloss function alignment versus signature alignment.

# 4. Pilot decision rules

The pilot is not merely a check that a second coder can fill the form. It determines what article can honestly be written.

## Decision line 1: differential field reliability

### Evidence that supports the full model

- high or moderate function agreement;
- non-uniform agreement across signature fields;
- disagreement concentrated in theoretically intelligible fields;
- confusion pairs that correspond to known boundary distinctions;
- stable coder use of alternatives and uncertainty.

### Evidence against the full model

- uniformly low field agreement;
- arbitrary field use;
- systematic coder collapse of multiple fields into the memo;
- inability to distinguish locus from mechanism;
- agreement achieved only through extensive author coaching.

## Decision line 2: queryable cross-case patterns

### Evidence that supports the full model

At least one pattern should emerge that is difficult to identify from outcome labels alone, such as:

- same function, different locus clusters;
- same locus, different mechanism clusters;
- same mechanism, different epistemic support;
- tradition- or genre-linked signature patterns;
- contested cases concentrated in specific locus-mechanism combinations;
- cross-language function alignment with threshold relocation.

### Evidence against the full model

- signatures merely restate the memo;
- every case is effectively unique;
- no cross-case pattern survives close reading;
- field combinations do not add interpretive meaning.

## Decision line 3: adjudication difficulty

### Candidate indicators

Test whether the following are associated with later adjudication:

- low initial uncertainty confidence;
- presence of `alternative_signature`;
- particular `friction_locus` values;
- compound mechanisms;
- original/gloss divergence;
- long or highly qualified rationale notes.

### Strongest possible result

`friction_locus` or specific signature structures predict which cases require adjudication even after accounting for function label.

### Weak result

Fields explain disagreement after the fact but do not predict or localize it prospectively.

## Decision line 4: cross-language construct validity

Classify original/gloss pairs into:

- function and signature aligned;
- function aligned, locus or mechanism shifted;
- source friction softened in gloss;
- friction introduced by gloss;
- function itself changed;
- unresolved due to source-language interpretation.

The most informative result is function-level agreement with signature-level relocation, because it demonstrates variation hidden by the outcome label.

# 5. Pilot result typology

## Type 1: full convergence

Function, source span, and signature agree.

Interpretation:

- evidence of usability and reproducibility;
- not by itself proof that all fields are necessary.

## Type 2: same function, different route

Function agrees, but locus, mechanism, support, temporality, or alternative pathway differs.

Interpretation:

- strongest evidence for TRIM’s core argument;
- requires close case analysis to establish that the difference is substantive rather than coder noise.

## Type 3: different function, partially shared route

Function differs, but part of the signature converges.

Interpretation:

- may show shared interpretive pressure beneath divergent outcomes;
- potentially important for adjudication and theory revision.

## Type 4: original/gloss relocation

Function agrees across layers, but dominant locus or mechanism changes.

Interpretation:

- strongest cross-language construct-validity result;
- shows why function-level equivalence is insufficient.

## Type 5: schema failure

Coders cannot distinguish fields, fields are redundant, or the signature adds no cross-case information.

Interpretation:

- simplify or ablate the model;
- do not protect fields merely because they required substantial development.

# 6. Article-scale outcomes

## Outcome A: full TRIM article

Use only if the pilot shows:

- usable field-level reliability;
- substantive same-function/different-route cases;
- at least one queryable cross-case signature pattern;
- and evidence that structured fields add value beyond memo.

Article claim:

> a multidimensional annotation model makes interpretive conversion pathways directly comparable and localizes variation concealed by shared function labels.

## Outcome B: narrower fielded-rationale article

Use if:

- some fields work but the full signature is over-specified;
- locus and mechanism remain useful;
- other fields are mostly descriptive or redundant.

Article claim:

> a small set of structured rationale fields improves the comparison of humanities annotations beyond labels and prose memos.

## Outcome C: friction-locus diagnostic article

Use if:

- `friction_locus` is reliable or predicts adjudication;
- the remaining signature provides limited added value.

Article claim:

> prospective coding of interpretive pressure helps identify and compare difficult evidence-to-function assignments.

## Outcome D: negative or reflective methods article

Use if:

- independent coding exposes serious instability;
- the fields cannot be reliably separated;
- but the failure reveals important limits of formalizing interpretation.

This outcome is still publishable if reported honestly, but it would be a different article.

# 7. Current research questions

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

# 8. Current safe contribution statement

> TRIM is a source-anchored interpretive annotation model that structures selected scholarly commitments involved in assigning project-defined functions to textual evidence. It combines practices established in discourse annotation, argument modelling, qualitative coding, narratological annotation, provenance, and disagreement-aware rationale analysis. Its contribution, if supported by the pilot, is the operationalization of the evidence-to-function conversion as a multidimensional comparative record, including a prospective field for locating dominant interpretive pressure.

# 9. Epistemic boundaries

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

# 10. Literature verification queue

## Priority 1: closest threats

- LiTEx: primary paper, taxonomy, reliability, same-span/different-reason evidence.
- Agree, Disagree, Explain: final venue and across-label findings.
- Gius and Jacke 2017: exact disagreement model and its relation to CATMA/SANTA.
- Walton: argument schemes and critical questions most directly comparable to `friction_locus`.
- From Dissonance to Insights: expert-rationale disagreement taxonomy and study design.

## Priority 2: infrastructure and humanities annotation

- CATMA and heureCLÉA meta-annotation.
- Annotation Graphs.
- W3C Web Annotation and PROV-O.
- CRMinf and relevant CIDOC-CRM inference/belief classes.
- Story Workbench, DramaBank, SIG, and Drammar.
- RST and enhanced RST signalling.
- Nanopublications.

## Priority 3: conceptual analogues

- rhetorical stasis;
- undercutting defeaters;
- literary blanks and indeterminacy;
- sources-of-disagreement taxonomies;
- interpretive communities;
- annotation perspectivism;
- rationale faithfulness and retrospective rationalization.

For each item, verify exact bibliographic metadata and passage-level support before using it in article prose.

# 11. Stop rule

Do not modify the TRIM schema in response to this document before independent pilot data are available.

The next revision decision must be based on observed evidence about:

- field usability;
- field-level agreement;
- redundancy;
- cross-case patterns;
- adjudication difficulty;
- and cross-language relocation.

Until then, this file is a research and writing instrument, not a specification change request.
