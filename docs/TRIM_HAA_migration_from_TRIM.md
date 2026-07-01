# TRIM-HAA migration from legacy TRIM

Legacy TRIM remains historical and supported. Frozen v0.2.1/v0.2.2 coder-facing packages, source packets, codebooks, manifests, templates, hashes, and submissions are unchanged.

TRIM-HAA is a research extension, not v0.2.3.

## Reused legacy utilities

- segment-list coercion;
- controlled uncertainty values;
- selected legacy pathway vocabularies in optional depth;
- comparison patterns for evidence overlap;
- validation style;
- package/hash discipline as a design pattern.

## Fields dropped from Core

- `cue_family`;
- `broad_function_family`;
- `evidence_highlight`;
- `language_access_mode`;
- `case_scope`;
- `shared_context_ids`;
- full six-field signature.

## Fields moved to optional depth

- `context_segment_ids`;
- `evidence_anchor`;
- `anchor_node`;
- `friction_locus`;
- `epistemic_support`;
- `discourse_level`;
- `temporal_orientation`;
- full alternative signature;
- question-log reference.

## New provenance relationships

- pre-AI human lock;
- AI independent model run;
- post-AI human revision linked to the locked pre record;
- explicit exposed-AI linkage from post-AI provenance to the AI record/model run shown;
- exposure-event rows for future multiple-exposure support;
- optional control second pass linked to the locked pre record.

The lock status flag is not sufficient. A pre-AI record is auditably locked only when its canonical Core payload hash is stored in a lock manifest and later verified.

## Historical records

There is no automatic conversion of historical human-only TRIM records into human-AI records. Old human records may be reused only after contamination and ethics review.
