# Intercoder Workflow

## Purpose

The intercoder workflow compares independently completed TRIM annotations. It produces field-level agreement measures, compound-mechanism reports, disagreement tables, and a preserved record for adjudication.

## Preparing Files

1. Prepare primary- and second-coder CSV files with the same TRIM schema and `case_id` values.
2. Assign distinct `coder_id` values.
3. Preserve the independently completed files before comparison.
4. Keep the source packet and coding manuals available for later review.

The ten-case pilot uses:

- `data/blinded_pilot_source_packet.md`
- `data/blinded_pilot_case_manifest.csv`
- `data/blinded_pilot_coding_template.csv`

The three-case templates remain useful for software demonstration and onboarding.

## Comparison Utilities

The module `trim.intercoder` provides:

- `pivot_coder_annotations(df, field)`
- `percent_agreement(df, field)`
- `pairwise_agreement(df, field)`
- `compound_value_metrics(left, right)`
- `pairwise_compound_agreement(df, field)`
- `cohen_kappa_if_two_coders(df, field)`
- `disagreement_table(df, fields)`
- `contested_disagreement_report(df)`

Install Cohen's kappa support with:

```bash
python -m pip install -e ".[reliability]"
```

Example:

```python
import pandas as pd
from trim.intercoder import (
    disagreement_table,
    pairwise_agreement,
    pairwise_compound_agreement,
)

primary = pd.read_csv("data/demo_annotations.csv", dtype=str, keep_default_na=False)
second = pd.read_csv("data/second_coder_completed.csv", dtype=str, keep_default_na=False)
combined = pd.concat([primary, second], ignore_index=True)

print(pairwise_agreement(combined, "friction_locus"))
print(pairwise_compound_agreement(combined, "rationale_mechanism"))
print(disagreement_table(combined, ["friction_locus", "rationale_mechanism"]))
```

## Reading Agreement

Simple controlled fields use exact string agreement. Compound mechanisms require several views:

- exact-set agreement;
- primary-mechanism agreement;
- any-overlap agreement;
- mean Jaccard overlap;
- order differences where the same values appear in a different sequence.

This keeps `authorizes+reframes` and `reframes+authorizes` analytically distinct. They share the same set of mechanisms while assigning a different primary operation.

## Reviewing Disagreement

Each disagreement is traced to the point where the annotations diverge: evidence selection, anchor construction, function assignment, locus, mechanism, support, discourse level, temporality, uncertainty, or compound order.

`contested_disagreement_report` prepares review columns for source clarity, rationale coherence, and adjudication. The original metrics and disagreement tables remain archived before discussion begins.

Plural-reading disagreements receive their own count and remain visible alongside the agreement results. They contribute to the case analysis without altering the pre-adjudication agreement rate.

## Demonstration Script

`examples/run_intercoder_demo.py` checks the template format and writes a short preparation report. The three-case run verifies the software workflow. The ten-case pilot evaluates manual usability, field boundaries, and three pre-specified comparative patterns. A larger out-of-sample study will evaluate stability across a broader corpus.
