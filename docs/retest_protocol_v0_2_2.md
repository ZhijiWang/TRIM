# Retest Protocol v0.2.2

## Purpose

The v0.2.2 retest evaluates whether revisions based on the completed v0.2.0
usability pilot and a v0.2.1 machine-executed protocol dry run improve coder
usability, evidence discrimination, boundary calibration, and question logging
before human external-coder deployment.

The retest is prospective. The original ten formal cases are not recoded and
are not reused as the retest corpus.

## Corpus

The retest contains 12 new cases drawn from legally reusable public-domain or
public-domain-translated materials. The sample deliberately mixes source
families so that function labels cannot be inferred from corpus type alone.

The design stresses:

- analyst-level function versus actor-level actionability;
- authorization versus stabilization;
- authorization versus extended deliberation;
- explicit interpretive operation versus implicit context inference;
- warrant attribution versus warrant relation;
- confession or testimony as act versus standpoint-dependent self-presentation;
- reported speech versus frame narrative;
- local case versus shared narrative context;
- primary evidence versus contextual segments;
- low versus medium uncertainty;
- `no_fit`;
- legitimate alternative signatures;
- cases where not all supplied segments should be primary evidence.

The coder-facing packet does not provide expected labels.

## Materials

Coder-facing:

- `docs/TRIM_codebook_v0_2_2.md`
- `docs/TRIM_Coding_Manual_v0_2_2_friction_locus.md`
- `docs/TRIM_Coding_Manual_v0_2_2_rationale_mechanism.md`
- `docs/discourse_level_guide_v0_2_2.md`
- `docs/retest_v0_2_2_coder_guide.md`
- `data/retest_v0_2_2_case_manifest.csv`
- `data/retest_v0_2_2_shared_context_registry.csv`
- `data/retest_v0_2_2_source_packet.md`
- `data/retest_v0_2_2_source_text_provenance.csv`
- `data/retest_v0_2_2_coding_template.csv`
- `data/retest_v0_2_2_question_log_template.csv`
- `data/retest_v0_2_2_practice_cases.md`
- `data/retest_v0_2_2_language_access_form.csv`

Research-only materials, pilot results, adjudication, tests, comparison
reports, article notes, and expected labels are excluded from the coder-facing
ZIP. The researcher-facing design manifest is
`data/retest_v0_2_2_research_manifest.csv`; it is not part of the coder package.

## Procedure

1. Complete the language-access form.
2. Read the codebook, manuals, discourse guide, and coder guide.
3. Complete the practice cases.
4. Code the 12 formal retest cases independently.
5. Record every definitional, interpretive, procedural, or packet-level question
   in the question log when the question arises.
6. Lock the coding sheet, question log, and language-access form.
7. Validate the locked files.
8. Generate raw comparison outputs.
9. Conduct adjudication without overwriting locked coder values.

## Language Conditions

For each coder and case, record whether the coding was based on direct
original-language access, a published translation, project-authored close
support, summary-mediated access, or mixed access.

If coders cannot directly read a source language, report the retest as
translation-mediated for those cases and interpret agreement accordingly.

## Shared Context

The manifest states each case's permitted scope. Coders may use only the local
passage, multi-passage single case, complete work, supplied related cases, or
shared narrative field named in the manifest. Cross-case context is not assumed.

`multi_passage_single_case` is used when one formal case contains separated
passages from the same work and no other formal case is used as cross-case
context. It must not use `shared_context_ids`, and
`cross_case_context_permitted` must be `no`.

The shared-context registry is the authoritative map from `shared_context_ids`
to member cases and permitted cross-case segments. Validation fails if a
manifest names an unknown shared-context ID, if a registry member case or
permitted segment does not exist, if a required context segment is outside the
declared group, or if a local-passage case supplies cross-case required context.

All formal coding must be possible from the supplied source packet. Formal
segments supply actual source text or the documented public-domain translation
text. External URLs in the manifest are provenance references and are not
required for coding.

## Metadata Separation

Coder-facing metadata uses neutral bibliographic and structural descriptors.
Research-only analytic categories are retained only in the researcher-facing
manifest for later design analysis. Coder-facing `case_type` values must not
duplicate or approximate controlled TRIM function, locus, discourse-level,
rationale-mechanism, or epistemic-support values.

`cue_family` and `broad_function_family` are researcher-facing descriptive
metadata only. They are not coder-generated v0.2.2 fields, are not required for
coder submission, and are not included in v0.2.2 agreement calculations.

## Question-Log Timing

Questions should be logged when they arise during coding, not reconstructed in a
batch after all cases are complete. Self-resolved questions must still be logged.
Timestamps should reflect when the issue arose. If exact timing is unavailable,
mark the timestamp as approximate rather than fabricating precision. Batch-created
identical timestamps should be disclosed as a protocol deviation.

## Package Audit

The package builder performs explicit leakage checks and a separate
semantic-steering scan. Instructional files may contain controlled vocabulary.
Case-specific files are scanned for controlled values, prohibited analytic
descriptors, original pilot case IDs, and answer-bearing phrases. Verified
source-text quotation matches are reported separately from project-authored
metadata or navigation prose. Unreviewed high-risk project-authored matches fail
package generation.

## Analysis

Report:

- schema validity;
- question-log use;
- exact agreement;
- compatible single-versus-compound agreement;
- evidence-segment exact and overlap metrics;
- disagreement categories;
- language-access strata;
- local versus shared-context strata;
- retained substantive pathway variation.

Do not use adjudicated outcomes to overwrite raw agreement.

## Decision Rule For Next Empirical Step

Proceed to a larger reliability design only if the v0.2.2 retest shows complete
records, discriminative evidence selection, meaningful question logging,
stable handling of revised boundary pairs, and no new systematic leakage or
scope ambiguity.
