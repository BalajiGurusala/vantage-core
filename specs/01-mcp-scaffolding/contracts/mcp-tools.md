# MCP Tool Contracts

**Feature**: 01-mcp-scaffolding | **Date**: 2026-07-04

**Transport**: stdio (Model Context Protocol)

**Security**: Tools that interact with the edge bridge MUST NOT transmit human-readable symbol names. Only `hex_offset` values appear in bridge payloads (FR-009).

---

## Tool: `vantage_health`

**Kind**: functional

**Description**: Returns operational status of the Vantage MCP server including version, uptime, and registered tool count.

### Input

No arguments.

### Output

```json
{
  "status": "ok",
  "version": "0.1.0",
  "uptime_seconds": 12.5,
  "tools_registered": ["vantage_health", "resolve_dwarf_symbol", "inject_probe"]
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| status | string | yes | `"ok"` when healthy |
| version | string | yes | Semver |
| uptime_seconds | number | yes | >= 0 |
| tools_registered | string[] | yes | All registered tool names |

---

## Tool: `resolve_dwarf_symbol`

**Kind**: placeholder

**Description**: Resolves a symbol name to a memory offset in a binary via DWARF debug info. Not implemented in scaffold; returns informative stub.

### Input

```json
{
  "binary_path": "/usr/bin/drone_flight_controller",
  "symbol_name": "sendThrottle"
}
```

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| binary_path | string | yes | Non-empty |
| symbol_name | string | yes | Non-empty |

### Output (stub)

```json
{
  "implemented": false,
  "message": "DWARF symbol resolution is not yet implemented. This tool will parse DWARF debug info to compute hex offsets.",
  "binary_path": "/usr/bin/drone_flight_controller",
  "symbol_name": "sendThrottle"
}
```

### Validation Error Example

Invalid input (empty `symbol_name`):

```json
{
  "error": "Validation failed",
  "fields": {
    "symbol_name": "Field required and must be non-empty"
  }
}
```

---

## Tool: `inject_probe`

**Kind**: placeholder (uses mock edge bridge)

**Description**: Commands the edge daemon to attach an eBPF probe at a hex offset. Scaffold uses mock bridge to simulate inject_response and telemetry_event.

### Input

```json
{
  "target_binary_path": "/usr/bin/drone_flight_controller",
  "hex_offset": "0x4015A0",
  "probe_type": "uprobe",
  "telemetry_format": "latency_histogram"
}
```

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| target_binary_path | string | yes | Non-empty |
| hex_offset | string | yes | Pattern `^0x[0-9A-Fa-f]+$` |
| probe_type | string | yes | `uprobe` or `kprobe` |
| telemetry_format | string | yes | `latency_histogram`, `counter`, or `raw` |

### Output (stub with mock bridge)

```json
{
  "implemented": false,
  "message": "Probe injection is not fully implemented. Mock bridge simulated the edge daemon response.",
  "bridge_status": "success",
  "probe_id": "probe_mock_a1b2c3",
  "telemetry_sample": {
    "message_type": "telemetry_event",
    "payload": {
      "probe_id": "probe_mock_a1b2c3",
      "timestamp_ns": 1718294958102934,
      "raw_data": {
        "execution_time_ns": 14500,
        "cpu_core": 1
      }
    }
  }
}
```

### Bridge Payload (what crosses the wire)

Only the following is sent to the edge bridge (no symbol names):

```json
{
  "message_type": "inject_request",
  "payload": {
    "target_binary_path": "/usr/bin/drone_flight_controller",
    "hex_offset": "0x4015A0",
    "probe_type": "uprobe",
    "telemetry_format": "latency_histogram"
  }
}
```

See [inject_request.schema.json](./inject_request.schema.json) for full schema.

### Validation Error Example

Invalid `hex_offset` (missing `0x` prefix):

```json
{
  "error": "Validation failed",
  "fields": {
    "hex_offset": "Must match pattern ^0x[0-9A-Fa-f]+$"
  }
}
```

---

## Protocol Schema References

| Message | Schema File | Direction |
|---------|-------------|-----------|
| inject_request | [inject_request.schema.json](./inject_request.schema.json) | MCP → Edge |
| inject_response | [inject_response.schema.json](./inject_response.schema.json) | Edge → MCP |
| telemetry_event | [telemetry_event.schema.json](./telemetry_event.schema.json) | Edge → MCP (stream) |

Canonical copies also live at `libs/protocol/` for cross-language reference.
