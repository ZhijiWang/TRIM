# TRIM Coding Manual v0.2: `friction_locus`

## Purpose

Use `friction_locus` to mark where the main threshold problem lies in a human
annotation. This field records the coder's judgement about which part of the
evidence-to-function path most needs the threshold-rationale explanation.

Interpretive friction is a locatable difficulty in the warranted conversion
from textual evidence to an analytic function under an explicit interpretive
scheme. It is not a context-free property embedded in a passage. It arises
through the relation among textual evidence, the analytic task, the project's
function vocabulary, and the coder's stated rationale.

Each annotation receives one `friction_locus`. The value records the dominant
threshold that most directly explains evidence-to-function conversion.
Secondary difficulties go in `rationale_note` or `alternative_signature`.

Allowed values:

- `cue_function`
- `warrant_attribution`
- `warrant_relation`
- `operation_function`
- `boundary_setting`
- `temporal_layering`
- `perspective_assignment`
- `context_inference`

The current demo annotations contain positive coded examples for five of the
eight values. `boundary_setting` and `context_inference` are operational but
await positive out-of-sample testing. `cue_function` is a provisional reserved
value. For values without a positive demo example, use the documented contrast
as a boundary marker rather than as positive evidence.

Current examples are in-sample training examples from the demo annotations.
Out-of-sample coding is required for actual reliability testing.

## `cue_function`

### Definition

Use `cue_function` when the main friction is the function of the cue type
itself: what kind of work a cue such as divination, prophecy, or testimony is
doing in the annotation.

Status: provisional reserved value. It should not be treated as empirically
established in reliability reporting until supported by positive out-of-sample
cases and a stable decision rule. It has no positive demo example.

### Use when

- The cue type is the main source of uncertainty.
- The coder is deciding how the cue family functions in the case.
- No more specific locus explains the evidence-to-function conversion.
- Project-lead review has confirmed that `cue_function` best describes the
  dominant threshold after considering `operation_function`,
  `warrant_attribution`, `warrant_relation`, `temporal_layering`,
  `perspective_assignment`, `boundary_setting`, and `context_inference`.

### Use another value when

- A visible operation converts the cue into a function. Use
  `operation_function`.
- One source or medium receives authority. Use `warrant_attribution`.
- Multiple warrants interact, conflict, rank, qualify, or suspend one another.
  Use `warrant_relation`.
- The main point is that the same cue family supports different functions across
  cases. That is a comparison result rather than a single-row
  `friction_locus`.
- A more specific locus explains the conversion without needing this reserved
  value.

### Positive example from existing demo cases

No current demo annotation is coded as `cue_function`.

Contrast: the Macbeth prophecy cases share the cue family `prophecy`, but their
individual demo annotations are coded as `warrant_attribution`,
`operation_function`, and `temporal_layering`. Code them as `cue_function` only
when the cue type itself is the dominant threshold problem for the annotation
and project-lead review confirms that no more specific locus fits.

### Confusable with

- `operation_function`
- `warrant_attribution`

### Decision tip

Ask whether the problem is "what does this cue type do here?" If yes, consider
`cue_function` only after excluding the more specific loci and obtaining
project-lead review. If the problem is "what does this act of interpretation,
consultation, confession, recognition, or self-reading do?", use
`operation_function`.

## `warrant_attribution`

### Definition

Use `warrant_attribution` when one source, sign, medium, speaker, or result
receives warranting force.

### Use when

- A single source or medium is treated as authoritative enough to support the
  function label.
- The threshold problem is whether that source should carry warrant.
- The annotation turns on attribution of authority rather than on conflict among
  multiple warrants.

### Use another value when

- Multiple warrants interact, conflict, rank, qualify, or suspend one another.
  Use `warrant_relation`.
- The main issue is what a visible operation does. Use `operation_function`.
- The main issue is later fulfilment, retrospective readability, or reuse across
  time layers. Use `temporal_layering`.

### Positive example from existing demo cases

Min 1, 畢萬筮仕於晉: the milfoil/Yi-related result receives warranting force
through Xin Liao's auspicious interpretation. The demo annotation uses
`warrant_attribution`.

Macbeth Act 1.3: partial confirmation by Ross and Angus gives the witches'
prophecy warranting force. The demo annotation uses `warrant_attribution`.

### Confusable with

- `warrant_relation`
- `operation_function`

### Decision tip

If the main question is "which source is being granted authority?", use
`warrant_attribution`. If the main question is "how do multiple warrants relate
to one another?", use `warrant_relation`.

## `warrant_relation`

### Definition

Use `warrant_relation` when the main friction lies in the relation among two or
more warrants.

### Use when

- Multiple warrants interact.
- Warrants conflict, rank, qualify, suspend, or contradict one another.
- No single warrant source is enough to explain the function.

### Use another value when

- One source simply receives authority. Use `warrant_attribution`.
- The main issue is a visible operation converting into function. Use
  `operation_function`.
- The main issue is a later time layer changing the earlier sign's function.
  Use `temporal_layering`.
- The main issue is whose perspective or testimonial position controls the
  annotation. Use `perspective_assignment`.

### Positive example from existing demo cases

Xi 4, 初，晉獻公欲以驪姬為夫人：卜筮相違: turtle result, milfoil result, ranking
speech, and line text interact. The retrospective frame is a meaningful
secondary observation, while cross-warrant conflict is dominant. The demo
annotation uses `warrant_relation`.

Takehiro's posthumous testimony: the posthumous testimony introduces an
extraordinary warrant that contradicts rather than resolves preceding accounts.
The demo annotation uses `warrant_relation`.

### Confusable with

- `warrant_attribution`
- `temporal_layering`
- `perspective_assignment`

### Decision tip

Count the warrants. If the annotation depends on how more than one warrant
interacts, use `warrant_relation`. If there is one main source receiving
authority, use `warrant_attribution`.

## `operation_function`

### Definition

Use `operation_function` when a visible operation is converted into the
function. Operations include interpretation, confession, consultation,
recognition, or self-reading.

Treat fulfilment as an operation only when the coding focuses on the act of
treating fulfilment operationally. When later fulfilment reclassifies earlier
evidence, use `temporal_layering`.

### Use when

- The main issue is what an observable operation does in the annotation.
- A divinatory, prophetic, testimonial, or interpretive act changes the function
  of the case.
- The cue or source matters, but the threshold turns on the operation performed
  with it.

### Use another value when

- The main issue is whether one source receives authority. Use
  `warrant_attribution`.
- The main issue is the cue type itself. Use `cue_function`.
- The main issue is interaction among multiple warrants. Use
  `warrant_relation`.
- The main issue is later time-layered fulfilment or retrospective readability.
  Use `temporal_layering`.

### Positive example from existing demo cases

Xiang 7, 三卜郊不從: Meng Xianzi's ritual-timing explanation converts failed
divination into procedural intelligibility. The demo annotation uses
`operation_function`.

Macbeth Act 4.1: Macbeth converts equivocal conditional prophecy into practical
security. The demo annotation uses `operation_function`.

Tajōmaru's testimony: confession is converted from apparent truth-disclosure
into self-justifying self-display. The demo annotation uses
`operation_function`.

### Confusable with

- `cue_function`
- `warrant_attribution`

### Decision tip

Ask whether the decisive item is an action: interpreting, confessing,
consulting, recognizing, self-reading, or explicitly treating fulfilment as an
operation. If yes, use `operation_function`. If later fulfilment reclassifies
earlier evidence, use `temporal_layering`.

## `boundary_setting`

### Definition

Use `boundary_setting` when the main friction is where the case, interpretive
unit, category, or applicable scope begins and ends.

Status: operational value awaiting positive out-of-sample testing. It has no
positive demo example.

### Use when

- The coder must decide what counts as the relevant annotation unit.
- A boundary between cases, functions, warrants, speakers, or frames controls
  the annotation.
- The threshold problem is scope-setting rather than warranting, operation,
  time-layering, or perspective.

### Use another value when

- The boundary is clear and the main problem is warrant attribution. Use
  `warrant_attribution`.
- Multiple warrants interact within an already clear boundary. Use
  `warrant_relation`.
- A visible operation converts evidence into function. Use
  `operation_function`.

### Positive example from existing demo cases

No current demo annotation is coded as `boundary_setting`.

Contrast: Xi 4 has multiple elements in one annotation, and the demo annotation
treats the relation among warrants as dominant. It uses `warrant_relation`.

### Confusable with

- `warrant_relation`
- `context_inference`

### Decision tip

Ask whether changing the boundary of the annotation would change the result. If
yes, consider `boundary_setting`. If the boundary is stable but the warrants
inside it interact, use `warrant_relation`.

## `temporal_layering`

### Definition

Use `temporal_layering` when story-time, discourse-time, later fulfilment,
retrospective framing, or later reuse changes the function of the sign or
annotation.

### Use when

- A later moment makes an earlier sign readable differently.
- Prospective and retrospective orientations are both important.
- The sign remains active across time layers.
- The function depends on fulfilment, later recognition, or historical
  readability.

### Use another value when

- The main issue is relation among warrants at the same level. Use
  `warrant_relation`.
- A single source receives authority without time-layered reactivation. Use
  `warrant_attribution`.
- A visible operation is decisive for reasons other than time layering. Use
  `operation_function`.

### Positive example from existing demo cases

Zhuang 22, 陳厲公生敬仲：卜妻與周易觀之否: the sign remains active across projected
descent and later historical readability. The demo annotation uses
`temporal_layering`.

Macbeth Act 5.8: later fulfilment reclassifies Macbeth's earlier assurance as
an equivocal trap. The demo annotation uses `temporal_layering`.

### Confusable with

- `warrant_relation`
- `operation_function`

### Decision tip

Ask whether the function changes because of a later time layer. If yes, use
`temporal_layering`. If the change comes from how warrants relate, use
`warrant_relation`.

## `perspective_assignment`

### Definition

Use `perspective_assignment` when the main friction is whose perspective,
testimonial position, or narrative standpoint determines the function.

### Use when

- The annotation depends on a speaker's or witness's position.
- Testimonial role, self-defense, shame, accusation, or self-blame shapes the
  function.
- The main issue is perspective rather than source authority or warrant
  incompatibility.

### Use another value when

- The main issue is contradiction among multiple warrants. Use
  `warrant_relation`.
- A confession or testimony is mainly treated as a visible operation. Use
  `operation_function`.
- Later time-layering changes the function. Use `temporal_layering`.

### Positive example from existing demo cases

Masago's testimony: victim-position, shame, accusation, and self-blame qualify
one another, and the testimonial position is decisive. The demo annotation uses
`perspective_assignment`.

### Confusable with

- `warrant_relation`
- `operation_function`

### Decision tip

Ask whether changing the speaker or testimonial position would change the
annotation. If yes, use `perspective_assignment`. If the main issue is
incompatibility among multiple accounts as warrants, use `warrant_relation`.

## `context_inference`

### Definition

Use `context_inference` when the main friction depends on contextual inference
beyond the immediate textual anchor.

Status: operational value awaiting positive out-of-sample testing. It has no
positive demo example.

`context_inference` is a last-resort value. Do not assign it merely because
contextual evidence is used. Assign it only when the absence of a contextual
bridge is itself the dominant obstacle to evidence-to-function conversion.

### Use when

- The annotation requires metadata, historical context, parallel material, or
  other contextual framing, and the missing bridge is the dominant obstacle to
  conversion.
- The immediate cue requires a contextual bridge to support the function.
- The dominant conversion requires justification beyond local anchor, internal
  sequence, temporal layering, perspective, operation, or warrant relation.
- The coder must supply a contextual bridge and should document it in
  `rationale_note`.

### Use another value when

- The function follows from the immediate textual anchor and internal sequence.
  Use the more specific locus.
- Background knowledge is present but the dominant conversion is still explained
  by a local anchor, internal sequence, temporal layering, perspective,
  operation, or warrant relation.
- Later temporal framing is the main issue. Use `temporal_layering`.
- Multiple warrants within the text interact. Use `warrant_relation`.
- Perspective or testimonial position is decisive. Use
  `perspective_assignment`.

### Positive example from existing demo cases

No current demo annotation is coded as `context_inference`.

Contrast: Zhuang 22 involves later historical readability, but the demo
annotation treats the time-layered activation of the sign as dominant and uses
`temporal_layering` rather than `context_inference`.

### Confusable with

- `temporal_layering`
- `boundary_setting`
- `warrant_relation`

### Decision tip

Ask whether the judgement depends mostly on contextual information outside the
immediate anchor because the local evidence cannot sustain the function without
a contextual bridge. If yes, consider `context_inference`. If contextual
evidence merely supports a conversion whose obstacle lies elsewhere, record it
in `epistemic_support` and use the more specific locus. If later readability is
the decisive feature, use `temporal_layering`.

## Key Distinctions

### `friction_locus` vs `epistemic_support`

- `friction_locus` answers where the conversion is blocked or requires added
  inferential work.
- `epistemic_support` answers what evidence or support is used to cross that
  threshold.

For example, `narrative_context` or `external_historical_context` may be used as
`epistemic_support` while the dominant locus remains `warrant_relation`,
`temporal_layering`, or another more specific value. Contextual support does not
by itself justify `context_inference`.

### `warrant_attribution` vs `warrant_relation`

- `warrant_attribution`: one source or medium receives warranting force.
- `warrant_relation`: multiple warrants interact, conflict, rank, qualify, or
  suspend one another.

Use `warrant_attribution` for Min 1 and Macbeth Act 1.3. Use
`warrant_relation` for Xi 4 and Takehiro's posthumous testimony.

### `operation_function` vs `warrant_attribution`: transforming evidence or granting standing?

Authority is often assigned through an interpretive act, so coders should not
choose `operation_function` merely because interpretation occurs. The key
question is whether the operation transforms evidence whose standing is already
established, or whether the operation grants warranting standing to a source,
medium, speaker, or result.

Use `operation_function` when evidence already has standing in the local
sequence and the decisive threshold is what a visible operation does with it.

Use `warrant_attribution` when the decisive threshold is whether a source,
medium, speaker, or result receives warranting standing. The interpretive act
may be present, but its main role is to authorize the source/result as usable
evidence.

Counterfactual test:

- If the evidence already counts as the relevant evidence before the operation,
  while the function depends on how the operation handles it, prefer
  `operation_function`.
- If the evidence becomes usable as a warrant through the operation that grants
  it standing, prefer `warrant_attribution`.

Examples:

- Xiang 7 = `operation_function` because the failed divination already has
  standing as a non-compliant result; Meng Xianzi's explanation transforms it
  into procedural intelligibility.
- Min 1 = `warrant_attribution` because the Yi-related result becomes usable as
  warrant through Xin Liao's auspicious interpretation.

### `operation_function` vs `warrant_relation`: operation as converter or operation as relation-maker?

Use `operation_function` when the visible operation itself is the main converter
from evidence to function.

Use `warrant_relation` when an operation matters because it creates, exposes,
ranks, or intensifies a relation among warrants.

Counterfactual test:

- If the operation itself performs the conversion, prefer `operation_function`.
- If the operation mainly matters because it relates multiple warrants to one
  another, prefer `warrant_relation`.

Example:

Xi 4 uses `warrant_relation` because 筮短龜長 matters by ranking turtle-shell and
milfoil warrants. The speech is an operation, but its dominant role is to create
a hierarchy and conflict among warrants.

### `cue_function` vs `operation_function`

- `cue_function`: the evidentiary cue type itself leaves the function
  underdetermined.
- `operation_function`: a visible action such as interpretation, confession,
  consultation, recognition, or self-reading converts into function.

If the annotation turns on Macbeth's self-reading of the apparitions, use
`operation_function`, as in Macbeth Act 4.1. Use `cue_function` only when no
more specific locus explains the conversion and after project-lead review.

### `warrant_relation` vs `temporal_layering`: local conflict or time-layered reclassification?

- `warrant_relation`: use when local conflict, ranking, incompatibility, or
  mutual qualification among warrants produces the function.
- `temporal_layering`: use when later fulfilment, retrospective
  reclassification, historical readability, or reuse across time produces the
  function.

Counterfactual test: if removing the cross-warrant conflict removes the
function, prefer `warrant_relation`. If removing the later temporal frame or
later readability removes the function, prefer `temporal_layering`.

Use Xi 4 as `warrant_relation`: turtle result, milfoil result, ranking speech,
and line text create cross-warrant conflict. Use Zhuang 22 as
`temporal_layering`: projected descent and later historical readability keep the
sign active across time.

### `operation_function` vs `temporal_layering`: local operation or later reclassification?

Use `operation_function` when the visible operation locally converts evidence
into function.

Use `temporal_layering` when a later moment, fulfilment, retrospective frame, or
historical readability reclassifies earlier evidence.

Counterfactual test:

- If the function is produced by the local operation itself, prefer
  `operation_function`.
- If the operation registers a later temporal reclassification of earlier
  evidence, prefer `temporal_layering`.

Example:

Macbeth Act 5.8 uses `temporal_layering` because Macbeth's recognition marks
the moment when later fulfilment reclassifies the earlier prophecy as equivocal
trap.

### `perspective_assignment` vs `warrant_relation`

- `perspective_assignment`: whose perspective or testimonial position
  determines function.
- `warrant_relation`: incompatibility among multiple warrants determines
  function.

Use `perspective_assignment` for Masago's testimony. Use `warrant_relation` for
Takehiro's posthumous testimony.

## Friction Locus Decision Tree

Use this sequence when more than one `friction_locus` seems possible. The goal
is to identify the dominant converter from evidence to function.

1. Is the annotation unit or case boundary itself unstable?
   - Yes → `boundary_setting`.
   - No → continue.

2. Does speaker position, witness role, focalization, or testimonial
   perspective determine what function the evidence can have?
   - Yes → `perspective_assignment`.
   - No → continue.

3. Are multiple warrants interacting, conflicting, ranking, qualifying, or
   suspending one another?
   - Yes → `warrant_relation`.
   - No → continue.

4. Does later fulfilment, retrospective framing, historical readability, or
   reuse across time reclassify earlier evidence?
   - Yes → `temporal_layering`.
   - No → continue.

5. Is one source, medium, speaker, or result being granted warranting standing?
   - Yes → `warrant_attribution`.
   - No → continue.

6. Is a visible operation locally converting evidence into function?
   - Yes → `operation_function`.
   - No → continue.

7. Does the judgement depend mainly on contextual information outside the local
   anchor, after all more specific loci have been considered?
   - Yes → `context_inference`.
   - No → continue.

8. If none of the above applies, consider reserved `cue_function` with
   project-lead review.

Then apply the dominant-threshold protocol to the leading candidates:

1. **Counterfactual test:** which candidate locus, if removed, would make the
   function label hardest to sustain?
2. **Proximity test:** which locus most directly mediates the
   anchor-to-function conversion?
3. **Explanatory sufficiency test:** which locus explains the conversion with
   the fewest additional assumptions?

If the tests do not resolve the case, set `uncertainty_flag=high`, provide an
`alternative_signature` whenever possible, explain the unresolved choice in
`rationale_note`, and route the case to contested review.

This ordering is a coding convention for pilot testing. It gives coders a
stable route through cases where multiple thresholds are present. Alternative
orderings may be evaluated in a future reliability study.
