# AI Execution Pipeline Note

Two machine-executed protocol runs were planned before human deployment to test
package completeness, submission handling, and the planned comparison pipeline.
These runs are treated as software and protocol stress tests rather than
intercoder evidence. Their substantive annotations are not pooled with the human
retest dataset.

Current verified status:

- v0.2.1 Codex raw execution: expected ZIP filename and user-supplied SHA-256
  were documented, but the actual ZIP was not locally readable in this
  workspace.
- v0.2.2 Claude Opus 4.8 execution: complete five-file bundle found through the
  attached local archive and structurally validated.

The available AI execution materials helped verify:

- complete v0.2.2 submission-bundle ingestion;
- v0.2.2 field operability for one machine-filled return;
- source-segment and shared-context validation;
- return-manifest package-hash checking;
- question-log validation and question/annotation consistency checking;
- missing Codex-submission transparency;
- uncertainty and alternative-signature descriptive reporting;
- pathway-classification helper tests.

They do not verify:

- human usability;
- human intercoder reliability;
- cross-language validity;
- final package burden;
- human question-log timing in practice;
- substantive interpretation quality.

Because the Codex ZIP was not locally verifiable, Codex-Claude common-field
agreement, evidence-overlap, pathway-classification, and question-log
comparison metrics were not computed. Those metrics may be generated only after
both raw AI execution datasets are mounted or otherwise supplied in verifiable
form. Any such output remains exploratory technical evidence, not reliability
evidence.

Suggested article wording:

> Two machine-executed protocol runs were used before human deployment to test
> package completeness, submission handling, and the planned comparison
> pipeline. These runs were treated as software and protocol stress tests rather
> than intercoder evidence. Their substantive annotations were not pooled with
> the human retest dataset.
