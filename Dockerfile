# Canon optional HTTP MCP projection.
# Bakes the tagged commit's Northwind example law (AGENTS.md + law/ +
# decisions/) so find_repo_root() works without a bind-mount.
# Git remains the source of truth. Do not bake tokens.

FROM python:3.12-slim

RUN useradd --uid 1000 --create-home --home-dir /home/canon \
    --shell /usr/sbin/nologin canon

WORKDIR /app

# Install the projection at BUILD time. Never pip-install in CMD.
COPY mcp/pyproject.toml mcp/server.py mcp/README.md /app/mcp/
RUN pip install --no-cache-dir /app/mcp

COPY AGENTS.md LICENSE README.md /app/
COPY law /app/law
COPY decisions /app/decisions

RUN chown -R canon:canon /app

USER canon

EXPOSE 8787

# /health is behind BearerGate. Fail closed if CANON_MCP_TOKEN is unset.
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import os,sys,urllib.request; t=(os.environ.get('CANON_MCP_TOKEN') or '').strip(); sys.exit(1) if not t else None; r=urllib.request.Request('http://127.0.0.1:8787/health', headers={'Authorization':'Bearer '+t}); urllib.request.urlopen(r, timeout=4)"

CMD ["python", "mcp/server.py", "--host", "0.0.0.0", "--port", "8787"]
