# Locking and Lineage

TRIM-HAA lock records store a SHA-256 hash of a canonical Core annotation payload. Verification confirms that a later file still matches the locked record.

Locking supports auditability. It does not make an interpretation true, reliable, or independently validated.

Use:

```bash
trim-haa verify-lock tests/fixtures/trim_haa/core_valid.csv tests/fixtures/trim_haa/lock_valid.csv
```
