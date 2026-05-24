# Intercoder Workflow

## Purpose

The intercoder workflow prepares independently completed annotations for
comparison. It supports field-level agreement checks, disagreement tables, and
human review of contested thresholds.

## Preparing Files

1. Prepare a primary-coder CSV using the TRIM schema.
2. Prepare a second-coder CSV using the same schema and the same `case_id`
   values.
3. Use distinct `coder_id` values, such as `primary_coder` and `second_coder`.
4. Keep source segments and coding manuals available during independent coding.

The template `data/second_coder_template.csv` provides a three-case pilot
format for the In a Grove examples.

## Comparing Fields

The module `trim.intercoder` provides:

- `pivot_coder_annotations(df, field)`
- `percent_agreement(df, field)`
- `pairwise_agreement(df, field)`
- `cohen_kappa_if_two_coders(df, field)`
- `disagreement_table(df, fields)`
- `contested_disagreement_report(df)`

Example:

```python
import pandas as pd
from trim.intercoder import disagreement_table, pairwise_agreement

primary = pd.read_csv("data/demo_annotations.csv", dtype=str, keep_default_na=False)
second = pd.read_csv("data/second_coder_completed.csv", dtype=str, keep_default_na=False)
combined = pd.concat([primary, second], ignore_index=True)

print(pairwise_agreement(combined, "friction_locus"))
print(disagreement_table(combined, ["friction_locus", "rationale_mechanism"]))
```

## Reviewing Disagreements

Disagreements should be inspected as reviewable thresholds. Reviewers can ask:

- Is the source location clear?
- Is each coder's rationale coherent?
- Does the disagreement resist simple refinement?

The function `contested_disagreement_report` creates these human-review columns
for later adjudication.

## Demonstration Script

`examples/run_intercoder_demo.py` checks the template format and writes a short
intercoder preparation report. Completed second-coder data can be substituted
for the template in future reliability pilots.
