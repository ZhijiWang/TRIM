# TRIM v0.2.2 Retest Freeze Record

Version: v0.2.2

Freeze date: 2026-06-30

Branch: `pilot-informed-v0.2.2`

Commit SHA: recorded in the final PR head and release-readiness report. The
package contents are frozen by SHA-256 in
`data/retest_v0_2_2_frozen_file_hashes.csv`.

Source package inherited from v0.2.1:

- frozen v0.2.1 coder ZIP:
  `outputs/coder_packages/TRIM_retest_v0_2_1_coder_package.zip`
- frozen v0.2.1 SHA-256:
  `012a71280f46cdb2327a6a90d3f4eb788ec44258eea56dfad70a06c6f3467ade`

v0.2.2 coder-facing changes:

- removed `cue_family` from the coder-facing coding template;
- removed `broad_function_family` from the coder-facing coding template;
- clarified real-time question logging in the coder guide and execution
  protocol;
- included a coder return-manifest template;
- preserved all formal cases, source-text segments, source provenance,
  controlled vocabularies, shared-context registry, evidence-selection rules,
  and uncertainty definitions.

Coder package path:
`outputs/coder_packages/TRIM_retest_v0_2_2_coder_package.zip`

Coder package SHA-256:
`3b3ac302d8491e429d20b1d4fb1c66351ad0e6340698b2f5cd683adb5e0d4cb4`

Package file count: 14

Semantic-steering audit:

- `match_count=2`
- `verified_source_text_match_count=2`
- `unreviewed_high_risk_count=0`

The two matches occur inside verified source quotations backed by segment-level
provenance.

Tests:

- Python 3.11: `132 passed`
- Python 3.12: `132 passed` with two NetworkX future warnings

CI: verify GitHub Actions on the final PR head before distribution.

Known limitations:

- v0.2.2 has not yet been completed by human external coders.
- The v0.2.1 AI dry run is a protocol stress test only and is not reliability
  evidence.
- Public-domain translations support a standardized coding packet but do not
  establish cross-language validity.
- The function vocabulary remains project-specific.

This package is intended for human external-coder deployment after local tests
and CI pass.

No v0.2.2 coder-facing material may be changed after distribution without
creating a new version identifier, new package hash, documented migration note,
and explicit decision on whether previously completed coding remains comparable.
