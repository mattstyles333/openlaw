"""Drive shipped scripts/openlaw grok-to-hermes. Not a copy of the converter."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CLI = ROOT / "scripts" / "openlaw"
FIXTURE = ROOT / "examples" / "fixtures" / "grok-bot-export"
EXCERPT = ROOT / "scripts" / "excerpt-soul.sh"


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(CLI), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _copy_fixture(dest: Path) -> Path:
    shutil.copytree(FIXTURE, dest)
    return dest


def test_fixture_is_markdown_export_folder() -> None:
    assert FIXTURE.is_dir()
    assert (FIXTURE / "SOUL.md").is_file()
    skills = list((FIXTURE / "skills").glob("*.md"))
    assert len(skills) >= 2
    assert not (ROOT / "examples" / "fixtures" / "grok-bot-share.json").exists()


def test_grok_to_hermes_markdown_folder_happy_path(tmp_path: Path) -> None:
    out = tmp_path / "hermes-excerpts"
    constraints = ROOT / "law" / "constraints.md"
    agents = ROOT / "AGENTS.md"
    before_c = constraints.read_text(encoding="utf-8")
    before_a = agents.read_text(encoding="utf-8")
    proc = _run(["grok-to-hermes", str(FIXTURE), str(out)])
    assert proc.returncode == 0, proc.stderr
    assert "Traceback" not in proc.stderr
    soul = (out / "SOUL.md").read_text(encoding="utf-8")
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
    assert "Retrieval is not law" in soul
    assert "MEMORY.md" in soul
    identity = (FIXTURE / "SOUL.md").read_text(encoding="utf-8")
    assert "northwind-law" in soul
    assert "Northwind Coffee law bot" in soul
    for skill_src in (FIXTURE / "skills").glob("*.md"):
        src_body = skill_src.read_text(encoding="utf-8").strip()
        written = list((out / "skills").glob(f"*/SKILL.md"))
        assert any(src_body in p.read_text(encoding="utf-8") for p in written), skill_src.name
    roast = out / "skills" / "roast-dates" / "SKILL.md"
    assert roast.is_file()
    roast_text = roast.read_text(encoding="utf-8")
    assert roast_text.startswith("---\nname: roast-dates\n")
    assert "description:" in roast_text.split("---", 2)[1]
    assert not (out / "MEMORY.md").exists()
    assert not (out / "memories").exists()
    assert constraints.read_text(encoding="utf-8") == before_c
    assert agents.read_text(encoding="utf-8") == before_a
    assert "Wrote" in proc.stdout
    assert "routines.md" in proc.stderr
    assert identity.strip() in soul


def test_grok_to_hermes_emits_yaml_frontmatter(tmp_path: Path) -> None:
    out = tmp_path / "out"
    proc = _run(["grok-to-hermes", str(FIXTURE), str(out)])
    assert proc.returncode == 0, proc.stderr
    for skill in (out / "skills").glob("*/SKILL.md"):
        text = skill.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        _, fm, _body = text.split("---", 2)
        assert "name:" in fm
        assert "description:" in fm
        assert skill.parent.name in fm


def test_grok_to_hermes_slug_collision_and_all_punctuation_fail(tmp_path: Path) -> None:
    export = tmp_path / "collide"
    export.mkdir()
    (export / "SOUL.md").write_text("# bot\n", encoding="utf-8")
    skills = export / "skills"
    skills.mkdir()
    (skills / "Roast-Dates.md").write_text("# Roast Dates\n\nA\n", encoding="utf-8")
    (skills / "roast_dates.md").write_text("# roast_dates\n\nB\n", encoding="utf-8")
    out = tmp_path / "out-collide"
    proc = _run(["grok-to-hermes", str(export), str(out)])
    assert proc.returncode != 0
    assert "Traceback" not in proc.stderr
    assert "collision" in proc.stderr.lower()
    assert "Roast-Dates.md" in proc.stderr
    assert "roast_dates.md" in proc.stderr

    punct = tmp_path / "punct"
    punct.mkdir()
    (punct / "SOUL.md").write_text("# bot\n", encoding="utf-8")
    (punct / "skills").mkdir()
    (punct / "skills" / "bang.md").write_text("# !!!\n\nno slug\n", encoding="utf-8")
    proc2 = _run(["grok-to-hermes", str(punct), str(tmp_path / "out-punct")])
    assert proc2.returncode != 0
    assert "Traceback" not in proc2.stderr
    assert "all-punctuation" in proc2.stderr


def test_grok_to_hermes_kind_profile_whitelist(tmp_path: Path) -> None:
    export = _copy_fixture(tmp_path / "export-mem")
    sidecar = {
        "not": "used as primary export",
    }
    (export / "memory.json").write_text(
        json.dumps(
            [
                {"kind": "profile", "content": "Northwind is a fictional independent coffee roaster and cafe."},
                {"kind": "log", "content": "Tuesday 09:14: opened the till."},
                {"content": "no-kind line must not enter SOUL"},
                {"kind": "profile", "content": 12345},
            ]
        ),
        encoding="utf-8",
    )
    del sidecar
    out = tmp_path / "out-mem"
    proc = _run(["grok-to-hermes", str(export), str(out)])
    assert proc.returncode == 0, proc.stderr
    soul = (out / "SOUL.md").read_text(encoding="utf-8")
    assert "Durable conventions" in soul
    assert "fictional independent coffee roaster" in soul
    assert "opened the till" not in soul
    assert "no-kind line" not in soul
    assert "12345" not in soul
    assert "kind='log'" in proc.stderr or 'kind="log"' in proc.stderr or "kind=log" in proc.stderr
    assert "no-kind" in proc.stderr
    assert "non-string" in proc.stderr


def test_grok_to_hermes_rerun_warns_and_prunes_stale_skills(tmp_path: Path) -> None:
    export_a = tmp_path / "export-a"
    export_a.mkdir()
    (export_a / "SOUL.md").write_text("# first-soul\n", encoding="utf-8")
    (export_a / "skills").mkdir()
    (export_a / "skills" / "alpha.md").write_text("# Alpha\n\nalpha body unique\n", encoding="utf-8")
    out = tmp_path / "out-rerun"
    first = _run(["grok-to-hermes", str(export_a), str(out)])
    assert first.returncode == 0, first.stderr
    assert (out / "skills" / "alpha" / "SKILL.md").is_file()

    export_b = tmp_path / "export-b"
    export_b.mkdir()
    (export_b / "SOUL.md").write_text("# second-soul\n", encoding="utf-8")
    (export_b / "skills").mkdir()
    (export_b / "skills" / "beta.md").write_text("# Beta\n\nbeta body unique\n", encoding="utf-8")
    second = _run(["grok-to-hermes", str(export_b), str(out)])
    assert second.returncode == 0, second.stderr
    assert "warn:" in second.stderr
    assert "pruned" in second.stderr
    assert not (out / "skills" / "alpha").exists()
    assert (out / "skills" / "beta" / "SKILL.md").is_file()
    soul = (out / "SOUL.md").read_text(encoding="utf-8")
    assert "second-soul" in soul
    assert "first-soul" not in soul
    assert "beta body unique" in (out / "skills" / "beta" / "SKILL.md").read_text(
        encoding="utf-8"
    )


def test_grok_to_hermes_refuses_law_root_file_and_memory(tmp_path: Path) -> None:
    existing = tmp_path / "already-a-file"
    existing.write_text("nope\n", encoding="utf-8")
    cases = [
        (ROOT / "law", "law/"),
        (ROOT, "repository root"),
        (existing, "existing file"),
        (tmp_path / "MEMORY.md", "MEMORY.md"),
    ]
    for dest, needle in cases:
        proc = _run(["grok-to-hermes", str(FIXTURE), str(dest)])
        assert proc.returncode != 0, dest
        assert "Traceback" not in proc.stderr, proc.stderr
        assert "FAIL:" in proc.stderr
        assert needle in proc.stderr
    missing = _run(["grok-to-hermes", str(tmp_path / "missing-export"), str(tmp_path / "out")])
    assert missing.returncode != 0
    assert "Traceback" not in missing.stderr
    json_file = tmp_path / "not-a-folder.json"
    json_file.write_text("{}\n", encoding="utf-8")
    as_file = _run(["grok-to-hermes", str(json_file), str(tmp_path / "out2")])
    assert as_file.returncode != 0
    assert "folder" in as_file.stderr
    assert "Traceback" not in as_file.stderr
