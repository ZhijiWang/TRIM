# Human Retest Analysis Readiness

This document records what the repository can currently do after the v0.2.2 AI
execution stress-test pass.

## Readiness Questions

| Question | Current answer | Notes |
| --- | --- | --- |
| Can the repository ingest two independent submissions? | Yes, structurally. | `trim.ai_execution` compares two coding DataFrames when both are available. |
| Can it compare common fields across v0.2.1 and v0.2.2? | Yes. | Version-aware comparison uses common annotation fields and does not require removed v0.2.2 coder-template fields. |
| Can it preserve version differences? | Yes. | v0.2.1 and v0.2.2 package hashes and frozen file manifests remain separate. |
| Can it distinguish raw comparison from adjudication? | Yes. | AI comparison outputs are descriptive and separate from adjudication categories. |
| Can it produce case-level evidence overlap? | Yes. | Primary Jaccard, context Jaccard, exact primary match, and role reversal are implemented. |
| Can it classify same-function/different-pathway cases? | Yes. | Classification is conservative and descriptive. |
| Can it flag question/uncertainty inconsistencies? | Yes. | The complete Claude v0.2.2 bundle includes a question log, and question/annotation consistency validation completed with no warnings. |
| What still depends on human data? | Usability, reliability, language-access interpretation, burden, and validity. | AI executions are not human evidence. |

## Current AI Execution Status

The complete Claude Opus 4.8 v0.2.2 bundle was available through the attached
local archive and validated as a five-file AI execution return:

- coding CSV: 12/12 formal cases completed;
- question log: 9 rows;
- language-access form: 12 rows;
- return manifest: frozen v0.2.2 package hash matched;
- protocol-deviation note: present, with explicit AI/non-human limitation;
- approximate timestamps were disclosed with `~`;
- locked status was recorded as `yes`;
- reported completion time was approximately 55 minutes.

The prior Codex v0.2.1 ZIP was not locally readable in this workspace. The
expected path `/mnt/data/TRIM_retest_v0_2_1_completed_submission.zip` was not
mounted, and the attached `files.zip` contained only the Claude v0.2.2 files.
The request supplied an expected ZIP hash and contained filenames, but extracted
Codex file hashes and structural validation could not be computed without the
actual ZIP. Therefore:

- Claude submission ingestion, package-hash verification, question-log
  validation, language-access completeness, and lock metadata were verified;
- Codex-vs-Claude field agreement, evidence overlap, pathway classification,
  and question-log comparison were not computed;
- repeated AI friction points cannot be established from two executions in this
  workspace.

## Ready Components

- Coding-sheet structural validation.
- v0.2.2 source segment validation.
- v0.2.2 shared-context validation.
- Field-level comparison helpers.
- Evidence-overlap helpers.
- Primary/context role-reversal detection.
- Pathway classification.
- Uncertainty distribution reporting.
- Alternative-signature frequency reporting.
- Missing-submission transparency.
- Complete five-file v0.2.2 AI bundle validation.

## Human Data Still Needed

Human external-coder data are still required before making any claim about
human usability, field reliability, cross-language validity, interpretive
burden, or domain generality.
