# Alpha Release Procedure

Status: documentation for the `0.3.0a1` alpha line. This procedure does not
publish a package, create a GitHub release, or authorize any study activity.

## Artifact classes

The repository has four distinct release surfaces:

1. **Git repository.** The tracked development and research tree, including
   materials that are not approved for unrestricted redistribution as a
   standalone bundle.
2. **GitHub source snapshots.** GitHub-generated ZIP and tar archives reproduce
   the tracked tree at a tag or commit. A manual release manifest cannot remove
   files from those automatic snapshots.
3. **Python wheel and sdist.** Core `trim_haa` software distributions. They
   exclude study modules, study data, prompts, source packets, examples,
   research bundles, and study execution code. The sdist contains only its
   self-contained core distribution tests.
4. **Manually assembled research-software bundles.** Deliberately selected
   public files accompanied by a manifest and checksums. These bundles must be
   built from an exact clean commit and must follow the exclusions below.

## Required exclusion

Until a separate rights review resolves the English translation status, every
manually assembled public alpha bundle must exclude:

```text
examples/in_a_grove_walkthrough/
```

The directory remains tracked in this PR and is neither modified nor deleted.
Consequently, a full clone or automatically generated GitHub source snapshot
still contains it. The directory's future active-tree status requires a
separate, rights-focused decision.

The tagged `examples/in_a_grove_walkthrough_public_v0_2/` demonstration is a
different Japanese-canonical artifact and remains frozen and unchanged.

## Core Python distribution policy

- Build from a clean checkout of the intended commit.
- Keep package version `0.3.0a1` until a separately reviewed version change.
- Verify wheel and sdist contents before publication.
- Verify that `trim_haa.llm`, `trim_haa.human_coding`, prompts, source packets,
  study data, study schemas, study scripts, examples, research directories, and
  artifact ZIPs are absent.
- Extract the sdist, install it in an isolated environment, and run every test
  included in that sdist.
- Include `LICENSE`, `CITATION.cff`, `CHANGELOG.md`, `SECURITY.md`,
  `THIRD_PARTY_AND_CONTENT_RIGHTS.md`, the README, and packaging metadata.

## Manual bundle policy

A manual bundle needs an explicit allowlist, exact source commit, file hashes,
creation procedure, content-rights review, and a statement of research claim
boundaries. It must not use broad filesystem globs or include untracked working
files.

## Required checks

Before an alpha release candidate is approved:

- run the full Python 3.11 and 3.12 repository suites;
- build and inspect wheel and sdist;
- run the extracted-sdist tests;
- run package import and CLI smoke tests;
- verify frozen artifact checksums;
- run all blocked-study validators and dry-runs;
- validate repository-relative documentation links;
- confirm `git diff --check` passes;
- record the exact commit and final CI state.

No successful build or test changes provider, runtime, pricing, authorization,
human-coding, or model-execution gates.
