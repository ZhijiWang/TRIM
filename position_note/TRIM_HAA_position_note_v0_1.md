# Auditing Interpretive Annotation Beyond Final Labels: A TRIM-HAA Walkthrough

## Abstract

Interpretive annotations are increasingly produced by humans, language models, and workflows in which model output is reviewed by people. Yet most annotation datasets preserve only the final label. That record is too thin to show which evidence was selected, how the evidence was connected to the label, how uncertainty was expressed, whether alternatives remained open, or whether a human judgment was produced independently of model exposure.

TRIM-HAA addresses this audit problem by preserving selected evidence, function label, rationale mechanism, uncertainty, rationale note, alternative pathway, and provenance. It does not optimise human-AI collaboration or treat model output as an answer key. This position note presents a narrow author-only walkthrough of the independent-record layer using a short packet from Ryunosuke Akutagawa's "In a Grove" / "Yabu no Naka". One researcher-produced analytic record and one independently generated model record are compared field by field.

Final labels flatten the structure of both agreement and disagreement. TRIM-HAA preserves selected evidence, mechanism, uncertainty, alternatives, and provenance so that the structure of interpretive difference remains reviewable. The current walkthrough directly demonstrates disagreement flattening. It does not empirically demonstrate same-label hidden divergence. Same-label divergence remains a general motivation, a synthetic capability already supported by the dry run, and a future empirical target.

## 1. The Audit Problem

A final label is useful, but it is not a sufficient audit record. Two annotations may share a label while relying on different passages, different inferential relations, or different levels of certainty. Conversely, two annotations may use different labels while sharing much of their evidence and diverging mainly in how tightly they close interpretation.

A final-label comparison identifies disagreement but does not preserve its structure. It also identifies agreement without showing whether two records reached that agreement through the same evidence, mechanism, uncertainty posture, alternatives, or rationale.

TRIM-HAA records submitted annotation pathways: primary evidence, function label, rationale mechanism, uncertainty, rationale note, alternative pathway, and provenance. Its aim is not to rank human and model interpretations. It is to make the basis and history of an annotation inspectable.

## 2. Two Audit Layers

TRIM-HAA separates two related but distinct audit layers.

### Independent record audit

A human record and a model record are produced independently against the same source packet and instruction set. They can then be compared across evidence, label, mechanism, uncertainty, rationale, alternatives, and provenance.

### Exposure audit

A human-pre record is locked before model exposure. A frozen model record may then be shown, after which a human-post record is collected. A no-AI second-pass control provides a descriptive comparison for ordinary revision without model material.

This position note demonstrates only the independent-record layer. It creates no human-post records, no participant revisions, and no no-AI control records. It therefore makes no claim about exposure-associated change.

## 3. What Final Labels Flatten

Agreement flattening occurs when two records share a final label but differ in evidence, mechanism, uncertainty, alternatives, or rationale. The current walkthrough does not empirically demonstrate same-label hidden divergence because the author and AI records use different labels. Same-label divergence remains a general motivation, a synthetic dry-run capability, and a future empirical target.

Disagreement flattening occurs when different final labels reveal category-level disagreement but do not reveal whether that disagreement arises from evidence selection, evidence-to-label mechanism, uncertainty, alternative preservation, or rationale structure. The current walkthrough directly demonstrates disagreement flattening.

A same-label/different-pathway case would directly demonstrate agreement flattening, but no such case is added here because constructing one after inspecting the current AI output would create a post hoc demonstration.

## 4. The Walkthrough Record

The human-side record is explicitly a researcher-produced analytic demonstration; not human-subject data and not a gold standard. It was completed and cryptographically locked before the model record was generated or inspected.

The model record is treated as a submitted annotation record, not as access to hidden model reasoning. Its prompt hash, source packet, output, and model-run manifest are retained so that the artifact can be inspected and quiet substitution can be detected.

## 5. Design Dependence of the Walkthrough

The source packet was selected by the author. Segmentation was author-designed. The case-specific label vocabulary was author-designed. The mechanism vocabulary was author-designed. The label `unresolved_agency` encodes a theory-led interpretive question, while `contrast_or_tension` encodes a theory-led relation between self-stabbing and later unidentified intervention.

The packet and codebook were theory-informed and fixed before record comparison. Freezing them prevents post-comparison alteration, but it does not make them neutral or interpretation-free.

The walkthrough is therefore constructive. It does not show that the instrument independently discovered a naturally given mismatch. It tests whether a pre-specified interpretive question can be preserved and compared across records.

## 6. Case, Packet, and Evidence Rule

The packet uses a short excerpt from Akutagawa's "In a Grove", focusing on the dead samurai's testimony as conveyed through a medium. The English packet currently uses Takashi Kojima's 1952 translation as hosted by Wikisource.

The original Japanese text and the English translation must be considered separately. Wikisource hosting is not proof that public redistribution is legally safe in all jurisdictions. Public release therefore remains blocked pending copyright and translation review.

The formal evidence rule is packet-bound: background knowledge may inform interpretation, but every formal evidence claim must cite one or more packet segment IDs. External cultural claims must be explicitly marked as external and cannot substitute for textual evidence.

## 7. Procedure and Provenance

The author analytic record was completed first and locked using the TRIM-HAA locking utilities. The model prompt was then frozen. One model output was generated and saved. No retry was used.

Segment `IAG-SAM-012` was present in the packet, and the prompt required explicit alternative assessment. The absence of an alternative in the model record therefore cannot be attributed to missing input or a missing response field. Whether that segment warranted retaining an alternative remains open to independent evaluation.

## 8. Field-by-Field Comparison

The author record selects the medium framing segment, the self-stabbing segment, and the later unidentified removal of the small sword. It assigns `unresolved_agency`, uses `contrast_or_tension`, reports medium uncertainty, and retains a narrower self-inflicted-death reading as an alternative.

The model record selects the self-stabbing segment, the subsequent bodily-coldness segment, and the final-darkness segment. It assigns `self_inflicted_death`, uses `direct_action`, reports low uncertainty, and records no alternative pathway.

The records share the self-stabbing report but differ in evidence selection, mechanism, uncertainty, and alternative handling. This is the strongest result of the walkthrough: a label-only table records a category mismatch, while TRIM-HAA preserves the structure of that disagreement.

## 9. Candidate Certainty-Closure Tension

The secondary review question is a candidate certainty-closure tension. It is not an established certainty-alternative mismatch.

A candidate certainty-closure tension is an author-defined review condition in which a record reports low uncertainty and no alternative while not addressing a packet-anchored element that the walkthrough has designated as potentially relevant to interpretive closure.

An author-defined flag is not an adjudication. `candidate_visible` is a walkthrough display status. It means that the configured review condition was satisfied. It does not establish that the packet objectively contains a competing causal account, that an alternative interpretation is required, that low uncertainty is inappropriate, or that the inspected record is erroneous.

## 10. Causal Agency and Narrative Closure

`IAG-SAM-012` does not automatically establish that someone else caused the death. Self-inflicted death and unresolved later intervention may coexist. The later unidentified intervention may keep aspects of sequence, mediation, and narrative closure open without overturning self-stabbing or self-inflicted fatal injury.

The interpretive question concerns the breadth and closure of the submitted record, not a binary verdict about physical cause of death.

## 11. Representation Is Not Detection

The walkthrough demonstrates representation and display. It does not establish a validated detection rule.

An author-defined flag is not an adjudication. Sensitivity, specificity, false-positive behaviour, and false-negative behaviour are unknown. Multi-case and independent-evaluator work is required.

TRIM-HAA preserves the inputs needed for review. It does not, in this walkthrough, determine the correct interpretation or validate a detector of interpretive closure problems.

## 12. Model Provenance and Reproducibility Limits

The model-run manifest records `provider = OpenAI`, `model_name = Codex session model`, `model_version_or_date = 2026-07-01`, sampling unavailable, and system-prompt hash unavailable.

This supports local artifact auditability but not external experimental reproducibility. The model artifact is locally auditable but not externally reproducible from the recorded metadata alone.

## 13. What the Walkthrough Establishes

This walkthrough establishes representational feasibility for one real literary stress-test packet. It shows that TRIM-HAA can store an author analytic record and a model record under the same Core schema, verify a pre-comparison lock, retain provenance, and compare evidence, mechanism, uncertainty, rationale, and alternatives.

Most importantly, it shows that the author and model records differ not only in final label but also in evidence selection, mechanism, uncertainty, and alternative handling. TRIM-HAA preserves those dimensions so that the disagreement can be inspected rather than reduced to a category mismatch.

## 14. What the Walkthrough Does Not Establish

This walkthrough provides no human-subject evidence, no reliability estimate, no model-accuracy result, no human-superiority claim, no model-bias prevalence claim, no causal exposure result, no generalisation, and no empirical validation of TRIM-HAA.

It does not empirically demonstrate same-label hidden divergence. It does not establish a true certainty-alternative mismatch, model error, overconfidence, or invalid alternative handling.

## 15. Next Empirical Step

The next empirical step is the ethics-reviewed instrumentation pilot described elsewhere in the repository. That pilot would collect independent human-pre records, frozen model records, human-post records after model exposure, and no-AI second-pass controls.

The pilot has not been run and should not begin until ethics and protocol review are complete.

## 16. Conclusion

The methodological question is not whether a model agrees with a human reader. It is whether an annotation record preserves enough evidence, mechanism, uncertainty, alternatives, rationale, and provenance for agreement or disagreement to be meaningfully audited.

In this walkthrough, TRIM-HAA preserves the structure of disagreement rather than reducing it to a final-label mismatch. The candidate closure tension remains a secondary review question, not a finding of model error or a validated mismatch.