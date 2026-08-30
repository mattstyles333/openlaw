# Changelog

All notable changes to this project are documented in this file.

## 0.2.0 — 2026-08-31

Minor product drop: ranked harness permissions, the propose → review →
merge loop, and a build-time ops one-pager. Live Portainer pin stays
`ghcr.io/mattstyles333/canon-mcp:0.1.0`.

- Ranked harness list in `law/permissions.md`. Rank 1 (Herdr / Grok
  Build) may merge only via CODEOWNERS / human; rank 2+ propose via PR.
  Agents never auto-merge `law/` or `AGENTS.md`. `check-law` requires
  the file, a numbered list, and the CODEOWNERS parent rule.
- Propose → review → merge: `scripts/propose.sh`, `docs/LEARNING.md`,
  PR template, `.github/workflows/pr-law-review.yml`. The pull request
  is the discussion room. Never auto-merge law.
- Build-time Tailwind ops one-pager at `/ops/`. Generated from git
  markdown and workflow YAML at `astro build`. No live database, no
  runtime GitHub fetch.

## 0.1.0 — 2026-08-30

First public release of Openlaw (display **Openlaw**, repo
`mattstyles333/openlaw`): always-on law for AI agents, stored as git
markdown, never retrieved. This is law, not memory SaaS. Example law is
**Northwind Coffee** (fictional). MIT licensed.

- Law files (`AGENTS.md`, `law/`, `decisions/`) plus CI that enforces
  them (`scripts/check-law.sh`, GitHub Actions, GitLab CI).
- Optional thin HTTP MCP projection with fail-closed bearer auth
  (`OPENLAW_MCP_TOKEN` required; missing/wrong token is 401; no
  unauthenticated default; no SQL tool).
- Production `Dockerfile`: build-time `pip install`, non-root user,
  baked Northwind example law, HEALTHCHECK on `/health` with
  `Authorization: Bearer $OPENLAW_MCP_TOKEN`.
- Live GHCR pin `ghcr.io/mattstyles333/canon-mcp:0.1.0` (do not delete).
  Planned image `ghcr.io/mattstyles333/openlaw-mcp`. Prefer
  `OPENLAW_MCP_TOKEN`; `CANON_MCP_TOKEN` is a deprecated alias.
- Portainer-ready `docker-compose.yml`: that GHCR pin, port 8787 only,
  no bind-mount, no `pip install` at start, no postgres service.
- Website: Astro + Starlight on GitHub Pages at
  `https://mattstyles333.github.io/openlaw/` (Home, Why, Onboarding,
  Harness, Security, MCP/Portainer, Status).
- `llms.txt` (repo root and Pages) — what Openlaw is, what it is not,
  3-step onboard. Docs-only attach for Herdr, Grok Build, Cursor Grok
  Bot, Hermes, OpenCode, Portainer, GitHub Actions. Restart from zero:
  `scripts/reset-onboarding.sh`.
- Copy-paste **install prompts** per harness (README, onboarding, homepage,
  `llms.txt`). Paste into the agent. Done when `check-law.sh` exits 0.
