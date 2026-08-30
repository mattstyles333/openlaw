"""Shipped aha copy, llms.txt, docs-only onboarding, and reset-onboarding.sh.

Reads repo files and runs the real reset script. Not copies.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
README = ROOT / "README.md"
HOME = ROOT / "site" / "src" / "pages" / "index.astro"
LLMS = ROOT / "llms.txt"
LLMS_PAGES = ROOT / "site" / "public" / "llms.txt"
ONBOARD = ROOT / "site" / "src" / "content" / "docs" / "docs" / "onboarding.mdx"
HARNESS_DOCS = ROOT / "docs" / "HARNESS.md"
RESET = ROOT / "scripts" / "reset-onboarding.sh"
CONSTRAINTS = ROOT / "law" / "constraints.md"
EXAMPLES = ROOT / "examples"


def _head15(path: Path) -> str:
    return "\n".join(path.read_text(encoding="utf-8").splitlines()[:15])


def test_readme_first_15_lines_are_the_aha() -> None:
    head = _head15(README)
    low = head.lower()
    assert "retrieve" in low
    assert "hope" in low
    assert "always-on law" in low
    assert "git markdown" in low
    assert "ci" in low
    assert "mit" in low or "open source" in low
    assert "northwind" in low


def test_homepage_first_viewport_same_aha() -> None:
    text = HOME.read_text(encoding="utf-8")
    low = text.lower()
    assert "retrieve" in low
    assert "hope" in low
    assert "always-on law" in low
    assert "git markdown" in low
    assert "ci" in low
    assert "canon-hero.png" in text
    assert "not a brain" in low
    assert "memory saas" in low


def test_discovery_terms_in_readme_or_site() -> None:
    blob = "\n".join(
        [
            README.read_text(encoding="utf-8"),
            HOME.read_text(encoding="utf-8"),
            LLMS.read_text(encoding="utf-8"),
            ONBOARD.read_text(encoding="utf-8"),
        ]
    )
    required = [
        "open source",
        "MIT",
        "free forever",
        "self-hosted",
        "self host",
        "no SaaS",
        "no vendor lock-in",
        "local-first",
        "MCP",
        "AGENTS.md",
        "git markdown",
        "CI",
    ]
    missing = [t for t in required if t not in blob and t.lower() not in blob.lower()]
    assert missing == [], missing


def test_llms_txt_is_and_is_not_and_three_steps() -> None:
    for path in (LLMS, LLMS_PAGES):
        text = path.read_text(encoding="utf-8")
        low = text.lower()
        assert "what it is" in low
        assert "what it is not" in low
        assert "3-step onboard" in low
        assert "always-on law" in low
        assert "clone or fork" in low or "clone" in low
        assert "check-law.sh" in text
        assert path.is_file()
    assert LLMS.read_text(encoding="utf-8") == LLMS_PAGES.read_text(encoding="utf-8")


def test_onboarding_documents_full_stack_and_restart() -> None:
    text = "\n".join(
        [
            ONBOARD.read_text(encoding="utf-8"),
            HARNESS_DOCS.read_text(encoding="utf-8"),
            (EXAMPLES / "herdr.md").read_text(encoding="utf-8"),
            (EXAMPLES / "grok-build.md").read_text(encoding="utf-8"),
            (EXAMPLES / "grok-bot.md").read_text(encoding="utf-8"),
            (EXAMPLES / "hermes.md").read_text(encoding="utf-8"),
            (EXAMPLES / "opencode.md").read_text(encoding="utf-8"),
        ]
    )
    assert "cwd" in text.lower()
    assert "git repo" in text.lower() or "this git repo" in text.lower()
    assert "/workspace" in text
    assert "account-wide HTTP MCP" in text or "account-wide HTTP" in text
    assert "excerpt-soul.sh" in text
    assert "memory.provider" in text
    assert "unset" in text
    assert "oauth" in text.lower()
    assert "false" in text
    assert "Bearer" in text or "bearer" in text
    assert "CANON_MCP_TOKEN" in text
    assert "ghcr.io/mattstyles333/canon-mcp:0.1.0" in text
    assert "law-check" in text or "GitHub Actions" in text
    assert "Restart from zero" in text
    assert "reset-onboarding.sh" in text
    assert "/goal" in text


def test_reset_onboarding_script_restores_northwind_and_prints_wipes() -> None:
    assert RESET.is_file()
    assert RESET.stat().st_mode & 0o111
    proc = subprocess.run(
        ["bash", str(RESET)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    out = proc.stdout
    assert proc.returncode == 0
    assert "Northwind Coffee" in CONSTRAINTS.read_text(encoding="utf-8")
    assert "Herdr" in out
    assert "/goal" in out
    assert "Grok Bot" in out or "Bot thread" in out
    assert "Hermes" in out
    assert "OpenCode" in out
    assert "memory.provider" in out
