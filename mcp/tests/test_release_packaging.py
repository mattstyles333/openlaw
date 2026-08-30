"""Shipped production packaging: Dockerfile + Portainer compose + GHCR workflow.

Reads the files in this git tree (not copies). Fail-closed token, GHCR pin
:0.1.0, no postgres/5432, no bind-mount, no pip-at-start, no baked secret.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
COMPOSE = ROOT / "docker-compose.yml"
DOCKERFILE = ROOT / "Dockerfile"
GHCR_WORKFLOW = ROOT / ".github" / "workflows" / "ghcr.yml"


def test_compose_is_ghcr_portainer_stack() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    assert "ghcr.io/mattstyles333/canon-mcp:0.1.0" in text
    assert "python:3.12-slim" not in text
    assert "pip install" not in text
    assert "- .:" not in text
    assert ".:/" not in text
    assert "5432" not in text
    assert "image: postgres" not in text
    assert not re.search(r"(?m)^  postgres:", text)
    assert "${CANON_MCP_TOKEN:?" in text
    assert "${CANON_MCP_TOKEN:-" not in text
    assert "restart: unless-stopped" in text
    assert "8787:8787" in text


def test_dockerfile_bakes_law_and_fail_closed_healthcheck() -> None:
    text = DOCKERFILE.read_text(encoding="utf-8")
    assert "pip install --no-cache-dir" in text
    after_cmd = text.split("\nCMD", 1)
    assert len(after_cmd) == 2
    assert "pip install" not in after_cmd[1]
    assert "EXPOSE 8787" in text
    assert "HEALTHCHECK" in text
    assert "urllib.request" in text
    assert "Authorization" in text
    assert "Bearer" in text
    assert "CANON_MCP_TOKEN" in text
    assert "--uid 1000" in text
    assert "useradd" in text
    assert "COPY AGENTS.md" in text
    assert "COPY law" in text
    assert "COPY decisions" in text
    assert not re.search(r"ENV\s+CANON_MCP_TOKEN\s*=", text)
    assert "COPY .git" not in text
    assert ".venv" not in text


def test_ghcr_workflow_publishes_stripped_semver() -> None:
    text = GHCR_WORKFLOW.read_text(encoding="utf-8")
    assert "v*" in text
    assert "packages: write" in text
    assert "ghcr.io" in text
    assert "github.actor" in text
    assert "secrets.GITHUB_TOKEN" in text
    assert "ghcr.io/mattstyles333/canon-mcp" in text
    assert "{{version}}" in text
    assert "CANON_MCP_TOKEN=" not in text
