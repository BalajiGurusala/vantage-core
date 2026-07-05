"""End-to-end MCP stdio integration test for the scaffold.

Spawns the real `vantage-mcp` server over stdio and exercises the success
criteria: connect + health (SC-001), placeholder stubs (SC-002), field-level
validation (SC-004), 10-invocation stability (SC-005), and mock bridge
telemetry (SC-006).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

_SERVER_DIR = Path(__file__).resolve().parents[2]

# Launch the server with the current interpreter (`python -m vantage_mcp.server`)
# rather than `uv run`, so the test does not depend on the uv cache being
# writable. In normal use the console script `vantage-mcp` / `uv run vantage-mcp`
# is the entry point (see README / quickstart).
_SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,
    args=["-m", "vantage_mcp.server"],
    cwd=str(_SERVER_DIR),
    env=dict(os.environ),
)


def _payload(result: Any) -> dict[str, Any]:
    """Extract the JSON dict returned in a tool result's text content."""
    assert result.content, "tool result had no content"
    text = result.content[0].text
    parsed: dict[str, Any] = json.loads(text)
    return parsed


@pytest.mark.asyncio
async def test_connect_list_and_invoke_health() -> None:
    async with stdio_client(_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()  # SC-001: handshake

            tools = await session.list_tools()
            names = {tool.name for tool in tools.tools}
            assert {"vantage_health", "resolve_dwarf_symbol", "inject_probe"} <= names

            health = _payload(await session.call_tool("vantage_health", {}))
            assert health["status"] == "ok"
            assert health["uptime_seconds"] >= 0
            assert health["tools_registered"]


@pytest.mark.asyncio
async def test_placeholders_and_mock_bridge() -> None:
    async with stdio_client(_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # SC-002: placeholder stub responses
            dwarf = _payload(
                await session.call_tool(
                    "resolve_dwarf_symbol",
                    {"binary_path": "/bin/app", "symbol_name": "sendThrottle"},
                )
            )
            assert dwarf["implemented"] is False

            # SC-006: mock bridge simulates inject_response + telemetry_event
            inject = _payload(
                await session.call_tool(
                    "inject_probe",
                    {
                        "target_binary_path": "/bin/app",
                        "hex_offset": "0x4015A0",
                        "probe_type": "uprobe",
                        "telemetry_format": "latency_histogram",
                    },
                )
            )
            assert inject["bridge_status"] == "success"
            assert inject["probe_id"]
            assert inject["telemetry_sample"]["message_type"] == "telemetry_event"
            assert (
                inject["telemetry_sample"]["payload"]["probe_id"] == inject["probe_id"]
            )


@pytest.mark.asyncio
async def test_field_level_validation_errors() -> None:
    async with stdio_client(_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # SC-004: invalid inputs identify the offending field(s)
            empty = _payload(
                await session.call_tool(
                    "resolve_dwarf_symbol",
                    {"binary_path": "", "symbol_name": ""},
                )
            )
            assert empty["error"] == "Validation failed"
            assert "symbol_name" in empty["fields"]

            bad_hex = _payload(
                await session.call_tool(
                    "inject_probe",
                    {
                        "target_binary_path": "/bin/app",
                        "hex_offset": "4015A0",
                        "probe_type": "uprobe",
                        "telemetry_format": "raw",
                    },
                )
            )
            assert "hex_offset" in bad_hex["fields"]


@pytest.mark.asyncio
async def test_stability_ten_invocations() -> None:
    """SC-005: server stays up across a mix of valid and invalid calls."""
    valid_inject = {
        "target_binary_path": "/bin/app",
        "hex_offset": "0x4015A0",
        "probe_type": "uprobe",
        "telemetry_format": "latency_histogram",
    }
    sequence: list[tuple[str, dict[str, Any]]] = [
        ("vantage_health", {}),
        ("resolve_dwarf_symbol", {"binary_path": "/bin/app", "symbol_name": "f"}),
        ("inject_probe", valid_inject),
        ("resolve_dwarf_symbol", {"binary_path": "", "symbol_name": ""}),
        ("inject_probe", {**valid_inject, "hex_offset": "nope"}),
        ("vantage_health", {}),
        ("inject_probe", valid_inject),
        ("resolve_dwarf_symbol", {"binary_path": "/bin/app", "symbol_name": "g"}),
        ("vantage_health", {}),
        ("inject_probe", {**valid_inject, "probe_type": "xprobe"}),
    ]

    async with stdio_client(_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            for name, args in sequence:
                result = await session.call_tool(name, args)
                assert result.content, f"{name} returned no content"

            # Still responsive after the sequence.
            health = _payload(await session.call_tool("vantage_health", {}))
            assert health["status"] == "ok"
