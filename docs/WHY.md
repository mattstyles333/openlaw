# Why Canon exists

Always-on law for AI agents, stored as git markdown, never retrieved.

This is **law**, not memory SaaS. The rest of this page is the argument.

## Law vs recall

| | Law | Recall |
| --- | --- | --- |
| Question | What is the agent *allowed* to do? | What did we *say* last Tuesday? |
| Load | Always. Every session. | When similar, when asked, when indexed |
| Change process | Reviewable diff, CODEOWNERS, ADR | Re-embed, re-extract, hope |
| Failure mode | Agent did not read the file (CI catches drift) | Agent retrieved the wrong neighbour |
| System of record | git | a vendor database, a graph, a vector index |

Recall is useful. It is not law. Mixing them is how a specialist agent
"remembers" a discount you never ran, or a health claim you never made,
or a policy you retracted six weeks ago that still ranks well.

**Always-injected vs retrieved-when-similar** is the whole product. If
the constraint only appears when the embedding is close enough, it is a
search result. Search results are not binding.

## Why git

- **Diffs are reviewable.** A one-line change to `law/constraints.md` is
  a pull request. An embedding update is a blob.
- **History is the audit log.** `git log law/` is the policy timeline.
  There is no second store to reconcile.
- **CODEOWNERS is the permission model.** Who may merge law is a file,
  not a dashboard role that an agent can talk past.
- **Every harness already loads it.** `AGENTS.md`, `CLAUDE.md`,
  `GEMINI.md`, Cursor rules, Hermes `SOUL.md`. You do not need a new
  runtime to have law.

Git is the source of truth. MCP, if you attach it, is a projection.
Herdr is a multiplexer, not a brain.

## Why not Mem0 / Hindsight / Graphiti / Letta / ByteRover

Those products (and Hindsight-as-brain, and any "agent memory layer")
are built to **extract, store, and retrieve**. That is the right shape
for:

- "What did the customer say about the decaf blend last month?"
- "Which ticket discussed the leaking espresso group?"
- "Summarise the last five roast notes for Ethiopia."

It is the wrong shape for:

- "Never invent company policy."
- "Never put card data in git."
- "Roast dates on bags match the roast log."

A vector store cannot be CODEOWNERS. A graph edge cannot be an ADR.
"We retrieved a similar constraint" is not "the constraint loaded."

Use those tools *next to* Canon if you want recall. Do not replace
`law/` with them. Do not treat Hindsight as the brain. Do not leave
Hermes `MEMORY.md` as the store of policy. Leave `memory.provider`
unset if the only thing you needed was law.

gitagent and other "agent OS" projects are a different miss: they want
to *be* the runtime. Canon is the files your existing harness
already reads, plus CI that fails when those files are betrayed.

## Why CI is the security layer

Agents will rewrite policy if you let them. They will "helpfully"
shorten `AGENTS.md`, drop a hard rule, invent a brand claim, or patch
`constraints.md` in the same commit as a bugfix.

CI is how you don't let them:

- `AGENTS.md` stays short (80 lines / 12 KB) so it can be always-on.
- Hard-rule needles must be present (adopters replace the example
  needles with their own).
- ADRs have frontmatter and a status.
- Secret patterns are rejected in `law/` and `AGENTS.md`.
- `CODEOWNERS` covers `law/` and `AGENTS.md`.
- MCP, when present, fails closed and has no `execute_sql`.

The model is not the security boundary. The merge gate is.

## Why optional MCP at all

Cloud agents (Cursor Grok Bot, hosted Hermes, a Grok Build session that
cannot see your laptop) sometimes cannot read the working tree. An HTTP
MCP that returns the *current files* — not a search, not a summary —
lets them load the same law. Bearer required; fail closed; public
HTTPS for cloud; git still canonical.

If the agent can see the repo, skip MCP. Clone the law. That is the
happy path.
