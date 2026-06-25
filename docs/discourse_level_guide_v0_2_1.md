# TRIM Discourse-Level Guide v0.2.1

## Rule

Code the level at which the evidence-to-function conversion is analytically
operative.

- Use `reported_speech` when the local speech act, testimony, confession,
  quoted report, or embedded utterance itself carries the conversion.
- Use `frame_narrative` when the outer arrangement of embedded accounts changes
  the function.
- When both are relevant, choose the dominant level and record the other in
  `rationale_note` or `alternative_signature`.

## Why This Changed

The v0.2.0 pilot showed a systematic divergence: one coder coded local
presentation form for all three testimony cases, while the comparison baseline
coded the larger frame. v0.2.1 does not declare one scale universally correct.
It asks which level is doing the analytic work in the selected pathway.

## Controlled Values

- `intradiegetic`: the conversion operates within the story world.
- `extradiegetic`: the conversion operates from an outside narrating position.
- `frame_narrative`: the outer arrangement, sequence, or embedding of accounts
  changes the function.
- `dramatic_present`: the conversion operates in staged dramatic action.
- `reported_speech`: a quoted, reported, testimonial, or confessional speech
  act carries the conversion.
- `commentarial_discourse`: commentary, gloss, or retrospective explanatory
  discourse carries the conversion.

## Testimony/Frame Decision Tree

1. Is the selected primary evidence a local confession, testimony, quotation, or
   report?
   - If yes, continue.
   - If no, choose among the non-testimony levels.
2. Would the same local speech act still carry the coded function if read on
   its own?
   - If yes, `reported_speech` is likely dominant.
   - If no, continue.
3. Does the function depend on sequence, incompatibility, accumulation, or
   arrangement among multiple embedded accounts?
   - If yes, `frame_narrative` is likely dominant.
4. Are both true?
   - Choose the level that most directly mediates the selected function.
   - Record the other level in `rationale_note` or a complete
     `alternative_signature`.

## Neutral Positive/Near-Miss Pair

Positive `reported_speech`: a single witness statement contains the decisive
conversion. The witness's words themselves grant, qualify, or suspend the
function, and no outer sequence is needed for the annotation to hold.

Near miss: a single witness statement appears decisive, but its function changes
only because it is placed after another incompatible account. The outer
arrangement is doing the work, so `frame_narrative` may dominate.

Positive `frame_narrative`: several embedded accounts are each locally
intelligible, but the function emerges from their accumulated incompatibility or
placement.

Near miss: the surrounding frame exists, but the coded function is already
carried by one local utterance. Use `reported_speech` and mention frame context
in the rationale if needed.

## Shared Context

Frame-level coding requires explicit permission to use the relevant shared
context. Check `case_scope`, `shared_context_ids`,
`cross_case_context_permitted`, and `required_context_segments` before using
cross-case relations.

