"""Placeholder ``resolve_dwarf_symbol`` tool.

Will resolve a symbol name to a hex offset via DWARF debug info. Not
implemented in the scaffold; returns an informative stub (FR-003 / FR-004).

Security (FR-009): ``symbol_name`` is MCP-side input only and MUST NOT be
forwarded to any edge bridge payload.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

_STUB_MESSAGE = (
    "DWARF symbol resolution is not yet implemented. This tool will parse DWARF "
    "debug info to compute hex offsets for the edge daemon."
)


class DwarfResolveRequest(BaseModel):
    """Input to ``resolve_dwarf_symbol``."""

    model_config = ConfigDict(extra="forbid")

    binary_path: str = Field(min_length=1)
    symbol_name: str = Field(min_length=1)


class DwarfResolveResponse(BaseModel):
    """Stub output of ``resolve_dwarf_symbol``."""

    model_config = ConfigDict(extra="forbid")

    implemented: bool = False
    message: str
    binary_path: str
    symbol_name: str


def resolve_dwarf_symbol(request: DwarfResolveRequest) -> DwarfResolveResponse:
    """Return a structured stub echoing the request (no real DWARF math)."""
    return DwarfResolveResponse(
        message=_STUB_MESSAGE,
        binary_path=request.binary_path,
        symbol_name=request.symbol_name,
    )
