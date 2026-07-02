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

## Reliability and descriptive statistics

The analysis will not rely on Cohen's kappa alone. Planned reporting includes:

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

Zero-frequency categories cannot be meaningfully evaluated for reliability.
The study will not manufacture positive examples to stabilize statistics.

## Procedural disagreement metrics

For each human-AI pair, compute:

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

Instruction conditions:

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

## Stability analysis

For 3-5 repeated independent model runs per case:

- preserve every raw output and parsed record;
- compute self-consistency rate for primary label and friction_locus;
- compute label entropy;
- compute friction-locus entropy where support permits;
- report the full output distribution;
- report modal label only as a secondary summary;
- never replace the primary locked run with a majority vote.

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

Select 2-4 qualitative case studies after descriptive analysis. Candidate case
study types:

- same final label with divergent evidence and warrants;
- different final labels with shared alternatives and pathway structure;
- predicted confusion confirmed at a specific procedural boundary;
- unexpected confusion that suggests a manual blind spot.

Case studies must not be selected to imply general model behavior or truth of
one interpretation.

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

- procedural fields are too unreliable to interpret;
- outputs cannot be parsed consistently;
- repeated model runs are too unstable;
- categories collapse empirically;
- manual distinctions are not teachable;
- no additional information appears beyond final labels;
- sample construction is too contaminated or biased;
- human familiarity dominates the transfer set.

A null or negative result is publishable as a method limitation.

## Reporting boundaries

Reports must state that the study is a small-N demonstration of procedural
representation, not empirical validation of the whole framework. Reports must
not claim that the eight friction_locus categories are natural kinds, that one
annotator is a gold standard, that a model output is a truth verdict, or that
observed instability generalizes beyond the study conditions.
