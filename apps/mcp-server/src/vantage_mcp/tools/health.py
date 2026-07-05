"""Functional ``vantage_health`` tool.

Returns structured operational status for the MCP server (FR-002).
"""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field


class HealthStatus(BaseModel):
    """Output of the ``vantage_health`` tool."""

    model_config = ConfigDict(extra="forbid")

    status: str = Field(description="'ok' when the server is healthy")
    version: str = Field(description="Server package version (semver)")
    uptime_seconds: float = Field(ge=0.0)
    tools_registered: list[str] = Field(min_length=1)


def build_health_status(
    version: str,
    started_at: datetime,
    tools_registered: list[str],
) -> HealthStatus:
    """Compute the current :class:`HealthStatus`."""
    now = datetime.now(timezone.utc)
    uptime = max(0.0, (now - started_at).total_seconds())
    return HealthStatus(
        status="ok",
        version=version,
        uptime_seconds=uptime,
        tools_registered=list(tools_registered),
    )
