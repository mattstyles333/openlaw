# Herdr

Herdr is a **multiplexer, not a brain**. It does not store policy, it
does not retrieve policy, and it does not outrank `AGENTS.md`. Each
pane is an agent with a working directory; Openlaw lives in that
directory.

## Pane cwd = repo

Start the pane with cwd set to the Openlaw clone (or to the product
repo that is your law fork):

```bash
cd /path/to/openlaw   # or your fork
grok --resume           # continue this pane; do not start a second brain
```

The agent loads `AGENTS.md` from cwd the same way Grok Build does.
Herdr's job is to keep panes, tmux, and resumes straight — not to
interpret constraints.

## What not to do

- Do not run a "law pane" that summarises `law/` into Herdr-level
  memory and then tell other panes to trust the summary. That is a
  vector store with extra steps.
- Do not let a specialist pane edit `law/constraints.md` because the
  multiplexer had it focused. Specialists propose ADRs.
- Do not treat `grok --resume` as a source of truth. Resume is
  conversation continuity. Law is git.

## Optional MCP

Only if the pane cannot see the working tree (unusual for Herdr).
Same HTTP + bearer rules as every other harness: public HTTPS,
`OPENLAW_MCP_TOKEN` required on the server, missing bearer is **401**.
Prefer the files on disk.

## Wipe / start fresh

Law stays in git. Wipe the *pane* so the agent is blank, then re-read
`AGENTS.md`.

```bash
bash scripts/reset-onboarding.sh
# New Herdr pane, cwd = this repo, or a new /goal.
# Do not grok --resume if you want a blank agent.
```

## Checks

- Two panes on the same repo quote the same hard rules.
- A resume after restart still has `AGENTS.md`; you did not have to
  "remind" Herdr of policy.
- After wipe + new pane / new `/goal`, the three hard rules load from
  git without a reminder.
