# Canon v0.1 status

Always-on law for AI agents, stored as git markdown, never retrieved.
This is law, not memory SaaS. The example company in the template is
**Northwind Coffee** (fictional). Replace `law/` on fork.

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
export CANON_MCP_TOKEN=          # required; do not commit a value
docker compose up mcp          # port 8787

cd mcp
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pytest tests
```

See [mcp/README.md](../mcp/README.md). Cloud agents need public HTTPS,
not tailnet-only, not stdio, not localhost.
