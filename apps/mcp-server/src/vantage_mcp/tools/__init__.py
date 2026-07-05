"""MCP tool registry.

Builds the ordered set of tools the server exposes, wiring each tool's input
validation and handler. Handlers accept raw MCP arguments and return a
JSON-serializable ``dict`` (or raise
:class:`~vantage_mcp.tools.validation.ToolValidationError`).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable

from vantage_mcp.bridge.interface import EdgeBridge
from vantage_mcp.tools.dwarf import DwarfResolveRequest, resolve_dwarf_symbol
from vantage_mcp.tools.health import build_health_status
from vantage_mcp.tools.inject import InjectProbeRequest, inject_probe
from vantage_mcp.tools.validation import validate_input

ToolHandler = Callable[[dict[str, Any] | None], dict[str, Any]]

_EMPTY_INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {},
    "additionalProperties": False,
}


@dataclass(frozen=True)
class RegisteredTool:
    """A single registered MCP tool."""

    name: str
    description: str
    kind: str  # "functional" | "placeholder"
    input_schema: dict[str, Any]
    handler: ToolHandler


class ToolRegistry:
    """Ordered collection of registered tools with name-based lookup."""

    def __init__(self, tools: list[RegisteredTool]) -> None:
        self._tools = tools
        self._by_name = {tool.name: tool for tool in tools}

    def all_tools(self) -> list[RegisteredTool]:
        return list(self._tools)

    def names(self) -> list[str]:
        return [tool.name for tool in self._tools]

    def get(self, name: str) -> RegisteredTool | None:
        return self._by_name.get(name)


def build_registry(
    version: str,
    started_at: datetime,
    bridge: EdgeBridge,
) -> ToolRegistry:
    """Construct the tool registry with all runtime dependencies wired in."""
    tool_names = ["vantage_health", "resolve_dwarf_symbol", "inject_probe"]

    def health_handler(_arguments: dict[str, Any] | None) -> dict[str, Any]:
        status = build_health_status(version, started_at, tool_names)
        return status.model_dump(mode="json")

    def dwarf_handler(arguments: dict[str, Any] | None) -> dict[str, Any]:
        request = validate_input(DwarfResolveRequest, arguments)
        return resolve_dwarf_symbol(request).model_dump(mode="json")

    def inject_handler(arguments: dict[str, Any] | None) -> dict[str, Any]:
        request = validate_input(InjectProbeRequest, arguments)
        return inject_probe(request, bridge).model_dump(mode="json")

    tools = [
        RegisteredTool(
            name="vantage_health",
            description=(
                "Return operational status of the Vantage MCP server: version, "
                "uptime, and registered tool names."
            ),
            kind="functional",
            input_schema=dict(_EMPTY_INPUT_SCHEMA),
            handler=health_handler,
        ),
        RegisteredTool(
            name="resolve_dwarf_symbol",
            description=(
                "Resolve a symbol name to a memory offset in a binary via DWARF "
                "debug info. Placeholder: returns an informative stub."
            ),
            kind="placeholder",
            input_schema=DwarfResolveRequest.model_json_schema(),
            handler=dwarf_handler,
        ),
        RegisteredTool(
            name="inject_probe",
            description=(
                "Command the edge daemon to attach an eBPF probe at a hex offset. "
                "Placeholder: uses the mock bridge to simulate the edge flow."
            ),
            kind="placeholder",
            input_schema=InjectProbeRequest.model_json_schema(),
            handler=inject_handler,
        ),
    ]
    return ToolRegistry(tools)
