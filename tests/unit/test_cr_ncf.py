"""CR/NCF unit tests — Phase 1E groups."""

from __future__ import annotations

from pems.calculations.modules.cr_ncf import (
    CrNcfModule,
    excel_irr,
    profit_oil_hg_split,
)
from pems.domain.manual_input import case_input_from_mapping


def test_excel_irr_valid() -> None:
    # classic textbook-ish series
    r = excel_irr([-100.0, 60.0, 60.0, 60.0])
    assert isinstance(r, float)
    assert 0.3 < r < 0.4


def test_excel_irr_no_sign_change() -> None:
    assert excel_irr([0.0, 0.0, 0.0, 0.0]) == "NO_VALID_IRR"
    assert excel_irr([1.0, 1.0, 1.0]) == "NO_VALID_IRR"
    assert excel_irr([-1.0, -1.0]) == "NO_VALID_IRR"


def test_profit_oil_split_zero() -> None:
    assert profit_oil_hg_split(0.0, [50, 100, 250, 750, 1500], [0.05, 0.1, 0.15, 0.25, 0.35, 0.45]) == 0.0


def test_cr_bridge_basic() -> None:
    from pems.calculations.modules.flgt_royalties import FlgtRoyaltiesModule
    from pems.calculations.modules.production import ProductionModule
    from pems.calculations.modules.costs import CostsModule

    case = case_input_from_mapping(
        {
            "licence_lease_status": "New Acreage",
            "pfs_contract_type": "PSC/SC",
            "hurdle_rate": 0.15,
            "project_start_year": 2027,
            "equity_share_company_1": 0.49,
            "project_equity_total": 1.0,
            "oil_block_daily": [[2027, 1.0]],
            "oil_block_annual": [[2027, 0.36525]],
            "gas_block_daily": [[2027, 0.0]],
            "gas_block_annual": [[2027, 0.0]],
            "oil_tc_opex": [[2027, 15.23]],
            "oil_tc_exploration": [[2027, 0.0]],
            "oil_tc_capex_wells": [[2027, 0.0]],
            "oil_tc_capex_facilities": [[2027, 0.0]],
            "gas_tc_opex": [[2027, 0.0]],
            "gas_tc_exploration": [[2027, 0.0]],
            "gas_tc_capex_wells": [[2027, 0.0]],
            "gas_tc_capex_facilities": [[2027, 0.0]],
            "oil_sln_by_year": [[2027, 0.0]],
            "oil_acq_allowance_by_year": [[2027, 0.40816326530612246]],
            "terrain": "Shallow Water (<200m water depth)",
            "gas_utilization": "In-Country (Dom Gas)",
            "oil_price_usd_bbl": 50.0,
            "gas_price_usd_mscf": 2.18,
            "price_escalator": 0.0,
            "price_path_end_year": 2042,
        }
    )
    prod = ProductionModule().run(case)
    costs = CostsModule().run(case)
    flgt = FlgtRoyaltiesModule().run(case, upstream={"production": prod})
    # minimal project intermediates for one year
    case.extras["project_ncf_intermediates"] = {
        "A": [[2027, 2027]],
        "B": [[2027, flgt.total_revenue.get(2027, 0)]],
        "E": [[2027, 0]],
        "F": [[2027, 0]],
        "G": [[2027, 0]],
        "H": [[2027, 0]],
        "I": [[2027, 0]],
        "J": [[2027, 0]],
        "O": [[2027, 0]],
        "P": [[2027, 0]],
        "Q": [[2027, 0]],
        "R": [[2027, 0]],
        "W": [[2027, 0]],
        "X": [[2027, 0]],
        "AB": [[2027, 0]],
        "AC": [[2027, 0]],
        "AD": [[2027, 0]],
        "AK": [[2027, 0]],
    }
    case.extras["price_path_end_year"] = 2042
    r = CrNcfModule().run(case, upstream={"production": prod, "costs": costs, "flgt": flgt})
    assert r.cr_years
    assert r.cr_years[0].crl == 0.7 * (r.cr_years[0].total_rev - r.cr_years[0].royalties)
    assert r.au14_irr == "NO_VALID_IRR"  # zero AK series


def test_equity_scale() -> None:
    case = case_input_from_mapping(
        {
            "hurdle_rate": 0.0,
            "project_start_year": 2027,
            "equity_share_company_1": 0.5,
            "price_path_end_year": 2042,
            "licence_lease_status": "New Acreage",
            "pfs_contract_type": "PSC/SC",
        }
    )
    case.extras["project_ncf_intermediates"] = {
        "A": [[2027, 2027], [2028, 2028]],
        "B": [[2027, 100.0], [2028, 100.0]],
        "E": [[2027, 0], [2028, 0]],
        "F": [[2027, 10], [2028, 10]],
        "G": [[2027, 0], [2028, 0]],
        "H": [[2027, 0], [2028, 0]],
        "I": [[2027, 0], [2028, 0]],
        "J": [[2027, 0], [2028, 0]],
        "O": [[2027, 0], [2028, 0]],
        "P": [[2027, 0], [2028, 0]],
        "Q": [[2027, 0], [2028, 0]],
        "R": [[2027, 0], [2028, 0]],
        "W": [[2027, 0], [2028, 0]],
        "X": [[2027, 0], [2028, 0]],
        "AB": [[2027, 5], [2028, 5]],
        "AC": [[2027, 0], [2028, 0]],
        "AD": [[2027, 0], [2028, 0]],
        "AK": [[2027, 0], [2028, 0]],
    }
    case.extras["price_path_end_year"] = 2042
    r = CrNcfModule().run(case)
    assert abs(r.equity_ag51 - 0.5 * r.ag51) < 1e-12
    assert abs(r.equity_ah51 - 0.5 * r.ah51) < 1e-12


def test_equity_af_dncf_maps_slice_a() -> None:
    """Slice A: equity AF = project AF × share; AH = eAF/DF; AI uses strict < D22."""
    case = case_input_from_mapping(
        {
            "hurdle_rate": 0.10,
            "project_start_year": 2027,
            "equity_share_company_1": 0.5,
            "price_path_end_year": 2029,  # D22 = 2029
            "licence_lease_status": "New Acreage",
            "pfs_contract_type": "PSC/SC",
        }
    )
    # Years 2027, 2028, 2029, 2030 — D22=2029 so AI zero at 2029+
    case.extras["project_ncf_intermediates"] = {
        "A": [[2027, 2027], [2028, 2028], [2029, 2029], [2030, 2030]],
        "B": [[2027, 100.0], [2028, 100.0], [2029, 100.0], [2030, 100.0]],
        "E": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "F": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "G": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "H": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "I": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "J": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "O": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "P": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "Q": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "R": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "W": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "X": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "AB": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "AC": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "AD": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
        "AK": [[2027, 0], [2028, 0], [2029, 0], [2030, 0]],
    }
    case.extras["price_path_end_year"] = 2029
    r = CrNcfModule().run(case)
    share = 0.5
    d22 = 2029
    start = 2027
    hurdle = 0.10

    assert set(r.equity_contractor_af) == set(r.contractor_af)
    run = 0.0
    for y in r.years:
        eaf = r.contractor_af[y] * share
        assert abs(r.equity_contractor_af[y] - eaf) < 1e-12
        gate = y <= d22
        df = (1.0 + hurdle) ** (y - start) if gate else 1.0
        edncf = eaf / df if df else 0.0
        assert abs(r.equity_dncf_by_year[y] - edncf) < 1e-12
        run += edncf
        expected_cum = run if y < d22 else 0.0
        assert abs(r.equity_cum_dncf_by_year[y] - expected_cum) < 1e-12, (y, r.equity_cum_dncf_by_year[y], expected_cum)

    # Strict < D22: cumulative present for years before end, zero at D22 and after
    assert r.equity_cum_dncf_by_year[2028] != 0.0 or r.equity_dncf_by_year[2027] == 0.0
    assert r.equity_cum_dncf_by_year[2029] == 0.0
    assert r.equity_cum_dncf_by_year[2030] == 0.0
    # Project AI uses ≤ so may be non-zero at D22 while equity AI is 0
    assert r.disc_cncf_ai.get(2029, 0.0) != 0.0 or r.disc_contractor_ah.get(2029, 0.0) == 0.0
    # Scalars still project NPV × share
    assert abs(r.equity_ah51 - share * r.ah51) < 1e-12


def test_discount_year_zero() -> None:
    case = case_input_from_mapping(
        {
            "hurdle_rate": 0.15,
            "project_start_year": 2027,
            "equity_share_company_1": 0.49,
            "price_path_end_year": 2042,
        }
    )
    case.extras["project_ncf_intermediates"] = {
        "A": [[2027, 2027]],
        "B": [[2027, 0]],
        "E": [[2027, 0]],
        "F": [[2027, 0]],
        "G": [[2027, 0]],
        "H": [[2027, 0]],
        "I": [[2027, 0]],
        "J": [[2027, 0]],
        "O": [[2027, 0]],
        "P": [[2027, 0]],
        "Q": [[2027, 0]],
        "R": [[2027, 0]],
        "W": [[2027, 0]],
        "X": [[2027, 0]],
        "AB": [[2027, 0]],
        "AC": [[2027, 0]],
        "AD": [[2027, 10]],
        "AK": [[2027, 0]],
    }
    case.extras["price_path_end_year"] = 2042
    r = CrNcfModule().run(case)
    # AE = 10, disc at year 0 → AG = 10
    assert abs(r.host_ae[2027] - 10.0) < 1e-12
    assert abs(r.disc_host_ag[2027] - 10.0) < 1e-12


def test_determinism() -> None:
    case = case_input_from_mapping(
        {
            "hurdle_rate": 0.15,
            "project_start_year": 2027,
            "equity_share_company_1": 0.49,
            "price_path_end_year": 2042,
        }
    )
    case.extras["project_ncf_intermediates"] = {
        "A": [[2027, 2027], [2028, 2028]],
        "B": [[2027, 50], [2028, 60]],
        "E": [[2027, 1], [2028, 1]],
        "F": [[2027, 2], [2028, 2]],
        "G": [[2027, 0], [2028, 0]],
        "H": [[2027, 0], [2028, 0]],
        "I": [[2027, 3], [2028, 3]],
        "J": [[2027, 0], [2028, 0]],
        "O": [[2027, 0], [2028, 0]],
        "P": [[2027, 0], [2028, 0]],
        "Q": [[2027, 0], [2028, 0]],
        "R": [[2027, 0], [2028, 0]],
        "W": [[2027, 5], [2028, 0]],
        "X": [[2027, 0], [2028, 0]],
        "AB": [[2027, 1], [2028, 1]],
        "AC": [[2027, 0], [2028, 0]],
        "AD": [[2027, 0], [2028, 0]],
        "AK": [[2027, 0], [2028, 0]],
    }
    case.extras["price_path_end_year"] = 2042
    a = CrNcfModule().run(case).cell_map()
    b = CrNcfModule().run(case).cell_map()
    assert a == b
