# Human-LLM Friction-Locus Pilot Planning Files

This directory contains protocol-only materials for a future small-N
demonstration study. The study asks:

What becomes visible when interpretive disagreement is represented
procedurally rather than only as label divergence?

## Included files

- `human_llm_friction_locus_pilot_protocol.md`: study protocol.
- `human_llm_friction_locus_analysis_plan.md`: analysis plan.
- `friction_locus_lineage_table.csv`: provisional lineage and validity table.
- `predicted_confusions.csv`: manual-derived predicted confusable pairs.
- `human_llm_sample_selection_log.csv`: empty protocol-only selection log
  template.
- `human_llm_protocol_freeze_checklist.md`: incomplete checklist for a later
  freeze task.

Related machine-readable planning files:

- `schemas/human_llm_coder_output.schema.json`
- `templates/human_coder_record.json`
- `templates/model_coder_record.json`
- `templates/human_llm_run_manifest.json`
- `templates/human_llm_allocation_manifest.json`

## Scope

This is a design branch only. It adds no empirical case data, no model output,
no results, no new framework layer, and no change to the released public
walkthrough.

The protocol positions TRIM as a teachable and auditable
disagreement-registration protocol for interpretation-intensive small-N work.
It does not claim empirical validation, a truth verdict, a universal annotation
solution, or an exhaustive ontology of interpretation.

The current protocol adopts Design B: a single-researcher pre-exposure human
record compared with independently generated model records. It is a procedural
human-model comparison, not a human intercoder reliability study and not
validation of human reproducibility. No external human recruitment is permitted
under the current protocol.

## Required later steps

Before implementation:

1. Independently audit this protocol.
2. Freeze the sample and source packets.
3. Freeze manual and prompt versions.
4. Complete and lock human coding before any AI execution.
5. Preserve raw model outputs before parsing.
6. Analyze procedural disagreement without treating either record as a gold
   standard.
