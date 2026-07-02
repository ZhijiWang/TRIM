# Wheel Contents Audit v0.1

Wheel filename: `trim_haa-0.3.0a1-py3-none-any.whl`

SHA-256: `842d9ceee38e08d4b6d33fdc675821e6a8bd766a067a53220844e0fe8a353ed1`

Package version: `0.3.0a1`

## Included Top-Level Paths

- `trim_haa/`
- `trim_haa-0.3.0a1.dist-info/`

Included package modules:

- `trim_haa/__init__.py`
- `trim_haa/__main__.py`
- `trim_haa/cli.py`
- `trim_haa/comparison.py`
- `trim_haa/depth.py`
- `trim_haa/exposure.py`
- `trim_haa/hashing.py`
- `trim_haa/locking.py`
- `trim_haa/provenance.py`
- `trim_haa/reporting.py`
- `trim_haa/schema.py`
- `trim_haa/validator.py`

The wheel includes only package code, license metadata, entry-point metadata, and standard wheel metadata.

## Excluded Categories

Confirmed absent from the wheel:

- `research/`
- `examples/`
- `artifacts/`
- `tests/`
- ethics drafts
- source text packets
- legacy TRIM package paths
- artifact ZIP files

The walkthrough source packet is not distributed inside the wheel.

## Dependency Classification

`pandas` classification: `optional_reporting_only`.

The installed core package does not require `pandas` for import, validation, lock verification, provenance handling, comparison, or CLI smoke commands. `trim_haa.reporting` imports `pandas` only when reporting helpers are used. The optional dependency group is `trim-haa[reporting]`; the test extra includes `pandas` for reporting tests.

## Clean-Install Smoke Test

Clean environment location: temporary virtual environment outside the repository.

Result: passed.

Commands confirmed:

- `python -c "import trim_haa; print(trim_haa.__version__)"` printed `0.3.0a1`.
- `trim-haa --help` succeeded.
- `trim-haa version` printed `0.3.0a1`.
- `trim-haa validate <copied-valid-fixture>` succeeded.
- `trim-haa verify-lock <copied-annotation-fixture> <copied-lock-fixture>` succeeded.
- `trim-haa compare <copied-left-fixture> <copied-right-fixture>` succeeded.
- `trim-haa run-walkthrough` failed with the documented source-checkout requirement and no traceback.
- `trim-haa run-synthetic` failed with the documented source-checkout requirement and no traceback.

This audit does not claim that the package is ready for PyPI.
