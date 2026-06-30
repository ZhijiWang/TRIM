# AI Execution Comparison Protocol

This protocol governs exploratory comparison of machine-executed TRIM
submissions. It is a software and protocol stress test only.

AI execution outputs must not be described as human coder submissions,
intercoder reliability evidence, empirical validation, human usability evidence,
cross-language validation, or independent human replication.

## Workflow

1. Ingest only verifiable locked submission files.
2. Record file hashes before validation.
3. Preserve raw records separately from generated reports.
4. Validate coding files against the matching package version.
5. Validate source segment IDs and shared-context use.
6. Validate question logs where available.
7. Run question/annotation consistency validation where both files are available.
8. Compare only common fields across versions.
9. Calculate field-level descriptive agreement.
10. Calculate primary/context evidence overlap.
11. Detect primary/context role reversals.
12. Classify high-level pathway relations conservatively.
13. Generate question-log diagnostics only when both logs are available.
14. Preserve AI outputs separately from future human retest data.

## Version Handling

v0.2.1 and v0.2.2 records may be compared only on common fields. Fields removed
from the v0.2.2 coder-facing template, such as `cue_family` and
`broad_function_family`, should not be treated as missing coder work.

## Pathway Categories

- `same_function_same_pathway`
- `same_function_different_pathway`
- `different_function_partially_shared_pathway`
- `different_function_different_pathway`
- `no_fit_disagreement`
- `insufficient_comparable_data`

Use `same_function_same_pathway` conservatively. A one-field difference should
not automatically be treated as a completely different pathway.

## Reporting Rules

Report descriptive comparison only. Do not headline Cohen's kappa,
Krippendorff's alpha, or Gwet's AC1. If a coefficient is ever calculated to test
software plumbing, place it in a technical appendix and state that AI-AI
agreement is not inferential evidence of human reliability.

Substantive AI labels must not be used as answer keys or as evidence for
revising cases, source text, function vocabulary, friction loci, rationale
mechanisms, uncertainty rules, shared-context rules, or evidence-selection
rules.
