# Canon

**Always-on law for AI agents. Git markdown. Never retrieved.**

Law, not memory. Not a runtime. Not a SaaS.

Fork it. Replace `law/`. Keep `AGENTS.md` short. Turn on CI — that is the lock. Optional MCP is a projection of git, not the source of truth.

Website: [mattstyles333.github.io/canon](https://mattstyles333.github.io/canon/) ·
[Onboarding](https://mattstyles333.github.io/canon/docs/onboarding/) ·
[Why](docs/WHY.md) ·
[Security](docs/SECURITY-MODEL.md) ·
[Harness](docs/HARNESS.md) ·
[MIT](LICENSE)

The teaching example is **Northwind Coffee** (fictional). Replace it.

## Quickstart

```bash
git clone https://github.com/mattstyles333/canon.git
cd canon
# Replace law/ with yours. Inline three hard rules in AGENTS.md (max 80 lines / 12 KB).
bash scripts/check-law.sh
```

Hard rules (template — replace the needles in `scripts/check-law.sh` on fork):

- MUST never invent company policy
- always-on law is git markdown, never a vector store
- MUST propose decisions; do not edit law/constraints.md without review

Specialists propose ADRs in `decisions/` (`status: proposed`). Owners in `CODEOWNERS` merge. Do not silently edit `law/constraints.md`.

## CI gates

```bash
bash scripts/check-law.sh
cd mcp && python -m pytest tests
```

On push/PR: **law-check**, **secret-scan**, **agent-security**, **mcp-test**.  
On tag `v*`: GHCR image. On push to `main`: GitHub Pages.

Agents will rewrite policy if you let them. CI is how you do not.

## Docker / Portainer

Pin: `ghcr.io/mattstyles333/canon-mcp:0.1.0` (semver, no `v`).

```bash
export CANON_MCP_TOKEN=          # required; never commit
docker compose up -d             # stack file; port 8787
```

Portainer: stack name `canon-mcp`, paste `docker-compose.yml`, set `CANON_MCP_TOKEN` in the UI. Missing token fails closed. No postgres service. No bind-mount.

## Harness attach

The harness you already run loads this repo. You do not need a new agent OS.

| Harness | Law | MCP |
| --- | --- | --- |
| Grok Build | `AGENTS.md` | `grok mcp add --transport http` |
| Cursor Grok Bot | clone into `/workspace` | account-wide HTTP, public HTTPS |
| Herdr | pane cwd = repo | multiplexer, not a brain |
| OpenCode | `AGENTS.md` | remote HTTP, oauth false, bearer |
| Claude Code | `CLAUDE.md` → `AGENTS.md` | same HTTP MCP |
| Gemini CLI | `GEMINI.md` → `AGENTS.md` | same HTTP MCP |
| Hermes | short `SOUL.md` excerpt | leave `memory.provider` unset |

Recipes: [examples/](examples/). Matrix: [docs/HARNESS.md](docs/HARNESS.md).

## Layout

```
AGENTS.md                 always-on law (max 80 lines / 12 KB)
law/                      constraints, brand, SoR, priorities (Northwind)
decisions/                ADRs
mcp/                      optional HTTP projection
site/                     Astro + Starlight (GitHub Pages)
Dockerfile                production MCP image
docker-compose.yml        Portainer stack, GHCR :0.1.0
scripts/check-law.sh      local CI
```

## License

[MIT](LICENSE) © 2026 Canon contributors.
