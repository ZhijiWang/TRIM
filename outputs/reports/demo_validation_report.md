# Demo Validation Report

## Dataset Files

- `data/demo_annotations.csv`
- `data/demo_annotations.json`

## Validation Checks

- Required field coverage.
- Controlled vocabulary conformance.
- Compound `rationale_mechanism` values.
- Compound `epistemic_support` values.
- Friction signature structure.
- Alternative signature structure.
- Rationale-note review warnings.

## Results

| File | Records | Errors | Warnings | Status |
| --- | ---: | ---: | ---: | --- |
| `data/demo_annotations.csv` | 10 | 0 | 0 | passed |
| `data/demo_annotations.json` | 10 | 0 | 0 | passed |

## Controlled Vocabulary State

- `discourse_level` is the package field name.
- `commentarial_discourse` is the controlled value used for `ZZ_ZHUANG_22`.
- `extradiegetic` is the accepted spelling for the extradiegetic discourse
  level.

## Validated Case IDs

| case_id |
| --- |
| `ZZ_XIANG_7` |
| `ZZ_MIN_1` |
| `ZZ_XI_4` |
| `ZZ_ZHUANG_22` |
| `MAC_1_3` |
| `MAC_4_1` |
| `MAC_5_8` |
| `GROVE_TAJOMARU` |
| `GROVE_MASAGO` |
| `GROVE_TAKEHIRO` |

Validation completed with 0 errors and 0 warnings.
