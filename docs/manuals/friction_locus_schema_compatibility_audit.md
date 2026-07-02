# Friction Locus Schema Compatibility Audit

Status: compatible.

- Every manual value is accepted by `schemas/human_llm_coder_output.schema.json`: yes.
- `unresolved` handling is represented by the schema: yes.
- `requires_human_review` operational status is represented by the schema: yes.
- Counterfactual-test fields can represent manual tests: yes (`test_id`, `question`, `answer`, `cited_evidence`, `effect_on_decision`, `confidence`).
- Alternative pathways can be recorded: yes (`alternative_pathways`).
- Manual requirement lacking a schema field: none identified for v0.1.
- Core and provenance schemas were not modified.
