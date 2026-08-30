# Canon

Memory products retrieve similar chunks and hope the agent obeys. Canon is **always-on law**: short git markdown in context every session, locked by CI. If it is not in git, it is not policy.

Open source. MIT. Free forever. Self-hosted, local-first. Self host it. No SaaS. No vendor lock-in.

Not a memory SaaS. Not a new agent OS. Optional MCP is an HTTP projection of git, not a brain. Law lives in `AGENTS.md`.

Fork it. Replace `law/`. Teaching example: fictional **Northwind Coffee**.

Website: [mattstyles333.github.io/canon](https://mattstyles333.github.io/canon/) ·
[Onboarding](https://mattstyles333.github.io/canon/docs/onboarding/) ·
[llms.txt](llms.txt) ·
[MIT](LICENSE)

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

Docs-only attach (Herdr, Grok Build, Cursor Grok Bot, Hermes, OpenCode, Portainer, GitHub Actions): [onboarding](https://mattstyles333.github.io/canon/docs/onboarding/).

## CI is the lock

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

## Restart from zero

Law is git, not a vector store. Wipe the *harness session*, then re-read `AGENTS.md` from disk.

```bash
bash scripts/reset-onboarding.sh
```

That restores teaching Northwind law and prints wipe commands for Herdr / Grok Build, Cursor Grok Bot, Hermes, and OpenCode.

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
llms.txt                  what it is / is not / 3-step onboard
site/                     Astro + Starlight (GitHub Pages)
Dockerfile                production MCP image
docker-compose.yml        Portainer stack, GHCR :0.1.0
scripts/check-law.sh      local CI
scripts/reset-onboarding.sh   restore Northwind; print harness wipes
```

## License

[MIT](LICENSE) © 2026 Canon contributors. Open source. Free forever.
