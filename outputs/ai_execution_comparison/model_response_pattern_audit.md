# Model Response Pattern Audit

Label: Exploratory AI execution comparison. Not human intercoder reliability.

Only the Claude Opus 4.8 v0.2.2 coding CSV was available locally. The prior Codex raw submission and Claude companion files were not available, so this audit is Claude-only and cannot support AI-AI comparison claims.

## Claude Pattern Summary

- Cases completed in coding CSV: 12/12.
- Medium uncertainty: 11/12.
- Low uncertainty: 1/12.
- Alternative signatures present: 11/12.
- All-segment primary selection count: 0/12.
- Mean primary segment count: 1.58.
- Mean context segment count: 1.92.
- Median rationale-note length: 467.0 characters.
- No-fit count: 0/12.

## Interpretation

Claude appears to use medium uncertainty in most cases and complete alternative signatures in most cases. This should be treated as a model-style tendency or possible package stress point, not as a TRIM defect. Human data are needed to distinguish method friction, model-style tendency, source-case difficulty, and package ambiguity.

The available coding CSV does not show all-segment primary overuse. Context segments are commonly used, which may reflect either careful sequence support or a model preference for balanced-looking evidence structures.

## Unavailable Comparisons

Because Codex raw coding and Claude question log files were not available, this audit cannot compare question-log behavior, repeated friction points across model executions, real-time versus reconstructed timestamps, or AI-AI field agreement.
