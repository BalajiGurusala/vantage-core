"""Edge bridge interface and JSON-over-WebSockets payload models.

This module defines the abstraction the MCP server uses to talk to the edge
daemon, plus typed models mirroring the shared protocol schemas in
`libs/protocol/`. Only the interface and payload shapes live here; the live
WebSocket client is out of scope for the scaffold (see `mock_client.py`).

Security boundary (FR-009): bridge payloads carry raw hex offsets only. Symbol
names and other human-readable identifiers MUST NOT appear in any payload.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Callable, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field


class ProbeType(str, Enum):
    """eBPF probe attachment type."""

    UPROBE = "uprobe"
    KPROBE = "kprobe"


class TelemetryFormat(str, Enum):
    """Requested shape of telemetry emitted by a probe."""

    LATENCY_HISTOGRAM = "latency_histogram"
    COUNTER = "counter"
    RAW = "raw"


class InjectStatus(str, Enum):
    """Outcome reported by the edge daemon for an injection attempt."""

    SUCCESS = "success"
    ERROR = "error"


class BridgeConnectionState(str, Enum):
    """Connection state of an :class:`EdgeBridge` implementation."""

    MOCK = "mock"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


class InjectRequestPayload(BaseModel):
    """Body of an ``inject_request`` bridge message (hex-only, no symbols)."""

    model_config = ConfigDict(extra="forbid")

    target_binary_path: str = Field(min_length=1)
    hex_offset: str = Field(pattern=r"^0x[0-9A-Fa-f]+$")
    probe_type: ProbeType
    telemetry_format: TelemetryFormat


class InjectRequest(BaseModel):
    """MCP -> Edge command to attach an eBPF probe."""

    model_config = ConfigDict(extra="forbid")

    message_type: Literal["inject_request"] = "inject_request"
    payload: InjectRequestPayload


class InjectResponsePayload(BaseModel):
    """Body of an ``inject_response`` bridge message."""

    model_config = ConfigDict(extra="forbid")

    status: InjectStatus
    probe_id: str = Field(min_length=1)
    error_message: str | None = None


class InjectResponse(BaseModel):
    """Edge -> MCP acknowledgment of an injection attempt."""

    model_config = ConfigDict(extra="forbid")

    message_type: Literal["inject_response"] = "inject_response"
    payload: InjectResponsePayload


class TelemetryEventPayload(BaseModel):
    """Body of a ``telemetry_event`` bridge message.

    ``raw_data`` is opaque telemetry. Per FR-009 it MUST NOT contain
    human-readable symbol or function names.
    """

    model_config = ConfigDict(extra="forbid")

    probe_id: str = Field(min_length=1)
    timestamp_ns: int = Field(ge=1)
    raw_data: dict[str, Any]


class TelemetryEvent(BaseModel):
    """Edge -> MCP streamed telemetry sample for an active probe."""

    model_config = ConfigDict(extra="forbid")

    message_type: Literal["telemetry_event"] = "telemetry_event"
    payload: TelemetryEventPayload


TelemetryHandler = Callable[[TelemetryEvent], None]


@runtime_checkable
class EdgeBridge(Protocol):
    """Abstraction for MCP -> Edge communication.

    Implementations: :class:`~vantage_mcp.bridge.mock_client.MockEdgeBridge`
    (scaffold default). A live WebSocket client is reserved for a future feature.
    """

    @property
    def connection_state(self) -> BridgeConnectionState:
        """Current connection state of the bridge."""
        ...

    def set_telemetry_handler(self, handler: TelemetryHandler | None) -> None:
        """Register a callback invoked for each emitted telemetry event."""
        ...

    def send_inject_request(self, request: InjectRequest) -> InjectResponse:
        """Send a probe-injection command and return the edge acknowledgment."""
        ...
