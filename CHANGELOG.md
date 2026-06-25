# Changelog

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
  checksum output.
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
  warnings, and question-log fields while preserving v0.2.0 `evidence_nodes`
  compatibility.
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
