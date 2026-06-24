# Schema and Validator Changes for Unreleased 0.2.0

This note records the validation changes introduced before the first formal 0.2.0 release.

## Evidence and Anchor Structure

Standard annotations now include one or more evidence nodes, a source-facing `evidence_anchor`, and a normalized `anchor_node`.

The demonstration records already use this structure. Blank second-coder templates become valid after their evidence, anchor, signature, and rationale fields are completed.

Graph conversion now preserves the full evidence-to-anchor pathway. Projects adopting this source version should retain both the source reference and the analytic anchor label.

## Contested Rationale Structure

An `alternative_signature` activates two checks: the alternative pathway parses as a complete signature, and `rationale_note` contains at least 60 characters.

The length threshold provides a language-neutral minimum for review documentation. Interpretive quality remains part of scholarly assessment.

## Command-Line Status

`trim validate` writes the CSV report and returns `0` for valid or warnings-only input and `1` when errors are present. `--always-zero` supports report-only workflows.
