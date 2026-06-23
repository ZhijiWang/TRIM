# Changelog

## 0.1.2 - Unreleased

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
- Bumped the package and citation metadata to 0.1.2 without creating a GitHub
  Release.

### Removed

- Tracked macOS AppleDouble files and stale internal release-readiness reports.

## v0.1.1

TRIM v0.1.1 prepares the package for public research software release as a
digital humanities annotation support tool.

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
