"""Drive shipped scripts/propose.sh and Slice C learning-loop artifacts.

Invokes the real script from repo root. Does not copy, mock, or start
with the output file already present. Cleans up generated drafts.
"""

from __future__ import annotations

import re
import subprocess
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PROPOSE = ROOT / "scripts" / "propose.sh"
TEMPLATE = ROOT / "decisions" / "_template.md"
PROPOSED_DIR = ROOT / "decisions" / "proposed"
LEARNING = ROOT / "docs" / "LEARNING.md"
ADR = ROOT / "decisions" / "2026-08-30-propose-merge.md"
PR_TEMPLATE = ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md"
GITKEEP = PROPOSED_DIR / ".gitkeep"
PR_LAW_REVIEW = ROOT / ".github" / "workflows" / "pr-law-review.yml"

_WROTE = re.compile(r"^Wrote (\S+)", re.M)


def _run_propose(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(PROPOSE), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def _created_path(stdout: str) -> Path:
    match = _WROTE.search(stdout)
    assert match, f"stdout missing Wrote path:\n{stdout}"
    rel = match.group(1)
    assert not Path(rel).is_absolute(), rel
    path = ROOT / rel
    assert path.is_file(), path
    return path


def test_learning_loop_artifacts_exist_with_needles() -> None:
    assert LEARNING.is_file()
    assert ADR.is_file()
    assert TEMPLATE.is_file()
    assert GITKEEP.is_file()
    assert PR_TEMPLATE.is_file()
    learning = LEARNING.read_text(encoding="utf-8")
    adr = ADR.read_text(encoding="utf-8")
    for blob in (learning, adr):
        low = blob.lower()
        assert "propose" in low
        assert "review" in low
        assert "merge" in low
        assert "CODEOWNERS" in blob
        assert "never auto-merge law" in low
        assert "status: proposed" in blob
        assert "decisions/proposed/" in blob
        assert "AGENTS.md" in blob
        assert "law/" in blob
    assert "proposal vs law change" in PR_TEMPLATE.read_text(encoding="utf-8")
    assert re.search(r"^date:", adr, re.M)
    assert re.search(r"^owner:", adr, re.M)
    assert re.search(r"^status:\s*(proposed|decided|superseded)\s*$", adr, re.M)
    low_learning = learning.lower()
    assert "discussion room" in low_learning
    assert "silent" in low_learning
    assert "github" in low_learning
    assert "pull request" in low_learning
    assert "webhook" in low_learning
    assert "pr-law-review.yml" in learning
    assert "onboarding" in low_learning
    assert "fail soft" in low_learning


def test_propose_sh_copies_template_and_prints_next_steps() -> None:
    assert PROPOSE.is_file()
    assert PROPOSE.stat().st_mode & 0o111
    template = TEMPLATE.read_text(encoding="utf-8")
    slug = f"pytest-{uuid.uuid4().hex[:12]}"
    today = subprocess.check_output(["date", "-u", "+%Y-%m-%d"], text=True).strip()
    expected = PROPOSED_DIR / f"{today}-{slug}.md"
    assert not expected.exists(), expected

    proc = _run_propose(slug)
    created: Path | None = None
    try:
        assert proc.returncode == 0, proc.stderr
        created = _created_path(proc.stdout)
        assert created == expected
        body = created.read_text(encoding="utf-8")
        normalized = body.replace(f"date: {today}", "date: YYYY-MM-DD", 1)
        assert normalized == template
        assert "Copied by `scripts/propose.sh`" in body
        out = proc.stdout
        assert "Next steps:" in out
        assert "proposal vs law change" in out
        assert "CODEOWNERS" in out
        assert "Never auto-merge law" in out
        assert "law/" in out
        assert "AGENTS.md" in out
        assert "do not" in out.lower()
    finally:
        if created is not None and created.exists():
            created.unlink()
        elif expected.exists():
            expected.unlink()


def test_propose_sh_second_run_with_same_slug_writes_another_file() -> None:
    slug = f"pytest-twice-{uuid.uuid4().hex[:8]}"
    created: list[Path] = []
    try:
        first = _run_propose(slug)
        assert first.returncode == 0, first.stderr
        p1 = _created_path(first.stdout)
        created.append(p1)
        second = _run_propose(slug)
        assert second.returncode == 0, second.stderr
        p2 = _created_path(second.stdout)
        created.append(p2)
        assert p1 != p2
        assert p1.exists() and p2.exists()
        assert "Next steps:" in first.stdout
        assert "Next steps:" in second.stdout
        template = TEMPLATE.read_text(encoding="utf-8")
        today = subprocess.check_output(["date", "-u", "+%Y-%m-%d"], text=True).strip()
        for path in (p1, p2):
            body = path.read_text(encoding="utf-8")
            assert body.replace(f"date: {today}", "date: YYYY-MM-DD", 1) == template
    finally:
        for path in created:
            if path.exists():
                path.unlink()


def test_pr_law_review_workflow_runs_check_law_and_fail_soft_comment() -> None:
    assert PR_LAW_REVIEW.is_file()
    text = PR_LAW_REVIEW.read_text(encoding="utf-8")
    assert "pull_request:" in text
    assert "scripts/check-law.sh" in text
    assert "actions/github-script@" in text
    assert "continue-on-error: true" in text
    assert "fail soft" in text.lower()
    assert "pull-requests: write" in text
    assert "never auto-merge law" in text.lower()
    assert "gh pr merge" not in text
    assert "pulls.merge" not in text
    assert "API_KEY=" not in text
    assert "sk-live-" not in text
    assert "ghp_" not in text
    assert "gho_" not in text
    assert "password:" not in text


def test_propose_sh_source_is_offline_and_has_no_secrets() -> None:
    text = PROPOSE.read_text(encoding="utf-8")
    assert not re.search(r"\bcurl\b", text)
    assert not re.search(r"\bwget\b", text)
    assert not re.search(r"\bgh\b", text)
    assert not re.search(r"\bssh\b", text)
    assert "API_KEY=" not in text
    assert "sk-live-" not in text
    assert "ghp_" not in text
    assert "gho_" not in text
    assert "password:" not in text
    assert "BEGIN RSA PRIVATE KEY" not in text
