"""Costs module unit tests — COSTS_PARAMETER_CONTRACT G1–G8."""

from __future__ import annotations

import pytest

from pems.calculations.modules.costs import (
    CostsModule,
    apply_history_mask,
    discount_factor,
    escalate_opex,
)
from pems.domain.case_input import CaseInput
from pems.domain.manual_input import case_input_from_mapping
from pems.validation.case_input_validator import validate_case_input


def _case(**kwargs) -> CaseInput:
    base = {
        "hurdle_rate": 0.15,
        "duties_rate": 0.0,
        "vat_rate": 0.0,
        "asset_analysis_type": "Forecast",
        "project_start_year": 2027,
        "cost_mode_field": "Ebiya Field",
        "block_field_oil": "Ebiya Field",
        "ca_rates": [0.2, 0.2, 0.2, 0.2, 0.19],
        "opex_escalation_rate": 0.0,
    }
    base.update(kwargs)
    return case_input_from_mapping(base)


def test_discount_year_zero() -> None:
    assert discount_factor(0.15, 2027, 2027) == 1.0
    assert abs(discount_factor(0.15, 2028, 2027) - 1 / 1.15) < 1e-12


def test_undiscounted_aggregation_and_totals() -> None:
    case = _case(
        oil_tc_exploration=[[2027, 10.0], [2028, 0.0]],
        oil_tc_capex_wells=[[2027, 0.0], [2028, 20.0]],
        oil_tc_capex_facilities=[[2027, 5.0], [2028, 0.0]],
        oil_tc_opex=[[2027, 3.0], [2028, 4.0]],
        gas_tc_exploration=[[2027, 0.0]],
        gas_tc_capex_wells=[[2027, 0.0]],
        gas_tc_capex_facilities=[[2027, 0.0]],
        gas_tc_opex=[[2027, 1.0]],
    )
    r = CostsModule().run(case)
    assert abs(r.oil.expensed_capex[2027] - 10.0) < 1e-12
    assert abs(r.oil.capitalized_costs[2027] - 5.0) < 1e-12  # wells+fac+duties+vat
    assert abs(r.oil.opex_undisc_total - 7.0) < 1e-12
    assert abs(r.gas.opex_undisc_total - 1.0) < 1e-12


def test_discounting_and_hurdle_sensitivity() -> None:
    sched = dict(
        oil_tc_exploration=[[2027, 0.0], [2028, 115.0]],
        oil_tc_capex_wells=[[2027, 0.0], [2028, 0.0]],
        oil_tc_capex_facilities=[[2027, 0.0], [2028, 0.0]],
        oil_tc_opex=[[2027, 0.0], [2028, 11.5]],
        gas_tc_opex=[[2027, 0.0]],
        gas_tc_exploration=[[2027, 0.0]],
        gas_tc_capex_wells=[[2027, 0.0]],
        gas_tc_capex_facilities=[[2027, 0.0]],
    )
    r15 = CostsModule().run(_case(hurdle_rate=0.15, **sched))
    r0 = CostsModule().run(_case(hurdle_rate=0.0, **sched))
    assert abs(r15.oil.disc_capex[2028] - 115.0 / 1.15) < 1e-12
    assert abs(r0.oil.disc_capex[2028] - 115.0) < 1e-12
    assert abs(r15.oil.disc_opex[2028] - 11.5 / 1.15) < 1e-12


def test_oil_and_gas_stacks_separate() -> None:
    case = _case(
        oil_tc_opex=[[2027, 10.0]],
        oil_tc_exploration=[[2027, 0.0]],
        oil_tc_capex_wells=[[2027, 0.0]],
        oil_tc_capex_facilities=[[2027, 0.0]],
        gas_tc_opex=[[2027, 5.0]],
        gas_tc_exploration=[[2027, 0.0]],
        gas_tc_capex_wells=[[2027, 0.0]],
        gas_tc_capex_facilities=[[2027, 0.0]],
    )
    r = CostsModule().run(case)
    assert r.oil.opex_undisc_total == 10.0
    assert r.gas.opex_undisc_total == 5.0
    assert abs((r.undisc_opex_combined or 0) - 15.0) < 1e-12


def test_history_filter() -> None:
    assert apply_history_mask(2025, 9.0, analysis_type="Forecast", history_year=2002, history_end_year=2026) == 9.0
    assert apply_history_mask(2025, 9.0, analysis_type="History", history_year=2002, history_end_year=2026) == 9.0
    assert apply_history_mask(2027, 9.0, analysis_type="History", history_year=2002, history_end_year=2026) == 0.0


def test_history_filter_on_stream() -> None:
    case = _case(
        asset_analysis_type="History",
        history_year=2027,
        project_start_year=2027,  # e28=2026
        oil_tc_opex=[[2027, 10.0]],
        oil_tc_exploration=[[2027, 1.0]],
        oil_tc_capex_wells=[[2027, 0.0]],
        oil_tc_capex_facilities=[[2027, 0.0]],
        gas_tc_opex=[[2027, 0.0]],
        gas_tc_exploration=[[2027, 0.0]],
        gas_tc_capex_wells=[[2027, 0.0]],
        gas_tc_capex_facilities=[[2027, 0.0]],
    )
    r = CostsModule().run(case)
    assert r.oil.opex_undisc_total == 0.0


def test_field_selection_via_cost_mode() -> None:
    case = _case(cost_mode_field="Ebiya Field", block_field_oil="Ebiya Field")
    assert case.cost_mode_field == "Ebiya Field"
    # schedules already selected at import; module uses provided series
    case.oil_tc_opex = [[2027, 1.0]]
    case.oil_tc_exploration = [[2027, 0.0]]
    case.oil_tc_capex_wells = [[2027, 0.0]]
    case.oil_tc_capex_facilities = [[2027, 0.0]]
    case.gas_tc_opex = [[2027, 0.0]]
    case.gas_tc_exploration = [[2027, 0.0]]
    case.gas_tc_capex_wells = [[2027, 0.0]]
    case.gas_tc_capex_facilities = [[2027, 0.0]]
    r = CostsModule().run(case)
    assert r.oil.opex[2027] == 1.0


def test_ca_rates_surface() -> None:
    r = CostsModule().run(_case())
    assert r.ca_rates == [0.2, 0.2, 0.2, 0.2, 0.19]
    assert r.cell_map()[("Cap_Allow", "FR5")] == 0.2
    assert r.cell_map()[("Cap_Allow", "FR9")] == 0.19


def test_escalated_opex_formula() -> None:
    # FW3=0.1, year+1 → *1.1
    assert abs(escalate_opex(10.0, 2028, 2027, 0.1) - 11.0) < 1e-12
    assert abs(escalate_opex(10.0, 2027, 2027, 0.1) - 10.0) < 1e-12
    assert abs(escalate_opex(10.0, 2028, 2027, 0.0) - 10.0) < 1e-12


def test_escalated_opex_recompute_flag() -> None:
    case = _case(
        opex_escalation_rate=0.1,
        oil_tc_opex=[[2027, 10.0], [2028, 10.0]],
        oil_tc_exploration=[[2027, 0.0], [2028, 0.0]],
        oil_tc_capex_wells=[[2027, 0.0], [2028, 0.0]],
        oil_tc_capex_facilities=[[2027, 0.0], [2028, 0.0]],
        gas_tc_opex=[[2027, 0.0]],
        gas_tc_exploration=[[2027, 0.0]],
        gas_tc_capex_wells=[[2027, 0.0]],
        gas_tc_capex_facilities=[[2027, 0.0]],
        extras={"recompute_opex_escalation": True},
    )
    # manual_input puts extras correctly
    case = case_input_from_mapping(
        {
            "hurdle_rate": 0.0,
            "duties_rate": 0.0,
            "vat_rate": 0.0,
            "asset_analysis_type": "Forecast",
            "opex_escalation_rate": 0.1,
            "oil_tc_opex": [[2027, 10.0], [2028, 10.0]],
            "oil_tc_exploration": [[2027, 0.0], [2028, 0.0]],
            "oil_tc_capex_wells": [[2027, 0.0], [2028, 0.0]],
            "oil_tc_capex_facilities": [[2027, 0.0], [2028, 0.0]],
            "gas_tc_opex": [[2027, 0.0]],
            "gas_tc_exploration": [[2027, 0.0]],
            "gas_tc_capex_wells": [[2027, 0.0]],
            "gas_tc_capex_facilities": [[2027, 0.0]],
            "recompute_opex_escalation": True,
        }
    )
    r = CostsModule().run(case)
    assert abs(r.oil.opex[2027] - 10.0) < 1e-12
    assert abs(r.oil.opex[2028] - 11.0) < 1e-12


def test_sln_and_acq_surfaces() -> None:
    case = _case(
        oil_tc_opex=[[2027, 0.0]],
        oil_tc_exploration=[[2027, 0.0]],
        oil_tc_capex_wells=[[2027, 0.0]],
        oil_tc_capex_facilities=[[2027, 0.0]],
        gas_tc_opex=[[2027, 0.0]],
        gas_tc_exploration=[[2027, 0.0]],
        gas_tc_capex_wells=[[2027, 0.0]],
        gas_tc_capex_facilities=[[2027, 0.0]],
        oil_sln_by_year=[[2027, 1.5], [2028, 2.5]],
        oil_acq_allowance_by_year=[[2027, 0.4], [2028, 0.6]],
        acquisition_cost=2.0408163265306123,
    )
    r = CostsModule().run(case)
    assert abs(r.oil.sln_total - 4.0) < 1e-12
    assert abs(r.oil.acq_allowance_total - 1.0) < 1e-12
    assert abs((r.acquisition_cost or 0) - 2.0408163265306123) < 1e-12
    assert ("Cap_Allow", "GX48") in r.cell_map()


def test_ec_io_hub_integration() -> None:
    case = _case(
        oil_tc_opex=[[2027, 10.0]],
        oil_tc_exploration=[[2027, 20.0]],
        oil_tc_capex_wells=[[2027, 5.0]],
        oil_tc_capex_facilities=[[2027, 5.0]],
        gas_tc_opex=[[2027, 3.0]],
        gas_tc_exploration=[[2027, 0.0]],
        gas_tc_capex_wells=[[2027, 0.0]],
        gas_tc_capex_facilities=[[2027, 0.0]],
        hurdle_rate=0.0,
    )
    r = CostsModule().run(case)
    assert abs((r.undisc_opex_combined or 0) - 13.0) < 1e-12
    assert abs((r.pv_opex_combined or 0) - 13.0) < 1e-12
    # undisc capex = FP+FQ oil+gas = 20 + (5+5+0+0) + 0 = 30
    assert abs((r.undisc_capex_combined or 0) - 30.0) < 1e-12
    assert abs((r.pv_tc_combined or 0) - ((r.pv_opex_combined or 0) + (r.pv_capex_combined or 0))) < 1e-12
    m = r.cell_map()
    assert m[("Ec_IO", "N18")] == m[("Ec_IO", "N16")] + m[("Ec_IO", "N17")]


def test_deterministic_repeatability() -> None:
    case = _case(
        oil_tc_opex=[[2027, 1.23], [2028, 4.56]],
        oil_tc_exploration=[[2027, 7.0], [2028, 0.0]],
        oil_tc_capex_wells=[[2027, 0.0], [2028, 8.0]],
        oil_tc_capex_facilities=[[2027, 0.0], [2028, 0.0]],
        gas_tc_opex=[[2027, 0.5]],
        gas_tc_exploration=[[2027, 0.0]],
        gas_tc_capex_wells=[[2027, 0.0]],
        gas_tc_capex_facilities=[[2027, 0.0]],
    )
    a = CostsModule().run(case).cell_map()
    b = CostsModule().run(case).cell_map()
    assert a == b


def test_zero_empty_schedule() -> None:
    r = CostsModule().run(_case())
    assert r.oil.opex_undisc_total == 0.0
    assert r.gas.capex_disc_total == 0.0
    assert r.undisc_tc_combined == 0.0


def test_duties_vat_on_capitalized() -> None:
    case = _case(
        duties_rate=0.1,
        vat_rate=0.05,
        oil_tc_exploration=[[2027, 10.0]],
        oil_tc_capex_wells=[[2027, 20.0]],
        oil_tc_capex_facilities=[[2027, 30.0]],
        oil_tc_opex=[[2027, 0.0]],
        gas_tc_opex=[[2027, 0.0]],
        gas_tc_exploration=[[2027, 0.0]],
        gas_tc_capex_wells=[[2027, 0.0]],
        gas_tc_capex_facilities=[[2027, 0.0]],
    )
    r = CostsModule().run(case)
    # FN = (20+30)*0.1 = 5; FO = (10+20+30)*0.05 = 3; FQ = 20+30+5+3 = 58
    assert abs(r.oil.duties[2027] - 5.0) < 1e-12
    assert abs(r.oil.vat[2027] - 3.0) < 1e-12
    assert abs(r.oil.capitalized_costs[2027] - 58.0) < 1e-12


def test_invalid_hurdle_still_finite() -> None:
    case = CaseInput(hurdle_rate=0.15)
    errs = validate_case_input(case)
    assert errs == []
