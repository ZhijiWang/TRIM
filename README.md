# TRIM: Threshold–Rationale Interpretive Modelling

[![Tests](https://github.com/ZhijiWang/TRIM/actions/workflows/tests.yml/badge.svg)](https://github.com/ZhijiWang/TRIM/actions/workflows/tests.yml)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

TRIM structures the warranted conversion from textual evidence to interpretive
function as a locatable, reviewable, and comparable annotation pathway.

Current source version: 0.2.0 (unreleased).

## Core Model

```text
Evidence nodes → anchor node → threshold–rationale relation → function node
```

A TRIM annotation records a human interpretive judgement in six connected
fields:

- `friction_locus` locates the dominant threshold;
- `rationale_mechanism` records what the conversion does;
- `epistemic_support` identifies the support that carries the judgement;
- `discourse_level` places the conversion within the text's discursive structure;
- `temporal_orientation` records its temporal direction;
- `uncertainty_flag` marks the coder's level of confidence.

`alternative_signature` and `rationale_note` preserve competing pathways and the
reasoning that keeps them in view.

Standard annotations also include:

- one or more `evidence_nodes`;
- `evidence_anchor`, which returns the record to a source-facing span, quotation,
  or segment reference;
- `anchor_node`, which gives that evidence a normalized analytic centre.

Interpretive friction emerges where textual evidence, analytic function, and
warranting support meet. TRIM turns that point of pressure into an explicit
comparative object.

## Software Workflow

The package:

- validates required fields, controlled values, and compound signatures;
- parses and compares friction signatures;
- generates same-function, same-cue, broad-family, and contested-case tables;
- exports evidence-to-function graphs as GraphML and JSON;
- supports source segmentation;
- prepares pilot-scale intercoder comparison and disagreement reports.

Human coders define the evidence, function, and rationale. The software preserves
those choices in a form that can be checked, compared, and revisited.

## Installation and Quick Start

TRIM requires Python 3.11 or newer.

```bash
python -m pip install -e .
python -m pip install pytest
python -m pytest
python examples/demo_trim_workflow.py
```

Install Cohen's kappa support with:

```bash
python -m pip install -e ".[reliability]"
```

Command-line examples:

```bash
trim validate data/demo_annotations.csv --out outputs/reports/validation.csv
trim report data/demo_annotations.csv --out outputs/reports/demo_report.md
trim graph data/demo_annotations.csv --graphml outputs/graphs/demo.graphml --json outputs/graphs/demo.json
trim compare data/demo_annotations.csv --outdir outputs/tables
```

`trim validate` writes its CSV report before returning. Validation errors produce
status 1; valid and warnings-only input produce status 0. `--always-zero` supports
reporting pipelines that handle status outside the command.

## Demonstration Corpus

The ten-case corpus brings together:

- four *Zuo zhuan* divination cases;
- three *Macbeth* prophecy cases;
- three *In a Grove* testimony cases.

It demonstrates schema expressivity, traceable comparison, graph export, and
contested-threshold review. Generated tables provide structural
`comparison_prompt` text. Researcher-authored interpretations appear in
[`docs/substantive_demo_interpretations.md`](docs/substantive_demo_interpretations.md).

The repository also contains:

- a three-case software and onboarding demonstration;
- a complete ten-case blinded pilot protocol;
- a neutral case manifest;
- a blank second-coder template;
- a source packet for independent coding;
- field-level and compound-aware agreement utilities;
- a cross-language construct-validity protocol and
  [companion template](data/cross_language_validity_template.csv).

These materials establish a proof of concept and a fully specified validation
infrastructure. Independent second-coder execution forms the next empirical
stage.

## Methodological Contribution

TRIM contributes a structured account of how scholarly interpretation moves
from evidence to function. Its analytic object combines evidence, anchor,
conversion, support, discourse position, temporality, uncertainty, and viable
alternatives. This structure makes within-label variation, cross-case
convergence, and divergent conversion pathways available to direct comparison.

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
- [`docs/blinded_pilot_protocol.md`](docs/blinded_pilot_protocol.md)
- [`docs/cross_language_validity.md`](docs/cross_language_validity.md)
- [`data/cross_language_validity_template.csv`](data/cross_language_validity_template.csv)
- [`docs/software_scope.md`](docs/software_scope.md)
- [`docs/schema_validation_migration.md`](docs/schema_validation_migration.md)
- [`docs/article_use.md`](docs/article_use.md)
- [`CHANGELOG.md`](CHANGELOG.md)

## Citing and License

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). Before a formal
release, cite the exact commit used together with the repository URL. TRIM is
licensed under the MIT License; see [`LICENSE`](LICENSE).
