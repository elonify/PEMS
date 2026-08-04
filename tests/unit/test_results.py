"""RESULTS unit tests — Phase 1F groups T01–T08 (algebra / policy)."""

from __future__ import annotations

from pems.calculations.modules.cr_ncf import CrNcfModule, excel_irr
from pems.calculations.modules.results import (
    ResultsModule,
    _equity_share_text,
    _gas_bscf_text,
)
from pems.domain.manual_input import case_input_from_mapping


def _minimal_case(**overrides):
    base = {
        "country": "Nigeria",
        "fiscal_regime_label": "PIA 2021",
        "pfs_contract_type": "PSC/SC",
        "block_field_oil": "Ebiya Field",
        "licence_lease_status": "New Acreage",
        "terrain": "Shallow Water (<200m water depth)",
        "equity_share_company_1": 0.49,
        "hurdle_rate": 0.15,
        "project_life_years": 15.0,
        "project_start_year": 2027,
    }
    base.update(overrides)
    return case_input_from_mapping(base)


class _FakeProd:
    oil_eur_or_max_cum = 21.99778945637469  # V47
    gas_max_cum = 25.245481844297494  # Y47
    gas_mmboe = 4.349669511422724  # Y49
    total_mmboe = 26.347458967797415  # Y50
    project_life_years = 15.0


class _FakeCosts:
    pv_opex_combined = 211.0028398270456
    pv_capex_combined = 142.90293416618726
    undisc_opex_combined = 418.20333035660326
    undisc_capex_combined = 175.0


class _FakeFlgt:
    w51 = 1099.8894728187345
    x51 = 55.03515042056853
    ab51 = 61.313817716951526
    ac51 = 1.3758787605142133
    ad51 = 0.0


class _FakeCr:
    equity_ag51 = 73.2829654000993
    equity_ah51 = 38.2636887228085
    ae51 = 310.69425355464
    af51 = 250.725376476001
    ad51 = 42.0829559477558
    aj51 = 5.13925728744526
    years = list(range(2024, 2069))
    contractor_af: dict

    def __init__(self) -> None:
        # simple sign-change series for AIT IRR unit path
        self.contractor_af = {y: 0.0 for y in self.years}
        self.contractor_af[2024] = -100.0
        self.contractor_af[2025] = 60.0
        self.contractor_af[2026] = 60.0
        self.contractor_af[2027] = 60.0


def test_t01_identity_fields() -> None:
    case = _minimal_case()
    r = ResultsModule().run(case)
    assert r.l2_country == "Nigeria"
    assert r.l3_regime == "PIA 2021"
    assert r.l5_pfs == "PSC/SC"
    assert r.c5_field == "Ebiya Field"
    assert r.c6_licence == "New Acreage"
    assert r.c7_terrain == "Shallow Water (<200m water depth)"
    assert r.c8_equity_text == "Equity Share =49%"
    assert r.h7_hurdle == 0.15


def test_t02_c4_equity_scaling() -> None:
    case = _minimal_case(equity_share_company_1=0.49)
    r = ResultsModule().run(
        case, upstream={"costs": _FakeCosts(), "flgt": _FakeFlgt(), "production": _FakeProd()}
    )
    assert abs(r.h16_pv_opex_eq - 211.0028398270456 * 0.49) < 1e-12
    assert abs(r.j16_oil_rev_eq - 1099.8894728187345 * 0.49) < 1e-12
    assert abs(r.h22_oil_royalty_eq - 61.313817716951526 * 0.49) < 1e-12
    assert abs(r.n22_oil_prod_eq - 21.99778945637469 * 0.49) < 1e-12


def test_t03_unit_cost_formula_order() -> None:
    case = _minimal_case(equity_share_company_1=0.49)
    r = ResultsModule().run(
        case, upstream={"costs": _FakeCosts(), "flgt": _FakeFlgt(), "production": _FakeProd()}
    )
    # Excel: H16/Y50/C4 == N16/Y50 when H16=N16*C4
    expected = 211.0028398270456 / 26.347458967797415
    assert abs(r.h19_unit_pv_opex - expected) < 1e-12
    assert abs(r.h19_unit_pv_opex - 8.00847019384067) < 1e-9


def test_t04_err() -> None:
    case = _minimal_case()
    r = ResultsModule().run(
        case, upstream={"costs": _FakeCosts(), "flgt": _FakeFlgt(), "production": _FakeProd()}
    )
    assert abs(r.h26_err - r.h25_total_royalty_eq / r.j18_gross_rev_eq) < 1e-15
    assert abs(r.h26_err - 0.0542803358903504) < 1e-9


def test_t05_take_ratios() -> None:
    case = _minimal_case()
    case.extras["ht_ncf_oil_equity_intermediates"] = {
        "AS51": 37.2107219837393,
        "AT51": 73.018201942495,
        "AO51": 20.6206484144003,
        "AQ51": 75.74179362915734,
        "AR51": 199.31741617728693,
        "AV51": 4.87387900694515,
        "AR": [[2024, -1.0], [2025, 2.0], [2026, 2.0]],
    }
    r = ResultsModule().run(case, upstream={"cr_ncf": _FakeCr()})
    assert abs(r.j13_disc_host_take_bit - 37.2107219837393 / (37.2107219837393 + 73.018201942495)) < 1e-12
    assert abs(r.k13_disc_contractor_take_bit - (1 - r.j13_disc_host_take_bit)) < 1e-15
    assert abs(r.m12_undisc_host_take_ait - 310.69425355464 / (310.69425355464 + 250.725376476001)) < 1e-12


def test_t06_pvr_pi_grr() -> None:
    case = _minimal_case()
    case.extras["ht_ncf_oil_equity_intermediates"] = {
        "AS51": 37.2107219837393,
        "AT51": 73.018201942495,
        "AO51": 20.62,
        "AQ51": 75.74,
        "AR51": 199.32,
        "AV51": 4.87,
        "AR": [[2024, -10.0], [2025, 20.0]],
    }
    r = ResultsModule().run(
        case,
        upstream={
            "costs": _FakeCosts(),
            "flgt": _FakeFlgt(),
            "production": _FakeProd(),
            "cr_ncf": _FakeCr(),
        },
    )
    assert abs(r.k9_pvr_bit - r.k7_contractor_npv_bit / r.h18_pv_tc_eq) < 1e-12
    assert abs(r.k10_pi_bit - (1 + r.k9_pvr_bit)) < 1e-15
    assert abs(r.k11_grr_bit - (r.k10_pi_bit ** (1 / 15) * 1.15 - 1)) < 1e-12


def test_t07_irr_numeric() -> None:
    case = _minimal_case()
    # series with known positive IRR
    case.extras["ht_ncf_oil_equity_intermediates"] = {
        "AS51": 1.0,
        "AT51": 1.0,
        "AO51": 0.0,
        "AQ51": 1.0,
        "AR51": 1.0,
        "AV51": 1.0,
        "AR": [[2024, -100.0], [2025, 60.0], [2026, 60.0], [2027, 60.0]],
    }
    r = ResultsModule().run(case, upstream={"cr_ncf": _FakeCr()})
    assert isinstance(r.k8_irr_bit, float)
    assert 0.3 < float(r.k8_irr_bit) < 0.4
    assert isinstance(r.n8_irr_ait, float)


def test_t08_no_valid_irr() -> None:
    assert excel_irr([1.0, 1.0, 1.0]) == "NO_VALID_IRR"
    case = _minimal_case()
    case.extras["ht_ncf_oil_equity_intermediates"] = {
        "AS51": 0.0,
        "AT51": 0.0,
        "AO51": 0.0,
        "AQ51": 0.0,
        "AR51": 0.0,
        "AV51": 0.0,
        "AR": [[2024, 1.0], [2025, 1.0], [2026, 1.0]],
    }
    cr = _FakeCr()
    cr.contractor_af = {y: 1.0 for y in cr.years}
    r = ResultsModule().run(case, upstream={"cr_ncf": cr})
    assert r.k8_irr_bit == "NO_VALID_IRR"
    assert r.n8_irr_ait == "NO_VALID_IRR"


def test_equity_share_text_helper() -> None:
    assert _equity_share_text(0.49) == "Equity Share =49%"
    assert _equity_share_text(1.0) == "Equity Share =100%"


def test_gas_bscf_text() -> None:
    assert _gas_bscf_text(25.245481844297494, 0.49) == "(12.37 Bscf)"


def test_bit_ait_distinction() -> None:
    case = _minimal_case()
    case.extras["ht_ncf_oil_equity_intermediates"] = {
        "AS51": 37.21,
        "AT51": 73.02,
        "AO51": 20.62,
        "AQ51": 75.74,
        "AR51": 199.32,
        "AV51": 4.87,
        "AR": [[2024, -1.0], [2025, 2.0]],
    }
    r = ResultsModule().run(case, upstream={"cr_ncf": _FakeCr()})
    assert r.j7_host_npv_bit != r.m7_host_npv_ait
    assert r.k7_contractor_npv_bit != r.n7_contractor_npv_ait
