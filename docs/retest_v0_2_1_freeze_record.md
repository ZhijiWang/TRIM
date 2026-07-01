# TRIM v0.2.1 Retest Freeze Record

Freeze date: 2026-06-30

Branch: `pilot-informed-v0.2.1`

PR: #12, "Implement pilot-informed v0.2.1 revision and new-case retest package"

Frozen coder-package source commit: `ad59aaadd972bd1bbb65669903bf813ac76b1aa9`

Coder package path: `outputs/coder_packages/TRIM_retest_v0_2_1_coder_package.zip`

Coder package SHA-256: `012a71280f46cdb2327a6a90d3f4eb788ec44258eea56dfad70a06c6f3467ade`

Formal case count: 12

Package file count: 13

## Validation Status

Semantic-steering audit:

- `match_count=2`
- `verified_source_text_match_count=2`
- `unreviewed_high_risk_count=0`

The two semantic-steering matches occur inside verified source quotations with segment-level provenance:

- `ANT_GUARD_REPORT_S4`, F. Storr public-domain translation of Sophocles' *Antigone*
- `APOL_ORACLE_INQUIRY_S1`, Benjamin Jowett public-domain translation of Plato's *Apology*

Local tests: `120 passed`

GitHub Actions: Python 3.11 passed; Python 3.12 passed.

Source-text provenance status: every formal segment has non-empty source text, segment-level provenance, source location, edition or translation, quotation status, normalization notes, and copyright status.

Shared-context registry status: every remaining shared-context group has at least two member cases. The former singleton Othello group has been removed; `OTH_HANDKERCHIEF_CHAIN` uses `multi_passage_single_case`.

## Known Methodological Limitations

- The v0.2.0 pilot remains a diagnostic usability and method-development pilot, not a final reliability study.
- The v0.2.1 retest has not yet been completed and must not be reported as empirical evidence until external coding, locking, comparison, and adjudication are finished.
- Public-domain translations support offline coding but do not establish cross-language construct validity.
- The function vocabulary remains project-specific and should not be claimed as domain-general without later replication.
- Agreement should be interpreted field by field and pathway by pathway; one global reliability coefficient is not the headline outcome.
- Source-text provenance reduces summary mediation but does not remove interpretive judgment from evidence selection.

## Freeze Rule

After coder distribution, no further codebook, packet, schema, or formal case changes should occur under the same version identifier.

Any post-distribution change to coder-facing materials requires a new version identifier, new package hash, documented migration note, and explicit decision on whether previously completed coding remains comparable.
