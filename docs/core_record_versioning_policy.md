# Core Record Versioning and Legacy Compatibility Policy

## Status and scope

This document is the normative design for future Core record-version work.
It is accepted policy for later implementation; it does not claim that a
version-aware schema, reader, validator, serializer, lock, report, compatibility
namespace, or migration tool exists today.

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** express
binding requirements for future implementation. Statements labelled as future
options are non-binding until a later decision record adopts one.

The current repository remains unchanged at these boundaries:

- the installed package version is `0.3.0a1`;
- Core records have no explicit record-version field;
- strict annotation indexing API version `"1"` is available for active
  non-frozen Core annotation callers;
- frozen historical paths retain their original unversioned semantics; and
- provenance, lock, exposure, gate, assignment, composite-key, and other
  non-annotation identifier contracts remain deferred.

No stored record is assigned a version by this policy. Absence of version
metadata is not the serialized value `"0"` or `"1"`.

## Version taxonomy and terminology

### Package version

The **package version** identifies an installed Python distribution. The current
package version is `0.3.0a1`. A package release MAY contain readers for multiple
Core record versions and explicit legacy compatibility paths. The package
version MUST NOT be used to infer the semantic version of an individual record.

### Core record version

A **Core record version** identifies the semantic contract governing a Core
annotation's required fields, allowed values, identifier uniqueness, parent and
relationship semantics, validation expectations, serialization, hashing, and
migration behavior. It is serialized in the record itself for every future
explicit version.

### Indexing API version

The **indexing API version** identifies the contract of the strict annotation
indexing helper. Its current value is
`STRICT_INDEXING_API_VERSION == "1"`. Indexing API version `"1"` and Core record
version `"1"` use the same short value in different namespaces; they are related
by an explicit compatibility mapping, not by equality of their strings.

Implementations MUST NOT infer either version from the other.

### Study protocol version

A **study protocol version** identifies a study design or operating procedure.
It MUST NOT identify a Core record contract, package release, indexing API, or
artifact format unless an explicit manifest independently names each applicable
version.

### Artifact or manifest version

An **artifact or manifest version** identifies the shape of a dataset, lock, or
migration manifest. It MUST be versioned independently of the records it
describes. A manifest MAY declare the Core versions it contains, but its own
format version MUST NOT be treated as a Core record version.

### Legacy-unversioned record

A **legacy-unversioned record** is a Core record created before an explicit Core
record-version field existed. `legacy-unversioned` is the canonical policy term.
It describes absent version metadata and is not a formal serializable Core
version value. Future code MUST NOT write `legacy-unversioned` or `"0"` into the
`core_record_version` field as a substitute for migration.

### Frozen historical artifact

A **frozen historical artifact** is a record, file, walkthrough, manifest,
checksum, or validation path whose bytes and interpretation are protected for
reproducibility. A frozen artifact MUST remain byte-for-byte unchanged, and a
new reader MUST NOT silently assign it new semantics.

### Compatibility adapter

A **compatibility adapter** is an explicitly named reader, validator, serializer,
or verification path that handles declared legacy-unversioned material under its
original semantics. It MUST be selected by historical context or an explicit
compatibility declaration, never by field-shape guessing.

### Migration and migration artifact

A **migration** is a deliberate transformation that creates a new versioned
record or dataset and records its source. A **migration artifact** is the new
output plus its migration manifest. Migration MUST NOT mean reinterpreting,
overwriting, renaming, or reserializing the original artifact in place.

## First explicit Core version

The first future explicit Core record version identifier MUST be `"1"`. The
value is short, stable in text formats, and leaves the semantic namespace in the
field name instead of repeating it in values such as `"core-1"`.

Core version `"1"` MUST:

- use the current Core business fields with their current meanings;
- add serialized version metadata without silently changing existing field
  meanings;
- reject an empty or whitespace-only `annotation_id`;
- require `annotation_id` to be globally unique across the containing dataset,
  including across version partitions in a mixed dataset;
- select no winner for duplicate identifiers;
- preserve deterministic input order for unique records;
- make identifier failures content-redacted;
- resolve parent and other Core relationships through fail-closed indexing; and
- reject unresolved, ambiguous, or disallowed cross-version relationships.

These requirements make existing strictness explicit for new versioned records.
They do not permit existing legacy-unversioned records to be relabelled `"1"`.
Implementing Core version `"1"` requires the version-aware reader and dispatch
infrastructure described below before any schema field is added.

## Version field and metadata placement

The future serialized record field MUST be named `core_record_version`.

The field MUST be record-level because dispatch, validation, relationship
resolution, serialization, and lock verification must remain correct when
records are detached from their original dataset. Every record using an
explicit Core version MUST carry it.

A future dataset manifest MUST additionally declare:

- a manifest-format version;
- the explicit values permitted in `allowed_core_record_versions`;
- whether legacy-unversioned records are permitted;
- the named `compatibility_mode`, if legacy-unversioned records are permitted;
- whether the dataset is single-version or mixed-version;
- any compatibility-rule or migration-manifest identifiers needed for semantic
  processing; and
- a dataset identifier and content hash under the manifest's canonicalization
  rules.

The manifest declaration MUST constrain rather than replace record-level
metadata. A record version outside the declared set MUST fail validation. A
manifest MUST NOT supply a missing record version for new active input.

Migration-only fields such as `migration_id`, source and target hashes, rule
identifiers, and adjudication status belong in a migration manifest. They SHOULD
NOT be copied into every Core record unless a later schema decision identifies a
record-level interoperability need.

## Reader and validation dispatch

The preferred future public model is a new version-aware entry point such as:

```python
validate_versioned_core_record(record, *, context=None)
```

The name and signature remain future implementation details, but the dispatch
model is binding:

1. an explicit `core_record_version` in the record is authoritative;
2. a registry MUST map each supported value to exactly one version-specific
   validator and serializer contract;
3. an absent field MUST enter legacy behavior only through an explicit frozen
   context or named compatibility adapter;
4. an unsupported explicit value MUST fail before semantic validation; and
5. a separately supplied context MUST NOT override a conflicting record value.

Shared, version-independent checks MAY be reused behind dispatch. Version
orchestration MUST remain explicit so implementations do not duplicate all
validators or apply newest rules to older records.

Before any explicit Core version is introduced, future implementation MUST
inventory and classify every existing public and internal Core reader or
validator as exactly one of:

- a version-aware active entrypoint;
- an explicit legacy compatibility entrypoint; or
- a frozen historical entrypoint.

Future routing MUST prevent new active workflows from reaching
legacy-unversioned semantics implicitly. A supported explicit Core version MUST
NOT be introduced while any active non-frozen entrypoint can accept missing
version metadata and silently apply legacy-unversioned semantics.

Existing public APIs MAY remain importable for compatibility, but importability
MUST NOT imply that every call context remains valid for new active workflows.
Frozen behavior MUST remain unchanged. Active non-frozen callers MAY be routed
through version-aware dispatch only in a separately reviewed implementation PR
after their contexts are classified and tested.

The existing public validation functions remain unchanged in this design PR.
Their future transition MUST be defined and tested before Core version `"1"` is
introduced. Frozen validation MUST not be weakened or routed through new rules.

## Missing-version policy

### Frozen or explicitly declared historical context

A missing `core_record_version` MUST be interpreted as legacy-unversioned only
when the artifact is frozen historical material or the caller explicitly
selects the legacy-unversioned compatibility adapter. The original legacy
semantics, serializer, hashes, and verification behavior MUST be preserved.

A named adapter MUST NOT be a user-selectable escape hatch for arbitrary
malformed or new input. The caller MUST declare genuine frozen historical
provenance or migration-source context that the adapter can validate. Merely
requesting "legacy mode" MUST NOT transform new input into historical input.

### New active workflow

A missing `core_record_version` in new active input MUST produce a deterministic
`missing_core_record_version` validation error. It MUST NOT default to the
newest version, Core version `"1"`, the package version, or the indexing API
version.

Raw input MAY be retained for correction or archival, but semantic validation,
relationship resolution, locking, reporting, and migration MUST NOT proceed
until the caller supplies a valid explicit version or deliberately places a
genuine historical artifact in declared compatibility context. Field shape,
file date, path, and surrounding records MUST NOT be used as version heuristics.

## Unknown-version policy

An unsupported explicit value, including `"99"`, MUST produce a deterministic
`unsupported_core_record_version` error containing the field name and raw
version value but no annotation rationale or source content.

A preservation-only reader MAY store or transmit the original bytes and
minimal envelope metadata while marking the record uninterpreted. It MUST NOT:

- coerce the unknown value to a supported value;
- semantically validate or transform the record;
- resolve its relationships;
- include it in semantic reports;
- issue or reuse a semantic lock for it; or
- pass it to a version-specific validator by guessing.

Pass-through is therefore allowed only for explicit preservation channels.
Support for the version or an explicit migration rule is required before
semantic processing.

## Mixed-version datasets

Mixed Core versions MAY be stored, including legacy-unversioned records beside
future explicit records or multiple explicit versions. Mixed storage does not
authorize mixed semantic processing.

A mixed dataset MUST have a dataset manifest that enumerates every explicit
version, declares whether legacy-unversioned material is present, names the
compatibility mode, and identifies any partial migration. Readers MUST partition
records by declared context before validation. Unsupported partitions may be
preserved but MUST NOT be semantically processed.

Semantic validation and reporting across partitions MUST fail closed unless an
explicit compatibility plan names the participating version pair, allowed
operation, field mappings, relationship rules, and reporting semantics.
Otherwise reports MUST remain partitioned and MUST NOT silently combine metrics.

Parent-child and other Core relationships across versions MUST be rejected by
default. A directed version-pair rule MAY permit a specific relationship only
after it defines identifier scope, parent and child validation, field semantics,
lock implications, and reporting behavior. No such pair rule is defined by this
policy. In particular, legacy-unversioned to Core version `"1"` relationships
are not implicitly allowed.

Within one dataset, `annotation_id` uniqueness MUST span every partition.
Migration linkage MUST use the migration manifest rather than duplicate IDs that
would make record lookup ambiguous.

Partial migration MUST create a new mixed dataset and migration manifest. It
MUST leave the source dataset unchanged, enumerate migrated and unmigrated
members, and obey the same default rejection of cross-version relationships.

## Required input-context matrix

| Input context | Version metadata | Allowed reader | Interpretation | Mutation allowed |
| --- | --- | --- | --- | --- |
| Frozen historical artifact | Absent | Explicit legacy-unversioned compatibility path | Original legacy semantics | No |
| Declared legacy source for migration | Absent | Compatibility reader plus an approved migration rule | Legacy semantics before transformation | New output only |
| New active input | Absent | Version-aware reader | `missing_core_record_version` failure | No silent assumption |
| Future Core version `"1"` | Explicit supported value | Version-aware reader | Core version `"1"` semantics | Normal processing under version `"1"` |
| Unsupported future version | Explicit unknown value | Preservation-only reader | Uninterpreted bytes and envelope metadata | No semantic processing |
| Migration output | Explicit target version | Version-aware reader | Target semantics with linked migration provenance | New artifact only |

## Migration provenance

Every migration MUST produce a new artifact and a deterministic migration
manifest. The original source and, when frozen, its bytes and historical
verification path MUST remain unchanged.

At minimum, a migration manifest MUST record:

- migration identifier and migration-manifest format version;
- source record or dataset identifier;
- source Core version, using a context marker for legacy-unversioned input
  rather than writing that marker into a Core record;
- target Core version;
- migration tool name and version, including the package version;
- timestamp with timezone;
- migration rule identifier and rule version;
- source artifact hash and target artifact hash;
- source-to-target record identifier mapping when records are migrated
  individually;
- whether human adjudication occurred;
- migration classification;
- fields or meanings changed;
- any information that could not be represented; and
- notes describing non-lossless transformation.

The manifest SHOULD include the operator or automated process identity and the
validation results for the target artifact. A target hash MUST be computed only
after deterministic serialization.

## Migration classifications and review

A **lossless migration** preserves all source information and semantics and
permits deterministic reconstruction or verification of every source value from
the target plus its manifest.

A **normalization-only migration** changes representation under a documented
equivalence rule without changing semantic values. It counts as lossless only
when the original representation is preserved or deterministically
reconstructable and the equivalence rule is versioned.

A **semantic migration** changes the interpretation, controlled vocabulary,
relationship meaning, or derived value of a record even if no source text is
discarded.

A **non-lossless migration** discards, combines, guesses, or cannot represent
source information or meaning.

Human review MUST be required for semantic and non-lossless migration. It MUST
also be required when a source is invalid, a target value would be inferred,
normalization equivalence is ambiguous, a relationship cannot be mapped
deterministically, or the automated result conflicts with an existing lock.
Review MUST create a separate adjudication record and MUST NOT modify the source.

Lossless and unambiguous normalization-only migrations MAY be automated after
their rules, deterministic tests, dry-run behavior, and review thresholds are
approved. This policy does not authorize migration or human review activity.

## Compatibility namespace and existing imports

The preferred future namespace is:

```python
trim_haa.compat.legacy_unversioned
```

Future explicit adapters for legacy annotation indexing, frozen-record reading,
historical serialization, and compatibility validation MAY live there. Each
adapter MUST identify the historical contract it preserves. The namespace MUST
NOT become an implicit fallback for malformed new input.

Phase 1 MUST create `trim_haa.compat.legacy_unversioned`, or an equivalent
explicitly named legacy compatibility entrypoint, before Phase 2 may begin. The
preferred implementation is the named namespace. Later consolidation of active
callers and wrappers does not defer this initial compatibility boundary.

`trim_haa.provenance.annotation_index` MUST remain frozen indefinitely while
protected historical workflows depend on it. It is not recommended for new
development. A future compatibility wrapper MAY delegate to it, but the original
import path MUST NOT be removed, moved, changed, warned, or redirected in a way
that alters frozen outputs. Creating the compatibility namespace or wrappers is
future work and does not occur in this design PR.

## Strict indexing relationship

Every future explicit Core version MUST reject empty, whitespace-only, and
duplicate `annotation_id` values, select no duplicate winner, preserve
deterministic order for unique records, and report identifier and position
metadata without rationale or source content.

Core version `"1"` is designed to use strict indexing API version `"1"`.
Future Core versions MAY require a later strict indexing API only when their
version specification records an explicit mapping and compatibility tests.
Changing an indexing API version MUST NOT implicitly create or migrate a Core
record version, and changing a Core version MUST NOT mutate the existing strict
indexing version-1 contract.

Non-annotation identifier types MUST NOT be forced through the annotation
indexing API.

## Serialization

Every future explicit Core record MUST serialize `core_record_version`.
Version-specific canonical field order MUST be documented. For Core version
`"1"`, the version field SHOULD appear first in order-sensitive mappings and CSV
headers so dispatch metadata is visible before semantic fields.

Future canonical hashing MUST include the exact serialized version metadata and
MUST use version-specific canonicalization. A serializer MUST reject a record
whose explicit version it does not support.

Compatibility serializers MUST preserve original historical bytes wherever
byte identity is required. Parsing and reserializing a historical record is not
byte preservation. Migrating or reserializing it as an explicit version creates
a new artifact, new canonical payload, new hash, and migration manifest.

Current serializers and canonical hashing are unchanged by this policy.

## Locks and hashes

The version field MUST enter every future versioned canonical lock payload.
Future lock manifests MUST identify both their own format version and the Core
record version whose canonicalization was used. Lock verification MUST dispatch
by explicit Core version and MUST fail closed for missing, unknown, or
conflicting version metadata outside declared legacy context.

Existing historical locks remain valid for only the original historical
representation and legacy verification path. A migrated record MUST receive a
new lock after target serialization and validation. A lock created for one Core
version MUST NOT verify a record in another version, even when the remaining
field values are equal. Cross-version lock reuse is prohibited.

Current lock and hashing implementations are unchanged by this policy.

## Reporting and comparison

Future reporting MUST handle record contexts as follows:

- a legacy-only dataset requires the explicit legacy-unversioned compatibility
  path and retains historical reporting semantics;
- a dataset containing one supported explicit Core version uses that version's
  validator and reporting contract;
- a mixed dataset is reported by version partition unless an explicit
  compatibility plan permits a named cross-version report;
- an unsupported version is listed as preserved and uninterpreted, without
  semantic metrics; and
- a migrated record or dataset reports its migration identifier and source link
  without merging source and target observations as independent evidence.

Reports MUST NOT silently combine semantically incompatible versions. A
cross-version report MUST disclose every included version and the compatibility
rule applied.

Current reporting and comparison implementations are unchanged by this policy.

## Deprecation

Active non-frozen convenience imports MAY be deprecated through a documented,
versioned public transition after replacements exist and compatibility tests
pass. Frozen historical paths MUST remain supported indefinitely.

Deprecation warnings MUST NOT alter frozen outputs, checksum-sensitive streams,
or historical verification. Compatibility support MAY move behind explicit
namespaces for active callers only through a versioned public transition; the
protected original import path remains available where frozen workflows depend
on it.

This policy issues no runtime warning and deprecates no current API.

## Separate deferred identifier contracts

The active identifier-indexing audit records twenty non-annotation paths grouped
into these contract families:

- provenance rows;
- lock rows;
- exposure events;
- gate maps;
- participant/case assignments;
- case/stage composite indexes;
- second-pass indexes;
- candidate-category indexes; and
- manual and support-script indexes.

Core record versioning does not automatically version these record types or
define their uniqueness rules. Each family MUST receive its own identifier,
duplicate, error, serialization, and compatibility contract before migration.
A later contract MAY reference the Core version it accompanies. None is migrated
by this policy.

## Implementation roadmap

### Phase 0: current repository

- Core records remain legacy-unversioned.
- Strict annotation indexing API version `"1"` serves reviewed active
  non-frozen Core annotation callers.
- Frozen historical paths retain legacy behavior.
- No explicit Core record-version field exists.

### Phase 1: dispatch and compatibility boundary

Before any explicit Core version field is introduced, future work MUST:

- add version constants and an explicit dispatch registry;
- add deterministic missing-version and unsupported-version errors;
- add preservation-only handling for unsupported versions;
- create `trim_haa.compat.legacy_unversioned`, or an equivalent explicitly
  named legacy compatibility entrypoint;
- inventory and classify every existing public and internal Core reader or
  validator as version-aware active, explicit legacy compatibility, or frozen
  historical;
- establish routing rules that prevent new active workflows from reaching
  legacy-unversioned semantics implicitly;
- prove with compatibility tests that frozen historical workflows remain
  unchanged; and
- prove with active-call-site tests that new unversioned input fails closed.

Phase 1 MUST NOT migrate records or add an explicit Core version field. Existing
APIs MAY remain importable, but their permitted future call contexts MUST be
classified and enforced before Phase 2.

### Phase 2: first explicit Core version

Phase 2 MUST NOT begin until every Phase 1 compatibility-boundary and routing
test passes. Core version `"1"` MUST NOT be added to any production schema,
serializer, fixture, lock format, or record while any active non-frozen
entrypoint can accept missing version metadata and silently apply
legacy-unversioned semantics.

Only after that hard prerequisite is satisfied MAY future work introduce
`core_record_version`, version `"1"` schemas and serializers, canonical hash
rules, version-aware validators, lock metadata, and new synthetic fixtures.

### Phase 3: migration tooling

Future work MUST require explicit source and target versions, immutable sources,
migration manifests, deterministic output, dry-run support, and no automatic
overwrite. Human-review gates MUST follow the migration classifications above.

### Phase 4: active caller transition and compatibility consolidation

After the Phase 1 boundary exists, future work MAY migrate reviewed active
non-frozen callers, consolidate compatibility wrappers under
`trim_haa.compat.legacy_unversioned`, and document versioned transition paths.
Each caller transition requires separate compatibility review. Frozen original
imports MUST remain. Phase 4 MUST NOT be described as the first availability of
explicit legacy compatibility.

### Phase 5: stable release policy

Future work MUST publish a support matrix, deprecation documentation, and
long-term historical verification guarantees before stable release.

## Current non-implementation commitments

This policy does not add `core_record_version` to `CORE_FIELDS`, assign version
`"1"` to any record, create a runtime compatibility namespace, change
`STRICT_INDEXING_API_VERSION`, alter validation or serialization, change
canonical hashes or locks, migrate any deferred contract, change package
version, or change study gates. Provider calls, private-packet inspection, human
coding, and model execution remain outside its scope.
