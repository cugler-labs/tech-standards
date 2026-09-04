# Tech Standards

Org technical standards, distributed as a BMAD module so agents can advise
on (and later gate against) them during planning and review.

- [`standards/`](standards/) — the standards themselves: tool-neutral
  Markdown + checklists. This is the source of truth. Edit here.
- [`skills/standards-advisor/`](skills/standards-advisor/) — the BMAD skill
  that reads `standards/` and advises on it. Contains no standards content
  of its own.
- [`skills/release-manager/`](skills/release-manager/) — the maintainer skill
  for SemVer releases, changelog and release-note preparation, snapshot
  validation, and confirmation-gated publication.
- [`skills/pre-release/`](skills/pre-release/) — the maintainer skill for
  alpha, beta, and release-candidate validation and publication.
- [`.github/skills/`](.github/skills/) — the GitHub Copilot skill installation.

Why it's split this way, and what that means for adding a new standard or
distributing this module: [docs/adr/0001-two-layer-standards-architecture.md](docs/adr/0001-two-layer-standards-architecture.md).

For downstream installation and version pinning, see
[docs/consuming-standards.md](docs/consuming-standards.md).
For the step-by-step BMAD command, see
[docs/installer-guide.md](docs/installer-guide.md).

Use `pre-release` to validate an alpha, beta, or release candidate before
using `release-manager` to prepare and publish a stable SemVer tag.
