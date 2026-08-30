# Learning loop: propose → review → merge

Openlaw learns in git. It does not learn by rewriting `law/` from a
chat, a memory product, or an auto-merge. Retrieval is not law. The
loop is **propose → review → merge**.

The **pull request is the discussion room**. Every harness proposes by
opening a GitHub PR. Silent file writes to `law/` (or `AGENTS.md`) in a
working tree are not a proposal. They are an unsigned edit.

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

Then open a **GitHub pull request**. Mark it as a **proposal vs law
change**. Do not tick "law change" unless an owner has already marked
the matching ADR `decided` and asked for the `law/` patch. Do not leave
the draft only on disk.

## Review

Owners listed in `CODEOWNERS` read the proposal **on the PR**. They may
request edits, reject it, or accept it.

Review is a git review, not a dashboard vote and not a model
self-approving its own diff. CI (`scripts/check-law.sh`) still has to
pass. CI does not decide policy.

Pair the rooms:

1. **GitHub Action** on `pull_request` — `.github/workflows/pr-law-review.yml`
   runs `scripts/check-law.sh` and comments a short summary plus
   suggested improvements. It does not merge.
2. **Harness webhook** (where the harness supports it) — subscribe the
   proposing session to the same `pull_request` / review events so the
   agent sees that comment. The webhook must not write `law/`.

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

## Pairing: webhook + check-law review

| Half | What it does | What it must not do |
| --- | --- | --- |
| `.github/workflows/pr-law-review.yml` | On `pull_request`, run `bash scripts/check-law.sh` and post a PR comment (or review comment) with the result and suggested improvements | Merge; approve a law change; store secrets |
| Harness webhook (optional) | Tell the proposing harness that the PR got a check-law comment | Patch `law/` or `AGENTS.md`; auto-merge |

If the comment step lacks `pull-requests: write`, the comment is
**fail soft** (the job still reports the `check-law` exit). Missing
comment permission is not a reason to skip the gate, and it is not a
reason to write law locally instead.

## Onboarding

Enable the discussion room before the first agent proposal.

1. Keep `.github/workflows/pr-law-review.yml` in the fork. Turn GitHub
   Actions on. Do not delete the workflow to "unblock" an agent.
2. Repo **Settings → Actions → General → Workflow permissions**: Read
   and write so `GITHUB_TOKEN` can comment on pull requests. Do **not**
   tick "Allow GitHub Actions to create and approve pull requests" as a
   way to land `law/`. If comment permission is missing, the comment
   step is fail soft; `check-law` still runs.
3. Optional harness webhook: where the harness can receive GitHub
   `pull_request` (or pull-request review) events, point that webhook at
   this repository. The agent should read the PR thread, not invent a
   second policy store.
4. Never auto-merge law. Never grant a harness merge rights on `law/`
   or `AGENTS.md`.

Local draft:

```bash
bash scripts/propose.sh short-slug
# then open the GitHub PR — that is the proposal
bash scripts/check-law.sh
```

## Who may do what

| Actor | May | Must not |
| --- | --- | --- |
| Any harness (Herdr / Grok Build, Cursor Grok Bot, Hermes, OpenCode, Claude Code, Gemini CLI, …) | Propose via a GitHub PR (`decisions/proposed/` or `decisions/` with `status: proposed`); optional webhook to watch that PR | Silent writes to `law/` or `AGENTS.md`; auto-merge; invent policy |
| CODEOWNERS / parent | Review on the PR; mark the ADR `decided`; merge the law patch | Auto-merge law; skip the ADR |
| CI (`pr-law-review.yml` + `check-law.sh`) | Reject missing needles; comment suggested improvements | Decide policy; merge |

## What this is not

- Not a plugin SDK. A "skill" proposal is still a markdown file in git.
- Not a SQLite brain. There is no local store that becomes policy.
- Not auto-write of law. `propose.sh` copies a template; it does not
  patch `law/constraints.md`. The review workflow comments; it does
  not merge.
- Not a silent working-tree edit. If it is not on a GitHub PR, it is
  not a proposal.
- Not memory. A remembered conversation is not a decided constraint.
