# Changelog

This project is in alpha development. Entries describe repository and package
boundaries; they do not authorize research execution or human coding.

## Unreleased

- Fix non-frozen Core validation for parent relationships, retry counts, and
  timezone-aware chronological timestamps.
- Correct report label-change and explicit-boolean aggregation semantics, reject
  ambiguous duplicate stage rows, preserve Unicode rationale units, and make
  lock-manifest CLI selection fail closed.
- Remove duplicate legacy depth-field entries without changing their meaning.
- Preserve the frozen legacy `annotation_index()` behavior; a versioned strict
  duplicate-index migration remains deferred and is documented in
  [the Core indexing migration note](docs/core_indexing_migration_note.md).
- Repair the core-only Python source-distribution test boundary.
- Add repository-level third-party and content-rights disclosure.
- Document alpha release artifact boundaries and the unresolved older English
  walkthrough exclusion.
- Correct current pull-request lifecycle and provider-audit navigation.

## 0.3.0a1

- Establish the standalone `trim_haa` package and CLI.
- Preserve provenance, locking, comparison, and reporting helpers.
- Add synthetic and public technical demonstrations.
- Add blocked preparation scaffolds for the Design B Human-LLM pilot.

This changelog is not a substitute for frozen manifests, checksum records, or
component-specific release notes.
