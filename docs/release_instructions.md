# Release Instructions

1. Confirm tests pass:

```bash
python -m pytest
python examples/demo_trim_workflow.py
```

2. Update version if needed in:

- `pyproject.toml`
- `CITATION.cff`
- `CHANGELOG.md`

3. Commit changes.

4. Create GitHub release:

- Tag: `v0.1.1`
- Title: `TRIM v0.1.1: Demonstration Package`

Release notes:

TRIM v0.1.1 provides the first stable demonstration package for
Threshold–Rationale Interpretive Modelling. It includes the annotation schema,
controlled vocabulary validation, friction signature parsing, comparison
utilities, graph export, intercoder comparison utilities, a ten-case
demonstration dataset, and coder-facing documentation for `friction_locus`.

5. Archive release through Zenodo.

6. Add the Zenodo DOI to:

- `CITATION.cff`
- `README.md`
