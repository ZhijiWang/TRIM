# Core Indexing Migration Note

The current `trim_haa.provenance.annotation_index()` implementation may silently
overwrite an earlier annotation when duplicate `annotation_id` values are
supplied. That implementation is intentionally unchanged: its exact bytes are
hash-pinned by historical execution validation and the frozen public walkthrough.
Changing it in place would break reproducibility checks for those frozen records.

New code should not expand reliance on the silent-overwrite behavior. A future
versioned strict indexing API is required and should reject duplicate identifiers
explicitly. That migration must preserve access to the frozen legacy behavior for
historical verification, document the compatibility boundary, and include a
record-version or API-version decision before replacing any existing call path.

This note does not mark duplicate indexing as resolved. No pinned hash, frozen
artifact, study gate, or historical record is changed by the non-frozen Core
correctness work.
