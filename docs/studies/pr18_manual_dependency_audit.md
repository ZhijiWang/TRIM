# PR #18 Manual Dependency Audit

Status: `completed_for_manual_reference_update`

| path | current reference | expected authoritative reference | status | required change | change completed |
|---|---|---|---|---|---|
| data/studies/human_llm_pilot/manual_freeze_manifest.json | BLOCKED_INCOMPLETE_AUTHORITATIVE_MANUAL | authoritative manual v0.1 merged at 6364add9 | stale | updated manual path/version/hashes/status | yes |
| data/studies/human_llm_pilot/prompt_bundle_manifest.json | UNRESOLVED_PENDING_AUTHORITATIVE_MANUAL | manual v0.1 and schema hashes | stale | updated prompt hashes and compatibility statuses | yes |
| data/studies/human_llm_pilot/prompt_condition_difference_audit.json | blocked scaffolds pending manual | manual-compatible depth audit, execution blocked | stale | updated audit status | yes |
| data/studies/human_llm_pilot/freeze_status.json | manual blocker listed | manual resolved, rights/private/model remain blocked | stale | updated component statuses | yes |
| prompts/human_llm_pilot/condition_C.txt | invalid pending manual | deterministic authoritative manual reference and full Condition C requirements | stale | rebuilt | yes |
| prompts/human_llm_pilot/condition_A.txt | blocked scaffold only | short definitions plus full structured schema output requirement | stale | rebuilt | yes |
| prompts/human_llm_pilot/condition_B.txt | blocked scaffold only | concise rules plus full structured schema output requirement | stale | rebuilt | yes |
| prompts/human_llm_pilot/system_prompt.txt | old schema field list missing candidate_loci/review fields | shared structured output fields from authoritative schema | stale | rebuilt | yes |
| prompts/human_llm_pilot/user_prompt_template.txt | blocked pending manual | manual-compatible blocked template | stale | rebuilt | yes |
| prompts/human_llm_pilot/human_researcher_instructions.txt | missing | human-side manual-compatible instruction record | stale | created | yes |
| docs/studies/human_llm_pilot_freeze_report.md | manual blocked | manual compatibility passed, execution still blocked | stale | updated | yes |
| docs/studies/human_llm_prompt_condition_audit.md | Condition C invalid pending manual | A/B/C compatible by depth, execution blocked | stale | updated | yes |
| docs/studies/human_llm_protocol_freeze_checklist.md | manual unchecked | manual compatibility checked; executable prompts/model/rights remain unchecked | stale | updated | yes |
| docs/studies/human_llm_manual_gap_report.md | active manual absent | superseded by PR #19 manual | stale | updated | yes |
| scripts/validate_human_llm_pilot_freeze.py | expected blocked manual | expected authoritative manual and prompt compatibility | stale | updated | yes |
| tests/test_human_llm_pilot_freeze.py | expected blocked manual | expected authoritative manual and blocked execution | stale | updated | yes |
| data/studies/human_llm_pilot/model_execution_spec.json | manual pending in prompt/model text | manual-compatible prompts, model/account still blocked | stale | updated | yes |
| data/studies/human_llm_pilot/governance_status.json | unresolved model/rights only | explicit private packet audit blocker added | compatible | updated unresolved items | yes |
| data/studies/human_llm_pilot/authoritative_manual_reference.json | missing | canonical manual reference block | stale | created | yes |
| data/studies/human_llm_pilot/freeze_package_manifest.json | missing | non-circular package manifest with manual/prompt/status hashes | stale | created | yes |

No authoritative manual files were edited in this PR #18 correction. Manual metadata is referenced through `data/studies/human_llm_pilot/authoritative_manual_reference.json`.
