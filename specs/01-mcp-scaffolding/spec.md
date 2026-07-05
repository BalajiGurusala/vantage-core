# Feature Specification: MCP Server Scaffolding

**Feature Branch**: `01-mcp-scaffolding`

**Created**: 2026-07-04

**Status**: Draft

**Input**: User description: "Scaffold the Python MCP server in apps/mcp-server: project layout, typed Python tooling (mypy), MCP protocol server skeleton exposing placeholder tools for DWARF parsing and edge-daemon WebSocket bridge. Out of scope: actual DWARF math, eBPF injection, edge daemon implementation."

## Clarifications

### Session 2026-07-04

- Q: Which MCP transport should the scaffold support? → A: stdio only
- Q: How should the scaffold handle edge-daemon WebSocket connectivity? → A: Mock client; live optional
- Q: What authentication is required for MCP client connections in v1? → A: None for local dev
- Q: What is the scope of shared protocol definitions in libs/protocol? → A: JSON schema stubs only
- Q: What defines scaffold-complete for the edge bridge interface? → A: Interface plus mock client

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Connect AI Assistant to MCP Server (Priority: P1)

A developer working on Vantage observability wants to connect their AI assistant (e.g., Claude via Cursor) to the Vantage MCP server so the assistant can discover and invoke Vantage tools. They start the MCP server locally and confirm the connection succeeds with a basic health or status response.

**Why this priority**: Without a working MCP server skeleton and at least one callable tool, no downstream Vantage AI workflows are possible. This is the minimum viable scaffold.

**Independent Test**: Start the MCP server, connect an MCP client over stdio, invoke the health/status tool, and receive a structured success response within 5 seconds.

**Acceptance Scenarios**:

1. **Given** the MCP server is installed and configured, **When** a developer starts it and connects an MCP client via stdio, **Then** the client receives a successful handshake and can list available tools.
2. **Given** the MCP server is running, **When** the developer invokes the health/status tool, **Then** the server returns a structured response indicating operational status.
3. **Given** the MCP server fails to start (e.g., missing config), **When** the developer attempts to launch it, **Then** a clear error message explains the failure and how to fix it.

---

### User Story 2 - Discover Placeholder Vantage Tools (Priority: P2)

A developer wants the AI assistant to see the planned Vantage tool surface—tools for DWARF symbol resolution and edge-daemon probe injection—even before those capabilities are fully implemented. Placeholder tools return informative stub responses so the assistant understands intended workflows.

**Why this priority**: Establishes the contract between AI and Vantage early, enabling parallel development of MCP tools and edge daemon without blocking integration design.

**Independent Test**: Connect an MCP client, list tools, invoke each placeholder tool with sample inputs, and verify each returns a structured stub response describing future behavior.

**Acceptance Scenarios**:

1. **Given** the MCP server is running, **When** a client lists tools, **Then** placeholder tools for DWARF resolution and edge probe injection are visible with documented input schemas.
2. **Given** a placeholder tool is invoked with valid sample input, **When** the request is processed, **Then** the server returns a structured stub response (not an error) indicating the capability is not yet implemented.
3. **Given** a placeholder tool is invoked with invalid input, **When** the request is processed, **Then** the server returns a validation error with field-level guidance.

---

### User Story 3 - Maintain Type-Safe Python Codebase (Priority: P3)

A developer contributing to the MCP server wants static type checking enforced so that future DWARF parsing and WebSocket bridge code remains maintainable and catches errors before runtime.

**Why this priority**: The project constitution requires strictly typed Python; establishing this in the scaffold prevents technical debt from day one.

**Independent Test**: Run the project's type-check command against the scaffold codebase and confirm zero type errors on all scaffold modules.

**Acceptance Scenarios**:

1. **Given** the scaffold codebase is complete, **When** a developer runs the type-check command, **Then** all scaffold modules pass with zero errors.
2. **Given** a developer adds a function with incorrect type annotations, **When** type checking runs, **Then** the error is reported with file and line location.

---

### Edge Cases

- What happens when the MCP client disconnects mid-request? The server handles gracefully without crashing and can accept new connections.
- What happens when a placeholder tool receives an empty or malformed payload? The server returns a validation error, not a crash or silent failure.
- What happens when the edge-daemon WebSocket endpoint is unreachable during scaffold testing? The mock WebSocket client returns predictable stub responses; a live edge connection is optional and not required for scaffold acceptance. Unreachable live endpoints do not block scaffold validation.
- What happens when two MCP clients connect simultaneously? The server supports multiple concurrent client sessions without interference.
- What happens when the developer runs the server without required environment configuration? A clear startup error is shown with remediation steps.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a runnable MCP server entry point that an AI assistant can connect to via stdio transport.
- **FR-002**: System MUST expose at least one fully functional tool (health/status) that returns structured operational status.
- **FR-003**: System MUST register placeholder tools for DWARF symbol resolution and edge-daemon probe injection with documented input/output schemas.
- **FR-004**: Placeholder tools MUST return informative stub responses (not errors) when invoked, indicating the capability is planned but not yet implemented.
- **FR-005**: System MUST validate tool inputs and return field-level errors for invalid requests.
- **FR-006**: System MUST enforce static type checking across all scaffold modules with zero tolerated type errors on delivery.
- **FR-007**: System MUST define a project layout separating MCP protocol handling, tool definitions, and edge-daemon communication interfaces.
- **FR-008**: System MUST NOT perform actual DWARF parsing, eBPF injection, or edge-daemon implementation in this feature.
- **FR-009**: System MUST NOT transmit human-readable symbol names over the network bridge; only raw hex offsets per architecture security boundaries.
- **FR-010**: System MUST accept MCP client connections without authentication for local development in this scaffold.
- **FR-011**: System MUST define JSON schema stub documents in `libs/protocol` for inject_request, inject_response, and telemetry_event message types without shared runtime code.
- **FR-012**: System MUST implement an edge bridge interface with a mock WebSocket client that simulates inject_response and telemetry_event flows for scaffold testing.

### Key Entities

- **MCP Server**: The control-plane process exposing tools to AI assistants via stdio; attributes include connection status, registered tools, and operational health.
- **MCP Tool**: A callable capability exposed to AI assistants; attributes include name, description, input schema, and response schema. May be functional (health) or placeholder (DWARF, inject).
- **Edge Bridge Interface**: The abstraction for communicating with the edge daemon over JSON-over-WebSockets; attributes include connection state and message types (inject_request, inject_response, telemetry_event). Scaffold delivers interface definition plus mock client only.
- **Protocol Schema Stub**: JSON schema document defining message shape for a protocol payload; no runtime validation library required in this feature.
- **Placeholder Response**: A structured stub indicating planned behavior, returned by unimplemented tools.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer can connect an MCP client over stdio and invoke the health/status tool successfully on first attempt within 5 minutes of following setup instructions.
- **SC-002**: 100% of registered placeholder tools return structured stub responses (not errors or crashes) when invoked with valid sample input.
- **SC-003**: Static type checking passes with zero errors across all scaffold modules on delivery.
- **SC-004**: All tool input validation failures produce human-readable error messages identifying the invalid field(s).
- **SC-005**: The MCP server remains stable (no crash) after 10 consecutive tool invocations including mix of valid and invalid inputs.
- **SC-006**: Mock WebSocket client successfully simulates inject_response and telemetry_event without a live edge daemon.

## Assumptions

- Target users are developers building or operating the Vantage platform, not end-users of embedded devices.
- The MCP server runs on the developer's laptop or CI/CD runner, not on the embedded Linux target.
- Edge daemon (`apps/edge-daemon`) is out of scope; only the MCP-side bridge interface and mock client are scaffolded.
- Shared protocol message shapes are defined as JSON schema stub documents in `libs/protocol`; no shared runtime code or code generation in this feature.
- Python is the sole language for this feature per project constitution; no Rust code is introduced.
- Standard developer tooling (package manager, linter, type checker) is acceptable for the scaffold without prescribing specific tool names in this spec.
- Local development assumes trusted environment; authentication is deferred to a future production-hardening feature.

## Out of Scope

- Actual DWARF file parsing and memory offset calculation
- eBPF bytecode generation or injection
- Edge daemon (Rust) implementation
- Live telemetry streaming from hardware targets
- Production deployment, scaling, or multi-tenant hosting
- Dashboard or UI components
- MCP authentication or authorization
- Server-Sent Events (SSE) transport for MCP
- Shared runtime protocol library code in `libs/protocol`
