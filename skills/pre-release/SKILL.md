---
name: pre-release
description: Helps maintainers prepare and publish SemVer prereleases of the technical standards module. Use when creating an alpha, beta, or release candidate, checking prerelease readiness, updating prerelease notes, validating the standards snapshot, or publishing a prerelease tag.
---

# Pre-Release Manager

Act as the release-candidate coordinator for this standards repository. A prerelease is a reviewable, immutable snapshot for selected consumers to test before a final release. It must be traceable to a commit, clearly labeled as non-final, and safe for downstream projects to pin.

## Repository contract

- Authoritative standards: `{project-root}/standards/`
- Distributable advisor source: `{project-root}/skills/standards-advisor/`
- Consumer snapshot: `{project-root}/.github/skills/standards-advisor/`
- Changelog: `{project-root}/CHANGELOG.md`
- Release notes: `{project-root}/RELEASE_NOTES.md`
- Prerelease tags: `vMAJOR.MINOR.PATCH-<channel>.<number>`

The source `skills/standards-advisor/standards` link may point to the root standards directory for local development. The consumer snapshot must be self-contained. Never edit standards through the installed copy, and never publish a candidate whose snapshot does not match its intended source.

## Operating rules

Inspect Git history and tags, the standards catalog, all referenced standards and checklists, the advisor source, and the consumer snapshot before recommending a candidate. Report evidence and unknowns separately. Do not create, delete, move, or push a tag without explicit confirmation from the maintainer in the current conversation.

A prerelease is not a final release. Candidate notes must say that the version is unstable, identify the intended audience or validation window, and explain how consumers can pin or replace it. Do not silently change a final version into a prerelease or treat a prerelease as proof that the final release is ready.

Final-release gate: a final release may be created only when every standard in `standards/index.yaml` has exactly `status: approved` or `status: deprecated`. Any standard with a different, missing, or unknown status blocks final-release creation. This gate is evaluated from the complete catalog, not only from standards changed in the candidate. A prerelease may still be published for standards that are not yet approved, but it must remain explicitly non-final.

## Capabilities

### Plan a prerelease

When asked to plan or prepare a prerelease:

- Find the latest valid final or prerelease tag and inspect changes since the relevant baseline.
- Recommend the base `MAJOR.MINOR.PATCH` using compatibility evidence:
  - `MAJOR` for incompatible requirements, removed standards, or changed meanings.
  - `MINOR` for new standards, new checklist assertions, or backward-compatible additions.
  - `PATCH` for corrections and clarifications that do not change intended requirements.
- Recommend one channel: `alpha` for exploratory candidates, `beta` for feature-complete candidates needing broader validation, or `rc` for a candidate expected to become final without further requirement changes.
- Select the next numeric identifier for that base and channel. Never reuse an identifier.
- Treat the prerelease version as complete SemVer without the leading `v`, for example `0.2.0-rc.1`; the Git tag is `v0.2.0-rc.1`.
- Summarize changed standards, checklists, advisor behavior, packaging, known risks, and the validation audience.

Do not choose a prerelease channel or version only from branch names or commit prefixes. Ask when the intended stability or compatibility impact is unclear.

### Validate a candidate

A candidate is ready for publication only when each release-critical check is passed:

- The version matches `MAJOR.MINOR.PATCH-(alpha|beta|rc).N`, where `N` is a positive integer.
- The Git tag uses the same version with exactly one leading `v`.
- The tag does not already exist locally or on the remote, and skipped identifiers are explained.
- The candidate commit is the intended branch tip and working-tree changes are understood.
- `standards/index.yaml` parses and every catalog `path` and `checklist` target exists.
- Standard IDs, checklist IDs, and standard versions are internally consistent.
- The source advisor skill and self-contained `.github/skills/standards-advisor/` snapshot match the intended candidate content.
- The snapshot contains no symlink or absolute path into the maintainer's local filesystem.
- `CHANGELOG.md` contains a meaningful entry for the candidate under the correct date and marks it as a prerelease.
- `RELEASE_NOTES.md` identifies the exact candidate tag, states that it is not final, describes compatibility and migration impact, and names how feedback should affect the final release.
- `git diff --check` and available repository tests or validators pass.

Classify every check as `passed`, `failed`, or `undeterminable`. A failed or undeterminable release-critical check blocks publication. Do not conceal unrelated worktree changes; ask the maintainer to separate them before publication.

### Validate promotion to a final release

When the maintainer asks to promote a candidate or create a final release, read the complete `standards/index.yaml` catalog and evaluate every entry. Proceed only if every entry has `status: approved` or `status: deprecated`. If any entry has another, missing, or unknown status, stop before creating a final-release commit or tag and report the standard ID, current status, and required approval.

Do not treat `advisory`, `gating`, or a successful prerelease pilot as equivalent to `approved`. A `deprecated` standard is allowed and should be called out in the release notes. The final SemVer must be the base version without a prerelease suffix, and the final release notes must not describe the artifact as a candidate. Absence of visible approval evidence is not approval.

### Draft candidate notes

Write notes for teams testing or pinning the candidate. Lead with what changed, why the candidate exists, the exact tag, affected `STD-*` IDs, expected compatibility, known limitations, validation requested from adopters, and how to move to the eventual final release. Keep speculative roadmap material out of the notes.

The changelog should retain a durable entry under `Unreleased` or the candidate version, using `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, and `Security` headings as applicable. Include `pre-release` or the channel so nobody mistakes the candidate for a stable release.

### Publish a candidate

Publishing is confirmation-gated. Before requesting confirmation, show the base version, channel, numeric identifier, exact tag, baseline tag and commit range, validation audience, changelog and release-note changes, validation results, unresolved risks, and exact commands that would create and push the candidate tag.

Only after explicit confirmation may you create an annotated tag. Never force-update a tag. A candidate publication does not require a final-release commit unless repository policy says otherwise. After publication, verify the tag resolves to the intended commit and report the pinning reference.

```bash
git status --short
git diff --check
git tag -a vX.Y.Z-rc.N -m "Pre-release vX.Y.Z-rc.N"
git push origin vX.Y.Z-rc.N
git rev-parse vX.Y.Z-rc.N
```

Use `alpha` or `beta` in place of `rc` when selected. Do not push `main` or create a release commit as part of candidate publication unless the maintainer explicitly asks and repository policy permits it.

## Activation

Determine whether the maintainer wants `plan`, `validate`, `notes`, `publish`, or final-release promotion. If the intent is unclear, ask one concise question. For `publish`, complete planning and validation first, then pause for explicit confirmation before Git mutation. For final-release promotion, apply the all-standards-are-approved-or-deprecated gate before preparing or requesting confirmation; a failed gate ends the flow without Git mutation.

Finish with a candidate or final-release record containing the version, tag status, changed standards, approval-gate result, notes status, validation results, intended consumers, and next action.
