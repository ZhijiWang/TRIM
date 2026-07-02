# In a Grove Japanese-Canonical TRIM-HAA Walkthrough v0.2
## Summary

This draft describes a provenance-aware technical walkthrough demonstrating structured comparison between locked human and model annotations. The artifact is a representability demonstration, a descriptive locked-record comparison, and a provenance-preserving technical walkthrough.

It is not empirical validation, not a truth verdict, not a replication study, and not a general claim about model behaviour. No claim is made that the earlier certainty-alternative mismatch was reproduced.

## Included artifacts

- frozen Japanese canonical source packet
- non-authoritative English gloss
- locked author record
- frozen AI prompt
- preserved raw AI output
- locked AI record
- model-run metadata
- frozen descriptive comparison
- claim-boundary documentation
- checksum manifests

## Main descriptive result

- final labels differ
- evidence overlap is partial
- author uncertainty is high
- AI uncertainty is medium
- both preserve alternatives
- both retain substantially the same two pathways with different prioritisation
- the descriptive primary-alternative inversion is not equivalent to the earlier certainty-alternative mismatch
- the earlier mismatch is not reproduced in this v0.2 run
- the v0.2 AI record preserves an alternative pathway and records medium uncertainty

## What is not claimed

- no interpretation is declared correct
- no annotator is treated as a gold standard
- no truth verdict is assigned
- no causal claim is made about language, segmentation, prompt, model configuration, or run instance
- no sensitivity claim is established
- no replication claim is made
- no empirical validation of TRIM-HAA is claimed
- no generalisation is made to other texts, languages, models, or annotators

## Provenance and reproducibility

The author record was created and locked before the AI run. The author record was not exposed during the AI run. The AI prompt was frozen before execution, the AI was executed exactly once, and the raw output was preserved before parsing. Both records were locked before comparison. No adjudication, post-exposure human revision, or position-note update is included in this release draft.

## Validation

Validation for the closing pass should include Python 3.11 tests, Python 3.12 tests, build, CLI smoke, lock verification, checksum verification, and GitHub Actions. The PR remains draft until release scope and stacked dependency status are resolved or clearly disclosed.

## Citation and versioning

Recommended citation status: working technical artifact, not empirical validation.

Suggested version: `v0.2.0-public-walkthrough`.

Suggested tag: `in-a-grove-public-v0.2.0`.

No external release, archive, or DOI is claimed by this draft. Any post-release changes require a new version and new checksums.
