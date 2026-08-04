"""Calculation engines — NOT IMPLEMENTED in Phase 0.

Implement only from docs/02_SPECIFICATIONS/modules/* and Golden Master catalogue.
Do not invent formulas.
"""

from pems.core.exceptions import NotImplementedCalculationError

__all__ = ["NotImplementedCalculationError", "run_pipeline"]


def run_pipeline(case_input):  # type: ignore[no-untyped-def]
    """Full economic pipeline. Phase 0: not implemented."""
    raise NotImplementedCalculationError(
        "Calculation pipeline not implemented. "
        "Implement modules in dependency order per SPECIFICATION_FREEZE_AUDIT."
    )
