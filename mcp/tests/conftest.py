"""Smoke-test fixtures. Tokens are fake local values, never real secrets."""

from __future__ import annotations

import os
import sys
from pathlib import Path

MCP_DIR = Path(__file__).resolve().parent.parent
if str(MCP_DIR) not in sys.path:
    sys.path.insert(0, str(MCP_DIR))

# Fail-closed server refuses to listen without LAW_MCP_TOKEN.
os.environ.setdefault("LAW_MCP_TOKEN", "test-law-mcp-token")
os.environ.setdefault("LAW_COMMIT_TOKEN", "test-law-commit-token")
