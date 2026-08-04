"""Declared calculation dependency order (specification freeze).

Does not execute modules.
"""

from __future__ import annotations

# Order from module contracts / SPECIFICATION_FREEZE_AUDIT.md
MODULE_DEPENDENCY_ORDER: tuple[str, ...] = (
    "case_input",
    "fiscal_terms_pia",  # law table load
    "production",
    "costs",
    "flgt_royalties",
    "cr_ncf",
    "results",
)

# Presentation layer AFTER numerical validation of calc modules
PRESENTATION_AFTER_VALIDATION = True
