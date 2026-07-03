# Human Coder Access and Record Specification

Status: `HUMAN_ACCESS_SPECIFIED_EXECUTION_BLOCKED`

This specification defines the intended primary human coding setup. It does not authorize researcher coding.

## Human Condition C Content

The primary human coder receives the same substantive Condition C manual content as the model Condition C assembled input:

- manual source: `docs/manuals/friction_locus_manual_v0_1.json`
- manual SHA-256: `797d79fcdb29fc32850c3778c6afb029ac0768207ea33f66d714fe8fa8cb591a`
- delivery form: full authoritative JSON manual, LF-normalized
- worked examples: visible

The worked examples in the manual are training/manual examples, not study cases. They may be read as part of the manual. The coder must not copy example outcomes mechanically and must not treat examples as source evidence for any study case.

## Source Packet Access

The coder receives the same controlled source-packet layers that will later be supplied to model runs. Public PR packets are redacted metadata-only records and are not executable source packets.

No external browsing or secondary scholarship is allowed unless the frozen source packet itself includes a permitted contextual bridge.

## Search and Notes

Search within the supplied manual is allowed. This is an interface asymmetry relative to model prompt scanning, but the substantive manual content is identical. Personal procedural notes are allowed only if they are made before coding begins, contain no case-specific source text or expected outcomes, and are archived with the session materials if used.

## Human-Authored and System-Added Fields

The human authors interpretive fields such as selected evidence, primary label, candidate-locus states, counterfactual tests, proposed locus, alternatives, uncertainty, decision path, and rationale.

The system adds or verifies:

- record ID;
- timestamp;
- source packet hash;
- coding session ID when system-generated;
- final record hash.

The human coder does not manually calculate cryptographic hashes.

## Locking and Later Review

The primary human record is completed and locked before any model execution. A later adjudication or reflection event is a separate record. It must link to the original record and must not overwrite the original.
