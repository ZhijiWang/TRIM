# TRIM v0.2.2 External Coder Deployment Checklist

Use this checklist before sending the frozen v0.2.2 coder package to any human
external coder.

## Before Sending

- Verify coder identity is not exposed in public repository files.
- Assign an anonymous coder ID.
- Confirm the coder has not seen original pilot answers.
- Confirm the coder has not seen adjudication records.
- Confirm the coder has not seen the researcher manifest.
- Confirm the coder has not seen the case-design audit.
- Confirm the coder has not seen article notes.
- Confirm the coder has not seen expected interpretations.
- Verify package SHA-256:
  `3b3ac302d8491e429d20b1d4fb1c66351ad0e6340698b2f5cd683adb5e0d4cb4`.
- Verify the ZIP opens.
- Verify all 12 formal cases are present.
- Verify the coder can work offline using only the supplied package.
- Verify the coder has a reliable spreadsheet or CSV editing method.
- Confirm timezone and deadline separately outside the repository.
- Record whether the coder can read each source language directly.

## Files The Coder Receives

The coder should receive only the frozen v0.2.2 package:

- `docs/TRIM_codebook_v0_2_2.md`
- `docs/TRIM_Coding_Manual_v0_2_2_friction_locus.md`
- `docs/TRIM_Coding_Manual_v0_2_2_rationale_mechanism.md`
- `docs/discourse_level_guide_v0_2_2.md`
- `docs/retest_v0_2_2_coder_guide.md`
- `data/retest_v0_2_2_case_manifest.csv`
- `data/retest_v0_2_2_shared_context_registry.csv`
- `data/retest_v0_2_2_source_packet.md`
- `data/retest_v0_2_2_source_text_provenance.csv`
- `data/retest_v0_2_2_coding_template.csv`
- `data/retest_v0_2_2_question_log_template.csv`
- `data/retest_v0_2_2_practice_cases.md`
- `data/retest_v0_2_2_language_access_form.csv`
- `data/retest_v0_2_2_coder_return_manifest_template.csv`

Do not send pilot answers, adjudication records, researcher-facing design files,
article-planning notes, AI dry-run substantive labels, or expected
interpretations.

## Files The Coder Must Return

- Completed coding template.
- Completed question log, including self-resolved questions.
- Completed language-access form.
- Completed coder return manifest.
- Completion-time record.
- Protocol-deviation note, if applicable.
- Package SHA-256 used by the coder.
- Final lock confirmation.

## During Coding

- Provide no case-specific coaching.
- Allow only procedural clarification.
- Require every substantive question to be logged when it arises.
- Require self-resolved questions to be logged.
- Require approximate timing to be marked as approximate rather than invented.
- Require batch-created identical timestamps to be disclosed as a protocol
  deviation.
- Do not permit discussion with other coders.
- Do not provide access to researcher-facing materials.
- Require the coder to use only the supplied source packet.
- Treat external URLs as provenance references only, not as additional coding
  material.

## At Submission

- Coder confirms the work is final.
- Returned filenames include coder ID and version.
- Returned files are copied into a locked archive or made read-only.
- Compute SHA-256 for every returned file.
- Record submission timestamp.
- Do not edit raw coder files after lock.
