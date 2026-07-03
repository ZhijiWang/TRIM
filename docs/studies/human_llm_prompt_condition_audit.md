# Human-LLM Pilot Prompt Condition Audit

Status: `PASSED_STATIC_PROMPT_SCHEMA_AND_ASSEMBLY_COMPATIBILITY_EXECUTION_BLOCKED`

The A/B/C prompt bundle has been rebuilt against the authoritative manual `friction_locus_manual_v0_1` at merge commit `6364add9a89f3fe6d26043727b9d44cb21a76db0`. The prompt files are compatible with the model-authored response schema, deterministic assembly is specified, and the final enriched record contract is documented. They are not execution-authorized.

## Shared Boundaries

All prompt scaffolds preserve:

- same case source packet insertion point;
- same model-authored response schema;
- same evidence-ID requirement;
- same exact eight-entry `candidate_loci` requirement;
- same review-policy payload field;
- same alternative-pathway requirement;
- same no-browsing and no-tools rule;
- same session-isolation rule;
- same non-truth-verdict framing.

## Condition Assessment

Condition A is compatible as the short-definition condition. It does not include pairwise guidance, full dominance rules, full decision-tree material, full manual content, or worked examples.

Condition B is compatible as the concise-rule condition. It includes operational rules but not the full manual content or worked examples.

Condition C is rebuilt as a deterministic assembled payload. It injects the full authoritative JSON manual content between `BEGIN_FULL_MANUAL_JSON` and `END_FULL_MANUAL_JSON`; it does not rely on repository access by the model. It covers manual identity, category set, candidate detection, dominance resolution, governance, review linkage, context positive-evidence requirements, and cue positive-evidence requirements.

The manipulation is now described as: shared structured annotation baseline with increasing levels of interpretive guidance.

No prompt condition should be used for model execution until rights, private packets, model/account verification, and final execution authorization pass.
