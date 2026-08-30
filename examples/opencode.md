# OpenCode

OpenCode loads `AGENTS.md` from the repo. Point the working directory
at your AlwaysLaw fork (or a product repo that contains one).

## Law from git

```bash
cd /path/to/your-alwayslaw-fork
# OpenCode session in this directory.
# AGENTS.md is law. Retrieval is not.
```

Do not configure OpenCode's memory or knowledge-base features as the
place policy lives. If you use them, use them for recall of tickets
and notes, and keep `law/` as git markdown.

## Optional MCP

Remote MCP, OAuth off, bearer on:

- Transport: HTTP (public HTTPS for any agent that is not on localhost).
- `oauth: false` — AlwaysLaw MCP is a bearer token, not an OAuth app.
- Header: `Authorization: Bearer <LAW_MCP_TOKEN>`.
- Fail closed: missing bearer is 401, not "anonymous read".

Exact OpenCode config keys move between releases; the invariant is
**remote HTTP + bearer, oauth false**. Do not paste the token into a
committed `opencode.json`.

## Checks

- A new OpenCode session in this repo refuses to invent a Northwind
  brand claim.
- MCP, if configured, 401s without the bearer and returns full law
  with it (not a search snippet).
