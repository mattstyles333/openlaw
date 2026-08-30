# Harness attach

Canon is not a runtime. It attaches to the harness you already
use. Law loads as markdown the harness already reads; optional MCP is
the same HTTP projection for agents that cannot see the working tree.

Git is the source of truth. MCP is a projection. Herdr is a
multiplexer, not a brain.

Worked recipes live in [`examples/`](../examples/). This page is the
matrix.

## Matrix

| Harness | How `AGENTS.md` / law loads | Optional MCP |
| --- | --- | --- |
| **Grok Build** | Auto-loads `AGENTS.md` from the repo root. `CLAUDE.md` / `GEMINI.md` are unused here but kept for other tools in the same tree. | `grok mcp add --transport http <public-https-url>` with bearer. See [examples/grok-build.md](../examples/grok-build.md). |
| **Cursor Grok Bot** | Clone the law repo into `/workspace` (or make it the workspace). Bot reads `AGENTS.md` and `.cursor/rules/law.mdc`. | Account-wide HTTP MCP. **Public HTTPS**, not tailnet-only, not stdio, not localhost. See [examples/grok-bot.md](../examples/grok-bot.md). |
| **Herdr** | Each pane's `cwd` is the law repo (or the product repo that *is* the law fork). `grok --resume` continues the pane. Herdr does not interpret policy. | Same HTTP MCP as any other Grok client, if the pane cannot see git. See [examples/herdr.md](../examples/herdr.md). |
| **OpenCode** | Loads `AGENTS.md`. | Remote MCP, `oauth: false`, bearer token. See [examples/opencode.md](../examples/opencode.md). |
| **Claude Code** | Loads `CLAUDE.md`, which points at `AGENTS.md` and `law/`. | Same HTTP MCP + bearer. |
| **Gemini CLI** | Loads `GEMINI.md`, which points at `AGENTS.md` and `law/`. | Same HTTP MCP + bearer. |
| **Hermes** | Keep `SOUL.md` short. Paste the excerpt from `scripts/excerpt-soul.sh` (~15 lines of hard rules). Do not use `MEMORY.md` as the policy store. Leave `memory.provider` unset unless you *also* want recall — and even then, recall is not law. | Same HTTP MCP + bearer. See [examples/hermes.md](../examples/hermes.md). |

## Rules that apply to every harness

1. **Prefer the working tree.** If the agent can `read` `AGENTS.md`
   and `law/`, you do not need MCP.
2. **MCP is HTTP + bearer, fail closed.** No unauthenticated default.
   Cloud agents need a public HTTPS URL.
3. **Do not attach a generic Postgres MCP** and call it law. No
   `execute_sql`.
4. **Do not point memory products at `law/`.** Indexing constraints
   into a vector store so they can be "retrieved when relevant" undoes
   the product.
5. **CI stays on.** A harness attach that works locally and then lets
   an agent merge unsigned `law/` changes is not attached.

## What "loads" means

Always-on means the harness puts `AGENTS.md` (and, via that file,
`law/`) into the session up front — not as a tool the model may
forget to call. If a harness only offers "search workspace", treat
that as a defect and compensate: make `AGENTS.md` smaller, pin it in
the harness's always-include list, and keep the three hard rules
inlined so a truncated window still has them.
