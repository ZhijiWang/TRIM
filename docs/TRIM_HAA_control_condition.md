# TRIM-HAA control condition

`human_second_pass_control` represents rereading without AI exposure.

The participant:

1. locks `human_pre`;
2. later rereads the same case;
3. sees no AI output;
4. may revise the original record;
5. submits a control second-pass record linked to `human_pre`.

The control condition estimates ordinary second-pass change. It helps separate post-AI change from rereading, task familiarity, and revision opportunity.

Control provenance must use:

- `ai_output_exposed=none`;
- `exposure_order=control_second_pass`;
- `interface_condition=control_review`;
- empty `exposed_ai_annotation_id`;
- empty `exposed_model_run_id`.

Prototype reports may describe:

```text
AI-associated change = post-AI change - second-pass control change
```

This is descriptive in the prototype. It is not a causal estimate from a single participant or synthetic dataset.
