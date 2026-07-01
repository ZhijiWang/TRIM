# Auditing Interpretive Annotation Beyond Final Labels: A TRIM-HAA Walkthrough

## Abstract

Interpretive annotations are increasingly produced by humans, language models, and workflows in which model output is reviewed by people. Yet most annotation datasets preserve only the final label. That record is too thin to show which evidence was selected, how the evidence was connected to the label, how uncertainty was expressed, whether alternatives remained open, or whether a human judgment was produced independently of model exposure.

TRIM-HAA addresses this audit problem by preserving selected evidence, function label, rationale mechanism, uncertainty, rationale note, alternative pathway, and provenance. It does not optimise human-AI collaboration or treat model output as an answer key. This position note presents a narrow author-only walkthrough of the independent-record layer using a short packet from Ryunosuke Akutagawa's "In a Grove" / "Yabu no Naka". One researcher-produced analytic record and one independently generated model record are compared field by field.

The walkthrough directly demonstrates **disagreement flattening**. A final-label comparison shows that the records disagree, but it does not preserve whether the disagreement arises from evidence selection, evidence-to-label mechanism, uncertainty, alternative preservation, or rationale structure. The walkthrough does not empirically demonstrate same-label hidden divergence because the author and model records use different labels. Its contribution is therefore representational: TRIM-HAA preserves the structure of interpretive disagreement so that it can be inspected rather than reduced to a category mismatch.

## 1. The Audit Problem

A final label is useful, but it is not a sufficient audit record. Two annotations may share a label while relying on different passages, different inferential relations, or different levels of certainty. Conversely, two annotations may use different labels while sharing much of their evidence and diverging mainly in how tightly they close interpretation.

This limitation becomes more consequential when annotations are described as human-reviewed. Review after model exposure is not automatically independent human judgment. A reviewer may retain an earlier decision, revise after rereading, adopt a model label, incorporate model-selected evidence, adapt model wording, or reject the model record while changing for another reason. None of those pathways can be reconstructed from a final label alone.

TRIM-HAA is designed to preserve submitted annotation pathways. Its Core records:

- primary evidence;
- function label;
- rationale mechanism;
- uncertainty;
- rationale note;
- alternative pathway;
- provenance.

The aim is not to rank human and model interpretations. It is to make the basis and history of an annotation inspectable.

## 2. Two Audit Layers

TRIM-HAA separates two related but distinct audit layers.

### Independent-record audit

A human record and a model record are produced independently against the same source packet and instruction set. They can then be compared across evidence, label, mechanism, uncertainty, rationale, alternatives, and provenance. This layer asks what each record selected, foregrounded, and left open before any exposure occurred.

### Exposure audit

A human-pre record is locked before model exposure. A frozen model record may then be shown, after which a human-post record is collected. A no-AI second-pass control provides a descriptive comparison for ordinary revision without model material.

This position note demonstrates only the independent-record layer. It creates no human-post records, no participant revisions, and no no-AI control records. It therefore makes no claim about exposure-associated change.

## 3. What Final Labels Flatten

TRIM-HAA is motivated by two forms of flattening.

### Agreement flattening

Two records may share a final label while differing in evidence, mechanism, uncertainty, alternatives, or rationale. A label-only table may therefore make distinct interpretive pathways look equivalent.

The current walkthrough does not empirically demonstrate this form because the author and model records use different labels. Agreement flattening remains a general motivation, a synthetic dry-run capability, and a future empirical target. A same-label/different-pathway case is not added here because constructing one after inspecting the current model output would create a post hoc demonstration.

### Disagreement flattening

Different final labels identify category-level disagreement but do not explain its structure. They do not show whether the records diverge because they selected different passages, used different evidence-to-label mechanisms, expressed different uncertainty, or handled alternatives differently.

The current walkthrough directly demonstrates disagreement flattening. A final-label comparison identifies disagreement. TRIM-HAA preserves where that disagreement lies.

## 4. The Walkthrough Record

The human-side record is explicitly a **researcher-produced analytic demonstration; not human-subject data and not a gold standard**. It was completed and cryptographically locked before the model record was generated or inspected. The lock does not make the author's interpretation authoritative. It verifies that the record being compared is the record that existed before the model output was known.

The model record is likewise treated as a submitted annotation record, not as access to hidden model reasoning. Its prompt, source packet, output, and local manifests are retained so that the artifact can be inspected and quiet substitution can be detected.

The walkthrough therefore compares two fixed records under a shared schema. It does not adjudicate which record is correct.

## 5. Design Dependence of the Walkthrough

The source packet was selected by the author. Segmentation was author-designed. The case-specific label vocabulary and mechanism vocabulary were also author-designed. In particular, `unresolved_agency` encodes a theory-led interpretive question, while `contrast_or_tension` encodes a theory-led relation between self-stabbing and later unidentified intervention.

The packet and codebook were **theory-informed and fixed before record comparison**. Freezing them prevents post-comparison alteration, but it does not make them neutral or interpretation-free.

The walkthrough is therefore constructive. It tests whether a pre-specified interpretive question can be preserved and compared across records. It does not show that TRIM-HAA independently discovered a naturally given mismatch. Provenance makes design choices visible; it does not convert those choices into neutral discovery.

## 6. Case, Packet, and Evidence Rule

The packet uses a short excerpt from Akutagawa's "In a Grove", focusing on the dead samurai's testimony as conveyed through a medium. The English packet currently uses Takashi Kojima's 1952 translation as hosted by Wikisource.

The original Japanese text and the English translation must be considered separately. Akutagawa's original work is likely public domain in many jurisdictions, but the Kojima translation is a separate work with its own copyright status. Wikisource hosting is not proof that public redistribution is legally safe in all jurisdictions. Public release of the packet and ZIP therefore remains blocked pending jurisdiction-specific copyright and translation review.

The formal evidence rule is packet-bound:

> Background knowledge may inform interpretation, but every formal evidence claim must cite one or more packet segment IDs. External cultural claims must be explicitly marked as external and cannot substitute for textual evidence.

Segment IDs identify source position and speaker status rather than analytic conclusions. `IAG-SAM-012`, for example, identifies the segment in which the samurai reports an unidentified later action; it is not labelled as a contradiction, external killing, or proof of another cause.

## 7. Procedure and Provenance

The author analytic record was completed first and locked using the TRIM-HAA locking utilities. The lock manifest stores the canonical Core hash together with the source-packet and instruction-set hashes.

The model prompt was then frozen. It provided the source packet, local label and mechanism guide, schema requirements, and constraints against invented quotations and unsupported external facts. It required exact segment IDs and an explicit alternative-pathway assessment.

One model output was generated and saved. No retry was used. The parsed record was stored as an `ai_independent` annotation, with prompt, output, source, instruction, and model-run metadata retained.

This order matters. The author record cannot be quietly rewritten after the model record is known. At the same time, locking does not remove author bias or settle interpretation; it only secures the sequence and identity of the artifacts.

## 8. Field-by-Field Comparison

The author analytic record selects three evidence anchors:

- the medium framing segment;
- the self-stabbing segment;
- the later unidentified removal of the small sword.

It assigns `unresolved_agency`, uses `contrast_or_tension`, reports medium uncertainty, and retains a narrower self-inflicted-death reading as an alternative.

The model record selects:

- the self-stabbing segment;
- the subsequent bodily-coldness segment;
- the final-darkness segment.

It assigns `self_inflicted_death`, uses `direct_action`, reports low uncertainty, and records no alternative pathway.

The records share the self-stabbing report but differ elsewhere. The author foregrounds mediation and later unidentified intervention. The model foregrounds the direct action sequence within the testimony. Their difference is therefore not exhausted by the labels `unresolved_agency` and `self_inflicted_death`. It also involves evidence selection, mechanism, uncertainty, and alternative handling.

This is the strongest result of the walkthrough. A label-only table would record a category mismatch. TRIM-HAA makes the structure of that mismatch inspectable.

## 9. A Secondary Review Question: Certainty and Closure

The walkthrough also generates a secondary review question described as a **candidate certainty-closure tension**.

A candidate certainty-closure tension is an author-defined review condition in which a record reports low uncertainty and no alternative while not addressing a packet-anchored element that the walkthrough has designated as potentially relevant to interpretive closure.

The stored status `candidate_visible` remains for backward compatibility. It means only that the configured author-defined review rule was triggered. It does not establish that the packet objectively contains a competing causal account, that an alternative was required, or that the inspected record is erroneous. In human-readable reporting, `review_question_generated` is the preferred description.

The procedural finding is narrow but useful: `IAG-SAM-012` was present in the packet, and the prompt required explicit alternative assessment. The absence of an alternative in the model record therefore cannot be attributed to missing input or a missing response field. Whether that segment warranted retaining an alternative remains open to independent evaluation.

## 10. Causal Agency Is Not Narrative Closure

`IAG-SAM-012` does not automatically establish that another person caused the death. The testimony includes a direct self-stabbing report. Later removal of the blade may affect sequence, mediation, and narrative closure without overturning self-stabbing or self-inflicted fatal injury.

Self-inflicted death and unresolved later intervention may coexist. The review question concerns the breadth and closure of the submitted record, not a binary verdict about physical cause of death.

This distinction matters because an audit framework should not turn every omitted detail into a contradiction. Its value lies in preserving enough structure for a reviewer to ask whether an omission matters.

## 11. Representation Is Not Detection

The walkthrough demonstrates representation and display. It does not establish a validated detection rule.

An author-defined flag is not an adjudication. Sensitivity, specificity, false-positive behaviour, and false-negative behaviour are unknown. The current case cannot establish prevalence or generalisability. Multi-case work and independent evaluation would be required before any claim that TRIM-HAA detects interpretive closure problems.

TRIM-HAA preserves inputs needed for review. In this walkthrough, it does not determine the correct interpretation.

## 12. Model Provenance and Reproducibility Limits

The model-run manifest records:

- `provider = OpenAI`;
- `model_name = Codex session model`;
- `model_version_or_date = 2026-07-01`;
- sampling configuration unavailable;
- system-prompt hash unavailable.

This supports local artifact auditability but not external experimental reproducibility. The model artifact is **locally auditable but not externally reproducible from the recorded metadata alone**.

The exact public model identifier, provider-side system configuration, sampling configuration, and full session context cannot be reconstructed. The output should therefore be treated as a fixed development artifact. A public empirical version should use a publicly identifiable model/API configuration, or retain the present output only with this limitation made explicit.

## 13. What the Walkthrough Establishes

For one real literary stress-test packet, the walkthrough establishes that TRIM-HAA can:

- store an author analytic record and a model record under the same Core schema;
- cryptographically lock the author record before comparison;
- preserve prompt, source, instruction, model-run, and output provenance;
- compare evidence overlap and difference;
- compare mechanism, uncertainty, rationale, and alternative handling;
- display the structure of disagreement rather than reducing it to a final-label mismatch.

It also formulates a later empirical question: under what conditions do low-uncertainty records leave packet-anchored closure questions unaddressed, and how do independent reviewers evaluate such records?

## 14. What the Walkthrough Does Not Establish

This walkthrough provides:

- no human-subject evidence;
- no reliability estimate;
- no model-accuracy result;
- no human-superiority claim;
- no model-bias prevalence claim;
- no causal exposure result;
- no generalisation across cases, genres, domains, models, or annotators;
- no empirical validation of TRIM-HAA.

It does not empirically demonstrate same-label hidden divergence. It does not establish a true certainty-alternative mismatch, model error, overconfidence, or invalid alternative handling. It shows that a configured review condition was triggered and that the record preserves information needed for further review.

## 15. Next Empirical Step

The next empirical step is the ethics-reviewed instrumentation pilot described elsewhere in the repository. That pilot would collect independent human-pre records, frozen model records, human-post records after model exposure, and no-AI second-pass controls. Its first purpose is feasibility: whether participants can use the fields, whether records lock and link correctly, and whether burden and missingness remain manageable.

The pilot has not been run and should not begin until ethics and protocol review are complete.

Before public release of this note, three additional issues remain material:

1. participant-facing language and mechanism guides require human review;
2. the Kojima translation requires jurisdiction-specific legal review;
3. a public empirical model record requires a more reproducible model configuration.

## 16. Conclusion

The methodological question is not whether a model agrees with a human reader. It is whether an annotation record preserves enough evidence, mechanism, uncertainty, alternatives, rationale, and provenance for agreement or disagreement to be meaningfully audited.

In this walkthrough, the author and model records differ in final label, evidence selection, mechanism, uncertainty, and alternative handling. TRIM-HAA preserves those dimensions so that the disagreement can be inspected rather than reduced to a category mismatch. The candidate closure tension remains a secondary review question, not a finding of model error or a validated mismatch.