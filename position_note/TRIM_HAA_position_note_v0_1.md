# Auditing Interpretive Annotation Beyond Final Labels: A TRIM-HAA Walkthrough

## Abstract

TRIM-HAA audits the provenance and evidential licensing of interpretive annotation records, and traces how human records change after exposure to model-generated annotations. It does not optimise human-AI collaboration or treat model output as an answer key.

This position note reports a narrow author-only walkthrough of the independent-record layer using a short packet from Ryunosuke Akutagawa's "In a Grove" / "Yabu no Naka". One researcher-produced analytic record and one independently generated model record are compared across selected evidence, function label, rationale mechanism, uncertainty, rationale note, alternative pathway, and provenance.

The central contribution is claim-boundary work: Final labels flatten the structure of both agreement and disagreement. TRIM-HAA preserves selected evidence, mechanism, uncertainty, alternatives, and provenance so that the structure of interpretive difference remains reviewable. In this case, the author and model records differ not only in final label but also in evidence selection, mechanism, uncertainty, and alternative handling. TRIM-HAA preserves those dimensions so that the disagreement can be inspected rather than reduced to a category mismatch.

The walkthrough directly demonstrates disagreement flattening. A final-label comparison identifies disagreement, but it does not preserve whether the disagreement arises from evidence selection, evidence-to-label mechanism, uncertainty, alternative preservation, or rationale structure. The walkthrough does not empirically demonstrate same-label hidden divergence because the author and AI records use different labels. Same-label divergence remains a general motivation, a synthetic capability already supported by the dry run, and a future empirical target.

## 1. Introduction

Interpretive annotations are increasingly produced by humans, language models, or workflows that combine both. A final label alone is rarely enough to explain what an annotation record is doing. Two records may share a label while selecting different evidence. They may select the same passage while giving it different analytic force. They may both sound confident while preserving different levels of uncertainty or different alternative readings. A dataset that records only the final category loses much of this structure.

Label-only comparison can still identify an important fact: whether two records agree or disagree at the category level. The limitation is more precise. A final-label comparison identifies disagreement but does not preserve its structure, and it identifies agreement without showing whether the records reached that agreement through the same evidence, mechanism, uncertainty posture, alternatives, or rationale.

TRIM-HAA is designed for this audit problem. It records submitted annotation pathways: selected evidence, function label, evidence-to-label mechanism, uncertainty, rationale note, alternative pathway, and provenance. Its purpose is not to optimise human-AI collaboration, rank participants, or treat model output as an answer key. Its purpose is to make an annotation record reviewable enough that agreement, disagreement, certainty, and revision can be examined field by field.

This position note offers a narrow author-only walkthrough using a short packet from "In a Grove". The walkthrough compares one researcher-produced analytic record and one independently generated AI record. The strongest result is not a certainty-alternative adjudication. The strongest result is that the author and model records differ not only in final label but also in evidence selection, mechanism, uncertainty, and alternative handling, and TRIM-HAA preserves those dimensions for inspection.

This is a conceptual and technical demonstration. It is not a human-subject study. It is not a reliability study. It is not an accuracy comparison. It is not an AI-bias experiment. It is not a causal exposure study. It does not validate TRIM-HAA.

## 2. Two Audit Layers

TRIM-HAA separates two audit layers.

The first layer is independent record audit. A human record and a model record are produced independently against the same source packet and instruction set. They can then be compared across selected evidence, function label, rationale mechanism, uncertainty, rationale note, alternative pathway, and provenance. This layer asks what each record preserved, selected, foregrounded, and left open.

The second layer is exposure audit. A human-pre record is locked before model exposure. A frozen model record may be shown. A human-post record is then collected, with a no-AI second-pass control where possible. This layer asks what changed after exposure and whether similar second-pass change also appears without AI material.

This position note demonstrates only the independent-record layer. It creates no human-post records, no participant revisions, and no no-AI control records. It therefore makes no claim about exposure-associated change.

The distinction between these two layers is important because they answer different questions. Independent record audit is about comparability: what did each record select, claim, leave uncertain, or preserve as an alternative before any exposure occurred? Exposure audit is about revision: what changes after a person sees a model record, and how should those changes be described without assuming causation too quickly? The present demonstration keeps the layers apart.

## 3. Flattening: Agreement and Disagreement

TRIM-HAA is motivated by two related forms of label flattening.

Agreement flattening occurs when two records share a final label but differ in evidence, mechanism, uncertainty, alternatives, or rationale. In that situation, a label-only table may make records look equivalent even when their submitted interpretive pathways differ. The current walkthrough does not empirically demonstrate this form because the author and AI records use different labels. Agreement flattening should therefore be treated here as a general motivation, a synthetic capability already supported by the dry run, and a future empirical target.

Disagreement flattening occurs when different final labels reveal that records disagree but do not reveal whether disagreement arises from evidence selection, evidence-to-label mechanism, uncertainty, alternative preservation, or rationale structure. The current walkthrough directly demonstrates disagreement flattening. The author and model records use different final labels, and the field comparison shows that the difference is not only categorical. They also differ in selected evidence, mechanism, uncertainty, and alternative handling.

The claim is not that label-only comparison shows nothing. A final-label comparison identifies disagreement. It does not preserve the structure of that disagreement.

A same-label/different-pathway case would directly demonstrate agreement flattening, but no such case is added here because constructing one after inspecting the current AI output would create a post hoc demonstration. A future case must be run under a pre-frozen packet, codebook, author record, and model protocol, with the result retained regardless of whether labels agree.

## 4. TRIM-HAA Representation

The walkthrough uses the lightweight TRIM-HAA Core fields:

- primary evidence: packet segment IDs selected as direct support;
- function label: the analytic category assigned to the case;
- rationale mechanism: how the selected evidence supports the label;
- uncertainty: low, medium, or high;
- rationale note: a short submitted explanation;
- alternative pathway: whether another complete interpretation remains available;
- provenance: actor, stage, source packet, prompt, model, hashes, and lock records.

The rationale note is a submitted explanation. It is not a record of private cognition, and model rationale is not treated as hidden model reasoning. The record is what can be audited.

In this walkthrough, the human-side record is explicitly a researcher-produced analytic demonstration; not human-subject data and not a gold standard. It is locked before the model record is generated or inspected so that later comparison does not silently reshape the first record.

The lock is not merely a status flag. The author record is serialized in a deterministic Core field order and hashed. The lock manifest stores that canonical hash along with the source packet and instruction-set hashes. This does not make the author interpretation authoritative. It makes the record auditable: a later reader can verify that the record being compared is the same record that was locked before the model output was created.

The same principle applies to the model side. A model record is not treated as the model's private reasoning. It is a submitted annotation record produced under a prompt, model context, and source packet. The prompt hash, output hash, and model-run manifest make the local artifact inspectable and prevent quiet substitution of a more convenient model output. They do not make the model run externally reproducible from the recorded metadata alone.

## 5. Design Dependence of the Walkthrough

The source packet was selected by the author. Segmentation was author-designed. The case-specific label vocabulary was author-designed. The mechanism vocabulary was author-designed. The label `unresolved_agency` encodes a theory-led interpretive question. The mechanism `contrast_or_tension` encodes a theory-led relation between self-stabbing and later unidentified intervention.

The packet and codebook were theory-informed and fixed before record comparison. Freezing them prevents post-comparison alteration, but it does not make them neutral or interpretation-free.

The walkthrough is therefore constructive and theory-led. It does not show that the instrument independently discovered a naturally given mismatch. It tests whether a pre-specified interpretive question can be preserved and compared across records.

This design dependence is not a flaw to be hidden. It is part of the artifact being audited. TRIM-HAA can record when a study uses a theory-led packet and vocabulary, but provenance does not transform that design into neutral discovery.

## 6. Case, Packet, and Copyright Status

The source packet is `walkthrough/in_a_grove_v0_1/`. It uses a short excerpt from "In a Grove", focusing on the dead samurai's testimony as conveyed through a medium. The English packet currently uses Takashi Kojima's 1952 translation as hosted by Wikisource.

The original Japanese text and the English translation must be considered separately. Akutagawa's original Japanese work is likely public domain in many jurisdictions because Akutagawa died in 1927 and the story was first published in 1922, but jurisdiction-specific review remains required. The 1952 Kojima English translation is a separate work with its own copyright status. Wikisource hosting is not proof that public redistribution is legally safe in all jurisdictions.

Public release of the packet and ZIP remains blocked pending jurisdiction-specific copyright and translation review. A safer public version may need the Japanese public-domain original, a demonstrably public-domain translation, a newly commissioned or author-created translation where legally appropriate, or non-redistributed source references with minimal quotation.

The packet is segmented into stable IDs. The formal evidence rule is strict: background knowledge may inform interpretation, but every formal evidence claim must cite one or more packet segment IDs. External cultural claims must be explicitly marked as external and cannot substitute for textual evidence.

The segment table avoids embedding an interpretation in the segment labels. Segment IDs identify source position and speaker status, not analytic conclusions. Segment `IAG-SAM-012` is not labelled "external killer" or "contradiction"; it is the segment in which the samurai reports an unidentified later action.

## 7. Walkthrough Method

The author analytic record was completed first as `author_analytic_record.csv`. It was then locked using the TRIM-HAA locking utilities. The lock manifest stores the canonical Core annotation hash, lock time, author record version, source packet hash, and instruction-set hash.

The model prompt was then frozen in `prompts/in_a_grove_trim_haa_v0_1.txt`. It includes only the source packet, local label and mechanism guide, schema requirements, and constraints against invented quotations or unsupported external facts. It states that the model output is a submitted record, not hidden reasoning.

The model output was generated once and saved as `ai_raw_output.txt`. No retry was used. The parsed AI record is saved as `ai_independent_record.csv`, with `actor_type=model` and `annotation_stage=ai_independent`. The model-run manifest records provider, model name, date, prompt hash, output hash, retry count, and source/instruction hashes.

No human participants were involved. No exposure condition was created. No participant revision or control second pass was created. The author record is not an answer key.

The order of operations matters. The author record is not written as a response to the AI record. It is completed first and locked. Only then is the model record generated and parsed. This order does not remove author bias, but it prevents a specific artifact problem: the author record cannot be quietly adjusted after the AI output is known.

The prompt provides the source packet, local labels, local mechanisms, and schema constraints. It requires segment IDs and asks for an explicit alternative-pathway assessment. Segment `IAG-SAM-012` was present in the packet, and the prompt required explicit alternative assessment. The absence of an alternative in the AI record therefore cannot be attributed to missing input or a missing response field. Whether that segment warranted retaining an alternative remains open to independent evaluation.

## 8. Field-by-Field Walkthrough

The author analytic record selects three evidence anchors: the medium framing segment, the self-stabbing segment, and the later unidentified removal of the small sword. Its function label is `unresolved_agency`. Its mechanism is `contrast_or_tension`. Its uncertainty is `medium`. It records an alternative pathway: a narrower reading can foreground the samurai's statement that he stabbed himself.

The AI independent record selects the self-stabbing segment and the subsequent bodily/final-darkness segments. Its function label is `self_inflicted_death`. Its mechanism is `direct_action`. Its uncertainty is `low`. It records no alternative pathway.

The two records share one primary evidence segment: the self-stabbing report. The author record uniquely selects the medium framing and the unidentified removal of the small sword. The AI record uniquely selects the bodily coldness and final-darkness segments. The author and model records therefore differ not only in final label but also in evidence selection, mechanism, uncertainty, and alternative handling. TRIM-HAA preserves those dimensions so that the disagreement can be inspected rather than reduced to a category mismatch.

The rationale notes also differ. The author note foregrounds the tension between self-stabbing, mediation, and later unidentified action. The AI note foregrounds a direct-action sequence that presents the death as self-inflicted within the testimony. The comparison output records overlap descriptively but does not treat lexical difference as a cognition measure.

This field comparison is the strongest result of the walkthrough. It shows that final-label disagreement is only the beginning of review. A reviewer seeing only `self_inflicted_death` and `unresolved_agency` might treat the comparison as a category mismatch. A reviewer seeing selected evidence, mechanism, uncertainty, alternatives, and provenance can inspect where the interpretive pathways diverge.

## 9. Candidate Certainty-Closure Tension

The secondary illustrative review question is a candidate certainty-closure tension. It is not an established certainty-alternative mismatch.

A candidate certainty-closure tension is a record-level review condition in which a record reports low uncertainty and no alternative while omitting or not addressing a packet-anchored element that the walkthrough has designated for review as potentially relevant to interpretive closure.

This is an author-defined review condition. It is not an adjudicated property of the model record. It does not prove that an alternative interpretation is required. It does not prove that low uncertainty is inappropriate. It does not prove model error. It does not prove overconfidence. It generates a review question.

The existing display status `candidate_visible` remains for backward compatibility. `candidate_visible` is a walkthrough display status. It means that the configured review condition was satisfied. It does not establish that the packet objectively contains a competing causal account or that the inspected record is erroneous. Where a human-readable heading is used, `review_question_generated` is the preferred framing.

The AI record creates this display status because it uses low uncertainty, selects evidence that supports `self_inflicted_death`, records no alternative, and does not explicitly address `IAG-SAM-012`, the segment designated by the walkthrough for review as potentially relevant to interpretive closure. The status does not decide the interpretation. It does not depend solely on disagreement with the author record. It means the fields make a candidate question available for later review.

The author record also does not settle the passage. It chooses `unresolved_agency` with medium uncertainty and keeps a narrower self-inflicted pathway as an alternative. That is an analytic posture, not a gold standard. Another independent evaluator might decide that low uncertainty is acceptable because the self-stabbing report is direct and the later removal is not enough to change the submitted interpretation.

## 10. Causal Agency and Narrative Closure

Segment `IAG-SAM-012` does not automatically establish that someone else caused the death. The testimony includes a direct self-stabbing report, and later removal of the blade may affect narrative closure without overturning self-stabbing or self-inflicted fatal injury.

Self-inflicted death and unresolved later intervention may coexist. The later unidentified intervention keeps aspects of sequence, mediation, and narrative closure open, but it does not by itself refute the testimony's own account of death.

The interpretive question therefore concerns the breadth and closure of the submitted record, not a simple binary cause-of-death verdict. The procedural finding is narrow: `IAG-SAM-012` was available to the model and the response field for alternatives was available. Whether the segment warranted retaining an alternative remains open to independent evaluation.

## 11. Representation Is Not Detection

The walkthrough demonstrates representation and display. It does not establish a validated detection rule. An author-defined flag is not an adjudication. Sensitivity and specificity are unknown. False-positive and false-negative behaviour are unknown. Multi-case and independent-evaluator work is required. The current case cannot establish prevalence or generalisability.

TRIM-HAA preserves the inputs needed for review. It does not, in this walkthrough, determine the correct interpretation or validate a detector of interpretive closure problems.

The candidate closure tension is therefore secondary. It illustrates how a review question can be made visible once selected evidence, uncertainty, alternatives, rationale, and provenance are preserved. It is not the central result of the walkthrough.

## 12. Model Provenance and Reproducibility Limits

The model-run manifest records `provider = OpenAI`, `model_name = Codex session model`, `model_version_or_date = 2026-07-01`, `sampling = unavailable`, and `system prompt hash = unavailable`.

This supports local artifact auditability but not external experimental reproducibility. The model artifact is locally auditable but not externally reproducible from the recorded metadata alone.

The exact public model identifier is unavailable. Provider-side system configuration is unavailable. Sampling configuration is unavailable. Session context may not be reconstructable. The output should therefore be treated as a fixed development artifact, not as a model run that another researcher can reproduce from the manifest alone.

For a public empirical version, the model record should be regenerated using a publicly identifiable model/API configuration, or the current output should be explicitly retained only as a non-reproducible development demonstration.

## 13. What This Demonstration Establishes

This walkthrough establishes representational feasibility for one real literary stress-test packet. It shows that TRIM-HAA can store an author analytic record and a model record using the same Core schema. It shows that a pre-comparison author record can be locked with a canonical hash. It shows that prompt, source, instruction, model-run, and output hashes can be recorded. It shows that field-level comparison can identify evidence overlap, evidence difference, mechanism difference, uncertainty difference, rationale overlap, and alternative handling.

Most importantly, it shows that the author and model records differ not only in final label but also in evidence selection, mechanism, uncertainty, and alternative handling. TRIM-HAA preserves those dimensions so that the disagreement can be inspected rather than reduced to a category mismatch.

The walkthrough also shows a practical benefit of provenance. Without the lock and manifests, a reader would have to trust that the author record came first, that the prompt did not change, and that the AI output was not selected from several attempts. With the manifests, those claims become inspectable local artifacts. They are still not guarantees of external reproducibility.

## 14. What It Does Not Establish

This walkthrough provides no human-subject evidence. It provides no reliability estimate. It provides no model-accuracy result. It provides no human superiority claim. It provides no model-bias prevalence claim. It provides no causal exposure result. It provides no generalisation across cases, genres, domains, models, or annotators. It does not empirically validate TRIM-HAA.

It does not empirically demonstrate same-label hidden divergence. Agreement flattening remains a general motivation, a synthetic dry-run capability, and a future empirical target.

It does not establish a true certainty-alternative mismatch. It does not establish model error, overconfidence, or invalid alternative handling. It shows that the configured review condition was triggered and that the record structure preserves the information needed to ask a review question.

The selected passage is one stress-test case. The author analytic record is a demonstration record. The model output is one frozen development artifact from one Codex session model context. The translation and public-release status require legal review. The position note should not be treated as publication-ready until the blockers document is resolved.

## 15. Next Empirical Step

The next empirical step is the ethics-approved instrumentation pilot described elsewhere in the repository. That pilot would collect independent human-pre records, freeze AI records, collect human-post records after AI exposure, and include no-AI second-pass controls. It would measure feasibility, burden, missingness, lock verification, exposure linkage, procedural questions, and descriptive changes across labels, evidence, mechanisms, uncertainty, alternatives, and rationale notes.

The pilot has not been run. It must not begin until ethics and protocol review are complete. Its first purpose is instrumentation and feasibility, not estimation of a causal effect.

For the present note, the most important next step is not to scale immediately. It is to have the packet, guide, claim boundaries, legal status, and model-run provenance reviewed. If the selected translation cannot be publicly redistributed, the package should be revised before release. If the label or mechanism vocabulary is too leading, it should be simplified. If readers find the candidate display too close to adjudication, the language should remain framed as `review_question_generated` rather than as detection.

## 16. Conclusion

The methodological question is not whether the model agrees with a human reader, but whether the annotation record preserves enough evidence, mechanism, uncertainty, alternatives, rationale, and provenance for that agreement or disagreement to be meaningfully audited.

In this walkthrough, the author and model records differ not only in final label but also in evidence selection, mechanism, uncertainty, and alternative handling. TRIM-HAA preserves those dimensions so that the disagreement can be inspected rather than reduced to a category mismatch. The candidate closure tension is a secondary review question, not a finding of a true mismatch, model error, or overconfidence.
