# Active Identifier Indexing Audit

## Scope and result

This audit reviews identifier-index construction and lookup behavior at the
repository state derived from `main` commit
`456575b9732051f4a1ba58008c2e8ad6b4cc85a5`. It distinguishes Core annotation
indexes from provenance, lock, exposure, gate, stage, case, segment, and manual
record lookups. It does not claim that every identifier type now has a strict
contract.

The search produced 176 syntax candidates. Manual review added first-match
loops and documented compatibility references that syntax matching did not
fully describe, then consolidated repeated operations with the same key and
contract into 57 semantic candidate paths. Of those, 45 are genuine
identifier-indexing or compatibility-reference paths and 12 are non-index
dictionary uses.

| Category | Count |
| --- | ---: |
| `ACTIVE_STRICT_ALREADY` | 8 |
| `ACTIVE_SAFE_TO_MIGRATE` | 9 |
| `ACTIVE_REQUIRES_NEW_CONTRACT` | 20 |
| `FROZEN_LEGACY_COMPATIBILITY` | 5 |
| `TEST_OR_DOCUMENTATION_ONLY` | 3 |
| `NOT_AN_IDENTIFIER_INDEX` | 12 |
| **Total semantic candidates** | **57** |
| **Genuine identifier/compatibility paths** | **45** |

## Audit method

Candidate discovery covered all Python under `src/`, `scripts/`, and `tests/`,
plus relevant Markdown and package configuration. Searches included
`annotation_index`, `strict_annotation_index`, identifier field names,
`records_by_`, `by_id`, `by_case`, `by_stage`, `lookup`, `mapping`,
dictionary comprehensions, `dict(...)`, `setdefault(...)`, subscript
assignments, and first-match loops. An AST pass enumerated dictionary
comprehensions, `dict(...)` calls, `setdefault(...)`, selected index API calls,
and subscript writes.

Each candidate was then inspected manually for its key, input coercion,
duplicate and empty-key behavior, reachability, packaging boundary, frozen
status, downstream use, and whether an outer validator already makes
duplicates fatal. Serialization dictionaries, payload assembly, counters,
sets, and intentional one-to-many grouping were not treated as uniqueness
indexes.

## Complete audit table

| Location | Function or scope | Key | Current behavior | Reachability | Frozen status | Category | Action |
| -------- | ----------------- | --- | ---------------- | ------------ | ------------- | -------- | ------ |
| `src/trim_haa/indexing.py` | `strict_annotation_index` | `annotation_id` | Rejects empty and duplicate IDs; preserves order | Public package API | Non-frozen additive API | `ACTIVE_STRICT_ALREADY` | Keep version 1 unchanged |
| `src/trim_haa/validator.py` | `validate_core_records` duplicate scan | `annotation_id` | Empty IDs are record errors and duplicates are fatal validation issues | Public package validator and CLI | Non-frozen | `ACTIVE_STRICT_ALREADY` | Keep report contract; use strict success as the relationship-validation precondition |
| `src/trim_haa/validator.py` | `_validate_exposure_events` duplicate scan | `exposure_event_id` | A `seen` set emits a fatal duplicate issue | `validate_dataset` | Non-frozen | `ACTIVE_STRICT_ALREADY` | Keep; do not replace with annotation indexing |
| `src/trim_haa/reporting.py` | `_by_case` plus `_first_stage` | `(case_id, annotation_stage)` | One-to-many case grouping followed by explicit rejection of multiple stage rows | Public reporting APIs | Non-frozen | `ACTIVE_STRICT_ALREADY` | Keep the composite-stage contract |
| `src/trim_haa/cli.py` | `cmd_verify_lock` | lock row matching `annotation_id` | Zero or multiple matches fail; no lock winner is selected | Installed CLI | Non-frozen | `ACTIVE_STRICT_ALREADY` | Keep structured CLI failure behavior |
| `src/trim_haa/llm/dry_run.py` | `_validate_rights_records` | `case_id` | Length/set comparison rejects duplicate selected cases | Blocked study dry-run only | Non-frozen, study-only | `ACTIVE_STRICT_ALREADY` | Keep; execution remains blocked |
| `scripts/validate_human_llm_rights_gate.py` | rights inventory validation | `case_id` | Exact expected order and IDs are checked before evidence lookup | Existing validator | Protected historical inputs | `ACTIVE_STRICT_ALREADY` | Keep; no protected record changes |
| `scripts/validate_friction_locus_manual.py` | counterfactual test ID scan | `test_id` | Length/set comparison rejects duplicates | Existing manual validator | Manual inputs protected | `ACTIVE_STRICT_ALREADY` | Keep; no manual changes |
| `src/trim_haa/reporting.py` | `case_level_report` Core preparation | `annotation_id` | Before this PR duplicate Core IDs could reach report construction; now version-1 strict indexing fails closed | Public reporting APIs | Non-frozen | `ACTIVE_SAFE_TO_MIGRATE` | Migrated to `strict_annotation_index()` |
| `src/trim_haa/validator.py` | `validate_relationships` | `annotation_id` | Before this PR a comprehension selected the last duplicate; now a deterministic fatal validation issue reports identifier and positions and selects no winner | Public module validator; used by `validate_core_records` | Non-frozen | `ACTIVE_SAFE_TO_MIGRATE` | Migrated with validation-report translation |
| `src/trim_haa/validator.py` | `_validate_exposed_ai_links` Core lookup | `annotation_id` | Before this PR last duplicate won; now consumes the strict dataset Core index | `validate_dataset` | Non-frozen | `ACTIVE_SAFE_TO_MIGRATE` | Migrated through one prevalidated Core index |
| `src/trim_haa/validator.py` | `_validate_exposure_events` Core lookup | `annotation_id` | Before this PR last duplicate won; now consumes the strict dataset Core index | `validate_dataset` | Non-frozen | `ACTIVE_SAFE_TO_MIGRATE` | Migrated through one prevalidated Core index |
| `src/trim_haa/validator.py` | `_validate_locks` Core lookup | `annotation_id` | Before this PR last duplicate won; now consumes the strict dataset Core index | `validate_dataset` | Non-frozen | `ACTIVE_SAFE_TO_MIGRATE` | Migrated through one prevalidated Core index |
| `src/trim_haa/validator.py` | `_validate_changed_flag_consistency` Core lookup | `annotation_id` | Before this PR last duplicate won; now consumes the strict dataset Core index | `validate_dataset` | Non-frozen | `ACTIVE_SAFE_TO_MIGRATE` | Migrated through one prevalidated Core index |
| `scripts/run_trim_haa_synthetic_dry_run.py` | `run_dry_run` Core lookup | `annotation_id` | Before this PR a comprehension selected the last duplicate; now calls the strict Core helper | Source-checkout CLI dry-run | Non-frozen active script | `ACTIVE_SAFE_TO_MIGRATE` | Migrated to `_core_by_id()` using strict version 1 |
| `scripts/run_trim_haa_synthetic_dry_run.py` | `_observation_report` Core lookup | `annotation_id` | Before this PR a second comprehension selected the last duplicate; now calls the strict Core helper | Source-checkout CLI dry-run | Non-frozen active script | `ACTIVE_SAFE_TO_MIGRATE` | Migrated to `_core_by_id()` |
| `scripts/run_trim_haa_synthetic_dry_run.py` | `_core_by_id`, used by `_study_report` | `annotation_id` | Before this PR last duplicate won; now delegates directly to strict version 1 and accepts iterables | Source-checkout CLI dry-run | Non-frozen active script | `ACTIVE_SAFE_TO_MIGRATE` | Migrated and regression-tested |
| `src/trim_haa/exposure.py` | `exposure_index` | `exposure_event_id` | Empty or duplicate event IDs silently overwrite | Public module helper | Non-frozen | `ACTIVE_REQUIRES_NEW_CONTRACT` | Design an exposure-event-specific strict contract |
| `src/trim_haa/reporting.py` | `_provenance_by_id` | provenance `annotation_id` | Last provenance row wins | Public reporting path | Non-frozen | `ACTIVE_REQUIRES_NEW_CONTRACT` | Defer provenance-row contract |
| `src/trim_haa/reporting.py` | `_lock_by_annotation` | lock row `annotation_id` | Last lock row wins | Public reporting path | Non-frozen | `ACTIVE_REQUIRES_NEW_CONTRACT` | Defer lock-row contract |
| `src/trim_haa/validator.py` | `_validate_provenance_completeness` | provenance `annotation_id` | Last provenance row wins inside a validation-report API | `validate_dataset` | Non-frozen | `ACTIVE_REQUIRES_NEW_CONTRACT` | Define fatal provenance duplicate issues before migration |
| `src/trim_haa/validator.py` | `_validate_stage_condition_matrix` | provenance `annotation_id` | Last provenance row wins | `validate_dataset` | Non-frozen | `ACTIVE_REQUIRES_NEW_CONTRACT` | Defer provenance-row contract |
| `src/trim_haa/validator.py` | `_validate_exposed_ai_links` provenance lookup | provenance `annotation_id` | Last provenance row wins | `validate_dataset` | Non-frozen | `ACTIVE_REQUIRES_NEW_CONTRACT` | Defer provenance-row contract |
| `src/trim_haa/validator.py` | `_validate_exposure_events` provenance lookup | provenance `annotation_id` | Last provenance row wins | `validate_dataset` | Non-frozen | `ACTIVE_REQUIRES_NEW_CONTRACT` | Defer provenance-row contract |
| `src/trim_haa/validator.py` | `_validate_locks` provenance lookup | provenance `annotation_id` | Last provenance row wins | `validate_dataset` | Non-frozen | `ACTIVE_REQUIRES_NEW_CONTRACT` | Defer provenance-row contract |
| `src/trim_haa/validator.py` | `_validate_locks` lock lookup | lock row `annotation_id` | Last lock row wins | `validate_dataset` | Non-frozen | `ACTIVE_REQUIRES_NEW_CONTRACT` | Define a lock-row uniqueness contract |
| `src/trim_haa/validator.py` | `_validate_changed_flag_consistency` provenance lookup | provenance `annotation_id` | Last provenance row wins | `validate_dataset` | Non-frozen | `ACTIVE_REQUIRES_NEW_CONTRACT` | Defer provenance-row contract |
| `scripts/run_trim_haa_synthetic_dry_run.py` | `run_dry_run` provenance lookup | provenance `annotation_id` | Last provenance row wins | Source-checkout CLI dry-run | Non-frozen active script | `ACTIVE_REQUIRES_NEW_CONTRACT` | Defer provenance-row contract |
| `scripts/run_trim_haa_synthetic_dry_run.py` | `run_dry_run` lock lookup | lock row `annotation_id` | Last lock row wins | Source-checkout CLI dry-run | Non-frozen active script | `ACTIVE_REQUIRES_NEW_CONTRACT` | Defer lock-row contract |
| `scripts/run_trim_haa_synthetic_dry_run.py` | `run_dry_run` assignment lookup | `(participant_id, case_id)` | Last duplicate assignment wins | Source-checkout CLI dry-run | Non-frozen active script | `ACTIVE_REQUIRES_NEW_CONTRACT` | Define assignment composite-key rules |
| `scripts/run_trim_haa_synthetic_dry_run.py` | `_observation_report` AI lookup | `(case_id, ai_independent stage)` | Last AI record for a case wins | Source-checkout CLI dry-run | Non-frozen active script | `ACTIVE_REQUIRES_NEW_CONTRACT` | Define a case/stage contract |
| `scripts/run_trim_haa_synthetic_dry_run.py` | `_control_comparison` AI lookup | `(case_id, ai_independent stage)` | Last AI record for a case wins | Source-checkout CLI dry-run | Non-frozen active script | `ACTIVE_REQUIRES_NEW_CONTRACT` | Reuse a future case/stage contract |
| `scripts/run_trim_haa_synthetic_dry_run.py` | `_find_second_pass` | `(parent_annotation_id, expected stage)` | First matching second-pass row wins | Source-checkout CLI dry-run | Non-frozen active script | `ACTIVE_REQUIRES_NEW_CONTRACT` | Define composite second-pass uniqueness |
| `scripts/build_trim_haa_synthetic_dry_run.py` | `_find` | caller-selected field/value | First matching fixture row wins | Synthetic fixture builder | Non-frozen support script | `ACTIVE_REQUIRES_NEW_CONTRACT` | Do not force through annotation indexing |
| `src/trim_haa/llm/gates.py`; blocked-study validators and dry-runs | gate status normalization | gate name | Duplicate gate names can select a later status | Metadata-only validation/dry-run paths | Non-frozen, study-only | `ACTIVE_REQUIRES_NEW_CONTRACT` | Define a gate-manifest contract separately |
| `src/trim_haa/human_coding/disagreement.py` | `_confidence_signature` | candidate category | Later repeated categories overwrite confidence | Blocked human-coding dry-run/tests | Non-frozen, study-only | `ACTIVE_REQUIRES_NEW_CONTRACT` | Defer candidate-category contract |
| `scripts/validate_friction_locus_manual.py` | pair and example lookup | pair or `example_id` | Pair map is last-wins and `next(...)` is first-wins | Existing manual validator | Manual inputs protected | `ACTIVE_REQUIRES_NEW_CONTRACT` | Design manual-record-specific checks |
| `src/trim_haa/provenance.py` | `annotation_index` | `annotation_id` | Frozen last-record-wins behavior | Historical public API | Byte-frozen | `FROZEN_LEGACY_COMPATIBILITY` | Leave byte-for-byte unchanged |
| `src/trim_haa/provenance.py` | `lineage_for` | `annotation_id` via legacy helper | Calls frozen legacy index | Historical lineage verification | Byte-frozen | `FROZEN_LEGACY_COMPATIBILITY` | Keep explicit legacy call |
| `src/trim_haa/provenance.py` | `export_lineage_rows` | `annotation_id` via legacy helper | Calls frozen legacy index | Historical lineage export | Byte-frozen | `FROZEN_LEGACY_COMPATIBILITY` | Keep explicit legacy call |
| `scripts/run_trim_haa_synthetic_dry_run.py` | lineage export in `run_dry_run` | Core lineage through `export_lineage_rows` | Reaches the frozen legacy export and preserves historical output | Existing synthetic historical validation path | Compatibility-sensitive | `FROZEN_LEGACY_COMPATIBILITY` | Do not replace historical lineage behavior |
| `scripts/run_in_a_grove_walkthrough.py` | `_segment_lookup` | `segment_id` | Last duplicate segment wins | Older English walkthrough | Historical walkthrough boundary | `FROZEN_LEGACY_COMPATIBILITY` | Do not modify the older walkthrough |
| `tests/test_trim_haa_indexing.py`; `tests/sdist/test_core_distribution.py`; packaging tests | strict/legacy API assertions | `annotation_id` | Exercises strict behavior and frozen legacy contrast | Test-only | Not production | `TEST_OR_DOCUMENTATION_ONLY` | Keep tests; strengthen guard separately |
| Other dry-run, walkthrough, gate, checksum, and comparison tests | fixture-only lookup maps | fixture identifiers | Used only to assert fixtures and deterministic outputs | Test-only | Not production | `TEST_OR_DOCUMENTATION_ONLY` | Do not migrate as production callers |
| `docs/versioned_strict_indexing_design.md`; `docs/core_indexing_migration_note.md`; `docs/index.md`; `CHANGELOG.md` | API and migration references | N/A | Documentation only | Documentation | Not production | `TEST_OR_DOCUMENTATION_ONLY` | Update status and link to this audit |
| `src/trim_haa/schema.py` | record conversion | fixed field names | Serialization, not uniqueness indexing | Public package | Non-frozen | `NOT_AN_IDENTIFIER_INDEX` | No change |
| `src/trim_haa/depth.py` | record conversion | fixed field names | Serialization, not uniqueness indexing | Public package | Non-frozen | `NOT_AN_IDENTIFIER_INDEX` | No change |
| `src/trim_haa/locking.py` | canonical annotation payload | fixed schema fields | Canonical payload construction | Public package | Compatibility-sensitive | `NOT_AN_IDENTIFIER_INDEX` | No change |
| `src/trim_haa/provenance.py` | `children_by_parent` | `parent_annotation_id` | Intentional one-to-many grouping; duplicates are values, not winners | Historical/public helper | Byte-frozen | `NOT_AN_IDENTIFIER_INDEX` | No change |
| `src/trim_haa/exposure.py` | `exposures_by_human_post` | `human_post_annotation_id` | Intentional one-to-many grouping | Public helper | Non-frozen | `NOT_AN_IDENTIFIER_INDEX` | No change |
| `src/trim_haa/reporting.py` | `_by_case` grouping only | `case_id` | Intentional one-to-many grouping | Public reporting path | Non-frozen | `NOT_AN_IDENTIFIER_INDEX` | No change; stage uniqueness is a separate row above |
| `src/trim_haa/validator.py` | `events_by_post` | `human_post_annotation_id` | Intentional grouping used to warn on multiplicity | `validate_dataset` | Non-frozen | `NOT_AN_IDENTIFIER_INDEX` | No change |
| `src/trim_haa/validator.py` | `_copying_warnings` case grouping | `case_id` | Intentional one-to-many grouping | `validate_dataset` | Non-frozen | `NOT_AN_IDENTIFIER_INDEX` | No change |
| Human-coding and LLM request/response modules | payload assembly and `record_hash` writes | fixed payload fields | Record construction, not lookup indexing | Blocked study dry-runs | Protected study boundary | `NOT_AN_IDENTIFIER_INDEX` | No change |
| Comparison/report modules | summaries, counters, sets, and missingness maps | metric/field names | Aggregation and presentation | Active package | Non-frozen | `NOT_AN_IDENTIFIER_INDEX` | No change |
| Synthetic scripts | CSV row serialization, output maps, and counters | output field/metric names | Output construction, not identifier uniqueness | Source-checkout tools | Non-frozen | `NOT_AN_IDENTIFIER_INDEX` | No change |
| Tests | fixture mutation and captured-call dictionaries | fixed test fields | Test state mutation, not production indexing | Test-only | Not production | `NOT_AN_IDENTIFIER_INDEX` | No change |

## Active callers

Active packaged paths are the strict API, validators, reporting functions,
exposure helpers, lock verification CLI, and metadata-only study dry-runs.
Active source-checkout paths are the synthetic dry-run, its builder, and the
current validators. The migrated Core annotation callers are:

- `case_level_report`;
- `validate_relationships`;
- the four Core lookup consumers inside `validate_dataset`;
- `run_dry_run` and `_observation_report`; and
- `_core_by_id`, including its `_study_report` use.

The strict index preserves unique input order. Reporting and the synthetic
dry-run propagate `InvalidIdentifierError` or `DuplicateIdentifierError`.
`validate_relationships` preserves its validation-list contract by translating
the first strict failure into a fatal, content-redacted `ValidationIssue` with
identifier and position metadata and no selected winner.

## Silent-overwrite findings

Before this PR, the nine Category B Core annotation paths could silently select
a later duplicate or proceed with an ambiguous duplicate ID. They now fail
closed through strict indexing.

Silent selection remains in the 20 Category C non-annotation paths listed
above: provenance rows, lock rows, exposure events, gate names, assignment and
case/stage composites, candidate categories, and manual/support-script
identifiers. These paths are not safe to route through
`strict_annotation_index()` because their input types, error contracts, and
compatibility requirements differ. The five Category D paths retain historical
behavior deliberately.

## Frozen compatibility paths

`src/trim_haa/provenance.py` remains byte-for-byte frozen. Its
`annotation_index()` implementation, `lineage_for()` caller, and
`export_lineage_rows()` caller stay on legacy last-record-wins behavior.
The synthetic dry-run continues to call the frozen lineage export so its
historical lineage output is not reinterpreted. The older English walkthrough's
segment lookup also remains unchanged.

The compatibility guard allowlist is function-scoped and line-number
independent:

- `src/trim_haa/provenance.py::lineage_for`;
- `src/trim_haa/provenance.py::export_lineage_rows`.

No non-frozen production module imports or directly calls
`annotation_index()`.

## Deferred record-type contracts

Separate design work is required before migrating:

- provenance rows keyed by `annotation_id`;
- lock rows keyed by `annotation_id` or manifest identity;
- exposure events keyed by `exposure_event_id`;
- participant/case assignments and case/stage lookups;
- gate-manifest entries keyed by gate name;
- human-coding candidate categories; and
- manual, example, pair, and segment identifiers.

Each future contract must decide empty-key behavior, duplicate reporting,
position metadata, compatibility with validation-report APIs, and whether
historical records require an explicit legacy adapter.

## Migration decision

The nine Category B paths were safe because they index actual
`TrimHAAAnnotation` records, accept the existing version-1 strict contract
without API changes, are active and non-frozen, and do not provide a documented
last-record-wins guarantee. The migration does not alter data transformation,
return types, package exports, exception fields, or frozen historical callers.

No new generic indexing abstraction or record-type helper was added.

## Non-findings

Fixed-field serialization dictionaries, payload construction, record-hash
updates, summary dictionaries, counters, sets, and intentional one-to-many
grouping are not uniqueness indexes. They were searched and inspected but not
changed.

This audit resolves the reviewed active Core annotation lookup risks. It does
not establish repository-wide duplicate safety, and it does not resolve the
deferred non-annotation contracts.
