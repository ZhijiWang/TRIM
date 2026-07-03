# PR #18 Condition Manipulation Audit

Status: `passed_shared_baseline_with_declared_instruction_depth_increments_execution_blocked`

Revised manipulation name: shared structured annotation baseline with increasing levels of interpretive guidance.

The conditions are not "no manual versus concise manual versus full manual." All three receive the same task framing, source-packet envelope, model response schema, and structured annotation baseline. The manipulation is the amount of interpretive guidance supplied inside the condition payload.

## Shared Baseline

All three model conditions receive:

- no browsing and no tools;
- source packet only;
- no gold labels;
- no cross-condition visibility;
- no session reuse;
- same source-packet envelope;
- same model response schema;
- same evidence-ID requirement;
- same candidate-loci output requirement;
- same unresolved permission;
- same alternative-pathway requirement;
- same review-policy output field;
- same non-truth-verdict framing.

## Condition A Increment

Condition A adds:

- category names;
- short definitions;
- review-status wording for reserved and review-sensitive categories.

It does not add pairwise guidance, full dominance rules, full counterfactual suite, or manual worked examples.

## Condition B Increment

Condition B adds:

- concise operational sequence;
- no-candidate, one-candidate, two-candidate, and multi-candidate rules;
- cue and context positive-evidence rules;
- review-linkage rule.

It does not include the full manual content or manual worked examples.

## Condition C Increment

Condition C adds:

- full authoritative JSON manual content;
- full pairwise guidance;
- complete counterfactual suite;
- governance details;
- manual worked examples.

The full manual content is injected between `BEGIN_FULL_MANUAL_JSON` and `END_FULL_MANUAL_JSON` by the assembly harness.

## Isolation Checks

- shared system does not contain Condition B/C-only dominance guidance;
- Condition A does not contain pairwise or full dominance rules beyond the declared shared output baseline;
- Condition B does not contain the full manual;
- Condition C receives the declared full guidance;
- condition hashes are distinct;
- only the condition payload differs across A/B/C after shared components are fixed.

Execution remains blocked.
