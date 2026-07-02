# Human-LLM Pilot Freeze Report

Status: execution-preparation freeze only. No researcher coding, human annotation record, model call, model output, empirical agreement calculation, or findings were created.

## Candidate-Universe Definition

Layer 1 uses a bounded held-out same-domain universe: public-domain literary and narrative passages from named Project Gutenberg editions, excluding the released In a Grove walkthrough, public demos, manual examples, direct manual-development examples, direct friction-locus definition examples, counterfactual-test development examples, and predicted-confusion construction examples. The source universe is `L1_PG_HELD_OUT_NARRATIVE_2026_07_02`.

Layer 2 uses a bounded transfer universe: public-domain English working translations of classical, scriptural, medieval, and frame-narrative material. The source universe is `L2_CLASSICAL_TRANSFER_PD_TRANSLATIONS_2026_07_02`. It is classified as transfer/external application, not uncontaminated model exposure. Researcher prior familiarity is recorded for every candidate.

The study does not claim any source is unknown to the model.

## Screening Summary

- Candidate rows screened: 30
- Eligible selected cases: 25
- Excluded or not selected candidates: 5
- Exclusion counts by reason: {'EXCL_CONTEXT_TOO_LARGE': 3, 'EXCL_DUPLICATE_STRUCTURE': 1, 'EXCL_TRANSLATION_UNRESOLVED': 1}
- Selection method: eligibility-threshold census at target layer size after pre-label screening; no anticipated labels, expected disagreement, or friction_locus values were used.
- Random seed: 20260702; used for case-order allocation. No down-sampling was needed after eligibility because selected eligible counts matched layer targets.

## Final Selected Sample

- Total selected sample: 25
- Layer 1 held-out same-domain cases: 15
- Layer 2 transfer cases: 10
- Layer 1 case IDs: L1_AUSTEN_PNP_001, L1_SHELLEY_FRANK_001, L1_DICKENS_GE_001, L1_BRONTE_JE_001, L1_WILDE_DG_001, L1_JAMES_TS_001, L1_STEVENSON_JH_001, L1_POE_TELLTALE_001, L1_HAWTHORNE_SL_001, L1_CHOPIN_AWAKENING_001, L1_HARDY_TESS_001, L1_MELVILLE_BARTLEBY_001, L1_WHARTON_MIRTH_001, L1_COLLINS_MOONSTONE_001, L1_CONRAD_SECRET_001
- Layer 2 case IDs: L2_HOMER_ODYSSEY_001, L2_SOPHOCLES_ANTIGONE_001, L2_HERODOTUS_SCYTHIAN_001, L2_BIBLE_GENESIS_001, L2_BIBLE_SAMUEL_001, L2_AESOP_001, L2_OVID_DAPHNE_001, L2_MALORY_MORTE_001, L2_BEOWULF_DRAGON_001, L2_ARABIAN_NIGHTS_001

## Language, Familiarity, and Rights

- Language distribution: {'English': 15, 'English translation from Ancient Greek': 3, 'English translation from Biblical Hebrew': 2, 'English translation from Greek/Latin fable tradition': 1, 'English translation from Latin': 1, 'English/Middle English public-domain edition': 1, 'English translation from Old English': 1, 'English translation from Arabic/Persian narrative tradition': 1}
- Researcher-familiarity distribution: {'casual_familiarity': 25}
- Rights status: selected packets use Project Gutenberg public-domain source files or public-domain-translation working text layers with source-specific rights notes. Public release or redistribution beyond study review still requires rights review.

## Frozen Sources

- Source packet count: 25
- Source manifest: `data/studies/human_llm_pilot/source_manifest.csv`
- Source manifest SHA-256: `a94e61123573083f89f10074c38980bd7d04117ae7e1dac34d40014bf62b6b34`
- Selection log SHA-256: `91a53729693b26e610a6c0325c8d1c1d881654a6023381dcae5075163773c540`
- Researcher and model text-layer rule: identical frozen source packet layers for direct comparison.
- Source packets include no expected label, no friction_locus, no manual hints, no secondary scholarship, no researcher interpretation, and no model-facing instructions.

## Manual Freeze

- Manual version: `human_llm_friction_locus_manual_v0_1_design_b_freeze_2026_07_02`
- Manual path: `docs/studies/human_llm_friction_locus_pilot_protocol.md`
- Manual commit: `6998175eeca5d349072bf31012c69f2d568f28ec`
- Manual hash: `ca32a16b2dcc16f4d8a025c02a470278f57222c259347689feafd7f594b6e6d8`
- Category definitions hash: `0679a65fc13957f4f13931f31d840f9fbbbbb1ca71d568eda0c3d7e1f246252f`
- Predicted-confusions hash: `dc74ae5f84b626c4ad7fa598e50f0c6f52fced0e3bc7345d07ddbe308e4fb027`
- Output schema hash: `4ce445c04f349cd376f2104dc51df6b66c0f0f31930c634ea18e9576d0633235`

## Prompt Bundle

- Prompt bundle version: `human_llm_pilot_prompts_v0_1_2026_07_02`
- System prompt hash: `879fd81bf2571880e8ae63ec8c9397d589817188dc3f1389d54d251925fdc918`
- Condition A hash: `6af92aee8ab8ad8a20c809f6d35484a255dd91ae84a99becbb1abfb73cfdbe3e`
- Condition B hash: `8f635cb2b576f8fe0fc70611a228dbada8a0bfde67fe671108597721606b8ea7`
- Condition C hash: `22c3ed8b332187f440ffa6f1df4ce75d145541357e79e53397673d1fda775d38`
- User prompt template hash: `14552ba57aa8a753fa19ac3dab47a6540b4e94acf94e13504ef51620958d56e1`
- Browsing/tools: disabled.
- Session isolation: fresh stateless session for every case-condition-run.

## Model Specification

- Provider/model: OpenAI `gpt-5.4-mini`
- Decoding: temperature 0, top_p 1, max output tokens 4000.
- Provider-version limitation: Provider-side model weights, safety layers, and service configuration may change and cannot be fully reconstructed from the frozen local materials alone.

## Allocation, Stability, and Ablation

- Allocation ID: `human_llm_pilot_design_b_allocation_v0_1_2026_07_02`
- Allocation hash: `26de231340ede2c8aeb4197c8fdd3630741d5baf1eefc7244ac41dbc1d478d24`
- Primary condition: one Condition C run for all cases after all human records are locked.
- Ablation subset size: 6 cases; conditions A/B/C in separate isolated sessions.
- Stability design: 3 stability runs per selected case under Condition C.
- No case receives model execution before its human record is locked.

## Cost Ceiling

- Estimated upper-bound cost: USD 3.02
- Hard spending ceiling: USD 25.00
- Pricing note: Uses OpenAI API documentation observed on 2026-07-02 for gpt-5.4-mini: $0.75/input MTok and $4.50/output MTok. Pricing must be re-verified immediately before execution.

## Governance Status

- Protocol design: Design B.
- External human recruitment: prohibited.
- Participant data collection: none.
- Institutional status: `not_yet_formally_determined`.
- Formal ethics exemption claimed: false.
- Privacy review: no private or participant data planned; institutional privacy review not yet formally determined
- Rights review: source-level rights recorded for execution preparation; formal publication rights review still required

## Unresolved Execution Blockers

- Verify source-specific redistribution rights before public packet release.
- Verify model availability and current pricing immediately before execution.
- Complete and lock all researcher human records before any model execution.
- Preserve raw model outputs and run manifests when execution later occurs.

## Non-Execution Confirmation

- Human coding occurred: no.
- Model called: no.
- Model outputs created: no.
- Empirical agreement calculated: no.
- Findings generated: no.
- Released walkthrough artifacts modified: no.
