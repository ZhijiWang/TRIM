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
- pilot-scale intercoder comparison utilities.

Standard validated annotations require one or more evidence nodes, a
source-facing `evidence_anchor`, and a distinct normalized `anchor_node`. Graph
construction rejects records that omit these components rather than silently
falling back to an anchor-only model.

## Human Review Workflow

The validator checks whether annotation records conform to the coding schema.
Interpretive judgement is handled through human scholarly review. Contested
thresholds can be recorded through `alternative_signature` and documented in
`rationale_note`, making the annotation reviewable across cases and coders.

TRIM does not objectively detect friction, infer a coder's hidden cognitive
process, or generate substantive interpretations. It structures selected
human-created judgements and checks their form.

## Current Package Scope

Source version 0.2.0 remains unreleased and supports proof-of-concept
demonstration and pilot infrastructure.
The ten-case corpus shows how controlled signatures, comparison tables, graph
exports, and contested-case records work together. The three-case second-coder
workflow demonstrates software preparation. Neither establishes general
intercoder reliability.
