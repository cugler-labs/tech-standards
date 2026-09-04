# Consuming the Standards

Downstream BMad projects consume the technical standards through an immutable Git release tag. Do not point a project at `main` for normal use.

## Internal pilot

The current pilot release is:

```text
v0.1.0-alpha.2
```

Use that exact tag when installing the `standards-advisor` skill through the BMAD custom source. The release snapshot contains the standards catalog, standard documents, and checklists that were reviewed for this candidate. Do not copy the development tree directly: its `standards` path is a local-development link, not the portable consumer snapshot.

The pilot is advisory only. `STD-LOG-001` and `STD-API-001` remain `draft`, so consuming teams should use the advisor to identify applicable guidance and report unclear requirements or packaging problems. They must not treat the findings as mandatory policy.

## Update to a later release

When a new tag is published, update deliberately to the new tag and review its release notes. Do not silently follow the default branch.

```text
vMAJOR.MINOR.PATCH
vMAJOR.MINOR.PATCH-alpha.N
vMAJOR.MINOR.PATCH-beta.N
vMAJOR.MINOR.PATCH-rc.N
```

Record the selected tag in the consuming project's setup or dependency documentation so the standards version is auditable.

## Final releases

A final release is allowed only when every entry in `standards/index.yaml` has either:

```yaml
status: approved
```

or:

```yaml
status: deprecated
```

Any `draft`, `advisory`, `gating`, missing, or unknown status blocks final-release creation. A deprecated standard may remain in the catalog, but its retirement must be visible in the release notes.

## Using the advisor

After installing the tagged snapshot, ask the BMad advisor:

```text
Which standards apply here?
```

or:

```text
Check standards
```

The advisor reads the tagged catalog and reports findings by standard ID and checklist assertion ID. For example: `STD-LOG-001 / LOG-001-b`.
