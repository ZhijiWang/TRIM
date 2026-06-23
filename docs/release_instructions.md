# Release Instructions

The repository currently has no formal GitHub Release. Package version 0.1.2 is
an unreleased source version.

Before publishing a future release:

1. Confirm the package version is consistent in `pyproject.toml`,
   `CITATION.cff`, `CHANGELOG.md`, and the README.
2. Replace the changelog's `Unreleased` marker with the release date.
3. Run:

   ```bash
   python -m pytest
   python examples/demo_trim_workflow.py
   python examples/run_trim_with_source_segments.py
   python examples/run_intercoder_demo.py
   ```

4. Confirm regenerated outputs are committed and documentation links resolve.
5. Create a signed or annotated version tag only after the release commit is
   reviewed.
6. Publish the GitHub Release from that tag.
7. If Zenodo archiving is enabled, archive the release and add the verified DOI
   to `CITATION.cff` and the README.

Do not describe a package version as a GitHub Release until the corresponding
tag and release page exist.
