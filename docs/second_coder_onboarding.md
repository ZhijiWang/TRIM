# Second-Coder Onboarding

## Purpose

Independent coding evaluates how consistently TRIM fields can be applied across the same cases. This guide prepares a second coder to work from the blinded source packet and coding manuals, then return a preserved CSV for comparison.

## Materials

Read:

- `docs/TRIM_codebook_v0_2_0.md`
- `docs/TRIM_Coding_Manual_v0_2_friction_locus_final.md`
- `docs/TRIM_Coding_Manual_v0_2_rationale_mechanism.md`
- `docs/segmentation_workflow.md`
- `docs/blinded_pilot_protocol.md`

Use:

- `data/blinded_pilot_source_packet.md`
- `data/blinded_pilot_case_manifest.csv`
- `data/blinded_pilot_coding_template.csv`

## Coding Task

Complete:

- `evidence_anchor`
- `evidence_nodes`
- `anchor_node`
- `function_label`
- `friction_locus`
- `rationale_mechanism`
- `epistemic_support`
- `discourse_level`
- `temporal_orientation`
- `uncertainty_flag`
- `rationale_note`
- `alternative_signature` when a viable competing pathway remains

## Coding Environment

The source packet, codebook, and manuals define the independent coding environment. Primary-coder values, generated comparison tables, and substantive demonstration interpretations enter the workflow after the completed file has been preserved.

Uncertainty is recorded directly in `uncertainty_flag` and explained in `rationale_note`. Competing pathways remain visible through `alternative_signature`.

## Two-Round Procedure

### Round 1

Record:

- evidence and source-facing anchor;
- analytic anchor;
- function label;
- `friction_locus`;
- `uncertainty_flag`;
- `rationale_note`.

Apply the counterfactual, proximity, and explanatory-sufficiency tests when more than one locus appears plausible.

### Round 2

Complete:

- `rationale_mechanism`;
- `epistemic_support`;
- `discourse_level`;
- `temporal_orientation`;
- `alternative_signature` where needed.

Compound mechanisms preserve primary-to-secondary order.

### Preservation

Timestamp and preserve the completed CSV before viewing primary-coder annotations. Initial agreement measures and disagreement tables are generated from this version.

### Adjudication

Adjudication begins after the pre-adjudication outputs are archived. The original coding file remains available alongside any adjudicated version.

## Ten-Case Coverage

The pilot includes:

- four *Zuo zhuan* divination cases;
- three *Macbeth* prophecy cases;
- three *In a Grove* testimony cases;
- five demonstrated `friction_locus` values;
- simple and compound mechanisms;
- low, medium, and high uncertainty;
- one contested primary-coder case.

The design evaluates manual usability, field boundaries, disagreement location, and the replication of three pre-specified comparative patterns.

## Coder Profile

The pilot report records the coder's disciplinary background, language competence, and familiarity with the three source traditions. For the Classical Chinese cases, the report also states whether the coder used the original text, the close paraphrase, or both.

## Returning Data

Return the completed CSV with:

- a distinct `coder_id`, such as `second_coder`;
- a project-appropriate `status`;
- every required field completed;
- the original row order or the archived randomized order preserved.

See `docs/intercoder_workflow.md` for comparison and reporting.
