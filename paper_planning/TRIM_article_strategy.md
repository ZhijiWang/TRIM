# TRIM Article Strategy

Working branch reviewed: `pilot-informed-v0.2.2`  
Head inspected before v0.2.2 patch: `252f4b1c867751bd996885ec674f5f546ddbc110`  
Draft PR inspected: #12, open draft, no review comments or discussion threads as of review.

## Direct Verdict

TRIM is **ready to draft as a disciplined digital humanities methods article**, but **not ready to submit until the human v0.2.2 retest is completed and analyzed**.

The first article should not claim that TRIM has solved intercoder reliability. The current evidence supports a narrower but publishable argument: final-label agreement and disagreement are methodologically underspecified in interpretive annotation, and TRIM provides a structured pathway record that makes the location and character of interpretive disagreement inspectable.

Revised default architecture after the source-text and scope patch:

- one integrated methods article containing the final-label compression problem, TRIM architecture, v0.2.0 diagnostic usability pilot, pilot failure modes, v0.2.1 prospective source-text retest package, v0.2.1 AI protocol dry run, v0.2.2 minimal pre-human-deployment patch, future human v0.2.2 retest, pathway-level and field-level comparison, limitations, and future validation;
- a later second article only if it has genuinely new empirical scope: larger multi-coder validation, another domain, another function vocabulary, memo-only comparison, direct-source cross-language replication, or broader generalization.

A pre-retest paper would likely appear incomplete because the repository now contains a carefully corrected and leakage-tested prospective human retest package. The most credible article should use that design rather than stop at a pilot-informed promise. Drafting can begin now; submission should wait. No v0.2.1 AI dry-run or v0.2.2 human-retest empirical result should be invented or implied before human retest completion.

Before human deployment, a machine-executed dry run was used as a protocol
stress test. It identified ambiguity in two coder-facing metadata fields and a
need for a consistency warning between logged coding questions and final
uncertainty reporting. These issues were corrected prospectively in v0.2.2
without changing cases, source texts, source segments, or substantive coding
categories. The AI dry run is not empirical validation and its substantive
labels are not article findings.

## Article Model Evaluation

| Model | Central research question | Main contribution | Required empirical evidence | Reviewer expectations | Strongest feature | Greatest weakness | Current repo sufficient? | Retest needed first? | Likely journal family | Main risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A. Digital humanities methods article | How can interpretive annotation preserve the pathway from textual evidence to analytic function without pretending interpretation is mechanical? | A structured middle layer between categorical annotation and unrestricted memoing. | Method architecture; worked examples; v0.2.0 usability/adjudication; v0.2.1 prospective retest design; ideally completed retest. | Conceptual clarity, DH relevance, honest limits, evidence of usability, reproducible materials. | Best match for TRIM's actual contribution and repository evidence. | May look overbuilt if examples do not show payoff beyond a codebook. | Sufficient to draft; not ideal to submit without retest. | Strongly recommended. | DH / computational humanities. | Under-validated if framed as established method. |
| B. Computational literary studies / cultural analytics article | What is lost when literary interpretation is reduced to labels, features, themes, sentiments, events, or relations? | Models the conversion from evidence to interpretation rather than only the output. | Strong literary examples; comparison to existing CLS annotation/classification practices; retest helpful but less central than conceptual payoff. | Clear relation to operationalization, distant/close reading, annotation, modelling interpretation; article must do literary work, not only method governance. | TRIM's pathway idea answers a real CLS problem. | Current corpus is boundary-stress design, not a substantive literary study. | Draftable as methodological CLS; weak as substantive CLS. | Recommended for credible empirical section. | JCLS, JCA, DSH. | Under-theorized or too internally focused. |
| C. Qualitative methodology / interpretive methods article | How should interpretive disagreement be decomposed into error, ambiguity, insufficient evidence, compatible difference, substantive variation, and unresolved alternatives? | Disagreement is not a homogeneous reliability failure. | Larger multi-coder design; robust adjudication protocol; comparison to qualitative coding and reliability literature; possibly domains outside literature. | Stronger sampling, coder recruitment detail, reflexivity, validity discussion, and methodological generality. | TRIM's adjudication taxonomy is genuinely useful. | TRIM is currently literary/DH-specific and pilot-scale. | Not sufficient for top qualitative methods journals. | Yes, and probably more than v0.2.1. | Qualitative / social research methods. | Under-validated and disciplinary misfit. |
| D. Research software / infrastructure article | What software infrastructure supports reviewable interpretive annotation pathways? | Schema, validator, comparison utilities, package generation, leakage tests, graph representation. | Release, installability, tests, docs, example datasets, software statement, archival DOI, use case. | Working package, maturity, user need, maintenance plan, clear software contribution. | Repository has real validators, tests, package builder, graph exports. | Software is lightweight support for a method, not the central novelty. | Sufficient for a fallback software note after release. | Not essential, but retest would show use. | JORS, SoftwareX, JOHD only if data package angle. | Undersells interpretive contribution; invites software maturity critique. |

## Recommended Model

Primary model: **A. Digital humanities methods article**.

Secondary fallback: **B. Computational literary studies / cultural analytics methods article**.

Rejected as main route:

- **C. Qualitative methodology article** should be postponed until TRIM has a larger multi-coder validation design, possibly across different interpretive domains.
- **D. Research software article** should be kept as a fallback or companion note only after a formal release. It should not be the main paper because the software exists to support the methodological claim.

## Strongest Defensible Article Thesis

The strongest version is:

> Interpretive annotation becomes more reviewable when disagreement is decomposed across the pathway linking textual evidence to analytic function, rather than compressed into agreement or disagreement over final labels alone. TRIM operationalizes that pathway as a structured record of evidence, anchor, threshold, rationale, support, discourse level, temporality, uncertainty, and viable alternative signatures.

Supported refinement:

> Final-label agreement can conceal distinct evidential and inferential pathways, while final-label disagreement can arise from different methodological causes. TRIM makes those differences inspectable, but the current evidence supports method development and pilot usability, not validated intercoder reliability.

## Claim Types

- **Theoretical claim:** interpretation contains warranting pathways, not just outputs. Safe if positioned within hermeneutics, qualitative methodology, argumentation, annotation, and provenance.
- **Methodological claim:** TRIM decomposes evidence-to-function reasoning into fields that can be compared and adjudicated. Strongly supported by codebook, manuals, pilot adjudication, and utilities.
- **Software/infrastructure claim:** TRIM provides a schema, validator, comparison tools, graph exports, source-segment workflows, and leakage-tested retest packaging. Supported by implementation and tests.
- **Empirical pilot finding:** v0.2.0 showed independent completion and revealed specific instability points: evidence selection, function/actor uptake, discourse level, context inference, uncertainty, question logging, language mediation, and shared context.
- **Prospective validation claim:** v0.2.2 is designed for human external-coder testing of whether revisions improve usability and comparison. Not yet supported by outcomes.

## One Paper Or Two?

Do **not** split the current project into two papers now.

The default publication plan should be one integrated methods article:

1. final-label compression problem;
2. TRIM architecture;
3. v0.2.0 diagnostic usability pilot;
4. pilot failure modes;
5. prospective v0.2.1 source-text revision;
6. v0.2.1 AI protocol dry run;
7. v0.2.2 minimal pre-human-deployment patch;
8. out-of-sample human v0.2.2 retest;
9. pathway-level and field-level comparison;
10. limitations and future validation.

A pre-retest "Paper 1" would probably look like an incomplete methods note because the strongest empirical promise is already embodied in the corrected v0.2.2 retest package. The first pilot and AI dry run alone are insufficient for the preferred full methods article.

A later second paper may be justified if it adds new empirical scope: larger multi-coder validation, another interpretive domain, another function vocabulary, a memo-only comparison, direct-source cross-language replication, or larger-scale generalization.

Submission readiness: draft now; submit after the human v0.2.2 retest. The corrected source-text package and AI dry run improve methodological defensibility, but they do not themselves supply human retest findings.

## Final Recommendation

1. **Strongest paper TRIM can become:** a DH methods article on reviewable interpretive annotation through evidence-to-function pathways.
2. **What it should not be:** not a reliability triumph, not a universal hermeneutic framework, not a software-first paper, not a substantive literary interpretation article.
3. **Target first:** depends on retest outcome. If results are theoretically interesting, start with Journal of Computational Literary Studies. If results mainly show method refinement and infrastructure, start with Digital Humanities Quarterly.
4. **Most realistic target:** Digital Humanities Quarterly or Digital Studies / Le champ numérique.
5. **Is the first pilot enough for submission?** No for the preferred integrated methods article. It is enough to begin drafting, not enough to submit.
6. **Must human v0.2.2 retest be completed?** Yes for best submission odds; especially for JCLS, DSH, JCA, or any methods journal.
7. **Should a memo-only comparison be added?** Not required for Paper 1, but valuable for Paper 2 if feasible.
8. **Should the software be released before submission?** Yes. Make a tagged release, archive on Zenodo if possible, and cite exact commit/DOI.
9. **Three biggest publication risks:** pilot too small; method looks over-engineered; novelty challenged by qualitative coding, argumentation annotation, and provenance/annotation tooling.
10. **Exact next work:** use the corrected v0.2.2 package with external coders; complete the human retest; run field-specific and evidence-overlap analyses; finalize claim matrix; prepare two contrasting opening examples; release code/data; then submit one integrated methods article.
