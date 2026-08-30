"""Smoke-test fixtures. Tokens are fake local values, never real secrets."""

from __future__ import annotations

import os
import sys
from pathlib import Path

MCP_DIR = Path(__file__).resolve().parent.parent
if str(MCP_DIR) not in sys.path:
    sys.path.insert(0, str(MCP_DIR))

# Fail-closed server refuses to listen without OPENLAW_MCP_TOKEN
# (CANON_MCP_TOKEN is a deprecated alias).
os.environ.setdefault("OPENLAW_MCP_TOKEN", "test-openlaw-mcp-token")
os.environ.setdefault("OPENLAW_COMMIT_TOKEN", "test-openlaw-commit-token")
