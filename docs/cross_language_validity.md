# Cross-Language Construct Validity

## Problem

TRIM compares evidence-to-function conversions across languages and traditions. A translation or project-authored gloss can preserve, soften, introduce, or relocate the point at which that conversion becomes difficult. The resulting question concerns construct validity: whether `friction_locus` records the interpretive structure of the source passage or an effect of linguistic mediation.

The core signature remains tied to the textual layer on which coding occurred. Translation-mediated differences are recorded as provenance and cross-layer validity evidence.

## Two Analytic Layers

TRIM distinguishes:

- **authoritative layer**: the source-language text used to adjudicate the primary annotation;
- **access layer**: a gloss or translation used to make the case available to a coder who does not work directly in the source language.

For multilingual cases, the primary claim about `friction_locus` is anchored in the source-language layer and reviewed by a coder competent in that language. Access-layer coding evaluates whether the mediated version preserves the same interpretive threshold.

## Companion Provenance Fields

Cross-layer validity is recorded outside the six-field TRIM signature.

- `source_language`: language of the authoritative source text;
- `coding_layer`: `original` or `gloss`;
- `mediation_source`: `original_text`, `researcher_gloss`, or `published_translation`;
- `paired_record_id`: identifier linking original- and gloss-layer annotations for the same case;
- `cross_layer_relation`: `not_assessed`, `aligned`, `softened`, `introduced`, or `relocated`;
- `original_locus`: locus assigned from the source-language layer;
- `gloss_locus`: locus assigned from the mediated layer;
- `cross_layer_note`: concise account of the linguistic feature or reformulation associated with the result.

These fields describe the provenance and relation of two annotations. They remain separate from `friction_locus` because translational mediation is a relation between textual layers, while `friction_locus` describes the evidence-to-function conversion within one layer.

## Controlled Relations

- `not_assessed`: only one textual layer has been coded;
- `aligned`: both layers produce the same dominant locus;
- `softened`: a source-layer friction becomes less visible or disappears in the gloss;
- `introduced`: the gloss produces a friction absent from the source-layer reading;
- `relocated`: both layers remain interpretable, but the dominant locus moves from one TRIM value to another.

A relocated case records both values in `original_locus` and `gloss_locus`; the relation field itself remains categorical.

## Optional Double-Layer Check

For each Classical Chinese pilot case:

1. a source-language-competent coder completes an annotation from the original text;
2. a coder completes a separate annotation from the English close paraphrase without seeing the source-layer annotation;
3. both records are preserved before comparison;
4. the comparison records locus agreement, mechanism agreement, and `cross_layer_relation`;
5. any relocation is examined at the level of syntax, explicitness, temporal marking, agency, warrant relation, and other features changed by mediation.

This check produces construct-validity evidence. Alignment supports friction preservation across layers. Divergence identifies the direction and type of mediation effect.

## Claim Scale

The current ten-case packet includes both original Classical Chinese and project-authored close paraphrases. Until double-layer coding is completed, the paraphrases provide access and the source-language readings provide the basis for substantive claims about the Chinese cases.

Cross-layer divergence would qualify the multilingual comparison and become a result in its own right. It would not retroactively become a new `friction_locus` value or an uncertainty category.

## Relation to Adjacent Methods

Cross-lingual annotation projection often assumes meaning-preserving translation and then evaluates or corrects projected annotations against target-language evidence. Research on fine-grained cross-lingual semantic divergence likewise treats differences between aligned language versions as observable annotation targets. TRIM adapts this general principle to interpretive annotation by comparing the location of evidence-to-function friction across original and mediated layers.

Qualitative translation research adds a second methodological anchor. Helmich et al. show that grammar, syntax, metaphor, and sociolinguistic nuance can alter qualitative interpretation; they recommend transparent translation strategies and discuss source-oriented “ugly” translations that preserve visible difference. Zhao et al. argue that uncertainty and difference between original and translated texts can contribute to validity when they are made explicit and reflexively analysed, rather than treated only as defects to be eliminated.

Relevant verified starting points include:

- Abzianidze, Lasha, et al. 2017. “The Parallel Meaning Bank: Towards a Multilingual Corpus of Translations Annotated with Compositional Meaning Representations.” arXiv:1702.03964.
- Briakou, Eleftheria, and Marine Carpuat. 2020. “Detecting Fine-Grained Cross-Lingual Semantic Divergences without Supervision by Learning to Rank.” arXiv:2010.03662.
- Helmich, Esther, Sayra Cristancho, Laura Diachun, and Lorelei Lingard. 2017. “‘How Would You Call This in English?’: Being Reflective about Translations in International, Cross-Cultural Qualitative Research.” *Perspectives on Medical Education* 6 (2): 127–132. https://doi.org/10.1007/s40037-017-0329-1
- Zhao, Pengfei, Wen Qi, Pei-Jung Li, and Peiwei Li. 2024. “Reconceptualizing the Link Between Validity and Translation in Qualitative Research: Extending the Conversation Beyond Equivalence.” *International Journal of Qualitative Methods* 23. https://doi.org/10.1177/16094069241260134

Catford's concept of translation shift and van Leuven-Zwart's comparative model remain plausible additional anchors. Their direct application to friction-locus relocation is an inference developed by TRIM and should be introduced only after the exact bibliographic records and relevant passages have been checked.
