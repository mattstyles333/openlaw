# Canon — always-on law for agents

This repository is **law**, not memory. Retrieval is not law. Agents MUST
load this file and `law/` on every session. Similarity search is not a
substitute for always-injected constraints.

Full constraints, brand, systems of record, and this week's priorities live
in `law/`. Architecture Decision Records live in `decisions/`.

Optional MCP is a **projection of git**, not the source of truth.

## Hard rules (example — replace on fork)

1. MUST never invent company policy
2. always-on law is git markdown, never a vector store
3. MUST propose decisions; do not edit law/constraints.md without review

## Also non-negotiable

- Do not invent policy. If it is not in `law/`, it is not policy.
- Retrieval is not law. Do not treat memory, RAG, or embeddings as constraints.
- Propose decisions; do not edit law/constraints.md without review.
- Secrets never belong in law/. Tokens, keys, PII, and credentials stay in env.
- MCP is a projection of git, not the source of truth.

## How to use this repo

1. Fork. Replace `law/` with your organisation's files.
2. Keep this file short. Inline only the non-negotiables.
3. Turn on CI. CI is the agent security layer: agents will rewrite policy
   if you let them.
4. Specialists propose ADRs in `decisions/` (`status: proposed`).
   Owners listed in `CODEOWNERS` merge decided law.

Example company in this template: **Northwind Coffee** (fictional). Replace it.

See `docs/WHY.md`, `docs/SECURITY-MODEL.md`, `docs/HARNESS.md`, and `examples/`.
