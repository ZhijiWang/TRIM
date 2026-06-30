# TRIM Literature Positioning

## Positioning Summary

TRIM is not new because it uses annotation, codebooks, reliability checks, rationale notes, provenance, or graph representations. All of those have strong precedents.

TRIM's defensible novelty is narrower:

> It packages selected textual evidence, analytic anchor, final function, threshold location, rationale mechanism, support type, discourse level, temporality, uncertainty, and complete alternative signature into one comparable evidence-to-function pathway, then uses that pathway to diagnose disagreement without treating all disagreement as failed reliability.

This is a recombination and operationalization claim, not a first-in-history claim.

## Literature Map

### 1. Annotation and Intercoder Reliability

Core sources:

- Cohen, Jacob. 1960. "A Coefficient of Agreement for Nominal Scales." *Educational and Psychological Measurement* 20(1): 37-46. DOI: 10.1177/001316446002000104.
- Krippendorff, Klaus. 2018. *Content Analysis: An Introduction to Its Methodology*. 4th ed. SAGE.
- Hayes, Andrew F., and Klaus Krippendorff. 2007. "Answering the Call for a Standard Reliability Measure for Coding Data." *Communication Methods and Measures* 1(1): 77-89. DOI: 10.1080/19312450709336664.
- MacQueen, Kathleen M., Eleanor McLellan, Kelly Kay, and Bobby Milstein. 1998. "Codebook Development for Team-Based Qualitative Analysis." *Cultural Anthropology Methods* 10(2): 31-36. DOI: 10.1177/1525822X980100020301.
- Campbell, John L., Charles Quincy, Jordan Osserman, and Ove K. Pedersen. 2013. "Coding In-depth Semistructured Interviews: Problems of Unitization and Intercoder Reliability and Agreement." *Sociological Methods & Research* 42(3): 294-320. DOI: 10.1177/0049124113500475.

How TRIM fits:

- It accepts the need for agreement reporting but rejects the idea that final-label agreement alone is enough.
- It treats unitization/evidence selection as a first-class part of the annotation, not a preprocessing detail.
- It preserves raw disagreement before adjudication.

Novelty risk:

- Qualitative researchers will recognize much of this as codebook development, memoing, adjudication, and disagreement analysis.
- The article must explain why structured pathway fields do something that ordinary codebooks plus memos do not.

### 2. Qualitative and Interpretive Methodology

Core sources:

- Braun, Virginia, and Victoria Clarke. 2006. "Using Thematic Analysis in Psychology." *Qualitative Research in Psychology* 3(2): 77-101. DOI: 10.1191/1478088706qp063oa.
- Braun, Virginia, and Victoria Clarke. 2019. "Reflecting on Reflexive Thematic Analysis." *Qualitative Research in Sport, Exercise and Health* 11(4): 589-597. DOI: 10.1080/2159676X.2019.1628806.
- Barbour, Rosaline S. 2001. "Checklists for Improving Rigour in Qualitative Research: A Case of the Tail Wagging the Dog?" *BMJ* 322: 1115-1117. DOI: 10.1136/bmj.322.7294.1115.
- O'Connor, Cliodhna, and Helene Joffe. 2020. "Intercoder Reliability in Qualitative Research: Debates and Practical Guidelines." *International Journal of Qualitative Methods* 19. DOI: 10.1177/1609406919899220.

How TRIM fits:

- It should not sound hostile to interpretive plurality or reflexive method.
- It should say that transparency and auditability are not the same as validity.
- It can borrow the distinction between coding reliability and interpretive adequacy.

Novelty risk:

- Reflexive thematic analysis will challenge any implication that structured coding is inherently better.
- TRIM must be framed as useful for projects that choose comparative, reviewable annotation, not as a universal norm for all qualitative interpretation.

### 3. Digital Humanities and Computational Literary Studies

Core sources:

- Moretti, Franco. 2013. *Distant Reading*. Verso.
- Rockwell, Geoffrey, and Stéfan Sinclair. 2016. *Hermeneutica: Computer-Assisted Interpretation in the Humanities*. MIT Press.
- Mohr, John W., Robin Wagner-Pacifici, and Ronald L. Breiger. 2015. "Toward a Computational Hermeneutics." *Big Data & Society*. DOI: 10.1177/2053951715613809.
- Dobson, James. 2021. "Interpretable Outputs: Criteria for Machine Learning in the Humanities." *Digital Humanities Quarterly* 15(2), article 000555.
- Kleymann, Rabea, and Jan-Erik Stange. 2021. "Towards Hermeneutic Visualization in Digital Literary Studies." *Digital Humanities Quarterly* 15(2), article 000547. DOI: 10.63744/ekkjwp88jksx.
- Nelson, Laura K. 2020. "Computational Grounded Theory: A Methodological Framework." *Sociological Methods & Research* 49(1): 3-42. DOI: 10.1177/0049124117729703.

How TRIM fits:

- It belongs with work that asks how humanistic interpretation is operationalized and made computationally inspectable.
- It is closest to middle-range DH methods: neither unrestricted close reading nor automated extraction.
- It can answer a CLS problem: labels and features often hide the interpretive route that made them meaningful.

Novelty risk:

- DH has many annotation, categorization, and visualization projects. TRIM must not claim that "structured interpretation" is itself new.
- The article needs a worked example showing a payoff that would be hard to obtain from final labels alone.

### 4. Argumentation and Rationale Representation

Core sources:

- Toulmin, Stephen. 1958. *The Uses of Argument*. Cambridge University Press.
- Walton, Douglas, Chris Reed, and Fabrizio Macagno. 2008. *Argumentation Schemes*. Cambridge University Press.
- Rahwan, Iyad, and Chris Reed. 2009. "The Argument Interchange Format." In *Argumentation in Artificial Intelligence*. Springer. DOI: 10.1007/978-0-387-98197-0_19.
- Bird, Steven, and Mark Liberman. 2001. "A Formal Framework for Linguistic Annotation." *Speech Communication* 33(1-2): 23-60. DOI: 10.1016/S0167-6393(00)00068-6.

How TRIM fits:

- TRIM resembles evidence-to-claim and warrant representation, but its "claim" is a project-defined interpretive function.
- `rationale_mechanism` is not a Toulmin warrant; it is a controlled description of what the conversion does.
- `alternative_signature` resembles structured preservation of competing argument paths.

Novelty risk:

- Argumentation scholars may find TRIM under-formalized if it borrows warrant language loosely.
- Avoid saying "argument graph" unless the paper formally maps to argumentation structures.

### 5. Explainability, Auditability, and Provenance

Core sources:

- W3C. 2013. *PROV-O: The PROV Ontology*. W3C Recommendation.
- Mitchell, Margaret et al. 2019. "Model Cards for Model Reporting." *Proceedings of FAT* '19*. DOI: 10.1145/3287560.3287596.
- Gebru, Timnit et al. 2021. "Datasheets for Datasets." *Communications of the ACM* 64(12): 86-92. DOI: 10.1145/3458723.
- Bender, Emily M., and Batya Friedman. 2018. "Data Statements for Natural Language Processing." *Transactions of the ACL* 6: 587-604. DOI: 10.1162/tacl_a_00041.

How TRIM fits:

- It records provenance-like information about how a human annotation was warranted.
- It is closer to human audit trails than model explainability.
- Model cards and data statements are useful only by analogy: they show how structured documentation changes review conditions.

Novelty risk:

- XAI language can mislead reviewers into expecting machine learning evaluation.
- Use "auditability" and "reviewability" rather than "explainability" unless the article explicitly addresses XAI.

### 6. Existing Comparable Tools and Models

### 6. Annotation Disagreement And Perspectivist Annotation

Recent annotation research increasingly argues that disagreement is not always
noise. Perspectivist approaches retain annotator distributions, multiple labels,
or disagreement patterns because majority vote can erase meaningful ambiguity,
perspective, or social variation.

Core areas to cover before submission:

- perspectivist NLP and data annotation;
- disagreement as task ambiguity rather than only annotator error;
- annotator distributions and label variation;
- social and perspectival disagreement;
- limits of majority-vote aggregation.

How TRIM fits:

- Perspectivist annotation preserves multiple labels or label distributions.
- TRIM additionally represents the evidential and inferential pathway by which a
  coder reaches a function.
- TRIM should not claim to have invented meaningful disagreement. Its narrower
  claim is that pathway fields make certain kinds of disagreement easier to
  locate and adjudicate.

### 7. Hermeneutic Annotation And CATMA

The article needs a stronger account of hermeneutic annotation. CATMA and
related DH annotation work already treat annotation as interpretive, iterative,
overlapping, and non-exclusive. This literature is a serious novelty challenge.

Topics to cover:

- annotation as interpretive practice;
- overlapping and non-exclusive annotation;
- iterative annotation and the hermeneutic circle;
- markup as argument or reading practice;
- literary annotation platforms such as CATMA.

How TRIM differs:

- CATMA-style annotation can preserve rich interpretive markup.
- TRIM's distinctive unit is the evidence-to-function pathway: selected evidence,
  anchor, threshold, rationale, support, discourse level, temporality,
  uncertainty, and complete alternative signature.
- TRIM is not rediscovering hermeneutic annotation; it structures a particular
  pathway layer for comparison and disagreement analysis.

### 8. Rationale Annotation And Explanation Datasets

Rationale and explanation datasets distinguish supporting spans, extractive
rationales, free-text rationales, and explanation faithfulness. TRIM should be
positioned near this work but not collapsed into it.

Topics to cover:

- extractive rationale spans and evidence-span annotation;
- free-text explanations;
- explanation datasets and rationale disagreement;
- faithfulness debates where machine explanations are involved;
- within-label variation in explanation.

How TRIM differs:

- Rationale spans identify supporting text.
- TRIM structures how evidence is converted into an analytic function.
- TRIM supports complete alternative pathways and does not assume one uniquely
  correct rationale.

### 9. Annotation Provenance

The provenance discussion should go beyond W3C PROV. Add scholarly annotation
provenance, authorship, versioning, annotation lifecycle, source-text
provenance, and evidence traceability.

The v0.2.1 source-text patch strengthens this line of argument: the retest now
records actual segment text plus source-text provenance instead of asking coders
to treat project-authored summaries as evidence.

### 10. Classification And Data-Making

Critical data studies and classification literature can help explain why labels
are made rather than found. Use this literature selectively. It should support
the final-label compression problem without overwhelming the article's practical
methods argument.

| Existing approach | What it captures | What it loses | How TRIM differs | Risk of overstating novelty |
| --- | --- | --- | --- | --- |
| Qualitative codebooks and CAQDAS tools such as NVivo, ATLAS.ti, MAXQDA, QualCoder | Codes, memos, excerpts, coder comparison, sometimes adjudication | The pathway from evidence to analytic function is often free-text or project-specific | TRIM standardizes a pathway signature and alternative signature for comparison | High: qualitative coding already has memos and adjudication |
| CATMA and DH literary annotation platforms | Textual markup, categories, tags, interpretive annotation | Often records what is annotated and how it is tagged, not a structured evidence-to-function conversion | TRIM focuses on the warranting route behind a function label | Medium-high: CATMA is explicitly hermeneutic and DH-native |
| WebAnno / INCEpTION / brat | Annotation schemas, spans, relations, agreement workflows | Primarily linguistic/NLP annotation; interpretive rationale often external | TRIM's controlled fields target interpretive threshold and rationale | Medium: schema and span annotation are not new |
| Recogito / semantic annotation | Entities, places, semantic links, stand-off annotation | Rationale for interpretive function is not central | TRIM treats selected evidence and conversion as the object | Medium |
| Argument annotation / AIF | Claims, premises, attacks/supports, argument schemes | Literary interpretive function, discourse level, uncertainty, and alternatives are not normally packaged this way | TRIM borrows evidence-to-claim logic but adapts it to interpretive pathways | High if TRIM uses "warrant" too broadly |
| Provenance models such as W3C PROV | Entities, activities, agents, transformations | Domain-specific interpretive adequacy and disagreement taxonomy | TRIM is provenance-like but task-specific | Medium |
| Model/data documentation frameworks | Structured reporting of model/data assumptions and limits | Not annotation-level reasoning | TRIM documents individual interpretive records | Low if kept as analogy |
| Within-label variation in NLI explanation datasets | Same labels can have different reasons | Literary/humanistic interpretation and discourse-level pathway structure | TRIM makes within-label variation central in interpretive annotation | Medium; replace arXiv citations with ACL records before publication where possible |

## Bodies Of Literature That Challenge Novelty

1. **Qualitative coding and memoing.** Challenge: "You have reinvented codebooks plus analytic memos." Response: TRIM does not replace memos; it makes selected parts of the memo pathway field-comparable.
2. **Argumentation and rationale annotation.** Challenge: "Evidence-to-claim structures already exist." Response: TRIM adapts that logic to interpretive function, discourse level, temporality, uncertainty, and competing full signatures.
3. **DH annotation platforms.** Challenge: "Humanities annotation has long been interpretive and graphable." Response: TRIM's contribution is not annotation as such, but the evidence-to-function pathway as the comparable unit.
4. **Provenance and audit trails.** Challenge: "This is provenance metadata." Response: TRIM includes provenance-like features but also controlled interpretive categories and disagreement taxonomy.

## Language To Avoid

Avoid:

- "solves interpretation";
- "objective interpretation";
- "universal interpretive schema";
- "validated reliability";
- "cross-language validity";
- "automated rationale modelling";
- "argument graph" unless formally mapped;
- "explainable AI" unless the article engages XAI directly.

Prefer:

- reviewable interpretive annotation;
- evidence-to-function pathway;
- structured disagreement;
- pilot-informed method development;
- comparative pathway signature;
- project-specific function vocabulary;
- prospective retest.

## Sources Still Needing Final Verification Before Submission

- Current ACL Anthology records for LiveNLI and LiTEx if used.
- Current journal version of Graphilosophy if it moves beyond preprint.
- Exact CATMA/WebAnno/INCEpTION/brat citations selected for the final literature review.
