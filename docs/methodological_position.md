# Methodological Position

## TRIM as Structured Interpretive Annotation

TRIM sits between close reading, qualitative coding, graph modelling, and
intercoder review. It begins from human interpretive work and gives selected
judgements a structured form that can be inspected, compared, exported, and
revisited. The package is designed for digital humanities projects in which the
evidence is textual and the target of analysis is a narrative or discursive
function rather than a surface feature alone.

TRIM annotation records how a coder moves from evidence to function. The method
asks coders to identify evidence nodes, an anchor node, a threshold-rationale
relation, and a function label. The resulting record is not a replacement for
close reading; it is a disciplined representation of a reading that can be
validated for form, compared across cases, and reviewed by other coders.

TRIM's defensible contribution is specific: it makes the warranted conversion
from textual evidence to interpretive function an explicit, locatable,
reviewable, and comparable annotation object.

## Core Distinction

TRIM distinguishes surface evidence from narrative function. A passage may
contain prophecy, divination, testimony, report, recognition, confession, or
commentary, but the presence of such evidence does not by itself determine what
function the passage has in a particular annotation. The threshold-rationale
relation records the conversion from evidence to function: the locus of
friction, the mechanism of conversion, the epistemic support used by the coder,
the discourse level, the temporal orientation, and the uncertainty flag.

This distinction supports comparative analysis. Two cases can share a function
while differing in signature. Two cases can share a cue family while producing
different functions. A broad family can hold together while individual cases
show different threshold-rationale paths. TRIM makes these patterns explicit in
tables and graph outputs.

## What the Package Operationalizes

The package operationalizes the following method components:

- controlled annotation fields;
- evidence-to-function signatures;
- comparison patterns;
- graph representations;
- contested-threshold documentation;
- intercoder comparison preparation.

Controlled vocabulary validation checks whether selected fields conform to the
codebook. Signature parsing gives each annotation a compact representation of
its threshold-rationale path. Comparison utilities generate structural tables
for same-function, same-cue, broad-family, and contested-case patterns.
Graph export represents each annotation as a path from evidence nodes to anchor
node to threshold-rationale relation to function node, with threshold
attributes also available on a direct anchor-to-function edge.

Contested thresholds are recorded through `alternative_signature` and
`rationale_note`. This supports a review workflow in which alternative readings
remain visible and can be discussed by human coders or reviewers. Intercoder
utilities prepare multi-coder data for field-level comparison, disagreement
tables, and later reliability evaluation.

## Relation to Close Reading

TRIM begins from close reading. Coders identify relevant passages, create
evidence nodes, decide where the anchor lies, assign controlled fields, and
write rationale notes. The method preserves rationale prose alongside
structured fields so that interpretation remains inspectable rather than
flattened into a label alone.

Interpretive friction is a locatable difficulty in the warranted conversion
from textual evidence to an analytic function under an explicit interpretive
scheme. It is relational, not a context-free property naturally embedded in a
text. It arises through the relation among textual evidence, the analytic task,
the project's function vocabulary, and the coder's stated rationale. This
formulation keeps friction evidence-constrained and operational: coders must
locate the obstacle, identify the support used to cross it, and leave a
reviewable rationale.

The optional source segmentation workflow strengthens the link to close
reading. Source passages can be segmented into stable units before annotation,
allowing coders and reviewers to cite the same textual anchors when discussing
agreement, disagreement, or contested thresholds.

## Relation to DH Method

As a digital humanities method package, TRIM treats interpretive thresholds as
structured data while preserving the reviewable character of scholarly
judgement. It supports reproducible workflow steps: source segmentation,
annotation, validation, comparison, reporting, graph export, and intercoder
preparation. Its outputs can be read as tables, reports, or graph data, making
the same interpretive annotations available to different forms of analysis.

The method is especially suited to projects where recurring narrative cues do
not map directly onto stable functions. TRIM gives researchers a way to record
the rationale by which a cue becomes functional in context, then compare those
rationales across a corpus.

## Conceptual Neighbours

TRIM does not claim as novel the general observation that annotators can agree
on a label while offering different explanations. It also does not primarily
classify free-text explanations by reasoning type or capture hidden cognitive
processes. See [`related_methods.md`](related_methods.md) for positioning
against within-label variation, LiveNLI, LiTEx, qualitative coding, provenance
systems, and computational hermeneutics.
