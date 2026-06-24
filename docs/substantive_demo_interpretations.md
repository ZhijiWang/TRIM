# Substantive Demonstration Interpretations

TRIM's comparison software generates structural observations and prompts. The
interpretations below are researcher-authored worked demonstrations based on the
checked fields in `data/demo_annotations.csv`. They show what becomes visible
when signatures are compared across cases rather than read as isolated labels.

The current examples are provisional, single-coder comparisons. Their purpose is
to establish comparative payoff and identify concrete propositions for later
reliability testing.

## Generated and Curated Layers

The generated same-function table reports:

> Shared function label; differing threshold-rationale signatures. Interpret
> the substantive significance of the differing evidence-to-function pathways.

The table column is named `comparison_prompt`. Before package version 0.2.0,
the same structural text appeared under the misleading column name
`interpretive_payoff`. Consumers should migrate to `comparison_prompt`.

The following prose is a separate human-curated layer. Each demonstration keeps
four elements visible: checked annotations, evidence basis, worked
interpretation, and the boundary of the present claim.

## 1. Locus Migration within *Macbeth*

### Checked annotations

| Case | Function label | Friction locus | Rationale mechanism | Temporal orientation | Uncertainty |
|---|---|---|---|---|---|
| `MAC_1_3` | `ambition_trigger_authorization` | `warrant_attribution` | `authorizes+reframes` | `prospective` | `medium` |
| `MAC_4_1` | `false_security` | `operation_function` | `reframes+narrows` | `prospective-retrospective` | `low` |
| `MAC_5_8` | `retrospective_trap` | `temporal_layering` | `reframes` | `retrospective` | `low` |

### Evidence basis

In Act 1.3, the witches' salutation acquires practical force through partial
confirmation: Ross and Angus verify Macbeth's new title as Thane of Cawdor. The
interpretive threshold therefore lies in warrant attribution. Confirmation gives
the prophecy enough authority to reframe kingship as an actionable possibility.

In Act 4.1, the apparitions present conditional and equivocal claims. Macbeth
converts those claims into operational security by narrowing their possible
meanings. The interpretive pressure shifts from whether the prophecy deserves
authority to how its conditions are made to function in decision-making.

In Act 5.8, Macduff's disclosure retrospectively reorganizes Macbeth's earlier
assurance. The dominant threshold lies in temporal layering because later
fulfilment changes the status of the prior interpretation, revealing confidence
as a product of equivocation.

### Worked interpretation

TRIM shows that prophecy does not carry one stable interpretive difficulty
throughout the play. The dominant threshold migrates with the dramatic
sequence. It begins with the acquisition of warrant, moves into the operational
use of equivocal language, and ends in retrospective reclassification.

This migration matters because a cue-family analysis would group all three
scenes under prophecy, while a function-label analysis would separate them by
outcome. The TRIM comparison adds a third view: it tracks where interpretive
effort is concentrated at each stage of the same prophetic apparatus.

The sequence can be summarized as:

> warrant acquisition → operational narrowing → retrospective reclassification

The result is a within-text demonstration of schema expressivity. A single
dramatic device changes its dominant friction locus as its narrative role
develops.

### Demonstration boundary

This comparison supports locus migration as a structured reading of the three
annotated scenes. A blinded second-coder pilot can test whether independent
coders reproduce the same sequence and whether disagreement concentrates in
locus assignment, evidence selection, or mechanism.

## 2. Shared Locus, Divergent Epistemic Trajectories

### Checked annotations

| Case | Source | Function label | Friction locus | Rationale mechanism | Temporal orientation | Uncertainty |
|---|---|---|---|---|---|---|
| `ZZ_XI_4` | *Zuo zhuan* | `extended_deliberation` | `warrant_relation` | `extends` | `recursive` | `medium` |
| `GROVE_TAKEHIRO` | *In a Grove* | `epistemic_suspension` | `warrant_relation` | `contradicts+suspends` | `retrospective` | `high` |

### Evidence basis

In `ZZ_XI_4`, the turtle-shell and milfoil results conflict. Their disagreement
is intensified by ranking speech and ominous textual material. No single warrant
closes the matter cleanly, so the relation among warrants becomes the principal
site of interpretive pressure. The conflict extends deliberation and keeps
judgement narratively active.

In `GROVE_TAKEHIRO`, Takehiro's posthumous testimony enters an already
incompatible testimonial field. Its extraordinary status does not resolve the
preceding accounts. It adds another warrant that contradicts them and deepens
the difficulty of adjudication.

### Worked interpretation

These cases share the same dominant locus while producing different epistemic
trajectories. In both, the central difficulty lies in the relation among
competing warrants rather than in the isolated content of any one statement.

The consequences diverge:

- in `ZZ_XI_4`, warrant conflict remains productive and extends judgement;
- in `GROVE_TAKEHIRO`, warrant conflict suspends closure and raises uncertainty.

This comparison shows why `friction_locus` and `rationale_mechanism` remain
separate dimensions. A shared locus identifies the structural point at which
interpretation is under pressure; the mechanism records what that pressure does.

The comparison therefore supports the proposition:

> the same locus of friction can organize different epistemic trajectories.

### Demonstration boundary

The current annotations establish a focused comparative hypothesis. The key
reliability question is whether an independent coder also identifies
`warrant_relation` as dominant in both cases while distinguishing `extends` from
`contradicts+suspends`.

## 3. Shared Threshold across Traditions, Divergent Conversion

### Checked annotations

| Case | Source | Cue family | Function label | Friction locus | Rationale mechanism | Temporal orientation | Uncertainty |
|---|---|---|---|---|---|---|---|
| `ZZ_MIN_1` | *Zuo zhuan* | `divination` | `immediate_stabilization` | `warrant_attribution` | `stabilizes+projects` | `prospective` | `medium` |
| `MAC_1_3` | *Macbeth* | `prophecy` | `ambition_trigger_authorization` | `warrant_attribution` | `authorizes+reframes` | `prospective` | `medium` |

### Evidence basis

In `ZZ_MIN_1`, the Yi-related result is accepted through Xin Liao's
interpretation as a stable prospective judgement about lineage. The sign becomes
consequential when interpretive authority is attached to it and its implications
are projected forward.

In `MAC_1_3`, the witches' words gain practical authority through partial
confirmation. The confirmation reframes future kingship as a possibility to
which Macbeth can orient action.

### Worked interpretation

The cases differ in tradition, genre, cue family, function label, and narrative
consequence. Yet both place the dominant threshold at warrant attribution and
both orient that threshold prospectively.

In both cases, the consequential threshold lies where warranting force enables
the prospective claim to shape interpretation and action.

The conversion pathways then separate:

- `ZZ_MIN_1` stabilizes and projects a lineage judgement;
- `MAC_1_3` authorizes and reframes kingship as an actionable possibility.

TRIM therefore reveals a shared threshold location while preserving divergent
mechanisms and outcomes. This is the value of cross-traditional comparison at
the signature level: cases can converge structurally while retaining their
cultural and functional specificity.

### Demonstration boundary

The comparison supports the formulation **shared threshold, divergent
conversion**. The strongest next test is independent reproduction of the
`warrant_attribution` assignment in both cases together with preservation of the
different mechanisms.

## 4. Existing Same-Function Demonstrations

### `immediate_stabilization`

#### Checked annotations

- `ZZ_XIANG_7` — `operation_function / stabilizes /
  textual_anchor+ritual_sequence / intradiegetic / immediate / low`
- `ZZ_MIN_1` — `warrant_attribution / stabilizes+projects /
  textual_anchor+internal_sequence / intradiegetic / prospective / medium`

#### Worked interpretation

The shared function of stabilization is produced through different authority
structures. In Xiang 7, Meng Xianzi's interpretation restores ritual sequence,
converting failed divination into procedural intelligibility. In Min 1, Xin
Liao's interpretation grants the Yi-related result warranting force and projects
that force into prospective lineage significance. The shared function label
therefore contains a distinction between procedural stabilization and
warrant-bearing, future-oriented stabilization.

### `extended_deliberation`

#### Checked annotations

- `ZZ_XI_4` — `warrant_relation / extends /
  textual_anchor+internal_sequence / intradiegetic / recursive / medium`
- `ZZ_ZHUANG_22` — `temporal_layering / extends+projects /
  textual_anchor+internal_sequence / commentarial_discourse /
  prospective-retrospective / medium`

#### Worked interpretation

Extension arises through two different structures. In Xi 4, unresolved
relations among turtle result, milfoil result, ranking speech, and line text
delay closure within the warrant field. In Zhuang 22, projected descent and
later historical readability keep the sign available across temporal and
commentarial layers. The first pathway extends deliberation horizontally through
competing warrants; the second extends significance vertically through
projection and later uptake.

## Comparative Payoff

Taken together, the demonstrations establish a layered case for TRIM's
usefulness.

First, the *Macbeth* sequence shows differentiation within one text and one cue
family. Second, `ZZ_XI_4 × GROVE_TAKEHIRO` shows that a shared locus can produce
divergent epistemic trajectories. Third, `ZZ_MIN_1 × MAC_1_3` shows that distant
traditions can converge at the threshold level while retaining distinct
mechanisms and consequences.

The progression is:

> within-text differentiation → shared locus with divergent outcomes →
> cross-traditional threshold convergence

This progression clarifies what the signature contributes beyond labels. TRIM
creates a comparative object in which evidence, anchor, friction locus,
mechanism, support, discourse position, temporality, uncertainty, and
alternatives can be read together.

The present demonstrations also provide the substantive basis for the next
validation stage. A blinded pilot can test three concrete propositions:

1. independent coders reproduce the locus migration across the three *Macbeth*
   scenes;
2. independent coders identify `warrant_relation` in both `ZZ_XI_4` and
   `GROVE_TAKEHIRO` while preserving their different mechanisms;
3. independent coders identify `warrant_attribution` in both `ZZ_MIN_1` and
   `MAC_1_3` while preserving their different conversion pathways.

These tests connect reliability directly to the comparative findings the method
is designed to produce.

## Demonstration Boundary

These readings show what a researcher can do after structural differences have
been located. The software supports retrieval and comparison; the researcher
remains responsible for substantive interpretation, textual adequacy, and the
scope of each claim.
