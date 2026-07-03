# Human-LLM Pilot Prompt Condition Audit

Status: `PASSED_MANUAL_COMPATIBILITY_EXECUTION_BLOCKED`

The A/B/C prompt bundle has been rebuilt against the authoritative manual `friction_locus_manual_v0_1` at merge commit `6364add9a89f3fe6d26043727b9d44cb21a76db0`. The prompt files are compatible with the study-specific schema and manual-required structured fields, but they are not execution-authorized.

## Shared Boundaries

All prompt scaffolds preserve:

- same case source packet insertion point;
- same output schema;
- same evidence-ID requirement;
- same exact eight-entry `candidate_loci` requirement;
- same review-policy and review-linkage fields;
- same alternative-pathway requirement;
- same no-browsing and no-tools rule;
- same session-isolation rule;
- same non-truth-verdict framing.

## Condition Assessment

Condition A is compatible as the short-definition condition. It does not include full decision-tree or worked-example material.

Condition B is compatible as the concise-rule condition. It includes operational rules but not the full manual or worked examples.

Condition C is rebuilt by deterministic reference to the authoritative manual paths and hashes. It covers manual identity, category set, candidate detection, dominance resolution, governance, review linkage, context positive-evidence requirements, and cue positive-evidence requirements.

No prompt condition should be used for model execution until rights, private packets, model/account verification, and final execution authorization pass.
