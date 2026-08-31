"""Openlaw MCP — thin HTTP projection of git. Not the source of truth.

Git markdown (law/, decisions/) is canonical. Skills tools wrap
`scripts/openlaw` (law, priorities, permissions, check, decisions, propose)
and return that CLI's stdout. This process does not search, embed, or
replace AGENTS.md.

Auth (fail closed):
  - OPENLAW_MCP_TOKEN is required at startup; refuse to listen if unset.
    CANON_MCP_TOKEN is a deprecated alias so existing Portainer stacks keep working.
  - Every HTTP request needs Authorization: Bearer <token>.
  - Missing or wrong bearer → HTTP 401. There is no anonymous mode.
  - Owner tools (commit_decision, set_priorities) also require
    OPENLAW_COMMIT_TOKEN (X-Openlaw-Commit-Token header, or the same value as
    the Authorization bearer). CANON_COMMIT_TOKEN is a deprecated alias.

v0.1 persists to the law/ and decisions/ filesystem only.
Optional OPENLAW_POSTGRES_URL is documented in README.md, off by default,
and not implemented here. This projection is not a generic database MCP
and has no SQL tool.
"""

from __future__ import annotations

import argparse
import hmac
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.routing import Route

PROTOCOL_VERSION = "2025-03-26"
SERVER_NAME = "openlaw"
SERVER_VERSION = "0.2.0"


# ---------------------------------------------------------------------------
# Repo root: walk up from cwd looking for AGENTS.md + law/
# ---------------------------------------------------------------------------

def find_repo_root(start: Path | None = None) -> Path:
    """Walk up from cwd (then this file) until AGENTS.md and law/ exist."""
    starts = []
    starts.append((start or Path.cwd()).resolve())
    starts.append(Path(__file__).resolve().parent)
    seen: set[Path] = set()
    for origin in starts:
        if origin in seen:
            continue
        seen.add(origin)
        for candidate in [origin, *origin.parents]:
            if (candidate / "AGENTS.md").is_file() and (candidate / "law").is_dir():
                return candidate
    raise FileNotFoundError(
        "cannot find Openlaw repo root (need AGENTS.md + law/)"
    )


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Auth — fail closed. Bearer required. 401 if missing.
# ---------------------------------------------------------------------------

def mcp_token() -> str:
    # Prefer OPENLAW_MCP_TOKEN. CANON_MCP_TOKEN is a deprecated alias.
    # Whitespace-only is unset. Fail closed: no default token.
    primary = (os.environ.get("OPENLAW_MCP_TOKEN") or "").strip()
    if primary:
        return primary
    return (os.environ.get("CANON_MCP_TOKEN") or "").strip()


def commit_token() -> str:
    primary = (os.environ.get("OPENLAW_COMMIT_TOKEN") or "").strip()
    if primary:
        return primary
    return (os.environ.get("CANON_COMMIT_TOKEN") or "").strip()


def _bearer_from_request(request: Request) -> str:
    auth = request.headers.get("authorization") or ""
    if not auth.lower().startswith("bearer "):
        return ""
    return auth[7:].strip()


def unauthorized() -> JSONResponse:
    return JSONResponse(
        {"error": "unauthorized"},
        status_code=401,
        headers={"WWW-Authenticate": "Bearer"},
    )


class BearerGate:
    """ASGI middleware: fail closed; HTTP 401 without a valid bearer."""

    def __init__(self, app: Callable) -> None:
        self.app = app

    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        expected = mcp_token()
        if not expected:
            body = json.dumps(
                {
                    "error": "fail closed: OPENLAW_MCP_TOKEN is unset; refuse to listen"
                }
            ).encode()
            await send(
                {
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [
                        (b"content-type", b"application/json"),
                        (b"content-length", str(len(body)).encode()),
                        (b"www-authenticate", b"Bearer"),
                    ],
                }
            )
            await send({"type": "http.response.body", "body": body})
            return
        headers = {
            k.decode("latin-1").lower(): v.decode("latin-1")
            for k, v in scope.get("headers") or []
        }
        auth = headers.get("authorization", "")
        provided = ""
        if auth.lower().startswith("bearer "):
            provided = auth[7:].strip()
        if not provided or not hmac.compare_digest(provided, expected):
            body = json.dumps({"error": "unauthorized"}).encode()
            await send(
                {
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [
                        (b"content-type", b"application/json"),
                        (b"content-length", str(len(body)).encode()),
                        (b"www-authenticate", b"Bearer"),
                    ],
                }
            )
            await send({"type": "http.response.body", "body": body})
            return
        await self.app(scope, receive, send)


def require_owner(request: Request) -> None:
    """Owner tools fail closed unless OPENLAW_COMMIT_TOKEN (or alias) matches."""
    expected = commit_token()
    if not expected:
        raise PermissionError(
            "owner tools fail closed: OPENLAW_COMMIT_TOKEN is unset"
        )
    header = (
        request.headers.get("x-openlaw-commit-token")
        or request.headers.get("x-canon-commit-token")
        or ""
    ).strip()
    bearer = _bearer_from_request(request)
    if header and hmac.compare_digest(header, expected):
        return
    if bearer and hmac.compare_digest(bearer, expected):
        return
    raise PermissionError(
        "owner tools require OPENLAW_COMMIT_TOKEN "
        "(X-Openlaw-Commit-Token header, or Authorization bearer matching it)"
    )


# ---------------------------------------------------------------------------
# Skills CLI wrap: bash scripts/openlaw <command> from the repo root.
# ---------------------------------------------------------------------------

def run_openlaw(*cli_args: str) -> str:
    """Invoke the shipped skills CLI. Return stdout. Do not reimplement it."""
    root = find_repo_root()
    cli = root / "scripts" / "openlaw"
    proc = subprocess.run(
        ["bash", str(cli), *cli_args],
        cwd=str(root),
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        err = (proc.stderr or "").strip()
        out = (proc.stdout or "").strip()
        raise RuntimeError(
            err or out or f"scripts/openlaw {' '.join(cli_args)} failed ({proc.returncode})"
        )
    return proc.stdout


def tool_get_law(_args: dict[str, Any], _request: Request) -> str:
    """Full current constraints+brand+sor concatenated. NOT search."""
    return run_openlaw("law")


def tool_get_priorities(_args: dict[str, Any], _request: Request) -> str:
    return run_openlaw("priorities")


def tool_permissions(_args: dict[str, Any], _request: Request) -> str:
    return run_openlaw("permissions")


def tool_check(_args: dict[str, Any], _request: Request) -> str:
    return run_openlaw("check")


def tool_decisions(_args: dict[str, Any], _request: Request) -> str:
    return run_openlaw("decisions")


def tool_propose(args: dict[str, Any], _request: Request) -> str:
    slug = str(args.get("slug") or "").strip()
    if slug:
        return run_openlaw("propose", slug)
    return run_openlaw("propose")


def tool_search_decisions(args: dict[str, Any], _request: Request) -> str:
    keyword = str(args.get("keyword") or args.get("query") or "").strip()
    if not keyword:
        raise ValueError("search_decisions requires 'keyword'")
    root = find_repo_root()
    needle = keyword.lower()
    hits: list[str] = []
    for path in sorted((root / "decisions").glob("*.md")):
        text = _read(path)
        if needle in text.lower() or needle in path.name.lower():
            excerpt = next(
                (ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("---")),
                path.name,
            )
            hits.append(f"- {path.name}: {excerpt}")
    if not hits:
        return f"No decisions matched {keyword!r}."
    return "\n".join(hits)


def _decision_path(filename: str) -> Path:
    name = Path(str(filename)).name
    if not name or name != Path(str(filename).replace("\\", "/")).name:
        raise ValueError("get_decision: filename must be a basename, not a path")
    if not re.fullmatch(r"[A-Za-z0-9._-]+\.md", name):
        raise ValueError("get_decision: invalid filename")
    root = find_repo_root()
    decisions = (root / "decisions").resolve()
    path = (decisions / name).resolve()
    if path.parent != decisions:
        raise ValueError("get_decision: filename escapes decisions/")
    return path


def tool_get_decision(args: dict[str, Any], _request: Request) -> str:
    filename = str(args.get("filename") or args.get("name") or "").strip()
    if not filename:
        raise ValueError("get_decision requires 'filename'")
    path = _decision_path(filename)
    if not path.is_file():
        raise FileNotFoundError(f"decision not found: {path.name}")
    return _read(path)


def tool_commit_decision(args: dict[str, Any], request: Request) -> str:
    require_owner(request)
    filename = str(args.get("filename") or "").strip()
    if not filename:
        raise ValueError("commit_decision requires 'filename'")
    path = _decision_path(filename)
    if not path.is_file():
        raise FileNotFoundError(f"decision not found: {path.name}")
    text = _read(path)
    new, n = re.subn(
        r"^status:\s*(proposed|decided|superseded)\s*$",
        "status: decided",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n == 0:
        raise ValueError(f"{path.name} has no status: frontmatter to set decided")
    _write(path, new)
    return f"{path.name} status: decided. Owners still merge via git / CODEOWNERS."


def tool_set_priorities(args: dict[str, Any], request: Request) -> str:
    require_owner(request)
    content = args.get("content")
    if content is None:
        content = args.get("markdown")
    if content is None:
        raise ValueError("set_priorities requires 'content'")
    text = str(content)
    if not text.strip():
        raise ValueError("set_priorities: content is empty")
    if not text.endswith("\n"):
        text += "\n"
    root = find_repo_root()
    path = root / "law" / "priorities.md"
    _write(path, text)
    return "rewrote law/priorities.md. Git is still the source of truth."


_LAW_SCHEMA = {"type": "object", "properties": {}, "additionalProperties": False}
_PROPOSE_SCHEMA = {
    "type": "object",
    "properties": {"slug": {"type": "string"}},
}

TOOLS: dict[str, tuple[str, dict[str, Any], Callable[[dict[str, Any], Request], str]]] = {
    "law": (
        "Wrap scripts/openlaw law: full constraints+brand+sor. NOT search.",
        _LAW_SCHEMA,
        tool_get_law,
    ),
    "get_law": (
        "Alias of law. Wrap scripts/openlaw law. NOT search.",
        _LAW_SCHEMA,
        tool_get_law,
    ),
    "priorities": (
        "Wrap scripts/openlaw priorities: print law/priorities.md.",
        _LAW_SCHEMA,
        tool_get_priorities,
    ),
    "get_priorities": (
        "Alias of priorities. Wrap scripts/openlaw priorities.",
        _LAW_SCHEMA,
        tool_get_priorities,
    ),
    "permissions": (
        "Wrap scripts/openlaw permissions: print law/permissions.md.",
        _LAW_SCHEMA,
        tool_permissions,
    ),
    "check": (
        "Wrap scripts/openlaw check: run scripts/check-law.sh.",
        _LAW_SCHEMA,
        tool_check,
    ),
    "decisions": (
        "Wrap scripts/openlaw decisions: print decisions/20*.md (not binding).",
        _LAW_SCHEMA,
        tool_decisions,
    ),
    "propose": (
        "Wrap scripts/openlaw propose: copy decisions/_template.md. Does not write law/.",
        _PROPOSE_SCHEMA,
        tool_propose,
    ),
    "propose_decision": (
        "Alias of propose. Wrap scripts/openlaw propose. Does not edit law/.",
        _PROPOSE_SCHEMA,
        tool_propose,
    ),
    "search_decisions": (
        "Keyword search over decisions/*.md (substring, case-insensitive).",
        {
            "type": "object",
            "properties": {"keyword": {"type": "string"}},
            "required": ["keyword"],
        },
        tool_search_decisions,
    ),
    "get_decision": (
        "Return one ADR by filename (basename under decisions/).",
        {
            "type": "object",
            "properties": {"filename": {"type": "string"}},
            "required": ["filename"],
        },
        tool_get_decision,
    ),
    "commit_decision": (
        "Owner-only. Requires CANON_COMMIT_TOKEN. Sets an ADR status to decided.",
        {
            "type": "object",
            "properties": {"filename": {"type": "string"}},
            "required": ["filename"],
        },
        tool_commit_decision,
    ),
    "set_priorities": (
        "Owner-only. Requires CANON_COMMIT_TOKEN. Rewrites law/priorities.md.",
        {
            "type": "object",
            "properties": {"content": {"type": "string"}},
            "required": ["content"],
        },
        tool_set_priorities,
    ),
}


def dispatch(name: str, args: dict[str, Any], request: Request) -> str:
    spec = TOOLS.get(name)
    if spec is None:
        raise KeyError(name)
    return spec[2](args, request)


# ---------------------------------------------------------------------------
# HTTP + JSON-RPC MCP
# ---------------------------------------------------------------------------

def _tools_list() -> list[dict[str, Any]]:
    return [
        {"name": name, "description": desc, "inputSchema": schema}
        for name, (desc, schema, _) in TOOLS.items()
    ]


def _tool_call_payload(name: str, args: dict[str, Any], request: Request) -> dict[str, Any]:
    try:
        text = dispatch(name, args, request)
        return {"content": [{"type": "text", "text": text}], "isError": False}
    except PermissionError as exc:
        return {"content": [{"type": "text", "text": str(exc)}], "isError": True}
    except (KeyError, ValueError, FileNotFoundError, OSError, RuntimeError) as exc:
        return {"content": [{"type": "text", "text": str(exc)}], "isError": True}


def _jsonrpc_result(id_: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": id_, "result": result}


def _jsonrpc_error(id_: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}


async def handle_mcp(request: Request) -> Response:
    """JSON-RPC 2.0 MCP over HTTP (streamable-http style JSON)."""
    if request.method == "GET":
        return JSONResponse(
            {
                "name": SERVER_NAME,
                "version": SERVER_VERSION,
                "transport": "http",
                "note": "POST JSON-RPC to this path. Git is the source of truth.",
            }
        )
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse(
            _jsonrpc_error(None, -32700, "Parse error"),
            status_code=400,
        )
    if not isinstance(payload, dict):
        return JSONResponse(_jsonrpc_error(None, -32600, "Invalid Request"), status_code=400)

    method = str(payload.get("method") or "")
    id_ = payload.get("id")
    params = payload.get("params") if isinstance(payload.get("params"), dict) else {}

    if method in ("notifications/initialized", "initialized") and id_ is None:
        return Response(status_code=204)

    if method == "initialize":
        body = _jsonrpc_result(
            id_,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                "instructions": (
                    "Openlaw MCP is a projection of git. Git is the source of truth. "
                    "get_law returns full current files, not a search ranking."
                ),
            },
        )
    elif method in ("tools/list", "list_tools"):
        body = _jsonrpc_result(id_, {"tools": _tools_list()})
    elif method in ("tools/call", "call_tool"):
        name = str(params.get("name") or "")
        args = params.get("arguments") if isinstance(params.get("arguments"), dict) else {}
        if not name:
            body = _jsonrpc_error(id_, -32602, "tools/call requires params.name")
        else:
            body = _jsonrpc_result(id_, _tool_call_payload(name, args, request))
    elif method in ("ping", "notifications/ping"):
        body = _jsonrpc_result(id_, {})
    else:
        body = _jsonrpc_error(id_, -32601, f"Method not found: {method}")

    accept = (request.headers.get("accept") or "").lower()
    if "text/event-stream" in accept and "application/json" not in accept:
        data = json.dumps(body)
        return Response(
            f"event: message\ndata: {data}\n\n",
            media_type="text/event-stream",
        )
    return JSONResponse(body)


async def handle_tool_http(request: Request) -> Response:
    name = request.path_params["name"]
    args: dict[str, Any] = {}
    if request.method == "POST":
        try:
            body = await request.json()
            if isinstance(body, dict):
                args = body
        except Exception:
            args = {}
    try:
        text = dispatch(name, args, request)
    except KeyError:
        return JSONResponse({"error": f"unknown tool: {name}"}, status_code=404)
    except PermissionError as exc:
        return JSONResponse({"error": str(exc)}, status_code=403)
    except FileNotFoundError as exc:
        return JSONResponse({"error": str(exc)}, status_code=404)
    except ValueError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    except RuntimeError as exc:
        return PlainTextResponse(str(exc), status_code=400)
    return PlainTextResponse(text)


async def handle_health(request: Request) -> Response:
    # Bearer already enforced. No public unauthenticated probe.
    return JSONResponse(
        {
            "ok": True,
            "name": SERVER_NAME,
            "root": str(find_repo_root()),
            "source_of_truth": "git",
        }
    )


def create_app() -> Starlette:
    """Build the HTTP app. Fail closed if OPENLAW_MCP_TOKEN is unset."""
    token = mcp_token()
    if not token:
        raise SystemExit(
            "fail closed: OPENLAW_MCP_TOKEN is unset; refuse to listen"
        )
    starlette_app = Starlette(
        routes=[
            Route("/", handle_mcp, methods=["GET", "POST"]),
            Route("/mcp", handle_mcp, methods=["GET", "POST"]),
            Route("/health", handle_health, methods=["GET"]),
            Route("/tools/{name}", handle_tool_http, methods=["GET", "POST"]),
        ]
    )
    return BearerGate(starlette_app)  # type: ignore[return-value]


def main() -> None:
    if not mcp_token():
        print(
            "fail closed: OPENLAW_MCP_TOKEN is unset; refuse to listen",
            file=sys.stderr,
        )
        sys.exit(1)
    parser = argparse.ArgumentParser(
        description="Openlaw MCP HTTP projection. Git is the source of truth."
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("OPENLAW_MCP_HOST")
        or os.environ.get("CANON_MCP_HOST")
        or "0.0.0.0",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(
            os.environ.get("OPENLAW_MCP_PORT")
            or os.environ.get("CANON_MCP_PORT")
            or "8787"
        ),
    )
    args = parser.parse_args()
    uvicorn.run(create_app(), host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
