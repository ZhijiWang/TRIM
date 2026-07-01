# TRIM-HAA locking and lineage

TRIM-HAA uses two separate relationship types:

- `parent_annotation_id`: human revision lineage;
- `exposed_ai_annotation_id`: AI output shown during review.

For the standard human-first flow:

```text
HUMAN_POST.parent_annotation_id = HUMAN_PRE
HUMAN_POST provenance exposed_ai_annotation_id = AI_RECORD
```

The AI record is exposure evidence, not the parent of the human revision.

## Cryptographic lock

A locked status flag is not sufficient. A pre-AI record is auditably locked only when:

1. the Core row has `status=locked`;
2. the provenance row has `lock_status=locked`;
3. a lock-manifest row exists;
4. the current canonical Core payload hashes to the stored SHA-256.

## Canonical payload

The canonical payload uses:

- fixed `CORE_FIELDS` order;
- stable pipe-separated segment IDs;
- UTF-8 JSON;
- normalized line endings;
- no mutable runtime metadata;
- no timestamps outside Core fields;
- compact deterministic whitespace.

If the canonical hash changes, validation reports an error.

