# TRIM-HAA Pilot Interface Specification

Status: fixed pilot design for ethics and participant-language review. This does not change the Core schema or provenance fields.

Expected session length: approximately 60-90 minutes, including instructions, practice, breaks, annotation tasks, and feedback questions. This duration range is provisional and must be finalised before ethics submission and recruitment.

## Human-Pre Stage

The participant sees:

1. Original segmented source text.
2. Core annotation fields.

The participant does not see:

- AI output
- Other participant output
- Adjudicated output
- Researcher-preferred labels
- Any answer labelled as authoritative

The submitted human-pre record is locked before the second pass.

## AI-Review Second Pass

Display order:

1. Source text.
2. Panel labelled "Your earlier response".
3. Panel labelled "AI-generated response".
4. Editable form labelled "Your current response".

The participant sees:

- Original segmented source text
- Their own locked human-pre record
- One frozen AI Core record
- Editable second-pass Core fields

The participant must never complete a second-pass record without access to their own locked human-pre record.

## Control Second Pass

Display order:

1. Source text.
2. Panel labelled "Your earlier response".
3. Editable form labelled "Your current response".

The participant sees:

- Original segmented source text
- Their own locked human-pre record
- Editable second-pass Core fields
- No AI-generated material

The participant must never complete a second-pass record without access to their own locked human-pre record.

## Interface Parity

The AI-review and control second-pass interfaces must be equivalent in:

- Source-text display
- Participant-pre display
- Editable fields
- Field order
- Button labels
- Time window
- Typography
- Spacing
- Navigation
- Revision-reason prompt
- Burden questions

The only intended difference is:

- AI-review condition: frozen AI-response panel present.
- Control condition: AI-response panel absent.

## Panel Display Rules

- Recommended display order: source text, participant's locked prior response, AI-generated response only in AI-review, editable current-response form.
- AI panel: visible and expanded by default in AI-review cases.
- Participant earlier-response panel: visible and expanded by default in both second-pass conditions.
- Panel location: AI panel appears after the participant's earlier response and before the editable current-response form.
- Title wording: "Your earlier response", "AI-generated response", "Your current response".
- Visual emphasis: neutral styling; no colour suggesting correctness.
- Do not use checkmarks, confidence badges, recommendation icons, or expert-answer labels.
- The participant should not need to actively open the AI panel in the pilot design.
- If the interface records panel viewing, record only viewing metadata approved in the data-management plan.
- Scrolling requirements should be equivalent across conditions as far as possible. If scrolling differs, record it as an interface note.
- Mobile and desktop layouts should preserve the same display order and neutral labels. Any layout difference must be documented before recruitment.

## Editability

- Source text is not editable.
- "Your earlier response" is not editable.
- "AI-generated response" is not editable.
- "Your current response" is editable.
- Unchanged current responses are acceptable and must be submit-ready.

## Timing and Logging

If approved, record:

- Start and end of each stage
- Exposure timestamp for AI-review cases
- Post-edit timestamp
- Procedural questions
- Technical interruptions
- Protocol deviations
- Optional AI-panel viewing metadata

## Break Points

Breaks may occur after the practice case, after any submitted case, or when participant fatigue is visible.

## Researcher Visibility

The researcher may see technical status, completion status, and procedural logs. The researcher may not use interface visibility to guide labels, evidence, mechanisms, or interpretations.

## Never Shown

Never show:

- Answer framed as authoritative
- Answer framed as researcher-preferred
- Answer framed as fixing the participant's response
- Answer framed as better than the participant's response
- Other participant records
- Hidden model reasoning
- Gold labels
- Adjudicated answers
