"""MCP smoke tests: bearer get_law sees hard rules; missing bearer is HTTP 401.

No live Postgres. Tokens are local fixtures, not secrets.
"""

from __future__ import annotations

import os

from starlette.testclient import TestClient

from server import create_app

TOKEN = os.environ["CANON_MCP_TOKEN"]


def test_get_law_with_bearer_includes_hard_rule() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/tools/get_law",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    assert response.status_code == 200, response.text
    body = response.text
    assert (
        "MUST never invent company policy" in body or "always-on" in body
    ), body[:500]


def test_without_bearer_http_401() -> None:
    client = TestClient(create_app())
    response = client.get("/tools/get_law")
    assert response.status_code == 401, response.text
    rpc = client.post(
        "/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "get_law", "arguments": {}},
        },
    )
    assert rpc.status_code == 401, rpc.text
