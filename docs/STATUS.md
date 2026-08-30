# Openlaw v0.1 status

Always-on law for AI agents, stored as git markdown, never retrieved.
This is law, not memory. The example company in the template is
**Northwind Coffee** (fictional). Replace `law/` on fork.

Website: [mattstyles333.github.io/openlaw](https://mattstyles333.github.io/openlaw/).

Git is the source of truth. CI is the agent security layer. Optional MCP
is a projection of git. Herdr is a multiplexer, not a brain.

## Local CI

```bash
bash scripts/check-law.sh
bash scripts/excerpt-soul.sh    # Hermes SOUL.md block, stdout only
```

`check-law.sh` caps `AGENTS.md` (80 lines / 12 KB), greps the three
hard-rule needles, checks ADR frontmatter, rejects secret patterns in
`law/` and `AGENTS.md`, requires CODEOWNERS coverage, and (because
`mcp/server.py` exists) asserts fail-closed auth and no `execute_sql`.

Adopters replace the example needles in `scripts/check-law.sh` with
their own. GitHub Actions and GitLab CI run law-check, secret-scan
(gitleaks container, no action license), agent-security, and mcp-test.

## MCP smoke

Bearer required. `CANON_MCP_TOKEN` has no default; the server refuses to
listen if it is unset. Without a bearer, HTTP 401. With a bearer,
`get_law` includes an example hard rule (`MUST never invent company
policy` or `always-on`). No live Postgres.

```bash
cd mcp
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pytest tests
```

## Run with Docker / Portainer

Live pin: `ghcr.io/mattstyles333/canon-mcp:0.1.0`. Planned name: `ghcr.io/mattstyles333/openlaw-mcp`. Prefer `OPENLAW_MCP_TOKEN`; `CANON_MCP_TOKEN` is a deprecated alias.
Git tag `v0.1.0` publishes it; compose pins `:0.1.0`. Extra `:v0.1.0`
may exist.

```bash
export OPENLAW_MCP_TOKEN=          # required; do not commit a value
docker compose up -d             # Portainer stack name: openlaw-mcp
docker pull ghcr.io/mattstyles333/canon-mcp:0.1.0
```

Portainer: new stack `openlaw-mcp`, paste `docker-compose.yml`, set
`CANON_MCP_TOKEN` in the UI. Do not paste the token into git.

See [mcp/README.md](../mcp/README.md). Cloud agents need public HTTPS,
not tailnet-only, not stdio, not localhost.
