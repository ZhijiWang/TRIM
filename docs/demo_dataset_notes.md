# Demonstration Dataset Notes

The TRIM demonstration dataset is a method demonstration corpus with ten
annotations. It is designed to show how the schema, controlled vocabulary,
comparison utilities, graph export, and contested-threshold workflow operate
together.

## Dataset Composition

The dataset contains:

- four Zuo zhuan divination cases;
- three Macbeth prophecy cases;
- three In a Grove testimony cases.

Each row represents one TRIM annotation with human-selected evidence nodes,
anchor node, threshold-rationale signature, function label, rationale note, and
coder metadata.

## Demonstration Patterns

The dataset supports the following comparison patterns:

- same function / different signature;
- same cue / different function;
- broad testimonial form / different signature;
- contested dominant threshold review.

The dataset is a compact demonstration set rather than a full corpus. It is
intended for method illustration, software testing, and reproducible examples.
It establishes neither domain-general reliability nor universal
reproducibility.

Software-generated comparison tables identify structural patterns and provide
`comparison_prompt` text. Researcher-authored worked interpretations of the two
same-function groups are documented in
[`substantive_demo_interpretations.md`](substantive_demo_interpretations.md).
