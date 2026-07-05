# Protocol Requirements Quality Checklist: MCP Server Scaffolding

**Purpose**: Validate completeness, clarity, and consistency of JSON protocol schema and edge bridge requirements across spec, plan, data-model, contracts, and architecture
**Created**: 2026-07-04
**Feature**: [spec.md](../spec.md)

## Requirement Completeness

- [ ] CHK001 - Are all three protocol message types (inject_request, inject_response, telemetry_event) required in FR-011? [Completeness, Spec §FR-011]
- [ ] CHK002 - Are required payload fields for inject_request documented in requirements and schema stubs? [Completeness, Contract §inject_request.schema.json]
- [ ] CHK003 - Are required payload fields for inject_response documented in requirements and schema stubs? [Completeness, Contract §inject_response.schema.json]
- [ ] CHK004 - Are required payload fields for telemetry_event documented in requirements and schema stubs? [Completeness, Contract §telemetry_event.schema.json]
- [ ] CHK005 - Are requirements defined for dual schema locations (specs/contracts and libs/protocol)? [Completeness, Plan §Project Structure]
- [ ] CHK006 - Are mock bridge simulation requirements (inject_response + telemetry_event) fully specified in FR-012? [Completeness, Spec §FR-012]
- [ ] CHK007 - Are requirements explicit that libs/protocol contains JSON schema stubs only (no runtime code)? [Completeness, Spec §FR-011]
- [ ] CHK008 - Are WebSocket transport requirements for the bridge referenced from architecture in spec or plan? [Completeness, Architecture §2]

## Requirement Clarity

- [ ] CHK009 - Is hex offset validation pattern (`^0x[0-9A-Fa-f]+$`) consistently specified in spec, data-model, and JSON schemas? [Clarity, Data Model §VR-001]
- [ ] CHK010 - Is `message_type` const enforcement required and documented for all three schemas? [Clarity, Contract schemas]
- [ ] CHK011 - Are probe_type allowed values (uprobe, kprobe) consistently defined across data-model and schemas? [Clarity, Data Model §Enumerations]
- [ ] CHK012 - Are telemetry_format enum values consistently defined across requirements and schemas? [Clarity, Data Model §InjectProbeRequest]
- [ ] CHK013 - Is mock-vs-live edge connection behavior unambiguous in requirements (default mock, optional live)? [Clarity, Spec §Clarifications]
- [ ] CHK014 - Is scaffold telemetry scope (single sample vs continuous stream) explicitly defined relative to architecture? [Clarity, Gap]

## Requirement Consistency

- [ ] CHK015 - Do architecture.md §2.1–2.3 example payloads align with contract JSON schema field names and types? [Consistency, Architecture §2]
- [ ] CHK016 - Are inject_request fields in contracts identical to libs/protocol schema stubs? [Consistency, Plan §Project Structure]
- [ ] CHK017 - Are inject_response fields in contracts identical to libs/protocol schema stubs? [Consistency, libs/protocol]
- [ ] CHK018 - Are telemetry_event fields in contracts identical to libs/protocol schema stubs? [Consistency, libs/protocol]
- [ ] CHK019 - Do data-model InjectRequest entity fields match contract schema properties? [Consistency, Data Model §InjectRequest]
- [ ] CHK020 - Does plan target platform (macOS, Windows, Linux) conflict with spec assumptions (laptop/CI)? [Conflict, Plan vs Spec §Assumptions]
- [ ] CHK021 - Is kprobe in data-model enums reconciled with architecture examples showing only uprobe? [Ambiguity, Data Model §Enumerations]

## Acceptance Criteria Quality

- [ ] CHK022 - Does SC-006 define measurable mock bridge outcomes (inject_response + telemetry_event) at requirements level? [Measurability, Spec §SC-006]
- [ ] CHK023 - Can FR-011 compliance be verified by inspecting schema stub documents alone? [Measurability, Spec §FR-011]
- [ ] CHK024 - Are probe_id linkage requirements between inject_response and telemetry_event specified for mock flow? [Measurability, Data Model §VR-006]
- [ ] CHK025 - Is timestamp_ns requirement for telemetry_event quantified (positive integer)? [Measurability, Contract §telemetry_event.schema.json]

## Scenario Coverage

- [ ] CHK026 - Are primary-flow requirements defined for inject_request emission from inject_probe tool? [Coverage, Spec §FR-012]
- [ ] CHK027 - Are primary-flow requirements defined for inject_response handling in mock bridge? [Coverage, Spec §FR-012]
- [ ] CHK028 - Are primary-flow requirements defined for telemetry_event emission in mock bridge? [Coverage, Spec §SC-006]
- [ ] CHK029 - Are alternate-flow requirements defined for optional live WebSocket via VANTAGE_EDGE_WS_URL? [Coverage, Research §Mock Edge Bridge]
- [ ] CHK030 - Are exception-flow requirements defined when inject_response status is error? [Coverage, Gap]
- [ ] CHK031 - Are requirements defined for unreachable live edge endpoints vs mock fallback? [Coverage, Spec §Edge Cases]

## Edge Case Coverage

- [ ] CHK032 - Are requirements defined for inject_request with invalid hex_offset at schema validation level? [Edge Case, Data Model §VR-001]
- [ ] CHK033 - Are requirements defined for telemetry_event with missing or malformed raw_data? [Edge Case, Gap]
- [ ] CHK034 - Are requirements defined when mock bridge is used but live URL is also set? [Edge Case, Gap]
- [ ] CHK035 - Is continuous streaming (architecture) vs single sample (SC-006) scope boundary documented? [Edge Case, Architecture §2.3 vs Spec §SC-006]

## Non-Functional Requirements

- [ ] CHK036 - Are requirements explicit that no runtime validation library is required in libs/protocol for this feature? [Non-Functional, Spec §FR-011]
- [ ] CHK037 - Are JSON Schema Draft 2020-12 format requirements documented for protocol stubs? [Non-Functional, Data Model §ProtocolSchemaStub]
- [ ] CHK038 - Are protocol schema versioning or evolution requirements defined or intentionally deferred? [Non-Functional, Gap]

## Dependencies & Assumptions

- [ ] CHK039 - Are dependencies on architecture.md payload shapes documented in spec or plan? [Dependency, Architecture §2]
- [ ] CHK040 - Is the assumption of JSON-over-WebSockets for future live bridge documented in requirements? [Assumption, Architecture §2]
- [ ] CHK041 - Are edge daemon implementation dependencies explicitly out of scope while protocol stubs are in scope? [Dependency, Spec §Out of Scope]

## Ambiguities & Conflicts

- [ ] CHK042 - Is "mock WebSocket client" terminology consistent with in-process mock (no real network) in requirements? [Ambiguity, Spec §Clarifications]
- [ ] CHK043 - Are error_message nullability requirements consistent between architecture example and inject_response schema? [Consistency, Architecture §2.2]
- [ ] CHK044 - Is additionalProperties restriction on protocol schemas required and documented? [Clarity, Contract schemas]

## Notes

- Schema file parity between specs/01-mcp-scaffolding/contracts/ and libs/protocol/ is a requirements consistency concern, not an implementation test
- See [security.md](./security.md) for bridge payload security boundary requirements
