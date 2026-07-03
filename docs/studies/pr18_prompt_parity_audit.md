# PR #18 Prompt Parity and Comparability Audit

Status: `passed_with_documented_interface_and_metadata_asymmetries_execution_blocked`

Manual reference: `friction_locus_manual_v0_1` at `6364add9a89f3fe6d26043727b9d44cb21a76db0`.

This audit separates primary human-versus-model Condition C comparability from the A/B/C model-condition manipulation. It does not authorize execution.

## Primary Human Versus Model Condition C Comparability

| Dimension | Human Condition C | Model Condition C | Assessment |
|---|---|---|---|
| source packet | controlled private packet after rights/private-packet clearance | same controlled private packet after rights/private-packet clearance | identical once gates pass |
| substantive manual content | full authoritative JSON manual | full authoritative JSON manual injected into assembled prompt | identical substantive content |
| category definitions | authoritative eight categories | same | identical |
| candidate rules | all eight candidate-locus states required | same | identical |
| counterfactual guidance | full manual guidance | full manual guidance | identical |
| examples visible | full manual worked examples visible | same full manual worked examples visible | identical substantive visibility |
| context restrictions | packet-only, no external browsing unless packet permits bridge | packet-only, no browsing/tools | functionally equivalent |
| output fields | final human record includes interpretive fields plus system-added metadata | model-authored payload first; harness later enriches final record | intentional metadata/enrichment asymmetry |
| unresolved permission | allowed and required where evidence/tests do not support a final locus | same | identical |
| review policy | same reserved/review-sensitive/standard policy | same; model proposal later enriched by harness | functionally equivalent |
| interface affordance | human may search within the supplied manual | model receives prompt text and no tools | documented interface asymmetry |
| timing | human record locked before any model execution | model runs occur only after human lock | intentional methodological asymmetry |
| record locking | human record hash computed after completion | model raw response hash before parsing, final record hash after enrichment | intentional role-specific asymmetry |
| metadata enrichment | system adds record ID, timestamp, source hash, session ID, record hash | harness adds run/provider/prompt/source/raw-output/parse/retry metadata | intentional role-specific asymmetry |

Unresolved substantive asymmetries: none identified in the specified content. Execution remains blocked for rights, private-packet handling, model/account verification, runtime settings, and final authorization.

## A/B/C Model-Condition Manipulation

The A/B/C comparison is internal to model conditions only. It is not the same as human/model parity.

Revised manipulation name: shared structured annotation baseline with increasing levels of interpretive guidance.

Condition A adds short category definitions and review-status wording.

Condition B adds concise operational rules, including candidate-count dominance handling, cue/context positive rules, and review linkage.

Condition C adds full authoritative JSON manual content, including full pairwise guidance, complete counterfactual suite, governance details, and worked examples.

No condition receives gold labels, expected case outcomes, another condition's output, or a prior human record.
