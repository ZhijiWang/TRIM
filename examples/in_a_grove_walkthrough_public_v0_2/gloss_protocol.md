# Japanese-Canonical / English-Gloss Protocol v0.1

Status: `author_reviewed_frozen_text_layer`

## Governing rule

The Japanese text is the only canonical evidence layer. The English gloss is an accessibility aid. Annotation records must cite Japanese segment IDs and must not treat English wording as an independent evidential source.

## Source

The Japanese text is drawn from the Aozora Bunko electronic text of Akutagawa Ryūnosuke's 「藪の中」, first published in 1922. The selected passage is from 「巫女の口を借りたる死霊の物語」.

The source heading itself is preserved as `IAG-JP-FRAME-001`. This provides a citable canonical anchor for the mediated status of the testimony rather than replacing the frame with researcher-authored description.

## Segmentation

Segments are divided by narrated action, perceptual transition, or evidentially material change. The same granularity rule is applied across the packet rather than only to the later unidentified intervention.

In particular, the self-stabbing sequence and the final unidentified-intervention sequence are both divided into separate anchors for action, bodily response, perceptual transition, and final state. This segmentation was completed before any new author or model record and must not be adjusted to reproduce an earlier disagreement.

The segmentation was designed afresh from the Japanese text and does not preserve the earlier Kojima-based English segmentation.

## Gloss principles

The English gloss should:

- remain close to Japanese clause order where readable;
- preserve omitted or unidentified agents rather than supplying identities;
- retain epistemic markers such as `らしい`;
- preserve revisions of perception such as `いや`;
- avoid adding causal relations not stated in Japanese;
- avoid converting bodily or religious language into a settled factual interpretation;
- distinguish `太刀` from `小刀`;
- record consequential alternatives in a translation note;
- remain explicitly non-authoritative.

## Key decisions

- `太刀` is glossed as “long sword.”
- `小刀` is glossed as “dagger.” The two weapons remain distinct.
- `今度はおれの身の上だ` is glossed as “Now it is my turn,” avoiding an added obligation of self-protection.
- `腥い塊` is glossed as “some raw-smelling mass,” retaining both sensory quality and substantial form without reducing it to blood alone.
- `誰か` remains “someone” throughout.
- `見えない手` is glossed as “a hand I could not see,” without deciding whether the phrase is perceptual, figurative, or supernatural.
- `もう杉や竹も見えない` is glossed with “now,” not “soon.”
- `中有` is retained as *chūu* and explained as an intermediate post-death state rather than translated away.

## Assistance and responsibility

Initial gloss drafting and consistency checking were AI-assisted. Zhiji Wang reviewed and approved the public research gloss and segmentation on 2026-07-01 and remains responsible for the frozen text layer.

## Freeze boundary

This text layer was frozen on 2026-07-01. Any textual or segmentation change requires a new version and regenerated manifests.

A new author analytic record may now be created from the frozen Japanese segment IDs. A new AI record may not be created until the author record has been completed and locked.
