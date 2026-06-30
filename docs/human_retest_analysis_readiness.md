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
| Can it flag question/uncertainty inconsistencies? | Yes, where question logs are available. | Claude companion question log was not available locally, so this could not be run on that execution. |
| What still depends on human data? | Usability, reliability, language-access interpretation, burden, and validity. | AI executions are not human evidence. |

## Current AI Execution Limitation

Only the Claude Opus 4.8 v0.2.2 coding CSV was available locally. The return
manifest, question log, language-access form, and protocol-deviation note were
not available, and the prior Codex raw execution was not found. Therefore:

- package-hash confirmation for Claude could not be verified from the return
  manifest;
- Claude final lock confirmation could not be verified;
- question-log comparison could not be run;
- Codex-vs-Claude field agreement could not be computed;
- repeated AI friction points cannot be established.

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

## Human Data Still Needed

Human external-coder data are still required before making any claim about
human usability, field reliability, cross-language validity, interpretive
burden, or domain generality.
