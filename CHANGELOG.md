# Changelog

## 0.2.2 - Unreleased

### Added

- Versioned v0.2.2 coder package, freeze record, deployment checklist, migration
  note, execution protocol, return-manifest template, frozen file hash manifest,
  and AI dry-run archive record. The v0.2.2 coder package SHA-256 is
  `3b3ac302d8491e429d20b1d4fb1c66351ad0e6340698b2f5cd683adb5e0d4cb4`.
- Cross-file warning
  `QUESTION_CHANGED_CODE_BUT_LOW_UNCERTAINTY` for cases where an interpretive or
  definitional question changed the code but the final annotation uses low
  uncertainty and no complete alternative signature.

### Changed

- Removed `cue_family` and `broad_function_family` from the v0.2.2 coder-facing
  coding template. Schema support remains for backward compatibility and
  researcher-facing descriptive metadata.
- Clarified that question-log entries should be recorded when questions arise,
  with self-resolved questions included and batch-created timestamps disclosed.
- Bumped source and citation metadata to 0.2.2 without creating a formal
  release.

### Preserved

- v0.2.1 frozen package and SHA-256
  `012a71280f46cdb2327a6a90d3f4eb788ec44258eea56dfad70a06c6f3467ade`.
- Formal cases, source-text segments, source provenance, controlled
  vocabularies, shared-context structure, evidence-selection rules, no-fit
  rules, and uncertainty definitions.

## 0.2.1 - Unreleased

### Added

- Pilot-informed v0.2.1 codebook, friction-locus manual, mechanism manual,
  discourse-level guide, onboarding, workflow, retest protocol, coder guide,
  traceability report, and locked v0.2.0 pilot results report.
- Out-of-sample 12-case v0.2.1 retest corpus with explicit language-access,
  scope, shared-context, segment, and copyright metadata.
- v0.2.1 retest coding template with `primary_evidence_segment_ids`,
  `context_segment_ids`, `evidence_highlight`, `language_access_mode`,
  `case_scope`, `shared_context_ids`, `cross_case_context_permitted`, and
  `required_context_segments`.
- Revised question-log and language-access templates.
- Public pilot archive manifests and SHA-256 records for privately retained
  locked submissions, interview, and adjudication files.
- Reproducible coder-facing ZIP package builder with leakage checks and
  checksum output, shared-context referential-integrity checks, and
  semantic-steering audit reports.
- Shared-context registry for v0.2.1 retest cases.
- Source-text provenance table and source-text audit for all formal v0.2.1
  retest segments.
- Retest freeze record, external coder deployment checklist, execution
  protocol, return-manifest template, archive placeholders, and frozen
  coder-facing file hash manifest for package SHA-256
  `012a71280f46cdb2327a6a90d3f4eb788ec44258eea56dfad70a06c6f3467ade`.
- Researcher-facing retest manifest separated from the neutral coder-facing
  manifest.
- Intercoder evidence-overlap metrics, primary/context overlap reporting,
  compatible single-versus-compound agreement, language/scope strata, and
  adjudication-category columns that preserve raw disagreement.

### Changed

- Bumped source version and citation metadata to 0.2.1 without creating a
  formal release.
- Closed the repository's project-specific retest function-label vocabulary,
  including `no_fit`.
- Revised validation to support v0.2.1 primary/context evidence fields, shared
  context permissions, language-access metadata, uncertainty calibration
  warnings, question-log fields, and shared-context registry validation while
  preserving v0.2.0 `evidence_nodes` compatibility.
- Neutralized coder-facing retest metadata and source-packet summaries that
  could otherwise cue analytic choices.
- Replaced project-authored formal segment summaries in the v0.2.1 source
  packet with source text or documented public-domain translation text.
- Added `multi_passage_single_case` scope and moved the Othello distributed
  passage case out of the shared-context registry.
- Updated semantic-steering audit logic to allow verified source quotation
  matches only when backed by segment provenance.
- Reframed the completed v0.2.0 pilot as multilingual, translation- and
  summary-mediated usability evidence, not established reliability.

## 0.2.0 - Unreleased

### Added

- Optional source segmentation workflow and example data.
- Second-coder onboarding materials and template files.
- Coder-facing manual for `rationale_mechanism`.
- Minimal demonstration notebook.
- Methodological positioning and article-use documentation.
- Conceptual-neighbour positioning for within-label variation, LiveNLI, LiTEx,
  qualitative coding, provenance systems, and computational hermeneutics.
- Human-curated substantive interpretations for the two same-function
  demonstration groups.
- Compound-aware intercoder metrics for exact sets, primary mechanisms, any
  overlap, and Jaccard overlap.
- Optional `reliability` dependency group for scikit-learn-backed Cohen's
  kappa.
- Cross-language construct-validity protocol with separate layer-level
  annotation and pair-level comparison templates for recording original/gloss
  provenance outside the canonical signature.

### Changed

- Defined interpretive friction as a relational, evidence-constrained
  conversion difficulty.
- Clarified the distinction between `friction_locus` and `epistemic_support`,
  especially for `context_inference`.
- Marked `cue_function` as provisional/reserved and documented the
  demonstration status of all friction-locus values.
- Added a counterfactual, proximity, and explanatory-sufficiency protocol for
  selecting a dominant threshold.
- Reframed second-coder materials as three-case software demonstration and
  ten-case preliminary pilot infrastructure, not established reliability.
- Renamed generated comparison-table column `interpretive_payoff` to
  `comparison_prompt`. This is a deliberate output-schema migration: the
  software now emits structural prompts, while substantive interpretation is
  maintained separately.
- Bumped the package and citation metadata to 0.2.0 without creating a GitHub
  Release.
- Made contested-case rationale validation language-neutral, with a 60-character
  minimum when `alternative_signature` is present.
- Required at least one evidence node for standard annotations and made graph
  construction reject zero-evidence or incomplete anchor records.
- Defined `evidence_anchor` as source-facing location and `anchor_node` as the
  normalized analytic node label; both remain required.
- Unified standalone, record, and DataFrame signature validation through the
  canonical vocabulary helpers.
- Made `trim validate` return status 1 for validation errors after writing its
  report, with `--always-zero` for report-only pipelines.

### Removed

- Tracked macOS AppleDouble files and stale internal release-readiness reports.

## v0.1.1

TRIM v0.1.1 prepares the package for public research software release as a
Digital Humanities annotation support tool.

### Added

- Controlled vocabulary validation for threshold-rationale fields.
- Friction signature parsing and formatting.
- Comparison utilities for same-function, same-cue, broad-family, and contested
  case tables.
- Graph export to GraphML and node-link JSON.
- Intercoder comparison utilities for future multi-coder annotation projects.
- Demonstration dataset with ten annotations from Zuo zhuan, Macbeth, and In a
  Grove.
- Friction locus coding manual for human coders.
- Codebook documenting schema scope, controlled fields, compound values, and the
  human review workflow.

### Documentation

- Added coder-facing documentation for `friction_locus`.
- Added package scope documentation for schema conformance, comparability, and
  reviewable annotation.
- Added citation metadata and MIT license.

### Validation

- Test suite covers schema objects, validation behavior, comparison utilities,
  graph export, intercoder utilities, and command-line entry points.
