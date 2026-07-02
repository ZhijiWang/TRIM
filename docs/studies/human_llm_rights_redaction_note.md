# Human-LLM Pilot Rights Redaction Note

Status: `BLOCKED_RIGHTS_REVIEW_REQUIRED`

The public PR now stores source-packet metadata and private hashes only. Full passage text and translation text have been removed from the public source packets because source-level redistribution rights have not been independently cleared for every edition and translation.

The redaction preserves:

- case IDs;
- source universe IDs;
- bibliographic metadata;
- source URLs or source-file references;
- line-range references;
- private canonical-text hashes;
- private translation/gloss hashes where applicable;
- private source-packet hashes from the pre-redaction packet state;
- controlled-storage references without exposing local absolute paths.

The redaction does not establish that any source is unlawful to use for private research preparation. It only prevents the public PR from redistributing full packet text before edition-specific and translation-specific review is complete.

