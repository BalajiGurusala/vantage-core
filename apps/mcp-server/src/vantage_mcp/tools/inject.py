"""Placeholder ``inject_probe`` tool (uses the mock edge bridge).

Will command the edge daemon to attach an eBPF probe at a hex offset. In the
scaffold this is a placeholder at the MCP layer (``implemented: false``) that
drives the in-process mock bridge to demonstrate the future flow (FR-004 /
FR-012).

Security boundaries:
- Hex-only bridge payload (FR-009 / FR-014): only ``target_binary_path``,
  ``hex_offset``, ``probe_type``, ``telemetry_format`` cross the wire.
- Read-only probes (FR-013 / Architecture §3): probes are passive telemetry;
  the edge daemon rejects memory-writing eBPF. Documented here; enforced by the
  future edge daemon.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from vantage_mcp.bridge.interface import (
    EdgeBridge,
    InjectRequest,
    InjectRequestPayload,
    ProbeType,
    TelemetryEvent,
    TelemetryFormat,
)

_STUB_MESSAGE = (
    "Probe injection is not fully implemented. The mock bridge simulated the "
    "edge daemon response and a telemetry sample."
)


class InjectProbeRequest(BaseModel):
    """Input to ``inject_probe``."""

    model_config = ConfigDict(extra="forbid")

    target_binary_path: str = Field(min_length=1)
    hex_offset: str = Field(pattern=r"^0x[0-9A-Fa-f]+$")
    probe_type: ProbeType
    telemetry_format: TelemetryFormat


class InjectProbeResponse(BaseModel):
    """Stub output of ``inject_probe`` (populated from the mock bridge)."""

    model_config = ConfigDict(extra="forbid")

    implemented: bool = False
    message: str
    bridge_status: str
    probe_id: str
    telemetry_sample: TelemetryEvent | None = None


def inject_probe(request: InjectProbeRequest, bridge: EdgeBridge) -> InjectProbeResponse:
    """Drive the (mock) edge bridge and assemble the stub tool response.

    The bridge payload is constructed from hex/enum fields only — no symbol
    names — satisfying FR-009 / FR-014 (see VR-007 / SC-007).
    """
    captured: list[TelemetryEvent] = []
    bridge.set_telemetry_handler(captured.append)

    bridge_request = InjectRequest(
        payload=InjectRequestPayload(
            target_binary_path=request.target_binary_path,
            hex_offset=request.hex_offset,
            probe_type=request.probe_type,
            telemetry_format=request.telemetry_format,
        )
    )
    response = bridge.send_inject_request(bridge_request)

    return InjectProbeResponse(
        message=_STUB_MESSAGE,
        bridge_status=response.payload.status.value,
        probe_id=response.payload.probe_id,
        telemetry_sample=captured[0] if captured else None,
    )
