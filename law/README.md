# `law/` — always-on company law

This directory is the organisation's **law**. Agents MUST load it. Retrieval
(RAG, embeddings, memory SaaS, "search the wiki") is not a substitute.

The files in this template describe **Northwind Coffee**, a fictional
independent roaster and cafe. Fork the repo and replace every file here
with yours. Do not send real policy, real customers, or real secrets
upstream.

| File | What it is |
| --- | --- |
| [constraints.md](constraints.md) | Non-negotiable operating constraints |
| [brand.md](brand.md) | Claims we do and do not make |
| [sor.md](sor.md) | Who may merge law, who proposes, which systems are SoR |
| [priorities.md](priorities.md) | This week's list — rewrite, do not append forever |

`AGENTS.md` at the repo root inlines only the hard rules that must never
depend on retrieval, then points here. Keep `AGENTS.md` short.

Changes to constraints go through `decisions/` (`status: proposed`) and
are merged by the owners in `CODEOWNERS`. Agents MUST propose decisions;
they MUST NOT edit `constraints.md` without review.

Secrets never belong in these files. See [../SECURITY.md](../SECURITY.md).
