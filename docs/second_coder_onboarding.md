# Second-Coder Onboarding

## Purpose

Independent coding is used to evaluate how consistently coders can apply TRIM
fields. This packet prepares a second coder to work from source segments and
the coding manuals, then return a completed CSV for comparison.

## Materials to Read

- `docs/TRIM_codebook_v0_1_1.md`
- `docs/TRIM_Coding_Manual_v0_2_friction_locus_final.md`
- `docs/TRIM_Coding_Manual_v0_2_rationale_mechanism.md`
- `docs/segmentation_workflow.md`

## Coding Task

The second coder assigns selected TRIM fields independently. Recommended pilot
fields are:

- `function_label`
- `friction_locus`
- `rationale_mechanism`
- `epistemic_support`
- `discourse_level`
- `temporal_orientation`
- `uncertainty_flag`
- `rationale_note`
- `alternative_signature` when needed

## Independence Protocol

- The second coder should work from source segments and the coding manuals.
- The second coder should not consult the primary coder's completed labels
  during independent coding.
- Uncertainty should be recorded in `uncertainty_flag` and `rationale_note`.
- Contested readings should be recorded through `alternative_signature` when
  appropriate.

## Output Format

Use `data/second_coder_template.csv`. The file uses the same columns as
`data/demo_annotations.csv`, with coder-assigned fields left blank for
independent completion.

## Suggested Pilot

Use the ten demonstration cases or a smaller pilot subset. For a first test,
code only `friction_locus` and `rationale_note`; then expand to all signature
fields.

## Returning Data

The coder returns a completed CSV with `coder_id` set to a distinct value such
as `second_coder` and `status` set to the appropriate project stage.

## Comparison

Intercoder comparison can be run using the existing TRIM utilities after the
second-coder CSV is completed. See `docs/intercoder_workflow.md` and
`examples/run_intercoder_demo.py`.
