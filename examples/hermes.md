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
