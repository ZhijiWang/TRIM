# Using TRIM in an Article

## Software Citation

Cite a fixed GitHub release or Zenodo DOI rather than the mutable `main` branch.
The repository includes `CITATION.cff` for software citation metadata. When a
Zenodo DOI is available, use the DOI for article references and archival
citations.

## Suggested Method-Section Language

TRIM is implemented as a lightweight Python package accompanying this article.
The package encodes the annotation schema, validates controlled vocabulary
conformance, parses friction signatures, generates comparison tables, and
exports graph representations of evidence-to-function paths. It also includes
utilities for future intercoder comparison. The implementation supports
reviewable human annotation: coders assign interpretive labels and rationale
notes, while the package checks schema conformance and comparability.

## Reproducibility Statement

The repository contains:

- `data/demo_annotations.csv`;
- source segment examples;
- codebook;
- coding manuals;
- scripts;
- tests;
- generated output paths.

The demonstration workflow can be rerun with:

```bash
python -m pytest
python examples/demo_trim_workflow.py
```

The optional source-segment workflow can be rerun with:

```bash
python examples/run_trim_with_source_segments.py
```

## Versioning

The current package release is v0.1.1. Coding manuals may have independent
versions when they develop coder-facing guidance for specific controlled
fields. Articles should cite the software release version used for the analysis.
