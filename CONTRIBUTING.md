# Contributing to Canon

This repository is **law**, not a memory product and not an agent
runtime. Contributions should make the law files, the CI that enforces
them, or the docs that attach them to existing harnesses better.

## Fork, then replace example law

The `law/` tree is a **Northwind Coffee** template. It is fictional on
purpose. If you are adopting Canon for a real organisation:

1. Fork the repo.
2. Replace `law/constraints.md`, `law/brand.md`, `law/sor.md`, and
   `law/priorities.md` with yours.
3. Keep `AGENTS.md` short (max 80 lines, max 12 KB). Inline only the
   non-negotiables; point at `law/` for the rest.
4. Replace the example grep needles in `scripts/check-law.sh` with the
   same strings you inlined in `AGENTS.md`.
5. Turn on GitHub Actions or GitLab CI. CI is the agent security layer.

Do not send PRs that turn Northwind into a different fictional company
unless you are improving the template's teaching value.

## Propose decisions; do not silently edit constraints

Agents and contributors **MUST propose decisions**. Do not edit
`law/constraints.md` without review.

- New policy, or a change to existing policy: add
  `decisions/YYYY-MM-DD-slug.md` with `status: proposed`, using
  [decisions/TEMPLATE.md](decisions/TEMPLATE.md).
- Owners listed in `CODEOWNERS` review, set `status: decided`, and
  (only then) update `law/`.
- Rewrite `law/priorities.md` for the current week. Do not append
  forever.

## Keep AGENTS.md short

`AGENTS.md` is always-injected. If it grows past 80 lines or 12 KB, CI
fails. Put detail in `law/` and `docs/`. Pointers (`CLAUDE.md`,
`GEMINI.md`, `.cursor/rules/law.mdc`) stay one-liners.

## CI must pass

```bash
bash scripts/check-law.sh
```

PRs are also gated by secret-scan, agent-security, and (when `mcp/`
exists) MCP smoke tests. Do not weaken CODEOWNERS coverage of `law/`
or `AGENTS.md`. Do not add `execute_sql` under `mcp/`. Do not default
MCP to unauthenticated.

## Secrets

Never put secrets, live tokens, customer PII, or credentials in `law/`,
`AGENTS.md`, examples, or docs. MCP tokens are environment variables.
See [SECURITY.md](SECURITY.md).

## What belongs in a PR

- Template / docs / CI / examples: open a PR against this repo.
- Your organisation's actual law: keep it in **your fork**. Do not
  upstream real policy, real brand claims, or real systems of record.
