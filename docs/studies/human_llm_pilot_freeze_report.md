# Human-LLM Pilot Freeze Report

Status: `BLOCKED`. This PR is execution-preparation only. No researcher coding, human annotation record, model call, model output, empirical agreement calculation, or findings were created.

## Component Status

- sample_freeze_status: `FROZEN_WITH_COUNT_RECONCILIATION`
- source_packet_freeze_status: `BLOCKED_PUBLIC_TEXT_REDACTED_PENDING_RIGHTS_AND_PRIVATE_PACKET_AUDIT`
- rights_freeze_status: `BLOCKED_RIGHTS_REVIEW_REQUIRED`
- manual_freeze_status: `BLOCKED_INCOMPLETE_AUTHORITATIVE_MANUAL`
- prompt_freeze_status: `BLOCKED_PENDING_AUTHORITATIVE_MANUAL_AND_ACCOUNT_VERIFIED_MODEL`
- model_freeze_status: `BLOCKED_PENDING_ACCOUNT_AVAILABILITY_VERIFICATION`
- allocation_freeze_status: `FROZEN_ARITHMETIC_CLARIFIED_EXECUTION_BLOCKED_PENDING_MANUAL_MODEL_RIGHTS`
- governance_status: `not_yet_formally_determined`
- overall_execution_readiness: `BLOCKED`

No human coding may begin from this package.

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

## Final Selected Sample

- Total selected sample: 25
- Layer 1 held-out same-domain cases: 15
- Layer 2 transfer cases: 10
- Layer 1 case IDs: L1_AUSTEN_PNP_001, L1_SHELLEY_FRANK_001, L1_DICKENS_GE_001, L1_BRONTE_JE_001, L1_WILDE_DG_001, L1_JAMES_TS_001, L1_STEVENSON_JH_001, L1_POE_TELLTALE_001, L1_HAWTHORNE_SL_001, L1_CHOPIN_AWAKENING_001, L1_HARDY_TESS_001, L1_MELVILLE_BARTLEBY_001, L1_WHARTON_MIRTH_001, L1_COLLINS_MOONSTONE_001, L1_CONRAD_SECRET_001
- Layer 2 case IDs: L2_HOMER_ODYSSEY_001, L2_SOPHOCLES_ANTIGONE_001, L2_HERODOTUS_SCYTHIAN_001, L2_BIBLE_GENESIS_001, L2_BIBLE_SAMUEL_001, L2_AESOP_001, L2_OVID_DAPHNE_001, L2_MALORY_MORTE_001, L2_BEOWULF_DRAGON_001, L2_ARABIAN_NIGHTS_001

## Language, Familiarity, and Rights

- Researcher-familiarity distribution after audit: no known prior reading = 1; title/general-cultural familiarity only = 15; prior casual reading = 9.
- No case was changed based on familiarity after selection.
- Public source packets now contain metadata only. Full passage text and translation text are redacted pending edition-specific and translation-specific rights review.
- Rights status: blocked for public redistribution until source-specific review is complete.

## Source Packets

- Public source packet count: 25
- Source manifest: `data/studies/human_llm_pilot/source_manifest.csv`
- Rights manifest: `data/studies/human_llm_pilot/source_rights_manifest.csv`
- Substantive audit: `data/studies/human_llm_pilot/source_packet_substantive_audit.csv`
- Public packets include no expected label, no friction_locus, no manual hints, no secondary scholarship, no researcher interpretation, and no model-facing instructions.
- The future researcher and model must receive identical controlled private source layers after rights review.

## Manual Freeze

- Manual status: `BLOCKED_INCOMPLETE_AUTHORITATIVE_MANUAL`
- Authoritative manual path: none identified.
- Active candidates audited: protocol, lineage table, predicted-confusions table, output schema.
- Historical candidates found: legacy TRIM friction_locus manuals in the archival tag at commit `252f4b1c867751bd996885ec674f5f546ddbc110`.
- Completeness result: no active authoritative current Design B manual contains all category definitions, use-when/use-another guidance, confusable-with guidance, counterfactual tests, decision tree, examples, reserved-category rules, and escalation rules.
- Gap report: `docs/studies/human_llm_manual_gap_report.md`

## Prompt Bundle

- Prompt bundle status: `BLOCKED_NOT_EXECUTION_READY`
- Condition A validity: blocked scaffold only.
- Condition B validity: blocked scaffold only.
- Condition C validity: invalid for execution pending authoritative manual.
- Difference audit: `docs/studies/human_llm_prompt_condition_audit.md`
- Browsing/tools: disabled in the scaffold.
- Session isolation: retained as a future execution rule.

## Model Specification

- Original recorded model ID: `gpt-5.4-mini`
- Official public documentation status: `gpt-5.4-mini` appears in current OpenAI model documentation and pricing documentation checked on 2026-07-02.
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

## Cost Ceiling

- Hard spending ceiling: USD 25.00
- Estimated upper-bound cost: not final.
- Pricing note: official public OpenAI documentation observed on 2026-07-02 lists `gpt-5.4-mini` standard text pricing, but account availability and execution pricing must be verified before any run.

## Governance Status

- Protocol design: Design B.
- External human recruitment: prohibited.
- Participant data collection: none.
- Institutional status: `not_yet_formally_determined`.
- Formal ethics exemption claimed: false.
- Privacy review: not yet formally determined.
- Rights review: blocked for public redistribution.

## Unresolved Execution Blockers

- Complete or identify the authoritative current Design B friction_locus manual.
- Clear source and translation redistribution rights or keep full packets in controlled private storage only.
- Verify the execution model against the authenticated account.
- Re-audit prompt/model compatibility after the manual and model are frozen.
- Complete private source-packet substantive validity review before coding.

## Non-Execution Confirmation

- Human coding occurred: no.
- Model called: no.
- Model outputs created: no.
- Empirical agreement calculated: no.
- Findings generated: no.
- Released walkthrough artifacts modified: no.
