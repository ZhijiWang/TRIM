# Blinded Pilot Protocol

## Purpose

This ten-case pilot evaluates two things at once:

1. field-level agreement across independently completed TRIM annotations;
2. replication of the three comparative patterns developed in
   `docs/substantive_demo_interpretations.md`.

The second aim keeps reliability tied to the findings TRIM is designed to
produce. Agreement statistics describe field stability; the comparative tests
show whether the method's substantive patterns survive independent coding.

## Sample

The sample contains:

- four *Zuo zhuan* divination cases;
- three *Macbeth* prophecy cases;
- three *In a Grove* testimony cases.

Together they cover five demonstrated `friction_locus` values, simple and
compound mechanisms, three uncertainty levels, and one contested primary
annotation. Results are reported as pilot evidence with case-level analysis.

## Coding Environment

The coder receives:

- `data/blinded_pilot_source_packet.md`;
- `data/blinded_pilot_case_manifest.csv`;
- `data/blinded_pilot_coding_template.csv`;
- the current codebook and coding manuals.

Primary annotations, generated comparison outputs, and substantive demonstration
interpretations enter the workflow after the independent file has been
preserved. This sequence keeps the coding stage separate from comparison and
adjudication.

The source packet provides original or public-domain text, neutral location
notes, and fresh close paraphrases for the Classical Chinese passages. The case
order is randomized before delivery, and the exact commit SHA of every pilot
file is archived.

## Coder Preparation

Read:

- `docs/TRIM_codebook_v0_2_0.md`;
- `docs/TRIM_Coding_Manual_v0_2_friction_locus_final.md`;
- `docs/TRIM_Coding_Manual_v0_2_rationale_mechanism.md`;
- `docs/segmentation_workflow.md`;
- `docs/second_coder_onboarding.md`.

The pilot report records the coder's disciplinary background, language
competence, and familiarity with the three source traditions. The Classical
Chinese paraphrases also receive an independent neutrality check before the
pilot is circulated.

## Coding Sequence

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

Complete:

- `rationale_mechanism`;
- `epistemic_support`;
- `discourse_level`;
- `temporal_orientation`;
- `alternative_signature` when a competing pathway remains viable.

Compound mechanisms preserve primary-to-secondary order.

### Preservation point

Timestamp and archive the completed file before comparison. Initial agreement
measures and disagreement tables are generated from this preserved version.

### Adjudication

For each disagreement, record:

- the first field or upstream choice where divergence appears;
- the rule used by each coder;
- the source passage supporting each decision;
- the category of disagreement: manual wording, data entry, field boundary, or
  genuinely plural reading;
- the adjudicated value alongside both original values.

Plural-reading disagreements receive a separate count. They remain visible in
the case analysis and leave the pre-adjudication agreement rate unchanged.

## Agreement Analysis

### Categorical fields

For `friction_locus`, `epistemic_support`, `discourse_level`,
`temporal_orientation`, and `uncertainty_flag`, report:

- exact agreement count and proportion;
- Cohen's kappa where computable;
- the complete case-level disagreement table.

With ten cases, kappa functions as a descriptive statistic. Raw agreement and
the location of disagreement remain central.

### Compound mechanisms

For `rationale_mechanism`, report:

- exact-set agreement;
- primary-mechanism agreement;
- any-overlap agreement;
- mean Jaccard overlap;
- ordering differences where both coders selected the same values.

### Constructed and free-text fields

Review `evidence_anchor`, `evidence_nodes`, `anchor_node`, `function_label`, and
`rationale_note` through structured comparison:

- evidence-span overlap;
- selection of the same textual event;
- equivalent or divergent anchor construction;
- substantive equivalence of function labels;
- coherence between rationale and selected signature.

## Optional Double-Layer Construct-Validity Check

For Classical Chinese cases, an optional companion check records whether the
English close paraphrase preserves the same evidence-to-function threshold as
the source-language reading:

1. a source-language-competent coder annotates the original passage;
2. a second coder annotates the English close paraphrase without seeing the
   source-layer result;
3. both records are preserved before comparison;
4. compare `friction_locus` and `rationale_mechanism`;
5. assign `cross_layer_relation` in
   `data/cross_language_validity_template.csv`;
6. examine any relocation in relation to syntax, explicitness, agency, temporal
   marking, warrant structure, or another visible mediation change.

Plural-reading disagreement is counted separately from cross-layer mediation
effects. Plural-reading cases leave the pre-adjudication agreement rate intact
and enter the qualitative disagreement report.

Pilot reporting records coder disciplinary background and language competence.
The Classical Chinese paraphrases are researcher-authored access materials.
Source-language claims remain anchored in original-language reading until this
double-layer coding has been completed.

## Pre-Specified Comparative Tests

### Test A: *Macbeth* locus migration

Cases: `MAC_1_3`, `MAC_4_1`, `MAC_5_8`.

Full replication follows this sequence:

1. `warrant_attribution`;
2. `operation_function`;
3. `temporal_layering`.

Partial replication records at least two matching assignments together with
movement across more than one locus.

### Test B: shared locus, divergent trajectories

Cases: `ZZ_XI_4`, `GROVE_TAKEHIRO`.

Full replication combines:

- `warrant_relation` for both cases;
- an extending mechanism for `ZZ_XI_4`;
- a contradicting or suspending mechanism for `GROVE_TAKEHIRO`.

Locus replication and mechanism differentiation are reported separately.

### Test C: shared threshold, divergent conversion

Cases: `ZZ_MIN_1`, `MAC_1_3`.

Full replication combines:

- `warrant_attribution` for both cases;
- prospective orientation for both cases;
- stabilization or projection in `ZZ_MIN_1`;
- authorization or reframing in `MAC_1_3`.

Shared-threshold replication and conversion differentiation are reported
separately.

## Decision Rules

A larger out-of-sample study becomes appropriate when the packet is usable,
records are complete, disagreements can be traced to identifiable boundaries,
and at least two comparative tests show full or substantively clear partial
replication.

Manual revision becomes appropriate when the same distinction repeatedly
produces cross-case disagreement, especially around locus, mechanism, support,
compound order, uncertainty, or alternative pathways.

Schema revision requires repeated evidence of one structural problem across
cases. A difficult passage remains a case-level result until the same problem
recurs.

## Archive

Preserve:

- source-packet commit SHA and checksum;
- randomized order;
- blank template version;
- independent coding file;
- validation report;
- field-level agreement table;
- compound-mechanism metrics;
- disagreement table;
- comparative replication results;
- adjudication log;
- post-adjudication file.

## Reporting

Report four outcomes separately:

- schema validity;
- coder agreement;
- replication of comparative patterns;
- adjudicated consensus.
