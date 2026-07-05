# Tasks: MCP Server Scaffolding

**Input**: Design documents from `/specs/01-mcp-scaffolding/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Omitted — feature spec does not request TDD. pytest is listed in plan for future use; US3 covers mypy strict typing.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: User story label (US1, US2, US3) — only on user story phase tasks
- Include exact file paths in descriptions

## Path Conventions

- MCP server package: `apps/mcp-server/src/vantage_mcp/`
- Tests (reserved): `apps/mcp-server/tests/`
- Protocol schemas: `libs/protocol/`
- Feature docs: `specs/01-mcp-scaffolding/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create directory tree per plan in `apps/mcp-server/` (`src/vantage_mcp/tools/`, `src/vantage_mcp/bridge/`, `tests/unit/`, `tests/integration/`)
- [ ] T002 Create `apps/mcp-server/pyproject.toml` with uv, Python 3.11+, deps (`mcp>=1.0`, pydantic v2), script entry `vantage-mcp`, and `[tool.mypy]` strict stub
- [ ] T003 [P] Create `apps/mcp-server/src/vantage_mcp/__init__.py` with package version constant
- [ ] T004 [P] Create `apps/mcp-server/README.md` skeleton with install, run, and type-check commands
- [ ] T005 [P] Confirm `libs/protocol/*.schema.json` matches `specs/01-mcp-scaffolding/contracts/*.schema.json` and document parity in `apps/mcp-server/README.md`
- [ ] T006 Run `uv sync` in `apps/mcp-server/` to produce `uv.lock`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Implement `EdgeBridge` Protocol/ABC in `apps/mcp-server/src/vantage_mcp/bridge/interface.py`
- [ ] T008 Implement `MockEdgeBridge` with inject_response and telemetry_event simulation in `apps/mcp-server/src/vantage_mcp/bridge/mock_client.py`
- [ ] T009 Create shared field-level validation error helper in `apps/mcp-server/src/vantage_mcp/tools/validation.py`
- [ ] T010 Implement MCP stdio server skeleton using `mcp.server.stdio` in `apps/mcp-server/src/vantage_mcp/server.py`
- [ ] T011 [P] Create tool registration module in `apps/mcp-server/src/vantage_mcp/tools/__init__.py`
- [ ] T012 Add startup error handling with remediation messages in `apps/mcp-server/src/vantage_mcp/server.py`

**Checkpoint**: Server starts over stdio; tool registration framework ready; no user-facing tools yet.

---

## Phase 3: User Story 1 - Connect AI Assistant to MCP Server (Priority: P1) 🎯 MVP

**Goal**: Runnable stdio MCP server with functional `vantage_health` tool

**Independent Test**: Connect MCP client over stdio, invoke `vantage_health`, receive structured success response within 5 seconds (quickstart.md SC-001)

### Implementation for User Story 1

- [ ] T013 [US1] Implement `HealthStatus` Pydantic model and `vantage_health` tool in `apps/mcp-server/src/vantage_mcp/tools/health.py`
- [ ] T014 [US1] Register `vantage_health` on MCP server in `apps/mcp-server/src/vantage_mcp/server.py`
- [ ] T015 [US1] Wire `vantage-mcp` CLI entry point to `server.py` main in `apps/mcp-server/pyproject.toml`
- [ ] T016 [US1] Ensure startup failure paths emit clear errors with remediation in `apps/mcp-server/src/vantage_mcp/server.py`

**Checkpoint**: MVP — Cursor can connect via stdio and invoke `vantage_health`.

---

## Phase 4: User Story 2 - Discover Placeholder Vantage Tools (Priority: P2)

**Goal**: Placeholder tools `resolve_dwarf_symbol` and `inject_probe` with validation and mock bridge integration

**Independent Test**: List tools, invoke placeholders with valid/invalid input, confirm stubs and field-level errors (quickstart.md SC-002, SC-004, SC-006)

### Implementation for User Story 2

- [ ] T017 [P] [US2] Implement `resolve_dwarf_symbol` placeholder per contracts in `apps/mcp-server/src/vantage_mcp/tools/dwarf.py`
- [ ] T018 [P] [US2] Implement `inject_probe` placeholder with Pydantic input validation in `apps/mcp-server/src/vantage_mcp/tools/inject.py`
- [ ] T019 [US2] Integrate `MockEdgeBridge` into `inject_probe` with hex-only bridge payload in `apps/mcp-server/src/vantage_mcp/tools/inject.py`
- [ ] T020 [US2] Register placeholder tools in `apps/mcp-server/src/vantage_mcp/server.py`
- [ ] T021 [US2] Map validation failures to field-level errors via `validation.py` in `apps/mcp-server/src/vantage_mcp/tools/dwarf.py` and `inject.py`
- [ ] T022 [US2] Ensure stub responses include `implemented: false` and informative `message` in `apps/mcp-server/src/vantage_mcp/tools/dwarf.py` and `inject.py`

**Checkpoint**: All three tools callable; placeholders return structured stubs; mock bridge simulates edge flow.

---

## Phase 5: User Story 3 - Maintain Type-Safe Python Codebase (Priority: P3)

**Goal**: Strict mypy across all scaffold modules with zero errors

**Independent Test**: Run `uv run mypy src/vantage_mcp` and confirm zero errors (quickstart.md SC-003)

### Implementation for User Story 3

- [ ] T023 [US3] Add complete type annotations to all modules under `apps/mcp-server/src/vantage_mcp/`
- [ ] T024 [US3] Finalize `[tool.mypy]` strict config in `apps/mcp-server/pyproject.toml` (`mypy_path = "src"`, `packages = ["vantage_mcp"]`)
- [ ] T025 [US3] Document `uv run mypy src/vantage_mcp` command in `apps/mcp-server/README.md`

**Checkpoint**: `uv run mypy src/vantage_mcp` passes with zero errors.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, validation, and requirements coverage review

- [ ] T026 [P] Add Cursor MCP config snippet to `apps/mcp-server/README.md` per `specs/01-mcp-scaffolding/research.md`
- [ ] T027 [P] Validate success criteria SC-001 through SC-006 using `specs/01-mcp-scaffolding/quickstart.md` (includes SC-005 ten-invocation stability sequence) (includes SC-005 ten-invocation stability sequence)
- [ ] T028 Review FR-001 through FR-012 coverage across `apps/mcp-server/` and `libs/protocol/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — **BLOCKS all user stories**
- **User Stories (Phases 3–5)**: Depend on Phase 2 completion
  - US1 (Phase 3): MVP stop point after completion
  - US2 (Phase 4): Depends on Phase 2; shares `server.py` with US1 but independently testable for placeholder behavior
  - US3 (Phase 5): Best after US1 + US2 when all source modules exist
- **Polish (Phase 6)**: Depends on Phases 3–5

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational — no dependency on US2/US3
- **User Story 2 (P2)**: Starts after Foundational — integrates with `server.py` from US1 but placeholder tools are independently testable
- **User Story 3 (P3)**: Starts after US1 + US2 source modules exist

### Within Each User Story

- Models/tools before server registration
- Server registration before CLI wiring (US1)
- Bridge integration before placeholder registration (US2)
- All modules typed before mypy config finalization (US3)

### Parallel Opportunities

- Phase 1: T003, T004, T005 in parallel
- Phase 2: T011 parallel with T007–T010
- US2: T017 and T018 in parallel (different files)
- Polish: T026 and T027 in parallel

---

## Parallel Example: User Story 2

```bash
# Launch placeholder tool implementations together:
Task T017: "Implement resolve_dwarf_symbol in apps/mcp-server/src/vantage_mcp/tools/dwarf.py"
Task T018: "Implement inject_probe in apps/mcp-server/src/vantage_mcp/tools/inject.py"

# Then sequentially:
Task T019: "Integrate MockEdgeBridge in inject.py"
Task T020: "Register tools in server.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T006)
2. Complete Phase 2: Foundational (T007–T012)
3. Complete Phase 3: User Story 1 (T013–T016)
4. **STOP and VALIDATE**: quickstart.md SC-001
5. Demo MCP connection in Cursor

### Incremental Delivery

1. Setup + Foundational → server skeleton ready
2. User Story 1 → health tool → MVP demo
3. User Story 2 → placeholder tools + mock bridge → full tool surface
4. User Story 3 → mypy strict → constitution compliance
5. Polish → quickstart validation → release-ready scaffold

### Parallel Team Strategy

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T013–T016)
   - Developer B: User Story 2 (T017–T022) — after US1 registers server or coordinate on `server.py`
   - Developer C: User Story 3 (T023–T025) — after source modules exist
3. All converge on Polish (T026–T028)

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks in the same batch
- [Story] label maps task to user story for traceability
- Each user story is independently testable per spec Independent Test criteria
- No test tasks generated — spec does not request TDD
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Constitution: Python only in `apps/mcp-server/`; protocol stubs only in `libs/protocol/`
