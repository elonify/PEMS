"""Results packaging DTOs — structure only.

See docs/02_SPECIFICATIONS/modules/RESULTS_PARAMETER_CONTRACT.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MetricValue:
    """Single KPI with optional expected-error semantics."""

    name: str
    value: float | str | None
    unit: str | None = None
    gm_cell: str | None = None
    # e.g. NO_VALID_IRR when matching Project_NCF!AU14
    semantic_status: str | None = None


@dataclass
class ResultsPackage:
    """KPI package for dashboard / GTC compare (not yet populated by calc)."""

    metrics: list[MetricValue] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    extras: dict[str, Any] = field(default_factory=dict)
