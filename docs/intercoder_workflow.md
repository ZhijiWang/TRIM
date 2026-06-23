# Intercoder Workflow

## Purpose

The intercoder workflow prepares independently completed annotations for
comparison. It supports field-level agreement checks, disagreement tables, and
human review of contested thresholds.

It is pilot infrastructure. The included files do not constitute a completed
reliability study.

## Preparing Files

1. Prepare a primary-coder CSV using the TRIM schema.
2. Prepare a second-coder CSV using the same schema and the same `case_id`
   values.
3. Use distinct `coder_id` values, such as `primary_coder` and `second_coder`.
4. Keep source segments and coding manuals available during independent coding.

The template `data/second_coder_template.csv` provides a three-case software and
onboarding demonstration for the In a Grove examples.
`data/demo_annotations_second_coder_template.csv` provides the ten
demonstration case IDs as a schema scaffold. It does not itself provide the
blinded source packet needed for a broader preliminary usability pilot.

## Comparing Fields

The module `trim.intercoder` provides:

- `pivot_coder_annotations(df, field)`
- `percent_agreement(df, field)`
- `pairwise_agreement(df, field)`
- `compound_value_metrics(left, right)`
- `pairwise_compound_agreement(df, field)`
- `cohen_kappa_if_two_coders(df, field)`
- `disagreement_table(df, fields)`
- `contested_disagreement_report(df)`

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

`pairwise_agreement` compares raw strings and remains useful for simple
controlled fields. For compound fields such as `rationale_mechanism`, the
compound-aware report adds:

- exact-set agreement, which treats the compound as an unordered set and
  ignores value order;
- primary-mechanism agreement, which compares the first ordered mechanism;
- any-overlap agreement;
- mean Jaccard overlap.

This preserves the distinction between `authorizes+reframes` and
`reframes+authorizes`: they have exact-set agreement because order is ignored
for that metric, but not primary-mechanism agreement because their first
ordered mechanisms differ.

## Reviewing Disagreements

Disagreements should be inspected as reviewable thresholds. Reviewers can ask:

- Is the source location clear?
- Is each coder's rationale coherent?
- Does the disagreement resist simple refinement?

The function `contested_disagreement_report` creates these human-review columns
for later adjudication.

Independent coding must be completed before adjudication. Initial metrics and
disagreement tables should be preserved, then reviewers can discuss whether
manual clarification or a contested annotation is warranted.

## Demonstration Script

`examples/run_intercoder_demo.py` checks the template format and writes a short
intercoder preparation report. The three-case run verifies software preparation
only. A ten-case run can identify usability and boundary problems, but cannot
establish domain-general or population-level reliability.
