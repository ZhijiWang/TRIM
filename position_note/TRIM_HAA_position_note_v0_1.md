# Auditing Interpretive Annotation Beyond Final Labels: A TRIM-HAA Walkthrough

## 1. Introduction

Interpretive annotations are increasingly produced by humans, language models, or workflows that combine both. A final label alone is rarely enough to explain what an annotation record is doing. Two records may share a label while selecting different evidence. They may select the same passage while giving it different analytic force. They may both sound confident while preserving different levels of uncertainty or different alternative readings. A dataset that records only the final category loses much of this structure.

This matters especially when annotations are described as human-reviewed. Human review after model assistance is not automatically independent human judgment. A human reviewer may keep an earlier judgment, revise after rereading, adopt a model label, incorporate model-selected evidence, adapt model wording, or reject the model record while changing for another reason. Those possibilities cannot be recovered from final labels alone.

TRIM-HAA is designed for this audit problem. It records submitted annotation pathways: evidence, label, evidence-to-label mechanism, uncertainty, rationale note, alternative pathway, and provenance. Its purpose is not to optimise human-AI collaboration, rank participants, or treat model output as an answer key. Its purpose is to make an annotation record reviewable enough that agreement, disagreement, certainty, and revision can be examined field by field.

This position note offers a narrow author-only walkthrough using a short packet from Ryunosuke Akutagawa's "In a Grove" / "Yabu no Naka". The walkthrough compares one researcher-produced analytic record and one independently generated AI record. It asks whether TRIM-HAA can represent a candidate certainty-alternative mismatch: a situation where a record presents a strongly closed interpretation while the packet still preserves an explicit alternative that the record does not adequately address, distinguish, or exclude.

This is a conceptual and technical demonstration. It is not a human-subject study. It is not a reliability study. It is not an accuracy comparison. It is not an AI-bias experiment. It is not a causal exposure study. It does not validate TRIM-HAA.

The limited scope is intentional. A framework for auditing interpretive annotation should first show that it can preserve the parts of a record that make interpretation reviewable. If that representational layer is absent, later claims about human review, model assistance, or collaborative annotation rest on a thin evidential base. Conversely, if the record preserves only a final label, then many different processes can be made to look identical: independent convergence, copied labels, shared evidence selection, shared wording, ordinary rereading, and unresolved uncertainty can all collapse into the same cell in a spreadsheet.

The walkthrough therefore treats representation as a prerequisite for stronger empirical work. It does not argue that more fields are automatically better. A burdensome instrument can make a study worse by encouraging mechanical form filling or by forcing participants to invent distinctions they do not actually use. The question here is narrower: can a small record structure make visible a candidate situation that a final-label workflow would flatten?

## 2. Two Audit Layers

TRIM-HAA separates two audit layers.

The first layer is independent record audit. A human record and a model record are produced independently against the same source packet and instruction set. They can then be compared across evidence, label, mechanism, uncertainty, rationale, alternatives, and provenance. This layer asks what each record preserved, selected, foregrounded, and left open.

The second layer is exposure audit. A human-pre record is locked before model exposure. A frozen model record is shown. A human-post record is then collected, with a no-AI second-pass control where possible. This layer asks what changed after exposure and whether similar second-pass change also appears without AI material.

This position note demonstrates only the independent-record layer. It creates no human-post records, no participant revisions, and no no-AI control records. It therefore makes no claim about exposure-associated change.

The distinction between these two layers is important because they answer different questions. Independent record audit is about comparability: what did each record select, claim, leave uncertain, or preserve as an alternative before any exposure occurred? Exposure audit is about revision: what changes after a person sees a model record, and how should those changes be described without assuming causation too quickly? Mixing those layers would make the walkthrough stronger-sounding but weaker as evidence. The present demonstration keeps them apart.

In practical terms, the independent layer can be used before any human-subject work begins. It can stress-test a source packet, label guide, mechanism vocabulary, prompt, and reporting pipeline. It can also reveal whether the fields are capable of representing the interpretive differences the project claims to care about. The exposure layer requires ethics review, participant-facing materials, and a careful design for timing, consent, burden, and controls. That later layer is not simulated here.

## 3. TRIM-HAA Representation

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

The same principle applies to the model side. A model record is not treated as the model's private reasoning. It is a submitted annotation record produced under a prompt, model context, and source packet. The prompt hash, output hash, and model-run manifest do not make the output reproducible in the strict sense, because provider-side systems may change and session-level configuration may be unavailable. They do, however, make the local artifact inspectable and prevent quiet substitution of a more convenient model output.

## 4. Why Fiction Is a Stress Test

Fiction is useful here because interpretive plurality is not an edge case. Literary passages often support several readings at once. Evidence may be underdetermined. Testimony may be conflicting or mediated. Characters may speak from partial knowledge. Narrative framing may invite and frustrate closure at the same time.

"In a Grove" is a particularly sharp stress test because its structure is built from incompatible testimonies. The selected packet comes from the dead samurai's testimony as conveyed through a medium. It includes a direct report of self-stabbing, but it also includes a later unidentified action involving removal of the small sword. A record can legitimately foreground the self-stabbing report. Another record can foreground the tension between self-report, mediation, and later unidentified action. The methodological question is whether those differences are visible in the annotation record.

Fiction is a testbed, not the claimed domain limit of TRIM-HAA. The same audit problem appears in qualitative coding, cultural analysis, moderation review, historical-source interpretation, and other settings where evidence supports more than one defensible pathway.

The stress test is not that fiction is uniquely ambiguous. The stress test is that fiction makes ambiguity difficult to ignore. It gives the audit framework a passage where evidence selection, narrative framing, and alternative preservation are not auxiliary details but central features of the task. If an annotation system cannot show how a record handles those features, it will struggle in any domain where interpretation is not reducible to a single stable label.

The selected passage is also useful because it separates evidence from closure. The self-stabbing segment is strong evidence for a self-inflicted-death reading. The later unidentified action does not erase that evidence. It does, however, create a packet-visible reason to ask whether a low-uncertainty record with no alternative has closed the case too tightly. TRIM-HAA does not answer that question by itself. It preserves the record structure needed to ask it.

## 5. Case and Packet

The source packet is `walkthrough/in_a_grove_v0_1/`. It uses a short excerpt from "In a Grove", focusing on the dead samurai's testimony as conveyed through a medium. The source edition for the English text is `Rashomon and Other Stories` (1952), translated by Takashi Kojima, as hosted by Wikisource at https://en.wikisource.org/wiki/Rashomon_and_Other_Stories/In_a_Grove.

The packet records the original title, author, publication date, source edition, translator, translation date, and source URL. It also records legal uncertainty. The original Japanese work is likely public domain in many jurisdictions because Akutagawa died in 1927 and the story was first published in 1922. The 1952 English translation is a separate work. Wikisource hosts the translation and provides public-domain rationales for some translations, but public release still requires jurisdiction-specific review. For that reason, this packet is marked not publication-ready until final copyright and translation review is complete.

The packet is segmented into stable IDs. The formal evidence rule is strict: background knowledge may inform interpretation, but every formal evidence claim must cite one or more packet segment IDs. External cultural claims must be explicitly marked as external and cannot substitute for textual evidence.

This evidence rule is deliberately conservative. A reader may know conventions of honor, suicide, testimony, spirit possession, or Akutagawa's narrative design. Such knowledge may be useful in interpretation, but it should not be allowed to appear in the record as if it were packet evidence. The rule requires the record to distinguish what the packet says from what a reader brings to it. That distinction is especially important for model-generated annotations, which may blend textual evidence with broad cultural scripts in fluent language.

The segment table also avoids embedding an interpretation in the segment labels. Segment IDs identify source position and speaker status, not analytic conclusions. The segment `IAG-SAM-012` is not labelled "external killer" or "contradiction"; it is simply the segment in which the samurai reports an unidentified later action. That keeps the annotation task separate from the source-preparation task.

## 6. Walkthrough Method

The author analytic record was completed first as `author_analytic_record.csv`. It was then locked using the TRIM-HAA locking utilities. The lock manifest stores the canonical Core annotation hash, lock time, author record version, source packet hash, and instruction-set hash.

The model prompt was then frozen in `prompts/in_a_grove_trim_haa_v0_1.txt`. It includes only the source packet, local label and mechanism guide, schema requirements, and constraints against invented quotations or unsupported external facts. It states that the model output is a submitted record, not hidden reasoning.

The model output was generated once and saved as `ai_raw_output.txt`. No retry was used. The parsed AI record is saved as `ai_independent_record.csv`, with `actor_type=model` and `annotation_stage=ai_independent`. The model-run manifest records provider, model name, date, prompt hash, output hash, retry count, and source/instruction hashes.

No human participants were involved. No exposure condition was created. No participant revision or control second pass was created. The author record is not an answer key.

The order of operations matters. The author record is not written as a response to the AI record. It is completed first and locked. Only then is the model record generated and parsed. This order does not remove author bias, but it prevents a specific artifact problem: the author record cannot be quietly adjusted after the AI output is known.

The walkthrough also keeps the prompt narrow. The prompt provides the source packet, local labels, local mechanisms, and schema constraints. It does not invite broad literary commentary. It requires segment IDs and asks for an explicit alternative-pathway assessment. Those constraints are part of the audit: if the model record omits an alternative, that omission occurs in a context where the prompt asked for one.

## 7. Field-by-Field Walkthrough

The author analytic record selects three evidence anchors: the medium framing segment, the self-stabbing segment, and the later unidentified removal of the small sword. Its function label is `unresolved_agency`. Its mechanism is `contrast_or_tension`. Its uncertainty is `medium`. It records an alternative pathway: a narrower reading can foreground the samurai's statement that he stabbed himself.

The AI independent record selects the self-stabbing segment and the subsequent bodily/final-darkness segments. Its function label is `self_inflicted_death`. Its mechanism is `direct_action`. Its uncertainty is `low`. It records no alternative pathway.

The two records share one primary evidence segment: the self-stabbing report. The author record uniquely selects the medium framing and the unidentified removal of the small sword. The AI record uniquely selects the bodily coldness and final-darkness segments. This is precisely the type of difference that final labels alone cannot show. Even if both records had selected the same final label, the evidence and alternative fields would still matter.

The rationale notes also differ. The author note foregrounds the tension between self-stabbing, mediation, and later unidentified action. The AI note foregrounds a direct-action sequence that presents the death as self-inflicted within the testimony. The comparison output records overlap descriptively but does not treat lexical difference as a cognition measure.

The field comparison therefore does not simply ask whether the author and model agree. It asks what agreement would mean. If both records choose `self_inflicted_death`, but one uses only the self-stabbing segment while another cites the later unidentified action and records an alternative, then label agreement would hide a substantive difference. If both records choose different labels but share the same evidence, the disagreement might concern mechanism or closure rather than source selection. If uncertainty differs, the question becomes whether the record preserved the grounds for that difference.

This is why the evidence and alternative fields are not decorative. They determine what kind of review is possible. A reviewer seeing only `self_inflicted_death` and `unresolved_agency` might treat the comparison as disagreement. A reviewer seeing the selected segments can instead ask whether the later unidentified action is enough to sustain an alternative pathway, whether the medium framing should matter, and whether low uncertainty is justified by the direct self-stabbing report. Those are interpretive questions, not automatic system outputs.

## 8. Candidate Certainty-Alternative Mismatch

The walkthrough's candidate construct is cautious. A candidate certainty-alternative mismatch is a descriptive situation where a record reports low uncertainty or otherwise presents a strongly closed interpretation, selects evidence supporting that interpretation, and the same packet still preserves at least one explicit alternative that the record does not adequately address, distinguish, or exclude.

The AI record creates a `candidate_visible` display status in this walkthrough because it uses low uncertainty, selects evidence that supports `self_inflicted_death`, records no alternative, and does not explicitly address the segment where an unidentified "someone" removes the small sword. The status does not decide the interpretation. It does not depend solely on disagreement with the author record. It means the fields make a candidate question available for later review.

The author record also does not settle the passage. It chooses `unresolved_agency` with medium uncertainty and keeps a narrower self-inflicted pathway as an alternative. That is an analytic posture, not a gold standard. Another independent evaluator might decide that low uncertainty is acceptable because the self-stabbing report is direct and the later removal is not enough to reopen the primary interpretation. TRIM-HAA's contribution here is representational: it shows what evidence and alternatives each record did or did not preserve.

The candidate status is not a defect label. It is closer to a flag on a reading question: here is a record that closes strongly; here is packet material that might support a competing path; here is whether the record acknowledged that path. The next step could be independent adjudication, author revision, model-prompt revision, participant testing, or no action at all. The display is useful precisely because it does not collapse those choices into a single verdict.

The status also does not depend on the author's record being different. In principle, a candidate could be visible even if the author record were absent, as long as the packet contains an explicit alternative and the record being inspected does not address it. The author record is useful here because it illustrates another possible way to encode the passage, but the candidate logic must remain grounded in the inspected record and packet, not in author disagreement alone.

## 9. What This Demonstration Establishes

This walkthrough establishes representational feasibility for one real literary stress-test packet. It shows that TRIM-HAA can store an author analytic record and a model record using the same Core schema. It shows that a pre-comparison author record can be locked with a canonical hash. It shows that prompt, source, instruction, model-run, and output hashes can be recorded. It shows that field-level comparison can identify evidence overlap, evidence difference, mechanism difference, uncertainty difference, rationale overlap, and alternative handling.

It also shows that the candidate mismatch can be displayed without a binary truth verdict. The system can formulate a testable empirical question: in a larger study, how often do low-uncertainty records omit explicit packet alternatives, and how do human reviewers respond when such records are shown?

That empirical question is broader than this case. It could be asked of human records, model records, or post-exposure human records. It could be applied to literary interpretation, qualitative coding, policy classification, or expert review. The point is not that low uncertainty is suspicious. The point is that low uncertainty plus unaddressed packet alternatives is a pattern worth being able to see.

The walkthrough also shows a practical benefit of provenance. Without the lock and manifests, a reader would have to trust that the author record came first, that the prompt did not change, and that the AI output was not selected from several attempts. With the manifests, those claims become inspectable local artifacts. They are still not perfect guarantees of external reproducibility, but they are stronger than narrative assurance.

## 10. What It Does Not Establish

This walkthrough provides no human-subject evidence. It provides no reliability estimate. It provides no model-accuracy result. It provides no human superiority claim. It provides no model-bias prevalence claim. It provides no causal exposure result. It provides no generalisation across cases, genres, domains, models, or annotators. It does not empirically validate TRIM-HAA.

The selected passage is one stress-test case. The author analytic record is a demonstration record. The model output is one frozen record from one model context. The translation and public-release status require legal review. The position note should not be treated as publication-ready until the blockers document is resolved.

The walkthrough also does not show that the Core fields are easy for participants to use. It does not show that different humans would agree on the label guide or mechanism vocabulary. It does not show that the candidate construct appears frequently. It does not show that model exposure changes human judgments. Those are empirical matters for later work.

Finally, the walkthrough does not infer private cognition. A rationale note may be sincere, strategic, incomplete, or simply a convenient explanation. The same is true for a model-generated rationale as a submitted record. TRIM-HAA audits what is submitted and how it is linked to source evidence. It does not claim direct access to mental process or model internals.

## 11. Next Empirical Step

The next empirical step is the ethics-approved instrumentation pilot described elsewhere in the repository. That pilot would collect independent human-pre records, freeze AI records, collect human-post records after AI exposure, and include no-AI second-pass controls. It would measure feasibility, burden, missingness, lock verification, exposure linkage, procedural questions, and descriptive changes across labels, evidence, mechanisms, uncertainty, alternatives, and rationale notes.

The pilot has not been run. It must not begin until ethics and protocol review are complete. Its first purpose is instrumentation and feasibility, not estimation of a causal effect.

For the present note, the most important next step is not to scale immediately. It is to have the packet, guide, claim boundaries, and legal status reviewed. If the selected translation cannot be publicly redistributed, the package should be revised before release. If the label or mechanism vocabulary is too leading, it should be simplified. If readers find the candidate display too close to adjudication, the language should be tightened further. The point of this artifact is to make those review tasks concrete.

## 12. Conclusion

The methodological question is not whether the model agrees with a human reader, but whether the annotation record preserves enough evidence, uncertainty, alternatives, and provenance for that agreement or disagreement to be meaningfully audited.
