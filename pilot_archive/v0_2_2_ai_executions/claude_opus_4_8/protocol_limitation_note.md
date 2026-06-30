# Protocol Limitation Note

Only the Claude coding CSV was available locally. The expected question log, language-access form, return manifest, and protocol-deviation note were not available at `/mnt/data/claude_submission/` or in the thread workspace.

Consequences:

- the execution cannot be treated as a locked complete submission;
- package-hash confirmation cannot be verified;
- question-log timing and completeness cannot be assessed;
- language-access self-report cannot be assessed;
- question/annotation consistency warnings cannot be run against an actual log;
- AI-AI question-log comparison cannot be produced.

This limitation does not affect the frozen v0.2.2 package. It only limits what can be inferred from this local AI execution archive.
