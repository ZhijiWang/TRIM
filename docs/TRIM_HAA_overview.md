# TRIM-HAA overview

TRIM-HAA is a research extension of TRIM for human-AI annotation audit.

It compares separately preserved records:

- `HUMAN_PRE`: a locked independent human annotation;
- `AI_RECORD`: an independently generated model annotation;
- `HUMAN_POST_AI`: a human revision after AI output was shown;
- optional `HUMAN_SECOND_PASS_CONTROL`: a human second pass after rereading without AI exposure.

TRIM-HAA records submitted justificatory pathways and revision provenance. It does not recover human cognition or hidden model reasoning.

## Research problem

Human review after model assistance is not automatically independent human judgment. A final label can conceal whether agreement reflects independent convergence, label adoption, evidence adoption, rationale-mechanism adoption, uncertainty shift, alternative suppression, or ordinary rereading.

TRIM-HAA therefore treats agreement as a record relationship, not as a simple endpoint.

## Prototype layers

Layer 1: TRIM-HAA Core

- primary evidence;
- function label;
- rationale mechanism;
- uncertainty;
- rationale note;
- alternative presence.

Layer 2: assistance provenance sidecar

- AI exposure;
- model and prompt metadata;
- lock state;
- timestamps;
- changed-field flags;
- adoption classification.

Layer 3: optional interpretive-depth module

- context evidence;
- anchor information;
- selected legacy pathway fields;
- full alternative signature;
- question-log reference.

## Non-goals

TRIM-HAA does not:

- call live LLM APIs;
- store hidden chain-of-thought;
- create gold labels;
- treat AI output as correct;
- overwrite locked pre-AI records;
- claim causal AI effects from synthetic or single-participant data.

