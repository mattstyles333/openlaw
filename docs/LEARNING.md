# Learning loop: propose → review → merge

Openlaw learns in git. It does not learn by rewriting `law/` from a
chat, a memory product, or an auto-merge. Retrieval is not law. The
loop is **propose → review → merge**.

Any harness may **propose**. Only owners listed in `CODEOWNERS` **merge**
to `law/` or `AGENTS.md`. Never auto-merge law.

## Propose

A specialist (human or agent, any attached harness) writes an ADR or a
skill proposal. They do **not** edit `law/` or `AGENTS.md` in the same
change.

Two valid locations:

1. `decisions/proposed/YYYY-MM-DD-slug.md` (preferred for new drafts)
2. `decisions/YYYY-MM-DD-slug.md` with `status: proposed`

Use the skeleton:

```bash
bash scripts/propose.sh short-slug
```

`scripts/propose.sh` copies `decisions/_template.md`, writes a new file
under `decisions/proposed/`, and prints next steps. It is offline. It
does not need a network, a token, or MCP. It does not write `law/`.

Fill **Context**, **Decision**, and **Consequences**. Frontmatter must
include `date:`, `owner:`, and `status: proposed`.

Then open a pull request. Mark it as a **proposal vs law change**. Do
not tick "law change" unless an owner has already marked the matching
ADR `decided` and asked for the `law/` patch.

## Review

Owners listed in `CODEOWNERS` read the proposal. They may request
edits, reject it, or accept it.

Review is a git review, not a dashboard vote and not a model
self-approving its own diff. CI (`scripts/check-law.sh`) still has to
pass. CI does not decide policy.

A proposed ADR is not binding. Agents must not treat `status: proposed`
as law.

## Merge

On accept, owners:

1. Set the ADR `status: decided` (or `superseded` if a later ADR
   replaces it).
2. Apply the corresponding change to `law/` and, only if needed, to
   `AGENTS.md`.
3. Merge through the required-review path. `law/**` and `AGENTS.md`
   require CODEOWNERS.

Never auto-merge law. There is no bot, queue, or MCP tool that lands a
binding `law/` or `AGENTS.md` change without a human owner. Keys to the
castle stay with CODEOWNERS.

A decided ADR is the record of *why*. It is not law until `law/` (or
the always-on `AGENTS.md` needles) says so.

## Who may do what

| Actor | May | Must not |
| --- | --- | --- |
| Any harness (Herdr / Grok Build, Cursor Grok Bot, Hermes, OpenCode, Claude Code, Gemini CLI, …) | Propose an ADR or skill under `decisions/proposed/` or `decisions/` with `status: proposed`; open a PR marked proposal vs law change | Edit `law/` or `AGENTS.md`; auto-merge; invent policy |
| CODEOWNERS / parent | Review; mark the ADR `decided`; merge the law patch | Auto-merge law; skip the ADR |
| CI | Reject missing needles, secrets, oversized `AGENTS.md` | Decide policy |

## What this is not

- Not a plugin SDK. A "skill" proposal is still a markdown file in git.
- Not a SQLite brain. There is no local store that becomes policy.
- Not auto-write of law. `propose.sh` copies a template; it does not
  patch `law/constraints.md`.
- Not memory. A remembered conversation is not a decided constraint.
