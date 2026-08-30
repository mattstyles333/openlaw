# Gemini CLI

Gemini CLI loads `GEMINI.md` from the repository root. In this template
that file is a one-line pointer: read `AGENTS.md`; law lives in `law/`;
retrieval is not law.

## Law from git

```bash
cd /path/to/your-canon-fork
# Open this directory as the Gemini CLI workspace.
# GEMINI.md → AGENTS.md → law/.
bash scripts/check-law.sh
```

Do not store Northwind constraints in Gemini "memory" or a vector
index. Retrieval is not law.

## Optional MCP

Same HTTP + bearer as every other harness. Public HTTPS for cloud
sessions; `CANON_MCP_TOKEN` on the server; missing bearer is 401. Do
not use stdio or localhost for an agent that is not on this machine.

## Checks

- A fresh Gemini CLI session can state the three hard rules without a
  search tool.
- A request to invent a Northwind policy is refused.
- MCP, if attached, returns 401 without `Authorization: Bearer`.
