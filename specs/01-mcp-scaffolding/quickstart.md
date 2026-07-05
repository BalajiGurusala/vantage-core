# Quickstart: MCP Server Scaffolding Validation

**Feature**: 01-mcp-scaffolding | **Date**: 2026-07-04

This guide validates the scaffold against success criteria SC-001 through SC-006. Run these steps **after implementation** (via `/speckit-tasks` + `/speckit-implement`).

**References**:
- Tool contracts: [contracts/mcp-tools.md](./contracts/mcp-tools.md)
- Data model: [data-model.md](./data-model.md)
- Research decisions: [research.md](./research.md)

---

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) installed
- Repository cloned with feature branch `01-mcp-scaffolding`
- Cursor (or another MCP client) for stdio integration tests

---

## Setup

From repository root:

```bash
cd apps/mcp-server
uv sync
```

Verify entry point is registered:

```bash
uv run vantage-mcp --help
```

Expected: help text or server startup message (no import errors).

---

## Cursor MCP Configuration

Add to Cursor MCP settings (`.cursor/mcp.json` or global config):

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

---

## SC-001: Connect and Invoke Health Tool

**Goal**: Developer connects MCP client over stdio and invokes `vantage_health` within 5 minutes.

**Steps**:
1. Enable the `vantage` MCP server in Cursor.
2. Open MCP tool list; confirm `vantage_health`, `resolve_dwarf_symbol`, and `inject_probe` appear.
3. Invoke `vantage_health` with no arguments.

**Expected outcome**:
- Successful MCP handshake (no connection errors in Cursor MCP panel).
- Response includes `"status": "ok"`, a version string, `uptime_seconds >= 0`, and non-empty `tools_registered` list.
- Response arrives within 5 seconds.

---

## SC-002: Placeholder Tools Return Stubs

**Goal**: 100% of placeholder tools return structured stub responses for valid input.

**Steps**:
1. Invoke `resolve_dwarf_symbol` with:
   ```json
   { "binary_path": "/usr/bin/drone_flight_controller", "symbol_name": "sendThrottle" }
   ```
2. Invoke `inject_probe` with:
   ```json
   {
     "target_binary_path": "/usr/bin/drone_flight_controller",
     "hex_offset": "0x4015A0",
     "probe_type": "uprobe",
     "telemetry_format": "latency_histogram"
   }
   ```

**Expected outcome**:
- Both return `"implemented": false` with informative `message` fields.
- Neither returns an MCP protocol error or server crash.
- `inject_probe` additionally includes `bridge_status`, `probe_id`, and `telemetry_sample`.

---

## SC-003: Static Type Checking Passes

**Goal**: Zero mypy errors across all scaffold modules.

**Steps**:

```bash
cd apps/mcp-server
uv run mypy src/vantage_mcp
```

**Expected outcome**: `Success: no issues found in N source files` (zero errors).

---

## SC-004: Field-Level Validation Errors

**Goal**: Invalid inputs produce human-readable field-level errors.

**Steps**:
1. Invoke `resolve_dwarf_symbol` with `{ "binary_path": "", "symbol_name": "" }`.
2. Invoke `inject_probe` with `{ "target_binary_path": "/bin/app", "hex_offset": "4015A0", "probe_type": "uprobe", "telemetry_format": "raw" }` (note missing `0x` prefix).

**Expected outcome**:
- Each invocation returns a validation error identifying the invalid field(s) by name.
- Server does not crash.

---

## SC-005: Stability Under Repeated Invocations

**Goal**: No crash after 10 consecutive tool invocations.

**Steps**:
Run the following sequence via MCP client or test script (mix of valid and invalid):

1. `vantage_health` (valid)
2. `resolve_dwarf_symbol` (valid)
3. `inject_probe` (valid)
4. `resolve_dwarf_symbol` (invalid — empty symbol)
5. `inject_probe` (invalid — bad hex)
6. `vantage_health` (valid)
7. `inject_probe` (valid)
8. `resolve_dwarf_symbol` (valid)
9. `vantage_health` (valid)
10. `inject_probe` (invalid — bad probe_type)

**Expected outcome**: Server remains running; all valid calls succeed; invalid calls return validation errors.

---

## SC-006: Mock Bridge Simulates Edge Flow

**Goal**: Mock WebSocket client simulates `inject_response` and `telemetry_event` without live edge daemon.

**Steps**:
1. Ensure `VANTAGE_EDGE_WS_URL` is **not** set (forces mock mode).
2. Invoke `inject_probe` with valid input (see SC-002).
3. Inspect response for `telemetry_sample`.

**Expected outcome**:
- `bridge_status` is `"success"`.
- `probe_id` is a non-empty string (e.g., `probe_mock_*`).
- `telemetry_sample.message_type` is `"telemetry_event"`.
- `telemetry_sample.payload.probe_id` matches the inject response `probe_id`.
- `telemetry_sample.payload.raw_data` contains sample telemetry fields.

**Optional live test** (not required for scaffold acceptance):
- Set `VANTAGE_EDGE_WS_URL=ws://localhost:8765` when edge daemon is available in a future feature. Note: in this scaffold the mock is used even when this variable is set (the variable is read-and-ignored; live behavior arrives with the edge-daemon feature).

---

## SC-007: Bridge Payload Is Hex-Only (No Symbol Names)

**Goal**: The `inject_probe` edge-bridge payload contains only permitted fields and no human-readable symbol names (FR-009, FR-014).

**Steps**:
1. Invoke `inject_probe` with valid input (see SC-002).
2. Capture the `inject_request` payload emitted to the mock bridge (via the mock's recorded last request or an integration test hook).

**Expected outcome**:
- The payload's `payload` object contains exactly `target_binary_path`, `hex_offset`, `probe_type`, and `telemetry_format`.
- No `symbol_name` (or any other human-readable identifier) field is present.
- `hex_offset` matches `^0x[0-9A-Fa-f]+$`.

---

## Automated Test Commands

After implementation, run the full test suite:

```bash
cd apps/mcp-server
uv run pytest tests/ -v
```

Expected: all unit and integration tests pass.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| MCP server not listed in Cursor | Config path or `uv` not in PATH | Verify `mcp.json` and run `which uv` |
| Import errors on startup | Dependencies not installed | Run `uv sync` in `apps/mcp-server` |
| mypy errors | Missing type annotations | Fix reported file/line; see constitution |
| Empty tool list | Server failed during registration | Check stderr output from `uv run vantage-mcp` |

---

## Next Steps

After all scenarios pass, proceed to task breakdown:

```
/speckit-tasks
```
