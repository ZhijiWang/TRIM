# TRIM v0.1.1 Package Summary

## Purpose

TRIM is a humanistic annotation support package for Threshold–Rationale
Interpretive Modelling. It structures, validates, compares, and exports
human-created annotations of evidence-to-function conversion.

## Package Capabilities

- Schema support for TRIM annotations.
- Controlled vocabulary validation for threshold-rationale fields.
- CSV and JSON annotation input/output.
- Canonical friction signature parsing in `trim/signature.py`.
- Comparison utilities for same-function, same-cue, broad-family, and contested
  case tables.
- Optional cue-family filtering for same-cue comparison tables.
- Graph utilities for evidence-to-anchor-to-function paths.
- Intercoder comparison utilities for multi-coder annotation projects.
- Argparse command-line interface.

## Demonstration Corpus

- `data/demo_annotations.csv`: 10 records.
- `data/demo_annotations.json`: 10 records.
- `data/demo_annotations_second_coder_template.csv`: blank template for future
  second-coder annotation.

The demonstration corpus includes cases from Zuo zhuan, Macbeth, and In a
Grove. It supports the article's core comparison tests while preserving
case-specific annotation paths.

## Article-Facing Outputs

- Same function / different signature:
  - `immediate_stabilization`: `ZZ_XIANG_7`, `ZZ_MIN_1`
  - `extended_deliberation`: `ZZ_XI_4`, `ZZ_ZHUANG_22`
- Same cue / different function:
  - Primary article-facing test: `prophecy`, using the Macbeth cases.
  - Additional detected cue groups: `divination` and `testimony`.
- Broad family / different signature:
  - `self-exculpatory testimony`: `GROVE_TAJOMARU`, `GROVE_MASAGO`
- Contested dominant threshold:
  - `ZZ_XI_4`

## Graph Outputs

- `outputs/graphs/demo_corpus.graphml`
- `outputs/graphs/demo_corpus_graph.json`

The corpus graph contains 76 nodes and 102 edges. It preserves case-specific
paths from evidence nodes to anchors and from anchors through
threshold-rationale conversion to function nodes.

Graph exports include both:

- `anchor → threshold_rationale → function`
- direct `anchor → function` edges carrying the same threshold attributes

This supports node-based visualization and edge-based querying.

## Validation Scope

The validator checks schema conformance and comparability. Human scholarly
review handles interpretive adjudication. Intercoder reliability is evaluated
through independently coded annotations from multiple coders.

## Status

TRIM v0.1.1 is ready as a demonstration research software package for
validating, comparing, reporting, and graphing human-created annotations.
