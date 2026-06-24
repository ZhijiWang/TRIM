# Demonstration Dataset Notes

The TRIM demonstration dataset is a ten-case method corpus showing how the schema, controlled vocabulary, comparison utilities, graph export, and contested-threshold workflow operate together.

## Dataset Composition

The corpus contains:

- four *Zuo zhuan* divination cases;
- three *Macbeth* prophecy cases;
- three *In a Grove* testimony cases.

Each row records human-selected evidence nodes, an anchor node, a threshold-rationale signature, a function label, a rationale note, and coder metadata.

## Demonstration Patterns

The corpus supports four comparison patterns:

- shared function with different signatures;
- shared cue with different functions;
- shared broad form with different signatures;
- contested dominant-threshold review.

These patterns establish schema expressivity, workflow traceability, and comparative payoff. Software-generated tables locate structural relations through `comparison_prompt`. Researcher-authored interpretations appear in [`substantive_demo_interpretations.md`](substantive_demo_interpretations.md).

Independent coding and larger out-of-sample work form the next empirical stages.
