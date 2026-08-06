"""Presentation projection layer (Phase 1H first slice).

Consumes RunBundle from application services. No economic re-calculation.
"""

from pems.presentation import charts
from pems.presentation.formats import (
    format_money_mm,
    format_percent,
    is_unavailable,
)
from pems.presentation.view_models import PresentationBundle, build_presentation

__all__ = [
    "PresentationBundle",
    "build_presentation",
    "charts",
    "format_money_mm",
    "format_percent",
    "is_unavailable",
]

PRESENTATION_FIRST_SLICE = True
