# ADR: Repository Maintenance Boundary

## Status

Accepted for the current alpha line.

## Context

The current TRIM-HAA alpha has completed the reviewed non-frozen correctness
work, added version-1 strict annotation indexing, migrated reviewed active Core
annotation callers, and adopted a future Core record-version and legacy
compatibility policy. Frozen provenance, historical workflows, artifacts,
package boundaries, and blocked study gates remain intact.

The policy also names substantial future work. Its presence is not evidence
that the work is currently needed. Continuing speculative implementation would
increase compatibility surface before there is a real versioned record,
consumer, migration, or authorized study execution.

Software readiness for maintenance is distinct from empirical research
readiness. The repository does not establish scientific validity or authorize
execution.

## Decision

The current repository enters infrastructure maintenance mode for the
`0.3.0a1` alpha line. Work is driven by confirmed correctness, security,
reproducibility, packaging, dependency, documentation, or rights needs.
Speculative infrastructure expansion requires an explicit reopening decision.

Future Core versioning remains accepted policy but unimplemented. Phase 1 is
deferred until a concrete Core-versioning trigger exists. Deferred identifier
contracts are activated individually when a current path demonstrates a real
ambiguity or correctness risk; they are not implemented as a batch.

Blocked studies remain blocked. Software closure is not research completion,
empirical validation, ethics approval, or authorization for provider calls,
packet inspection, human coding, or model execution.

## Scope considered complete

For the current legacy-unversioned alpha schema, the maintained scope includes
Core representation and validation, strict annotation indexing for reviewed
active callers, provenance and frozen lineage support, current locking,
descriptive comparison and reporting, synthetic demonstrations, frozen public
walkthrough verification, packaging boundaries, artifact verification, and the
future version-policy record.

This completeness claim does not extend to hypothetical future schemas or
record families.

## Work intentionally deferred

Phase 1 dispatch, an explicit compatibility namespace, Core version `"1"`,
versioned serialization and locking, migration tooling, mixed-version
processing, and the twenty audited non-annotation identifier paths remain
`DEFERRED_BY_DESIGN`. Provider integration, empirical study execution, human
coding, and model execution remain `BLOCKED_BY_GATE`. A stable public release
remains outside the current alpha scope.

## Reopening criteria

Infrastructure development may reopen when one of these concrete conditions is
documented:

- a real record producer, dataset, external consumer, or schema change requires
  explicit Core version metadata and names affected entrypoints,
  compatibility, and tests;
- an active non-annotation path demonstrates that an empty or duplicate
  identifier changes a result, suppresses an error, or selects a winner;
- a named source artifact has an approved target schema, preservation rule,
  and migration rule;
- an external user requires supported behavior outside the current alpha
  contract; or
- all gates governing a proposed study activity have been explicitly cleared.

A deferred list, possible abstraction, alpha label, or desire for symmetric
implementation is not a reopening criterion.

## Consequences

The repository remains active and maintainable, but speculative architecture is
not default work. Correctness and reproducibility fixes remain welcome. Every
reopening decision must be narrower than its evidence and preserve current
compatibility commitments.

Future design documents may remain intentionally unimplemented. Test success
supports software confidence only; it does not add scientific claims.

## Alternatives rejected

- Implementing Phase 1 solely because the future policy exists was rejected
  because no explicit Core-version consumer currently needs it.
- Implementing all twenty deferred identifier paths for completeness was
  rejected because their record semantics and compatibility contracts differ.
- Assigning existing records version `"1"` was rejected because it would
  reinterpret legacy-unversioned history without migration.
- Declaring a stable release was rejected because there is no external-use
  evidence or stable support decision.
- Treating software closure as research completion was rejected because
  software tests cannot establish empirical, causal, reliability, validity, or
  ethics claims.

## Compatibility commitments

`src/trim_haa/provenance.py`, its historical callers, frozen public walkthrough,
artifact ZIPs, checksum sidecars, frozen schemas and manifests, PR #18 public
references, and protected historical validation paths remain unchanged.
Future compatibility infrastructure must preserve their bytes and
interpretation.

The current package version, public APIs, current schema, serialization,
canonical hashes, locks, records, strict indexing API version, distribution
boundary, and gate outcomes are unchanged by this decision.
