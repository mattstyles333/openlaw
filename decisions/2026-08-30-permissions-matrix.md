---
date: 2026-08-30
owner: openlaw-maintainers
status: proposed
supersedes:
---

# Harness permissions are a ranked list in law/

## Context

Openlaw attaches to several harnesses (Herdr / Grok Build, Cursor Grok
Bot, Hermes, OpenCode, Claude Code, Gemini CLI, and OpenClaw as a stub).
Who may merge law vs who may only propose was implied by `CODEOWNERS`
but was not a single always-on file. A three-column capability matrix is
more ceremony than the rule needs. A dashboard role, a plugin SDK, or
an agent auto-write would be the wrong shape. The permission model must
stay git markdown and stay easy to edit.

## Decision

Add `law/permissions.md` as a **ranked list**. Higher rank = more
authority. Top ranks may merge; merge is still **CODEOWNERS / human**.
The CODEOWNERS parent is the only merge path. Lower ranks read + propose
only via PR. Agents never auto-merge `law/` or `AGENTS.md`. OpenClaw is
a stub.

CI (`scripts/check-law.sh`) requires the file, a numbered ranked list,
and the CODEOWNERS parent merge rule. `docs/SECURITY-MODEL.md` and
`docs/HARNESS.md` point at the ranked list.

This does not change who owns law. It names the existing rule in a
place agents load.

## Consequences

- Always-on law stays a file. No SQLite brain, no plugin SDK, no
  auto-write of law.
- Missing `law/permissions.md`, missing ranked list, or missing
  CODEOWNERS parent wording fail CI.
- Changing authority is editing the numbered list and the cutoff.
- A full OpenClaw attach is out of scope; the stub is enough.
- Marking this ADR `decided` does not itself rewrite `law/constraints.md`;
  the ranked list *is* the law this decision adds.

See also the product README: [../README.md](../README.md).
