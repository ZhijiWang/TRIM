# Core Indexing Migration Note

The current `trim_haa.provenance.annotation_index()` implementation may silently
overwrite an earlier annotation when duplicate `annotation_id` values are
supplied. That implementation is intentionally unchanged: its exact bytes are
hash-pinned by historical execution validation and the frozen public walkthrough.
Changing it in place would break reproducibility checks for those frozen records.

New code should not expand reliance on the silent-overwrite behavior. A
version-1 strict API is defined in the
[versioned strict indexing design](versioned_strict_indexing_design.md) and
rejects duplicate identifiers explicitly. The
[active identifier indexing audit](active_identifier_indexing_audit.md) records
the completed caller classification: proven active non-frozen Core-annotation
callers have migrated, frozen historical callers remain on the legacy path, and
non-annotation record indexes remain deferred for contract-specific design.

A future Core record-version decision still needs an explicit compatibility
policy before strict indexing becomes the default for a new Core version.

This note does not mark duplicate indexing as resolved. No pinned hash, frozen
artifact, study gate, or historical record is changed by the non-frozen Core
correctness work.
