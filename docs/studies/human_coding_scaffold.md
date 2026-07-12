# Human-coding scaffold

Status: `HUMAN_CODING_BLOCKED`

This scaffold prepares metadata, authorization, lifecycle, locking, disagreement, and adjudication machinery for the frozen Design B human–LLM pilot. It does not register a real coder, authorize packet access, begin a coding session, create a selected-case annotation, complete an adjudication, or authorize model execution.

## Architecture

The implementation follows the existing `trim_haa` package under `src/trim_haa/human_coding/`.

- `gates.py` evaluates direct human-coding preconditions and raises `HumanCodingBlockedError` before any blocked session.
- `locking.py` provides canonical record hashes, frozen-coder-payload hash verification, immutable-state checks, and `LockedAnnotationError`.
- `lifecycle.py` implements copy-on-transition draft, submission, locking, amendment, supersession, and adjudication-source validation.
- `disagreement.py` compares two or more synthetic coder payloads without copying source-facing values or coder comments into its metadata summary.
- `schema_validation.py` resolves the existing frozen human coder schema locally. It has no network fallback.
- `dry_run.py` constructs only deterministic in-memory synthetic lifecycle records and validates the checked-in blocked plan.

The new annotation and adjudication schemas reference `schemas/human_llm_coder_output.schema.json#/$defs/human_coder_record`. They do not copy or modify the authoritative manual or frozen coder schema.

This scaffold is source-checkout research code, not part of the distributable `trim-haa` wheel or Python sdist and not a stable public API. Its dry-run requires the checked-in study metadata, schemas, synthetic fixtures, and vendored public PR #18 freeze files from a source checkout or repository source archive. It does not require a `.git` directory or access to the PR #18 branch.

## Coder roles and registry

The dry-run registry contains only:

- `SYNTHETIC_CODER_A` as a synthetic primary-coder role;
- `SYNTHETIC_CODER_B` as a synthetic secondary-coder role;
- `SYNTHETIC_ADJUDICATOR` as a synthetic adjudicator role.

These are test identifiers, not people or institutional identities. All three have training not started, authorization absent, coding eligibility false, private-packet access eligibility false, final authorization absent, and coding performed false.

Future real identity and role verification must occur outside public artifacts. Public records may use approved pseudonymous coder IDs only; they must not include addresses, private email, phone numbers, credentials, passwords, raw signatures, or other direct identifiers.

## Authorization lifecycle

A coding session may start only when every direct precondition passes:

1. rights evidence is sufficient for preparation;
2. controlled private-packet handling is sufficient for preparation;
3. coding environment is verified;
4. coder eligibility is true;
5. training is documented as passed;
6. coder authorization status is passed;
7. session authorization and a packet-access authorization reference are present;
8. packet hash verification is completed;
9. final authorization is passed;
10. the human-coding gate is passed;
11. record-locking readiness is verified.

The current restricted rights and controlled-access statuses satisfy preparation only. They do not authorize a packet view or coding event. Provider/model/account, runtime, and pricing are not added as direct human-coding dependencies because the current public protocol does not establish that coupling.

## Controlled coding environment

The checked-in environment is a draft candidate only. Network, clipboard, screenshots, printing, and exports are blocked. No packet is mounted, no real coder is logged in, encrypted storage is unverified, backup and retention controls are not verified, final authorization is blocked, and coding is not allowed.

Future operation requires a verified controlled local or institutional environment, access logging against `schemas/private_packet_access_log.schema.json`, controlled annotation storage, immutable record locking, and a retention policy that does not use deletion as correction.

## Blinded assignment

The checked-in assignment uses a non-resolving synthetic packet reference and a synthetic packet hash. It exposes no selected case, source identity, condition, packet path, or packet content. The assignment is not authorized for coding.

Future assignments must preserve the frozen allocation order while exposing only the minimum blinded reference needed by an authorized coder. This scaffold does not assign any real coder to any selected case.

## Annotation lifecycle

The wrapper supports these states:

- `DRAFT`: editable through a copy-returning edit function;
- `SUBMITTED`: no silent edits; a separate explicit withdrawal/reopen design would be required before future use;
- `LOCKED`: immutable;
- `AMENDED`: immutable correction record referencing the prior annotation ID and record hash;
- `SUPERSEDED`: readable, hash-valid lifecycle record linked to its amendment;
- `ADJUDICATION_PENDING`: no adjudicated label has been created;
- `ADJUDICATED`: future state requiring separate authorization and source-record linkage.

Every timestamp is supplied before the canonical hash is finalized. Any substantive change changes the hash. There is no force unlock, environment-variable bypass, deletion-based correction, or silent overwrite path.

## Locking and amendments

A draft can be edited without mutating the input object. Submission and locking return new records. A locked record cannot be edited or locked again. Correction requires a new immutable amendment that cites the locked record's annotation ID and exact record hash. A superseded lifecycle record is a new linked record; the prior locked record remains unchanged and hash-valid.

## Disagreement handling

The disagreement scaffold reports metadata only:

- exact substantive agreement;
- field names with disagreement;
- missing-value disagreement;
- candidate-category-set agreement;
- counts for multi-label intersection and union;
- confidence disagreement;
- whether adjudication is required.

Coder comments, free-text rationale, unresolved-ambiguity text, identities, session metadata, packet hashes, and other operational fields are excluded from automated agreement. The utility calculates no kappa, alpha, empirical reliability statistic, or study result.

## Adjudication workflow

Synthetic adjudication remains `DRAFT_BLOCKED`, has no adjudicated payload, and cites every source annotation record hash plus the disagreement-summary hash. Adjudication never replaces or mutates coder records. A future adjudicated record requires separate authorization, a verified adjudicator, all source hashes, a locked adjudication record, and preservation of all originals.

## Synthetic fixture and public/private policy

Fixtures contain invented neutral strings, synthetic coder/case/evidence identifiers, and synthetic hashes only. They contain no selected case IDs, source titles, quotations, packet text, screenshots, clipboard content, real identities, institutional identifiers, or credentials.

Public artifacts may contain pseudonymous identifiers, hashes, schema/manual references, lifecycle states, authorization references, timestamps, disagreement metadata, and adjudication metadata. They must not contain private packet content, source-derived coder comments, selected-source excerpts, private identity data, or credentials.

## Dry-run

Run:

```text
python scripts/dry_run_human_coding.py
```

The successful result is:

```text
DRY_RUN_VALID_HUMAN_CODING_BLOCKED
```

Success means only that the scaffold is internally consistent and fails closed. The plan reports zero packet inspections, zero real sessions, zero real annotations, zero real locks, and zero completed adjudications. Planned coder, annotation, double-coding, and adjudication counts remain `pending_protocol_freeze`; the scaffold does not infer them.

## Current unresolved blockers

- coding environment unverified;
- coder eligibility false;
- coder training incomplete;
- coder authorization absent;
- session authorization absent;
- packet hash verification not performed;
- final authorization blocked;
- human-coding gate blocked;
- record-locking readiness unverified pending independent audit.

Human coding remains `BLOCKED`. Model execution remains separately `BLOCKED` by its own provider/account, runtime, pricing, authorization, and execution gates.

## Future activation sequence

The only permitted future sequence is:

1. independently audit the human-coding scaffold;
2. verify real coder identities and roles outside public artifacts;
3. document coder training;
4. verify the controlled coding environment;
5. verify packet hashes under controlled access;
6. create real session authorizations;
7. grant final human-coding authorization;
8. begin human coding;
9. lock coder records;
10. run disagreement review;
11. adjudicate under separate authorization.

None of these steps is currently authorized.
