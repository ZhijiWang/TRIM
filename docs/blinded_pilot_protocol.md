# Blinded Pilot Protocol

## Purpose

This pilot tests whether a second coder can independently reproduce the field
assignments that support TRIM's current substantive demonstrations. It is a
small, diagnostic study of manual usability, field boundaries, and comparative
replication. The ten demonstration cases form the pilot sample.

The pilot has two linked aims:

1. evaluate agreement field by field;
2. test whether the three comparative patterns documented in
   `docs/substantive_demo_interpretations.md` reappear under independent coding.

The second aim is essential. A single aggregate agreement statistic cannot show
whether the findings TRIM is designed to produce are actually reproduced.

## Pilot Sample

The sample contains all ten demonstration cases:

- four *Zuo zhuan* divination cases;
- three *Macbeth* prophecy cases;
- three *In a Grove* testimony cases.

Using all ten preserves the current range of:

- source traditions;
- low, medium, and high uncertainty;
- `warrant_attribution`, `warrant_relation`, `operation_function`,
  `perspective_assignment`, and `temporal_layering`;
- simple and compound rationale mechanisms;
- one explicitly contested primary-coder case.

The sample is intentionally small. Results should be reported as pilot evidence
with case-level disagreement analysis.

## Blinding

The second coder receives:

- the source packet or source passages for each case;
- stable `case_id`, source, case label, language, and case type;
- the current codebook and coding manuals;
- `data/blinded_pilot_coding_template.csv`.

The second coder does not receive:

- the primary coder's evidence decomposition;
- `anchor_node`;
- `function_label`;
- `friction_locus`;
- `rationale_mechanism`;
- `epistemic_support`;
- `discourse_level`;
- `temporal_orientation`;
- `uncertainty_flag`;
- `alternative_signature`;
- primary-coder rationale notes;
- generated comparison tables;
- `docs/substantive_demo_interpretations.md` before coding is locked.

The case order should be randomized before the packet is sent. The random order
and the exact source packet version should be archived with the returned coding
file.

## Materials

The coder should read:

- `docs/TRIM_codebook_v0_2_0.md`;
- `docs/TRIM_Coding_Manual_v0_2_friction_locus_final.md`;
- `docs/TRIM_Coding_Manual_v0_2_rationale_mechanism.md`;
- `docs/segmentation_workflow.md`;
- `docs/second_coder_onboarding.md`.

The coder should work from a clean copy of:

- `data/blinded_pilot_case_manifest.csv`;
- `data/blinded_pilot_coding_template.csv`;
- a separately prepared source packet containing the relevant passages and any
  translations needed for independent interpretation.

The manifest is an administrative key. It contains no primary-coder signature
fields.

## Coding Procedure

### Round 1: Evidence and dominant threshold

For every case, the coder completes:

- `evidence_anchor`;
- `evidence_nodes`;
- `anchor_node`;
- `function_label`;
- `friction_locus`;
- `rationale_note`;
- `uncertainty_flag`.

The coder applies the counterfactual, proximity, and explanatory-sufficiency
tests in the friction-locus manual when more than one locus appears plausible.

### Round 2: Full signature

Without seeing the primary coder's values, the coder completes:

- `rationale_mechanism`;
- `epistemic_support`;
- `discourse_level`;
- `temporal_orientation`;
- `alternative_signature` when a competing pathway remains viable.

Compound mechanisms should preserve primary-to-secondary order.

### Lock point

The completed file is timestamped and preserved before any comparison or
adjudication. Initial metrics and disagreement tables are generated from this
locked file.

### Adjudication

Adjudication begins only after initial outputs are archived. For each disagreement,
record:

- whether the difference originates in evidence selection, anchor construction,
  function assignment, locus selection, mechanism, support, discourse level,
  temporality, uncertainty, or compound ordering;
- which manual rule was applied by each coder;
- whether the disagreement suggests a codebook clarification, a genuinely
  plural reading, or a data-entry issue;
- the adjudicated value, while retaining both original values.

## Agreement Analysis

Report each field separately.

### Categorical fields

For `friction_locus`, `epistemic_support`, `discourse_level`,
`temporal_orientation`, and `uncertainty_flag`, report:

- exact agreement count and proportion;
- Cohen's kappa where computable;
- the full case-level disagreement table.

With ten cases, kappa is descriptive and potentially unstable. Raw agreement
and the identity of disagreement cases remain central.

### Compound `rationale_mechanism`

Report:

- exact-set agreement;
- primary-mechanism agreement;
- any-overlap agreement;
- mean Jaccard overlap;
- order disagreements separately when the same values appear in different
  primary-secondary order.

### Free-text and constructed fields

`evidence_anchor`, `evidence_nodes`, `anchor_node`, `function_label`, and
`rationale_note` should not be reduced to naive string identity alone. Review
these through structured case comparison:

- evidence-span overlap or divergence;
- whether the same textual event is selected;
- whether anchor labels organize the same evidential relation;
- whether function labels are substantively equivalent, partially overlapping,
  or divergent;
- whether rationale notes support the selected signature.

## Comparative Replication Tests

The pilot pre-specifies three findings for replication.

### Test A: *Macbeth* locus migration

Cases:

- `MAC_1_3`;
- `MAC_4_1`;
- `MAC_5_8`.

Full replication occurs when the second coder assigns, in sequence:

1. `warrant_attribution`;
2. `operation_function`;
3. `temporal_layering`.

Partial replication occurs when at least two assignments match and the coded
sequence still moves across more than one locus. Report the exact case of any
break in the sequence.

### Test B: shared locus, divergent trajectories

Cases:

- `ZZ_XI_4`;
- `GROVE_TAKEHIRO`.

Full replication requires:

- `warrant_relation` for both cases;
- different rationale mechanisms for the two cases;
- an extending mechanism for `ZZ_XI_4`;
- a contradicting or suspending mechanism for `GROVE_TAKEHIRO`.

Report locus replication and mechanism differentiation separately.

### Test C: shared threshold, divergent conversion

Cases:

- `ZZ_MIN_1`;
- `MAC_1_3`.

Full replication requires:

- `warrant_attribution` for both cases;
- prospective temporal orientation for both cases;
- different rationale mechanisms reflecting stabilization/projection versus
  authorization/reframing.

Report shared-threshold replication and conversion-path differentiation
separately.

## Pilot Interpretation Rules

The pilot is used to decide what happens next.

### Proceed to a larger out-of-sample study

Proceed when:

- the coding packet is usable without intervention;
- most cases are complete and valid;
- disagreements can be traced to identifiable field boundaries;
- at least two of the three comparative tests show full or substantively clear
  partial replication;
- no single core field fails because its definition is consistently
  unintelligible.

### Revise manuals before expansion

Revise the codebook or manuals when:

- the same field distinction causes repeated disagreement across traditions;
- coders systematically confuse locus with mechanism or support;
- compound ordering cannot be applied consistently;
- uncertainty and alternative pathways are used in incompatible ways;
- the source packet does not provide enough context for independent coding.

Schema changes should follow repeated evidence of the same structural problem,
not one difficult case.

## Outputs to Archive

Archive:

- source-packet version and checksum;
- randomized case order;
- blank template version;
- completed independent coding file;
- validation report;
- field-level agreement table;
- compound-mechanism metrics;
- disagreement table;
- pre-adjudication comparative replication results;
- adjudication log;
- revised post-adjudication file, clearly separated from original coding.

## Reporting Language

Report this as a blinded ten-case pilot. Describe agreement statistics as
sample-specific diagnostics. Distinguish:

- schema validity;
- coder agreement;
- replication of comparative patterns;
- adjudicated consensus.

These are related outcomes, but they answer different questions.
