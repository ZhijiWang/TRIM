# Human-LLM Friction-Locus Demonstration Study Protocol

Status: protocol only. No empirical coding has been performed. No model has
been run for this study. The released In a Grove public walkthrough, release
tag, locked records, and frozen comparison package are out of scope and must not
be modified by this protocol.

## Primary research question

What becomes visible when interpretive disagreement is represented
procedurally rather than only as label divergence?

## Secondary research questions

1. At which procedural loci do human-LLM disagreements occur?
2. Do observed disagreements concentrate in the manual's predicted confusable
   category pairs?
3. Can identical final labels conceal different evidence selections, warrants,
   counterfactual judgments, uncertainty levels, or alternative pathways?
4. Does the full manual alter model outputs compared with lighter instruction
   conditions?
5. How stable are model annotations across repeated runs?

## Study positioning

This demonstration positions TRIM as a teachable and auditable
disagreement-registration protocol for small-N, interpretation-intensive cases.
It asks whether the protocol is usable, discriminating, procedurally
informative, and capable of revealing disagreement structures hidden by
final-label agreement.

The study does not position TRIM as an exhaustive ontology of interpretation, a
universal annotation solution, empirical validation of the whole framework, or
proof that disagreement objectively exists in exactly eight natural categories.
It also does not claim that the released In a Grove walkthrough supplies an
empirical finding; that release remains a frozen technical walkthrough and
working method artifact.

## Literature positioning

This literature positioning is provisional until every cited source is
independently verified. It avoids publication metadata and does not expand the
literature review for length.

Hermeneutic and non-dogmatic annotation work, including Gius and Jacke and
CATMA-related annotation traditions, has emphasized that literary annotation is
not merely the recovery of one stable answer. Such work makes interpretive
plurality, annotation rationale, and the difficulty of reliability in
interpretation-intensive tasks visible. TRIM shares this interest in auditable
interpretive operations, while narrowing the present protocol to a small set of
procedural decision points that can be recorded, locked, and compared.

Perspectivist NLP and disagreement-aware annotation approaches treat
disagreement as signal rather than only noise, often preserving label
distributions, annotator perspectives, or uncertainty over labels. TRIM's
narrower distinction is not that perspectivist work never analyzes rationales
or annotator profiles. Rather, perspectivist approaches preserve or model
disagreement distributions; TRIM attempts to localize disagreement within an
explicit interpretive procedure, including evidence selection, counterfactual
judgments, decision rules, uncertainty, and alternative pathways.

LLM-as-annotator research has often concentrated on larger-scale tasks,
including social-media-scale classification, where reliability, contamination,
prompt sensitivity, and accountability are central concerns. Less work directly
tests canonical or interpretation-intensive texts where evidence boundaries,
warrants, narrative perspective, and alternative interpretive pathways are
themselves part of the task. This protocol treats LLM output as an auditable
annotation record, not as an answer key, a truth verdict, or a substitute for
human interpretation.

## Provisional audit vocabulary, not exhaustive ontology

The `friction_locus` categories are a provisional audit vocabulary. They are
derived from recurring interpretive decision points in prior TRIM work, but they
are not claimed to exhaust all forms of interpretation. Agreement in this study
may show that the frozen protocol can produce comparable records under the
specific researcher-model conditions studied. It does not establish
reproducibility across independent human analysts or ontological truth.

Category lineage should be mapped to relevant traditions where defensible,
including argumentation theory, narratology, hermeneutics, discourse analysis,
and warrant analysis. Inherited distinctions and TRIM-specific operational
extensions must be separated. Where lineage is ambiguous, the protocol records
the ambiguity instead of inventing certainty.

The provisional lineage table is maintained at
`docs/studies/friction_locus_lineage_table.csv`.

## Human-comparison design

Design adopted: Design B, single-researcher human-model procedural comparison.

Reason: recruiting or evaluating an external second human coder may require
institutional human-research ethics and governance arrangements that are not
currently available. The study therefore does not recruit another coder, does
not create participant-facing materials, and does not estimate human intercoder
reliability.

Human record:

- one researcher creates one pre-exposure human record for every case;
- all human records are completed before any AI output is inspected;
- human records are locked and hashed;
- no post-exposure revision is allowed;
- any later reflection or adjudication is stored separately and never overwrites
  the original;
- the human record is not a gold standard;
- the human record represents one documented interpretive position under a
  frozen protocol.

Model records:

- one primary locked model run per case;
- additional isolated model runs for stability;
- no human record exposure;
- no adaptive prompting;
- all raw outputs preserved;
- no majority-vote replacement of the primary run.

Comparison estimates correspondence and procedural divergence between two
different record-producing conditions: researcher-produced pre-exposure records
and independently generated model records. It does not estimate reproducibility
among human coders.

Prominent limitation: because the study contains one researcher-produced human
record per case, it cannot determine whether another human analyst would apply
the protocol similarly. All findings concern the relation between one documented
human interpretive position and model records under frozen conditions. This is a
deliberate scope boundary, not hidden missing data.

The study addresses procedural visibility in human-model comparison. It does
not establish whether TRIM is reproducible across independent human analysts.

## Ethics and governance boundary

- no external human coder will be recruited in this study;
- no participant-facing recruitment, consent, compensation, interview, survey,
  or performance evaluation will occur;
- the researcher's own analytic records are treated as research outputs;
- textual cases must be public-domain, openly licensed, or otherwise lawfully
  used;
- no private or participant data will be processed;
- no claim of formal ethics exemption will be made without written
  institutional confirmation;
- any future addition of a second human coder would constitute a separate
  protocol change requiring institutional ethics/governance advice before
  recruitment or coding;
- a second human coder cannot be added retrospectively to the frozen study
  without a new protocol version.

Protocol status fields:

- `institutional_status = not_yet_formally_determined`
- `external_human_recruitment = prohibited_under_current_protocol`

## Sample design

The study uses a two-layer sample totaling 20-30 cases. Cases are not selected
to force every category to appear. Natural prevalence must be preserved, and
zero-frequency categories must be reported as not observed rather than filled by
constructed positive examples.

Sampling must follow an auditable selection workflow:

1. Define the source universe for each layer.
2. Create a candidate pool with stable candidate IDs.
3. Screen eligibility before final selection.
4. Record the case selector, selector's prior knowledge, and whether labels or
   expected friction loci were visible during selection.
5. Record inclusion and exclusion decisions with reason codes.
6. Freeze the final sample manifest before any coding.
7. Record the final sample-freeze timestamp and sample manifest hash.

The protocol-only selection-log template is
`docs/studies/human_llm_sample_selection_log.csv`. It must remain empty of
actual cases until a later sample-selection task.

A source universe must be bounded before individual case selection by one or
more named works, a named anthology, a fixed edition, a frozen scene or passage
list, or another enumerated corpus boundary. The boundary is recorded before
candidate screening begins, and later expansion requires a new universe record
and rationale.

Exclusion-reason codes:

- `released_walkthrough_case`
- `manual_demo_case`
- `insufficient_source_provenance`
- `rights_or_access_unclear`
- `requires_secondary_scholarship`
- `span_not_freezable`
- `metadata_reveals_expected_label`
- `selected_to_force_category`
- `confidential_or_participant_data`
- `outside_layer_definition`
- `other_documented_reason`

Each candidate also records `manual_development_influence` with one of these
values:

- `none_known`
- `indirect`
- `direct`
- `uncertain`

Cases with direct influence on friction-locus definitions, counterfactual tests,
or predicted-confusion examples are excluded from the held-out same-domain layer.

### Layer 1: held-out same-domain cases

Target: 12-18 cases.

Same-domain means cases drawn from interpretation-intensive literary or
narrative texts where the coding task turns on evidence selection, warranting,
perspective, temporal framing, boundary-setting, context inference, uncertainty,
or alternative interpretive pathways. Each case must contain an identifiable
evidence-to-function or evidence-to-label decision, permit at least one explicit
rationale and, where relevant, an alternative pathway, and be analyzable without
unrestricted external scholarship. Held-out means excluded from manual/demo
development and from the released public walkthrough; it does not mean unknown
to the model or absent from its possible training data.

Cases must:

- not appear in the released In a Grove walkthrough;
- not be used as demonstration examples in the manual;
- be similar enough to the development domain to test protocol use without a
  major domain-transfer burden;
- include interpretation-intensive evidence-to-label decisions;
- be short enough for independent coding from a frozen packet.

Provisional case-length rule: the preferred canonical-text span is
approximately 100-600 words in English-equivalent length. Word equivalence is
not exact across languages. Shorter spans are allowed when the interpretive unit
is self-contained. Longer spans are allowed only when the frozen context-window
rule requires them, and each exception must be documented in the source
manifest.

### Layer 2: transfer cases

Target: 8-12 cases.

Transfer cases may include selected Zuo zhuan cases or another
interpretation-intensive domain/tradition. If Zuo zhuan cases are used, the
researcher's prior familiarity means they are not fully uncontaminated. They
must be described as a transfer or external-application set, not as pure
out-of-sample validation. Domain, language, and prior-analysis effects must be
reported.

### Inclusion criteria

- The case has a bounded source passage that can be frozen before coding.
- The passage supports at least one plausible interpretive decision under the
  current manual.
- Primary evidence can be segmented into stable IDs.
- The case can be coded without secondary scholarship.
- Rights and source-provenance notes can be documented.
- The case is not selected because it is known to instantiate a desired
  category.

### Exclusion criteria

- The case appeared in the released public walkthrough.
- The case is a manual demonstration example.
- The case directly shaped friction-locus definitions, counterfactual tests, or
  predicted-confusion examples.
- The case requires confidential, private, participant, or restricted-source data.
- The case cannot be represented with a frozen source packet.
- The case requires secondary scholarship to understand the coding task.
- The case's expected label is obvious from metadata that cannot be removed.
- The case is selected only to manufacture category support.

## Annotation unit

One case is one bounded interpretive episode or passage packet with a stable
case ID, source citation, segment IDs, and visible coding instructions. The
researcher analyst and model see the frozen case packet only: source text,
permitted translation or gloss, segment IDs, contextual passages if
pre-specified, and the manual version assigned to that condition.

Contextual passages may be included only when they are frozen before coding and
identified as context rather than primary evidence. Secondary scholarship is
excluded from the coder packet unless a later protocol explicitly studies
scholarly-context effects. If translation is used, the source text remains
canonical where the coder has language access; glosses or translations are
marked non-authoritative unless the study design names them as the working text.

The default context window is one focal passage plus one immediately preceding
and one immediately following structural unit where available. A structural unit
may be a paragraph, scene, testimony block, stanza, entry, or other
source-appropriate unit defined before coding. Researcher and model packets must
use the same context window for direct correspondence estimates. No
case-specific expansion is allowed after coding begins. Any extended context is
frozen before coding and listed in the source manifest.

Case order is randomized within layer and condition unless a blocking variable
requires stratification. Metadata likely to reveal expected labels, prior demo
status, or researcher hypotheses is removed or neutralized before coding. Each
case requires a frozen source packet before any human or AI coding begins.

## Source, translation, and context controls

Every frozen packet must state:

- canonical-language source status;
- translation or gloss status;
- whether a translation or gloss is authoritative or non-authoritative;
- whether the model sees source text, translation/gloss, or both;
- whether human and model coders see identical text layers;
- context-window boundaries;
- secondary scholarship exclusion;
- paratext removal;
- proper-name and metadata masking where needed;
- version or edition citation;
- source rights status.

If different language-access conditions are used, they are separate
experimental conditions or are excluded from direct agreement estimates.
Language effects must not be conflated with human-model record-condition
effects.

Direct human-model correspondence estimates are computed only for records
created from identical text layers. Model-training familiarity cannot be
verified; canonical-text familiarity is recorded as a limitation, not treated as
evidence that a case is uncontaminated. Researcher familiarity is recorded as
prior close analysis, prior publication use, prior annotation, casual
familiarity, or no known prior analysis. Prior familiarity does not
automatically exclude transfer cases, but it must be reported.

Each candidate requires source citation, edition or version, rights status,
public-domain, open-license, or lawful-use basis, source retrieval date, source
file or URL reference, source text hash, and translation or gloss provenance
where used.

## Human coding protocol

1. The researcher analyst receives a frozen case packet and a specified manual
   version or instruction condition.
2. The researcher analyst completes all records before any AI output is
   inspected.
3. Human records are locked and hashed.
4. No post-exposure revision is allowed.
5. Any later adjudication is stored separately and never overwrites the original
   record.

Human records must include:

- evidence selected;
- primary label;
- friction_locus;
- rationale mechanism;
- uncertainty;
- alternative pathway;
- counterfactual-test answers;
- escalation status;
- free-text rationale;
- unresolved ambiguity.

If the researcher analyst later reflects on AI output after comparison, that
post-comparison analytic review is recorded in a separate reflection,
exposure, or adjudication layer. The original pre-exposure record remains
unchanged. Any future external human-coder component requires a separate
protocol version and governance review before recruitment or coding.

## AI coding design

The study separates primary analysis from stability analysis.

### Primary analysis

For each case, run one pre-registered locked model run. Record exact model,
provider, date, prompt, parameters, and retry status. Human records are not
exposed. Prompting is non-adaptive. No retry is allowed unless there is a
technical failure: no response returned, connection failure, provider execution
failure, or no output bytes produced. Preserve the raw output before parsing.

The single locked run answers the question: what does the pre-registered model
run produce under the specified instruction condition?

### Stability analysis

For this freeze package, the planned stability interpretation is three
additional independent model runs under the stability condition for each case,
beyond the primary locked run. The primary run is not counted as a stability
run. Preserve all runs. Do not substitute a majority vote for the primary run. A
modal label may be reported only as a secondary summary. Calculate
self-consistency rate and label entropy, and preserve the full distribution of
outputs.

The repeated stability runs answer a different question: how stable are model
annotations under repeated execution with the same frozen materials?

### Model-run independence and reproducibility controls

Each model run must record exact decoding parameters, temperature, top_p if
available, seed if supported, tool availability, browsing availability, system
prompt or its unavailability, provider-side version limitations, execution
date, region if relevant, retry policy, rate-limit failure handling, technical
failure definition, and independence of repeated runs.

Repeated stability runs must be conducted in isolated sessions. No conversation
state, prior output, human record, or cross-run summary may be visible. API and
model stochasticity and provider-side updates limit exact reproducibility; this
limitation must be reported with the run manifests.

## Study-local hashing rules

These rules apply only to this study protocol and do not create a new
repository-wide hashing framework. Self-referential hash fields include
`record_hash`, `allocation_hash`, `sample_manifest_hash`, `source_packet_hash`,
`prompt_hash`, and `raw_output_hash`.

Hashes are SHA-256 values computed over UTF-8 bytes with LF line endings.
Canonical JSON payloads are produced by recursively sorting object keys,
preserving array order, serializing without insignificant whitespace, encoding
as UTF-8, and excluding the target hash field from the object before
serialization. CSV and text payloads use their exact frozen UTF-8 bytes after LF
normalization. No timestamp or metadata may be added after hashing; any
post-hash modification invalidates the hash. The canonicalization procedure
version must be recorded with the manifest or record that uses the hash.

Each model run manifest contains or references `system_prompt_hash`,
`user_prompt_template_hash`, `condition_prompt_hash`, `source_packet_hash`,
`output_schema_hash`, `manual_version`, `manual_file_hash`, and
`prompt_bundle_version`. Prompt hashes are computed before model execution. Raw
model output is hashed immediately after receipt and before parsing. Parsed
model records are hashed separately from raw output. Technical failures remain
recorded and are not silently overwritten. A retry caused by technical failure
receives a new `run_id` and its own manifest entry.

## Manual freeze requirements

Before empirical coding, one exact manual file path and one exact commit SHA
must be designated. The manual file SHA-256 must be recorded. Category
definitions, counterfactual tests, confusable-with relations, and
reserved/review-required category rules must be frozen. The
`docs/studies/predicted_confusions.csv` table must be checked against that exact
manual version.

No manual wording may change after researcher coding begins. Any later revision
requires a new protocol/manual version and cannot overwrite original records.
An exact commit/file reference is preferred over duplicating the manual unless
duplication is required for archival clarity. This PR does not freeze the manual.

## Prompt freeze requirements

Before model execution, instruction conditions A, B, and C must each have an
exact system prompt, exact user prompt template, exact source-packet insertion
rule, exact output-schema instruction, exact model/provider, exact decoding
parameters, browsing/tool status, session-isolation rule, retry policy,
technical-failure policy, prompt version ID, prompt hashes, and execution-order
or counterbalancing rule.

Prompts are not frozen in PR #17. Final prompt text belongs to a later prompt
freeze task.

## Instruction-ablation design

Use at least three conditions on a subset of cases:

- A. label names and short definitions only;
- B. concise decision rules;
- C. full manual including counterfactual tests and confusable-with guidance.

The purpose is to test whether richer procedural guidance produces observable
changes in evidence selection, counterfactual adherence, friction_locus
assignment, uncertainty, alternative-pathway retention, and rationale
structure.

This ablation does not detect training-data contamination. Similar outputs
across conditions may reflect robust task structure, model priors, insensitive
instructions, contamination, or ceiling/floor effects. Those explanations must
not be collapsed into a single causal claim without an additional design.

For the small-N pilot, the allocation design is: all selected ablation cases
receive all three conditions in separate independent sessions, unless a
pre-freeze cost ceiling makes this infeasible. If infeasible, the protocol must
be amended to a preregistered balanced incomplete design before execution.

Ablation independence requirements:

- separate stateless session for every case-condition-run;
- no conversation reuse;
- no output from another condition visible;
- identical case packet across conditions;
- identical task framing except the intended instruction difference;
- fixed model and parameters across conditions;
- frozen prompt for each condition;
- frozen execution order or randomized/counterbalanced order;
- no adaptive prompting;
- no retries except documented technical failure;
- raw output preserved before parsing.

## Allocation and randomization plan

Allocation is frozen before coding in
`templates/human_llm_allocation_manifest.json` and the later filled manifest.
The allocation plan records case order randomization, human record completion order, condition allocation, ablation subset selection, model stability run count, random seed, stratification, and prohibited reallocations.

Random seed generation must be documented before allocation. Stratification is
permitted only when preregistered for layer, language, source tradition, or
case-length balance. Post hoc reallocations are prohibited except for documented
administrative failure before any coder sees the affected case; any such change
requires a new allocation manifest and hash.

## Mandatory structured AI output

AI output must be machine-readable and must conform to the model-specific
record in `schemas/human_llm_coder_output.schema.json`. Human records conform
to the human-specific record. Shared procedural fields include:

- `case_id`
- `record_id`
- `timestamp`
- `manual_version`
- `selected_evidence`
- `primary_label`
- `friction_locus_proposed`
- `friction_locus_operational_status`
- `final_operational_label`
- `rationale_mechanism`
- `uncertainty`
- `alternative_pathways`
- `counterfactual_tests`
- `decision_path`
- `escalation_required`
- `escalation_reason`
- `free_text_rationale`
- `unresolved_ambiguity`
- `record_hash`

Human-specific fields include `analyst_id_pseudonym`, `analyst_role`,
`self_record_status`, `exposure_status`, `coding_session_id`, and
`source_packet_hash`. Human records must not require provider, model, model
version, prompt version, or raw model output hash. They must not describe the
researcher as a participant, recruited coder, or study subject.

Model-specific fields include `run_id`, `provider`, `model`,
`model_version_if_known`, `prompt_version`, `instruction_condition`,
`source_packet_hash`, `raw_output_hash`, `parse_status`, `retry_count`, and
`technical_failure_status`. API keys, account identifiers, and secret
credentials must never be stored.

For every relevant confusable pair, `counterfactual_tests` must record:

- `test_id`
- `question`
- `answer`
- `cited_evidence`
- `effect_on_decision`
- `confidence`

## Reserved-category escalation

Reserved or review-required categories do not prevent the model from expressing
its proposed interpretation. The model must use:

- `friction_locus_proposed`
- `friction_locus_operational_status = requires_human_review`
- `final_operational_label = unresolved`

The AI must not autonomously convert a review-required category into a final
approved label.

Escalation is required when:

- the proposed category is reserved by the manual;
- the manual states that project-lead or human review is required;
- the output proposes a category outside the controlled vocabulary;
- the output cites evidence IDs not present in the frozen packet;
- counterfactual tests do not resolve the category assignment;
- the model's procedural route conflicts with a governance rule;
- parse repair would require substantive rewriting.

Escalation records are outcomes, not failures. They identify cases where the
procedure requires human governance before a final operational label is used.

## Disagreement decomposition

Disagreement is recorded at eight levels:

1. Evidence-selection disagreement: records select different source segments or
   assign them different primary/contextual roles.
2. Counterfactual-answer disagreement: records answer one or more required
   boundary tests differently.
3. Decision-rule disagreement: records use different rule routes to reach a
   label.
4. Friction-locus disagreement: records propose different dominant procedural
   loci.
5. Primary-label disagreement: records assign different final labels.
6. Uncertainty disagreement: records assign different uncertainty levels or
   different justifications for uncertainty.
7. Alternative-pathway disagreement: records differ in whether alternatives are
   retained, named, or treated as complete.
8. Escalation/governance disagreement: one record requires review, unresolved
   status, or governance routing while the other does not.

Two records can therefore have:

- the same final label but different procedure;
- different final labels but substantially shared interpretive structure;
- the same evidence but different warrants;
- the same counterfactual answers but different category assignment.

## Stop conditions

Stop before coding if source packets are not frozen, rights/provenance status is
unclear, the manual version is not frozen, prompts are not frozen, or metadata
reveals expected labels. Stop before sample freeze if Design B has not been formally adopted in the
protocol, institutional ethics/governance status has not been recorded, or
source rights status is unresolved. Stop before model execution if human records
are not locked, prompts are adaptive, provider metadata cannot be recorded, or
output preservation cannot be guaranteed. Stop before analysis if parsing is
substantively rewriting records, locked records have changed, or comparison
rules were not pre-specified.

## Deliverables for implementation

This branch supplies only the protocol, analysis plan, provisional lineage
table, predicted-confusion table, JSON schema, and blank templates. A later task
must independently audit the protocol, freeze the sample, freeze prompt and
manual versions, and complete human coding before any AI execution.
