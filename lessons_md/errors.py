"""Structured error types — same shape as research.md."""

from __future__ import annotations

from typing import Any


class LessonError(Exception):
    def __init__(self, message: str, code: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.details = details


class LessonValidationError(LessonError):
    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message, "VALIDATION_ERROR", details)


class LessonGateError(LessonError):
    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message, "GATE_ERROR", details)


class LessonNotFoundError(LessonError):
    def __init__(self, entity: str, id: str):
        super().__init__(
            f"{entity} '{id}' not found.", "NOT_FOUND", {"entity": entity, "id": id}
        )
