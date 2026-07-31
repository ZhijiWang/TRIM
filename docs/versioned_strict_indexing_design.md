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
- No historical caller is migrated.
- `annotation_index()` retains its silent last-record-wins behavior only as a
  legacy compatibility boundary.

The reviewed active, non-frozen Core-annotation callers now use the strict API.
The repository-wide classification and migration decisions are recorded in the
[active identifier indexing audit](active_identifier_indexing_audit.md).

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

Indexing API version `"1"` is not itself a Core record version. The future
mapping between these independent contracts is defined in the
[Core Record Versioning Policy](core_record_versioning_policy.md); no current
record receives version metadata through the indexing API.

For validation-report APIs, fail-closed indexing prevents checks that would
require choosing an ambiguous record; it does not abort unrelated validation.
Record-only errors that do not depend on the unavailable index continue to be
collected in the same report.

## Other index risks

The active-index audit confirmed that provenance rows, exposure events, lock
manifests, gate maps, and composite stage or assignment lookups also use
identifier-based patterns. Some active validators already detect particular
duplicates, while other dictionary-building paths may still select a later
value. These paths remain deferred for record-type-specific contract design.
They are not forced through the annotation contract, and this design does not
claim that all duplicate-index risks are resolved.

## Migration phases

These are strict-indexing adoption phases. Their Phase 1 is not Phase 1 of the
[Core Record Versioning Policy](core_record_versioning_policy.md): the indexing
new-call-site phase below is complete, while Core version-aware dispatch and
its compatibility boundary remain unimplemented.

### Phase 0: compatibility preservation

- The legacy function remains frozen.
- Frozen historical workflows retain their explicit legacy paths.
- Frozen historical callers are never migrated solely because they use the
  legacy helper.

### Phase 1: new-call-site adoption — complete

- All new modules use the strict helper.
- The recursive compatibility guard rejects new production imports or calls of
  the legacy helper except for a function-scoped compatibility allowlist.
- The guard is independent of line numbers, permits the strict API, and has a
  regression proving that a new production legacy import fails.
- Additional record-type helpers are introduced only after their contracts are
  separately reviewed.

### Phase 2: non-frozen caller migration — reviewed Core callers complete

- The active-index audit reviewed production, test, script, validator, and
  documentation candidates.
- Proven active non-frozen Core annotation lookups in reporting, validation,
  and the synthetic dry-run use `strict_annotation_index()`.
- Caller regressions cover unique, duplicate, invalid, generator, order, and
  redaction behavior.
- Frozen workflows retain an explicit legacy path.
- Non-annotation indexes remain deferred rather than being forced through the
  annotation contract.

### Phase 3: Core record version boundary

- A new Core record/API version names strict indexing as its default contract.
- Record-version and migration metadata define how mixed-version data is handled.
- Legacy behavior remains available only through an explicit compatibility
  namespace or adapter used for historical verification.

### Phase 4: stable release

- Release documentation MAY define a transition or deprecation policy only for
  active non-frozen convenience surfaces after replacements exist,
  compatibility tests pass, affected active callers are identified, and a
  separately reviewed public transition is approved.
- Frozen historical imports and verification paths remain supported
  indefinitely and receive no removal timeline. They retain their original
  semantics and import paths wherever protected historical workflows depend on
  them.
- Frozen historical paths MUST NOT be redirected in a way that changes output
  or emit warnings that alter checksum-sensitive or frozen behavior.
- Historical verification support is preserved indefinitely.
- Frozen records are never rewritten or reinterpreted.

## Caller guidance

New Core-annotation indexing code should import `strict_annotation_index` from
`trim_haa` or `trim_haa.indexing`. All audited active non-frozen Core-annotation
callers have migrated. Code that verifies frozen historical workflows may
continue to use `trim_haa.provenance.annotation_index()` and should label that
dependency as legacy compatibility behavior. Non-annotation record indexes
require separate contract-specific design before migration.

## Non-goals

This design does not:

- migrate frozen historical callers;
- migrate non-annotation record indexes;
- change `provenance.py`, frozen files, manifests, or hashes;
- resolve every provenance, exposure, lock, or report-index duplicate risk;
- change future-state schemas or study gates;
- authorize provider execution, model execution, or human coding.
