"""MCP HTTP wrap of the shipped scripts/openlaw CLI.

Drives create_app() with a real bearer. Compares HTTP bodies to
`bash scripts/openlaw <command>` on this tree — does not hard-code markdown
or reimplement the CLI.
"""

from __future__ import annotations

import os
import re
import subprocess
import uuid
from pathlib import Path

from starlette.testclient import TestClient

import server

ROOT = Path(__file__).resolve().parent.parent.parent
CLI = ROOT / "scripts" / "openlaw"
TOKEN = os.environ.get("OPENLAW_MCP_TOKEN") or os.environ["CANON_MCP_TOKEN"]
AUTH = {"Authorization": f"Bearer {TOKEN}"}
_WROTE = re.compile(r"^Wrote (\S+)", re.M)
_ADR = re.compile(r"decisions/proposed/\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md")


def _cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(CLI), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )


def _client() -> TestClient:
    return TestClient(server.create_app())


def test_server_invokes_shipped_openlaw_cli() -> None:
    text = (ROOT / "mcp" / "server.py").read_text(encoding="utf-8")
    assert "scripts/openlaw" in text
    assert "run_openlaw" in text
    assert "bash" in text


def test_wrap_reads_match_cli_stdout_and_on_disk_files() -> None:
    client = _client()
    for cmd in ("law", "priorities", "permissions", "check", "decisions"):
        proc = _cli(cmd)
        response = client.get(f"/tools/{cmd}", headers=AUTH)
        assert response.status_code == 200, f"{cmd}: {response.text[:500]}"
        assert response.text == proc.stdout, f"{cmd} HTTP body != scripts/openlaw {cmd}"

    law_body = client.get("/tools/law", headers=AUTH).text
    for name in ("constraints.md", "brand.md", "sor.md"):
        shipped = (ROOT / "law" / name).read_text(encoding="utf-8").strip()
        assert shipped in law_body
        assert f"<!-- law/{name} -->" in law_body
    assert "MUST never invent company policy" in law_body

    pri = client.get("/tools/priorities", headers=AUTH).text
    assert pri == (ROOT / "law" / "priorities.md").read_text(encoding="utf-8")
    perm = client.get("/tools/permissions", headers=AUTH).text
    assert perm == (ROOT / "law" / "permissions.md").read_text(encoding="utf-8")

    alias = client.get("/tools/get_law", headers=AUTH)
    assert alias.status_code == 200
    assert alias.text == _cli("law").stdout


def test_wrap_propose_invokes_cli_without_touching_law_or_agents() -> None:
    constraints = ROOT / "law" / "constraints.md"
    agents = ROOT / "AGENTS.md"
    before_constraints = constraints.read_text(encoding="utf-8")
    before_agents = agents.read_text(encoding="utf-8")
    cli_slug = f"wrap-cli-{uuid.uuid4().hex[:10]}"
    mcp_slug = f"wrap-mcp-{uuid.uuid4().hex[:10]}"
    created: list[Path] = []
    try:
        cli_proc = _cli("propose", cli_slug)
        cli_match = _WROTE.search(cli_proc.stdout)
        assert cli_match, cli_proc.stdout
        created.append(ROOT / cli_match.group(1))

        client = _client()
        response = client.post(
            "/tools/propose",
            headers=AUTH,
            json={"slug": mcp_slug},
        )
        assert response.status_code == 200, response.text
        mcp_match = _WROTE.search(response.text)
        assert mcp_match, response.text
        created.append(ROOT / mcp_match.group(1))
        assert created[-1].is_file()
        assert created[-1].parent == ROOT / "decisions" / "proposed"
        body = created[-1].read_text(encoding="utf-8")
        assert re.search(r"^status:\s*proposed\s*$", body, re.M)

        def _norm(text: str) -> str:
            return _ADR.sub("decisions/proposed/DATE-slug.md", text)

        assert _norm(response.text) == _norm(cli_proc.stdout)
        assert "Wrote" in response.text
        assert "proposed" in response.text.lower()
        assert constraints.read_text(encoding="utf-8") == before_constraints
        assert agents.read_text(encoding="utf-8") == before_agents
    finally:
        for path in created:
            if path.exists():
                path.unlink()
        assert constraints.read_text(encoding="utf-8") == before_constraints
        assert agents.read_text(encoding="utf-8") == before_agents


def test_wrap_without_bearer_is_http_401() -> None:
    client = _client()
    response = client.get("/tools/law")
    assert response.status_code == 401
