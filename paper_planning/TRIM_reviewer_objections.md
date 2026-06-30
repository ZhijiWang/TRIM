# TRIM Reviewer Objections

| Objection | Is it valid? | How the article should respond | Evidence still needed | Wording to add | Claims to withdraw |
| --- | --- | --- | --- | --- | --- |
| 1. This is just a complicated coding manual. | Partly. The repository is manual-heavy. | Show the payoff: final-label agreement can hide pathway divergence; disagreement can be located by field and adjudication category. | Worked examples and v0.2.1 pathway comparison. | "TRIM is not a longer codebook; it makes the evidence-to-function pathway the comparative unit." | Any claim that complexity is self-justifying. |
| 2. The categories are project-specific. | Yes for function labels; less so for architecture. | Explicitly separate project-specific labels from transferable pathway structure. | Retest with another function vocabulary eventually. | "The function list is project-specific; the proposed transferable element is the pathway architecture." | Universal function taxonomy. |
| 3. The method formalizes interpretation without improving it. | Serious risk. | Define "improvement" as reviewability, not truth. | Memo-only comparison or reviewer reconstruction task. | "TRIM improves the conditions under which interpretive annotations can be reviewed, compared, and revised." | Better interpretation, more valid interpretation. |
| 4. The pilot is too small. | Yes for reliability; no for method development. | Treat v0.2.0 as usability and diagnostic evidence only. | Complete v0.2.1; larger study later. | "The pilot is not a reliability study; it identifies revision targets." | Validated reliability. |
| 5. The method confuses transparency with validity. | Valid if wording is careless. | Make transparency a necessary but insufficient condition. | Adjudication examples showing textual adequacy review. | "Auditability does not make an interpretation valid; it makes the basis for evaluating it more accessible." | Validity-through-transparency. |
| 6. Free-text memos already do this. | Partly. | Argue that memos are rich but hard to compare systematically; TRIM structures selected memo content while retaining notes. | Optional memo-only baseline. | "TRIM does not replace memos; it makes selected components of rationale comparable." | Superiority over memos without baseline. |
| 7. The schema overfits the original cases. | Serious risk. | Emphasize out-of-sample v0.2.1 retest and leakage controls. | Retest outcomes; later corpus. | "v0.2.1 is explicitly prospective and does not recode the original pilot cases." | Stability across domains. |
| 8. The closed function list limits generality. | Yes. | Present closure as a project-level design choice needed for retest. | Demonstrate architecture with alternate vocabularies later. | "TRIM requires an explicit function vocabulary, not this vocabulary." | General function labels. |
| 9. Multilingual claim is weak because coding is translation-mediated. | Yes. | Remove cross-language validation claims. Report language access as a condition. | Direct-language coders or layer/pair design. | "The pilot was multilingual in materials but translation- and summary-mediated in access." | Cross-language validity. |
| 10. The software layer creates false precision. | Valid risk. | Say validators check structure, not interpretive correctness. | Examples where validator passes but adjudication remains interpretive. | "The software preserves and compares human judgments; it does not adjudicate them." | Automated interpretation. |
| 11. The disagreement taxonomy is adjudicator-dependent. | Yes. | Treat taxonomy as a review framework requiring examples and possible multiple adjudicators. | Inter-adjudicator comparison if feasible. | "Adjudication categories are analytic classifications applied after raw disagreement is preserved." | Objective disagreement classification. |
| 12. The method is too burdensome for practical annotation. | Likely. | Measure burden and show when the method is worth it: small/medium interpretive corpora, contested categories, audit needs. | Completion time, coder feedback, field burden. | "TRIM is for projects where reviewable interpretive pathways matter enough to justify added structure." | Lightweight for all annotation tasks. |
| 13. The article lacks a substantive literary result. | Valid for some journals, not DH methods venues. | Make clear this is a methods paper; use literary cases as demonstrations. | Strong worked examples. | "The corpus is designed to stress method boundaries, not to make a corpus-level literary claim." | Substantive literary discovery. |
| 14. Agreement metrics are inappropriate for such small samples. | Partly. | Use descriptive field-level agreement; put kappa/alpha/AC1 in supplement only if justified. | Larger sample for inferential claims. | "Chance-corrected coefficients are reported, if at all, descriptively." | Statistical reliability proof. |
| 15. Alternative signatures invite indecision. | Partly. | Require complete six-field alternative and rationale; pair with at least medium uncertainty. | Retest evidence on use frequency and adjudication. | "Alternatives are recorded only when a complete competing pathway remains defensible." | All ambiguity should become alternative signatures. |
| 16. The retest packet still mediates evidence through summaries. | This was valid before the final patch; it is now addressed. | Explain that every formal segment now supplies actual source text or documented public-domain translation text, with provenance, and that external URLs are references only. | Independent source-text spot check; coder feedback on packet usability. | "The final v0.2.1 packet removes project-authored summaries as formal evidence text." | Any claim that summaries and source text are equivalent. |
| 17. Othello used a singleton shared-context group. | Valid before the final patch. | Explain the new `multi_passage_single_case` scope and why it avoids forcing same-case distributed evidence into a cross-case registry. | Retest evidence on whether coders understand the scope distinction. | "`multi_passage_single_case` covers separated passages within one formal case; it is not cross-case context." | Treating singleton shared context as genuinely cross-case. |

## Claims To Withdraw Or Avoid In The Manuscript

- TRIM validates intercoder reliability.
- TRIM proves cross-language construct validity.
- TRIM is superior to free-text memos.
- TRIM is domain-general.
- TRIM automates interpretive reasoning.
- TRIM eliminates subjective adjudication.
- TRIM solves hermeneutics.

## Claims To Keep

- TRIM structures evidence-to-function reasoning.
- TRIM makes pathway-level disagreement inspectable.
- TRIM separates raw disagreement from adjudication categories.
- TRIM's first pilot exposed usability and boundary problems.
- TRIM v0.2.1 is a prospective retest design.
- TRIM's software validates structure and supports comparison, not interpretation.
