# TRIM-HAA

TRIM-HAA is a provenance-aware framework for preserving and auditing evidence selection, interpretive labels, rationale mechanisms, uncertainty, alternatives, and annotation lineage across human and model records.

## What It Does

TRIM-HAA stores structured annotation records with selected evidence, function labels, rationale mechanisms, uncertainty, optional alternative pathways, and provenance. It supports record locking, lineage checks, independent human/model record comparison, and exposure-audit workflows in which a locked earlier human record can be compared with a later response after AI review or a no-AI second pass.

The software preserves the structure of interpretive difference. It helps reviewers inspect where records differ: evidence, label, mechanism, uncertainty, alternative handling, rationale text, and provenance.

## What It Does Not Do

TRIM-HAA does not determine interpretive truth. It does not treat model output as an answer key, optimize human-AI collaboration, or make causal claims about model exposure by default.

The current repository contains a software prototype, synthetic dry run, and author-only walkthrough. It does not contain empirical human validation, ethics approval, participant data, or a validated detector of interpretive problems.

## Installation

From a source checkout:

```bash
git clone https://github.com/ZhijiWang/TRIM.git
cd TRIM
python -m pip install -e .
```

For local development with tests:

```bash
python -m pip install -e ".[test]"
```

## Python Quickstart

```python
from trim_haa import TrimHAAAnnotation, validate_core_record, lock_annotation

record = TrimHAAAnnotation(
    annotation_id="ann-001",
    case_id="case-001",
    actor_id="human-001",
    actor_type="human",
    annotation_stage="human_pre",
    primary_evidence_segment_ids=("seg-001",),
    function_label="unresolved_agency",
    rationale_mechanism="contrast_or_tension",
    uncertainty_flag="medium",
    rationale_note="The selected text supports the label while leaving room for another path.",
    alternative_pathway_present="yes",
    alternative_mechanism="unidentified_intervention",
    alternative_note="A later event may affect narrative closure.",
    status="locked",
)

issues = validate_core_record(record)
lock = lock_annotation(
    record,
    lock_manifest_id="lock-001",
    locked_at="2026-07-01T00:00:00Z",
    locked_by="example",
)
```

## CLI Quickstart

```bash
trim-haa --help
trim-haa version
trim-haa validate tests/fixtures/trim_haa/core_valid.csv
trim-haa verify-lock tests/fixtures/trim_haa/core_valid.csv tests/fixtures/trim_haa/lock_valid.csv
trim-haa compare examples/in_a_grove_walkthrough/author_analytic_record.csv examples/in_a_grove_walkthrough/ai_independent_record.csv
trim-haa run-walkthrough
```

## Repository Structure

- `src/trim_haa`: importable Python package.
- `docs`: standalone TRIM-HAA documentation.
- `examples/synthetic_dry_run`: valid and invalid synthetic technical fixtures.
- `examples/in_a_grove_walkthrough`: author-only walkthrough demonstration.
- `research/position_note`: position-note draft and claim-boundary materials.
- `research/future_human_study`: deferred human-study ethics and protocol drafts.
- `artifacts`: frozen position-note and future-study packages.

## Research Status

Implemented: Core schema objects, validation, provenance records, lock verification, comparison helpers, reporting helpers, synthetic dry run, and an author-only walkthrough.

Demonstrated: representational feasibility, local artifact auditability, deterministic lock checks, and structured comparison of author/model records in one literary walkthrough.

Deferred: empirical human-exposure study, independent participant review, institution-specific ethics approval, and legal publication review for source-text redistribution.

Not established: interpretive truth, model error, model overconfidence, causal effects of AI exposure, prevalence, generalisability, reliability, or a validated detector.

## Legacy TRIM

The original TRIM project is archived in Git history and the `legacy-trim-v0.2.1` reference. It is no longer part of the active package.

## Citation

See `CITATION.cff`.
