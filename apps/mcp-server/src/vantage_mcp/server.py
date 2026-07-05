"""Vantage MCP server: stdio entry point and tool dispatch.

Builds a Model Context Protocol server over stdio (FR-001), registers the
Vantage tools (FR-002/FR-003), and dispatches calls to the tool registry.
Input validation is handled inside each tool so that invalid input yields a
structured field-level error (FR-005 / SC-004) rather than a protocol error.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any

import anyio
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

from vantage_mcp import __version__
from vantage_mcp.bridge.interface import EdgeBridge
from vantage_mcp.bridge.mock_client import MockEdgeBridge
from vantage_mcp.tools import ToolRegistry, build_registry
from vantage_mcp.tools.validation import ToolValidationError

SERVER_NAME = "vantage"


class StartupError(Exception):
    """Raised when the server cannot start; message includes remediation."""


def _select_bridge() -> EdgeBridge:
    """Select the edge bridge implementation.

    Scaffold always uses the in-process mock. ``VANTAGE_EDGE_WS_URL`` is read
    but ignored (reserved for the future live-bridge feature); a note is emitted
    to stderr so the operator is not surprised.
    """
    live_url = os.environ.get("VANTAGE_EDGE_WS_URL")
    if live_url:
        print(
            f"[vantage] VANTAGE_EDGE_WS_URL={live_url!r} is set but ignored in "
            "this scaffold; using the in-process mock edge bridge.",
            file=sys.stderr,
        )
    return MockEdgeBridge()


def build_server(registry: ToolRegistry) -> Server:
    """Create and configure the MCP server for the given tool registry."""
    server: Server = Server(SERVER_NAME)

    @server.list_tools()  # type: ignore[no-untyped-call, untyped-decorator]
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name=tool.name,
                description=tool.description,
                inputSchema=tool.input_schema,
            )
            for tool in registry.all_tools()
        ]

    @server.call_tool(validate_input=False)  # type: ignore[untyped-decorator]
    async def handle_call_tool(
        name: str,
        arguments: dict[str, Any] | None,
    ) -> list[types.TextContent]:
        tool = registry.get(name)
        if tool is None:
            result: dict[str, Any] = {
                "error": "Unknown tool",
                "tool": name,
                "available_tools": registry.names(),
            }
        else:
            try:
                result = tool.handler(arguments)
            except ToolValidationError as exc:
                result = exc.to_dict()
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

    return server


async def _serve(server: Server) -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> None:
    """Console-script entry point (``vantage-mcp``)."""
    try:
        started_at = datetime.now(timezone.utc)
        bridge = _select_bridge()
        registry = build_registry(__version__, started_at, bridge)
        server = build_server(registry)
    except StartupError as exc:
        print(f"[vantage] startup failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    except Exception as exc:  # noqa: BLE001 - surface any startup failure clearly
        print(
            "[vantage] startup failed while initializing the MCP server: "
            f"{exc}\n"
            "Remediation: run `uv sync` in apps/mcp-server, confirm Python 3.11+, "
            "and check the Cursor MCP config (command/args) in your mcp.json.",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc

    try:
        anyio.run(_serve, server)
    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl-C / client teardown.
        pass


if __name__ == "__main__":
    main()
