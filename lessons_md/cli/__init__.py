"""lessons-md Typer CLI surface.

``lessons-md <subcommand> [--json] [opts]`` — everything is here. The MCP
server (``lessons_md.mcp_server``) will expose a single ``help`` tool that
introspects this Typer app. mcp_server.py and cli/mcp.py land later.
"""

from ._app import app, main

__all__ = ["app", "main"]
