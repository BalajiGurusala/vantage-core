"""Shared field-level validation error helper for MCP tools.

Converts Pydantic ``ValidationError`` into a structured, human-readable
field-level error (FR-005 / SC-004) rather than letting raw exceptions escape.
"""

from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

ModelT = TypeVar("ModelT", bound=BaseModel)


class ToolValidationError(Exception):
    """Raised when tool input fails validation.

    Carries a ``fields`` mapping of ``field name -> message`` suitable for
    returning to an MCP client.
    """

    def __init__(self, fields: dict[str, str]) -> None:
        self.fields = fields
        super().__init__("Validation failed")

    def to_dict(self) -> dict[str, Any]:
        return {"error": "Validation failed", "fields": self.fields}


def validate_input(model: type[ModelT], arguments: dict[str, Any] | None) -> ModelT:
    """Validate ``arguments`` against ``model``.

    Returns the parsed model instance, or raises :class:`ToolValidationError`
    with per-field messages.
    """
    try:
        return model.model_validate(arguments or {})
    except ValidationError as exc:
        fields: dict[str, str] = {}
        for error in exc.errors():
            location = ".".join(str(part) for part in error["loc"]) or "(root)"
            fields[location] = error["msg"]
        raise ToolValidationError(fields) from exc
