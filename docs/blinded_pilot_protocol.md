# Blinded Pilot Protocol

## Purpose

This ten-case pilot evaluates whether a second coder can independently apply
TRIM and reproduce the comparative patterns documented in
`docs/substantive_demo_interpretations.md`.

It has two linked aims:

1. measure agreement field by field;
2. test whether the current substantive comparisons reappear under independent
   coding.

A single aggregate statistic is insufficient because it cannot show whether the
specific comparative findings TRIM is designed to produce are reproduced.

## Pilot Sample

The sample contains:

- four *Zuo zhuan* divination cases;
- three *Macbeth* prophecy cases;
- three *In a Grove* testimony cases.

Together they cover five demonstrated `friction_locus` values, simple and
compound mechanisms, low-to-high uncertainty, and one contested primary-coder
case. Results should be reported as pilot diagnostics with case-level analysis.

## Blinded Materials

The second coder receives only:

- `data/blinded_pilot_source_packet.md`;
- `data/blinded_pilot_case_manifest.csv`;
- `data/blinded_pilot_coding_template.csv`;
- the current codebook and coding manuals.

The second coder does not receive the primary coder's:

- evidence decomposition or anchor labels;
- function labels;
- friction loci or rationale mechanisms;
- support, discourse, temporal, or uncertainty fields;
- alternative signatures or rationale notes;
- generated comparison outputs;
- substantive demonstration document before coding is locked.

The source packet contains original or public-domain source text, neutral
location notes, and fresh close paraphrases for the Classical Chinese passages.
It contains no primary-coder TRIM labels.

The case order should be randomized before delivery. Archive the randomized
order and the exact commit SHA of all pilot files.

## Coder Preparation

Read:

- `docs/TRIM_codebook_v0_2_0.md`;
- `docs/TRIM_Coding_Manual_v0_2_friction_locus_final.md`;
- `docs/TRIM_Coding_Manual_v0_2_rationale_mechanism.md`;
- `docs/segmentation_workflow.md`;
- `docs/second_coder_onboarding.md`.

## Coding Procedure

### Round 1: evidence and dominant threshold

Complete:

- `evidence_anchor`;
- `evidence_nodes`;
- `anchor_node`;
- `function_label`;
- `friction_locus`;
- `rationale_note`;
- `uncertainty_flag`.

Apply the counterfactual, proximity, and explanatory-sufficiency tests when more
than one locus appears plausible.

### Round 2: full signature

Without viewing primary values, complete:

- `rationale_mechanism`;
- `epistemic_support`;
- `discourse_level`;
- `temporal_orientation`;
- `alternative_signature` when a competing pathway remains viable.

Compound mechanisms preserve primary-to-secondary order.

### Lock point

Timestamp and preserve the completed file before comparison. Generate initial
metrics and disagreement tables from this locked version.

### Adjudication

Begin adjudication only after pre-adjudication outputs are archived. For each
disagreement, record:

- the field or upstream choice where divergence began;
- the rule used by each coder;
- whether the difference reflects ambiguity, manual wording, data entry, or a
  genuinely plural reading;
- the adjudicated value while retaining both original values.

## Agreement Analysis

### Categorical fields

For `friction_locus`, `epistemic_support`, `discourse_level`,
`temporal_orientation`, and `uncertainty_flag`, report:

- exact agreement count and proportion;
- Cohen's kappa where computable;
- the complete case-level disagreement table.

With ten cases, kappa is descriptive and potentially unstable. Raw agreement
and disagreement location remain central.

### Compound mechanisms

For `rationale_mechanism`, report:

- exact-set agreement;
- primary-mechanism agreement;
- any-overlap agreement;
- mean Jaccard overlap;
- ordering differences where both coders selected the same values.

### Constructed and free-text fields

Review `evidence_anchor`, `evidence_nodes`, `anchor_node`, `function_label`, and
`rationale_note` through structured comparison rather than raw string identity:

- evidence-span overlap;
- selection of the same textual event;
- equivalent or divergent anchor construction;
- substantive equivalence of function labels;
- coherence between rationale and selected signature.

## Pre-specified Comparative Tests

### Test A: *Macbeth* locus migration

Cases: `MAC_1_3`, `MAC_4_1`, `MAC_5_8`.

Full replication requires the sequence:

1. `warrant_attribution`;
2. `operation_function`;
3. `temporal_layering`.

Partial replication requires at least two matching assignments and movement
across more than one locus.

### Test B: shared locus, divergent trajectories

Cases: `ZZ_XI_4`, `GROVE_TAKEHIRO`.

Full replication requires:

- `warrant_relation` for both;
- different mechanisms;
- extension for `ZZ_XI_4`;
- contradiction or suspension for `GROVE_TAKEHIRO`.

Report locus replication and mechanism differentiation separately.

### Test C: shared threshold, divergent conversion

Cases: `ZZ_MIN_1`, `MAC_1_3`.

Full replication requires:

- `warrant_attribution` for both;
- prospective orientation for both;
- different mechanisms reflecting stabilization/projection versus
  authorization/reframing.

Report shared-threshold replication and conversion differentiation separately.

## Decision Rules

Proceed to a larger out-of-sample study when:

- the packet can be used without intervention;
- most records are complete and valid;
- disagreements are traceable to identifiable boundaries;
- at least two comparative tests show full or substantively clear partial
  replication;
- no core field repeatedly fails because its definition is unintelligible.

Revise manuals before expansion when the same distinction repeatedly causes
cross-case disagreement, locus is confused with mechanism or support, compound
ordering is unstable, or uncertainty and alternatives are applied
incompatibly.

Schema revision requires repeated evidence of one structural problem across
cases. One difficult passage is not enough.

## Archive

Preserve:

- source-packet commit SHA and checksum;
- randomized order;
- blank template version;
- locked independent coding file;
- validation report;
- field-level agreement table;
- compound-mechanism metrics;
- disagreement table;
- comparative replication results;
- adjudication log;
- post-adjudication file, clearly separated from original coding.

## Reporting

Describe this as a blinded ten-case pilot. Keep four outcomes distinct:

- schema validity;
- coder agreement;
- replication of comparative patterns;
- adjudicated consensus.
