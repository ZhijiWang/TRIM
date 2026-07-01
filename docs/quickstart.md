# Quickstart

Install from a checkout:

```bash
python -m pip install -e .
```

Use the package:

```python
from trim_haa import TrimHAAAnnotation, compare_annotations, validate_core_record

left = TrimHAAAnnotation(
    annotation_id="left",
    case_id="case",
    actor_id="human",
    actor_type="human",
    annotation_stage="human_pre",
    primary_evidence_segment_ids=("s1",),
    function_label="unresolved_agency",
    rationale_mechanism="contrast_or_tension",
    uncertainty_flag="medium",
    rationale_note="The record keeps an unresolved interpretive path visible.",
)

right = TrimHAAAnnotation(
    annotation_id="right",
    case_id="case",
    actor_id="model",
    actor_type="model",
    annotation_stage="ai_independent",
    primary_evidence_segment_ids=("s1", "s2"),
    function_label="self_inflicted_death",
    rationale_mechanism="direct_action",
    uncertainty_flag="low",
    rationale_note="The record emphasizes direct action.",
)

assert not validate_core_record(left)
comparison = compare_annotations(left, right)
```

Use the CLI:

```bash
trim-haa --help
trim-haa validate tests/fixtures/trim_haa/core_valid.csv
trim-haa compare examples/in_a_grove_walkthrough/author_analytic_record.csv examples/in_a_grove_walkthrough/ai_independent_record.csv
```
