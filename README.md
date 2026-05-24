# TRIM: Threshold–Rationale Interpretive Modelling

[![Tests](https://github.com/ZhijiWang/TRIM/actions/workflows/tests.yml/badge.svg)](https://github.com/ZhijiWang/TRIM/actions/workflows/tests.yml)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

TRIM is a Python package for structuring, validating, comparing, and exporting
human-created annotations of evidence-to-function conversion in narrative
analysis. It supports well-formed, comparable, and reviewable annotation through
controlled vocabulary checks, friction signature parsing, comparison tables,
graph export, contested-threshold review, and intercoder comparison utilities.

Current release: v0.1.1 demonstration package.

## What TRIM Provides

- Controlled vocabulary validation for threshold-rationale fields.
- Friction signature parsing and formatting.
- Comparison tables for shared functions, shared cues, broad families, and
  contested cases.
- Graph export to GraphML and node-link JSON.
- Contested-threshold review workflow using `alternative_signature` and
  `rationale_note`.
- Intercoder comparison utilities for multi-coder annotation projects.
- Optional source-segmentation workflow for auditable textual units.
- Second-coder onboarding materials for reliability pilots.

## Core Model

```text
Evidence nodes → anchor node → threshold–rationale edge → function node
```

Each annotation records human-selected evidence nodes, an anchor node, the
threshold-rationale conversion, and a project-specific function label. Graph
exports include both an explicit `anchor → threshold_rationale → function` path
for node-based visualization and a direct `anchor → function` edge carrying the
same threshold attributes for edge-based querying.

## Installation

TRIM requires Python 3.11 or newer.

Install locally from the project root:

```bash
python -m pip install -e .
```

For test development:

```bash
python -m pip install -e .
python -m pip install pytest
```

## Quick Start

Run the test suite and demonstration workflow:

```bash
python -m pytest
python examples/demo_trim_workflow.py
```

The demo workflow loads the CSV and JSON demonstration annotations, validates
them, writes comparison tables, generates reports, and exports corpus graphs.

## Command-Line Examples

```bash
trim validate data/demo_annotations.csv --out outputs/reports/validation.csv
trim report data/demo_annotations.csv --out outputs/reports/demo_report.md
trim graph data/demo_annotations.csv --graphml outputs/graphs/demo.graphml --json outputs/graphs/demo.json
trim compare data/demo_annotations.csv --outdir outputs/tables
```

## Demonstration Dataset

The included dataset contains ten method demonstration annotations:

- four Zuo zhuan divination cases;
- three Macbeth prophecy cases;
- three In a Grove testimony cases.

The dataset supports comparison patterns for same function / different
signature, same cue / different function, broad testimonial form / different
signature, and contested dominant threshold review.

Optional source segmentation can be used upstream of TRIM annotation to make
textual evidence units auditable before validation, comparison, and graph
export.

## Scope

The validator checks schema conformance and comparability. Human scholarly
review handles interpretive adjudication. Intercoder reliability is evaluated
through separate multi-coder annotation.

Human coders assign interpretive labels; the package validates and compares
those annotations. The current demonstration corpus establishes expressivity and
traceability. Reliability evaluation proceeds through independently coded
annotations from multiple coders.

## Documentation

The package version is v0.1.1. The `friction_locus` coding manual is versioned
separately as v0.2 because it develops coder-facing guidance for the controlled
field.

- [`docs/TRIM_codebook_v0_1_1.md`](docs/TRIM_codebook_v0_1_1.md)
- [`docs/TRIM_Coding_Manual_v0_2_friction_locus_final.md`](docs/TRIM_Coding_Manual_v0_2_friction_locus_final.md)
- [`docs/TRIM_Coding_Manual_v0_2_rationale_mechanism.md`](docs/TRIM_Coding_Manual_v0_2_rationale_mechanism.md)
- [`docs/software_scope.md`](docs/software_scope.md)
- [`docs/demo_dataset_notes.md`](docs/demo_dataset_notes.md)
- [`docs/segmentation_workflow.md`](docs/segmentation_workflow.md)
- [`docs/second_coder_onboarding.md`](docs/second_coder_onboarding.md)
- [`docs/intercoder_workflow.md`](docs/intercoder_workflow.md)
- [`docs/methodological_position.md`](docs/methodological_position.md)
- [`docs/article_use.md`](docs/article_use.md)
- [`docs/release_instructions.md`](docs/release_instructions.md)
- [`CHANGELOG.md`](CHANGELOG.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Citing

Citation metadata is provided in [`CITATION.cff`](CITATION.cff).

## License

MIT. See [`LICENSE`](LICENSE).
