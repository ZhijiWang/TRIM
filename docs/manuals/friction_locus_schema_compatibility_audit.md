# Friction Locus Schema Compatibility Audit v0.1

Status: `compatible`

The study-specific schema `schemas/human_llm_coder_output.schema.json` now structurally represents the manual-required procedure. This is a study schema only; Core and provenance schemas are unchanged.

Schema hash: `2abdf5f5690aada67f1694f8d83dfe95236fbcba46c1bbcfca169567dbda7b12`

| Manual requirement | Exact field(s) | Enforcement | Status | Notes |
|---|---|---|---|---|
| proposed locus | `friction_locus_proposed` | JSON Schema enum plus validator cross-field checks | compatible | Allows eight substantive categories plus `unresolved`/null. |
| candidate set | `candidate_loci[]` | JSON Schema exact contains/min/max plus validator set equality | compatible | Exactly eight entries, one per substantive category. |
| candidate state | `candidate_loci[].state` | JSON Schema enum | compatible | `candidate_supported`, `candidate_not_supported`, `insufficient_evidence`, `not_applicable`. |
| supported candidate evidence | `candidate_loci[].cited_evidence` | JSON Schema conditional plus validator | compatible | Supported candidates require at least one evidence ID. |
| final operational label | `final_operational_label` | JSON Schema plus validator | compatible | Review-required proposals force `unresolved`. |
| operational status | `friction_locus_operational_status` | JSON Schema enum plus validator | compatible | Includes `accepted_for_analysis`, `requires_human_review`, `unresolved`, `not_supplied`. |
| unresolved | `friction_locus_proposed`, `friction_locus_operational_status`, `final_operational_label` | JSON Schema plus validator | compatible | Unresolved is not allowed as a candidate category. |
| escalation | `escalation_required`, `escalation_reason` | JSON Schema plus validator | compatible | Reserved/review-sensitive model proposals force escalation. |
| alternative pathways | `alternative_pathways[]` | JSON Schema | compatible | Separate from uncertainty and unresolved. |
| uncertainty | `uncertainty` | JSON Schema enum | compatible | Separate from alternatives and escalation. |
| counterfactual tests | `counterfactual_tests[]` | JSON Schema | compatible | Test ID, question, answer, evidence, effect, confidence are structured. |
| review policy applied | `review_policy_applied` | JSON Schema object plus validator cross-field rules | compatible | Category, status, trigger, review requirement, and final label before review are structured. |
| original proposal preservation | `record_id`, `record_hash`, `review_of_record_id`, `review_of_record_hash`, separate record requirement | JSON Schema plus validator plus protocol | compatible | Original records remain independently hashable; review records link rather than overwrite. |
| review-record linkage | `review_of_record_id`, `review_of_record_hash` | JSON Schema conditional plus validator | compatible | `adjudicator_separate_record` requires both fields. |
| separate later review event | `analyst_role = adjudicator_separate_record`, linkage fields, independent `record_id`/`record_hash` | JSON Schema plus validator plus protocol | compatible | Review record is a separate event. |

## Enforcement Classes

- JSON Schema-enforced: field presence, enum values, candidate array length, one entry for each substantive category, supported-candidate evidence minimum, adjudicator linkage presence, and basic hash syntax.
- Validator-enforced: candidate-order independence, cross-field policy matching, reserved/review-sensitive model proposal consequences, distinct review record IDs/hashes, cue_function positive-only rule, worked-record completeness, and manifest hash consistency.
- Protocol-enforced: actual immutability of a stored original record after a linked review event and independent final audit before coding begins.

No manual-required algorithmic state exists only in unstructured prose. `decision_path` may summarize the process but is not the authoritative store for candidate states or review policy application.
