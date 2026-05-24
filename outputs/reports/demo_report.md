# TRIM Demo Comparison Report

## Validation Summary

- Records: 10
- Errors: 0
- Warnings: 0

Validation passed with no issues.

## Same Function / Different Signature

| function_label | case_ids | case_labels | signature_count | signatures | interpretive_payoff |
| --- | --- | --- | --- | --- | --- |
| immediate_stabilization | ZZ_XIANG_7; ZZ_MIN_1 | Xiang 7, 三卜郊不從; Min 1, 畢萬筮仕於晉 | 2 | operation_function / stabilizes / textual_anchor+ritual_sequence / intradiegetic / immediate / low; warrant_attribution / stabilizes+projects / textual_anchor+internal_sequence / intradiegetic / prospective / medium | Same function label appears with different threshold-rationale signatures. |
| extended_deliberation | ZZ_XI_4; ZZ_ZHUANG_22 | Xi 4, 初，晉獻公欲以驪姬為夫人：卜筮相違; Zhuang 22, 陳厲公生敬仲：卜妻與周易觀之否 | 2 | warrant_relation / extends / textual_anchor+internal_sequence / intradiegetic / recursive / medium; temporal_layering / extends+projects / textual_anchor+internal_sequence / commentarial_discourse / prospective-retrospective / medium | Same function label appears with different threshold-rationale signatures. |

## Same Cue / Different Function

### Primary same-cue test: prophecy

| cue_family | case_ids | case_labels | function_count | functions | signatures |
| --- | --- | --- | --- | --- | --- |
| prophecy | MAC_1_3; MAC_4_1; MAC_5_8 | Act 1.3, witches' prophecy and Cawdor confirmation; Act 4.1, apparition prophecies; Act 5.8, Macduff disclosure and double sense | 3 | ambition_trigger_authorization; false_security; retrospective_trap | warrant_attribution / authorizes+reframes / textual_anchor+internal_sequence / dramatic_present / prospective / medium; operation_function / reframes+narrows / textual_anchor+internal_sequence / dramatic_present / prospective-retrospective / low; temporal_layering / reframes / textual_anchor+internal_sequence / dramatic_present / retrospective / low |

### Additional detected same-cue groups

| cue_family | case_ids | case_labels | function_count | functions | signatures |
| --- | --- | --- | --- | --- | --- |
| divination | ZZ_XIANG_7; ZZ_MIN_1; ZZ_XI_4; ZZ_ZHUANG_22 | Xiang 7, 三卜郊不從; Min 1, 畢萬筮仕於晉; Xi 4, 初，晉獻公欲以驪姬為夫人：卜筮相違; Zhuang 22, 陳厲公生敬仲：卜妻與周易觀之否 | 2 | immediate_stabilization; extended_deliberation | operation_function / stabilizes / textual_anchor+ritual_sequence / intradiegetic / immediate / low; warrant_attribution / stabilizes+projects / textual_anchor+internal_sequence / intradiegetic / prospective / medium; warrant_relation / extends / textual_anchor+internal_sequence / intradiegetic / recursive / medium; temporal_layering / extends+projects / textual_anchor+internal_sequence / commentarial_discourse / prospective-retrospective / medium |
| testimony | GROVE_TAJOMARU; GROVE_MASAGO; GROVE_TAKEHIRO | Tajōmaru's testimony; Masago's testimony; Takehiro's posthumous testimony | 3 | self_justification; self_defence_self_accusation; epistemic_suspension | operation_function / reframes / textual_anchor+narrative_context / frame_narrative / retrospective / medium; perspective_assignment / qualifies / textual_anchor+narrative_context / frame_narrative / retrospective / high; warrant_relation / contradicts+suspends / textual_anchor+narrative_context / frame_narrative / retrospective / high |

### Full same-cue output table

| cue_family | case_ids | case_labels | function_count | functions | signatures |
| --- | --- | --- | --- | --- | --- |
| divination | ZZ_XIANG_7; ZZ_MIN_1; ZZ_XI_4; ZZ_ZHUANG_22 | Xiang 7, 三卜郊不從; Min 1, 畢萬筮仕於晉; Xi 4, 初，晉獻公欲以驪姬為夫人：卜筮相違; Zhuang 22, 陳厲公生敬仲：卜妻與周易觀之否 | 2 | immediate_stabilization; extended_deliberation | operation_function / stabilizes / textual_anchor+ritual_sequence / intradiegetic / immediate / low; warrant_attribution / stabilizes+projects / textual_anchor+internal_sequence / intradiegetic / prospective / medium; warrant_relation / extends / textual_anchor+internal_sequence / intradiegetic / recursive / medium; temporal_layering / extends+projects / textual_anchor+internal_sequence / commentarial_discourse / prospective-retrospective / medium |
| prophecy | MAC_1_3; MAC_4_1; MAC_5_8 | Act 1.3, witches' prophecy and Cawdor confirmation; Act 4.1, apparition prophecies; Act 5.8, Macduff disclosure and double sense | 3 | ambition_trigger_authorization; false_security; retrospective_trap | warrant_attribution / authorizes+reframes / textual_anchor+internal_sequence / dramatic_present / prospective / medium; operation_function / reframes+narrows / textual_anchor+internal_sequence / dramatic_present / prospective-retrospective / low; temporal_layering / reframes / textual_anchor+internal_sequence / dramatic_present / retrospective / low |
| testimony | GROVE_TAJOMARU; GROVE_MASAGO; GROVE_TAKEHIRO | Tajōmaru's testimony; Masago's testimony; Takehiro's posthumous testimony | 3 | self_justification; self_defence_self_accusation; epistemic_suspension | operation_function / reframes / textual_anchor+narrative_context / frame_narrative / retrospective / medium; perspective_assignment / qualifies / textual_anchor+narrative_context / frame_narrative / retrospective / high; warrant_relation / contradicts+suspends / textual_anchor+narrative_context / frame_narrative / retrospective / high |

## Broad Family / Different Signature

| broad_function_family | case_ids | case_labels | signature_count | signatures | interpretive_payoff |
| --- | --- | --- | --- | --- | --- |
| self-exculpatory testimony | GROVE_TAJOMARU; GROVE_MASAGO | Tajōmaru's testimony; Masago's testimony | 2 | operation_function / reframes / textual_anchor+narrative_context / frame_narrative / retrospective / medium; perspective_assignment / qualifies / textual_anchor+narrative_context / frame_narrative / retrospective / high | Same broad function family appears with different threshold-rationale signatures. |

## Contested Cases

| case_id | case_label | function_label | cue_family | signature | alternative_signature | rationale_note |
| --- | --- | --- | --- | --- | --- | --- |
| ZZ_XI_4 | Xi 4, 初，晉獻公欲以驪姬為夫人：卜筮相違 | extended_deliberation | divination | warrant_relation / extends / textual_anchor+internal_sequence / intradiegetic / recursive / medium | temporal_layering / extends / textual_anchor+internal_sequence / commentarial_discourse / retrospective / medium | The dominant threshold is warrant_relation because conflict among turtle result, milfoil result, ranking speech, and line text prevents clean closure. Temporal layering is a meaningful secondary observation. |
