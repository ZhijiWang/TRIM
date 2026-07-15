# Third-Party and Content Rights

This file describes the repository's content-rights boundary. It is a
navigation and disclosure record, not legal advice and not a determination of
copyright status in every jurisdiction.

## Root license boundary

The root MIT license applies to original TRIM-HAA software code and original
repository material only to the extent that the author has the rights required
to license that material. It does not automatically relicense third-party
texts, translations, quotations, externally licensed material, or other
incorporated content.

Users must consult the component-specific provenance, rights, and usage notices
before copying or redistributing non-software content.

## Component summary

| Component | Rights status and required handling |
|---|---|
| TRIM-HAA software in `src/trim_haa/` | Original software released under the root MIT license. |
| Repository documentation and author-created research materials | Covered by the root license only to the extent the author has rights to license the particular material. Embedded quotations and referenced third-party content retain their own status. |
| Public-domain source texts | Public-domain status is source- and jurisdiction-specific. Use the provenance and rights record associated with each text; repository presence alone is not evidence of worldwide public-domain status. |
| Aozora-derived Japanese text in the public walkthrough v0.2 | Governed by the recorded Aozora source provenance and usage-guidance record. See `examples/in_a_grove_walkthrough_public_v0_2/source_provenance.md` and `aozora_usage_guidance_record.md`. These records document the project's basis and do not constitute legal advice. |
| Author-created English glosses | Non-authoritative research aids created for the walkthrough. They do not relicense the underlying source work or any third-party translation. |
| Model-generated outputs | Preserved for provenance-aware technical demonstrations where present. Provider terms, source-content rights, and component-specific notices may also apply; the root MIT license does not independently resolve those questions. |
| Frozen In a Grove Public Walkthrough v0.2 | A tagged technical demonstration with its own provenance, claim-boundary, and checksum records. Frozen files must not be silently replaced under the same version. |
| Older author-only English In a Grove walkthrough in `examples/in_a_grove_walkthrough/` | **`NOT_AUTHORIZED_FOR_UNRESTRICTED_REDISTRIBUTION`**. Its legal review records unresolved rights in the English translation. Its presence in the Git repository or Git history does not establish permission to redistribute that translation. |
| Research artifacts and ZIP packages | Consult each manifest, provenance record, source notice, and checksum sidecar. A ZIP's presence does not enlarge rights in third-party material contained or referenced by it. |

## Older English walkthrough

The older author-only walkthrough must not be treated as a generally
redistributable release asset. Its existing legal review remains authoritative
for its unresolved status and must not be rewritten to imply approval.

The Python wheel and sdist exclude repository examples. Manually assembled
public release bundles must also exclude `examples/in_a_grove_walkthrough/`
until a separate rights review resolves its active-tree and redistribution
status. A complete Git clone and GitHub's automatically generated source
snapshots still contain every tracked file at the selected commit, including
that directory.

See `docs/alpha_release_procedure.md` for the distinction between distribution
artifacts and full repository snapshots.
