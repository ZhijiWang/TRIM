# Friction Locus Schema Compatibility Audit

Status: `compatible_with_documented_protocol_constraint`.

This audit checks the study-specific coder schema, not the released Core or provenance schemas.

| Manual requirement | Schema field used | Compatibility result | Limitation |
| --- | --- | --- | --- |
| proposed locus | `friction_locus_proposed` | compatible | Field stores one proposed value or unresolved/null; candidate set is not stored here. |
| final operational label | `final_operational_label` | compatible | Schema permits string/null and protocol constrains unresolved for review-required cases. |
| operational status | `friction_locus_operational_status` | compatible | Enum includes `accepted_for_analysis`, `requires_human_review`, `unresolved`, `not_supplied`. |
| unresolved | friction_locus enum and `final_operational_label` | compatible | Manual distinguishes unresolved as final label from substantive proposed locus. |
| escalation | `escalation_required`, `escalation_reason` | compatible | Reason text must identify policy or evidence problem. |
| original proposal preservation | immutable record practice plus `record_hash` | compatible_with_documented_protocol_constraint | Schema does not by itself prevent mutation; locking and hashing enforce preservation. |
| alternative pathways | `alternative_pathways` | compatible | Supported with cited evidence and status. |
| uncertainty | `uncertainty` | compatible | Supported enum. |
| counterfactual test fields | `counterfactual_tests[].test_id/question/answer/cited_evidence/effect_on_decision/confidence` | compatible | Answer states are free text and constrained by manual, not schema enum. |
| candidate loci | `decision_path` and `counterfactual_tests` | compatible_with_documented_protocol_constraint | No dedicated `candidate_set` field exists. Candidate set must be encoded in decision path/test records. |
| review policy application | `friction_locus_operational_status`, `final_operational_label`, `escalation_required`, `escalation_reason`, `decision_path` | compatible_with_documented_protocol_constraint | No dedicated review_policy field exists. |
| separate later review record | `analyst_role = adjudicator_separate_record` for human records | compatible_with_documented_protocol_constraint | Schema lacks an explicit `original_record_id` linkage field; linkage must be documented externally or in rationale/record management. |

No Core schema or provenance schema change is made. A future study-schema revision may add dedicated `candidate_set`, `review_policy_applied`, and `review_of_record_id` fields, but this task documents the current constraint rather than modifying the schema.
