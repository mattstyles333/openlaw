"""Drive shipped scripts/openlaw grok-to-hermes. Not a copy of the converter."""

from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

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


def _frontmatter(text: str) -> dict:
    assert text.startswith("---\n"), text[:80]
    _, fm, _body = text.split("---", 2)
    data = yaml.safe_load(fm)
    assert isinstance(data, dict)
    return data


def test_fixture_is_freeze_export_folder() -> None:
    assert FIXTURE.is_dir()
    assert not (FIXTURE / "SOUL.md").exists()
    assert not (FIXTURE / "instructions.md").exists()
    assert not (FIXTURE / "memory.json").exists()
    assert (FIXTURE / "00-FREEZE.md").is_file()
    assert (FIXTURE / "README.md").is_file()
    assert (FIXTURE / "grok-bot" / "roster.md").is_file()
    assert (FIXTURE / "grok-bot" / "skills.md").is_file()
    assert (FIXTURE / "grok-bot" / "memory.md").is_file()
    assert (FIXTURE / "secrets-redacted.md").is_file()
    secrets = (FIXTURE / "secrets-redacted.md").read_text(encoding="utf-8")
    assert "FAKE" in secrets
    assert "password:" not in secrets
    assert "API_KEY=" not in secrets
    assert "sk-live-" not in secrets
    assert "ghp_" not in secrets


def test_grok_to_hermes_freeze_export_happy_path(tmp_path: Path) -> None:
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
    roster = (FIXTURE / "grok-bot" / "roster.md").read_text(encoding="utf-8")
    assert "Openlaw law bot" in soul
    assert "sample freeze export" in soul
    assert roster.splitlines()[0].lstrip("#").strip() in soul or "Roster" in soul
    git_law = out / "skills" / "git-markdown-law" / "SKILL.md"
    assert git_law.is_file()
    git_text = git_law.read_text(encoding="utf-8")
    assert git_text.startswith("---\n")
    meta = _frontmatter(git_text)
    assert meta["name"] == "git-markdown-law"
    assert isinstance(meta["name"], str)
    assert not (out / "skills" / "roast-dates").exists()
    assert not (out / "skills" / "cafe-hours").exists()
    skill_dirs = {p.name for p in (out / "skills").iterdir() if p.is_dir()}
    for junk in skill_dirs:
        assert not junk.startswith("user-created")
        assert not junk.startswith("cursor-managed")
        assert not junk.startswith("plugin-skills")
    assert "registry" in proc.stderr or "User-created" in proc.stderr
    assert "70% off" in soul
    assert "£19.97" in soul
    assert "WINBACK5" in soul
    assert "FAKE-PROCESS" in soul
    assert "opened the till" not in soul
    assert not (out / "skills" / "secrets-redacted").exists()
    skill_names = {p.parent.name for p in (out / "skills").glob("*/SKILL.md")}
    for banned in (
        "secrets-redacted",
        "architecture",
        "decisions",
        "in-flight",
        "openlaw",
        "00-freeze",
    ):
        assert banned not in skill_names
    for skipped in (
        "secrets-redacted.md",
        "architecture.md",
        "decisions.md",
        "in-flight.md",
        "openlaw.md",
    ):
        assert skipped in proc.stderr, skipped
    assert not (out / "MEMORY.md").exists()
    assert not (out / "memories").exists()
    assert constraints.read_text(encoding="utf-8") == before_c
    assert agents.read_text(encoding="utf-8") == before_a
    assert "Wrote" in proc.stdout


def test_grok_to_hermes_yaml_safe_frontmatter(tmp_path: Path) -> None:
    export = tmp_path / "yaml-export"
    export.mkdir()
    (export / "README.md").write_text("# yaml-bot\n", encoding="utf-8")
    skills = export / "skills"
    skills.mkdir()
    cases = {
        "colon.md": "# Note: do this\n\ncolon-space heading\n",
        "dash.md": "# - leading dash\n\ndash heading\n",
        "brace.md": "# {braced}\n\nbrace heading\n",
        "yes.md": "# yes\n\nyes-style heading\n",
    }
    for name, body in cases.items():
        (skills / name).write_text(body, encoding="utf-8")
    out = tmp_path / "yaml-out"
    proc = _run(["grok-to-hermes", str(export), str(out)])
    assert proc.returncode == 0, proc.stderr
    loaded: dict[str, dict] = {}
    for skill in (out / "skills").glob("*/SKILL.md"):
        text = skill.read_text(encoding="utf-8")
        data = _frontmatter(text)
        assert isinstance(data["name"], str)
        assert not isinstance(data["name"], bool)
        assert data["name"] is not None
        loaded[skill.parent.name] = data
    assert "yes" in loaded
    assert loaded["yes"]["name"] == "yes"
    assert any(":" in str(d.get("description", "")) or "Note" in str(d.get("description", "")) for d in loaded.values())
    assert any(str(d.get("description", "")).startswith("-") or "dash" in str(d.get("description", "")).lower() for d in loaded.values())
    assert any("{" in str(d.get("description", "")) or "braced" in str(d.get("description", "")).lower() for d in loaded.values())


def test_grok_to_hermes_slug_collision_and_all_punctuation_fail(tmp_path: Path) -> None:
    export = tmp_path / "collide"
    export.mkdir()
    (export / "README.md").write_text("# bot\n", encoding="utf-8")
    skills = export / "skills"
    skills.mkdir()
    (skills / "Roast-Dates.md").write_text("# Roast Dates\n\nA\n", encoding="utf-8")
    (skills / "roast_dates.md").write_text("# roast_dates\n\nB\n", encoding="utf-8")
    proc = _run(["grok-to-hermes", str(export), str(tmp_path / "out-collide")])
    assert proc.returncode != 0
    assert "Traceback" not in proc.stderr
    assert "collision" in proc.stderr.lower()
    assert "Roast-Dates.md" in proc.stderr
    assert "roast_dates.md" in proc.stderr

    punct = tmp_path / "punct"
    punct.mkdir()
    (punct / "README.md").write_text("# bot\n", encoding="utf-8")
    (punct / "skills").mkdir()
    (punct / "skills" / "bang.md").write_text("# !!!\n\nno slug\n", encoding="utf-8")
    proc2 = _run(["grok-to-hermes", str(punct), str(tmp_path / "out-punct")])
    assert proc2.returncode != 0
    assert "Traceback" not in proc2.stderr
    assert "all-punctuation" in proc2.stderr


def test_grok_to_hermes_honors_memory_md(tmp_path: Path) -> None:
    out = tmp_path / "out-mem"
    proc = _run(["grok-to-hermes", str(FIXTURE), str(out)])
    assert proc.returncode == 0, proc.stderr
    soul = (out / "SOUL.md").read_text(encoding="utf-8")
    memory = (FIXTURE / "grok-bot" / "memory.md").read_text(encoding="utf-8")
    assert "## Durable conventions" not in memory
    assert "FAKE-ORG" in soul
    assert "70% off" in soul
    assert "£19.97" in soul
    assert "WINBACK5" in soul
    assert "FAKE-PROCESS" in soul
    assert "opened the till" not in soul
    assert "Session log" in memory
    assert "Session log" in proc.stderr
    assert not (FIXTURE / "memory.json").exists()


def test_grok_to_hermes_prose_catalog_section_still_maps(tmp_path: Path) -> None:
    export = tmp_path / "prose-cat"
    export.mkdir()
    (export / "README.md").write_text("# bot\n", encoding="utf-8")
    grok = export / "grok-bot"
    grok.mkdir()
    (grok / "skills.md").write_text(
        "# Skills\n\n"
        "## User-created (`/home/box/agent-data/workflows`)\n\n"
        "| id | name | when |\n|---|---|---|\n| five-part-brief | Five-part brief | start |\n\n"
        "## Roast dates\n\n"
        "Print roast dates from the roast log, never invent them.\n\n"
        "Roast dates printed on bags MUST match the roast log. If the log is missing, say so.\n",
        encoding="utf-8",
    )
    out = tmp_path / "prose-out"
    proc = _run(["grok-to-hermes", str(export), str(out)])
    assert proc.returncode == 0, proc.stderr
    assert (out / "skills" / "roast-dates" / "SKILL.md").is_file()
    body = (out / "skills" / "roast-dates" / "SKILL.md").read_text(encoding="utf-8")
    assert "Roast dates printed on bags MUST match the roast log" in body
    skill_dirs = {p.name for p in (out / "skills").iterdir() if p.is_dir()}
    assert not any(n.startswith("user-created") for n in skill_dirs)
    assert "registry" in proc.stderr or "User-created" in proc.stderr


def test_grok_to_hermes_rerun_warns_and_prunes_stale_skills(tmp_path: Path) -> None:
    export_a = tmp_path / "export-a"
    export_a.mkdir()
    (export_a / "README.md").write_text("# first-soul\n", encoding="utf-8")
    (export_a / "skills").mkdir()
    (export_a / "skills" / "alpha.md").write_text("# Alpha\n\nalpha body unique\n", encoding="utf-8")
    out = tmp_path / "out-rerun"
    first = _run(["grok-to-hermes", str(export_a), str(out)])
    assert first.returncode == 0, first.stderr
    assert (out / "skills" / "alpha" / "SKILL.md").is_file()

    export_b = tmp_path / "export-b"
    export_b.mkdir()
    (export_b / "README.md").write_text("# second-soul\n", encoding="utf-8")
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
