# Research: MCP Server Scaffolding

**Feature**: 01-mcp-scaffolding | **Date**: 2026-07-04

## 1. MCP Python SDK

**Decision**: Use the official `mcp` Python package (>=1.0) with the `stdio_server` entry pattern and `Server` class tool registration.

**Rationale**: The official SDK is maintained by the Model Context Protocol project, supports stdio transport (required by spec), integrates Pydantic for tool schemas, and is the standard choice for Cursor MCP server integration. The `mcp.server.stdio.stdio_server` context manager handles stdin/stdout lifecycle.

**Alternatives considered**:
- **Custom JSON-RPC over stdio**: Rejected — reinvents protocol handling, no schema tooling, higher maintenance.
- **FastMCP only without stdio**: Rejected — spec requires stdio; FastMCP can wrap SDK but adds indirection without benefit for scaffold.

**Cursor MCP config snippet** (for quickstart reference):

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

---

## 2. Package Manager

**Decision**: Use `uv` with `pyproject.toml` (PEP 621) for dependency management and script entry points.

**Rationale**: `uv` provides fast installs, lockfile support (`uv.lock`), and native `uv run` for MCP server invocation without manual venv activation. Aligns with modern Python monorepo practices and keeps CI setup minimal.

**Alternatives considered**:
- **pip + requirements.txt**: Rejected — no lockfile by default, slower CI, manual venv management.
- **Poetry**: Rejected — heavier tooling for a small scaffold; `uv` covers same use cases with less overhead.

---

## 3. Tool Schema Pattern

**Decision**: Define Pydantic v2 `BaseModel` classes for each tool's input; register tools via MCP SDK decorators; map `ValidationError` to field-level error strings in tool handlers.

**Rationale**: Pydantic is bundled with the MCP SDK ecosystem, satisfies FR-005 (field-level validation errors), and supports mypy strict typing via typed models. Placeholder tools return structured dict responses with `implemented: false` rather than raising errors.

**Alternatives considered**:
- **Manual dict validation**: Rejected — error-prone, poor mypy support, duplicates Pydantic.
- **JSON Schema only (no Pydantic)**: Rejected — loses compile-time type safety required by constitution.

---

## 4. Mock Edge Bridge

**Decision**: Implement an in-process `MockEdgeBridge` class satisfying an `EdgeBridge` Protocol/ABC. No real WebSocket network required for scaffold acceptance (SC-006). Optional `VANTAGE_EDGE_WS_URL` env var reserved for future live integration; when unset, mock is used exclusively. **Scaffold precedence**: even when `VANTAGE_EDGE_WS_URL` is set, this feature continues to use the mock bridge (the live `LiveEdgeBridge` is a reserved, unimplemented stub); the variable is read-and-ignored so the future feature can wire in live behavior without changing the interface.

**Rationale**: Spec clarifies mock client is sufficient; in-process mock avoids flaky network tests, satisfies FR-012, and simulates `inject_response` followed by `telemetry_event` synchronously or via async callback.

**Alternatives considered**:
- **Real WebSocket to test container**: Rejected — edge daemon out of scope; adds CI complexity.
- **`websockets` library with local echo server**: Rejected — unnecessary for scaffold; mock interface is cleaner.

**Mock behavior**:
1. Accept `InjectRequest` payload (hex offset only on wire per FR-009).
2. Return `InjectResponse` with `status: success`, generated `probe_id`.
3. Emit one `TelemetryEvent` with sample `raw_data`.

---

## 5. mypy Configuration

**Decision**: Enable mypy `strict = true` in `pyproject.toml` with `packages = ["vantage_mcp"]`, `mypy_path = "src"`, and `python_version = "3.11"`.

**Rationale**: Constitution requires strictly typed Python. Strict mode catches optional misuse, untyped defs, and missing return types before runtime. Src layout requires explicit `mypy_path`.

**Alternatives considered**:
- **Partial strict (disallow_untyped_defs only)**: Rejected — constitution implies full strictness; partial leaves gaps.
- **pyright instead of mypy**: Rejected — constitution explicitly references mypy standards.

---

## 6. Protocol Schema Format

**Decision**: JSON Schema Draft 2020-12 documents in `libs/protocol/` mirroring architecture.md payloads. No code generation, no runtime validation library in this feature.

**Rationale**: FR-011 requires schema stubs only. JSON Schema is language-agnostic (usable by future Rust edge daemon tooling) and matches constitution's shared-payload-via-`libs/protocol` rule.

**Alternatives considered**:
- **Protobuf**: Rejected — not in architecture spec; adds codegen complexity.
- **Shared Python dataclasses in libs/protocol**: Rejected — violates no-shared-runtime-code clarification.

---

## Resolved Technical Context Items

| Original unknown | Resolution |
|------------------|------------|
| Package manager (`uv` vs `pip`) | `uv` + `pyproject.toml` |
| Mock vs real WebSocket | In-process mock; live optional via env var |
| MCP SDK choice | Official `mcp` package, stdio_server |

All NEEDS CLARIFICATION items from Technical Context are resolved.
