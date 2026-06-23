# Intercoder Workflow

## Purpose

The intercoder workflow compares independently completed TRIM annotations. It produces field-level agreement, compound-mechanism reports, disagreement tables, and an adjudication record.

## Preparation

Prepare two files with the same schema and `case_id` values. Assign distinct `coder_id` values and preserve both completed files before comparison.

The ten-case pilot uses the source packet, case manifest, and coding template in `data/`. The three-case templates remain available for software demonstration.

## Comparison Utilities

`trim.intercoder` provides agreement, compound-overlap, kappa, disagreement, and contested-case reports. Install the optional reliability dependency with:

```bash
python -m pip install -e ".[reliability]"
```

Simple controlled fields use exact agreement. Compound mechanisms are read through exact-set agreement, primary-mechanism agreement, any-overlap agreement, mean Jaccard overlap, and order differences.

## Reviewing Disagreement

Each disagreement is traced to the first point of divergence: evidence, anchor, function, locus, mechanism, support, discourse level, temporality, uncertainty, or compound order. Initial outputs remain archived before adjudication begins.

Plural-reading disagreements receive a separate count. They remain visible in the case analysis and leave the pre-adjudication agreement rate unchanged.

## Reporting Scale

The three-case script verifies the software workflow. The ten-case pilot evaluates manual usability, field boundaries, and three pre-specified comparative patterns. A larger out-of-sample study will evaluate stability across a broader corpus.
