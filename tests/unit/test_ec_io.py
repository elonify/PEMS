"""Ec_IO pure derivation unit tests."""

from __future__ import annotations

from pems.calculations.modules.ec_io import EcIoModule
from pems.domain.case_input import CaseInput


def test_price_format_real() -> None:
    case = CaseInput(
        price_escalator=0.0, equity_share_company_1=0.49, project_equity_total=1.0
    )
    r = EcIoModule().run(case)
    assert r.price_format == "Real"
    assert abs((r.equity_share_company_2 or 0) - 0.51) < 1e-12


def test_price_format_nominal() -> None:
    case = CaseInput(price_escalator=0.02)
    r = EcIoModule().run(case)
    assert r.price_format == "Nominal"


def test_equity_derived() -> None:
    case = CaseInput(equity_share_company_1=0.49, project_equity_total=1.0)
    r = EcIoModule().run(case)
    assert abs((r.equity_share_company_2 or 0) - 0.51) < 1e-12


def test_timeline_helpers() -> None:
    case = CaseInput(project_start_year=2027, project_life_years=15)
    r = EcIoModule().run(case)
    assert r.history_end_year_e28 == 2026
    assert r.forecast_anchor_d29 == 2027
    assert r.project_end_year_e29 == 2042


def test_field_defaults() -> None:
    case = CaseInput(block_field_oil="Ebiya Field")
    r = EcIoModule().run(case)
    assert r.block_field_gas_effective == "Ebiya Field"
    assert r.cost_mode_field_effective == "Ebiya Field"


def test_cell_map_keys() -> None:
    case = CaseInput(
        equity_share_company_1=0.49,
        project_equity_total=1.0,
        project_start_year=2027,
        price_escalator=0.0,
        block_field_oil="Ebiya Field",
    )
    r = EcIoModule().run(case)
    m = r.cell_map()
    assert m[("Ec_IO", "C13")] == "Real"
    assert m[("Equity Dash", "C5")] == 0.51
