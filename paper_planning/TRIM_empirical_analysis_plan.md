# TRIM Empirical Analysis Plan

This plan assumes the human v0.2.2 retest is completed with at least two
independent human coders, locked submissions, locked question logs, and
language-access forms. The v0.2.1 AI dry run is a protocol stress test only and
must not be pooled with human v0.2.2 retest data.

## Data Preservation

Before analysis, archive:

- coder-facing ZIP and checksum;
- each locked coding sheet;
- each question log;
- each language-access form;
- validation reports;
- manifest and shared-context registry;
- source-packet version;
- package version and SHA-256 used by each coder;
- adjudication notes;
- analysis scripts and outputs.

Do not overwrite raw coder values with adjudicated values.

## Descriptive Completion And Usability

Report:

- completion status by coder and case;
- missing required fields by field and coder;
- validation errors and warnings;
- completion time if collected;
- question-log frequency per coder and per case;
- questions by type: definitional, interpretive, procedural, packet-level;
- questions by field: function label, primary evidence, context evidence, friction locus, rationale mechanism, epistemic support, discourse level, temporality, uncertainty, alternative signature;
- blocking versus nonblocking questions;
- did-question-change-code rate;
- requires-manual-revision counts;
- protocol deviations;
- language-access condition by coder and case.

Key outputs:

- table: completion and validation summary;
- chart: questions by field;
- table: question log with provisional resolution categories.

## Agreement

Report field-specific results. Do not collapse into one global score.

Required fields:

- `function_label` exact agreement;
- `friction_locus` exact agreement;
- `rationale_mechanism` exact set agreement, primary-value agreement, compatible single/compound agreement, any-overlap agreement, mean Jaccard;
- `epistemic_support` exact set agreement, primary-value agreement, compatible single/compound agreement, any-overlap agreement, mean Jaccard;
- `discourse_level` exact agreement;
- `temporal_orientation` exact agreement;
- `uncertainty_flag` exact agreement;
- `alternative_signature` presence/absence agreement and, where both present, signature-field comparison.

Statistics:

- Simple percent agreement is required.
- Cohen's kappa may be reported descriptively only if exactly two coders, adequate category variation, and enough comparable cases exist. With 12 cases and sparse categories, it should be interpreted cautiously or omitted.
- Krippendorff's alpha is more flexible for multiple coders and missingness, but the sample is likely too small for strong claims.
- Gwet's AC1 can reduce prevalence problems but may look opportunistic if introduced without a clear preregistered reason.
- Best first-reporting approach: descriptive field-level agreement plus
  confidence-aware narrative. Chance-corrected coefficients may appear in
  supplementary material with strong caveats, but one global kappa or alpha
  should not be the headline result.

## Evidence Selection

Report:

- exact primary segment-set agreement;
- primary segment Jaccard overlap;
- context segment Jaccard overlap;
- cross-role overlap where one coder marks a segment primary and another marks it contextual;
- all-segment-selection rate;
- primary segment-count distribution;
- context segment-count distribution;
- unknown/unpermitted segment validation errors;
- local primary evidence compliance;
- shared-context segment use.

Key interpretation:

- Success is not maximum evidence overlap. Success is discriminative, reviewable evidence selection that supports later disagreement diagnosis.

## Pathway Comparison

Classify each coder-pair/case relation:

- same function / same signature;
- same function / different signature;
- different function / substantially shared pathway;
- different function / partially shared pathway;
- different function / different pathway;
- no-fit disagreement;
- same evidence / different conversion;
- different evidence / same function;
- complete alternative recorded by one coder only.

For each case, identify the first divergence point:

1. evidence selection;
2. anchor;
3. function label;
4. friction locus;
5. rationale mechanism;
6. epistemic support;
7. discourse level;
8. temporal orientation;
9. uncertainty;
10. alternative signature.

## Question-Log Analysis

For each question:

- type;
- field implicated;
- blocking/nonblocking;
- provisional resolution;
- whether code changed;
- whether manual revision requested;
- whether packet revision requested;
- whether question predicts disagreement.

Report:

- total questions per coder;
- questions per case;
- field-specific question rates;
- questions that led to code change;
- questions later classified as codebook ambiguity or insufficient evidence.

## Adjudication Categories

Preserve raw disagreement and classify separately:

- substantive pathway variation;
- codebook ambiguity;
- coder error;
- insufficient evidence;
- compatible difference;
- unresolved legitimate alternatives;
- near-complete alignment.

For each category, provide:

- definition;
- count;
- representative case;
- whether it requires manual revision, packet revision, schema revision, or no revision.

Do not report adjudicated values as if they were original coder agreement.

## Stratification

Use cautiously because the sample is small.

Possible strata:

- direct-language versus translation-mediated;
- local passage versus supplied related cases/shared narrative field/complete work;
- anchor versus boundary-stress versus distractor/no-fit cases;
- source family;
- case complexity by segment count;
- shared-context required versus not required.

Treat strata as diagnostic patterns, not inferential proof.

## Optional Memo-Only Baseline

Not necessary for Paper 1, but valuable for Paper 2 if resources allow.

Design:

- Group A uses function label plus free-text memo.
- Group B uses TRIM.
- Independent reviewers attempt to identify evidence, pathway, disagreement type, and adjudication needs.

Compare:

- ability to locate disagreement;
- ability to reconstruct evidence;
- ability to classify disagreement;
- adjudication time;
- reviewer confidence;
- missing rationale elements.

Use this only if adding a baseline will not delay core retest completion.

## Minimum Reportable Retest Package

At minimum, publish:

- anonymized locked coder sheets;
- question logs;
- language-access forms;
- manifest and registry;
- validation outputs;
- field-level agreement tables;
- evidence-overlap tables;
- adjudication-category table;
- package checksum;
- analysis script.
