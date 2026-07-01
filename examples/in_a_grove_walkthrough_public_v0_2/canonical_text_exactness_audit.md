# Canonical Text Exactness Audit

source_url: https://www.aozora.gr.jp/cards/000879/files/179_15255.html
segments_checked: 22
exact_match_status: passed_draft_check
normalisation_applied: Aozora HTML ruby annotations were ignored for comparison; whitespace and HTML line wrapping were ignored. No Japanese source characters, punctuation, quotation marks, or dashes were silently modernised in the repository text. CSV quoting is treated only as CSV escaping, not as source-text alteration.
differences_found: none
corrections_made: none
remaining_manual_check: author_final_review_required_before_freeze

## Scope

The check covered `IAG-JP-FRAME-001` and `IAG-JP-001` through `IAG-JP-021` against the Aozora Bunko electronic text of 芥川龍之介「藪の中」, section 「巫女の口を借りたる死霊の物語」.

The selected range begins with 「妻はおれがためらう内に」 and ends with 「中有の闇へ沈んでしまった」. The Aozora text continues with trailing ellipsis marks after the final sentence; the selected packet ends before those trailing marks by design.

## Findings

- omitted_punctuation_changing_meaning: none found
- repository_modernisation: none found
- accidental_kanji_substitution: none found
- lost_quotation_marks: none found
- altered_dashes: none found
- kojima_translation_text_imported: none found

## Boundary

This is a draft exactness audit for author review. It is not a freeze manifest, does not create `source_manifest.csv`, `gloss_manifest.csv`, `SHA256SUMS.txt`, or `frozen_packet.zip`, and does not authorise annotation.
