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


_handed_lessons = False


@app.callback()
def _root_callback() -> None:
    """Register the CWD project and hand active lessons on the first command.

    LOOK-0001 F-0001: boot used to register silently. Retrieval has to happen
    without the agent remembering project-set.
    """
    global _handed_lessons
    from .._logic._session import boot_from_cwd
    from .._logic.lesson import lesson_relevant

    project_id = boot_from_cwd()
    if not project_id or _handed_lessons:
        return
    _handed_lessons = True
    typer.echo(lesson_relevant(project_id), err=True)


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
        from ..errors import LessonError

        if isinstance(e, LessonError):
            typer.echo(f"error: {e}", err=True)
        else:
            typer.echo(f"error: {type(e).__name__}: {e}", err=True)
        sys.exit(1)
