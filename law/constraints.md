# Northwind Coffee — constraints

Fictional independent coffee roaster and cafe. Replace this file on fork.

These constraints are **always-on**. Agents MUST load this file on every
session. Retrieval is not a substitute. Similarity search, memory tools,
and chat history are not law.

## Hard rules

- MUST never invent company policy. If it is not written in `law/`, it
  is not policy. Ask, or propose a decision.
- MUST propose decisions; do not edit law/constraints.md without review.
- Secrets never belong in law files. No tokens, no live credentials, no
  customer PII, no card data.
- Public claims must match `law/brand.md`. Do not invent awards, health
  claims, or origin stories.
- Payments and PII: never log card data; never store customer emails in
  git. The POS is the system of record for tenders; this repo is not.

## Operations

- Roast dates printed on bags MUST match the roast log. The system of
  record for roast dates is the roast-log spreadsheet, not chat, not
  MCP, not an agent's memory.
- Do not invent SKUs, blend recipes, or allergen statements. Those live
  in the roast log and the packaged-goods spec the owners maintain.
- Cafe hours, menu availability, and wholesale accounts are owner
  questions. An agent that does not know must say so.

## How to change this file

Specialists (human or agent) open an ADR under `decisions/` with
`status: proposed`. Owners listed in `CODEOWNERS` review, mark the ADR
`decided`, and only then edit this file. That is the whole process.
