# Human-LLM Friction-Locus Analysis Plan

Status: analysis plan only. This document defines planned comparisons and
outputs. It contains no empirical findings.

## Comparison sets

The planned study will compare:

- human pre-exposure records against the primary locked AI run;
- primary locked AI runs against repeated stability runs;
- AI outputs across instruction-ablation conditions;
- final-label relations against procedural-record relations.

No author record is treated as a truth verdict, and no model record is treated
as an answer key. Agreement and disagreement are descriptive properties of
locked records under a stated protocol.

## Analysis hierarchy

Primary analyses:

1. Final-label correspondence.
2. Evidence-selection overlap.
3. Friction-locus correspondence.
4. Counterfactual-answer divergence.
5. Decision-path divergence.
6. Uncertainty relation.
7. Alternative-pathway relation.
8. Same-label/procedure-different cases.
9. Different-label/pathway-shared cases.
10. Predicted versus observed confusion.

Secondary analyses:

1. Model stability.
2. Instruction ablation.
3. Descriptive cross-record agreement coefficients.
4. Qualitative case studies selected by frozen rules.

Raw counts, proportions, confusion structures, and case-level decomposition are primary. If reported, Cohen's kappa, Krippendorff's alpha, and Gwet's AC1 describe correspondence between one human-record condition and one model-record condition across cases. They do not estimate human intercoder reliability, do not validate the ontology, and do not make the researcher's record a gold standard.

Raw agreement remains the most transparent agreement summary. Gwet's AC1 may be reported as a secondary cross-condition summary under sparse or prevalence-imbalanced categories, with Cohen's kappa and Krippendorff's alpha treated as sensitivity/descriptive checks. No coefficient is primary evidence of ontological validity.

## Predicted versus observed confusion

The pre-analysis table at `docs/studies/predicted_confusions.csv` records
manual-derived confusable pairs. The table includes:

- category pair;
- predicted source of confusion;
- counterfactual test intended to distinguish them;
- expected direction of error;
- whether the pair has prior positive examples;
- whether the prediction is symmetric or directional.

Observed confusion matrices will be created for:

- human-AI confusions;
- AI self-instability confusions across repeated runs;
- instruction-condition confusions;
- unexpected confusions not predicted by the manual.

Observed confusions will be interpreted with these non-exclusive categories:

- anticipated boundary pressure;
- possible manual ambiguity;
- possible case ambiguity;
- possible model instability;
- unanticipated blind spot.

Predicted confusion is not treated as ontological or irreducible by default.

## Descriptive agreement statistics

The analysis will not rely on Cohen's kappa alone and will not describe coefficients as human coding reliability. Planned reporting includes:

- raw agreement;
- per-category support;
- confusion matrix;
- Cohen's kappa;
- Krippendorff's alpha;
- Gwet's AC1;
- macro and micro summaries where appropriate;
- prevalence and bias indices if useful;
- bootstrap confidence intervals if sample size permits;
- explicit reporting of category absence as not observed.

Zero-frequency categories cannot be meaningfully evaluated with per-category
agreement coefficients. The study will not manufacture positive examples to
stabilize statistics.

Minimum support rules:

- Per-category coefficients require at least five observations in the relevant
  category and at least two coders or record-producing conditions in the
  comparison set.
- Bootstrap confidence intervals require enough nonzero support to resample
  without degenerating into all-zero or all-one samples; otherwise report counts
  and exact proportions only.
- Zero-support and near-zero-support categories are reported as not observed or
  insufficiently supported.
- Sparse categories may be included in macro summaries only with an explicit
  support table.

## Procedural disagreement metrics

For each researcher-model record pair, compute:

- final-label exact match;
- friction-locus exact match;
- evidence Jaccard overlap;
- counterfactual-test agreement rate;
- decision-path exact or partial overlap;
- uncertainty relation;
- alternative-pathway relation;
- escalation/governance relation.

For same-label pairs, flag whether evidence, warrants, counterfactual answers,
uncertainty, alternatives, or escalation differ. For different-label pairs,
flag whether evidence, alternatives, decision paths, or pathway structures
substantially overlap.

## Instruction-ablation analysis

Instruction conditions use a shared structured annotation baseline with
increasing levels of interpretive guidance:

- A: label names and short definitions only;
- B: concise decision rules;
- C: full manual including counterfactual tests and confusable-with guidance.

Planned outcomes:

- evidence-selection overlap and divergence;
- counterfactual-test completion and consistency;
- friction_locus assignment distribution;
- uncertainty distribution;
- alternative-pathway retention;
- rationale structure and decision-path completeness;
- escalation rate.

The ablation does not test training-data contamination. Similar outputs across
conditions may have multiple explanations and must be reported cautiously.
It is secondary and exploratory; it does not by itself establish that the full
manual causes a particular model behavior.

## Stability analysis

For this freeze package, the planned stability interpretation is three additional independent Condition C runs per selected case beyond the primary locked run. The primary run is not counted as a stability run. If the blocked manual/model/right-status issues are later resolved, preserve the following stability rules:

- preserve every raw output and parsed record;
- compute self-consistency rate for primary label and friction_locus;
- compute label entropy;
- compute friction-locus entropy where support permits;
- report the full output distribution;
- report modal label only as a secondary summary;
- never replace the primary locked run with a majority vote.

Repeated runs must use isolated sessions. The run manifest records temperature,
top_p if available, seed if supported, tool and browsing availability, system
prompt status, provider-side version limitations, execution date, region if
relevant, retry policy, rate-limit failure handling, and technical failure
status. Provider-side model updates and stochastic decoding limit exact
reproducibility and must be reported.

## Main figures and tables

Figure 1: Procedural disagreement pipeline.

Figure 2: Predicted versus observed confusion network.

Figure 3: Final-label agreement versus procedural disagreement.

Table 1: Sample composition.

Table 2: Category support and agreement statistics.

Table 3: Predicted and observed confusable pairs.

Table 4: Cases with same final label but divergent interpretive procedure.

Table 5: Cases with different final labels but shared pathway structure.

Table 6: Instruction-ablation effects.

Table 7: Model self-consistency and entropy.

## Qualitative case studies

Select 2-4 qualitative case studies after descriptive analysis using this
deterministic selection algorithm:

1. Select the same-final-label case with greatest procedural divergence.
2. Select the different-final-label case with greatest pathway/evidence overlap.
3. Select one case from the most frequent predicted confusion pair.
4. Select one case from the most consequential unexpected confusion, where
   consequence is defined before coding as affecting escalation status,
   alternative-pathway retention, or inclusion in a primary-analysis table.

Tie-breaking:

1. Prefer the case with more complete counterfactual-test data.
2. If still tied, prefer the case with higher evidence-union count.
3. If still tied, prefer the earliest case in the frozen randomized order.

Case studies must not be selected for rhetorical vividness, narrative drama, or
whether they support a preferred conclusion. They must not be used to imply
general model behavior or truth of one interpretation.

## Demonstration-study success criteria

The study counts as substantively successful only if it reveals at least one
finding that would be invisible in a final-label-only analysis, such as:

- same label, different evidence and warrants;
- different labels, shared alternatives and pathway structure;
- predicted confusion confirmed at a specific procedural boundary;
- unexpected confusion revealing a manual blind spot;
- high final-label agreement masking low procedural agreement;
- lower alternative-pathway retention in AI records;
- instruction condition changing procedural compliance without changing final
  labels.

The study does not pre-commit to any substantive result.

## Failure criteria

The demonstration may fail if:

- researcher-specific interpretations dominate results;
- no evidence beyond final-label comparison is produced;
- procedural fields cannot be applied consistently;
- model output is unstable or unparseable;
- categories collapse empirically;
- manual distinctions are not teachable;
- the study cannot distinguish model effects from case-selection effects;
- sample construction is too contaminated or biased;
- human familiarity dominates the transfer set;
- the lack of a second human coder prevents any claim about human reproducibility.

A null or negative result is publishable as a method limitation.

## Reporting boundaries

Reports must state that the study is a small-N demonstration of procedural
representation, not empirical validation of the whole framework. Reports must
not claim that the eight friction_locus categories are natural kinds, that the researcher record is a gold standard, that a model output is a truth verdict, that the study estimates human intercoder reliability, or that observed instability generalizes beyond the study conditions.

The study is primarily descriptive. It does not claim broad confirmatory
hypothesis testing. Ablation and stability analyses are secondary and
exploratory. Multiple metrics do not constitute multiple independent
confirmations. No model-general or domain-general inference is made. Findings
are tied to the frozen cases, model, prompt, manual, and execution dates.
