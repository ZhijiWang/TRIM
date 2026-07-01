# TRIM-HAA construct definitions

## Independent convergence

A human-pre record and an AI-independent record match on a specified field before any AI output was shown to the human.

## Exposure-associated convergence

The human-post record becomes more similar to the AI record than the human-pre record was.

Use exposure-associated, not exposure-caused, in prototype reports.

## Label adoption

The human post-AI label changes to match the exposed AI label.

## Evidence adoption

TRIM-HAA separates evidence incorporation from evidence convergence.

`ai_evidence_incorporated`: the human post-AI primary evidence contains at least one AI-selected segment that was absent from human-pre.

`evidence_convergence_increased`: Jaccard(post, AI) is greater than Jaccard(pre, AI).

## Evidential displacement

One or more pre-AI primary segments are removed and replaced by AI-selected segments in the post-AI record.

Displacement is not assumed to be harmful.

## Mechanism adoption

The human post-AI rationale mechanism changes to the AI mechanism.

## Uncertainty shift

The human uncertainty flag changes after AI exposure. Lower uncertainty is not treated as improvement.

## Alternative suppression

An alternative present in human-pre is absent in human-post.

## Alternative generation

No alternative was present in human-pre, but one is present in human-post.

## Alternative modification

An alternative remains present in both pre and post, but its mechanism or note changes. If the post alternative mechanism matches the AI alternative mechanism while the pre mechanism differed, the report records `alternative_mechanism_adopted_from_ai`.

## Rationale convergence

The submitted human post-AI rationale becomes lexically closer to the submitted AI rationale. Lexical similarity is not evidence of internal belief adoption.
