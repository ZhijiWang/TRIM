# Human-LLM Pilot Manual Gap Report

Status: `BLOCKED_INCOMPLETE_AUTHORITATIVE_MANUAL`

This audit found no complete authoritative current Design B friction_locus coding manual in the active repository tree. The freeze therefore cannot treat the protocol, lineage table, and predicted-confusions table as an executable manual bundle.

## Candidate Files Audited

| Candidate | Commit | Assessment |
| --- | --- | --- |
| `docs/studies/human_llm_friction_locus_pilot_protocol.md` | `6998175eeca5d349072bf31012c69f2d568f28ec` | Study protocol. It defines Design B and study governance, but it is not a complete operational coding manual. |
| `docs/studies/friction_locus_lineage_table.csv` | `6998175eeca5d349072bf31012c69f2d568f28ec` | Category lineage and short definitions. It does not provide a full decision procedure. |
| `docs/studies/predicted_confusions.csv` | `6998175eeca5d349072bf31012c69f2d568f28ec` | Confusable-pair and counterfactual-test table. It is supporting material, not a manual. |
| `docs/TRIM_Coding_Manual_v0_2_1_friction_locus.md` | `252f4b1c867751bd996885ec674f5f546ddbc110` | Historical legacy TRIM manual found in the archival tag. It is not in the active tree and has not been adopted as the authoritative current Design B manual. |
| `docs/TRIM_Coding_Manual_v0_2_friction_locus_final.md` | `252f4b1c867751bd996885ec674f5f546ddbc110` | Earlier historical legacy TRIM manual. It is not an active current Design B manual. |

## Completeness Result

No active file was found that contains all required operational components:

- all controlled category values with operational definitions;
- use-when guidance for each value;
- use-another-value guidance for near misses;
- confusable-with guidance;
- counterfactual tests;
- a full decision tree;
- positive examples approved for manual use without leaking study-sample material;
- reserved or review-required category rules;
- escalation rules.

The legacy manuals contain substantial operational guidance, but they are historical TRIM documents. Re-adopting or revising them for Design B would be a new manual-authoring task, not a correction that can be silently made inside this freeze revision.

## Consequence

The manual freeze remains blocked. Condition C cannot be execution-ready because it cannot include or deterministically reference a complete authoritative current manual. Conditions A and B remain non-executable scaffolds until the manual and model are both frozen.

