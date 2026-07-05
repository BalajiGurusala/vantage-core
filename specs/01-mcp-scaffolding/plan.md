# Implementation Plan: MCP Server Scaffolding

**Branch**: `01-mcp-scaffolding` | **Date**: 2026-07-04 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/01-mcp-scaffolding/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Scaffold a typed Python MCP server in `apps/mcp-server` with stdio transport, one functional health tool, two placeholder tools (DWARF symbol resolution and probe injection), an edge-bridge interface with in-process mock client, and JSON schema stubs in `libs/protocol`. Research decisions are documented in [research.md](./research.md).

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Official `mcp` Python SDK (>=1.0), Pydantic v2 (tool input validation), pytest + pytest-asyncio (testing)

**Storage**: N/A (stateless scaffold)

**Testing**: pytest, pytest-asyncio; integration tests via MCP client invocation patterns

**Target Platform**: Developer laptop / CI (macOS, Windows, Linux)

**Project Type**: MCP server (stdio CLI process)

**Performance Goals**: Health tool response under 1 second; no throughput targets for scaffold

**Constraints**: mypy strict mode; no MCP auth; no symbol strings over bridge payloads; Python-only in `apps/mcp-server`; stdio transport only

**Scale/Scope**: 3 MCP tools, 3 protocol JSON schemas, ~12 source modules

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Verdict | Notes |
|------|---------|-------|
| Python only in `apps/mcp-server` | PASS | All scaffold code under `apps/mcp-server/` |
| Rust stays in `apps/edge-daemon` | PASS | Edge daemon untouched; mock bridge only |
| No shared source between nodes | PASS | Only JSON schema stubs in `libs/protocol/` |
| Strictly typed Python (mypy) | PASS | `strict = true` in pyproject.toml |
| Spec-driven execution | PASS | Plan and design artifacts before implementation |

**Post-design re-check (Phase 1 complete)**: All gates still PASS. Protocol contracts are JSON-only. Bridge mock is in-process Python; `inject_probe` contract enforces hex-only bridge payloads (FR-009). No Complexity Tracking entries required.

## Project Structure

### Documentation (this feature)

```text
specs/01-mcp-scaffolding/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── mcp-tools.md
│   ├── inject_request.schema.json
│   ├── inject_response.schema.json
│   └── telemetry_event.schema.json
└── tasks.md             # Phase 2 output (/speckit-tasks — not yet created)
```

### Source Code (repository root)

```text
apps/mcp-server/
├── pyproject.toml
├── README.md
├── src/vantage_mcp/
│   ├── __init__.py
│   ├── server.py              # stdio MCP entry point
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── health.py          # FR-002: functional
│   │   ├── dwarf.py           # FR-003/004: placeholder
│   │   └── inject.py          # FR-003/004: placeholder
│   └── bridge/
│       ├── __init__.py
│       ├── interface.py       # EdgeBridge protocol/ABC
│       └── mock_client.py     # FR-012: simulates inject_response + telemetry_event
└── tests/
    ├── unit/
    └── integration/

libs/protocol/
├── inject_request.schema.json
├── inject_response.schema.json
└── telemetry_event.schema.json
```

**Structure Decision**: Monorepo layout with Python package under `apps/mcp-server/src/` (src layout) and protocol schemas as language-agnostic JSON in `libs/protocol/`, matching `.specify/memory/architecture.md` message shapes. Package manager: `uv` with `pyproject.toml` (see research.md).

## Complexity Tracking

> No constitution violations. Table intentionally empty.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
