"""Drive shipped scripts/openlaw grok-to-hermes. Not a copy of the converter."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CLI = ROOT / "scripts" / "openlaw"
FIXTURE = ROOT / "examples" / "fixtures" / "grok-bot-share.json"
EXCERPT = ROOT / "scripts" / "excerpt-soul.sh"


def _run(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(CLI), *args],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
    )


def test_fixture_uses_real_share_template_fields() -> None:
    assert FIXTURE.is_file()
    dump = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert "profile" in dump
    assert dump["profile"]["name"]
    assert "description" in dump["profile"]
    assert isinstance(dump["skills"], list)
    assert dump["skills"][0]["name"]
    assert dump["skills"][0]["content"]
    kinds = {item.get("kind") for item in dump["memory"]}
    assert "profile" in kinds
    assert "log" in kinds


def test_grok_to_hermes_writes_soul_and_skill_excerpts(tmp_path: Path) -> None:
    dump = json.loads(FIXTURE.read_text(encoding="utf-8"))
    out = tmp_path / "hermes-excerpts"
    constraints = ROOT / "law" / "constraints.md"
    agents = ROOT / "AGENTS.md"
    before_c = constraints.read_text(encoding="utf-8")
    before_a = agents.read_text(encoding="utf-8")
    proc = _run(["grok-to-hermes", str(FIXTURE), str(out)])
    assert proc.returncode == 0, proc.stderr
    soul_path = out / "SOUL.md"
    assert soul_path.is_file()
    soul = soul_path.read_text(encoding="utf-8")
    excerpt = subprocess.run(
        ["bash", str(EXCERPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    for needle in (
        "MUST never invent company policy",
        "always-on law is git markdown, never a vector store",
        "MUST propose decisions",
    ):
        assert needle in soul
        assert needle in excerpt
    assert "MEMORY.md" in soul
    assert "Retrieval is not law" in soul
    assert dump["profile"]["name"] in soul
    profile_mem = next(
        item["content"] for item in dump["memory"] if item.get("kind") == "profile"
    )
    log_mem = next(item["content"] for item in dump["memory"] if item.get("kind") == "log")
    assert profile_mem in soul
    assert log_mem not in soul
    skill = dump["skills"][0]
    skill_path = out / "skills" / "roast-dates" / "SKILL.md"
    assert skill_path.is_file()
    body = skill_path.read_text(encoding="utf-8")
    assert skill["content"] in body
    assert skill["name"] in body
    assert not body.lstrip().startswith("---")
    assert not (out / "MEMORY.md").exists()
    assert not (out / "memories").exists()
    assert constraints.read_text(encoding="utf-8") == before_c
    assert agents.read_text(encoding="utf-8") == before_a
    assert "Wrote" in proc.stdout


def test_grok_to_hermes_refuses_law_and_memory_paths(tmp_path: Path) -> None:
    law_out = _run(["grok-to-hermes", str(FIXTURE), str(ROOT / "law")], check=False)
    assert law_out.returncode != 0
    assert "law/" in law_out.stderr
    mem_out = _run(
        ["grok-to-hermes", str(FIXTURE), str(tmp_path / "MEMORY.md")], check=False
    )
    assert mem_out.returncode != 0
    assert "MEMORY.md" in mem_out.stderr
    bad = _run(["grok-to-hermes", str(tmp_path / "missing.json")], check=False)
    assert bad.returncode != 0
    empty = tmp_path / "empty.json"
    empty.write_text("{}\n", encoding="utf-8")
    missing_name = _run(["grok-to-hermes", str(empty)], check=False)
    assert missing_name.returncode != 0
    not_obj = tmp_path / "list.json"
    not_obj.write_text("[]\n", encoding="utf-8")
    listed = _run(["grok-to-hermes", str(not_obj)], check=False)
    assert listed.returncode != 0
