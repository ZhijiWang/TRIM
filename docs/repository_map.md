# TRIM Repository Map

This page maps the repository as it exists on `main`. It is a navigation aid, not a migration plan. No current file movement is recommended.

## Stable naming hierarchy

- **Repository:** TRIM
- **Software framework/package:** TRIM-HAA
- **Python distribution:** `trim-haa`
- **Python namespace:** `trim_haa`
- **Active study:** Design B Human–LLM Friction-Locus Pilot
- **Public example:** In a Grove Public Walkthrough v0.2
- **Deferred human-subject line:** TRIM-HAA Human-Subject Exposure/Instrumentation Pilot
- **Historical line:** Legacy TRIM External-Coder Retest v0.2.x

## Current architecture

| Path | Purpose | Status | Authoritative? | Notes |
|---|---|---|---|---|
| Root metadata (`README.md`, `pyproject.toml`, `CITATION.cff`, `LICENSE`, `MANIFEST.in`) | Package identity, installation, citation, licensing, and distribution boundaries | `AUTHORITATIVE_ACTIVE` | Yes | `README.md` is the top-level entry point; packaging metadata defines the `trim-haa` distribution. |
| `src/trim_haa/` | Active TRIM-HAA Python implementation | `AUTHORITATIVE_ACTIVE` | Yes | Core installed-package namespace for validation, locking, provenance, comparison, and reporting. |
| `src/trim_haa/llm/` | No-call request, response-preservation, hashing, and execution-gate scaffold for the active study | `ACTIVE_SCAFFOLD` | No; study implementation | Source-checkout-only experimental study module. It is excluded from wheel and sdist. |
| `src/trim_haa/human_coding/` | No-coding authorization, lifecycle, locking, disagreement, and adjudication scaffold | `ACTIVE_SCAFFOLD` | No; study implementation | Source-checkout-only experimental study module. It is excluded from wheel and sdist. |
| `schemas/` | Core-adjacent and study-specific JSON Schemas | `AUTHORITATIVE_ACTIVE` | Mixed | Includes frozen coder/model interfaces and active blocked-study envelope and workflow schemas. Check references before changing paths. |
| `docs/` | Repository, software, methods, and research navigation | `AUTHORITATIVE_ACTIVE` | Yes for current documentation | Begin with [`docs/index.md`](index.md) and the [study index](studies/index.md). |
| `docs/manuals/` | Friction-locus coding manual, manifest, and compatibility/audit materials | `AUTHORITATIVE_FROZEN` | Yes | Contains frozen authoritative manual material established through PR #19. |
| `docs/studies/` | Active-study protocol, status, scaffold, and gate documentation | `ACTIVE_BLOCKED_STUDY` | Mixed | The [study index](studies/index.md) distinguishes active, demonstration, deferred, and historical lines. |
| `data/` | Public templates and repository-bound demonstration/study data | `AUTHORITATIVE_ACTIVE` | Mixed | Contents range from software templates to public study metadata; status is determined by the owning subsystem. |
| `data/studies/human_llm_pilot/` | Public study metadata, vendored public freeze references, and blocked preparation records | `ACTIVE_BLOCKED_STUDY` | Yes for current public study state | Controlled packet text is not part of the merged public preparation layer. Execution and human coding remain blocked. |
| `templates/` | Human/model record and run/allocation templates | `ACTIVE_SCAFFOLD` | Mixed | Some paths are referenced by frozen manifests or validators and require dependency review before migration. |
| `examples/synthetic_dry_run/` | Valid and invalid synthetic technical fixtures and rebuilt outputs | `PUBLIC_DEMONSTRATION` | No | Demonstrates deterministic validation behavior; it is not empirical validation. |
| `examples/in_a_grove_walkthrough/` | Repository-bound author-only walkthrough | `PUBLIC_DEMONSTRATION` | No | Demonstration material requiring a source checkout; it is not a human-subject study. |
| `examples/in_a_grove_walkthrough_public_v0_2/` | Frozen Japanese-canonical public walkthrough with locked author/model records and descriptive comparison | `PUBLIC_DEMONSTRATION` | Yes, as a frozen public demonstration | Tagged `in-a-grove-public-v0.2.0`; not empirical validation or a truth verdict. |
| `research/position_note/` | Position-note drafts, claim boundaries, manifests, and review response | `DEFERRED` | No | Separate research line; not the active Design B study. |
| `research/future_human_study/` | Ethics and protocol drafts for a future exposure/instrumentation pilot | `DEFERRED` | No | Not approved for recruitment, data collection, or current Design B execution. |
| `scripts/` | Source-checkout commands for demonstrations, validators, package builders, and blocked dry-runs | `AUTHORITATIVE_ACTIVE` | Operational | Installed-package and study-only boundaries vary by script; study scripts require repository resources. |
| `tests/` | Package, demonstration, frozen-boundary, and blocked-study tests | `AUTHORITATIVE_ACTIVE` | Yes for verification | Tests enforce package boundaries, frozen references, zero-call/zero-coding states, and schema behavior. |
| `artifacts/` | Frozen ZIP packages and checksum sidecars for position-note and future-study releases | `AUTHORITATIVE_FROZEN` | Yes for preserved artifacts | Treat ZIP/checksum pairs as immutable release evidence. |
| `docs/legacy_history.md` and tag `legacy-trim-v0.2.1` | Navigation to the removed Legacy TRIM External-Coder Retest v0.2.x runtime | `HISTORICAL_RETAINED` | Yes as history | Legacy runtime is retained through Git history/tag, not the active tree. |
| Frozen packet and prompt references associated with PR #18 | Controlled/frozen dependency references for the Design B study | `PRIVATE_OR_CONTROLLED_REFERENCE_ONLY` | Yes as frozen references | PR #18 remains open and draft. Controlled packet text is not present in the merged public preparation layer. |

## Distribution boundary

The installed `trim-haa` distribution contains the active core `trim_haa` modules. The experimental `trim_haa.llm` and `trim_haa.human_coding` study modules remain available only from a repository source checkout or repository source archive and are explicitly excluded from both wheel and sdist.

## Do not move without a versioned migration

The following paths or references are hash-, manifest-, validator-, test-, tag-, or audit-sensitive:

- `docs/manuals/`
- `schemas/human_llm_coder_output.schema.json`
- `schemas/human_llm_model_response.schema.json`
- `examples/in_a_grove_walkthrough_public_v0_2/`
- artifact ZIPs and their `.sha256` checksum sidecars under `artifacts/`
- study records with canonical hashes under `data/studies/human_llm_pilot/`
- frozen prompt and packet references associated with PR #18

Any future relocation requires a separately reviewed, versioned migration that identifies path consumers, preserves original provenance, updates permitted references, and explains hash consequences. This navigation cleanup intentionally makes no such movement.
