"""In-process mock edge bridge for scaffold testing.

``MockEdgeBridge`` simulates the edge daemon without any real network: it
acknowledges an ``inject_request`` with a successful ``inject_response`` and
emits a single ``telemetry_event`` sample via the registered telemetry handler
(SC-006). No live WebSocket is used even if ``VANTAGE_EDGE_WS_URL`` is set;
that variable is reserved for a future live-bridge feature.
"""

from __future__ import annotations

import secrets
import time

from vantage_mcp.bridge.interface import (
    BridgeConnectionState,
    EdgeBridge,
    InjectRequest,
    InjectResponse,
    InjectResponsePayload,
    InjectStatus,
    TelemetryEvent,
    TelemetryEventPayload,
    TelemetryHandler,
)


class MockEdgeBridge(EdgeBridge):
    """Deterministic-shape, in-process stand-in for the live edge daemon."""

    def __init__(self) -> None:
        self._telemetry_handler: TelemetryHandler | None = None
        self._last_request: InjectRequest | None = None

    @property
    def connection_state(self) -> BridgeConnectionState:
        return BridgeConnectionState.MOCK

    @property
    def last_request(self) -> InjectRequest | None:
        """The most recent request sent to the bridge (for inspection/tests)."""
        return self._last_request

    def set_telemetry_handler(self, handler: TelemetryHandler | None) -> None:
        self._telemetry_handler = handler

    def send_inject_request(self, request: InjectRequest) -> InjectResponse:
        """Simulate a probe injection: always succeeds, then emits telemetry.

        Handling of ``error`` status responses is deferred to the live
        edge-daemon feature (FR-012).
        """
        self._last_request = request
        probe_id = f"probe_mock_{secrets.token_hex(3)}"

        response = InjectResponse(
            payload=InjectResponsePayload(
                status=InjectStatus.SUCCESS,
                probe_id=probe_id,
                error_message=None,
            )
        )

        if self._telemetry_handler is not None:
            self._telemetry_handler(self._build_telemetry_sample(probe_id))

        return response

    @staticmethod
    def _build_telemetry_sample(probe_id: str) -> TelemetryEvent:
        return TelemetryEvent(
            payload=TelemetryEventPayload(
                probe_id=probe_id,
                timestamp_ns=time.time_ns(),
                raw_data={"execution_time_ns": 14500, "cpu_core": 1},
            )
        )
