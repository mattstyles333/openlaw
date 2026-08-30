# Security model

Openlaw's security model is boring on purpose. Chief/owner writes
law via git. Specialists propose decisions. CI is the agent security
layer. Secrets never enter the repo. MCP, when present, fails closed.

## Roles

| Role | What they may do | What they may not do |
| --- | --- | --- |
| Owner / chief (CODEOWNERS) | Merge `law/`, `AGENTS.md`, decided ADRs | Put secrets in git |
| Specialist (human or agent) | Propose `decisions/*.md` with `status: proposed`; read law | Edit `law/constraints.md` without review; invent policy |
| CI | Reject oversized `AGENTS.md`, missing needles, secret patterns, unauthenticated MCP, `execute_sql` | Decide policy |
| MCP | Project current git files over HTTP; insert proposed ADRs | Be the source of truth; run SQL; skip bearer |

The owner writes law in git. That is the only write path that becomes
binding. Everything else is a proposal or a projection.

## Harness rank

Authority is a **ranked list**, not a dashboard role. See
[`law/permissions.md`](../law/permissions.md). Higher rank = more
authority. Top ranks may merge; merge is still **CODEOWNERS / human**.
Lower ranks read + propose only via PR. Agents never auto-merge `law/`
or `AGENTS.md`. OpenClaw is a stub.

## CI is the agent security layer

Language-model instructions are not a control. Agents will rewrite
policy if you let them — to be helpful, to unstick a task, to "clean
up" a long `AGENTS.md`.

The controls are:

1. **Size cap** on `AGENTS.md` (80 lines, 12 KB). Always-on files that
   grow past the harness window stop being always-on.
2. **Hard-rule needles** grepped by `scripts/check-law.sh`. Adopters
   replace the example needles with their own non-negotiables.
3. **ADR frontmatter** on `decisions/20*.md`.
4. **Secret patterns** rejected in `law/` and `AGENTS.md`. Docs such as
   this file and `SECURITY.md` may *name* token variables.
5. **CODEOWNERS** must cover `law/` and `AGENTS.md`.
6. **Permissions ranked list**: `law/permissions.md` must exist, list
   harnesses in rank order, and state the CODEOWNERS parent merge rule.
7. **MCP fail-closed**: if `mcp/server.py` exists, it must require
   bearer / 401 / `CANON_COMMIT_TOKEN` language and must not contain
   `execute_sql` or default to unauthenticated.
8. **Gitleaks** (or equivalent) on every push and pull request.

GitHub Actions and GitLab CI run the same gates. Fork, turn them on,
do not delete them to "unblock" an agent.

## No secrets in the repo

Tokens, keys, customer emails, card data, and live credentials do not
belong in `law/`. MCP tokens are environment variables:

- `CANON_MCP_TOKEN` — required at MCP startup; refuse to listen if unset.
- `CANON_COMMIT_TOKEN` — owner tools (`commit_decision`, `set_priorities`).

Public docs may mention those *names*. Values never ship in git, in
docker-compose defaults, or in example commands with a real secret.

## MCP bearer, fail closed

When `mcp/` is present:

- Every request requires `Authorization: Bearer <token>`. Missing or
  wrong credentials return **401**. There is no unauthenticated default.
- The process refuses to listen if `CANON_MCP_TOKEN` is unset.
- Owner tools require `CANON_COMMIT_TOKEN` in addition.
- Cloud agents need **public HTTPS**. Tailnet-only, stdio, and
  localhost are not sufficient for an agent that does not share your
  network. Cursor Grok Bot in particular is account-wide HTTP MCP on
  a public URL, not a tunnel you forgot to bring up.
- Git is canonical. MCP writes land as files (`decisions/` proposed
  ADRs, `law/priorities.md` rewrites) that still go through git and
  CODEOWNERS before they are law.

## What this model does not claim

- It does not sandbox the model. A local agent with write access to
  the working tree can still edit files; CI and CODEOWNERS catch it
  **before merge**, not before the keystroke.
- It does not replace your POS, identity provider, or roast log. Those
  stay the systems of record named in `law/sor.md`.
- It does not make retrieval safe-as-law. If you attach Mem0, it is
  still recall. Do not point `get_law` at it.
