# Related Methods and Conceptual Neighbours

TRIM builds on a general observation already established in neighbouring work:
label agreement does not imply explanatory agreement. TRIM does not claim that
observation as novel. Its narrower contribution is to make the warranted
conversion from textual evidence to interpretive function an explicit,
locatable, reviewable, and comparable annotation object.

## Within-Label Variation, LiveNLI, and LiTEx

LiveNLI demonstrates that annotators can select the same natural-language
inference label while giving different reasons. LiTEx then develops a linguistic
taxonomy for categorizing free-text explanations and analysing within-label
variation. TRIM is adjacent to this work but does not primarily classify
free-text explanations by linguistic reasoning type.

TRIM instead models a human-coded evidence-to-function pathway. Its comparative
object combines:

- evidence nodes;
- an anchor node;
- a threshold-rationale relation;
- `friction_locus`;
- `rationale_mechanism`;
- `epistemic_support`;
- discourse and temporal position;
- uncertainty;
- optional alternative pathways.

The resulting signature can show where two scholarly interpretations share a
function label but differ in the warranted route used to sustain it.

## Qualitative Coding and Computational Grounded Theory

TRIM shares qualitative coding's dependence on explicit codebooks, coder
judgement, rationale notes, independent coding, and adjudication. It adds a
specific graphable architecture for evidence-to-function conversion and
controlled fields for locating and comparing the conversion threshold. It does
not replace project-specific function vocabularies or interpretive judgement.

Computational grounded theory structures a staged workflow that combines
computational exploration and modelling with human interpretation. TRIM's unit
of structure is narrower: the interpretive conversion itself, recorded as a
reviewable annotation pathway rather than inferred from a model output.

## Provenance and Reasoning-Trace Systems

TRIM has a provenance-like concern with making evidential support and
transformation steps inspectable. Its records are deliberate scholarly
annotations, however, not measurements of hidden cognition. TRIM does not claim
to capture a coder's full reasoning process, and it is not an LLM
chain-of-thought or automated reasoning-trace system.

## Computational Hermeneutics and Interpretable Outputs

TRIM belongs near computational hermeneutics and computational close reading
because it preserves human interpretation while making selected relations
available for validation, comparison, tables, and graph export. Mohr,
Wagner-Pacifici, and Breiger describe computational hermeneutics as an
alternative to forms of content analysis that primarily extract and map a
text's main meanings. Rockwell and Sinclair likewise theorize text analysis as
computer-assisted interpretive practice rather than automated interpretation.

TRIM's distinctive focus is the warranted conversion from textual evidence to a
project-defined interpretive function, not context-free detection of friction in
texts. The repository does not claim that TRIM directly operationalizes a
specific "breakdown" concept from *Hermeneutica*: that stronger genealogy would
require passage-level textual evidence.

Dobson's criteria for interpretable outputs are especially close to TRIM's claim
boundary. He argues that text-derived features should remain visible and that
computational claims must be assessable as warranted by evidence within an
interpretive community. TRIM addresses a related problem at the annotation
level by preserving the evidence, anchor, conversion fields, uncertainty, and
alternative path used to support an interpretive function.

Kleymann and Stange's hermeneutic visualization similarly treats interfaces and
visualizations as sites where digital methods must preserve the epistemological
demands of literary interpretation. TRIM is complementary rather than
identical: it structures the annotation pathway that tables and graphs later
render.

## Graph-Based Classical-Text Digital Humanities

Graphilosophy is a recent and close subject-domain neighbour. It uses an
ontology-guided, multilayer knowledge graph, multilingual semantic
representations, and humanistic analysis to model linguistic, conceptual, and
interpretive relationships in *The Four Books*. It also explicitly aims to
preserve scholarly nuance and interpretive plurality.

TRIM differs in its primary graph object. Graphilosophy models relationships
within and across a classical-text knowledge resource; TRIM models how a human
coder converts selected textual evidence into a project-defined interpretive
function and records where that conversion requires its dominant warrant. The
current comparison is based on Graphilosophy's 2026 preprint and should be
revisited if a substantially revised journal version appears.

## Verified References

- Dobson, James. 2021. "Interpretable Outputs: Criteria for Machine Learning in
  the Humanities." *Digital Humanities Quarterly* 15 (2), article 000555.
  https://www.digitalhumanities.org/dhq/vol/15/2/000555/000555.html
- Do, Minh-Thu, Quynh-Chau Le-Tran, Duc-Duy Nguyen-Mai, Thien-Trang Nguyen,
  Khanh-Duy Le, Minh-Triet Tran, Tam V. Nguyen, and Trung-Nghia Le. 2026.
  "Graphilosophy: Graph-Based Digital Humanities Computing with The Four
  Books." arXiv:2603.28755. https://doi.org/10.48550/arXiv.2603.28755
- Hong, Pingjun, Beiduo Chen, Siyao Peng, Marie-Catherine de Marneffe, and
  Barbara Plank. 2025. "LiTEx: A Linguistic Taxonomy of Explanations for
  Understanding Within-Label Variation in Natural Language Inference."
  arXiv:2505.22848. Accepted to the EMNLP 2025 main conference.
  https://doi.org/10.48550/arXiv.2505.22848
- Jiang, Nan-Jiang, Chenhao Tan, and Marie-Catherine de Marneffe. 2023.
  "Ecologically Valid Explanations for Label Variation in NLI."
  arXiv:2310.13850. Findings of EMNLP 2023.
  https://doi.org/10.48550/arXiv.2310.13850
- Kleymann, Rabea, and Jan-Erik Stange. 2021. "Towards Hermeneutic
  Visualization in Digital Literary Studies." *Digital Humanities Quarterly*
  15 (2), article 000547.
  https://www.digitalhumanities.org/dhq/vol/15/2/000547/000547.html
- Mohr, John W., Robin Wagner-Pacifici, and Ronald L. Breiger. 2015. "Toward a
  Computational Hermeneutics." *Big Data & Society*. First published online
  December 1, 2015. https://doi.org/10.1177/2053951715613809
- Nelson, Laura K. 2020. "Computational Grounded Theory: A Methodological
  Framework." *Sociological Methods & Research* 49 (1): 3-42.
  https://doi.org/10.1177/0049124117729703
- Rockwell, Geoffrey, and Stéfan Sinclair. 2016. *Hermeneutica:
  Computer-Assisted Interpretation in the Humanities*. Cambridge, MA: The MIT
  Press. Hardcover ISBN 9780262034357.

## Deliberate Exclusions

- No Baumer et al. 2017 entry is included because the previously suggested work
  has not been identified with enough precision to verify its relevance.
- No claim is made that Rockwell and Sinclair's use of "breakdown" is the direct
  philosophical source of TRIM's `friction_locus`; that claim remains
  unsupported without an exact passage and contextual reading.
- Proceedings pagination for LiveNLI and LiTEx should be substituted for the
  arXiv citations only after the corresponding anthology records are available
  and verified.
