# Tech Standards Repository

This repository contains organization-wide technical standards and the BMad standards-advisor skill that explains how to apply them.

## Source Of Truth

- `standards/` contains the authoritative standards, their catalog, and checklists.
- `skills/standards-advisor/` is the distributable source skill. Keep it tool-neutral and keep standards content out of the skill package.
- `.github/skills/` contains the GitHub Copilot skill installation.
- `docs/adr/` records architectural decisions about the repository and distribution model.

## Working With Standards

When a task concerns an API, logging, or another area covered by the catalog, use the `standards-advisor` skill. Read `standards/index.yaml`, then the complete applicable standard and checklist. Cite findings with both the standard ID and checklist assertion ID. Classify each assertion as met, violated, or undeterminable from the visible work.

The standards advisor is advisory: report violations and continue working. Do not invent requirements, treat missing evidence as compliance, or edit standards while advising on implementation work.

## Change Guidelines

- Edit standards in `standards/`, not in an installed skill copy.
- Keep checklists synchronized with their corresponding standard.
- Preserve the two-layer architecture documented in `docs/adr/0001-two-layer-standards-architecture.md`.
- Keep changes focused and validate Markdown, YAML, and skill structure before committing.