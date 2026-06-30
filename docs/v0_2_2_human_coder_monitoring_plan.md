# v0.2.2 Human Coder Monitoring Plan

This plan is observational. Do not modify the frozen v0.2.2 package before
deployment based on this plan alone.

## Before Coding

- Verify package hash:
  `3b3ac302d8491e429d20b1d4fb1c66351ad0e6340698b2f5cd683adb5e0d4cb4`.
- Confirm no prior access to AI outputs.
- Confirm no access to researcher-facing files.
- Record language access.
- Record coder background.
- Assign anonymous coder ID.

## During Coding

Observe without coaching:

- whether evidence selection is difficult;
- whether all supplied segments are selected;
- whether alternative signatures are overused or underused;
- whether uncertainty is calibrated;
- whether question logs are contemporaneous;
- whether discourse-level distinctions remain difficult;
- whether shared context is used correctly;
- whether any field appears unnecessary.

## After Coding

Collect:

- completion time;
- post-coding interview;
- perceived hardest fields;
- perceived redundant fields;
- confidence in evidence selection;
- whether manuals were consulted;
- whether any questions were omitted from the log;
- package usability feedback.

## Observation Priorities From AI Stress Testing

| Case | Field/boundary | Codex issue | Claude issue | Priority for human observation | Why |
| --- | --- | --- | --- | --- | --- |
| All | question-log timing | Raw Codex execution unavailable | Claude question log unavailable | high | Companion files are necessary to test lock, timing, and consistency workflow. |
| All | uncertainty / alternative signature calibration | Raw Codex execution unavailable | Claude coding uses medium uncertainty and alternatives in most cases | medium | May be model style, source difficulty, or package ambiguity; human behavior is needed before revising anything. |
| Shared-context cases | context use | Raw Codex execution unavailable | Claude coding file validates structurally | low | No repeated friction can be established without a second raw execution and logs. |

High priority requires repeated friction across model executions or a strong
protocol inconsistency. No manual or package revision should be made from this
table alone.
