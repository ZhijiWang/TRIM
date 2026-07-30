# Repository Maintenance Boundary

This document is the authoritative operational boundary for the current
TRIM-HAA alpha infrastructure. It records a stopping point for speculative
infrastructure work. It is not an archival shutdown, a stable-release
declaration, an execution authorization, or evidence that the research has
been empirically validated.

The terms **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are normative for work
performed while this boundary remains in force.

## 1. Current authoritative state

This audit started from authoritative `main` commit
`14a011e5d4a13dab3e213a8bd2bba443bfc92607`, after PRs #24, #25, #26, and #27
had merged and before this documentation-only closure branch was created.

| Boundary | Current state |
| --- | --- |
| Package version | `0.3.0a1` (alpha) |
| Strict annotation-indexing API | Version `"1"` |
| Core records | Legacy-unversioned current alpha records |
| Explicit Core version | No explicit Core version is implemented |
| Phase 1 dispatch | Not implemented |
| Runtime compatibility namespace | `src/trim_haa/compat` is absent |
| Frozen provenance implementation | SHA-256 `92e075aa74afd0661fb6446c1253863883b651df735aaec0ec073638af0fdd14` |
| Provider/model/account | `BLOCKED` |
| Runtime | `BLOCKED_PENDING_SYNTHETIC_NO_SOURCE_INFERENCE_VERIFICATION` |
| Pricing | `BLOCKED_PENDING_POINT_IN_TIME_PRICING_FREEZE` |
| Final authorization | `BLOCKED` |
| Human coding | `BLOCKED` |
| Model execution | `BLOCKED` |
| Overall execution | `EXECUTION_BLOCKED` |
| Baseline repository tests | 389 passed on Python 3.11 and 389 passed on Python 3.12 at the starting commit |

The test counts are audit evidence at the named commit, not permanent targets
and not scientific evidence.

Current Core records are **legacy-unversioned**. `legacy-unversioned` is a
policy term for the absence of explicit version metadata; it is not a stored
version value. No existing record is formal Core version `"0"`, and no current
record is explicit Core version `"1"`. Core version `"1"` is not implemented.
Phase 1 is not implemented. Version-aware dispatch and the explicit legacy
compatibility boundary are not implemented.

The importable distribution remains the current core `trim_haa` package. The
wheel contains `trim_haa/indexing.py`, and the sdist contains
`src/trim_haa/indexing.py` plus its two standard-library distribution tests.
The study-only `trim_haa.llm` and `trim_haa.human_coding` modules, study data,
schemas, scripts, examples, research material, source packets, and protected
artifacts remain outside both wheel and sdist. Demonstrations and blocked-study
scaffolds remain source-checkout-only.

### Open-item register

Before this closure PR was opened, the GitHub state inspected on 2026-07-31
contained zero open pull requests and one open issue. The only open issue is
[#4, “Test provisional friction-locus values out of sample”](https://github.com/ZhijiWang/TRIM/issues/4).
It is deferred empirical research requiring a suitable out-of-sample corpus or
the later blinded pilot; it does not identify a current critical correctness,
data-loss, reproducibility, or packaging defect. The critical open-item count
is therefore zero. This record does not close or modify the issue.

## 2. What is considered complete

The following areas are complete **for the current alpha scope**:

- the current Core schema and `TrimHAAAnnotation` representation;
- parsing of current legacy-unversioned Core records;
- current Core record, relationship, and dataset validation;
- strict annotation indexing for every reviewed active non-frozen Core caller;
- deterministic rejection of empty and duplicate Core annotation identifiers
  without selecting a winner;
- provenance sidecar record support and frozen legacy lineage support;
- Core lock creation and verification under the current canonical payload;
- descriptive annotation and pre/AI/post comparison;
- case-, participant-, and study-level reporting helpers;
- valid and invalid synthetic dry-run workflows;
- verification of the frozen public walkthrough;
- wheel and sdist inclusion and exclusion boundaries;
- frozen ZIP, checksum-sidecar, and public-walkthrough verification; and
- the accepted future Core record-version and legacy compatibility policy.

“Complete” here means maintained behavior within the current schema and
compatibility boundary. It MUST NOT be read as completeness for every future
schema, identifier family, data source, execution environment, or study.

## 3. What remains deliberately incomplete

The status vocabulary used here is:

- `DEFERRED_BY_DESIGN`: accepted future work that lacks a concrete activation
  trigger;
- `BLOCKED_BY_GATE`: work prohibited until its recorded gates are explicitly
  cleared; and
- `OUT_OF_CURRENT_SCOPE`: work that is not part of maintaining the current
  alpha infrastructure.

| Deliberately incomplete area | Status | Current boundary |
| --- | --- | --- |
| Phase 1 version dispatch | `DEFERRED_BY_DESIGN` | No registry, dispatch errors, or compatibility adapter exists |
| Explicit compatibility adapter | `DEFERRED_BY_DESIGN` | `trim_haa.compat.legacy_unversioned` does not exist |
| Explicit Core version `"1"` schema | `DEFERRED_BY_DESIGN` | `core_record_version` is absent from `CORE_FIELDS` |
| Versioned serialization and canonical hashing | `DEFERRED_BY_DESIGN` | Current serialization and hashes remain unchanged |
| Versioned locking | `DEFERRED_BY_DESIGN` | Current lock payloads remain legacy-unversioned |
| Versioned migration and migration manifests | `DEFERRED_BY_DESIGN` | No records currently require migration |
| Mixed-version processing and reports | `DEFERRED_BY_DESIGN` | No explicit Core versions exist to mix |
| Provenance strict-index contract | `DEFERRED_BY_DESIGN` | Provenance-row identity needs its own error and compatibility contract |
| Lock-row strict-index contract | `DEFERRED_BY_DESIGN` | Lock and manifest identity need their own uniqueness contract |
| Exposure-event public strict-index contract | `DEFERRED_BY_DESIGN` | Exposure-event identifiers are not annotation identifiers |
| Gate-map contract | `DEFERRED_BY_DESIGN` | Gate entries require a manifest-specific contract |
| Participant/case assignment contract | `DEFERRED_BY_DESIGN` | Composite assignment identity remains contract-specific |
| Case/stage composite contract | `DEFERRED_BY_DESIGN` | Stage multiplicity is not an annotation-ID contract |
| Second-pass contract | `DEFERRED_BY_DESIGN` | Parent/stage uniqueness requires explicit semantics |
| Candidate-category contract | `DEFERRED_BY_DESIGN` | Study-only confidence categories need a separate contract |
| Manual and support-script contracts | `DEFERRED_BY_DESIGN` | Protected inputs and first-match behavior require individual review |
| Empirical study activity | `BLOCKED_BY_GATE` | Empirical execution is not authorized |
| Provider execution | `BLOCKED_BY_GATE` | Provider/account, runtime, pricing, and authorization remain blocked |
| Human coding and adjudication | `BLOCKED_BY_GATE` | Human-coding authorization remains blocked |
| Ethics approval | `OUT_OF_CURRENT_SCOPE` | No institution-specific approval is claimed |
| Stable public release | `OUT_OF_CURRENT_SCOPE` | The package remains `0.3.0a1`; no stability evidence is claimed |

The active identifier-indexing audit enumerates twenty non-annotation paths
across these contract families. Their existence does not by itself require
implementation. They become blockers only if a current active path
demonstrably depends on ambiguous identifiers and can produce an incorrect
result.

## 4. Maintenance-mode definition

Maintenance mode means the current alpha behavior and protected history are
preserved while changes are driven by observed needs rather than architectural
completeness.

During maintenance mode, the repository MAY accept:

- confirmed correctness or data-loss fixes;
- security fixes;
- reproducibility fixes;
- packaging breakage fixes;
- dependency compatibility fixes;
- documentation corrections;
- rights or licensing corrections;
- frozen-artifact verification fixes that do not change frozen content; and
- focused test improvements for existing behavior.

Such changes SHOULD identify the observed failure, affected current entrypoint,
compatibility impact, and validation evidence.

During maintenance mode, the repository MUST NOT accept without an explicit
reopening decision:

- speculative schema expansion or speculative abstractions;
- Core version `"1"` or Phase 1 implementation;
- new compatibility machinery without a concrete consumer;
- migration tooling without real records requiring migration;
- generic strict-index helpers without an active record-type contract;
- batch implementation of deferred paths for conceptual completeness;
- provider integration, human coding, or model execution;
- changes to study gates or frozen history; or
- new empirical, causal, reliability, validity, or generalisability claims.

## 5. Reopening triggers

Infrastructure development MAY reopen only when the triggering need is recorded
and independently reviewable.

### Core versioning trigger

A real dataset, external consumer, or required schema change needs explicit
version metadata. The reopening record MUST identify the actual record
producer, actual target schema, why legacy-unversioned handling is insufficient,
affected active entrypoints, compatibility requirement, and testing plan.

### Deferred identifier-contract trigger

A deferred record type is actively used in a path where an empty or duplicate
identifier can change a result, suppress an error, or select a winner. The
reopening record MUST name the record type, active caller, key semantics,
observed ambiguity, error contract, and compatibility boundary. A hypothetical
duplicate possibility is insufficient.

### Migration trigger

A real source artifact must be transformed to a different explicit schema
version. The source artifact, target contract, migration reason, preservation
requirement, and reviewed migration rule MUST all exist before tooling is
implemented. The source MUST remain unchanged.

### Study-execution trigger

Every applicable provider, runtime, pricing, final-authorization, ethics,
human-coding, model-execution, and overall-execution gate has been explicitly
cleared by its governing process. Preparation-only or controlled-access status
MUST NOT be treated as execution authorization.

### External-use trigger

An actual external user or dependent package requires behavior not covered by
the current alpha infrastructure. The reopening record MUST identify the
consumer, current incompatibility, support commitment, and acceptance tests.

## 6. Non-triggers

None of the following is sufficient to reopen infrastructure development:

- a deferred-work list exists;
- a future policy mentions a phase;
- an abstraction could appear cleaner;
- a generic helper could reduce code;
- a record type might someday need versioning;
- every dictionary has not been converted to a strict helper;
- the repository has not reached an imagined perfect architecture;
- the package remains an alpha;
- a developer wants to increase the test count;
- a developer wants every design document to have a matching implementation;
  or
- conceptual discomfort with deliberately deferred work.

## 7. Current API status

Current generic Core validators operate on the current legacy-unversioned
schema. Their names MUST NOT be interpreted as version-aware dispatch, and they
are not renamed or made version-aware by this boundary.

| Surface | Current role | Current input contract | Maintenance status | Future versioning status |
| --- | --- | --- | --- | --- |
| `TrimHAAAnnotation` | Current Core record object | Current legacy-unversioned Core fields | Maintained current-alpha API | Future explicit records require separate version-aware representation or dispatch |
| `validate_core_record` | Validate one Core record | Object or mapping using current legacy-unversioned schema | Maintained top-level API | Not version-aware |
| `validate_core_records` | Validate records, uniqueness, and relationships | Iterable of current Core records | Maintained top-level API; duplicate IDs are fatal | Not version-aware |
| `validate_relationships` | Validate parent links and cycles | Iterable of current Core records | Maintained module API; duplicate IDs select no winner | Not version-aware |
| `validate_dataset` | Validate Core, provenance, exposure, and lock relationships | Current legacy-unversioned record families | Maintained top-level API | Not mixed-version dispatch |
| `strict_annotation_index` | Fail-closed Core annotation lookup | Core objects or mappings with non-empty unique `annotation_id` | Maintained additive API, indexing version `"1"` | Independent of future Core record versions |
| `case_level_report` | Descriptive case report | Current Core records plus optional sidecars | Maintained module API; Core IDs and duplicate stages fail closed | Future mixed-version reporting is deferred |
| `participant_level_report` | Aggregate descriptive participant report | Current Core records and optional case report | Maintained module API | Future mixed-version reporting is deferred |
| `study_level_report` | Aggregate current descriptive study report | Current Core and sidecar families | Maintained module API | Future mixed-version reporting is deferred |
| `create_lock_record` / `lock_annotation` | Create current Core lock rows | Current legacy-unversioned Core record plus lock metadata | Maintained API | Versioned lock payloads are deferred |
| `verify_locked_annotation` | Verify current canonical Core payload | Current Core record and current `LockRecord` | Maintained top-level API | Cross-version lock reuse is forbidden by future policy |
| `AssistanceProvenance` and provenance helpers | Sidecar representation, hashes, grouping, lineage, export | Current provenance and Core records | Maintained; legacy indexing callers remain frozen | Future adapters must preserve original behavior |
| CLI `validate` | Validate one or more Core CSV files | Current legacy-unversioned Core CSV | Maintained installed command | Not version-aware |
| CLI `verify-lock` | Verify the first annotation against exactly one matching lock row | Current Core CSV and lock-manifest CSV | Maintained installed command; ambiguity fails | Versioned lock dispatch is deferred |
| CLI `compare` | Descriptively compare first rows | Two current legacy-unversioned Core CSV files | Maintained installed command | Versioned comparison is deferred |
| Source-checkout walkthrough | Run the older author-only technical demonstration | Repository-bound protected walkthrough files | Maintained compatibility demonstration | MUST remain outside unrestricted bundles |
| Synthetic dry run | Exercise current validation, locking, comparison, and reports | Repository synthetic fixtures | Maintained source-checkout demonstration | New versioned fixtures require a reopening decision |

## 8. Frozen and compatibility boundaries

The following boundaries remain protected:

- `src/trim_haa/provenance.py` is byte-frozen at SHA-256
  `92e075aa74afd0661fb6446c1253863883b651df735aaec0ec073638af0fdd14`;
- `annotation_index()`, `lineage_for()`, and `export_lineage_rows()` retain
  historical last-record-wins compatibility behavior;
- the function-scoped, line-number-independent legacy-call allowlist contains
  only `src/trim_haa/provenance.py::lineage_for` and
  `src/trim_haa/provenance.py::export_lineage_rows`;
- the synthetic dry run retains its compatibility-sensitive use of the frozen
  lineage export;
- the Japanese-canonical public walkthrough v0.2, its nested checksum records,
  and its tagged interpretation remain frozen;
- artifact ZIPs and `.sha256` checksum sidecars under `artifacts/` remain
  immutable verification evidence;
- frozen schemas, manifests, records, prompts, and PR #18 public references
  retain their pinned hashes and historical validation paths; and
- the older English walkthrough remains
  `NOT_AUTHORIZED_FOR_UNRESTRICTED_REDISTRIBUTION` and excluded from manually
  assembled public bundles.

Protected files MAY be inspected through established public metadata,
documentation, hash checks, and verification tests. Rights-sensitive or
controlled content MUST NOT be inspected without its separate authorization.
No protected file, checksum sidecar, pinned expectation, historical record, or
gate record may be mutated merely to satisfy current tests or future design.

Future compatibility infrastructure MUST preserve these paths and their
original interpretation exactly. The legacy allowlist MUST NOT be broadened for
convenience.

## 9. Deferred-work register

| Work item | Current status | Why deferred | Activation trigger | Forbidden shortcut |
| --- | --- | --- | --- | --- |
| Phase 1 dispatch and compatibility boundary | `DEFERRED_BY_DESIGN` | No explicit Core version or real consumer needs dispatch | A qualifying Core-versioning trigger names producers, entrypoints, compatibility, and tests | Implementing it only because the policy describes it |
| Core version `"1"` | `DEFERRED_BY_DESIGN` | Current records and consumers use the legacy-unversioned alpha schema | Phase 1 is complete and a real schema or external-use need exists | Adding `core_record_version="1"` to current records |
| Migration tooling | `DEFERRED_BY_DESIGN` | No source artifact has an approved explicit target contract | A named source, target, reason, preservation rule, and migration rule exist | In-place rewriting or relabelling legacy records |
| Mixed-version reports | `DEFERRED_BY_DESIGN` | No explicit Core versions currently coexist | A real mixed dataset and approved compatibility plan exist | Silently combining partitions |
| Provenance indexing | `DEFERRED_BY_DESIGN` | Provenance identity and report-error behavior need a distinct contract | A current provenance caller demonstrates result-changing ambiguity | Using `strict_annotation_index()` on provenance rows |
| Lock indexing | `DEFERRED_BY_DESIGN` | Annotation identity and manifest identity are not interchangeable | A current lock consumer demonstrates ambiguous selection | Reusing the annotation exception contract without review |
| Exposure indexing | `DEFERRED_BY_DESIGN` | Exposure-event IDs have their own lifecycle and validation behavior | Active exposure processing demonstrates result-changing duplicate or empty IDs | Treating an exposure event as a Core annotation |
| Gate maps | `DEFERRED_BY_DESIGN` | Gate status is manifest-governed study metadata | An active gate consumer demonstrates ambiguous duplicate gate entries | Normalizing duplicates before validation |
| Assignments | `DEFERRED_BY_DESIGN` | Participant/case identity is a composite contract | A real active assignment path demonstrates winner selection | Generic tuple indexing without assignment semantics |
| Case/stage indexes | `DEFERRED_BY_DESIGN` | Allowed stage multiplicity depends on reporting semantics | A current path demonstrates ambiguous same-case/same-stage rows not already rejected | Applying annotation-ID uniqueness to stage keys |
| Second-pass indexes | `DEFERRED_BY_DESIGN` | Parent/stage multiplicity needs an explicit rule | A real active second-pass workflow demonstrates first-winner ambiguity | Keeping only the first match |
| Candidate-category indexes | `DEFERRED_BY_DESIGN` | The path is study-only and categories are multi-valued domain data | Authorized study use reveals result-changing repeated categories | Deduplicating categories silently |
| Manual and support-script indexes | `DEFERRED_BY_DESIGN` | Inputs are varied and some are protected historical material | A named active script and identifier contract require correction | Repository-wide `strict_index_by` abstraction |
| Empirical study | `BLOCKED_BY_GATE` | Research, ethics, access, and execution prerequisites are incomplete | Applicable study and ethics gates are explicitly cleared | Treating passing software tests as empirical readiness |
| Provider integration | `BLOCKED_BY_GATE` | Account, runtime, pricing, and authorization are blocked | Exact provider/account and runtime evidence plus authorization exist | A live call during maintenance verification |
| Human coding | `BLOCKED_BY_GATE` | Eligibility, environment, packet, and authorization gates are blocked | The human-coding activation sequence is independently cleared | Packet inspection or synthetic status treated as consent |
| Stable release | `OUT_OF_CURRENT_SCOPE` | No external-use evidence or stable support commitment exists | A separate release decision defines support, compatibility, rights, and distribution evidence | Calling the current alpha stable |

## 10. Closure verdict

Code inspection, the strict-index audit, Python 3.11 and 3.12 baseline suites,
package construction and clean-install checks, extracted-sdist tests, frozen
hash and artifact checks, blocked dry-runs, gate records, rights documentation,
and GitHub open-item inspection identify no current critical correctness,
data-loss, reproducibility, or packaging blocker.

This is a software-infrastructure verdict only. It does not establish
interpretive truth, model error, model overconfidence, causal effects of AI
exposure, prevalence, generalisability, human reliability, detector validity,
ethics approval, participant validation, or authorization to execute a study.

READY_FOR_INFRASTRUCTURE_MAINTENANCE_MODE
