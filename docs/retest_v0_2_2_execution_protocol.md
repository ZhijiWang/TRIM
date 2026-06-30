# TRIM v0.2.2 Retest Execution Protocol

This protocol governs execution after the v0.2.2 coder package has been frozen and distributed. It does not change the empirical design, codebook, schema, source packet, or case selection.

## Empirical Sequence

1. Distribute the frozen coder package.
2. Record the package SHA-256 used by each coder.
3. Complete coding independently.
4. Complete the question log in real time as questions arise and complete the
   language-access form.
5. Submit and lock raw coder files.
6. Validate returned file structure.
7. Produce a raw comparison report.
8. Calculate field-level agreement.
9. Calculate evidence overlap.
10. Identify pathway configurations.
11. Conduct a post-coding interview if planned.
12. Perform close adjudication.
13. Classify disagreement type.
14. Preserve raw disagreement.
15. Write retest results without retroactively altering coder records.

## Locking Rules

- Raw submissions are locked before comparison.
- Raw disagreement is preserved even when adjudication later identifies error, ambiguity, or compatible difference.
- Adjudication output is a separate analytic layer.
- Any change to coder-facing materials after distribution requires a new version identifier and package hash.
- Questions should be logged when they arise during coding, not reconstructed in
  a batch after all cases are complete.
- Self-resolved questions must still be logged.
- Timestamps should reflect when the issue arose. If exact timing is unavailable,
  mark the timestamp as approximate rather than fabricating precision.
- Batch-created identical timestamps must be disclosed as a protocol deviation.

## Planned Outcome Categories

- Exact alignment.
- Compatible difference.
- Same function / different pathway.
- Different function / partially shared pathway.
- Substantive pathway variation.
- Codebook ambiguity.
- Coder error.
- Insufficient evidence.
- Unresolved legitimate alternatives.

## Analysis Order

Begin with descriptive completion and usability checks, then field-level comparison, then evidence-overlap analysis, then pathway-level classification, and only then adjudication. Do not treat the primary coder as ground truth.

Chance-corrected reliability coefficients may be reported in supplementary material with caveats if the final design and sample size justify them. They should not replace field-level and pathway-level reporting.
