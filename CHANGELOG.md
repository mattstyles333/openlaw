# Changelog

All notable changes to this project are documented in this file.

## 0.1.0 — 2026-08-30

First public release of Canon: always-on law for AI agents, stored as git
markdown, never retrieved. This is law, not memory SaaS. Example law is
**Northwind Coffee** (fictional). MIT licensed.

- Law files (`AGENTS.md`, `law/`, `decisions/`) plus CI that enforces
  them (`scripts/check-law.sh`, GitHub Actions, GitLab CI).
- Optional thin HTTP MCP projection with fail-closed bearer auth
  (`CANON_MCP_TOKEN` required; missing/wrong token is 401; no
  unauthenticated default; no SQL tool).
- Production `Dockerfile`: build-time `pip install`, non-root user,
  baked Northwind example law, HEALTHCHECK on `/health` with
  `Authorization: Bearer $CANON_MCP_TOKEN`.
- GHCR image `ghcr.io/mattstyles333/canon-mcp:0.1.0` (semver pin, no
  `v` prefix). Git tag `v0.1.0` publishes it; compose pins `:0.1.0`.
- Portainer-ready `docker-compose.yml`: that GHCR pin, port 8787 only,
  no bind-mount, no `pip install` at start, no postgres service.
- Website: Astro + Starlight on GitHub Pages at
  `https://mattstyles333.github.io/canon/` (Home, Why, Onboarding,
  Harness, Security, MCP/Portainer, Status).
- `llms.txt` (repo root and Pages) — what Canon is, what it is not,
  3-step onboard. Docs-only attach for Herdr, Grok Build, Cursor Grok
  Bot, Hermes, OpenCode, Portainer, GitHub Actions. Restart from zero:
  `scripts/reset-onboarding.sh`.
- Copy-paste **install prompts** per harness (README, onboarding, homepage,
  `llms.txt`). Paste into the agent. Done when `check-law.sh` exits 0.
