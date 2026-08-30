# Cursor Grok Bot

Cursor Grok Bot is a cloud agent. It does not share your laptop's
filesystem or your tailnet. Law must be in the workspace it is cloned
into, and any MCP it calls must be **public HTTPS**.

## Law from git

1. Fork Canon (or use a product repo that *is* your law fork).
2. Clone that repo into the Bot's `/workspace` (the workspace root
   Cursor gives the agent).
3. Confirm `AGENTS.md`, `law/`, and `.cursor/rules/law.mdc` are at
   the paths this template uses. The Bot loads them as workspace
   rules; `.cursor/rules/law.mdc` is `alwaysApply: true`.

Do not paste policy into a Bot "memory" or a Cursor index and then
delete `law/`. Retrieval is not law.

## Optional MCP (account-wide HTTP)

If the Bot must read law from a canonical repo it did not clone:

- Run the Canon MCP behind **public HTTPS** (a reverse proxy with
  a real certificate).
- Add it as **account-wide HTTP MCP** in Cursor. Not stdio. Not
  localhost. Not tailnet-only. The Bot will not reach `127.0.0.1` on
  your machine and will not join your tailnet.
- Bearer token required. Fail closed. The token is an env var on the
  server (`CANON_MCP_TOKEN`), never a file in git.

Cloud agents that cannot present a bearer should not get a
fail-open fallback. They should get 401.

## Checks

- Bot can quote a hard rule from `AGENTS.md` without calling a search
  tool.
- A request to invent a Northwind policy is refused.
- MCP, if attached, returns 401 without `Authorization: Bearer`.
