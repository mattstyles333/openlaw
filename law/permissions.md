# Harness permissions

Who may **read** law, **propose** ADRs, and **merge** law is this matrix —
not a dashboard role, not a plugin SDK, not an agent auto-write of law.

**Parent/merge is CODEOWNERS / human.** Agents never auto-merge `law/` or
`AGENTS.md`. The CODEOWNERS parent is the only merge path.

| Harness | read | propose | merge |
| --- | --- | --- | --- |
| Herdr/Grok Build | yes | yes | no — CODEOWNERS / human |
| Cursor Grok Bot | yes | yes | no — CODEOWNERS / human |
| Hermes | yes | yes | no — CODEOWNERS / human |
| OpenCode | yes | yes | no — CODEOWNERS / human |
| Claude Code | yes | yes | no — CODEOWNERS / human |
| Gemini CLI | yes | yes | no — CODEOWNERS / human |
| OpenClaw (stub) | yes | yes | no — CODEOWNERS / human |

## Notes

- **read**: load `AGENTS.md` and `law/` (working tree preferred; optional MCP is a projection of git).
- **propose**: open an ADR under `decisions/` with `status: proposed`. Any listed harness may propose. Proposals are not law until merged.
- **merge**: only the humans listed in `CODEOWNERS`. Never an agent, never CI, never auto-write.
- OpenClaw is a **stub** row only. A full attach is not this file.
- Retrieval, memory products, and SQLite stores are not a permission model. This file is.
