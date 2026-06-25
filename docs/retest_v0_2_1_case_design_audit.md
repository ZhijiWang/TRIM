# Retest v0.2.1 Case-Design Audit

This is a researcher-facing hostile audit of the 12 formal v0.2.1 retest cases.
It does not provide expected function labels or hidden answer keys. Its purpose
is to check whether the corpus still stresses the pilot-informed boundaries
without letting source family or metadata decide the annotation in advance.

## Set-Level Review

- Formal case count remains 12.
- No original v0.2.0 formal pilot case is reused.
- The corpus includes anchor, boundary-stress, shared-context, evidence-selection,
  and distractor/no-fit stress cases.
- At least one realistic no-fit candidate remains in the set.
- At least one case can plausibly support a complete alternative signature before
  adjudication.
- At least one case includes supplied segments that should not all be selected as
  primary evidence without a specific rationale.
- At least one case makes actor action visible without making authorization
  automatic.
- At least one case uses explicit shared-context permission.
- At least one case stresses local speech act versus larger frame.
- No formal case was replaced in this audit patch.

## Case Review

| Case ID | Classification | Neutral case description | Likely source-family prior | Boundary being stressed | Can function be guessed from source or case type alone? | More than one function plausible before close reading? | Evidence-selection challenge | Scope/shared-context challenge | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `JC_CALPURNIA_DECIUS` | boundary-stress case | Caesar hears a dream report, sacrificial report, and Decius's alternative account before deciding whether to go. | Shakespeare omen scenes may cue prophecy or political decision-making. | Analyst-level function versus actor uptake; authorization versus stabilization or deliberation. | No. The scene includes several signs and a decision, but the analytic target depends on which conversion is selected. | Yes. Several complete pathways remain possible before close reading. | Not all five segments should be primary unless the coder argues that each is indispensable. | Local passage only; no cross-case context. | Retain. |
| `JC_IDES_SOOTHSAYER` | anchor case | A public warning is spoken, repeated, and dismissed by Caesar. | A famous warning scene may cue an easy sign-response reading. | Actor action should not automatically determine analytic function. | Partly, because the scene is compact, but the coder must still distinguish warning content from uptake. | Limited but plausible at low complexity. | Segment selection should distinguish the spoken warning from Caesar's dismissal. | Local passage only. | Retain as an easy anchor. |
| `HAM_GHOST_COMMAND` | boundary-stress case | The Ghost identifies itself, names a death account as false, commands revenge, and Hamlet swears remembrance. | Ghost scenes may cue command or authorization. | Actor-level command versus project-defined analytic function; action-guiding standing versus narrative structure. | No. Command form is visible, but classification depends on the evidence-to-function conversion. | Yes. Command, testimony, and memory pathways remain plausible before close reading. | The coder must decide whether identification, accusation, command, or Hamlet's response is primary. | Local passage only. | Retain. |
| `HAM_PLAY_REACTION` | boundary-stress case | Hamlet stages a play and compares Claudius's response with Horatio. | Hamlet play-within-play scenes may cue a test. | Explicit textual operation versus context inference; local speech versus outer arrangement; shared-context use. | No. The context relation matters and is declared, not assumed. | Yes. The staged scene, observation, and prior report can support more than one complete pathway. | Primary evidence should not automatically include the entire paired context. | Uses `HAMLET_CONTEXT_A`; required context is limited to `HAM_GHOST_COMMAND_S2`. | Retain. |
| `OTH_HANDKERCHIEF_CHAIN` | boundary-stress case | The handkerchief moves among characters and is later described by Iago, demanded by Othello, and brought in by Bianca. | Material-object scenes may cue evidence or proof. | Warrant attribution versus warrant relation; primary evidence versus context. | No. The object sequence alone does not settle which relation is dominant. | Yes. Possession, report, demand, and later appearance create competing pathways. | The case deliberately contains more segments than should normally be primary. | Uses `OTHELLO_CONTEXT_A`; all permitted segments are in one case group. | Retain. |
| `ANT_GUARD_REPORT` | boundary-stress case | A guard reports burial traces, sentries' reaction, and Creon's response. | Greek messenger/report scenes may cue reported speech. | Reported speech versus frame narrative; actor response versus analytic conversion. | No. Presentation form alone is insufficient. | Yes. Local report and surrounding response can pull differently. | The report details and Creon's response should be separated as primary/context where appropriate. | Local passage only. | Retain. |
| `ANT_TEIRESIAS_OMENS` | boundary-stress case | Teiresias reports bird cries, failed sacrifice, and the city's condition to Creon. | Prophetic/omen scenes may cue actionability too quickly. | Authorization versus stabilization or extended deliberation; explicit interpretive operation versus context. | No. Omen source family is not enough. | Yes. Signs, failed ritual, and Teiresias's statement can support different pathways. | The coder must decide whether signs, failed sacrifice, or address to Creon is primary. | Local passage only. | Retain. |
| `OED_TIREISIAS_ACCUSATION` | boundary-stress case | Oedipus asks Teiresias to speak, Teiresias resists, then accuses Oedipus, who rejects the charge. | Accusation scenes may cue testimony or perspective. | Operation as act versus standpoint and self-presentation; uncertainty calibration. | No. The case type does not settle whether speech act or standpoint dominates. | Yes. The resistance, accusation, and rejection leave multiple pathways available before close reading. | The accusation may be primary, while resistance and rejection may be contextual depending on the pathway. | Local passage only. | Retain. |
| `OED_MESSENGER_SHEPHERD` | shared-context stress case | Messenger and shepherd statements are heard before Oedipus says all has come to light. | Recognition scenes may cue a single obvious discovery. | Shared narrative field; required context; alternative signature and uncertainty calibration. | No. The shared-context permission is necessary but not answer-bearing. | Yes. Local statements and earlier rejected accusation can both matter. | Not every statement in the scene should be primary unless justified. | Uses `THEBES_CONTEXT_A`; required context is limited to `OED_TIREISIAS_ACCUSATION_S4`. | Retain. |
| `APOL_ORACLE_INQUIRY` | distractor/no-fit stress case | Socrates reports an oracle answer and describes visiting reputedly wise people. | Oracle material may cue prophecy-like mapping. | Explicit operation versus context inference; no-fit pressure; complete-work scope. | No. The corpus family and oracle source could mislead without close reading. | Yes. Reported oracle, inquiry sequence, and philosophical conclusion pull differently. | The inquiry sequence should be discriminated from the initial oracle report. | Complete work permitted; no shared-context registry entry. | Retain. |
| `SILVER_BLAZE_DOG` | anchor case | Holmes and Gregory discuss the dog doing nothing in the night-time. | Detective passages may cue inference. | Explicit textual operation versus implicit context inference. | Partly, because it is a compact famous exchange, but source family still does not provide a TRIM label. | Limited but nonzero; absence-as-evidence and dialogue form can be separated. | The key exchange is compact, so the coder should avoid selecting all segments reflexively. | Local passage only. | Retain as an anchor case. |
| `AESOP_FOX_GRAPES` | distractor/no-fit stress case | A fox tries to reach grapes, fails, and says they are probably sour. | Fable source family may cue moral or self-presentation. | No-fit candidate; standpoint-dependent speech; evidence-selection discipline. | No. The fable form supplies a temptation, not a TRIM answer. | Yes. Before close reading, the action, failure, and final speech can be handled differently. | The final speech may dominate for one pathway while the attempt/failure remain context. | Local passage only. | Retain as a distractor/no-fit stress case. |

## Focused Review Of Easier Cases

`AESOP_FOX_GRAPES`, `JC_IDES_SOOTHSAYER`, and `SILVER_BLAZE_DOG` were reviewed
as possible over-easy cases. They are retained because the retest needs a small
number of anchors and distractors, and because each still tests a specific pilot
revision: no-fit pressure, actor uptake, or explicit textual operation. Their
researcher-facing classifications do not enter the coder-facing package.
