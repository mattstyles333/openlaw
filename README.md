# Canon

> Paste this into your coding agent to install Canon as always-on law.

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

## Install prompts

Paste this into your coding agent to install Canon as always-on law.

```
Install Canon as always-on law. Open source, MIT, self-hosted. Not a memory SaaS. Not a new agent OS.

1. Clone https://github.com/mattstyles333/canon.git (or fork). cwd MUST be the repo root: AGENTS.md and law/ exist.
2. Read AGENTS.md. Retrieval is not law. If it is not in git, it is not policy. Keep AGENTS.md under 80 lines / 12 KB with three hard rules inlined. Teaching example is fictional Northwind Coffee; replace law/ when adopting.
3. Turn CI on: run bash scripts/check-law.sh. Enable GitHub Actions (law-check, secret-scan, agent-security, mcp-test).
4. Optional MCP only if you cannot see the working tree: public HTTPS, fail-closed bearer. Never commit CANON_MCP_TOKEN. Pin ghcr.io/mattstyles333/canon-mcp:0.1.0. Example: grok mcp add --transport http https://YOUR-PUBLIC-MCP-HOST
5. You are done when bash scripts/check-law.sh exits 0.
```

### Herdr / Grok Build

```
You are a Grok Build / Herdr agent. Install Canon as always-on law.

1. cwd = this git repo. Clone https://github.com/mattstyles333/canon.git if needed. Herdr pane cwd MUST be the clone. Do not grok --resume an old session for a blank install.
2. Read AGENTS.md and law/. Retrieval is not law. If it is not in git, it is not policy.
3. Optional MCP: grok mcp add --transport http https://YOUR-PUBLIC-MCP-HOST with Authorization: Bearer $CANON_MCP_TOKEN — never commit the token; unset token must fail closed. Pin ghcr.io/mattstyles333/canon-mcp:0.1.0.
4. Turn CI on: bash scripts/check-law.sh and enable GitHub Actions (law-check, secret-scan, agent-security, mcp-test).
5. You are done when bash scripts/check-law.sh exits 0.
```

### Cursor Grok Bot

```
You are Cursor Grok Bot. Install Canon as always-on law.

1. Clone https://github.com/mattstyles333/canon.git into /workspace (the Bot workspace root). cwd is /workspace. Read AGENTS.md, law/, .cursor/rules/law.mdc (alwaysApply).
2. Retrieval is not law. If it is not in git, it is not policy.
3. Optional account-wide HTTP MCP on public HTTPS (not localhost, not tailnet, not stdio): URL https://YOUR-PUBLIC-MCP-HOST with Authorization: Bearer $CANON_MCP_TOKEN — never commit the token. Pin ghcr.io/mattstyles333/canon-mcp:0.1.0.
4. Human: enable GitHub Actions on the fork. Run bash scripts/check-law.sh if you have a shell.
5. You are done when bash scripts/check-law.sh exits 0.
```

### Hermes

```
You are Hermes. Install Canon as always-on law.

1. cwd = clone of https://github.com/mattstyles333/canon.git. Read AGENTS.md. Run bash scripts/excerpt-soul.sh and put stdout in SOUL.md. Leave memory.provider unset. Do not use MEMORY.md as law.
2. Optional HTTP MCP: public HTTPS https://YOUR-PUBLIC-MCP-HOST with Authorization: Bearer $CANON_MCP_TOKEN — never commit the token. Pin ghcr.io/mattstyles333/canon-mcp:0.1.0.
3. Turn CI on: bash scripts/check-law.sh and GitHub Actions.
4. You are done when bash scripts/check-law.sh exits 0.
```

### OpenCode

```
You are OpenCode. Install Canon as always-on law.

1. cwd = clone of https://github.com/mattstyles333/canon.git. Read AGENTS.md. Retrieval is not law.
2. Optional remote HTTP MCP: oauth false, URL https://YOUR-PUBLIC-MCP-HOST, Authorization: Bearer $CANON_MCP_TOKEN — never commit a live token in opencode.json. Pin ghcr.io/mattstyles333/canon-mcp:0.1.0.
3. Turn CI on: bash scripts/check-law.sh and GitHub Actions.
4. You are done when bash scripts/check-law.sh exits 0.
```

### Claude Code

```
You are Claude Code. Install Canon as always-on law.

1. cwd = clone of https://github.com/mattstyles333/canon.git. Read CLAUDE.md, then AGENTS.md and law/.
2. Optional HTTP MCP: public HTTPS https://YOUR-PUBLIC-MCP-HOST with Authorization: Bearer $CANON_MCP_TOKEN — never commit the token. Pin ghcr.io/mattstyles333/canon-mcp:0.1.0.
3. Turn CI on: bash scripts/check-law.sh and GitHub Actions.
4. You are done when bash scripts/check-law.sh exits 0.
```

### Gemini CLI

```
You are Gemini CLI. Install Canon as always-on law.

1. cwd = clone of https://github.com/mattstyles333/canon.git. Read GEMINI.md, then AGENTS.md and law/.
2. Optional HTTP MCP: public HTTPS https://YOUR-PUBLIC-MCP-HOST with Authorization: Bearer $CANON_MCP_TOKEN — never commit the token. Pin ghcr.io/mattstyles333/canon-mcp:0.1.0.
3. Turn CI on: bash scripts/check-law.sh and GitHub Actions.
4. You are done when bash scripts/check-law.sh exits 0.
```

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
