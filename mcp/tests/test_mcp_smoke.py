"""MCP smoke tests driving the shipped projection (mcp/server.py).

- With bearer, get_law includes a Northwind example rule.
- Without bearer, or with a wrong bearer, HTTP 401.
- Missing / blank CANON_MCP_TOKEN: create_app and main refuse to listen.
- Shipped server.py has no SQL execution tool and no unauthenticated default.
No live Postgres. Fixture tokens are local, not secrets.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from starlette.testclient import TestClient

import server

TOKEN = os.environ["CANON_MCP_TOKEN"]
SERVER_PY = Path(__file__).resolve().parent.parent / "server.py"
COMPOSE = Path(__file__).resolve().parent.parent.parent / "docker-compose.yml"


def test_get_law_with_bearer_includes_northwind_rule() -> None:
    client = TestClient(server.create_app())
    response = client.get(
        "/tools/get_law",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    assert response.status_code == 200, response.text
    body = response.text
    assert "Northwind" in body, body[:800]
    assert "MUST never invent company policy" in body, body[:800]
    assert "always-on" in body, body[:800]


def test_without_bearer_http_401() -> None:
    client = TestClient(server.create_app())
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


def test_wrong_bearer_http_401() -> None:
    client = TestClient(server.create_app())
    response = client.get(
        "/tools/get_law",
        headers={"Authorization": "Bearer definitely-not-the-token"},
    )
    assert response.status_code == 401, response.text


def test_create_app_refuses_to_listen_if_token_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CANON_MCP_TOKEN", raising=False)
    with pytest.raises(SystemExit) as excinfo:
        server.create_app()
    msg = str(excinfo.value)
    assert "fail closed" in msg
    assert "CANON_MCP_TOKEN" in msg
    assert "refuse to listen" in msg


def test_create_app_refuses_to_listen_if_token_blank(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CANON_MCP_TOKEN", "   ")
    with pytest.raises(SystemExit) as excinfo:
        server.create_app()
    assert "fail closed" in str(excinfo.value)


def test_main_refuses_to_listen_if_token_missing(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("CANON_MCP_TOKEN", raising=False)
    with pytest.raises(SystemExit) as excinfo:
        server.main()
    assert excinfo.value.code == 1
    err = capsys.readouterr().err
    assert "fail closed" in err
    assert "CANON_MCP_TOKEN" in err


def test_shipped_server_has_no_sql_tool_or_auth_bypass() -> None:
    text = SERVER_PY.read_text(encoding="utf-8")
    forbidden_sql = "execute" + "_sql"
    assert forbidden_sql not in text
    assert "AUTH_DISABLED" not in text
    assert "allow_anonymous" not in text
    compose = COMPOSE.read_text(encoding="utf-8")
    assert "CANON_MCP_TOKEN: ${CANON_MCP_TOKEN}" in compose
    assert "${CANON_MCP_TOKEN:-" not in compose
