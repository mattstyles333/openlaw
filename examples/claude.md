# Claude Code

Claude Code loads `CLAUDE.md` from the repository root. In this template
that file is a one-line pointer: read `AGENTS.md`; law lives in `law/`;
retrieval is not law.

## Law from git

```bash
cd /path/to/your-openlaw-fork
# Open this directory as the Claude Code workspace.
# CLAUDE.md → AGENTS.md → law/.
bash scripts/check-law.sh
```

Do not paste Northwind constraints into a Claude project "memory" and
then delete `law/`. Retrieval is not law.

## Optional MCP

Same HTTP + bearer as every other harness. Public HTTPS for cloud
sessions; `CANON_MCP_TOKEN` on the server; missing bearer is 401. Do
not use stdio or localhost for an agent that is not on this machine.

## Checks

- A fresh Claude Code session can state the three hard rules without a
  search tool.
- A request to invent a Northwind policy is refused.
- MCP, if attached, returns 401 without `Authorization: Bearer`.
