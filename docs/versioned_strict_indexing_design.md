# Versioned Strict Indexing Design

## Problem

The frozen `trim_haa.provenance.annotation_index()` function builds a dictionary
by assignment. When the same `annotation_id` appears more than once, the later
record silently replaces the earlier record. Historical execution and the frozen
public walkthrough pin that module byte-for-byte, so changing the legacy function
in place would break reproducibility.

TRIM-HAA therefore introduces a separate version-1 strict indexing API in
`trim_haa.indexing`. It is additive: no historical result or existing function is
reinterpreted.

## Compatibility boundary

- Historical verification continues to use the frozen legacy implementation.
- New development must use `strict_annotation_index()`.
- Frozen artifacts and historical hashes remain reproducible.
- No historical caller is migrated by this design PR.
- `annotation_index()` retains its silent last-record-wins behavior only as a
  legacy compatibility boundary.

## API contract

`strict_annotation_index(records)` accepts an iterable of
`TrimHAAAnnotation` objects or compatible mappings. Mapping inputs use the same
Core coercion rules as existing APIs. The function returns a standard dictionary
keyed by `annotation_id`; unique records retain deterministic input order.

The strict contract is:

- empty, whitespace-only, or missing annotation IDs raise
  `InvalidIdentifierError`;
- every repeated ID raises `DuplicateIdentifierError`, including byte-identical
  rows, conflicting rows, and rows from different cases;
- duplicate positions are zero-based input positions;
- no record is selected as the winner;
- input objects and mappings are not mutated;
- the implementation has no external dependency.

Both exceptions derive from `IdentifierIndexError`, which derives from
`ValueError`. `DuplicateIdentifierError` exposes the identifier type, duplicate
identifier, first and second positions, and both case IDs. The invalid-ID error
exposes identifier type, position, and case ID. Neither exception stores or
prints full records, rationales, source text, or other annotation content.

`STRICT_INDEXING_API_VERSION` is `"1"`. The helper and exception hierarchy are
available from both `trim_haa.indexing` and the top-level `trim_haa` namespace.
No existing export is removed.

## Other index risks

Provenance rows, exposure events, lock manifests, and stage-keyed reporting also
use identifier-based lookup patterns. Some active validators already detect
particular duplicates, while other dictionary-building paths may still select a
later value. This PR does not generalize an abstraction before each record type's
identifier and compatibility contract is reviewed. It therefore adds only the
strict annotation index and does not claim that all duplicate-index risks are
resolved.

## Migration phases

### Phase 0: current state

- The legacy function remains frozen.
- The strict version-1 helper is introduced.
- No historical or active caller is migrated.
- A source guard prevents new non-frozen production modules from importing or
  calling the legacy helper.

### Phase 1: new-call-site adoption

- All new modules use the strict helper.
- The compatibility guard continues to reject new reliance on the legacy helper.
- Additional record-type helpers are introduced only after their contracts are
  separately reviewed.

### Phase 2: non-frozen caller migration

- Active non-frozen paths are audited and migrated in a separate PR.
- Each migration receives duplicate, empty-ID, ordering, and compatibility tests.
- Frozen workflows retain an explicit legacy path.

### Phase 3: Core record version boundary

- A new Core record/API version names strict indexing as its default contract.
- Record-version and migration metadata define how mixed-version data is handled.
- Legacy behavior remains available only through an explicit compatibility
  namespace or adapter used for historical verification.

### Phase 4: stable release

- Release documentation defines the legacy deprecation timeline.
- Historical verification support is preserved indefinitely.
- Frozen records are never rewritten or reinterpreted.

## Caller guidance

New code should import `strict_annotation_index` from `trim_haa` or
`trim_haa.indexing`. Code that verifies frozen historical workflows may continue
to use `trim_haa.provenance.annotation_index()` and should label that dependency
as legacy compatibility behavior. Active callers should migrate only through the
phases above, with an explicit Core version decision before strict indexing
becomes the default.

## Non-goals

This PR does not:

- migrate existing historical or active callers;
- change `provenance.py`, frozen files, manifests, or hashes;
- resolve every provenance, exposure, lock, or report-index duplicate risk;
- change future-state schemas or study gates;
- authorize provider execution, model execution, or human coding.
