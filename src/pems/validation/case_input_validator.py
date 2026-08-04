"""Validate CaseInput — single path for manual and import.

Rules from EC_IO_PARAMETER_CONTRACT §5 / INPUT_SCHEMA_CRITICAL_PATH.
"""

from __future__ import annotations

import math
from typing import Iterable

from pems.core.exceptions import ValidationError
from pems.domain.case_input import CaseInput

ASSET_ANALYSIS_TYPES = frozenset({"History", "Forecast", "Complete"})
PFS_CONTRACT_TYPES = frozenset({"R/T (SR)", "PSC/SC"})
PP_MODES = frozenset({"STOIIP", "GIIP"})


def _finite_number(name: str, value: object, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        errors.append(f"{name}: must be numeric")
        return
    if not math.isfinite(float(value)):
        errors.append(f"{name}: must be finite")


def _year(name: str, value: object, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, int) or isinstance(value, bool):
        # allow float years that are whole
        if isinstance(value, float) and value.is_integer():
            return
        errors.append(f"{name}: must be integer year")
        return
    if value < 1900 or value > 2200:
        errors.append(f"{name}: year out of plausible range [1900,2200]")


def validate_case_input(
    case: CaseInput,
    *,
    strict: bool = False,
    require_fields: Iterable[str] | None = None,
) -> list[str]:
    """Return validation messages (empty = ok for non-strict)."""
    errors: list[str] = []

    for name in (
        "equity_share_company_1",
        "project_equity_total",
        "production_days_per_year",
        "oil_price_usd_bbl",
        "price_escalator",
        "hurdle_rate",
        "gas_price_usd_mscf",
        "gas_flare_penalty_usd_mscf",
        "dom_gas_fraction",
        "duties_rate",
        "vat_rate",
        "asset_salvage_frac_of_retention",
        "nag_crl",
        "nag_ita",
        "nag_min_tax_rate",
        "nag_cpr",
        "project_life_years",
        "stoiip_inplace",
        "giip_inplace",
        "oil_rf",
        "gas_rf",
        "gor_scf_bbl",
        "prod_start_lag_years",
        "pp_days_in_year",
        "eff_decline_rate",
        "qi_buildup",
        "qp_plateau",
        "qel_end",
        "t1_buildup_yrs",
        "t2_plateau_yrs",
        "gas_boe_factor",
        "analysis_oil_scale",
        "analysis_gas_scale",
    ):
        _finite_number(name, getattr(case, name), errors)

    for name in ("project_start_year", "history_year", "complete_year", "year_end_anchor"):
        _year(name, getattr(case, name), errors)

    if case.asset_analysis_type is not None:
        if case.asset_analysis_type not in ASSET_ANALYSIS_TYPES:
            errors.append(
                f"asset_analysis_type: must be one of {sorted(ASSET_ANALYSIS_TYPES)}"
            )

    if case.pfs_contract_type is not None:
        if case.pfs_contract_type not in PFS_CONTRACT_TYPES:
            errors.append(
                f"pfs_contract_type: must be one of {sorted(PFS_CONTRACT_TYPES)}"
            )

    if case.pp_mode is not None and case.pp_mode not in PP_MODES:
        errors.append(f"pp_mode: must be one of {sorted(PP_MODES)}")

    if case.production_days_per_year is not None and case.production_days_per_year <= 0:
        errors.append("production_days_per_year: must be > 0")

    if case.pp_days_in_year is not None and case.pp_days_in_year <= 0:
        errors.append("pp_days_in_year: must be > 0")

    for rf_name in ("oil_rf", "gas_rf"):
        v = getattr(case, rf_name)
        if v is not None and (float(v) < 0 or float(v) > 1):
            errors.append(f"{rf_name}: outside [0,1]")

    # Suggested equity bounds (not workbook-enforced) — warn only in messages as soft
    if case.equity_share_company_1 is not None:
        e = float(case.equity_share_company_1)
        if e < 0 or e > 1:
            errors.append(
                "equity_share_company_1: outside [0,1] (workbook does not enforce; flagged)"
            )

    if require_fields:
        for f in require_fields:
            if getattr(case, f, None) is None:
                errors.append(f"{f}: required")

    if strict:
        if not case.is_complete_for_gtc001():
            errors.append("CaseInput incomplete for GTC-001 baseline (strict)")
        if errors:
            raise ValidationError("; ".join(errors))

    return errors
