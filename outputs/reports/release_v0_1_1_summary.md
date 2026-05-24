# TRIM v0.1.1 Release Summary

## Package Purpose

TRIM supports human-created annotation for Threshold–Rationale Interpretive
Modelling. The package structures evidence-to-function annotations, validates
schema conformance, parses friction signatures, generates comparison tables,
exports graphs, and prepares data for future intercoder review.

## Included Dataset

The demonstration corpus contains ten annotations from Zuo zhuan, Macbeth, and
In a Grove. It supports the article's core comparison tests:

- same function / different signature;
- same cue / different function;
- broad family / different signature;
- contested dominant threshold review.

## Validation Checks

- Required fields.
- Controlled vocabulary values.
- Compound `rationale_mechanism` values.
- Compound `epistemic_support` values.
- Friction signature format.
- Alternative signature format.
- Rationale-note review warnings.

## Generated Outputs

- Comparison tables in `outputs/tables/`.
- Demo comparison report in `outputs/reports/demo_comparison_report.md`.
- Demo validation report in `outputs/reports/demo_validation_report.md`.
- Graph summary in `outputs/reports/graph_summary.md`.
- GraphML and JSON graph exports in `outputs/graphs/`.

## Known Scope

The validator checks schema conformance and comparability. Human scholarly
review handles interpretive adjudication. The current demonstration corpus
establishes expressivity and traceability; reliability evaluation proceeds
through independently coded annotations from multiple coders.

## Tests

`python -m pytest` completed with 47 passing tests. The demo workflow completed
successfully and wrote the comparison, report, and graph outputs.
