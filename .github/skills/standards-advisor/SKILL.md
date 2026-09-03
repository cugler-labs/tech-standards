---
name: standards-advisor
description: Advises on applicable org technical standards during planning, implementation, or review, citing specific STD-* standards by ID and reporting checklist compliance. Use when the user says 'check standards', 'which standards apply', 'standards review', or is designing/implementing something a standard in the corpus covers (e.g. logging format, API design).
---

# Standards Advisor

## Overview

Read-only advisor over the org's technical standards corpus at `{skill-root}/standards/`. It does not author, edit, or gate a standard — it identifies which standards apply to the work at hand, cites them by ID, and reports which checklist assertions are met, violated, or can't be determined from what's visible. Every finding in this phase is advisory: a `must`-severity violation is flagged clearly but never blocks anything.

## Resolution rules

- `{skill-root}` → this skill's installed directory (where this SKILL.md lives).
- `{project-root}` → the project the skill is running in.

**Args:** `setup` or `configure` always (re)runs module registration, regardless of whether it's already registered.

## On Activation

1. If the user passed `setup` or `configure`, load `./assets/module-setup.md` and complete registration, then continue below. Otherwise, check whether `{project-root}/_bmad/config.yaml` has a `stds` section — if it does not, load `./assets/module-setup.md` and complete registration first (this is a one-time step on first use in a project).
2. Read `{skill-root}/standards/index.yaml` — the catalog of every standard (`id`, `title`, `status`, `version`, `path`, `checklist`, `applies_to`).
3. From the work under discussion (code, spec, plan, or PR), determine which standards' `applies_to` matches. If it's ambiguous which standards are in scope, ask rather than guessing.
4. For each applicable standard, read its full `.md` file at `{skill-root}/standards/{path}` (not just the title from the catalog) and its checklist at `{skill-root}/standards/{checklist}`.
5. Evaluate each checklist assertion against the visible work and classify it as **met**, **violated**, or **undeterminable** (not enough visible to judge — say what's missing to judge it). Always cite the standard ID and assertion ID together (e.g. `STD-LOG-001 / LOG-001-b`). Never state a MUST requirement without naming the standard it comes from.
6. Report grouped by severity: `must` violations first, then `should` items, then undeterminable items. Do not block or refuse to proceed on a `must` violation — flag it and continue.

## What this skill is not

Not a linter and not a gate. A later gating phase wires these same checklist files into CI so `must` items fail a build automatically — this skill only reports what a human or another agent should act on. See each checklist's `severity` field for what a future gate will enforce.
