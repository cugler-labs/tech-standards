# Tech Standards

Org technical standards, distributed as a BMAD module so agents can advise
on (and later gate against) them during planning and review.

- [`standards/`](standards/) — the standards themselves: tool-neutral
  Markdown + checklists. This is the source of truth. Edit here.
- [`skills/standards-advisor/`](skills/standards-advisor/) — the BMAD skill
  that reads `standards/` and advises on it. Contains no standards content
  of its own.
- [`.github/skills/`](.github/skills/) — the GitHub Copilot skill installation.

Why it's split this way, and what that means for adding a new standard or
distributing this module: [docs/adr/0001-two-layer-standards-architecture.md](docs/adr/0001-two-layer-standards-architecture.md).
