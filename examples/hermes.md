# Hermes

Hermes wants a short `SOUL.md`. Openlaw already has the hard rules
in `AGENTS.md`; the excerpt script prints a ~15-line block you can
paste so the soul file stays small.

## Law from git + a short soul excerpt

```bash
cd /path/to/your-openlaw-fork
bash scripts/excerpt-soul.sh
# Paste stdout into SOUL.md. Leave the rest of law in git.
```

The excerpt is the three hard rules plus "retrieval is not law". It
is not a substitute for cloning the repo. Hermes should still have
the working tree (or HTTP MCP) so it can read `law/`.

## Grok Bot freeze-export → Hermes excerpts

Grok Bot export is a **freeze-export folder of named markdown files**,
not a JSON dump and not a required `SOUL.md`. Convert it to
Hermes-loadable `SOUL.md` plus `skills/<slug>/SKILL.md` (YAML
frontmatter). That is git-markdown law, not `MEMORY.md`.

```bash
bash scripts/openlaw grok-to-hermes <export-folder> <out-dir>
```

Example:

```bash
bash scripts/openlaw grok-to-hermes examples/fixtures/grok-bot-export out-dir
# Paste out-dir/SOUL.md into Hermes SOUL.md.
# Copy out-dir/skills/<slug>/SKILL.md into the Hermes profile skills.
# Leave memory.provider unset. Do not copy anything into MEMORY.md.
```

What maps: identity from `grok-bot/roster.md`, `README.md`, and
`00-FREEZE.md`; skills from `grok-bot/skills.md` and `skills/`; durable
conventions from `grok-bot/memory.md`. What does **not** map: routines,
marketplace plugins, session logs, snapshots (`architecture.md`,
`decisions.md`, `in-flight.md`, `openlaw.md`, `00-FREEZE.md` as a
skill), and especially `secrets-redacted.md` (named on stderr). The
converter refuses `law/`, the repo root, `AGENTS.md`, `MEMORY.md`, and
`memories/`.

## Memory is not law

- Leave `memory.provider` **unset** unless you independently want
  recall. Openlaw does not need it.
- Do **not** use `MEMORY.md` as the store of policy. `MEMORY.md` is
  recall. Law is `AGENTS.md` + `law/` in git.
- Do not index `law/` into Hermes memory so it can be "retrieved when
  relevant". That is retrieved-when-similar, which this project
  exists to refuse.

## Optional MCP

Same HTTP + bearer as every other harness. Useful when Hermes is
hosted and cannot see the clone. Public HTTPS for cloud;
`OPENLAW_MCP_TOKEN` required on the server; HTTP 401 without bearer.

## Wipe / start fresh

New Hermes session. Leave `memory.provider` **unset**. Remove or
ignore `MEMORY.md`. Re-paste `bash scripts/excerpt-soul.sh` into
`SOUL.md`. Run `bash scripts/reset-onboarding.sh` on the clone.

## Checks

- `SOUL.md` contains the excerpt and is still short.
- `memory.provider` is unset in the Openlaw-only setup.
- The agent does not treat a `MEMORY.md` anecdote as a constraint.
