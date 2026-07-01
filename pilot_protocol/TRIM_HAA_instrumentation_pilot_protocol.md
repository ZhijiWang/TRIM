# TRIM-HAA Instrumentation Pilot Protocol

Status: provisionally frozen for ethics review or exemption assessment. This document does not claim approval.

## Design

- Participants: 4 to 6 adults.
- Cases: 4 to 6 short segmented cases.
- AI records: one frozen synthetic or pre-generated AI Core record per case.
- Instrument: TRIM-HAA Core only.
- Conditions: independent human-pre record, AI-review second pass for most assigned cases, and no-AI second-pass control for at least one case per participant.
- Assignment: counterbalanced case assignment. No participant sees both AI-review and control versions of the same case.
- Model procedure: no live model generation during participant sessions and no model retries during the pilot.
- Adjudication: none during data collection.

## Fixed Interface Design

Human-pre stage: participant sees original segmented source text and Core annotation fields. The participant sees no AI output and no other participant output. The submitted human-pre record is locked.

AI-review second pass: participant sees original segmented source text, their own locked human-pre record, one frozen AI Core record, and editable second-pass Core fields.

Control second pass: participant sees original segmented source text, their own locked human-pre record, no AI record, and editable second-pass Core fields.

The participant must never complete a second-pass record without access to their own locked human-pre record. The only intended condition difference is the presence or absence of the frozen AI record.

## Inclusion Criteria

- Adult participant aged 18 or older.
- Able to read the selected case language at the level required by the source text.
- Able to provide informed consent.
- Able to complete short structured annotation tasks in a research session.
- Meets the practice-case comprehension standard or is retained only for usability feedback if consent permits.

## Exclusion Criteria

- Under 18.
- Cannot provide informed consent.
- Prior direct exposure to the frozen AI outputs, adjudicated records, or exact pilot materials.
- Accessibility need that the pilot setup cannot reasonably support after discussion.
- Cannot distinguish function label from rationale mechanism after standardised re-explanation in the practice protocol.

## Expertise

Literary expertise is not required for the instrumentation pilot unless the selected cases are revised to require specialist interpretation. Relevant background will be recorded only to interpret feasibility findings.

## Reading Level

Cases should be short and readable without extensive external knowledge. The expected reading level must be reviewed with the selected source texts before ethics submission.

## Session Structure

1. Information sheet and consent.
2. Pseudonymous participant ID assignment.
3. Background questionnaire.
4. Core instructions, label guide, and mechanism guide.
5. Practice case and practice-case comprehension check.
6. Human-pre records for assigned cases.
7. Locking of each human-pre record.
8. Second-pass records: AI-review for assigned AI cases and control review for assigned no-AI cases.
9. Revision-reason responses.
10. Burden and comprehension questionnaire.
11. Debrief.

Expected session length: approximately 60-90 minutes, including instructions, practice, breaks, annotation tasks, and feedback questions. This duration range is provisional and must be finalised before ethics submission and recruitment.

## Breaks

Participants may request breaks. The researcher may also pause after the practice case or after a block of cases if fatigue is visible.

## Researcher Intervention Limits

The researcher may repeat written definitions, the approved synthetic practice example, and standardised procedural instructions. The researcher may not suggest labels, evidence, mechanisms, interpretations, or whether the AI output is correct.

## Practice-Case Standard

The practice case is not scored for interpretive correctness. It tests whether the participant can select evidence, distinguish function label from rationale mechanism, choose uncertainty, write a short rationale note, understand that alternatives are optional, and understand that AI output is not an answer key.

Practice outcomes are `ready_for_formal_pilot`, `ready_with_documented_support`, `usability_feedback_only`, and `stop_session`.

If a participant cannot distinguish function label from rationale mechanism after standardised re-explanation, do not proceed with formal pilot data collection. Retain only usability feedback if consent permits. Record the issue as instrument failure, not participant failure.

## Stopping Rules

Stop or pause if technical locking or exposure linkage fails, the participant cannot distinguish Core fields after practice, participant distress appears, burden is clearly excessive, or the participant requests withdrawal.

## Protocol Deviations

Record deviations in a protocol-deviation log with participant ID, case ID if relevant, deviation type, corrective action, and whether the record remains usable for feasibility analysis.
