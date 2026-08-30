# Canon MCP (optional)

Thin HTTP projection of this git repo. **Git is the source of truth. MCP is
not.** Do not treat this server as law. Agents that can see `AGENTS.md` and
`law/` should read the files; attach MCP only when a cloud agent cannot see
the working tree.

This is not Mem0, not a vector index, and not a generic database server.
`get_law` returns the current files concatenated. It does not search.

## How to run

From the repository root (the directory that contains `AGENTS.md` and `law/`):

```bash
export CANON_MCP_TOKEN=          # set a real token in your shell; do not commit it
# optional, for owner tools:
export CANON_COMMIT_TOKEN=

cd mcp
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
python server.py --host 0.0.0.0 --port 8787
```

### Run with Docker / Portainer

Production image pin (semver, no `v` prefix):
`ghcr.io/mattstyles333/canon-mcp:0.1.0`.

Git tag `v0.1.0` publishes that image. Extra tag `:v0.1.0` may exist;
**compose pins `:0.1.0`**.

```bash
export CANON_MCP_TOKEN=          # required; do not commit a value
docker compose up -d             # repo-root Portainer stack; port 8787
```

Portainer: new stack `canon-mcp`, paste `docker-compose.yml`, set
`CANON_MCP_TOKEN` in the stack env UI. Never paste the token into the
committed file.

```bash
docker pull ghcr.io/mattstyles333/canon-mcp:0.1.0
```

Developers who want a bind-mount can use `compose.dev.yml` (not for
production).

The process **refuses to listen** if `CANON_MCP_TOKEN` is unset. That is fail
closed.

The server finds the repo by walking up from the working directory until it
sees `AGENTS.md` and `law/`.

## Auth

Every request needs:

```
Authorization: Bearer <CANON_MCP_TOKEN>
```

Missing or wrong credentials → **HTTP 401**. There is no anonymous read,
no stdio fallback, and no "open on localhost" mode for cloud agents.

### Owner token

`commit_decision` and `set_priorities` also require `CANON_COMMIT_TOKEN`.
Send it as `X-Canon-Commit-Token: <CANON_COMMIT_TOKEN>`, or use a bearer that
matches `CANON_COMMIT_TOKEN` (only if you chose to set the two env vars equal —
prefer two different values).

If `CANON_COMMIT_TOKEN` is unset, owner tools fail closed.

Tokens are environment variables. They never belong in `law/`, in this
README as real values, or as Compose default secrets.

## Tools

| Tool | Who | What |
| --- | --- | --- |
| `get_law` | any bearer | `law/constraints.md` + `brand.md` + `sor.md`, concatenated. **Not search.** |
| `get_priorities` | any bearer | `law/priorities.md` |
| `search_decisions` | any bearer | keyword over `decisions/*.md` |
| `get_decision` | any bearer | one ADR by filename |
| `propose_decision` | any bearer | insert `decisions/YYYY-MM-DD-slug.md` with `status: proposed` |
| `commit_decision` | owner | set that ADR `status: decided` |
| `set_priorities` | owner | rewrite `law/priorities.md` |

Writes land as files. CODEOWNERS and CI still gate what becomes law.
A proposed ADR is not policy until an owner merges it.

HTTP:

- `GET`/`POST` `/tools/get_law` (and the other tool names) — convenience
- `POST` `/mcp` — JSON-RPC 2.0 (`initialize`, `tools/list`, `tools/call`)

Example:

```bash
curl -sS -H "Authorization: Bearer $CANON_MCP_TOKEN" http://127.0.0.1:8787/tools/get_law
```

## Public HTTPS for cloud agents

Cursor Grok Bot, Grok Build remote sessions, and other cloud agents do not
share your laptop or your tailnet. Serve this projection behind **public
HTTPS** (reverse proxy + real certificate). Then:

```bash
grok mcp add --transport http https://law.example.invalid
```

Not tailnet-only. Not stdio. Not `localhost` for an agent that is not on
this machine. Configure the client with the same bearer; do not paste the
token into a committed config file.

## Persistence (v0.1)

Default: the filesystem of `law/` and `decisions/` in this clone.

`CANON_POSTGRES_URL` is reserved, documented here, and **off by default**.
v0.1 does not implement Postgres. The Portainer stack does not ship a
postgres service. Do not attach a generic Postgres MCP to Canon.

## Smoke tests

```bash
cd mcp
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pytest tests
```

Does not need Postgres. Checks: bearer `get_law` includes an example hard
rule; without bearer the server returns HTTP 401.
