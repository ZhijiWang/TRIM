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
are not claimed to exhaust all forms of interpretation. Agreement on these
categories would demonstrate teachability and reproducibility of the protocol,
not ontological truth.

Category lineage should be mapped to relevant traditions where defensible,
including argumentation theory, narratology, hermeneutics, discourse analysis,
and warrant analysis. Inherited distinctions and TRIM-specific operational
extensions must be separated. Where lineage is ambiguous, the protocol records
the ambiguity instead of inventing certainty.

The provisional lineage table is maintained at
`docs/studies/friction_locus_lineage_table.csv`.

## Sample design

The study uses a two-layer sample totaling 20-30 cases. Cases are not selected
to force every category to appear. Natural prevalence must be preserved, and
zero-frequency categories must be reported as not observed rather than filled by
constructed positive examples.

### Layer 1: held-out same-domain cases

Target: 12-18 cases.

Cases must:

- not appear in the released In a Grove walkthrough;
- not be used as demonstration examples in the manual;
- be similar enough to the development domain to test protocol use without a
  major domain-transfer burden;
- include interpretation-intensive evidence-to-label decisions;
- be short enough for independent coding from a frozen packet.

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
- The case requires confidential, participant, or restricted-source data.
- The case cannot be represented with a frozen source packet.
- The case requires secondary scholarship to understand the coding task.
- The case's expected label is obvious from metadata that cannot be removed.
- The case is selected only to manufacture category support.

## Annotation unit

One case is one bounded interpretive episode or passage packet with a stable
case ID, source citation, segment IDs, and visible coding instructions. The
coder sees the frozen case packet only: source text, permitted translation or
gloss, segment IDs, contextual passages if pre-specified, and the manual
version assigned to that condition.

Contextual passages may be included only when they are frozen before coding and
identified as context rather than primary evidence. Secondary scholarship is
excluded from the coder packet unless a later protocol explicitly studies
scholarly-context effects. If translation is used, the source text remains
canonical where the coder has language access; glosses or translations are
marked non-authoritative unless the study design names them as the working text.

Case order is randomized within layer and condition unless a blocking variable
requires stratification. Metadata likely to reveal expected labels, prior demo
status, or researcher hypotheses is removed or neutralized before coding. Each
case requires a frozen source packet before any human or AI coding begins.

## Human coding protocol

1. The human coder receives a frozen case packet and a specified manual version
   or instruction condition.
2. The human coder completes all records before any AI output is inspected.
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

If a human coder later reviews AI output, that exposure is recorded in a
separate exposure or adjudication layer. The original pre-exposure record
remains unchanged.

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

For each case, run 3-5 additional independent model runs under the stability
condition. Preserve all runs. Do not substitute a majority vote for the primary
run. A modal label may be reported only as a secondary summary. Calculate
self-consistency rate and label entropy, and preserve the full distribution of
outputs.

The repeated stability runs answer a different question: how stable are model
annotations under repeated execution with the same frozen materials?

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

## Mandatory structured AI output

AI output must be machine-readable and must conform to
`schemas/human_llm_coder_output.schema.json`. Required fields include:

- `case_id`
- `run_id`
- `provider`
- `model`
- `model_version_if_known`
- `timestamp`
- `prompt_version`
- `instruction_condition`
- `selected_evidence`
- `primary_label`
- `friction_locus_proposed`
- `friction_locus_operational_status`
- `rationale_mechanism`
- `uncertainty`
- `alternative_pathways`
- `counterfactual_tests`
- `decision_path`
- `escalation_required`
- `escalation_reason`
- `free_text_rationale`
- `parse_status`
- `raw_output_hash`

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
reveals expected labels. Stop before model execution if human records are not
locked, prompts are adaptive, provider metadata cannot be recorded, or output
preservation cannot be guaranteed. Stop before analysis if parsing is
substantively rewriting records, locked records have changed, or comparison
rules were not pre-specified.

## Deliverables for implementation

This branch supplies only the protocol, analysis plan, provisional lineage
table, predicted-confusion table, JSON schema, and blank templates. A later task
must independently audit the protocol, freeze the sample, freeze prompt and
manual versions, and complete human coding before any AI execution.
