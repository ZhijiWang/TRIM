# Human-LLM Pilot Freeze Report

Status: `BLOCKED_PENDING_RIGHTS_PRIVATE_PACKETS_MODEL_ACCOUNT_RUNTIME_SETTINGS_PRICING_AND_FINAL_EXECUTION_AUTHORIZATION`. This PR is execution-preparation only. No researcher coding, human annotation record, model call, model output, empirical agreement calculation, or findings were created.

## Component Status

- sample_freeze_status: `FROZEN_WITH_COUNT_RECONCILIATION`
- source_packet_freeze_status: `BLOCKED_PUBLIC_TEXT_REDACTED_PENDING_RIGHTS_AND_PRIVATE_PACKET_AUDIT`
- rights_freeze_status: `BLOCKED_RIGHTS_REVIEW_REQUIRED`
- private_packet_status: `BLOCKED_PRIVATE_PACKET_AUDIT_REQUIRED_BEFORE_CODING`
- manual_freeze_status: `MANUAL_COMPATIBILITY_PASSED_AUTHORITATIVE_FOR_PROTOCOL_REVIEW`
- prompt_freeze_status: `STATIC_PROMPT_SCHEMA_AND_ASSEMBLY_COMPATIBLE_EXECUTION_BLOCKED_PENDING_RIGHTS_PRIVATE_PACKETS_MODEL_ACCOUNT_RUNTIME_SETTINGS`
- static_prompt_schema_status: `PASSED_MODEL_RESPONSE_SCHEMA_COMPATIBILITY_EXECUTION_BLOCKED`
- prompt_assembly_status: `PASSED_PROMPT_ASSEMBLY_SPECIFIED_EXECUTION_BLOCKED`
- model_response_enrichment_status: `PASSED_CONTRACT_SPECIFIED_EXECUTION_BLOCKED`
- human_model_content_comparability_status: `PASSED_IDENTICAL_SOURCE_AND_MANUAL_CONTENT_WITH_DOCUMENTED_ACCESS_AFFORDANCE_ASYMMETRIES_EXECUTION_BLOCKED`
- condition_manipulation_status: `PASSED_SHARED_BASELINE_WITH_DECLARED_INSTRUCTION_DEPTH_INCREMENTS_EXECUTION_BLOCKED`
- runtime_settings_status: `BLOCKED_PENDING_PROVIDER_ACCOUNT_VERIFICATION`
- pricing_status: `BLOCKED_PENDING_PROVIDER_ACCOUNT_PRICING_RECHECK`
- model_freeze_status: `BLOCKED_PENDING_ACCOUNT_AVAILABILITY_VERIFICATION`
- allocation_freeze_status: `FROZEN_ARITHMETIC_CLARIFIED_EXECUTION_BLOCKED_PENDING_RIGHTS_PRIVATE_PACKETS_MODEL_ACCOUNT`
- governance_status: `not_yet_formally_determined`
- overall_execution_readiness: `BLOCKED_PENDING_RIGHTS_PRIVATE_PACKETS_MODEL_ACCOUNT_RUNTIME_SETTINGS_PRICING_AND_FINAL_EXECUTION_AUTHORIZATION`

No human coding may begin from this package.

## Manual Reference

- Manual status: `AUTHORITATIVE_FOR_PROTOCOL_REVIEW`
- Manual merge commit: `6364add9a89f3fe6d26043727b9d44cb21a76db0`
- Markdown: `docs/manuals/friction_locus_manual_v0_1.md` / `f26f5de05819c4fd36c0d88e7d86320d7374c27185c36575b18b584fc5d9b426`
- JSON: `docs/manuals/friction_locus_manual_v0_1.json` / `797d79fcdb29fc32850c3778c6afb029ac0768207ea33f66d714fe8fa8cb591a`
- Manifest: `docs/manuals/friction_locus_manual_manifest.json` / `1b80c0931a0ed8159aaeeb6e7b348331beb33130776469f223ae2a8cfe89d8de`
- Schema: `schemas/human_llm_coder_output.schema.json` / `2abdf5f5690aada67f1694f8d83dfe95236fbcba46c1bbcfca169567dbda7b12`

Manual authority is resolved for protocol review only. This is not empirical validation, coder-reliability validation, ontology validation, or execution authorization.

## Candidate-Universe Definition

Layer 1 uses a bounded held-out same-domain universe: public-domain literary and narrative passages from named Project Gutenberg editions, excluding the released In a Grove walkthrough, public demos, manual examples, direct manual-development examples, direct friction-locus definition examples, counterfactual-test development examples, and predicted-confusion construction examples.

Layer 2 uses a bounded transfer universe: public-domain working translations of classical, scriptural, medieval, and frame-narrative material. It is transfer/external application, not an uncontaminated layer. The study does not claim any source is unknown to the model.

## Screening Reconciliation

- Candidate rows screened: 30
- Eligible candidates: 26
- Ineligible candidates: 4
- Eligible but not selected candidates: 1
- Selected candidates: 25
- Arithmetic: 30 = 25 selected + 1 eligible-not-selected + 4 ineligible.
- Eligibility exclusion counts: `EXCL_CONTEXT_TOO_LARGE` = 3; `EXCL_TRANSLATION_UNRESOLVED` = 1.
- Post-eligibility non-selection counts: `NOT_SELECTED_DUPLICATE_STRUCTURE` = 1.
- Selection method: eligibility-threshold census at target layer size after pre-label screening; no anticipated labels, expected disagreement, or friction_locus values were used.
- Random seed: 20260702 for case-order allocation.

## Source Packets, Rights, and Private Packets

Public source packet count: 25. Public source packets contain metadata only. Full passage text and translation text are redacted pending edition-specific and translation-specific rights review. Controlled private packet handling remains blocked pending audit. The future researcher and model must receive identical controlled private source layers after rights review and private-packet audit.

## Prompt Bundle

- Prompt bundle status: `BLOCKED_NOT_EXECUTION_READY`
- Manual compatibility: passed.
- Static prompt/schema compatibility: passed for the model-authored response schema.
- Prompt assembly: specified, hashable, and non-self-referential; execution still blocked.
- Model response enrichment contract: specified.
- Human/model content comparability: identical source/manual content with documented access affordance and metadata asymmetries.
- Condition manipulation: renamed and frozen as shared structured annotation baseline with increasing levels of interpretive guidance.
- Condition C: full authoritative JSON manual injection specified.
- Difference audit: `docs/studies/human_llm_prompt_condition_audit.md`
- Prompt parity audit: `docs/studies/pr18_prompt_parity_audit.md`
- Prompt assembly spec: `docs/studies/human_llm_prompt_assembly_spec.md`
- Model enrichment contract: `docs/studies/model_record_enrichment_contract.md`
- Human access spec: `docs/studies/human_coder_access_and_record_spec.md`
- Condition manipulation audit: `docs/studies/pr18_condition_manipulation_audit.md`
- Prompt contamination audit: `docs/studies/pr18_prompt_contamination_audit.md`
- Browsing/tools: disabled.
- Session isolation: retained as a future execution rule.
- Assembled prompt hash: harness-only metadata, not model-visible.
- Model response candidate coverage: exact eight-category set enforced.

## Model Specification

- Original recorded model ID: `gpt-5.4-mini`
- Account availability: not verified because no authenticated OpenAI API credential was available in this environment.
- Frozen execution model: `UNRESOLVED_PENDING_OFFICIAL_VERIFICATION`
- Model freeze status: `BLOCKED`
- Cost estimate status: not final.

## Allocation, Stability, and Ablation

- Allocation ID: `human_llm_pilot_design_b_allocation_v0_1_2026_07_02`
- Primary condition: one Condition C run for all cases after all human records are locked.
- Ablation subset size: 6 cases; conditions A/B/C in separate isolated sessions.
- Stability interpretation: three additional Condition C stability runs beyond the primary run for each selected case.
- Planned runs: 25 primary + 75 additional stability + 18 ablation = 118.
- The primary run is not double-counted in the stability-run count.
- No case receives model execution before its human record is locked.

## Governance Status

- Protocol design: Design B.
- External human recruitment: prohibited.
- Participant data collection: none.
- Institutional status: `not_yet_formally_determined`.
- Formal ethics exemption claimed: false.
- Privacy review: not yet formally determined.
- Rights review: blocked for public redistribution.

## Unresolved Execution Blockers

- Clear source and translation redistribution rights or keep full packets in controlled private storage only.
- Establish compliant controlled private source-packet handling and audit private packet validity before coding.
- Verify the execution model against the authenticated account and freeze endpoint/settings.
- Obtain final execution authorization after prompt, model, rights, and private-packet gates pass.

## Non-Execution Confirmation

- Human coding occurred: no.
- Model called: no.
- Model outputs created: no.
- Empirical agreement calculated: no.
- Findings generated: no.
- Private packets inspected in this task: no.
- Released walkthrough artifacts modified: no.
