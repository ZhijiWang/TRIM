# TRIM: Threshold–Rationale Interpretive Modelling

[![Tests](https://github.com/ZhijiWang/TRIM/actions/workflows/tests.yml/badge.svg)](https://github.com/ZhijiWang/TRIM/actions/workflows/tests.yml)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

TRIM structures the warranted conversion from textual evidence to interpretive
function as a locatable, reviewable, and comparable annotation pathway.

Current source version: 0.2.0 (unreleased). No formal GitHub Release has been published.

## What TRIM Annotates

```text
Evidence nodes → anchor node → threshold–rationale relation → function node
```

Human coders select the evidence, anchor, function label, and rationale. The
main friction signature records:

- `friction_locus`;
- `rationale_mechanism`;
- `epistemic_support`;
- `discourse_level`;
- `temporal_orientation`;
- `uncertainty_flag`.

Annotations may also include `alternative_signature` and `rationale_note` for
contested-threshold review.

Interpretive friction is relational: it is a locatable difficulty in the
warranted conversion from evidence to function under an explicit interpretive
scheme, not a context-free property automatically detected in a text.

## What the Software Does

- validates required fields, controlled values, and compound signatures;
- parses and compares friction signatures;
- generates same-function, same-cue, broad-family, and contested-case tables;
- exports evidence-to-function graphs as GraphML and JSON;
- supports optional source segmentation;
- provides raw and compound-aware intercoder comparison utilities.

The software does not choose function labels, adjudicate interpretations,
generate literary claims, or capture a coder's full reasoning process.

## Installation and Quick Start

TRIM requires Python 3.11 or newer.

```bash
python -m pip install -e .
python -m pip install pytest
python -m pytest
python examples/demo_trim_workflow.py
```

Command-line examples:

```bash
trim validate data/demo_annotations.csv --out outputs/reports/validation.csv
trim report data/demo_annotations.csv --out outputs/reports/demo_report.md
trim graph data/demo_annotations.csv --graphml outputs/graphs/demo.graphml --json outputs/graphs/demo.json
trim compare data/demo_annotations.csv --outdir outputs/tables
```

## Demonstration and Validation Status

The ten-case demonstration corpus contains four Zuo zhuan divination cases,
three Macbeth prophecy cases, and three In a Grove testimony cases. It
demonstrates schema expressivity, traceable comparison, graph export, and one
contested threshold.

Generated comparison tables provide structural `comparison_prompt` text only.
Researcher-authored worked interpretations are kept separately in
[`docs/substantive_demo_interpretations.md`](docs/substantive_demo_interpretations.md).

The repository also includes:

- a three-case software/onboarding demonstration for second-coder workflow;
- a ten-case template scaffold that requires a separate blinded source packet
  before use in a preliminary usability pilot;
- intercoder agreement and disagreement utilities.

These materials can test manual usability, field boundaries, and workflow
operation. They do not establish domain-general reliability, stable
population-level agreement, or universal reproducibility.

## Methodological Position

TRIM does not claim as novel the general observation that label agreement can
coexist with explanatory disagreement. It does not primarily classify
free-text explanations by linguistic reasoning type, and it is not an LLM
chain-of-thought or hidden-cognition system. Its contribution is the combined
evidence, anchor, conversion, support, discourse, temporal, uncertainty, and
alternative-path structure for reviewable human scholarly interpretation.

See [`docs/related_methods.md`](docs/related_methods.md) and
[`docs/methodological_position.md`](docs/methodological_position.md).

## Documentation

- [`docs/TRIM_codebook_v0_2_0.md`](docs/TRIM_codebook_v0_2_0.md)
- [`docs/TRIM_Coding_Manual_v0_2_friction_locus_final.md`](docs/TRIM_Coding_Manual_v0_2_friction_locus_final.md)
- [`docs/TRIM_Coding_Manual_v0_2_rationale_mechanism.md`](docs/TRIM_Coding_Manual_v0_2_rationale_mechanism.md)
- [`docs/demo_dataset_notes.md`](docs/demo_dataset_notes.md)
- [`docs/substantive_demo_interpretations.md`](docs/substantive_demo_interpretations.md)
- [`docs/segmentation_workflow.md`](docs/segmentation_workflow.md)
- [`docs/second_coder_onboarding.md`](docs/second_coder_onboarding.md)
- [`docs/intercoder_workflow.md`](docs/intercoder_workflow.md)
- [`docs/software_scope.md`](docs/software_scope.md)
- [`docs/article_use.md`](docs/article_use.md)
- [`CHANGELOG.md`](CHANGELOG.md)

## Citing and License

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). Until a formal
release exists, cite the exact commit used. TRIM is licensed under the MIT
License; see [`LICENSE`](LICENSE).
