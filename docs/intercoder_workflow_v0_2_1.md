# Intercoder Workflow v0.2.1

## Purpose

The v0.2.1 workflow compares independently completed annotations while keeping
raw coder submissions locked. Adjudication categories describe disagreement;
they do not overwrite raw agreement.

## Preservation

Before comparison, archive:

- completed coding sheets;
- completed question logs;
- language-access forms;
- source packet and manifest checksums;
- validation reports.

Use anonymous role labels in public reporting: Coder A, Coder B, and
Adjudicator 1.

## Validation

Run validation on each completed coding sheet. v0.2.1 validation checks:

- required fields;
- closed function labels, including `no_fit`;
- controlled signature values;
- primary evidence segment limit of one to three IDs;
- duplicate and overlapping primary/context segments;
- unknown segment IDs when a case manifest is supplied;
- shared-context permissions;
- complete `alternative_signature`;
- warning when a complete alternative is paired with low uncertainty.

Question logs are validated separately for definitional, interpretive,
procedural, and packet-level questions.

## Agreement Views

Report each view separately.

Categorical fields:

- exact agreement;
- pairwise percent agreement;
- Cohen's kappa only as a descriptive statistic when conditions permit.

Compound fields:

- exact raw string agreement;
- exact set agreement;
- primary-value agreement;
- compatible single-versus-compound agreement;
- any-overlap agreement;
- Jaccard overlap.

Evidence fields:

- exact primary-segment set agreement;
- primary-segment overlap and Jaccard;
- context-segment overlap;
- cross-role overlap, where one coder marks a segment primary and another marks
  it contextual.

Metadata strata:

- language-access mode;
- local versus shared-context case scope.

## Disagreement Categories

Raw disagreement remains raw. Add a separate category column only after human
review:

- `compatible_difference`;
- `codebook_ambiguity`;
- `substantive_pathway_variation`;
- `insufficient_evidence`;
- `coder_error`;
- `unresolved_legitimate_alternatives`;
- `near_complete_alignment`.

Do not collapse all disagreement into one score. A compatible single-versus-
compound difference, a retained substantive pathway variation, and a likely
coder error have different methodological meanings.

## Adjudication

For every disagreement, record:

- the first field where divergence appears;
- each coder's pathway;
- the evidence-selection relation;
- whether the difference is raw, compatible, ambiguous, substantive variation,
  insufficient evidence, coder error, or unresolved;
- whether manual, schema, packet, or analysis revision is needed.

The adjudicated value, if any, is a review result. It must not replace either
locked submission in raw agreement outputs.

## Reporting Limits

v0.2.1 remains method development and usability retesting. Report descriptive
agreement, disagreement location, and evidence of improved usability. Do not
claim validated intercoder reliability, cross-language construct validity, or
domain-general stability.

