# Retest v0.2.1 Semantic-Steering Audit

This audit records the human review of case-specific wording in the v0.2.1
coder-facing retest packet. It does not record expected function labels,
expected friction-locus values, adjudication outcomes, or hidden answer keys.

The review target was wording that could tell a coder what analytic work a
segment performs instead of describing observable textual content. The package
builder also runs a machine scan over case-specific files and fails on
unreviewed high-risk matches.

| Case ID | Potentially loaded wording reviewed | Final neutral wording decision | Remaining wording type | Reviewer conclusion |
| --- | --- | --- | --- | --- |
| `JC_CALPURNIA_DECIUS` | Earlier wording described Decius as reinterpreting the dream. | Segment `S5` now says Decius gives a different account of the dream and states what he says about Caesar's blood and the crown. | Direct textual description with brief quotation support. | Retain. Wording names the speech content without naming a TRIM operation. |
| `JC_IDES_SOOTHSAYER` | Warning-scene phrasing was checked for analytic cueing. | Segments state the warning, Caesar's request to see the speaker, repetition, and dismissal. | Direct textual description and quotation. | Retain. The case remains concise but does not supply an expected analytic label. |
| `HAM_GHOST_COMMAND` | Command and memory language was checked for actor-action steering. | Segments state what the Ghost says and what Hamlet swears to remember. | Direct textual description and quotation. | Retain. Actor action is visible, but the packet does not tell the coder how to classify it. |
| `HAM_PLAY_REACTION` | Earlier wording could imply a testing or evidentiary mechanism. | Segment `S1` now says Hamlet asks Horatio to watch Claudius and compare what they see; later segments state the staged murder, Claudius's exit, and the comparison. | Direct textual description. | Retain. Shared context is explicit through the registry, not by analytic wording. |
| `OTH_HANDKERCHIEF_CHAIN` | The case label and registry ID previously used warrant-like wording. | Coder-facing metadata now uses a neutral scene label and registry ID; segments list possession and reported sightings of the handkerchief. | Direct textual sequence. | Retain. The sequence remains available without naming a TRIM rationale or locus. |
| `ANT_GUARD_REPORT` | Earlier segment wording suggested report uptake and exposition. | Segments now describe the covered corpse, missing tracks, sentry argument, and Creon's stated concerns. | Direct textual description. | Retain. Presentation form is visible without naming discourse-level categories. |
| `ANT_TEIRESIAS_OMENS` | Omen wording was checked for automatic authorization cues. | Segments state the seat of augury, bird cries, failed sacrifice, and Teiresias's statement to Creon. | Direct textual description. | Retain. The packet does not say what function the signs should have. |
| `OED_TIREISIAS_ACCUSATION` | Accusation wording was checked for perspective and testimony cues. | Segments state the request, resistance, accusation, and Oedipus's rejection. | Direct textual description. | Retain. The packet records who says what without assigning the analytic boundary. |
| `OED_MESSENGER_SHEPHERD` | Earlier wording used recognition-chain language. | Segment `S5` now says that after hearing the messenger and shepherd, Oedipus says all has come to light. | Direct textual description. | Retain. The shared narrative field is explicit, but the wording does not name a mechanism. |
| `APOL_ORACLE_INQUIRY` | Earlier wording could imply Socrates tests the oracle as an analytic label. | Segment `S3` now states that Socrates visited people reputed to be wise and compared what they knew with what he knew. | Direct textual description. | Retain. The packet records the reported sequence of inquiry. |
| `SILVER_BLAZE_DOG` | The famous phrase was checked for over-directing an inference case. | Segments keep the quoted exchange about the dog and the night-time. | Direct quotation and minimal description. | Retain. The case is an anchor case, but the packet does not name the analytic result. |
| `AESOP_FOX_GRAPES` | Fable moral and self-justification wording was checked. | Segments state the fox sees grapes, fails to reach them, and says they are probably sour. | Direct textual description. | Retain. No moral or TRIM label is supplied. |

## Machine Audit Result

The current package-builder semantic scan reports:

- `match_count: 0`
- `allowlisted_match_count: 0`
- `unreviewed_high_risk_count: 0`

No allowlist entry is currently needed for the formal coder-facing case files.
