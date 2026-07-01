# AI Run Protocol v0.1

Status: frozen

This protocol governs one independent AI run for `IAG_JP_PUBLIC_002` using `prompt.txt`.

## Pre-Run Boundary

1. The author record is already locked before the AI run.
2. The model must not receive:
   - the author record;
   - author evidence choices;
   - author labels;
   - author rationale;
   - author uncertainty;
   - author alternatives;
   - previous model output.
3. The only substantive input is the frozen prompt.

## Run Rule

4. The run occurs exactly once.
5. No retry is allowed for an uninteresting, inconvenient, malformed, or disagreeing answer.
6. A technical retry is allowed only if:
   - no response is returned;
   - the connection fails;
   - the provider reports an execution failure;
   - no output bytes are produced.
7. If a technical retry occurs:
   - preserve the failed-attempt metadata;
   - increment `retry_count`;
   - explain the failure;
   - do not discard successful-but-unhelpful content.

## Preservation And Parsing

8. Preserve the raw response exactly before parsing.
9. Compute raw output SHA-256 before any transformation.
10. Parsing may repair only transport-level formatting such as removal of surrounding code fences.
11. Parsing must not substantively rewrite:
   - labels;
   - rationale;
   - uncertainty;
   - evidence IDs;
   - alternatives.
12. If the output is invalid JSON but contains recoverable content:
   - preserve raw output;
   - document each mechanical repair;
   - do not ask the model to regenerate.
13. If the output is substantively incomplete:
   - preserve it as the run result;
   - do not fill missing interpretation fields manually;
   - report validation failure.

## Analysis Boundary

14. Do not compare with the human record until the AI record is parsed, validated, frozen, and hashed.
15. No position-note claim may be updated before comparison.
16. The run is a technical demonstration, not empirical human validation.
17. Model output is not an answer key or truth verdict.

## Current State

No model run has occurred. No AI output, AI annotation record, comparison output, or updated research finding exists for this run.
