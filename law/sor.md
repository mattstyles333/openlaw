# Northwind Coffee — systems of record

Fictional independent coffee roaster and cafe. Replace this file on fork.

A system of record (SoR) is the thing you treat as true when two
sources disagree. Chat is never SoR. MCP is never SoR. Memory and
recall tools are **not** SoR for policy.

## Who may merge law

- Law files (`law/**`, `AGENTS.md`) merge only to `main` with review
  from the owners listed in `CODEOWNERS`.
- Who may merge law: those owners.
- Who proposes: any specialist agent (or human) via `decisions/`, with
  `status: proposed`. Owners mark `decided` and then update `law/`.

## Systems of record

| Domain | SoR | Not SoR |
| --- | --- | --- |
| Law / policy | this git repo (`law/`, `AGENTS.md`, decided ADRs) | chat, MCP, memory products |
| Roast dates and roast batches | roast-log spreadsheet | chat, MCP, bag photos guessed by a model |
| Payments, tenders, refunds | Square (example POS) | this git repo, agent logs |
| Customer contact and tickets | the cafe's own inbox / POS customer directory | git, `law/`, MCP |
| Priorities for this week | `law/priorities.md` (rewritten, not appended) | a running chat thread |

## Notes

- The roast log is a spreadsheet. Agents may *read a copy they are
  given*; they must not *become* the log, and they must not invent
  rows.
- Square is named as an example POS so adopters have a slot to replace.
  It is not an integration in this template.
- Memory/recall tools (Mem0, Hindsight, Graphiti, Letta, ByteRover, a
  local `MEMORY.md`) are not SoR for policy. Retrieval is not law.
