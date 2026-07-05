# Vantage MCP Server

Control-plane MCP server for the Vantage eBPF observability platform. It exposes
Vantage tools to AI assistants (e.g. Claude via Cursor) over the **Model Context
Protocol (stdio transport)**.

> **Scaffold scope**: This package is a scaffold. It ships one functional tool
> (`vantage_health`) and two placeholder tools (`resolve_dwarf_symbol`,
> `inject_probe`). Actual DWARF parsing, eBPF injection, and the live Rust edge
> daemon are out of scope — see `specs/01-mcp-scaffolding/spec.md`.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Install

```bash
cd apps/mcp-server
uv sync
```

## Run

```bash
uv run vantage-mcp
```

The server communicates over stdio and is intended to be launched by an MCP
client rather than run interactively.

## Type check

Strict `mypy` is enforced across all modules (project constitution):

```bash
uv run mypy src/vantage_mcp
```

Expected: `Success: no issues found`.

## Tests

```bash
uv run pytest tests/ -v
```

## Tools

| Tool | Kind | Description |
|------|------|-------------|
| `vantage_health` | functional | Returns operational status (version, uptime, registered tools). |
| `resolve_dwarf_symbol` | placeholder | Will resolve a symbol name to a hex offset via DWARF. Returns a stub. |
| `inject_probe` | placeholder | Will command the edge daemon to attach an eBPF probe. Uses the in-process mock bridge to simulate `inject_response` + a `telemetry_event` sample. |

### Security boundary

The `inject_probe` bridge payload is **hex-only**: it carries
`target_binary_path`, `hex_offset`, `probe_type`, `telemetry_format` and never
human-readable symbol names (FR-009 / FR-014). Probes are read-only/passive by
architecture (FR-013); runtime enforcement is the future edge daemon's job.

## Cursor MCP configuration

Add to your Cursor MCP settings (`.cursor/mcp.json` or global config):

```json
{
  "mcpServers": {
    "vantage": {
      "command": "uv",
      "args": ["run", "--directory", "apps/mcp-server", "vantage-mcp"]
    }
  }
}
```

Restart Cursor or reload MCP servers after saving.

## Protocol schemas (`libs/protocol`)

Bridge message shapes are language-agnostic JSON Schema (Draft 2020-12) stubs in
`libs/protocol/`:

- `inject_request.schema.json`
- `inject_response.schema.json`
- `telemetry_event.schema.json`

These are **schema stubs only** — no shared runtime code crosses the node
boundary (constitution §2). The copies under
`specs/01-mcp-scaffolding/contracts/` are byte-identical to the canonical
`libs/protocol/` copies (verified via `diff`); keep them in sync when either
changes.

## Layout

```text
apps/mcp-server/
├── pyproject.toml
├── README.md
├── src/vantage_mcp/
│   ├── __init__.py
│   ├── server.py          # stdio MCP entry point + tool registration
│   ├── tools/
│   │   ├── health.py      # functional
│   │   ├── dwarf.py       # placeholder
│   │   ├── inject.py      # placeholder (uses mock bridge)
│   │   └── validation.py  # field-level validation error helper
│   └── bridge/
│       ├── interface.py   # EdgeBridge protocol/ABC
│       └── mock_client.py # in-process mock edge bridge
└── tests/
    ├── unit/
    └── integration/
```
