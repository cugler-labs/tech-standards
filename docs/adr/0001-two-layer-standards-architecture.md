# ADR 0001: Separate the standards corpus from the BMAD delivery mechanism

- Status: accepted
- Date: 2026-09-03

## Context

We need to distribute org technical standards (API design, logging format,
etc.) so that agents (and eventually CI) can advise on and later gate
against them during planning and review. BMAD was chosen as the delivery
mechanism — distributed as a custom module from our internal Git host, no
new hosting infrastructure, and version pinning via SemVer tags gives us
"this build was made against vX" guarantees. MCP was considered and
rejected for now: it's infrastructure for problems we don't have yet.

The open question was where the actual standards *content* should live —
authored directly inside BMAD's skill format, or somewhere else.

## Decision

Split the repo into two layers:

- **`standards/`** (layer 1) — the tool-neutral source of truth. Plain
  Markdown standards (`STD-*.md`) with YAML front matter, a flat
  `index.yaml` catalog, and machine-checkable checklists
  (`checklists/*.check.yaml`) written with discrete, RFC-2119-tagged
  (MUST/SHOULD/MAY) assertions from day one — even while enforcement is
  advisory-only.
- **`skills/standards-advisor/`** (layer 2) — a thin BMAD skill that reads
  layer 1 and advises on it. It contains no standards content of its own;
  `skills/standards-advisor/standards` is a symlink back to the root
  `standards/` directory, not a copy.

We are a governance function with a multi-year horizon. BMAD may not be
the tool this org uses in three years; the standards corpus must outlive
it. Keeping the corpus in plain files with no BMAD-specific structure
means the same corpus can later feed a CI linter, a docs site, or an MCP
server without re-authoring anything — only a new thin adapter is needed,
same as layer 2 is for BMAD today.

Checklists exist from the start (not just prose) so that the move from
advisory to gating is a wiring change, not a content rewrite: the same
`checklists/*.check.yaml` file that `standards-advisor` reads for advice
today is what a future CI job runs to fail a build on `severity: must`
violations.

## Consequences

- Editing a standard's substance always happens in `standards/`, never
  inside `skills/standards-advisor/`. The skill folder should never
  accumulate standards content directly — if it does, the split has been
  violated and should be corrected.
- Distribution requires the symlink to become a real copy:
  `skills/standards-advisor/standards` works for local development because
  both directories are versioned together, while the Copilot installation
  under `.github/skills/` needs a self-contained snapshot. Packaging must
  rebuild that installation from `skills/` so it cannot drift from the
  source skill.
- New standards are added by creating a new `STD-*.md` + checklist pair
  and registering it in `standards/index.yaml`; they do not require any
  change to `skills/standards-advisor/SKILL.md` itself, since that skill
  reads the catalog generically rather than hardcoding standard IDs.
- Rollout controls (SemVer tags, pinned installs, `repoUrl` per consuming
  team for adoption auditing) apply to layer 2's packaging, not to layer 1
  directly — layer 1's own `version:` field in each standard's front
  matter is what a consuming team's pinned install snapshot actually
  reflects.

## Alternatives considered

- **Author standards directly as BMAD skill content.** Rejected: couples
  the governance artifact's lifespan to BMAD's, and blocks reuse by a
  future linter/docs site/MCP server without re-authoring.
- **MCP server now.** Rejected: real option later, but premature
  infrastructure investment for problems not yet encountered.
