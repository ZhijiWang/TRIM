# Using TRIM in an Article

## Software Citation

The current source version is 0.2.0. Before a formal release, cite the exact commit used together with the repository URL. `CITATION.cff` provides the repository metadata. A later GitHub Release or Zenodo DOI can supply the archival identifier.

## Suggested Method-Section Language

TRIM is implemented as a lightweight Python package accompanying the article. The package encodes the annotation schema, validates controlled fields, parses friction signatures, generates comparison tables, and exports graph representations of evidence-to-function paths. It also supports pilot-scale intercoder comparison.

Coders assign evidence, function labels, and rationale notes. The package preserves those judgements in a form that can be validated and compared. Generated `comparison_prompt` text identifies structural patterns; substantive interpretation is developed in the article.

## Cross-Language Construct Validity

For multilingual cases, the article should identify the textual layer on which each annotation was made. Source-language coding provides the basis for claims about the original passage. Glosses and translations provide access and can be assessed separately for whether they preserve, soften, introduce, or relocate the dominant friction locus.

Cross-layer differences are reported as provenance and construct-validity evidence rather than folded into the six-field TRIM signature. The companion protocol in `docs/cross_language_validity.md` records the source language, coding layer, mediation source, paired record, original and gloss loci, and the observed cross-layer relation.

Until double-layer coding has been completed, the Classical Chinese close paraphrases should be described as researcher-authored access materials. Substantive claims about the Chinese cases remain anchored in source-language reading.

## Reproducibility Statement

The repository contains the demonstration annotations, source-segment examples, codebook, coding manuals, scripts, tests, generated-output paths, blinded-pilot materials, and a cross-language validity companion template.

Run the main workflow with:

```bash
python -m pytest
python examples/demo_trim_workflow.py
```

Run the source-segment workflow with:

```bash
python examples/run_trim_with_source_segments.py
```

`trim validate` writes its CSV report before returning. Errors produce a non-zero status; warnings-only reports return zero. `--always-zero` supports pipelines that manage status separately.

## Present Claim Scale

The ten-case demonstration establishes schema expressivity, workflow traceability, and comparative payoff. The blinded packet establishes pilot readiness. Independent coding will evaluate field-level agreement and the replication of the three pre-specified comparative patterns. Double-layer coding can separately evaluate whether linguistic mediation preserves the assigned friction locus. Larger out-of-sample work will test stability across a wider corpus.
