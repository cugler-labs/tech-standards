# Release v0.1.0-alpha.1

## Internal pilot prerelease

This is an internal pilot snapshot of the technical standards advisor. It is intended for selected teams to test standards discovery, checklist interpretation, packaging, and the consumer workflow before a final release.

This release is not final. The standards remain advisory and are still marked `draft`.

## Included

- `STD-LOG-001` - Structured Logging Format
- `STD-API-001` - General API Design Principles
- `standards-advisor` for identifying applicable standards and reporting checklist findings
- `release-manager` and `pre-release` guidance for SemVer release preparation and validation

## Consumer reference

Pin the exact prerelease tag:

```text
v0.1.0-alpha.1
```

Do not consume `main` for the pilot. The tag is the reproducible snapshot under evaluation.

## Pilot validation requested

Pilot teams should verify that they can:

- install or copy the standards-advisor snapshot from the tagged repository;
- ask which standards apply to their work;
- understand findings cited by standard and checklist assertion ID;
- update to a later prerelease without relying on unversioned `main` content; and
- report unclear requirements, missing applicability categories, packaging problems, or unexpected consumer impact.

## Final-release policy

A final release may be created only when every catalog entry has `status: approved` or `status: deprecated`. The current catalog contains two `draft` standards, so this candidate must not be promoted to a final release yet.

Feedback from the pilot should be addressed in a later prerelease or documented as accepted risk before approval and final-release promotion.
