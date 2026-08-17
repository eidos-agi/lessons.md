"""Typer root + shared output formatter for lessons-md."""

from __future__ import annotations

import json as _json

import typer

app = typer.Typer(
    name="lessons-md",
    help="lessons.md — the learning forge. Durable lessons from execution.",
    no_args_is_help=True,
    add_completion=False,
    pretty_exceptions_enable=False,
)


@app.callback()
def _root_callback() -> None:
    """Auto-register any lessons.md project rooted at or above CWD before each command."""
    from .._logic._session import boot_from_cwd

    boot_from_cwd()


def emit(result, *, json_mode: bool) -> None:
    """Print a result. JSON mode dumps; otherwise the original string is preserved."""
    if json_mode:
        typer.echo(_json.dumps(result, indent=2, default=str))
        return
    if isinstance(result, str):
        typer.echo(result)
    elif isinstance(result, (dict, list)):
        typer.echo(_json.dumps(result, indent=2, default=str))
    else:
        typer.echo(str(result))


def _wire() -> None:
    from . import lesson as _lesson_cmd
    from . import mcp as _mcp_cmd
    from . import project as _project_cmd

    _project_cmd.register(app)
    _lesson_cmd.register(app)
    app.add_typer(_mcp_cmd.app, name="mcp", help="MCP server operations.")


_wire()


def main() -> None:
    """Console-script entry point (``lessons-md``)."""
    import sys

    try:
        app()
    except KeyboardInterrupt:
        sys.exit(130)
    except (typer.Exit, typer.Abort, SystemExit):
        raise
    except Exception as e:
        typer.echo(f"error: {type(e).__name__}: {e}", err=True)
        sys.exit(1)
