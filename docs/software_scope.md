# TRIM Software Scope

TRIM provides a Python schema and supporting utilities for structured annotations of evidence-to-function conversion.

## Supported Workflows

TRIM supports:

- schema conformance checks;
- controlled vocabulary validation;
- compound signature validation;
- friction signature parsing;
- contested-case documentation;
- comparison across annotated cases;
- graph export for evidence-to-anchor-to-function structures;
- pilot-scale intercoder analysis.

A standard annotation contains one or more evidence nodes, a source-facing `evidence_anchor`, and a normalized `anchor_node`. These fields preserve both textual location and analytic organization. Graph construction uses the full pathway.

## Review Workflow

Validation checks the formal integrity of each record. Scholarly review evaluates the interpretation. `alternative_signature` and `rationale_note` preserve competing pathways and keep their evidential basis available for comparison and adjudication.

The package structures selected scholarly judgements and checks their form. Function labels, substantive interpretation, and final adjudication remain part of the research process.

## Current Scope

Source version 0.2.0 supports proof-of-concept demonstration and pilot infrastructure. The ten-case corpus establishes schema expressivity, traceable comparison, and graph-based representation. The blinded materials establish pilot readiness through a protocol, source packet, neutral manifest, and blank coding template.

Independent coding and out-of-sample testing form the next empirical stages.
