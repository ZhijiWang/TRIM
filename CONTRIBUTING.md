# Contributing

Contributions to TRIM are welcome through GitHub issues and pull requests.
Useful contributions include documentation improvements, validation tests,
reporting refinements, graph export improvements, and examples that clarify the
existing annotation workflow.

## Development Workflow

1. Open an issue describing the proposed change.
2. Fork the repository or create a feature branch.
3. Add or update tests where the change affects package behavior.
4. Run the test suite:

```bash
python -m pytest
python examples/demo_trim_workflow.py
```

5. Open a pull request with a concise summary of the change.

## Controlled Vocabulary Changes

Changes to controlled vocabulary require careful documentation. A proposal
should include:

- the proposed value;
- a definition;
- use conditions;
- contrasts with existing values;
- at least one worked example;
- expected effects on validation and comparison outputs.

Controlled vocabulary changes should preserve comparability across annotations.

## Annotation Scope

TRIM supports human-created annotation. Human coders assign interpretive labels,
write rationale notes, and adjudicate contested thresholds through scholarly
review.

Automated label inference is outside the core validation workflow. Contributions
should keep the package focused on schema conformance, controlled vocabulary
validation, comparison, graph export, and review support.
