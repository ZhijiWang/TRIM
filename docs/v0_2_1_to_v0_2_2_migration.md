# v0.2.1 to v0.2.2 Migration Note

## Why v0.2.2 Exists

A machine-executed protocol dry run of the frozen v0.2.1 package found residual
deployment issues before human external-coder use:

1. residual ambiguity in two coder-facing metadata fields;
2. a need for a question-log / final-uncertainty consistency warning;
3. a need to clarify real-time question logging.

The dry run is treated only as an AI protocol stress test. It is not a human
external-coder submission, intercoder reliability evidence, completed v0.2.1
empirical retest, cross-language validation, or evidence that human usability
has been established.

## What Changed

- Removed coder-facing `cue_family`.
- Removed coder-facing `broad_function_family`.
- Added a warning when an interpretive or definitional question changed the code
  but the final annotation uses low uncertainty and no complete alternative
  signature.
- Clarified that questions should be logged when they arise during coding.
- Added an AI dry-run archive record with safe metadata only.

## What Did Not Change

- Formal cases.
- Source-text segments.
- Source provenance.
- Function vocabulary.
- Friction loci.
- Rationale mechanisms.
- Discourse levels.
- Temporal orientation.
- Uncertainty definitions.
- Shared-context registry.
- Evidence-selection rules.
- No-fit rules.
- Case-design rationale.

## Comparability Statement

The v0.2.1 AI dry-run results remain a protocol stress test and are not pooled
with future human v0.2.2 retest data. v0.2.2 human coding is the prospective
empirical dataset. No substantive label from the AI dry run was used to alter
the codebook, case selection, source texts, source segments, controlled
vocabularies, or case-design rationale.
