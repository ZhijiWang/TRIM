# Cross-Language Construct Validity

## Problem

TRIM compares evidence-to-function conversions across languages and traditions. A translation or project-authored gloss can preserve, soften, introduce, or relocate the point at which that conversion becomes difficult. The resulting question concerns construct validity: whether `friction_locus` records the interpretive structure of the source passage or an effect of linguistic mediation.

The core signature remains tied to the textual layer on which coding occurred. Translation-mediated differences are recorded as provenance and cross-layer validity evidence outside the canonical six-field signature.

## Two Analytic Layers

TRIM distinguishes:

- **authoritative layer**: the source-language text used to adjudicate the primary annotation;
- **access layer**: a gloss or translation used to make the case available to a coder who does not work directly in the source language.

The source-language layer is authoritative because it avoids an additional translation step. It remains a human scholarly interpretation, not absolute ground truth. Access-layer coding evaluates whether a mediated version preserves the same interpretive threshold.

## Normalized Companion Tables

Cross-language validity uses two companion templates:

- `data/cross_language_layer_annotations_template.csv`;
- `data/cross_language_pair_comparisons_template.csv`.

The layer-level table records one annotation for one textual layer. The pair-level table records one comparison between a locked original-layer record and a locked gloss-layer record. Keeping these tables separate prevents annotation values and comparison outcomes from silently overwriting one another.

## Layer-Level Annotation Table

Each row in `data/cross_language_layer_annotations_template.csv` represents one textual layer.

Required columns:

- `record_id`: stable identifier for the layer-level annotation;
- `case_id`: case shared with the canonical dataset;
- `paired_record_id`: pair identifier shared by the original and gloss rows;
- `source_language`: language of the authoritative source text;
- `coding_layer`: `original` or `gloss`;
- `mediation_source`: `original_text`, `researcher_gloss`, or `published_translation`;
- `canonical_record_id`: canonical annotation identifier for original-layer rows where applicable;
- `friction_locus`: layer-level `friction_locus`, filled only when that layer has been coded;
- `rationale_mechanism`: layer-level `rationale_mechanism`, filled only when that layer has been coded;
- `coder_id`: coder responsible for the layer record;
- `status`: `planned`, `in_progress`, `locked`, or `adjudicated`;
- `note`: brief provenance or coding note.

Original and gloss rows share `paired_record_id`. Gloss-layer rows may leave `canonical_record_id` blank. Pair-level comparison outcomes do not belong in this table.

## Pair-Level Comparison Table

Each row in `data/cross_language_pair_comparisons_template.csv` represents one original–gloss pair.

Required columns:

- `paired_record_id`: pair identifier linking the two layer rows;
- `case_id`: case shared with both layer records;
- `original_record_id`: locked source-layer record;
- `gloss_record_id`: locked access-layer record;
- `original_locus`: copied from the locked original-layer record;
- `gloss_locus`: copied from the locked gloss-layer record;
- `original_mechanism`: copied from the locked original-layer record;
- `gloss_mechanism`: copied from the locked gloss-layer record;
- `cross_layer_relation`: `not_assessed`, `aligned`, `softened`, `introduced`, or `relocated`;
- `cross_layer_note`: concise account of the linguistic feature or reformulation associated with the result;
- `comparison_status`: `planned`, `ready`, `compared`, or `adjudicated`;
- `adjudicator_id`: reviewer responsible for the pair-level comparison.

No independent coding is performed in the pair-level table. Values are copied or joined only from locked layer records. A relocated case records `relocated` as the categorical relation and preserves the actual movement in `original_locus` and `gloss_locus`. Mechanism differences remain visible through `original_mechanism` and `gloss_mechanism`.

## Source of Truth and Data Flow

1. Existing canonical original-layer TRIM annotations remain authoritative in the canonical annotation dataset.
2. The layer-level companion table references those records through `canonical_record_id`.
3. The companion table does not silently override canonical original-layer values.
4. Gloss-layer annotations are new analytical records and use the layer-level companion table as their source of truth.
5. Pair-level comparisons are derived only after both layer records are locked.
6. The pair-level comparison table is not an independent annotation source.
7. Any correction to an original-layer value must first occur in the canonical dataset, then propagate to the companion comparison.
8. Any correction to a gloss-layer value must first occur in the layer-level companion table.
9. Pair-level results may be regenerated from the two locked layer records.

## Controlled Relations

- `not_assessed`: only one textual layer has been coded, or the pair has not yet been compared;
- `aligned`: both layers produce the same dominant locus;
- `softened`: a source-layer friction becomes less visible or disappears in the gloss;
- `introduced`: the gloss produces a friction absent from the source-layer reading;
- `relocated`: both layers remain interpretable, but the dominant locus moves from one TRIM value to another.

## Optional Double-Layer Check

For each Classical Chinese pilot case:

1. a source-language-competent coder completes or confirms the original-layer record;
2. a coder completes a separate gloss-layer record from the English close paraphrase without seeing the source-layer result;
3. both layer records are locked;
4. the pair-level row is created or moved to `ready`;
5. the comparison copies `friction_locus` and `rationale_mechanism` from the locked layer records;
6. the adjudicator assigns `cross_layer_relation`;
7. any relocation is examined at the level of syntax, explicitness, temporal marking, agency, warrant relation, and other features changed by mediation.

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
