"""Shipped leftover gate + Astro/Starlight Pages structure.

Reads scripts/check-law.sh, site/, and .github/workflows/pages.yml — not copies.
Needles in this file are concatenated so the leftover grep does not fire on tests.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECK = ROOT / "scripts" / "check-law.sh"
SITE = ROOT / "site"
PAGES = ROOT / ".github" / "workflows" / "pages.yml"


def test_leftover_gate_needles_and_self_exclude() -> None:
    text = CHECK.read_text(encoding="utf-8")
    always_law_camel = "Always" + "Law"
    always_law_lower = "always" + "law"
    old_env_prefix = "LAW_" + "MCP"
    hyphen_token = "always" + "-law"
    always_on = "always" + "-on"
    needle = "|".join(
        [always_law_camel, always_law_lower, old_env_prefix, hyphen_token]
    )
    assert needle in text
    assert "--exclude=check-law.sh" in text
    assert always_on in text
    assert hyphen_token != always_on
    assert always_on not in needle


def test_site_is_astro_starlight_with_canon_base() -> None:
    pkg = (SITE / "package.json").read_text(encoding="utf-8")
    assert '"astro"' in pkg
    assert "@astrojs/starlight" in pkg
    cfg = (SITE / "astro.config.mjs").read_text(encoding="utf-8")
    assert "base: '/canon/'" in cfg
    assert "mattstyles333.github.io" in cfg
    home = (SITE / "src" / "pages" / "index.astro").read_text(encoding="utf-8")
    assert "canon-hero.png" in home
    assert "canon-mark.png" in home
    assert "canon-og.png" in home
    docs = SITE / "src" / "content" / "docs" / "docs"
    for name in (
        "index.mdx",
        "why.mdx",
        "onboarding.mdx",
        "harness.mdx",
        "security.mdx",
        "mcp.mdx",
        "status.mdx",
    ):
        assert (docs / name).is_file(), name
    onboarding = (docs / "onboarding.mdx").read_text(encoding="utf-8")
    assert "Northwind" in onboarding
    assert "80 lines" in onboarding
    assert "CANON_MCP_TOKEN" in onboarding
    assert "ghcr.io/mattstyles333/canon-mcp:0.1.0" in onboarding
    assert "Grok Build" in onboarding


def test_pages_workflow_github_pages() -> None:
    text = PAGES.read_text(encoding="utf-8")
    assert "branches: [main]" in text or "branches:\n      - main" in text or "main" in text
    assert "upload-pages-artifact" in text
    assert "deploy-pages" in text
    assert "pages: write" in text
    assert "id-token: write" in text
    assert "custom domain" not in text.lower() or "No custom domain" in text
    assert "CNAME" not in text
