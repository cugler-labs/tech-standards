---
id: STD-LOG-001
title: Structured Logging Format
status: draft
version: 0.1.0
owners: [platform-standards]
applies_to: [services, cli-tools, background-jobs]
supersedes: []
checklist: checklists/STD-LOG-001.check.yaml
---

# STD-LOG-001: Structured Logging Format

## Purpose

Logs are the primary signal for debugging production incidents and for
building cross-service tracing. Free-text logs cannot be reliably parsed,
correlated, or alerted on at scale. This standard defines the minimum shape
every log line MUST have so that any service's logs can be ingested,
queried, and joined with logs from any other service without per-service
parsing rules.

## Requirements

### Format

1. Log output MUST be a single JSON object per line (newline-delimited JSON,
   no pretty-printing) when written to stdout/stderr or a log file.
2. A log line MUST NOT span multiple lines. Multi-line payloads (e.g. stack
   traces) MUST be encoded as a JSON string field with embedded `\n`.

### Required fields

Every log line MUST include:

| Field       | Type   | Description                                              |
|-------------|--------|-----------------------------------------------------------|
| `timestamp` | string | ISO 8601, UTC, millisecond precision (e.g. `2026-09-03T14:22:01.123Z`) |
| `level`     | string | One of `debug`, `info`, `warn`, `error`, `fatal` (lowercase) |
| `service`   | string | The service/app name emitting the log, matching its deploy manifest name |
| `message`   | string | Human-readable summary, free text                        |

### Conditionally required fields

3. If the log line is emitted within a traced request, it MUST include
   `trace_id` (string) so it can be correlated across services.
4. If the log line is emitted while handling an error or exception, it MUST
   include `error.message` and `error.stack` (or the language's nearest
   equivalent) as nested fields under an `error` object, not flattened into
   `message`.

### Recommended fields

5. Log lines SHOULD include `context` as a nested object for
   request-specific structured data (user id, resource id, etc.) rather than
   interpolating that data into `message`.
6. Log lines SHOULD include `env` (`prod`, `staging`, `dev`) when the
   logging pipeline does not already tag this at the transport level.

### Prohibitions

7. Log lines MUST NOT contain secrets, tokens, passwords, or full payment
   card numbers in any field, including `context` and `error`.
8. Services MUST NOT use `console.log`/`print`/equivalent raw stdout calls
   for anything other than local development scratch debugging that is
   removed before merge.

## Non-goals

This standard does not mandate a specific logging library, transport, or
retention policy — only the wire format of the emitted line. It also does
not cover metrics or traces as separate telemetry types.

## Rationale

RFC 2119 keywords are used deliberately: MUST items are what the checklist
enforces mechanically; SHOULD items are advised but not gated, since some
services have legitimate reasons to omit them (e.g. no per-request context
to attach).
