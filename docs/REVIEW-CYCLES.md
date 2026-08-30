# Review cycles (Openlaw v0.1)

Three independent review cycles. Each lists findings, in-repo fixes,
re-run results, and what still fails. Cycles 2 and 3 inspect different
bug classes than cycle 1. Example law remains Northwind Coffee.

## Cycle 1 — 2026-08-30 — auth / fail-closed

Class: MCP HTTP projection authentication. Git is the source of truth;
this cycle only checks that the optional projection fails closed.

### Findings

- `mcp/tests` set a fixture token via `setdefault` and never called
  `create_app()` or `main()` with `CANON_MCP_TOKEN` missing, so the
  refuse-to-listen path was unproven.
- Wrong bearer was not asserted (only missing header).
- Bearer `get_law` did not assert the Northwind example company by name.
- `mcp_token()` treated whitespace-only env values as a live token, so
  `CANON_MCP_TOKEN="   "` would listen instead of failing closed.
- `scripts/check-law.sh` grepped `execute_sql` only in `mcp/server.py`,
  not other shipped Python under `mcp/`.

### Fixes

- Strip MCP and commit tokens; blank/whitespace is unset.
- Tests now drive shipped `server.create_app` / `server.main`: Northwind
  + `MUST never invent company policy` with bearer; HTTP 401 without
  bearer and with a wrong bearer; `SystemExit` refuse-to-listen when the
  token is missing or blank; shipped `server.py` has no `execute_sql`.
- `check-law.sh` greps `execute_sql` across shipped `mcp/` Python
  (excludes `.venv` and `tests/`).

### Re-run

- `bash scripts/check-law.sh` — exit 0 (`check-law-cycle1.log`).
- `pytest tests` in `mcp/` — 7 passed (`mcp-pytest-cycle1.log`).

### Still fails

- Starlette `TestClient` emits a deprecation warning (httpx vs httpx2).
  Tests still hit the shipped ASGI app. Not a fail-open.

## Cycle 2 — 2026-08-30 — law size, secret scan, product-name tokens

Class: law file budget, credential patterns, and product-name
consistency in the public tree. Not a re-run of cycle 1's auth review.

### Findings

- `AGENTS.md` is 37 lines / 1533 bytes (caps 80 / 12000). Size is fine;
  no trim required.
- Secret-pattern grep covered only `law/` and `AGENTS.md`. `decisions/`
  and `examples/` could have held `ghp_`, `sk-live-`, or `password:`.
- `.gitleaks.toml` allowlisted env-var *names* with no path filter, which
  could hide `CANON_MCP_TOKEN=<secret>` in an arbitrary file.
- CI did not fail the tree on stray product-name tokens (needles live
  only in `scripts/check-law.sh`). Phrase "always-on law" is allowed.
- Compose already had no `${CANON_MCP_TOKEN:-...}` default; CI did not
  assert that.

### Fixes

- Secret-pattern grep now includes `decisions/` and `examples/`.
- `check-law.sh` fails if compose defaults `CANON_MCP_TOKEN`.
- `check-law.sh` greps the tree (excluding `.git`, `.venv`, and itself)
  for forbidden product-name tokens. Phrase "always-on law" is allowed.
- Gitleaks name allowlist is path-scoped to docs, CI, compose, scripts,
  and the MCP module.

### Re-run

- `bash scripts/check-law.sh` — exit 0 (`check-law-cycle2.log`).
- `pytest tests` in `mcp/` — 7 passed (`mcp-pytest-cycle2.log`).
- Product-name gate: no hits. Northwind still present in `law/`.

### Still fails

- The second Gitleaks allowlist still ignores the words `bearer` and
  `token` in markdown/CI so docs can name them. Prefix rules (`ghp_`,
  `sk-live-`) still apply. Residual risk: a generic high-entropy rule
  whose match is only those words.

## Cycle 3 — 2026-08-30 — harness attach examples

Class: how existing harnesses load `AGENTS.md` / `law/` and attach the
optional MCP. Not auth internals (cycle 1) and not secret or
product-name gates (cycle 2).

### Findings

- `docs/HARNESS.md` listed Claude Code and Gemini CLI with no example
  files (unlike Grok Build, Grok Bot, Herdr, OpenCode, Hermes).
- `examples/herdr.md` optional-MCP paragraph did not name
  `CANON_MCP_TOKEN` or 401.
- `examples/grok-build.md` `grok mcp add` did not say the client must
  send the bearer and must not commit it.
- `examples/hermes.md` optional MCP did not name `CANON_MCP_TOKEN`.
- `check-law.sh` did not require the example recipes to exist, so a
  deleted attach file would not fail CI.
- `scripts/excerpt-soul.sh` did not mention that a missing MCP bearer
  is 401.

### Fixes

- Added `examples/claude.md` and `examples/gemini.md`; linked from
  `docs/HARNESS.md` and the README matrix.
- Herdr / Grok Build / Hermes examples now state public HTTPS, required
  `CANON_MCP_TOKEN`, and HTTP 401 without bearer.
- `check-law.sh` requires the seven example files.
- Soul excerpt notes missing bearer is 401.

### Re-run

- `bash scripts/check-law.sh` — exit 0 (`check-law-cycle3.log`).
- `pytest tests` in `mcp/` — 7 passed (`mcp-pytest-cycle3.log`).

### Still fails

- No dedicated example for every possible fork of OpenCode config keys
  (the OpenCode file already says keys move between releases; invariant
  is remote HTTP + bearer, oauth false).
