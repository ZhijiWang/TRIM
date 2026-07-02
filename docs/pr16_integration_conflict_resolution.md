# PR #16 Integration Conflict Resolution

## Merge inputs

- Head branch: `refactor/standalone-trim-haa`
- Starting head SHA: `2897382e634c93e0f5883784fb83f2eb43b60b6d`
- Integration branch merged: `origin/pilot-informed-v0.2.1`
- Integration branch SHA: `43104e3b6ef3279094244740bdc7a54904d0f008`
- Merge method: normal non-fast-forward merge commit
- Rebase, squash, and force-push: not used

## Resolution principles

The final tree follows the standalone TRIM-HAA architecture:

- active package under `src/trim_haa`;
- public API under `trim_haa`;
- standalone `trim-haa` CLI;
- legacy TRIM removed from the active tree;
- historical retest and legacy material preserved through Git history and reference history, not restored as active runtime content;
- frozen public walkthrough artifacts preserved without byte changes.

Conflicts were resolved path by path. No blanket one-sided resolution was used for the full conflict set.

## Conflict inventory

| Path | Conflict type | Classification | Final action | Justification |
| --- | --- | --- | --- | --- |
| `CHANGELOG.md` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy active-tree release history was removed by the standalone conversion; current release history is preserved through Git history and PR records. |
| `README.md` | content | C_MANUAL_SEMANTIC_MERGE | manually merged | Kept the standalone TRIM-HAA README and updated the public v0.2 description to match the current frozen walkthrough state without restoring legacy active-package claims. |
| `data/retest_v0_2_1_case_manifest.csv` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Retest active-workspace data is legacy TRIM material and is not required by the standalone package. |
| `data/retest_v0_2_1_coding_template.csv` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Retest active-workspace template is legacy TRIM material and is not required by the standalone package. |
| `data/retest_v0_2_1_research_manifest.csv` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Retest active-workspace manifest is legacy TRIM material and is not required by the standalone package. |
| `data/retest_v0_2_1_shared_context_registry.csv` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Retest active-workspace registry is legacy TRIM material and is not required by the standalone package. |
| `data/retest_v0_2_1_source_packet.md` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Retest active-workspace source packet is legacy TRIM material and is not required by the standalone package. |
| `docs/TRIM_codebook_v0_2_1.md` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy TRIM codebook was intentionally removed from active documentation by the standalone conversion. |
| `docs/retest_protocol_v0_2_1.md` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy retest protocol was intentionally removed from active documentation by the standalone conversion. |
| `docs/retest_v0_2_1_case_design_audit.md` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy retest audit material was intentionally removed from active documentation by the standalone conversion. |
| `docs/retest_v0_2_1_coder_guide.md` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy retest coder guide was intentionally removed from active documentation by the standalone conversion. |
| `docs/retest_v0_2_1_semantic_steering_audit.md` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy retest audit output was intentionally removed from active documentation by the standalone conversion. |
| `docs/schema_validation_migration.md` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy migration note described the pre-standalone TRIM validator boundary and is superseded by the standalone package documentation. |
| `outputs/coder_packages/TRIM_retest_v0_2_1_coder_package.SHA256SUMS.txt` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy retest package checksum output is not an active standalone TRIM-HAA artifact. |
| `outputs/coder_packages/TRIM_retest_v0_2_1_coder_package.zip` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy retest package output is not an active standalone TRIM-HAA artifact. |
| `outputs/coder_packages/TRIM_retest_v0_2_1_semantic_steering_audit.json` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy retest audit output is not an active standalone TRIM-HAA artifact. |
| `outputs/coder_packages/TRIM_retest_v0_2_1_semantic_steering_audit.txt` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy retest audit output is not an active standalone TRIM-HAA artifact. |
| `scripts/build_retest_v0_2_1_package.py` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy package builder is not part of the standalone `trim-haa` CLI or runtime. |
| `tests/test_retest_package.py` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy retest package test enforced removed active-tree behavior. Current tests cover standalone packaging and frozen artifacts. |
| `tests/test_validator.py` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | Legacy `trim.validator` test enforced the removed legacy package. Current tests cover `trim_haa`. |
| `trim/validator.py` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | The old `trim` implementation must not be restored as an active parallel package. |
| `trim/vocabulary.py` | modify/delete | A_INTENTIONAL_PR16_DELETION | deleted | The old `trim` implementation must not be restored as an active parallel package. |

## Files deleted intentionally

The conflict paths classified as `A_INTENTIONAL_PR16_DELETION` were deleted. In addition, integration-side retest additions from `pilot-informed-v0.2.1` were reviewed and not retained in the active standalone tree:

- `data/retest_v0_2_1_coder_return_manifest_template.csv`
- `data/retest_v0_2_1_frozen_file_hashes.csv`
- `data/retest_v0_2_1_source_text_provenance.csv`
- `docs/retest_v0_2_1_execution_protocol.md`
- `docs/retest_v0_2_1_external_coder_deployment_checklist.md`
- `docs/retest_v0_2_1_freeze_record.md`
- `docs/retest_v0_2_1_source_text_audit.md`
- `paper_planning/TRIM_article_outline.md`
- `paper_planning/TRIM_article_strategy.md`
- `paper_planning/TRIM_claim_evidence_matrix.md`
- `paper_planning/TRIM_empirical_analysis_plan.md`
- `paper_planning/TRIM_journal_fit_matrix.md`
- `paper_planning/TRIM_literature_positioning.md`
- `paper_planning/TRIM_reviewer_objections.md`
- `paper_planning/TRIM_title_abstract_options.md`
- `paper_planning/TRIM_v0_2_1_retest_results_shell.md`
- `pilot_archive/v0_2_1_retest/README.md`
- `pilot_archive/v0_2_1_retest/adjudication/README.md`
- `pilot_archive/v0_2_1_retest/checksums/README.md`
- `pilot_archive/v0_2_1_retest/comparison/README.md`
- `pilot_archive/v0_2_1_retest/submissions/README.md`

These files are preserved in the integration branch history but are not restored as active content in PR #16.

## Integration content preserved

The merge preserves PR #15 and `pilot-informed-v0.2.1` ancestry through the merge commit. No retest active-tree file was restored into the standalone package tree because doing so would reintroduce legacy TRIM boundaries that PR #16 intentionally removed.

## Manually merged files

- `README.md`: retained the standalone TRIM-HAA package description, CLI, and repository-structure boundary; updated the public v0.2 walkthrough sentence to describe the frozen locked-record comparison accurately.
- `docs/research_status.md`: updated the public walkthrough status from the earlier text-layer-only draft state to the current frozen locked-record comparison state, while preserving the non-empirical and non-truth-verdict boundaries.
- `tests/test_documentation_sync.py`: updated the obsolete documentation-sync assertion so it tests the current frozen public v0.2 status and its non-claim boundaries instead of the earlier draft text-layer status.

## Frozen-artifact verification

Pre-merge baseline verification passed for the public v0.2 author record, AI record, prompt, raw AI output, source segments, English gloss, comparison checksums, old frozen walkthrough hashes, Core schema, provenance schema, and position note.

Post-resolution verification is recorded in the final PR #16 integration report.

## Validation

- `git diff --cached --check`: passed before merge commit.
- `python3.11 -m pytest`: 117 passed before merge commit.
- `python3.12 -m pytest`: 117 passed before merge commit.
- Public v0.2 author and AI canonical lock hashes: verified with the repository locking helper.
- Frozen public v0.2 file hashes, comparison checksums, old frozen walkthrough hashes, schema files, and position-note hashes: verified unchanged before merge commit.
- Build, CLI smoke, post-push GitHub mergeability, and GitHub Actions results are reported in the PR #16 integration report.

## Remaining risks

- GitHub mergeability and Actions status must be rechecked after pushing the merge commit.
- The final PR #16 diff should be inspected to confirm that legacy retest active-tree material was not reintroduced.
- PR #16 must remain draft and unmerged until a separate final review and merge authorization step.
