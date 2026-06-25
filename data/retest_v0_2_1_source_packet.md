# TRIM v0.2.1 Retest Source Packet

## Instructions

Use the case manifest for source, language-access, copyright, and scope
metadata. For each formal case, select one to three primary evidence segment
IDs. Add context segment IDs only when they support sequence, speaker role, or
permitted shared context.

All formal coding must be based on the supplied packet. External links are
provenance references and are not required for completion. This packet contains
no expected labels.

---

## `JC_CALPURNIA_DECIUS`

**Source:** William Shakespeare, *Julius Caesar*, Act 2, Scene 2  
**Scope:** local passage only  
**Text basis:** MIT Shakespeare electronic text

- `JC_CALPURNIA_DECIUS_S1`: Caesar reports unrest: "Nor heaven nor earth have
  been at peace to-night" and Calpurnia cried out in sleep that Caesar was
  murdered.
- `JC_CALPURNIA_DECIUS_S2`: Caesar orders sacrifices and asks for the priests'
  "opinions of success."
- `JC_CALPURNIA_DECIUS_S3`: The servant reports that the augurers found no
  heart in the beast and advise Caesar not to go forth.
- `JC_CALPURNIA_DECIUS_S4`: Calpurnia describes the dream of Caesar's statue
  spouting blood while Romans smile and bathe their hands.
- `JC_CALPURNIA_DECIUS_S5`: Decius gives a different account of the dream,
  saying Caesar's blood will provide life for Rome, and tells Caesar the Senate
  intends to give him a crown.

---

## `JC_IDES_SOOTHSAYER`

**Source:** William Shakespeare, *Julius Caesar*, Act 1, Scene 2  
**Scope:** local passage only  
**Text basis:** MIT Shakespeare electronic text

- `JC_IDES_SOOTHSAYER_S1`: The soothsayer calls from the crowd: "Beware the
  ides of March."
- `JC_IDES_SOOTHSAYER_S2`: Caesar asks to see the man and hears the warning
  repeated.
- `JC_IDES_SOOTHSAYER_S3`: Caesar dismisses him: "He is a dreamer; let us
  leave him."

---

## `HAM_GHOST_COMMAND`

**Source:** William Shakespeare, *Hamlet*, Act 1, Scene 5  
**Scope:** local passage only  
**Text basis:** MIT Shakespeare electronic text

- `HAM_GHOST_COMMAND_S1`: The Ghost identifies itself as Hamlet's father's
  spirit and says it is bound to walk at night.
- `HAM_GHOST_COMMAND_S2`: The Ghost says the report of a serpent's sting is
  false and names "the serpent that did sting thy father's life."
- `HAM_GHOST_COMMAND_S3`: The Ghost commands Hamlet to revenge "foul and most
  unnatural murder."
- `HAM_GHOST_COMMAND_S4`: Hamlet swears to remember and sets aside other
  records from memory.

---

## `HAM_PLAY_REACTION`

**Source:** William Shakespeare, *Hamlet*, Act 3, Scene 2  
**Scope:** supplied related cases permitted  
**Shared context:** `HAMLET_CONTEXT_A`
**Required context:** `HAM_GHOST_COMMAND_S2` may be used as context

- `HAM_PLAY_REACTION_S1`: Hamlet asks Horatio to watch Claudius during the play
  and says they will compare what they see.
- `HAM_PLAY_REACTION_S2`: The dumb show and play stage a king murdered in a
  garden by poison poured into his ear.
- `HAM_PLAY_REACTION_S3`: Claudius rises and stops the play.
- `HAM_PLAY_REACTION_S4`: Hamlet and Horatio compare their observations after
  Claudius exits.

---

## `OTH_HANDKERCHIEF_CHAIN`

**Source:** William Shakespeare, *Othello*, Act 3, Scenes 3-4  
**Scope:** supplied related cases permitted  
**Shared context:** `OTHELLO_CONTEXT_A`

- `OTH_HANDKERCHIEF_CHAIN_S1`: Desdemona offers Othello her handkerchief; it
  drops unnoticed.
- `OTH_HANDKERCHIEF_CHAIN_S2`: Emilia picks up the handkerchief and gives it to
  Iago, who has often asked for it.
- `OTH_HANDKERCHIEF_CHAIN_S3`: Iago tells Othello that he saw Cassio wipe his
  beard with the handkerchief.
- `OTH_HANDKERCHIEF_CHAIN_S4`: Othello demands the handkerchief from Desdemona;
  she cannot produce it.
- `OTH_HANDKERCHIEF_CHAIN_S5`: Bianca later enters with the handkerchief and
  complains that Cassio gave it to her to copy.

---

## `ANT_GUARD_REPORT`

**Source:** Sophocles, *Antigone*, translated by F. Storr  
**Scope:** local passage only  
**Text basis:** Project Gutenberg #31

- `ANT_GUARD_REPORT_S1`: The guard reports that someone has covered the corpse
  with dust and performed burial rites.
- `ANT_GUARD_REPORT_S2`: He says there was no mark of pickaxe or mattock and no
  wheel track.
- `ANT_GUARD_REPORT_S3`: The sentries argue with one another after the report.
- `ANT_GUARD_REPORT_S4`: Creon hears the report and speaks about disobedience
  and bribery.

---

## `ANT_TEIRESIAS_OMENS`

**Source:** Sophocles, *Antigone*, translated by F. Storr  
**Scope:** local passage only  
**Text basis:** Project Gutenberg #31

- `ANT_TEIRESIAS_OMENS_S1`: Teiresias says he sat at the old seat of augury and
  heard strange cries among birds.
- `ANT_TEIRESIAS_OMENS_S2`: He reports that the birds were tearing one another
  with bloody talons.
- `ANT_TEIRESIAS_OMENS_S3`: He tried burnt sacrifice, but the fire would not
  blaze and the signs failed.
- `ANT_TEIRESIAS_OMENS_S4`: Teiresias tells Creon that the city is sick through
  his counsel.

---

## `OED_TIREISIAS_ACCUSATION`

**Source:** Sophocles, *Oedipus the King*, translated by F. Storr  
**Scope:** local passage only  
**Text basis:** Project Gutenberg #31

- `OED_TIREISIAS_ACCUSATION_S1`: Oedipus asks Teiresias to reveal what he knows
  about Laius's murderer.
- `OED_TIREISIAS_ACCUSATION_S2`: Teiresias resists speaking and warns that
  knowledge will bring grief.
- `OED_TIREISIAS_ACCUSATION_S3`: Under pressure, Teiresias says that Oedipus
  himself is the pollution of the land.
- `OED_TIREISIAS_ACCUSATION_S4`: Oedipus rejects the charge and suspects
  conspiracy.

---

## `OED_MESSENGER_SHEPHERD`

**Source:** Sophocles, *Oedipus the King*, translated by F. Storr  
**Scope:** shared narrative field  
**Shared context:** `THEBES_CONTEXT_A`
**Required context:** `OED_TIREISIAS_ACCUSATION_S4` may be used as context

- `OED_MESSENGER_SHEPHERD_S1`: A Corinthian messenger says Polybus was not
  Oedipus's father by blood.
- `OED_MESSENGER_SHEPHERD_S2`: The messenger recalls receiving Oedipus as an
  infant from another shepherd.
- `OED_MESSENGER_SHEPHERD_S3`: The Theban shepherd is brought in and resists
  answering.
- `OED_MESSENGER_SHEPHERD_S4`: Under threat, the shepherd admits the child came
  from Laius's house.
- `OED_MESSENGER_SHEPHERD_S5`: After hearing the messenger and shepherd,
  Oedipus says that all has come to light.

---

## `APOL_ORACLE_INQUIRY`

**Source:** Plato, *Apology*, translated by Benjamin Jowett  
**Scope:** complete work permitted  
**Text basis:** Project Gutenberg #1656

- `APOL_ORACLE_INQUIRY_S1`: Socrates reports that Chaerephon asked the Delphic
  oracle whether anyone was wiser than Socrates.
- `APOL_ORACLE_INQUIRY_S2`: The oracle answered that no one was wiser.
- `APOL_ORACLE_INQUIRY_S3`: Socrates says he visited people reputed to be wise
  after hearing the oracle's answer and compared what they knew with what he
  knew.
- `APOL_ORACLE_INQUIRY_S4`: He concludes that his advantage is recognizing that
  he does not know what he does not know.

---

## `SILVER_BLAZE_DOG`

**Source:** Arthur Conan Doyle, "Silver Blaze" in *The Memoirs of Sherlock Holmes*  
**Scope:** local passage only  
**Text basis:** Project Gutenberg #834

- `SILVER_BLAZE_DOG_S1`: Inspector Gregory asks Holmes whether there is any
  point to which he would draw attention.
- `SILVER_BLAZE_DOG_S2`: Holmes identifies "the curious incident of the dog in
  the night-time."
- `SILVER_BLAZE_DOG_S3`: Gregory says the dog did nothing in the night-time;
  Holmes replies that this was the curious incident.

---

## `AESOP_FOX_GRAPES`

**Source:** "The Fox and the Grapes" in *Three Hundred Aesop's Fables*,
translated by George Fyler Townsend  
**Scope:** local passage only  
**Text basis:** Project Gutenberg #21

- `AESOP_FOX_GRAPES_S1`: A hungry fox sees ripe grapes hanging from a vine.
- `AESOP_FOX_GRAPES_S2`: The fox tries repeatedly to reach them but cannot.
- `AESOP_FOX_GRAPES_S3`: As he leaves, the fox says the grapes are probably
  sour.

---

## Source Record

- Shakespeare passages use MIT Shakespeare electronic texts.
- Sophocles passages use Project Gutenberg #31, F. Storr translation.
- Plato's *Apology* uses Project Gutenberg #1656, Benjamin Jowett translation.
- "Silver Blaze" uses Project Gutenberg #834.
- "The Fox and the Grapes" uses Project Gutenberg #21, George Fyler Townsend
  translation.
