# TRIM Article Outline

Recommended target: **Journal of Computational Literary Studies** if the v0.2.1 retest is completed; **Digital Humanities Quarterly** as the most realistic broad DH target.

Recommended length: **8,000-9,000 words** for JCLS/DSH-style article; **7,000-8,500 words** for DHQ.

## Revised Argument-Led Architecture

The article should no longer use a generic methods-report structure. It should
open with two contrasting examples:

- same final function, different pathway;
- different final function, substantially shared pathway.

Neither example should identify the primary coder as ground truth.

Recommended sections:

1. The false clarity of final-label agreement
2. What annotation systems preserve-and erase
3. TRIM as an evidence-to-function pathway
4. A diagnostic pilot, not a reliability test
5. What the first pilot made visible
6. Prospective revision and out-of-sample retest
7. Retest findings
8. What pathway agreement adds-and does not add
9. Limitations
10. Conclusion

The v0.2.1 retest section should explicitly note the final source-text patch:
formal segments now use source text or documented public-domain translation text,
with provenance, rather than project-authored summaries.

## Section Blueprint

| Section | Purpose | Evidence | Figures/tables | Words | Main risk |
| --- | --- | --- | --- | ---: | --- |
| 1. Introduction: the missing middle in interpretive annotation | Establish problem: labels alone are too thin, memos alone are hard to compare. | Pilot asymmetry: function 80% agreement but pathway fields far lower; examples of same-label/different-pathway logic. | Figure 1: evidence-to-function pathway; Table 1: article claims and limits. | 900 | Overstating novelty or reliability. |
| 2. Why final labels are insufficient | Argue that label agreement and disagreement have multiple methodological meanings. | v0.2.0 field-level agreement and adjudication categories. | Table 2: final-label vs pathway disagreement types. | 900 | Sounding anti-reliability rather than more precise about reliability. |
| 3. Related approaches and methodological gap | Position against qualitative coding, DH annotation, operationalization, argumentation, provenance, XAI. | Literature review from claim matrix and positioning file. | Table 3: existing approaches and what TRIM adds. | 1,200 | Thin literature review or excessive novelty claim. |
| 4. TRIM architecture | Define the model and fields. | Codebook v0.2.1; schema; validator; graph components. | Figure 2: TRIM architecture; Figure 3: one complete annotation pathway. | 1,100 | Becoming documentation rather than argument. |
| 5. Pilot design: v0.2.0 | Explain first pilot as usability/method-development, not validation. | Ten cases; independent second coder; post-pilot interview; locked archive. | Table 4: pilot corpus and conditions. | 800 | Reviewers may see pilot as too small. |
| 6. What the first pilot revealed | Present diagnostic findings. | Completion; field agreement; all-segment selection; question-log gap; boundary findings. | Figure 4: field-level agreement chart; Table 5: adjudication categories. | 1,100 | Treating descriptive agreement as reliability proof. |
| 7. Pilot-informed v0.2.1 revisions | Show traceability from pilot findings to revisions. | Revision traceability; manuals; schema validation; package leakage tests. | Figure 5: revision trace; Table 6: pilot issue -> revision -> retest measure. | 900 | Looking like patch notes. |
| 8. Prospective retest design | Describe the 12-case out-of-sample retest and planned analysis. | Retest protocol, case audit, semantic-steering audit, manifest, source packet. | Table 7: retest design matrix; Figure 6: adjudication workflow. | 800 | Too much future tense if results absent. |
| 9. Discussion: disagreement as structure rather than noise | Explain contribution: disagreement categories, auditability, interpretive plurality. | Worked examples; field-specific disagreement logic. | Figure 7: two pathways to same function or divergent pathways. | 900 | Sounding like transparency equals validity. |
| 10. Limitations | State limitations plainly. | Pilot size, language mediation, project-specific labels, burden, adjudication dependence, no memo baseline. | None or Table 8: limitations and next evidence. | 600 | Too defensive or too brief. |
| 11. Conclusion | Re-state contribution and next empirical step. | Summary of claim scale. | None. | 300 | Inflated closing. |

## Figures And Tables

Main article:

1. **TRIM evidence-to-function architecture.** Evidence nodes -> anchor -> threshold-rationale relation -> function.
2. **One complete annotation pathway.** Use `MAC_1_3` or `ZZ_XI_4` from demo/pilot.
3. **Two pathways leading to same or related function.** Use a pilot-adjudicated substantive variation case if text can be shown without overloading.
4. **v0.2.0 field-level agreement chart.** Exact and compatible agreement where applicable.
5. **Disagreement taxonomy.** Raw disagreement preserved, then categorized.
6. **v0.2.0 to v0.2.1 revision trace.** Pilot issue -> revision -> retest measure.
7. **Retest workflow.** Package -> independent coding -> validation -> comparison -> adjudication -> revision decision.

Supplement:

- Full codebook and manuals.
- Full retest manifest and source packet.
- Evidence-overlap matrix after retest.
- Case-level pathway comparison after retest.
- Validation and leakage-test outputs.
- Question-log summary after retest.

## Worked Examples

Use in main article:

- **Same function / different pathway:** `MAC_1_3` is promising because partial confirmation can be read through warrant attribution or warrant relation.
- **Codebook ambiguity:** function versus actor uptake from `ZZ_MIN_1` or `JC_CALPURNIA_DECIUS`.
- **Local speech versus outer frame:** `GROVE_TAKEHIRO` or retest `ANT_GUARD_REPORT` / `OED_MESSENGER_SHEPHERD`.
- **Primary versus contextual evidence:** retest `OTH_HANDKERCHIEF_CHAIN` or `HAM_PLAY_REACTION`.

Use in supplement:

- All 12 retest cases with design roles.
- Full pilot-adjudication detail.
- Translation-mediated language-access examples.
- All alternative-signature cases.

## Draft Skeleton

### Title

Beyond Final-Label Agreement: Evidence-to-Function Pathways in Interpretive Annotation

### Abstract

[Use the primary abstract from `TRIM_title_abstract_options.md`; update the last two sentences after v0.2.1 retest.]

### Keywords

interpretive annotation; digital humanities methods; computational literary studies; intercoder disagreement; qualitative coding; evidence modelling; auditability

### 1. Introduction: The Missing Middle In Interpretive Annotation

Paragraph 1 topic sentence: Interpretive annotation commonly converts complex textual reasoning into a final code, category, or label.

Evidence/citations: qualitative coding literature; DH annotation; CLS operationalization.

Paragraph 2 topic sentence: Final labels are necessary for comparison, but they are too thin to show how evidence became function.

Evidence/citations: v0.2.0 asymmetry; Cohen 1960; Krippendorff 2018; Campbell et al. 2013.

Paragraph 3 topic sentence: TRIM proposes a structured middle layer between categorical annotation and unrestricted memoing.

Figure callout: Figure 1.

Paragraph 4 topic sentence: The article's claim is methodological and limited: TRIM improves reviewability, not interpretive truth.

Table callout: Table 1.

### 2. Why Final Labels Are Insufficient

Paragraph 1 topic sentence: Agreement on the final label can mask different evidential selections and rationales.

Paragraph 2 topic sentence: Disagreement on the final label can arise from several causes that should not be collapsed.

Paragraph 3 topic sentence: The v0.2.0 pilot demonstrates this problem at small scale.

Evidence: field agreement table from pilot.

Figure callout: Figure 4.

### 3. Related Approaches And The Methodological Gap

Paragraph 1 topic sentence: Qualitative coding already offers codebooks, memos, reliability checks, and adjudication.

Paragraph 2 topic sentence: DH annotation platforms make textual spans and categories visible, but do not usually standardize the evidence-to-function route.

Paragraph 3 topic sentence: Argumentation and provenance models show how evidence-to-claim and process trails can be represented, but TRIM adapts this to interpretive function.

Paragraph 4 topic sentence: TRIM's gap is therefore narrow: it makes pathway variation itself comparable.

Table callout: Table 3.

### 4. TRIM Architecture

Paragraph 1 topic sentence: A TRIM record links selected evidence to a project-defined function through an analytic anchor and threshold-rationale relation.

Paragraph 2 topic sentence: The six signature fields locate the threshold, mechanism, support, discourse level, temporal orientation, and coder uncertainty.

Paragraph 3 topic sentence: `alternative_signature` records a complete competing pathway only when it remains defensible.

Paragraph 4 topic sentence: The software layer validates structure and produces comparison objects but does not judge interpretation.

Figure callouts: Figures 2 and 3.

### 5. Pilot Design

Paragraph 1 topic sentence: The v0.2.0 pilot was designed as a usability and method-development pilot, not a final reliability study.

Paragraph 2 topic sentence: The ten cases deliberately mixed divination, prophecy, and testimony across languages and traditions.

Paragraph 3 topic sentence: The pilot used independent coding, locked submissions, post-pilot interview, and adjudication.

Table callout: Table 4.

### 6. What The First Pilot Revealed

Paragraph 1 topic sentence: Completion was successful, but the empty question log proved misleading.

Paragraph 2 topic sentence: Field-level agreement showed that final function was more stable than several pathway fields.

Paragraph 3 topic sentence: Evidence selection failed as a discriminative task when one coder selected all segments.

Paragraph 4 topic sentence: Several disagreements were not coder error but boundary ambiguity or substantive pathway variation.

Paragraph 5 topic sentence: Language mediation and shared-context ambiguity constrained the pilot's claims.

Table callout: Table 5.

### 7. Pilot-Informed Revision

Paragraph 1 topic sentence: v0.2.1 keeps the v0.2.0 record locked and revises prospectively.

Paragraph 2 topic sentence: The revised codebook clarifies actor uptake, context inference, warrant attribution/relation, operation/perspective, and discourse level.

Paragraph 3 topic sentence: The revised schema adds primary/context evidence segments, language access, shared-context registry, and question-log validation.

Paragraph 4 topic sentence: The coder package includes leakage and semantic-steering tests.

Figure callout: Figure 5.

### 8. Prospective Retest

Paragraph 1 topic sentence: The v0.2.1 retest uses 12 out-of-sample public-domain or public-domain-translation cases.

Paragraph 2 topic sentence: The corpus deliberately includes anchor, boundary-stress, shared-context, evidence-selection, and no-fit/distractor cases.

Paragraph 3 topic sentence: The planned analysis reports completion, field-specific agreement, evidence overlap, question logs, pathway comparison, adjudication categories, and strata.

Placeholder: [INSERT V0.2.1 RETEST RESULT]

Table callout: Table 7.

### 9. Discussion: Disagreement As Structure Rather Than Noise

Paragraph 1 topic sentence: TRIM's main payoff is not higher agreement by itself, but a clearer account of what disagreement is about.

Paragraph 2 topic sentence: Structured alternatives allow interpretive plurality to remain visible without abandoning review.

Paragraph 3 topic sentence: The method is most useful for projects where interpretive categories are recurrent, contested, and worth auditing.

Paragraph 4 topic sentence: TRIM should be understood as constrained transparency, not positivist reduction.

### 10. Limitations

Paragraph 1 topic sentence: The pilot is too small to validate reliability.

Paragraph 2 topic sentence: The current function list is project-specific.

Paragraph 3 topic sentence: Translation-mediated cases cannot support cross-language validity claims.

Paragraph 4 topic sentence: The method is burdensome and likely inappropriate for lightweight annotation.

Paragraph 5 topic sentence: Adjudication categories themselves require further validation.

### 11. Conclusion

Paragraph 1 topic sentence: Interpretive annotation needs records that show not only what label was chosen, but how evidence was converted into that label.

Paragraph 2 topic sentence: TRIM offers one pathway architecture for that purpose and a retest design for evaluating it prospectively.

Final sentence: Future claims about reliability, language validity, and domain generality depend on completing the v0.2.1 retest and extending the design beyond the current project.
