"""lessons-md Typer CLI surface.

``lessons-md <subcommand> [--json] [opts]`` — everything is here. The MCP
server exposes a single ``help`` tool that introspects this Typer app.
"""

from ._app import app, main

__all__ = ["app", "main"]
