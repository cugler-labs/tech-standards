---
id: STD-API-001
title: General API Design Principles
status: draft
version: 0.1.0
owners: [platform-standards]
applies_to: [services, public-apis, internal-apis]
supersedes: []
checklist: checklists/STD-API-001.check.yaml
source:
  name: Zalando RESTful API Guidelines — "General Guidelines" section
  url: https://opensource.zalando.com/restful-api-guidelines/#general-guidelines
  license: CC-BY 4.0
  adapted: true
  note: >
    Content below is adapted from Zalando's guidelines (rules 100, 101, 102,
    103, 234), generalized to remove Zalando-internal tooling and URLs.
    Attribution retained per CC-BY 4.0. Original rule numbers are cited in
    each requirement for traceability back to the source.
---

# STD-API-001: General API Design Principles

## Purpose

These are the foundational rules every API-producing team follows before
any endpoint-level design work starts. They exist to catch the most
expensive class of mistake — an API that ships without ever being
specified, reviewed, or written in a way other teams can consume — before
it happens, rather than fixing it after clients have integrated.

## Requirements

### 1. Follow an API-first workflow (source: Zalando #100, MUST)

Teams MUST:

1. Define the API contract (OpenAPI) *before* writing implementation code.
2. Design it consistently with this standards corpus, checked with
   whatever automated API-linting tooling the org provides.
3. Request review feedback from peers and prospective client-team
   developers *before* the API is considered final, for any API whose
   audience is not purely internal to the owning team.

### 2. Specify APIs using OpenAPI (source: Zalando #101, MUST)

1. Every API MUST have an OpenAPI specification as a single, self-contained
   file (prefer YAML for readability).
2. The specification MUST be version-controlled alongside (or referenced
   from) the service's source repository.
3. The specification MUST be published/accessible wherever the API is
   deployed, not just held locally by the authoring team.
4. Teams SHOULD default to the OpenAPI version the org's tooling supports
   most completely; if adopting a newer OpenAPI major version, teams MUST
   confirm compatibility with existing internal tooling first, since
   OpenAPI 3.1 changed Schema Object semantics (e.g. dropped `nullable` in
   favor of JSON Schema-native constructs) in ways that can silently break
   older linters/generators.

### 3. Provide a user manual for non-trivial APIs (source: Zalando #102, SHOULD)

Beyond the machine-readable spec, APIs intended for consumption by other
teams SHOULD ship a short manual covering:

- scope, purpose, and intended use cases
- concrete request/response examples
- known edge cases and error situations, with how to recover from them
- architectural context (what it depends on, what depends on it)

This SHOULD be linked from the OpenAPI spec's `externalDocs.url` field so
the two artifacts stay discoverable together.

### 4. Write APIs in a single, consistent language (source: Zalando #103, MUST)

All API elements — resource names, property names, descriptions, error
messages, enum values — MUST be written in U.S. English, including
spelling conventions (e.g. `color` not `colour`). This is a consistency
requirement, not a statement about client-facing localization, which is a
separate concern.

### 5. Keep specification references durable and immutable (source: Zalando #234, MUST)

1. OpenAPI specifications MUST be self-contained where practical. A
   specification MUST NOT reference external content by a mutable pointer
   (a branch ref, a `latest` tag, an editable wiki page, an arbitrary
   GitHub URL) where that content could change after the spec is published
   without the spec's own version changing.
2. Shared/reusable fragments MAY be referenced by URL only when that URL
   is guaranteed immutable per revision (e.g. a content-addressed or
   version-pinned internal spec repository). Org platform teams
   maintaining such a repository are responsible for that immutability
   guarantee.
3. Rationale: a spec that silently changes meaning because something it
   pointed to changed is worse than one that duplicates a little content,
   because it breaks the "this build was made against vX" guarantee the
   whole standards program depends on.

## Non-goals

This standard does not prescribe resource naming, HTTP method usage,
status codes, or payload formats — those are covered by other STD-API-*
standards. It also does not mandate a specific OpenAPI tooling vendor.

## Rationale

As with other standards in this corpus, MUST items are what a future
gating check gains authority over; SHOULD items remain advisory
indefinitely unless explicitly promoted.
