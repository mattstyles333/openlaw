# Canon

**Always-on law for AI agents, stored as git markdown, never retrieved.**

This is **law**, not memory SaaS. Fork the repo, replace `law/` with your
organisation's constraints, and keep `AGENTS.md` short with the
non-negotiables inlined. CI is the agent security layer. Optional MCP is a
projection of git, not the source of truth. Herdr is a multiplexer, not a
brain.

[Why not Mem0 / Hindsight / Graphiti / Letta / ByteRover](docs/WHY.md) ·
[Security model](docs/SECURITY-MODEL.md) ·
[Harness attach](docs/HARNESS.md) ·
[Changelog](CHANGELOG.md) ·
[MIT License](LICENSE)

---

## What this is

Canon is three things, in this order:

1. **Law files** every existing harness already loads — `AGENTS.md`,
   `CLAUDE.md`, `GEMINI.md`, Cursor rules, a Hermes `SOUL.md` excerpt.
2. **CI that enforces them** — size limits, hard-rule needles, ADR
   frontmatter, secret patterns, CODEOWNERS coverage. Agents will rewrite
   policy if you let them; CI is how you don't let them.
3. **Optional thin HTTP MCP** — a read/propose projection of the same git
   files for cloud agents that cannot see the working tree. Git remains
   canonical.

It is **not** an agent runtime. It is **not** a memory product. It does
not extract, embed, or recall. Law that is retrieved-when-similar is not
law; it is a search result.

The example company in this template is **Northwind Coffee**, a fictional
independent roaster and cafe. Nothing here is a real business, a real
customer, or a real secret.

## What this is not

| Product | What it does | Why Canon is different |
| --- | --- | --- |
| Mem0, Hindsight, Graphiti, Letta, ByteRover | Recall / extraction / graph memory | Retrieval is not law |
| gitagent | A whole agent OS | Canon is files + CI + optional MCP |
| Generic Postgres MCP | `execute_sql` against a database | Forbidden here. Law is markdown in git |

See [docs/WHY.md](docs/WHY.md).

## Quickstart

```bash
git clone https://github.com/mattstyles333/canon.git
cd canon
# 1. Fork (or clone your fork).
# 2. Replace law/ with your organisation's constraints, brand, SoR, priorities.
# 3. Keep AGENTS.md short. Inline your non-negotiables (the 3 hard-rule pattern).
# 4. Turn on GitHub Actions (or GitLab CI). CI is the agent security layer.
bash scripts/check-law.sh
```

Adopters replace the example grep needles in `scripts/check-law.sh` with
their own hard-rule strings. The Northwind needles are a template, not
universal policy.

### The 3 hard-rule pattern

`AGENTS.md` stays under 80 lines and 12 KB. It **inlines** the rules that
must never depend on retrieval, then points at `law/` for the rest:

- MUST never invent company policy
- always-on law is git markdown, never a vector store
- MUST propose decisions; do not edit law/constraints.md without review

Specialists propose ADRs in `decisions/` (`status: proposed`). They do
not silently edit `law/constraints.md`. Owners listed in `CODEOWNERS`
review and merge.

## Harness attach

Every mainstream coding harness already loads markdown from the repo.
You do not need a new runtime.

| Harness | How law loads | Optional MCP |
| --- | --- | --- |
| Grok Build | `AGENTS.md` auto-load | `grok mcp add --transport http` |
| Cursor Grok Bot | clone into `/workspace` | account-wide HTTP MCP (public HTTPS) |
| Herdr | pane `cwd` = repo; `grok --resume` | multiplexer, not a brain |
| OpenCode | `AGENTS.md` | remote MCP, oauth false + bearer |
| Claude Code | `CLAUDE.md` → `AGENTS.md` | same HTTP MCP; [examples/claude.md](examples/claude.md) |
| Gemini CLI | `GEMINI.md` → `AGENTS.md` | same HTTP MCP; [examples/gemini.md](examples/gemini.md) |
| Hermes | short `SOUL.md` excerpt | same MCP; leave `memory.provider` unset |

Details: [docs/HARNESS.md](docs/HARNESS.md) and [examples/](examples/).

```bash
# Hermes SOUL.md excerpt (stdout only)
bash scripts/excerpt-soul.sh
```

## Optional MCP

MCP is **optional** and **not the source of truth**. `mcp/` is a thin HTTP
projection of `law/` and `decisions/` with bearer auth that **fails closed**
(no unauthenticated default). Cloud agents need public HTTPS — not
tailnet-only, not stdio, not localhost.

`CANON_MCP_TOKEN` is required. The process refuses to listen if it is unset.
Owner tools (`commit_decision`, `set_priorities`) also need
`CANON_COMMIT_TOKEN`. There is no `execute_sql`. Postgres is reserved and
unimplemented; it is not in the default compose stack.

### Run with Docker / Portainer

Production pin (semver, no `v` prefix):
`ghcr.io/mattstyles333/canon-mcp:0.1.0`.

Git tag `v0.1.0` publishes that image to GHCR. An extra `:v0.1.0` tag may
also exist; **compose and Portainer pin `:0.1.0`**.

```bash
export CANON_MCP_TOKEN=          # required; no default secret; do not commit
docker compose up -d             # Portainer stack file; listens on 8787
```

Portainer: new stack named `canon-mcp`, paste `docker-compose.yml`, set
`CANON_MCP_TOKEN` in the stack environment UI. Do not paste the token
into the committed compose file.

```bash
docker pull ghcr.io/mattstyles333/canon-mcp:0.1.0
```

Local pip-install remains for developers (`cd mcp && pip install -e ".[dev]"`).
Bind-mount development uses `compose.dev.yml`, not the Portainer stack.

Details: [mcp/README.md](mcp/README.md). [v0.1 status](docs/STATUS.md).

## Layout

```
AGENTS.md                 short always-on law (max 80 lines)
CLAUDE.md / GEMINI.md     one-line pointers
.cursor/rules/law.mdc     pointer only
law/                      constraints, brand, SoR, priorities
decisions/                ADRs (propose; owners merge)
mcp/                      optional HTTP projection of git
Dockerfile                production image for the MCP projection
CHANGELOG.md              0.1.0 first public release
docs/                     why, security model, harness matrix
examples/                 attach recipes per harness
scripts/check-law.sh      local CI
scripts/excerpt-soul.sh   Hermes SOUL.md hard-rule block
docker-compose.yml        Portainer stack: GHCR pin :0.1.0, port 8787
```

## Local CI

```bash
bash scripts/check-law.sh
```

GitHub Actions and GitLab CI run the same gates on push and pull
request: law-check, secret-scan, agent-security, and mcp-test.
See [docs/STATUS.md](docs/STATUS.md).

## License

[MIT](LICENSE) © 2026 Canon contributors.
