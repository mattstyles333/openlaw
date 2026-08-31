"""Drive the shipped scripts/openlaw CLI (skills entry). Offline. Not a copy."""

from __future__ import annotations

import re
import subprocess
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CLI = ROOT / "scripts" / "openlaw"
_WROTE = re.compile(r"^Wrote (\S+)", re.M)


def _run(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(CLI), *args],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
    )


def test_cli_exists_and_is_executable() -> None:
    assert CLI.is_file()
    assert CLI.stat().st_mode & 0o111
    text = CLI.read_text(encoding="utf-8")
    assert "Not a memory product" in text or "not a memory" in text.lower()
    assert "NOT search" in text or "not search" in text.lower()


def test_openlaw_law_prints_shipped_markdown() -> None:
    proc = _run(["law"])
    assert proc.returncode == 0
    body = proc.stdout
    for name in ("constraints.md", "brand.md", "sor.md"):
        assert f"<!-- law/{name} -->" in body
        shipped = (ROOT / "law" / name).read_text(encoding="utf-8").strip()
        assert shipped in body
    assert "MUST never invent company policy" in body
    extra = _run(["law", "this-is-not-a-search-query"])
    assert extra.returncode == 0
    assert (ROOT / "law" / "constraints.md").read_text(encoding="utf-8").strip() in extra.stdout


def test_openlaw_priorities_and_permissions() -> None:
    pri = _run(["priorities"])
    assert pri.returncode == 0
    assert pri.stdout == (ROOT / "law" / "priorities.md").read_text(encoding="utf-8")
    perm = _run(["permissions"])
    assert perm.returncode == 0
    assert perm.stdout == (ROOT / "law" / "permissions.md").read_text(encoding="utf-8")


def test_openlaw_help_and_unknown() -> None:
    help_ = _run(["help"])
    assert help_.returncode == 0
    for name in (
        "law",
        "priorities",
        "permissions",
        "check",
        "decisions",
        "propose",
        "grok-to-hermes",
    ):
        assert name in help_.stdout
    assert "export-folder" in help_.stdout
    assert "share.json" not in help_.stdout
    default = _run([])
    assert default.returncode == 0
    assert "Usage:" in default.stdout
    bad = _run(["not-a-command"], check=False)
    assert bad.returncode != 0
    assert "unknown command" in bad.stderr


def test_openlaw_check_runs_shipped_check_law() -> None:
    proc = _run(["check"])
    assert proc.returncode == 0
    assert "check-law: all gates passed" in proc.stdout
    assert "scripts/openlaw" in (ROOT / "scripts" / "check-law.sh").read_text(
        encoding="utf-8"
    )


def test_openlaw_decisions_prints_shipped_adr() -> None:
    files = sorted((ROOT / "decisions").glob("20*.md"))
    assert files, "need at least one shipped decisions/20*.md"
    proc = _run(["decisions"])
    assert proc.returncode == 0
    body = proc.stdout
    shipped = files[0].read_text(encoding="utf-8")
    assert shipped.strip() in body
    assert f"<!-- decisions/{files[0].name} -->" in body
    extra = _run(["decisions", "this-is-not-a-search-query"])
    assert extra.returncode == 0
    assert shipped.strip() in extra.stdout


def test_openlaw_propose_writes_proposed_adr_without_touching_law() -> None:
    constraints = ROOT / "law" / "constraints.md"
    agents = ROOT / "AGENTS.md"
    before_constraints = constraints.read_text(encoding="utf-8")
    before_agents = agents.read_text(encoding="utf-8")
    slug = f"cli-pytest-{uuid.uuid4().hex[:12]}"
    proc = _run(["propose", slug], check=False)
    created: Path | None = None
    try:
        assert proc.returncode == 0, proc.stderr
        match = _WROTE.search(proc.stdout)
        assert match, f"stdout missing Wrote path:\n{proc.stdout}"
        rel = match.group(1)
        created = ROOT / rel
        assert created.is_file(), created
        assert created.parent == ROOT / "decisions" / "proposed"
        body = created.read_text(encoding="utf-8")
        assert re.search(r"^status:\s*proposed\s*$", body, re.M)
        assert constraints.read_text(encoding="utf-8") == before_constraints
        assert agents.read_text(encoding="utf-8") == before_agents
        assert "Never auto-merge law" in proc.stdout
    finally:
        if created is not None and created.exists():
            created.unlink()
        assert constraints.read_text(encoding="utf-8") == before_constraints
        assert agents.read_text(encoding="utf-8") == before_agents
