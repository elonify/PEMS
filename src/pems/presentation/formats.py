"""Presentation format transforms only — no economic calculations.

Authority: UNIT_AND_CURRENCY_SPECIFICATION, NUMBER_FORMAT_SPECIFICATION,
PHASE1H_PRESENTATION_READINESS §10–11.
"""

from __future__ import annotations

from typing import Any


UNAVAILABLE_TOKENS = frozenset(
    {
        "NO_VALID_IRR",
        "NO_SIGN_CHANGE",
        "#NUM!",
        "#DIV/0!",
        "#VALUE!",
        "UNAVAILABLE",
    }
)


def is_unavailable(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip().upper() in {t.upper() for t in UNAVAILABLE_TOKENS} or value.strip().startswith(
            "#"
        )
    return False


def format_percent(value: Any, decimals: int = 2) -> str:
    """Fraction 0–1 → percentage display. Never formats NO_VALID_IRR as 0%."""
    if is_unavailable(value):
        return "UNAVAILABLE"
    if value is None:
        return "—"
    try:
        f = float(value)
    except (TypeError, ValueError):
        return str(value)
    return f"{f * 100:.{decimals}f}%"


def format_money_mm(value: Any, decimals: int = 2) -> str:
    """$mm accounting-style display."""
    if is_unavailable(value):
        return "UNAVAILABLE"
    if value is None:
        return "—"
    try:
        f = float(value)
    except (TypeError, ValueError):
        return str(value)
    if abs(f) < 5e-13:
        return "—"
    if f < 0:
        return f"({abs(f):,.{decimals}f})"
    return f"{f:,.{decimals}f}"


def format_currency_usd(value: Any, decimals: int = 2) -> str:
    """Absolute $ (e.g. RESULTS unit costs / revenue lines)."""
    if is_unavailable(value):
        return "UNAVAILABLE"
    if value is None:
        return "—"
    try:
        f = float(value)
    except (TypeError, ValueError):
        return str(value)
    if abs(f) < 5e-13:
        return "—"
    if f < 0:
        return f"(${abs(f):,.{decimals}f})"
    return f"${f:,.{decimals}f}"


def format_number(value: Any, decimals: int = 2) -> str:
    if is_unavailable(value):
        return "UNAVAILABLE"
    if value is None:
        return "—"
    try:
        f = float(value)
    except (TypeError, ValueError):
        return str(value)
    return f"{f:,.{decimals}f}"


def format_years(value: Any, decimals: int = 2) -> str:
    if is_unavailable(value):
        return "UNAVAILABLE"
    if value is None:
        return "—"
    try:
        f = float(value)
    except (TypeError, ValueError):
        return str(value)
    return f"{f:.{decimals}f}"


def format_text(value: Any) -> str:
    if value is None:
        return "—"
    if is_unavailable(value):
        return "UNAVAILABLE"
    return str(value)
