# TRIM Software Scope

TRIM supports structured humanistic annotation for Threshold–Rationale
Interpretive Modelling. It provides a Python schema and supporting utilities for
human-created annotations of evidence-to-function conversion.

## Supported Workflows

TRIM supports:

- schema conformance checks;
- controlled vocabulary validation;
- compound signature validation;
- friction signature parsing;
- contested-case documentation;
- comparison patterns across annotated cases;
- graph outputs for evidence-to-anchor-to-function structures;
- intercoder comparison utilities for future multi-coder validation.

## Human Review Workflow

The validator checks whether annotation records conform to the coding schema.
Interpretive judgement is handled through human scholarly review. Contested
thresholds can be recorded through `alternative_signature` and documented in
`rationale_note`, making the annotation reviewable across cases and coders.

## Current Release Scope

Version 0.1.1 supports proof-of-concept demonstration and prepares the data
model for future intercoder validation. The included demonstration corpus shows
how controlled signatures, comparison tables, graph exports, and contested-case
records work together in a research workflow.
