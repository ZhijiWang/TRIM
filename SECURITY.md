# Security Policy

## Supported status

TRIM-HAA is alpha research software. The current supported development line is
the latest `main` revision and the `0.3.0a1` package series. Frozen research
artifacts remain immutable evidence and are not silently patched in place.

## Reporting a vulnerability

Do not include credentials, private packet text, participant information,
unreleased source material, or other sensitive data in a public issue.

Report security concerns privately through GitHub's security-advisory workflow
for `ZhijiWang/TRIM` when available. If that workflow is unavailable, open a
minimal public issue requesting a private contact channel without disclosing
the sensitive details.

## Scope boundaries

- The installed package contains no live model-provider adapter.
- Source-checkout study scaffolds remain blocked and are excluded from wheel
  and sdist.
- A preparation-gate pass is not execution or human-coding authorization.
- Content-rights concerns are documented separately in
  `THIRD_PARTY_AND_CONTENT_RIGHTS.md`.

Security fixes to frozen or tagged artifacts require a new version or an
external correction record; checksummed historical files must not be silently
rewritten.
