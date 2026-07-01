# Retest v0.2.1 Source-Text Audit

This audit records the human review of the v0.2.1 coder-facing source packet
after replacing project-authored formal segment summaries with source text or
documented public-domain translation text. It does not include expected TRIM
labels, expected signature fields, adjudication outcomes, or hidden answers.

| Case ID | Source | Edition or translation | Source location | Segment structure | Omissions marked? | Wording exact or normalized? | Language-access classification | Summary removed? | Navigation neutral? | Reviewer conclusion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `JC_CALPURNIA_DECIUS` | *Julius Caesar* | MIT Shakespeare electronic text | Act 2, Scene 2 | Distributed excerpts within one scene | No omissions inside segment excerpts | Exact source wording; blockquote formatting added | `direct_original_language_access` | Yes | Yes | Retain. |
| `JC_IDES_SOOTHSAYER` | *Julius Caesar* | MIT Shakespeare electronic text | Act 1, Scene 2 | Contiguous local exchange split into three segments | No | Exact source wording; blockquote formatting added | `direct_original_language_access` | Yes | Yes | Retain. |
| `HAM_GHOST_COMMAND` | *Hamlet* | MIT Shakespeare electronic text | Act 1, Scene 5 | Distributed excerpts within one scene | No omissions inside segment excerpts | Exact source wording; blockquote formatting added | `direct_original_language_access` | Yes | Yes | Retain. |
| `HAM_PLAY_REACTION` | *Hamlet* | MIT Shakespeare electronic text | Act 3, Scene 2, with required context from Act 1, Scene 5 | Distributed excerpts within one scene plus permitted context segment | No omissions inside segment excerpts | Exact source wording; long stage direction wrapped as packet prose | `direct_original_language_access` | Yes | Yes | Retain. |
| `OTH_HANDKERCHIEF_CHAIN` | *Othello* | MIT Shakespeare electronic text | Act 3, Scenes 3-4 | Separated passages from one formal case | No omissions inside segment excerpts | Exact source wording; blockquote formatting added | `direct_original_language_access` | Yes | Yes | Retain as `multi_passage_single_case`. |
| `ANT_GUARD_REPORT` | *Antigone* | F. Storr translation, Project Gutenberg #31 | Guard's first report to Creon | Contiguous local passage split into four segments | No | Public-domain translation text normalized to ASCII apostrophes/double hyphens | `published_translation` | Yes | Yes | Retain. |
| `ANT_TEIRESIAS_OMENS` | *Antigone* | F. Storr translation, Project Gutenberg #31 | Teiresias speech to Creon | Contiguous speech split into four segments | No | Public-domain translation text normalized to ASCII apostrophes/double hyphens | `published_translation` | Yes | Yes | Retain. |
| `OED_TIREISIAS_ACCUSATION` | *Oedipus the King* | F. Storr translation, Project Gutenberg #31 | Teiresias exchange with Oedipus | Distributed excerpts within one local exchange | No omissions inside segment excerpts | Public-domain translation text normalized to ASCII apostrophes/double hyphens | `published_translation` | Yes | Yes | Retain. |
| `OED_MESSENGER_SHEPHERD` | *Oedipus the King* | F. Storr translation, Project Gutenberg #31 | Messenger and herdsman recognition exchange | Distributed excerpts within one exchange plus declared shared narrative context | No omissions inside segment excerpts | Public-domain translation text normalized to ASCII apostrophes/double hyphens | `published_translation` | Yes | Yes | Retain. |
| `APOL_ORACLE_INQUIRY` | *Apology* | Benjamin Jowett translation, Project Gutenberg #1656 | Socrates' account of Chaerephon and subsequent inquiry | Contiguous prose passage split into four segments | No | Public-domain translation text with line wrapping normalized | `published_translation` | Yes | Yes | Retain. |
| `SILVER_BLAZE_DOG` | "Silver Blaze" | Arthur Conan Doyle, Project Gutenberg #834 | Holmes and Gregory carriage exchange | Contiguous exchange split into three segments | No | Public-domain text with indentation normalized to blockquotes | `direct_original_language_access` | Yes | Yes | Retain. |
| `AESOP_FOX_GRAPES` | "The Fox and the Grapes" | George Fyler Townsend translation, Project Gutenberg #21 | Full fable text | Contiguous short fable split into three segments | No | Public-domain translation text with line wrapping normalized | `published_translation` | Yes | Yes | Retain. |

## Set-Level Conclusion

Every formal segment now supplies source text or the documented public-domain
translation text. Project-authored summaries no longer substitute for formal
evidence text. Navigation notes remain limited to speaker, scene, sequence, or
segment-boundary information. External URLs remain provenance references only,
and the package remains intended for offline completion.
