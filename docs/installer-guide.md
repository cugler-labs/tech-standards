# Install the Company Standards Advisor

This guide explains how to install the internal `standards-advisor` BMAD module from a GitHub release tag.

The module is hosted in the private repository:

```text
https://github.com/cugler-labs/tech-standards.git
```

The current internal testing release is:

```text
v0.1.0-alpha.2
```

Use a release tag rather than `main` so every project receives a reproducible standards snapshot.

## Prerequisites

Install Node.js and confirm that the BMAD installer is available:

```bash
node --version
npx bmad-method --help
```

You must also have read access to the private `cugler-labs/tech-standards` repository. Authenticate using the company's approved GitHub method, such as GitHub CLI, SSH, or your organization's credential manager. Never put a GitHub token in the repository URL or in project configuration.

## Install BMAD and the standards module

From the root of the consuming BMad project, run:

```bash
npx bmad-method install \
  --custom-source https://github.com/cugler-labs/tech-standards.git \
  --pin stds=v0.1.0-alpha.2
```

The `stds` value is the module code from `skills/standards-advisor/assets/module.yaml`. The `--pin` option makes the selected release explicit and prevents the project from silently receiving changes from `main`.

If BMAD is already installed, the same command can be used to add or update the standards module. Review the installer output before accepting changes.

## Verify the installation

The consuming project should contain the standards advisor and its self-registration assets:

```text
.github/skills/standards-advisor/
  SKILL.md
  assets/module.yaml
  assets/module-help.csv
  assets/module-setup.md
  scripts/merge-config.py
  scripts/merge-help-csv.py
  standards/index.yaml
  standards/STD-API-001.md
  standards/STD-LOG-001.md
  standards/checklists/
```

The project configuration should also include module code `stds` in:

```text
_bmad/config.yaml
_bmad/module-help.csv
```

The installer may write personal settings to:

```text
_bmad/config.user.yaml
```

That file should remain protected according to the consuming project's repository policy.

## Use the advisor

Ask the BMad advisor:

```text
Which standards apply here?
```

or:

```text
Check standards
```

The advisor reads the tagged catalog, loads the applicable standards and checklists, and reports findings by standard ID and checklist assertion ID, for example:

```text
STD-LOG-001 / LOG-001-b
```

Findings are advisory in the pilot. The current standards are still marked `draft` and must not be treated as mandatory policy.

## Update to a later release

Update deliberately to a new immutable tag and review its release notes first:

```bash
npx bmad-method install \
  --custom-source https://github.com/cugler-labs/tech-standards.git \
  --pin stds=v0.1.0-alpha.2
```

Supported tag shapes include:

```text
vMAJOR.MINOR.PATCH-alpha.N
vMAJOR.MINOR.PATCH-beta.N
vMAJOR.MINOR.PATCH-rc.N
vMAJOR.MINOR.PATCH
```

Record the selected tag in the consuming project's setup or dependency documentation. Do not use `--next` or point the module at `main` for normal project work.

## Troubleshooting

### Private repository access fails

Confirm that your GitHub identity can read `cugler-labs/tech-standards` and that the Git URL is reachable. Do not work around an authorization failure by embedding credentials in the URL.

### The module is not discovered

Confirm that the command includes both options:

```bash
--custom-source https://github.com/cugler-labs/tech-standards.git
  --pin stds=v0.1.0-alpha.2
```

The repository is a custom module source; it is not part of the public BMAD module list.

### Claude marketplace discovery

This repository also contains `.claude-plugin/marketplace.json` for Claude-style
plugin discovery. That manifest is separate from BMAD's native module registry.
For BMAD projects, continue using `--custom-source` and `--pin` as shown above.

### The project installed the wrong version

Inspect the consuming project's BMAD configuration and confirm the module is pinned to `v0.1.0-alpha.2`. Re-run the install command with the desired tag. Do not edit the installed standards by hand.

### A final release is unavailable

A final release can be created only when every standard in `standards/index.yaml` has either `status: approved` or `status: deprecated`. `draft`, `advisory`, `gating`, missing, and unknown statuses block final-release creation. The current pilot is therefore intentionally prerelease-only.

## Related documents

- [Consuming the Standards](consuming-standards.md)
- [Release Notes](../RELEASE_NOTES.md)
- [Changelog](../CHANGELOG.md)
