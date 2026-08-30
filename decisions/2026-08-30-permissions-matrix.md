---
date: 2026-08-30
owner: openlaw-maintainers
status: proposed
supersedes:
---

# Harness permissions matrix lives in law/

## Context

Openlaw attaches to several harnesses (Herdr / Grok Build, Cursor Grok
Bot, Hermes, OpenCode, Claude Code, Gemini CLI, and OpenClaw as a stub).
Who may **read** law, **propose** ADRs, and **merge** law was implied by
`CODEOWNERS` and `docs/SECURITY-MODEL.md` but was not a single always-on
file. A dashboard role, a plugin SDK, or an agent auto-write would be
the wrong shape. The permission model must stay git markdown.

## Decision

Add `law/permissions.md` as a harness × capability matrix with columns
**read**, **propose**, and **merge**. Every listed harness may read and
propose. Parent/merge is **CODEOWNERS / human**. Agents never auto-merge
`law/` or `AGENTS.md`. OpenClaw is a stub row only.

CI (`scripts/check-law.sh`) requires the file and greps it for those
needles so the matrix cannot silently disappear. `docs/SECURITY-MODEL.md`
and `docs/HARNESS.md` point at the file.

This does not change who owns law. It names the existing rule in a
place agents load.

## Consequences

- Always-on law stays a file. No SQLite brain, no plugin SDK, no
  auto-write of law.
- Missing `law/permissions.md` or missing needles fail CI.
- A full OpenClaw attach is out of scope; the stub row is enough.
- Marking this ADR `decided` does not itself rewrite `law/constraints.md`;
  the matrix file *is* the law this decision adds.

See also the product README: [../README.md](../README.md).
