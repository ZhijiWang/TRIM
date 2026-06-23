# Using TRIM in an Article

## Software Citation

No formal GitHub Release currently exists. Until one is published, cite the
exact commit used and the repository URL. Once a fixed GitHub Release or Zenodo
DOI exists, prefer that archival identifier. The repository includes
`CITATION.cff` for citation metadata.

## Suggested Method-Section Language

TRIM is implemented as a lightweight Python package accompanying this article.
The package encodes the annotation schema, validates controlled vocabulary
conformance, parses friction signatures, generates comparison tables, and
exports graph representations of evidence-to-function paths. It also includes
pilot-scale intercoder comparison utilities. The implementation supports
reviewable human annotation: coders assign interpretive labels and rationale
notes, while the package checks schema conformance and comparability. The
software-generated comparison prompts are structural; substantive
interpretation remains researcher-authored.

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

## Claim Boundary

The current package version is 0.2.0. It is not a formal GitHub Release. Coding
manuals may have independent versions when they develop coder-facing guidance
for specific controlled fields.

The ten-case demonstration establishes schema expressivity and workflow
traceability, not domain-general reliability. A three-case workflow can verify
software operation; a ten-case preliminary pilot can identify usability and
boundary problems. Neither supports population-level reliability claims.
