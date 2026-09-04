# Release v0.1.0-alpha.2

## Internal testing prerelease

This release improves the internal installation and discovery path for the technical standards advisor. It is intended for company teams testing BMAD installation from a pinned GitHub release and, where applicable, Claude-style marketplace discovery.

This release is not final. The standards remain advisory and are still marked `draft`.

## Included

- The unchanged `standards-advisor` module and standards snapshot from `v0.1.0-alpha.1`.
- GitHub installer instructions using BMAD's `--custom-source` and `--pin` options.
- `.claude-plugin/marketplace.json` for company-only Claude marketplace discovery.
- Clarification that BMAD module installation and Claude marketplace discovery are separate mechanisms.

## Consumer reference

Pin the exact prerelease tag:

```text
v0.1.0-alpha.2
```

Install the BMAD module with:

```bash
npx bmad-method install \
  --custom-source https://github.com/cugler-labs/tech-standards.git \
  --pin stds=v0.1.0-alpha.2
```

Do not consume `main` for testing. The tag is the reproducible snapshot under evaluation.

## Testing requested

Internal teams should verify that they can:

- install the private module from the tagged repository;
- authenticate without placing credentials in the repository URL;
- see the self-registration assets under `.github/skills/standards-advisor/`;
- use `Which standards apply here?` or `Check standards` after installation;
- discover the Claude marketplace manifest if that integration is enabled; and
- report installation, discovery, or standards interpretation problems.

## Final-release policy

A final release may be created only when every catalog entry has `status: approved` or `status: deprecated`. The current catalog contains two `draft` standards, so this candidate must not be promoted to a final release yet.
