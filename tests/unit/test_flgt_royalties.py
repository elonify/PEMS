"""FLGT/Royalties unit tests — Phase 1D groups R-G1…F-G11."""

from __future__ import annotations

from pems.calculations.modules.flgt_royalties import (
    FiscalLawParams,
    FlgtRoyaltiesModule,
    gas_royalty_rate,
    oil_price_path,
    price_royalty_rate,
    sliding_oil_royalty_rate,
)
from pems.domain.manual_input import case_input_from_mapping


def _band_shallow():
    law = FiscalLawParams.pia_default_from_gm_gtc()
    return next(b for b in law.oil_tiers if "Shallow" in b.terrain_label)


def _case(**kw):
    base = {
        "terrain": "Shallow Water (<200m water depth)",
        "gas_utilization": "In-Country (Dom Gas)",
        "oil_price_usd_bbl": 50.0,
        "gas_price_usd_mscf": 2.18,
        "price_escalator": 0.0,
        "project_start_year": 2027,
        "project_life_years": 15.0,
        "oil_block_daily": [[2027, 1.0], [2028, 10.0], [2029, 0.0]],
        "oil_block_annual": [[2027, 0.36525], [2028, 3.6525], [2029, 0.0]],
        "gas_block_daily": [[2027, 1.2], [2028, 12.0], [2029, 0.0]],
        "gas_block_annual": [[2027, 0.0], [2028, 4.38], [2029, 0.0]],
        "oil_tc_opex": [[2027, 11.45], [2028, 28.76]],
        "oil_tc_exploration": [[2027, 0.0], [2028, 35.0]],
        "oil_tc_capex_wells": [[2027, 0.0], [2028, 0.0]],
        "oil_tc_capex_facilities": [[2027, 0.0], [2028, 80.0]],
        "gas_tc_opex": [[2027, 3.78], [2028, 3.78]],
        "gas_tc_exploration": [[2027, 0.0], [2028, 0.0]],
        "gas_tc_capex_wells": [[2027, 0.0], [2028, 0.0]],
        "gas_tc_capex_facilities": [[2027, 0.0], [2028, 0.0]],
        "price_path_end_year": 2042,
        "forecast_anchor_year": 2027,
        "analysis_n12": 0.0,
        "analysis_n13": 0.0,
        "analysis_n15": 0.0,
    }
    base.update(kw)
    return case_input_from_mapping(base)


def test_timeline_years() -> None:
    r = FlgtRoyaltiesModule().run(_case())
    assert 2027 in r.years and 2028 in r.years


def test_terrain_shallow_oil_rate() -> None:
    band = _band_shallow()
    assert abs(sliding_oil_royalty_rate(1.0, band) - 0.05) < 1e-12
    assert abs(sliding_oil_royalty_rate(0.0, band) - 0.0) < 1e-12


def test_sliding_oil_rate_mid_band() -> None:
    band = _band_shallow()
    # 10 mb/d = 10000 bopd → top of mid: progressive
    r = sliding_oil_royalty_rate(10.0, band)
    assert abs(r - 0.0625) < 1e-9


def test_gas_royalty_dom_and_out() -> None:
    law = FiscalLawParams.pia_default_from_gm_gtc()
    assert gas_royalty_rate(1.0, "In-Country (Dom Gas)", law) == 0.025
    assert gas_royalty_rate(1.0, "Out-Country", law) == 0.05
    assert gas_royalty_rate(0.0, "In-Country (Dom Gas)", law) == 0.0


def test_oil_price_path_and_price_royalty() -> None:
    p, q, r = oil_price_path(
        2027,
        oil_price=50.0,
        escalator=0.0,
        start_year=2027,
        price_end_year=2042,
        analysis_n12=0.0,
        analysis_n15=0.0,
        daily_oil=1.0,
        d29_year=2027,
    )
    assert p == 50.0 and q == 1.0 and r == 50.0
    law = FiscalLawParams.pia_default_from_gm_gtc()
    assert price_royalty_rate(50.0, 2027, law) == 0.0
    assert abs(price_royalty_rate(100.0, 2027, law) - 0.05) < 1e-12
    assert price_royalty_rate(150.0, 2027, law) == 0.10


def test_revenues_and_royalties_mm() -> None:
    r = FlgtRoyaltiesModule().run(_case())
    assert abs(r.oil_revenue[2027] - 50.0 * 0.36525) < 1e-9
    assert abs(r.gas_revenue[2028] - 2.18 * 4.38) < 1e-9
    assert abs(r.oil_royalty_mm[2027] - 0.05 * 50.0 * 0.36525) < 1e-9
    assert abs(r.gas_royalty_mm[2028] - 0.025 * 2.18 * 4.38) < 1e-9
    assert r.price_royalty_mm[2027] == 0.0


def test_rentals_hcdt_nddc() -> None:
    r = FlgtRoyaltiesModule().run(_case())
    # rental when oil daily > 0
    assert r.rentals[2027] > 0
    assert r.rentals[2029] == 0.0
    # AF lag: 2028 uses 2027 opex * 0.03
    assert abs(r.hcdt_oil[2028] - 11.45 * 0.03) < 1e-9
    assert r.hcdt_oil[2027] == 0.0  # no prior opex
    # AG 2027: opex only 11.45 * 0.03
    assert abs(r.nddc_oil[2027] - 11.45 * 0.03) < 1e-9
    assert abs(r.nddc_gas[2027] - 3.78 * 0.03) < 1e-9


def test_bonus_core_zero() -> None:
    r = FlgtRoyaltiesModule().run(_case())
    assert r.aa51 == 0.0


def test_err_and_ec_io_hubs() -> None:
    r = FlgtRoyaltiesModule().run(_case())
    assert abs(r.al51 - (r.ab51 + r.ac51 + r.ad51)) < 1e-12
    if r.y51:
        assert abs(r.am51 - r.al51 / r.y51) < 1e-12
    m = r.cell_map()
    assert m[("Ec_IO", "G11")] == r.am51
    assert m[("Ec_IO", "G15")] == r.al51


def test_analysis_import_as_saved_identity() -> None:
    r0 = FlgtRoyaltiesModule().run(_case(analysis_n12=0.0))
    r1 = FlgtRoyaltiesModule().run(_case(analysis_n12=0.1))
    assert r1.price_nominal[2027] > r0.price_nominal[2027]


def test_determinism() -> None:
    case = _case()
    a = FlgtRoyaltiesModule().run(case).cell_map()
    b = FlgtRoyaltiesModule().run(case).cell_map()
    assert a == b


def test_zero_production() -> None:
    r = FlgtRoyaltiesModule().run(
        _case(
            oil_block_daily=[[2027, 0.0]],
            oil_block_annual=[[2027, 0.0]],
            gas_block_daily=[[2027, 0.0]],
            gas_block_annual=[[2027, 0.0]],
        )
    )
    assert r.ab51 == 0.0 and r.ac51 == 0.0 and r.w51 == 0.0
