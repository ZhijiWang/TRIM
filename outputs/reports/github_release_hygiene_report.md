# GitHub Release Hygiene Report

## Completed

- Removed macOS resource files from the local release tree.
- Updated `.gitignore` for macOS files, Python cache files, virtual
  environments, environment files, build artifacts, and package metadata.
- Replaced the static test badge with the GitHub Actions workflow badge.
- Checked `CITATION.cff` and added repository URLs.
- Added release instructions in `docs/release_instructions.md`.
- Added repository settings recommendations in
  `outputs/reports/github_repository_settings_recommendations.md`.
- Simplified the `friction_locus` decision tree to follow a linear coding
  sequence.

## Verification

- `python -m pytest`: 47 passed.
- `python examples/demo_trim_workflow.py`: completed successfully.

## Remaining Manual Steps

- Add repository description and topics on GitHub.
- Create the `v0.1.1` GitHub release.
- Connect the release to Zenodo.
- Add the DOI after the Zenodo archive is created.
