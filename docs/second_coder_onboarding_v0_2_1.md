# Second-Coder Onboarding v0.2.1

## Purpose

This guide prepares a coder for the v0.2.1 out-of-sample retest. The retest
checks whether pilot-informed revisions improve usability and boundary
calibration. It does not recode the locked v0.2.0 pilot.

## Read First

- `docs/TRIM_codebook_v0_2_1.md`
- `docs/TRIM_Coding_Manual_v0_2_1_friction_locus.md`
- `docs/TRIM_Coding_Manual_v0_2_1_rationale_mechanism.md`
- `docs/discourse_level_guide_v0_2_1.md`
- `docs/retest_v0_2_1_coder_guide.md`
- `docs/retest_protocol_v0_2_1.md`

Use:

- `data/retest_v0_2_1_source_packet.md`
- `data/retest_v0_2_1_case_manifest.csv`
- `data/retest_v0_2_1_coding_template.csv`
- `data/retest_v0_2_1_question_log_template.csv`
- `data/retest_v0_2_1_language_access_form.csv`

## Coding Task

Complete every required annotation field, including:

- one to three `primary_evidence_segment_ids`;
- optional `context_segment_ids`;
- optional `evidence_highlight`;
- `evidence_anchor`;
- `anchor_node`;
- closed-list `function_label`, including `no_fit` when appropriate;
- full six-field friction signature;
- calibrated `uncertainty_flag`;
- `rationale_note`;
- `alternative_signature` when a complete competing pathway remains viable.

## Evidence Selection

Primary evidence is the smallest segment set without which the annotation would
not hold. Context segments explain sequence, speaker role, background, or shared
field. Do not mark every supplied segment primary by default.

If more than three segments seem indispensable, choose the one to three where
the conversion turns, mark the rest as context, and explain the dependency.

## Questions

Record every definitional, interpretive, procedural, or packet-level question in
the question log, even when you can provisionally resolve it yourself.

Formal coding still prohibits case-specific coaching before lock. The log is a
method-development record, not a request for live answers.

## Language Access

Complete the language-access form before formal coding. For each case, record
whether you used:

- direct original-language access;
- a published translation;
- project-authored close support;
- summary-mediated support;
- mixed access.

The v0.2.1 retest must be reported honestly as direct-language or
translation-mediated depending on the completed forms.

## Shared Context

Use only the context permitted by the manifest:

- `local_passage`;
- `complete_work`;
- `supplied_related_cases`;
- `shared_narrative_field`.

If `cross_case_context_permitted=no`, do not use other cases to decide the
signature. If shared context is permitted, record any required context segments
in the appropriate field.

## Uncertainty

- Low: one complete pathway is clearly preferable and no complete alternative
  remains viable.
- Medium: one pathway is preferable but a complete alternative signature is
  reasonably defensible.
- High: evidence or rules cannot stabilize the choice.

A complete alternative signature normally requires at least medium uncertainty.

## Locking

Submit the completed coding sheet and question log before seeing comparison,
adjudication, pilot results, or article working notes. Do not revise the locked
file after debriefing.

