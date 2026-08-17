"""Razor-thin MCP server for lessons-md.

Exposes ONE tool: ``help``. Every other operation happens via the CLI
(``lessons-md lesson-create``, ``lessons-md project-list``, etc.). This is the
CLI-first / razor-thin-MCP shape — see ADR-006 in governor.md/.governor/adr/.

Discovery flow:
  1. Agent calls ``mcp__lessons-md__help()`` — gets the full command tree.
  2. Agent calls ``mcp__lessons-md__help(subcommand="lesson-create")`` —
     gets that subcommand's full --help output.
  3. Agent invokes the actual work via Bash:
     ``lessons-md lesson-create ... --json``.
"""

from __future__ import annotations

import asyncio
import io
import sys

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool


HELP_DESCRIPTION = (
    "REQUIRED at session start for any lessons-md work: returns the full "
    "lessons-md command tree. Call with no args for the top-level surface, "
    "or with subcommand='<name>' for that subcommand's full --help. All "
    "real work happens via Bash: `lessons-md <subcommand> [--json] [opts]`. "
    "Start every session with `lessons-md project-info` after project-set "
    "to orient. This MCP server is razor-thin by design."
)


HELP_TOOL = Tool(
    name="help",
    description=HELP_DESCRIPTION,
    inputSchema={
        "type": "object",
        "properties": {
            "subcommand": {
                "type": "string",
                "description": (
                    "Optional subcommand name (e.g. 'lesson-create', "
                    "'lesson-promote', 'project-set'). When set, returns "
                    "that subcommand's full --help. When omitted, returns "
                    "the top-level command tree."
                ),
            },
        },
    },
)


async def _on_list_tools(ctx, params) -> ListToolsResult:
    return ListToolsResult(tools=[HELP_TOOL])


def _capture_help(argv: list[str]) -> str:
    from .cli import app

    buf = io.StringIO()
    real_stdout = sys.stdout
    sys.stdout = buf
    try:
        try:
            app(argv, standalone_mode=False)
        except SystemExit:
            pass
        except Exception as e:
            return f"error rendering help: {type(e).__name__}: {e}"
    finally:
        sys.stdout = real_stdout
    return buf.getvalue()


def _build_top_level_help() -> str:
    return "\n".join(
        [
            "lessons-md — The learning forge. Durable lessons from execution.",
            "",
            "USAGE:  lessons-md <subcommand> [--json] [options]",
            "",
            "SESSION START:",
            "  lessons-md project-set <path>             # register, returns project_id",
            "  lessons-md project-info --project-id <id> # one-line orient",
            "",
            "PROJECTS:",
            "  lessons-md project-init <path>            # initialize a new project",
            "  lessons-md project-list                   # list registered projects",
            "",
            "LESSONS:",
            "  lessons-md lesson-create                  # new lesson (confidence CONFIRMED illegal)",
            "  lessons-md lesson-list                    # list (optionally include superseded)",
            "  lessons-md lesson-view <id>               # full lesson detail",
            "  lessons-md lesson-update <id>             # update fields / append body",
            "  lessons-md lesson-supersede <id>          # replace with a new lesson",
            "  lessons-md lesson-promote <id>            # link research_id and/or adr",
            "",
            "MCP:",
            "  lessons-md mcp serve                      # boots this MCP server (you're talking to it now)",
            "",
            "DRILL IN:    lessons-md <subcommand> --help    "
            "OR    mcp__lessons-md__help(subcommand='<name>')",
            "JSON MODE:   add --json to any subcommand for machine-readable output",
        ]
    )


async def _on_call_tool(ctx, params) -> CallToolResult:
    name = params.name
    arguments = params.arguments or {}
    if name != "help":
        text = f"unknown tool: {name!r}"
    else:
        sub = arguments.get("subcommand")
        if sub:
            text = _capture_help([sub, "--help"])
            if not text.strip():
                text = f"no help available for subcommand {sub!r}"
        else:
            text = _build_top_level_help()
    return CallToolResult(content=[TextContent(type="text", text=text)])


server = Server(
    "lessons-md",
    on_list_tools=_on_list_tools,
    on_call_tool=_on_call_tool,
)


async def _main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


def run() -> None:
    """Entry point used by ``lessons-md mcp serve``."""
    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        sys.exit(0)
