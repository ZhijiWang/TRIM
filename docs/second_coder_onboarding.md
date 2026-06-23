# Second-Coder Onboarding

## Purpose

Independent coding is used to evaluate how consistently coders can apply TRIM
fields. This packet prepares a second coder to work from source segments and
the coding manuals, then return a completed CSV for comparison.

The repository currently provides pilot infrastructure, not a completed
reliability study.

## Materials to Read

- `docs/TRIM_codebook_v0_2_0.md`
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

## Available Templates

- `data/second_coder_template.csv` contains three In a Grove cases and is suited
  to a software and onboarding demonstration.
- `data/demo_annotations_second_coder_template.csv` contains all ten
  demonstration case IDs as a schema scaffold. It must be paired with a
  separately prepared, blinded source packet before it can support a
  preliminary usability pilot.

Both files use the TRIM schema, with coder-assigned fields left blank for
independent completion. They are incomplete scaffolds, not valid standard
annotations: `evidence_nodes`, `anchor_node`, signature fields, and rationale
documentation must be completed before validation succeeds.

## Staged Pilot Procedure

1. First round: code `friction_locus` and `rationale_note`.
2. Second round: code the full signature fields.
3. Complete all independent coding before viewing the primary coder's labels.
4. Compute initial metrics before adjudication.
5. Review disagreements only after the independent comparison is preserved.

If the dominant-threshold protocol does not resolve a case, set
`uncertainty_flag=high`, provide `alternative_signature` when possible, and
explain the unresolved choice in `rationale_note`.

## TRIM-Specific Ten-Case Pilot

After a blinded source packet is prepared, using all ten demonstration cases
provides a compact preliminary design that covers:

- Zuo zhuan, Macbeth, and In a Grove;
- all five currently demonstrated `friction_locus` values;
- `warrant_attribution` versus `warrant_relation`;
- `operation_function` versus `temporal_layering`;
- `operation_function` versus `perspective_assignment`;
- the contested Xi 4 annotation;
- low, medium, and high uncertainty levels.

This is a usability or preliminary pilot, not a definitive reliability sample.
A smaller subset should retain all three traditions, at least one contested
case, more than one uncertainty level, and the confusable pairs relevant to the
research question.

## What the Pilot Can and Cannot Establish

A small pilot can test whether:

- the manuals are usable;
- field boundaries are intelligible;
- disagreements can be located and described;
- the data and adjudication workflow function.

It cannot establish:

- domain-general reliability;
- stable population-level agreement;
- universal reproducibility.

## Returning Data

The coder returns a completed CSV with `coder_id` set to a distinct value such
as `second_coder` and `status` set to the appropriate project stage.

## Comparison

Intercoder comparison can be run using the existing TRIM utilities after the
second-coder CSV is completed. See `docs/intercoder_workflow.md` and
`examples/run_intercoder_demo.py`.
