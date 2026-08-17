"""Lesson subcommands."""

from __future__ import annotations

from typing import Annotated, Optional

import typer

from .._logic import lesson as _lesson
from ._helpers import parse_str_list


def register(app: typer.Typer) -> None:
    @app.command("lesson-create")
    def cmd_lesson_create(
        project_id: Annotated[str, typer.Option(help="Project GUID.")],
        title: Annotated[str, typer.Option(help="Lesson title.")],
        claim: Annotated[
            str, typer.Option(help="One sentence another agent can act on.")
        ],
        content: Annotated[str, typer.Option(help="Lesson body.")] = "",
        confidence: Annotated[
            str,
            typer.Option(help="UNVERIFIED | LOW | REASONED | CONFIRMED."),
        ] = "LOW",
        concerns: Annotated[
            Optional[str],
            typer.Option("--concerns", help="JSON array of concerns."),
        ] = None,
        origin_task: Annotated[
            Optional[str], typer.Option(help="Originating task id.")
        ] = None,
        applies_when: Annotated[
            Optional[str],
            typer.Option(
                help="Situation trigger: when should the next agent apply this?"
            ),
        ] = None,
        json_: Annotated[
            bool, typer.Option("--json", "-J", help="JSON output.")
        ] = False,
    ) -> None:
        """Create a lesson."""
        from ._app import emit

        result = _lesson.lesson_create(
            project_id=project_id,
            title=title,
            claim=claim,
            content=content,
            confidence=confidence,
            concerns=parse_str_list(concerns, "--concerns"),
            origin_task=origin_task,
            applies_when=applies_when,
        )
        emit(result, json_mode=json_)

    @app.command("lesson-list")
    def cmd_lesson_list(
        project_id: Annotated[str, typer.Option(help="Project GUID.")],
        include_superseded: Annotated[
            bool,
            typer.Option("--include-superseded", help="Include superseded lessons."),
        ] = False,
        json_: Annotated[
            bool, typer.Option("--json", "-J", help="JSON output.")
        ] = False,
    ) -> None:
        """List lessons."""
        from ._app import emit

        result = _lesson.lesson_list(
            project_id=project_id,
            include_superseded=include_superseded,
        )
        emit(result, json_mode=json_)

    @app.command("relevant")
    def cmd_relevant(
        project_id: Annotated[str, typer.Option(help="Project GUID.")],
        query: Annotated[
            Optional[str],
            typer.Argument(help="Optional tokens to match title, claim, applies-when."),
        ] = None,
        json_: Annotated[
            bool, typer.Option("--json", "-J", help="JSON output.")
        ] = False,
    ) -> None:
        """Hand the caller the open lessons they should read before acting."""
        from ._app import emit

        result = _lesson.lesson_relevant(project_id=project_id, query=query)
        emit(result, json_mode=json_)

    @app.command("lesson-view")
    def cmd_lesson_view(
        project_id: Annotated[str, typer.Option(help="Project GUID.")],
        lesson_id: Annotated[str, typer.Argument(help="Lesson ID.")],
        json_: Annotated[
            bool, typer.Option("--json", "-J", help="JSON output.")
        ] = False,
    ) -> None:
        """View a lesson's full frontmatter and body."""
        from ._app import emit

        result = _lesson.lesson_view(project_id=project_id, lesson_id=lesson_id)
        emit(result, json_mode=json_)

    @app.command("lesson-update")
    def cmd_lesson_update(
        project_id: Annotated[str, typer.Option(help="Project GUID.")],
        lesson_id: Annotated[str, typer.Argument(help="Lesson ID.")],
        title: Annotated[Optional[str], typer.Option(help="New title.")] = None,
        claim: Annotated[Optional[str], typer.Option(help="New claim.")] = None,
        content: Annotated[Optional[str], typer.Option(help="Replace content.")] = None,
        append_content: Annotated[
            Optional[str], typer.Option(help="Append to content.")
        ] = None,
        confidence: Annotated[
            Optional[str],
            typer.Option(help="UNVERIFIED | LOW | REASONED | CONFIRMED."),
        ] = None,
        concerns: Annotated[
            Optional[str],
            typer.Option("--concerns", help="JSON array of concerns."),
        ] = None,
        status: Annotated[Optional[str], typer.Option(help="New status.")] = None,
        applies_when: Annotated[
            Optional[str],
            typer.Option(help="Situation trigger: when to apply this lesson."),
        ] = None,
        json_: Annotated[
            bool, typer.Option("--json", "-J", help="JSON output.")
        ] = False,
    ) -> None:
        """Update a lesson."""
        from ._app import emit

        result = _lesson.lesson_update(
            project_id=project_id,
            lesson_id=lesson_id,
            title=title,
            claim=claim,
            content=content,
            append_content=append_content,
            confidence=confidence,
            concerns=parse_str_list(concerns, "--concerns"),
            status=status,
            applies_when=applies_when,
        )
        emit(result, json_mode=json_)

    @app.command("lesson-supersede")
    def cmd_lesson_supersede(
        project_id: Annotated[str, typer.Option(help="Project GUID.")],
        old_id: Annotated[str, typer.Argument(help="Lesson ID to supersede.")],
        title: Annotated[str, typer.Option(help="Title for the replacement lesson.")],
        claim: Annotated[
            str, typer.Option(help="One sentence another agent can act on.")
        ],
        content: Annotated[str, typer.Option(help="Replacement lesson body.")] = "",
        confidence: Annotated[
            str,
            typer.Option(help="UNVERIFIED | LOW | REASONED | CONFIRMED."),
        ] = "LOW",
        json_: Annotated[
            bool, typer.Option("--json", "-J", help="JSON output.")
        ] = False,
    ) -> None:
        """Supersede a lesson with a new one."""
        from ._app import emit

        result = _lesson.lesson_supersede(
            project_id=project_id,
            old_id=old_id,
            new_title=title,
            claim=claim,
            content=content,
            confidence=confidence,
        )
        emit(result, json_mode=json_)

    @app.command("lesson-promote")
    def cmd_lesson_promote(
        project_id: Annotated[str, typer.Option(help="Project GUID.")],
        lesson_id: Annotated[str, typer.Argument(help="Lesson ID.")],
        research_id: Annotated[
            Optional[str],
            typer.Option(
                help="research-md project GUID or 0001-style finding id. "
                "Omit to create a finding in the nearest .research/."
            ),
        ] = None,
        adr: Annotated[Optional[str], typer.Option(help="ADR identifier.")] = None,
        use_research: Annotated[
            bool,
            typer.Option(
                "--research/--no-research",
                help="Shell out to research-md (default on).",
            ),
        ] = True,
        research_path: Annotated[
            Optional[str],
            typer.Option(help="Path to a research-md project (contains .research/)."),
        ] = None,
        json_: Annotated[
            bool, typer.Option("--json", "-J", help="JSON output.")
        ] = False,
    ) -> None:
        """Promote a lesson by creating or verifying a research-md finding."""
        from ._app import emit

        result = _lesson.lesson_promote(
            project_id=project_id,
            lesson_id=lesson_id,
            research_id=research_id,
            adr=adr,
            use_research=use_research,
            research_path=research_path,
        )
        emit(result, json_mode=json_)
