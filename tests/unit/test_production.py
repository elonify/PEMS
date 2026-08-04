"""Production module unit tests — PRODUCTION_PROFILE_CONTRACT G1–G5."""

from __future__ import annotations

import math

from pems.calculations.modules.production import ProductionModule
from pems.domain.case_input import CaseInput
from pems.domain.manual_input import case_input_from_mapping
from pems.validation.case_input_validator import validate_case_input


def _gtc_pp_case(**overrides) -> CaseInput:
    base = {
        "pp_mode": "STOIIP",
        "stoiip_inplace": 42.451776,
        "giip_inplace": 238.36032,
        "oil_rf": 0.35,
        "gas_rf": 0.75,
        "gor_scf_bbl": 2000.0,
        "prod_start_lag_years": 1.0,
        "year_end_anchor": 2026,
        "pp_days_in_year": 365.0,
        "eff_decline_rate": 0.125,
        "qi_buildup": 1000.0,
        "qp_plateau": 6000.0,
        "qel_end": 500.0,
        "t1_buildup_yrs": 2.0,
        "t2_plateau_yrs": 3.0,
        "project_start_year": 2027,
        "asset_analysis_type": "Forecast",
        "gas_boe_factor": 5.804,
        "production_days_per_year": 365.0,
    }
    base.update(overrides)
    return case_input_from_mapping(base)


def test_pp_mode_validation() -> None:
    case = CaseInput(pp_mode="BAD")
    errs = validate_case_input(case)
    assert any("pp_mode" in e for e in errs)


def test_oil_ur_g1() -> None:
    case = _gtc_pp_case()
    r = ProductionModule().run(case)
    assert r.oil_ur is not None
    assert abs(r.oil_ur - 14.8581216) < 1e-9
    assert abs((r.gas_ur or 0) - 178.77024) < 1e-9
    assert r.ur_target == r.oil_ur


def test_giip_mode_ur() -> None:
    case = _gtc_pp_case(pp_mode="GIIP")
    r = ProductionModule().run(case)
    assert r.oil_ur is not None
    assert abs(r.oil_ur - 178.77024) < 1e-9
    assert r.af21_stream_flag == "NAG"


def test_buildup_plateau_decline_design() -> None:
    case = _gtc_pp_case()
    r = ProductionModule().run(case)
    assert r.a1_buildup is not None
    assert abs(r.a1_buildup - math.log(1000 / 6000) / 2) < 1e-12
    assert abs((r.np2 or 0) - 6.57) < 1e-12
    assert abs((r.np1 or 0) - 2.0371037869120525) < 1e-9
    assert abs((r.np3 or 0) - 6.251017813087948) < 1e-9
    assert abs((r.a3_decline or 0) - 0.32114770106667034) < 1e-9
    assert abs((r.t3_decline_yrs or 0) - 7.737581933591774) < 1e-9
    assert abs((r.field_time_total or 0) - 13.737581933591773) < 1e-9


def test_pp_rate_buildup_plateau() -> None:
    case = _gtc_pp_case()
    r = ProductionModule().run(case)
    # lag=1 → 2026 rate 0; 2027 time=1 buildup
    assert r.pp_rate_by_year.get(2026, None) == 0.0
    # D at t=1: 1000*exp(-a1*0)/1000 wait c_t=1, lag=1: c_t>=lag and c_t < t1+lag → buildup at (1-1)=0
    # qi*exp(0)/1000 = 1.0
    assert abs(r.pp_rate_by_year[2027] - 1.0) < 1e-9
    # plateau years: t from 3 to 5 inclusive start: t1+lag=3 → 2029 is t=3 plateau start
    assert abs(r.pp_rate_by_year[2029] - 6.0) < 1e-9
    assert abs(r.pp_rate_by_year[2030] - 6.0) < 1e-9
    assert abs(r.pp_rate_by_year[2031] - 6.0) < 1e-9


def test_gor_associated_gas() -> None:
    case = _gtc_pp_case()
    r = ProductionModule().run(case)
    # G = D * 2000 / 1000 = 2*D
    assert abs(r.pp_ag_rate_by_year[2027] - 2.0) < 1e-9
    assert r.pp_ag_rate_by_year[2026] == 0.0


def test_gor_zero_in_giip_mode() -> None:
    case = _gtc_pp_case(pp_mode="GIIP")
    r = ProductionModule().run(case)
    assert all(v == 0.0 for v in r.pp_ag_rate_by_year.values())


def test_block_path_annualization_and_totals() -> None:
    # Simple two-year block series
    case = _gtc_pp_case(
        oil_block_daily=[[2027, 10.0], [2028, 10.0], [2029, 0.0]],
        oil_block_annual=[[2027, 3.6525], [2028, 3.6525], [2029, 0.0]],
        gas_block_daily=[[2027, 12.0], [2028, 12.0], [2029, 0.0]],
        gas_block_annual=[[2027, 4.38], [2028, 4.38], [2029, 0.0]],
        analysis_oil_scale=0.0,
        analysis_gas_scale=0.0,
    )
    r = ProductionModule().run(case)
    assert r.path_used == "block_selected"
    assert abs((r.oil_eur_or_max_cum or 0) - 7.305) < 1e-9
    assert abs((r.gas_max_cum or 0) - 8.76) < 1e-9
    assert r.project_life_years == 2.0
    assert abs((r.gas_mmboe or 0) - 8.76 / 5.804) < 1e-9
    assert abs((r.total_mmboe or 0) - (7.305 + 8.76 / 5.804)) < 1e-9


def test_history_filter_zeros_outside_window() -> None:
    case = _gtc_pp_case(
        asset_analysis_type="History",
        history_year=2027,
        project_start_year=2027,  # e28 = 2026 → all years > 2026 zeroed?
        # e28 = start-1 = 2026; year 2027 > 2026 → zero
        oil_block_daily=[[2027, 5.0]],
        oil_block_annual=[[2027, 1.0]],
        gas_block_daily=[[2027, 1.0]],
        gas_block_annual=[[2027, 0.5]],
    )
    r = ProductionModule().run(case)
    # S5=2027 > E28=2026 → history mask zero
    assert r.oil_daily_series.get(2027, 0) == 0.0


def test_start_lag_zeros_before_commencement() -> None:
    case = _gtc_pp_case()
    r = ProductionModule().run(case)
    assert r.pp_rate_by_year[2026] == 0.0


def test_ec_io_life_interface() -> None:
    case = _gtc_pp_case(
        oil_block_daily=[[2027 + i, 1.0 if i < 15 else 0.0] for i in range(20)],
        oil_block_annual=[[2027 + i, 0.1 if i < 15 else 0.0] for i in range(20)],
        gas_block_daily=[[2027 + i, 1.0 if i < 15 else 0.0] for i in range(20)],
        gas_block_annual=[[2027 + i, 0.1 if i < 15 else 0.0] for i in range(20)],
    )
    r = ProductionModule().run(case)
    assert r.project_life_years == 15.0
    assert r.cell_map()[("Ec_IO", "C6")] == 15.0
    assert r.cell_map()[("Prod_Summary", "AF26")] == 15.0


def test_field_selection_via_block_series() -> None:
    case = _gtc_pp_case(
        block_field_oil="Ebiya Field",
        oil_block_daily=[[2027, 1.0]],
        oil_block_annual=[[2027, 0.36525]],
        gas_block_daily=[[2027, 1.2]],
        gas_block_annual=[[2027, 0.0]],
    )
    r = ProductionModule().run(case)
    assert r.path_used == "block_selected"
    assert abs(r.oil_daily_series[2027] - 1.0) < 1e-12
