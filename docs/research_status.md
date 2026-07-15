# Research Status

## Implemented

- Python package in `src/trim_haa`.
- Core annotation schema.
- Validation helpers.
- Provenance and exposure records.
- Lock creation and verification.
- Field-level comparison helpers.
- CLI smoke commands.

The software package is standalone for record validation, lock verification, provenance handling, and comparison. Demonstrations remain repository-bound and require a source checkout.

## Active Blocked Study

The Design B Human–LLM Friction-Locus Pilot is the active study. PR #20 has merged into `main` as a blocked preparation layer covering rights evidence, controlled packet handling, provider planning, no-call LLM preservation, and no-coding human annotation scaffolds.

Execution and human coding remain blocked. Provider/model/account availability, runtime verification, pricing, final authorization, human coding, and model execution are unresolved. No empirical execution has occurred, and no private packet content was merged into the public preparation layer.

The metadata-only provider/runtime capability audit dated 2026-07-13 found no local API credential, so it made no provider request and did not verify account access to `gpt-5.4-mini`. The [current evidence index](studies/human_llm_current_evidence_index.md) distinguishes this v0.2 audit from the historical v0.1 blocked records. Runtime candidates are documented but remain unfrozen pending separately authorized no-source synthetic inference verification; pricing and final authorization remain blocked.

## Demonstrated

- Synthetic dry run with valid and invalid fixtures.
- Author-only In a Grove walkthrough.
- Japanese-canonical public walkthrough v0.2 with locked author/model records and a frozen descriptive comparison.
- Position-note technical draft.
- Frozen artifact preservation by SHA-256.

## Under Review

- The Japanese-canonical public walkthrough v0.2 is frozen and tagged as `in-a-grove-public-v0.2.0`. It is a provenance-aware technical walkthrough demonstrating structured comparison between locked human and model annotations. It remains a representability demonstration and descriptive locked-record comparison, not empirical validation, a truth verdict, a replication study, or a general claim about model behaviour.

## Deferred

- Human-subject exposure study.
- Institution-specific ethics application.
- Independent participant-language review.
- Empirical validation and reliability analysis.
- A separate rights decision for the older author-only English walkthrough before unrestricted redistribution. The Japanese-canonical public walkthrough v0.2 has separate provenance and usage-guidance records.

## Not Established

TRIM-HAA has not established interpretive truth, model error, model overconfidence, causal effects of AI exposure, ethics approval, human validation, or a validated detector of interpretive closure problems.
