# Security Requirements Quality Checklist: MCP Server Scaffolding

**Purpose**: Validate completeness, clarity, and consistency of security-related requirements across spec, plan, contracts, and architecture — not implementation behavior
**Created**: 2026-07-04
**Reviewed**: 2026-07-04 (checklist review against spec/plan/data-model/contracts/architecture/constitution)
**Feature**: [spec.md](../spec.md)

## Requirement Completeness

- [x] CHK001 - Are no-symbol-transmission rules explicitly defined for all bridge message types (inject_request, inject_response, telemetry_event)? [Completeness, Spec §FR-009]
- [x] CHK002 - Are prohibited bridge payload fields (e.g., symbol names, function identifiers) enumerated or exemplified in requirements? [Completeness, Spec §FR-009]
- [x] CHK003 - Are MCP-side-only data fields (e.g., `symbol_name` on DWARF tool input) distinguished from bridge-transmitted fields in requirements? [Completeness, Gap]
- [x] CHK004 - Are local-development no-authentication requirements scoped to this feature only? [Completeness, Spec §FR-010]
- [x] CHK005 - Are deferred production authentication requirements explicitly listed in Out of Scope? [Completeness, Spec §Out of Scope]
- [x] CHK006 - Are read-only probe constraints from architecture referenced where inject_probe requirements are defined? [Completeness, Architecture §3] — Resolved: FR-013 + contract "Security & Scope Notes" reference architecture §3 read-only probe constraint.
- [x] CHK007 - Are requirements defined for what data MUST NOT cross the MCP-to-edge network boundary? [Completeness, Spec §FR-009]
- [x] CHK008 - Are security boundary requirements traceable from constitution through spec to contracts? [Completeness, Constitution §2]

## Requirement Clarity

- [x] CHK009 - Is "human-readable symbol names" defined with concrete prohibited examples in requirements? [Clarity, Spec §FR-009]
- [x] CHK010 - Is "raw hex offsets" format specified with validation pattern requirements (e.g., `0x` prefix)? [Clarity, Data Model §VR-001]
- [x] CHK011 - Is the trusted local environment assumption defined with explicit scope boundaries? [Clarity, Spec §Assumptions]
- [x] CHK012 - Are requirements clear that FR-010 applies to scaffold/local dev only, not production deployment? [Clarity, Spec §FR-010]
- [x] CHK013 - Is the security implication of stdio-only MCP transport documented in requirements? [Clarity, Spec §Clarifications] — Resolved: Assumptions now state stdio exposes no network listener, limiting attack surface to the local process (justifies FR-010).
- [x] CHK014 - Are requirements unambiguous about which tools may accept symbol names on the MCP channel? [Clarity, Contract §resolve_dwarf_symbol]

## Requirement Consistency

- [x] CHK015 - Do FR-009 security rules align with the DwarfResolveRequest security note in data-model? [Consistency, Data Model §DwarfResolveRequest]
- [x] CHK016 - Do inject_probe bridge payload requirements in contracts exclude symbol_name consistently with FR-009? [Consistency, Contract §inject_probe]
- [x] CHK017 - Are architecture §3 security boundaries consistent with spec FR-009 wording? [Consistency, Architecture §3]
- [x] CHK018 - Do Out of Scope auth exclusions conflict with FR-010 functional auth requirements? [Conflict, Spec §FR-010 vs Out of Scope]
- [x] CHK019 - Are mock bridge security requirements consistent with live WebSocket requirements for hex-only payloads? [Consistency, Spec §Clarifications]
- [x] CHK020 - Do plan.md security constraints align with spec FR-009 and FR-010 without contradiction? [Consistency, Plan §Technical Context]

## Acceptance Criteria Quality

- [x] CHK021 - Can FR-009 compliance be objectively assessed from written requirements and contract schemas alone? [Measurability, Spec §FR-009]
- [x] CHK022 - Does SC-006 define mock bridge behavior in terms that preserve security boundary requirements? [Measurability, Spec §SC-006]
- [x] CHK023 - Are success criteria free of security assumptions that contradict Out of Scope auth deferral? [Measurability, Spec §SC-001–SC-006]
- [x] CHK024 - Is there a measurable requirement linking inject_probe tool output to hex-only bridge payloads? [Measurability, Gap] — Resolved: FR-014 + SC-007 + data-model VR-007 define a verifiable hex-only bridge-payload criterion.

## Scenario Coverage

- [x] CHK025 - Are primary-flow security requirements defined for resolve_dwarf_symbol (MCP input vs bridge output)? [Coverage, User Story 2]
- [x] CHK026 - Are primary-flow security requirements defined for inject_probe bridge payload composition? [Coverage, Spec §FR-012]
- [x] CHK027 - Are exception-flow requirements defined when invalid hex offsets are submitted (no silent bridge transmission)? [Coverage, Spec §FR-005] — Resolved: FR-005 now states invalid input MUST be rejected before any bridge payload is emitted.
- [x] CHK028 - Are alternate-flow requirements defined for optional live edge connection vs mock-only mode? [Coverage, Spec §Clarifications]
- [x] CHK029 - Are recovery requirements defined if live edge endpoint is unreachable (mock fallback without security regression)? [Coverage, Spec §Edge Cases]

## Edge Case Coverage

- [x] CHK030 - Are security requirements defined for concurrent MCP clients accessing tools that handle sensitive inputs? [Edge Case, Spec §Edge Cases]
- [x] CHK031 - Are requirements defined for MCP client disconnect during tool invocation (no partial bridge leakage)? [Edge Case, Gap] — Resolved (deferred with rationale): Out of Scope now explicitly defers partial/aborted bridge-transmission handling (no live bridge; in-process mock completes synchronously).
- [x] CHK032 - Are requirements defined for startup failures involving security-related configuration? [Edge Case, User Story 1 scenario 3]
- [x] CHK033 - Are edge cases where placeholder tools echo symbol names in MCP responses distinguished from bridge transmission rules? [Edge Case, Data Model §DwarfResolveResponse]

## Non-Functional Requirements (Security)

- [x] CHK034 - Are threat assumptions for unauthenticated local MCP documented or explicitly deferred? [Non-Functional, Spec §Assumptions]
- [x] CHK035 - Are data protection requirements defined for symbol names held in MCP tool inputs? [Non-Functional, Gap] — Resolved (deferred with rationale): Assumptions now explicitly defer MCP-side symbol-name data protection under the trusted-local assumption; only the bridge no-symbol rule (FR-009) is enforced.
- [x] CHK036 - Are requirements aligned with constitution boundary rules (no shared runtime code across nodes)? [Non-Functional, Constitution §2]

## Dependencies & Assumptions

- [x] CHK037 - Is the assumption of trusted local development validated against documented threat scenarios? [Assumption, Spec §Assumptions] — Resolved (deferred with rationale): Assumptions now state a formal threat model is out of scope for the scaffold; trusted-local stands in until a production-hardening feature is specified.
- [x] CHK038 - Are dependencies on architecture.md security boundaries explicitly referenced in spec requirements? [Dependency, Architecture §3]
- [x] CHK039 - Are future production-hardening security requirements explicitly excluded with rationale? [Assumption, Spec §Out of Scope]

## Ambiguities & Conflicts

- [x] CHK040 - Is the term "network bridge" unambiguously scoped to MCP-to-edge WebSocket payloads (not MCP stdio)? [Ambiguity, Spec §FR-009]
- [x] CHK041 - Are there conflicting statements about auth being both required (Out of Scope exclusion) and absent (FR-010)? [Conflict, Spec §FR-010]
- [x] CHK042 - Is it clear whether telemetry_event payloads may contain human-readable strings in raw_data? [Ambiguity, Architecture §2.3] — Resolved: FR-009 + data-model TelemetryEvent now state `raw_data` MUST NOT contain human-readable symbol/function names.

## Notes

- Items validate requirement writing quality only; checking boxes does not substitute for implementation security review
- Cross-reference [requirements.md](./requirements.md) for general spec quality (separate checklist)
- **Review result (2026-07-04)**: 42/42 pass after remediation. 4 fixed via new requirements (CHK006→FR-013, CHK024→FR-014/SC-007/VR-007, CHK027→FR-005, CHK042→FR-009); 4 resolved by explicit deferral rationale in spec (CHK013, CHK031, CHK035, CHK037).
