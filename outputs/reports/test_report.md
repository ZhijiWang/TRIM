# TRIM v0.1.1 Test Report

## Commands

```bash
python -m pytest
```

Result: 47 passed.

```bash
python examples/demo_trim_workflow.py
```

Result: demo workflow completed successfully.

## Workflow Outputs

- Loaded 10 CSV annotations.
- Loaded 10 JSON annotations.
- Completed validation with 0 errors and 0 warnings.
- Wrote normalized annotations, comparison tables, and reports.
- Built schema-component graph with 56 nodes and 46 edges.
- Built corpus graph with 76 nodes and 102 edges.
- Wrote GraphML and JSON graph outputs.

## Behavioral Checks

| Check | Result |
| --- | --- |
| Correct `extradiegetic` spelling is accepted | passed |
| Previous misspelling is rejected | passed |
| `discourse_level` is treated as a field name | passed |
| Invalid `friction_locus` vocabulary value is rejected | passed |
| Short `rationale_note` emits the review warning | passed |
| Same function / different signature table includes `immediate_stabilization` | passed |
| Same function / different signature table includes `extended_deliberation` | passed |
| Same cue / different function table includes `prophecy` | passed |
| Same-cue filter isolates `prophecy` | passed |
| Same-cue report separates the primary prophecy test from additional groups | passed |
| Broad family / different signature table includes `self-exculpatory testimony` | passed |
| Contested cases table includes `ZZ_XI_4` | passed |
| GraphML output exists and is non-empty | passed |
| JSON graph output exists and is non-empty | passed |

## Test Suite Summary

- Test files collected: `test_cli.py`, `test_compare.py`, `test_graph.py`,
  `test_intercoder.py`, `test_schema.py`, `test_validator.py`
- Total tests: 47
- Passed: 47
- Failed: 0
