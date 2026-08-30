# Security Policy

## How to report

Report vulnerabilities via GitHub **private vulnerability reporting** on
this repository (Security → Report a vulnerability). Please do not open
a public issue for a live exploit or a leaked credential.

We aim to acknowledge reports within a few days. This is a small MIT
project; there is no bug bounty.

## What is in scope

- CI gates that can be bypassed so an agent can rewrite `law/` without
  review.
- MCP authentication that fails *open* (missing bearer accepted).
- Secret leakage through law files, examples, logs, or CI artifacts.
- `execute_sql` or other unconstrained execution surfaces added under
  `mcp/`.

## What is not in scope

- "An agent ignored AGENTS.md." That is why CI exists. Teach the
  harness; do not treat a model refusal-to-follow-instructions as a
  AlwaysLaw CVE.
- Secrets you committed to **your fork's** `law/`. Rotate them; this
  template cannot unsay them.

## Never put secrets in law/

**NEVER** put secrets, tokens, customer PII, or live credentials in
`law/`, `AGENTS.md`, `decisions/`, or examples.

- MCP tokens are environment variables (`LAW_MCP_TOKEN`,
  `LAW_COMMIT_TOKEN`). They are never files in git.
- Customer emails, card data, and roast-log row dumps do not belong in
  this repo. Systems of record stay in the systems named in
  `law/sor.md`.
- Docs may *name* token variables (`bearer`, `LAW_MCP_TOKEN`) so that
  operators know what to set. Names are not values.

`scripts/check-law.sh` rejects common credential patterns in `law/` and
`AGENTS.md`. Gitleaks runs on every push and pull request. These are
backstops, not permission to get sloppy.

## MCP

When `mcp/` is present:

- Bearer auth is required. The server **fails closed** if the token is
  missing at startup or on the request.
- Cloud agents need public HTTPS. Tailnet-only, stdio, and localhost
  are not sufficient for agents that do not share your network.
- Owner tools require a separate commit token.
- There is no `execute_sql`. Generic Postgres MCP is out of scope.
