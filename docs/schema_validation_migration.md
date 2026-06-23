# Schema and Validator Hardening for Unreleased 0.2.0

This note describes validation-boundary changes made before any formal 0.2.0
release. No released TRIM version is being retroactively changed.

## Evidence and Anchor Migration

Standard annotations now require:

- at least one non-empty `evidence_nodes` item;
- a source-facing `evidence_anchor`;
- a normalized analytic `anchor_node`.

Existing complete demonstration records already satisfy these rules. Incomplete
second-coder templates remain scaffolds and will fail validation until their
coding fields are filled.

Graph conversion no longer substitutes one anchor field for another and no
longer emits an evidence-free standard graph. Projects with records missing
these fields should add evidence-node decomposition and preserve both the source
reference and analytic anchor label before adopting this source version. No
field is deleted and no automatic rewriting is performed.

## Contested Rationale Migration

`alternative_signature` no longer triggers an English-keyword check. Instead:

- the alternative signature must parse and validate;
- `rationale_note` must contain at least 60 characters.

The character threshold is a minimal, language-neutral documentation safeguard,
not an assessment of interpretive quality.

## CLI Migration

`trim validate` now writes the requested CSV report and returns:

- `0` for no errors, including warnings-only reports;
- `1` when one or more errors are present.

Use `--always-zero` only for report-generation workflows that intentionally
handle validation status outside the process exit code.
