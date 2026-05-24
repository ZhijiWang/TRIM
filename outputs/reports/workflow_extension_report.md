# Workflow Extension Report

## Files Added

- `data/source_segments_demo.csv`
- `data/second_coder_template.csv`
- `data/second_coder_practice_cases.csv`
- `docs/segmentation_workflow.md`
- `docs/second_coder_onboarding.md`
- `docs/intercoder_workflow.md`
- `docs/TRIM_Coding_Manual_v0_2_rationale_mechanism.md`
- `docs/methodological_position.md`
- `docs/article_use.md`
- `examples/run_trim_with_source_segments.py`
- `examples/run_intercoder_demo.py`
- `examples/TRIM_demo_workflow.ipynb`
- `tests/test_source_segments_workflow.py`

## Source Segmentation Workflow Status

The optional source-segmentation layer is documented and demonstrated with
three In a Grove source segments. The example script links segment IDs to the
existing TRIM annotation schema and writes validation, comparison, report, and
graph outputs.

Generated outputs:

- `data/in_a_grove_three_cases_with_segments.csv`
- `outputs/reports/in_a_grove_segments_validation.csv`
- `outputs/reports/in_a_grove_segments_report.md`
- `outputs/tables/in_a_grove_segments/`
- `outputs/graphs/in_a_grove_segments.graphml`
- `outputs/graphs/in_a_grove_segments.json`

## Second-Coder Packet Status

The repository now includes a second-coder onboarding document, a three-case
template, practice cases, an intercoder workflow guide, and a small report
script. These files prepare future independent coding and field-level
comparison.

Generated output:

- `outputs/reports/intercoder_demo_report.md`

## Rationale Mechanism Manual Status

The `rationale_mechanism` coding manual documents allowed values, compound
mechanism rules, value definitions, demo examples, key distinctions, and a
decision sequence for reliability work.

## Notebook Status

`examples/TRIM_demo_workflow.ipynb` provides a minimal notebook for loading
demo annotations, validating records, displaying comparison tables, and
summarizing the corpus graph.

## Verification

- `python -m pytest`: 53 passed.
- `python examples/run_trim_with_source_segments.py`: completed successfully.
- `python examples/run_intercoder_demo.py`: completed successfully.

## Remaining Future Work

- Real second-coder pilot.
- Zenodo DOI after release.
- Possible future PyPI release.
- Optional expansion to the full Zuo zhuan corpus.
