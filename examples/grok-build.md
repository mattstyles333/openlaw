# Grok Build

Grok Build auto-loads `AGENTS.md` from the repository root. That is
the attach. You do not need a plugin to have law.

## Law from git

```bash
git clone https://github.com/YOU/your-canon-fork.git
cd your-canon-fork
# Open this directory as the Grok Build workspace.
# AGENTS.md is always-on. law/ is pointed at from AGENTS.md.
bash scripts/check-law.sh
```

Keep `AGENTS.md` under 80 lines so the auto-load stays inside the
always-injected budget. Detail goes in `law/`.

## Optional MCP

When the session cannot see a particular canonical clone (or you want
the same law on a bot that is not this workspace):

```bash
# Public HTTPS URL of the Canon MCP. Bearer required on the server.
grok mcp add --transport http https://law.example.invalid
```

Replace the URL with yours. Do not use stdio for cloud-adjacent
sessions. Do not default the server to unauthenticated.

`grok mcp add --transport http` attaches a projection. It does not
replace `AGENTS.md`. If both are present, they must say the same
thing because they are the same files.

## Checks

- The agent, on a fresh session, can state the three hard rules
  without a tool call.
- `bash scripts/check-law.sh` exits 0.
- After `grok mcp add`, `get_law` (when MCP is present) includes
  `MUST never invent company policy`.
