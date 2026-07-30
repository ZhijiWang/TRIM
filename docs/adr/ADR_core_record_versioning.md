# ADR: Core Record Versioning and Legacy Compatibility

## Status

Accepted for future implementation.

## Context

Current Core records have no explicit record-version field. Package version
`0.3.0a1`, strict indexing API version `"1"`, study protocols, manifests, and
frozen historical behavior are separate concepts. Future records need explicit
semantic dispatch without relabelling or reinterpreting legacy-unversioned
artifacts.

## Decision

- The first explicit Core record version will be `"1"`.
- Its record-level field will be `core_record_version`.
- Version `"1"` will preserve current Core business-field meanings while making
  strict identifier uniqueness and fail-closed relationships normative.
- Missing metadata is legacy-unversioned only in frozen or explicitly declared
  compatibility context; it fails validation in new active workflows.
- Unknown versions fail closed and may pass only through preservation channels
  without semantic interpretation.
- Mixed versions may be stored with a manifest, but cross-version validation,
  reporting, and relationships require explicit compatibility rules.
- Validation will use an explicit version-dispatch registry; it will not guess
  from shape or package version.
- Migration creates a new artifact, hash, lock, and provenance manifest while
  preserving the source.
- The preferred future compatibility namespace is
  `trim_haa.compat.legacy_unversioned`.
- `trim_haa.provenance.annotation_index` remains frozen and supported for
  protected historical workflows.
- Strict indexing API version `"1"` remains independent of Core record version
  `"1"`.

The full binding requirements are in the
[Core Record Versioning and Legacy Compatibility Policy](../core_record_versioning_policy.md).

## Consequences

Future implementation must build explicit reader dispatch before adding the
first version field. Versioned canonical payloads and locks include version
metadata. Partial migration yields a declared mixed dataset, not an in-place
rewrite. Unsupported versions cannot enter semantic validation or reports.

## Alternatives rejected

- Treating legacy records as formal version `"0"` was rejected because it would
  invent serialized metadata and semantics that were not present.
- Inferring record version from package version, indexing API version, file
  shape, date, or location was rejected as ambiguous.
- Defaulting missing metadata to the newest version was rejected because it
  silently reinterprets history.
- Reusing locks or relationships across versions by field equality was rejected
  because canonical and semantic contracts differ.
- Moving or changing the frozen legacy import was rejected because historical
  verification depends on its original behavior.

## Compatibility commitments

Frozen artifacts, validation paths, hashes, and imports retain their original
bytes and semantics indefinitely. Legacy compatibility is explicit, not a
fallback for new input. Current public APIs, package version, strict indexing
API version, and gate statuses remain unchanged by this decision.

## Deferred work

Version-aware readers, schemas, serializers, validators, locks, reports,
migration tooling, and compatibility adapters require later implementation
PRs. The twenty audited non-annotation identifier paths require separate
provenance, lock, exposure, gate, assignment, composite-key, candidate-category,
and manual/support-script contracts.
