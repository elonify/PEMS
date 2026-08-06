"""Unit tests for ChartDataset builders (presentation only — no calc invention)."""

from __future__ import annotations

import inspect

import pytest

from pems.calculations.modules.costs import CostsResult, StreamCostResult
from pems.calculations.modules.cr_ncf import CrNcfResult
from pems.calculations.modules.flgt_royalties import FlgtResult
from pems.calculations.modules.production import ProductionResult
from pems.presentation.charts import datasets as datasets_mod
from pems.presentation.charts.datasets import (
    ChartDataset,
    ChartSeries,
    cost_profile_dataset,
    discounted_ncf_dataset,
    economic_limit_dataset,
    flgt_take_dataset,
    production_summary_dataset,
)
from pems.presentation.charts.templates import CHART_TEMPLATES

_FLGT_SERIES_KEYS = (
    "bonuses",
    "oil_royalty_mm",
    "gas_royalty_mm",
    "price_royalty_mm",
    "rentals",
    "hcdt_oil",
    "nddc_oil",
)

_FLGT_EXCLUDED_ATTRS = (
    "flgt_total",
    "royalty_sum",
    "err_annual",
    "nddc_gas",
    "oil_revenue",
    "gas_revenue",
    "total_revenue",
)


def _cr_ncf_with_disc_series() -> CrNcfResult:
    """Minimal CrNcfResult with pre-computed disc maps (not calculated here)."""
    years = [2027, 2028, 2029]
    return CrNcfResult(
        years=years,
        disc_contractor_ah={2027: -10.0, 2028: 5.0, 2029: 12.5},
        disc_cncf_ai={2027: -10.0, 2028: -5.0, 2029: 7.5},
    )


def _production_with_oil_rates() -> ProductionResult:
    """Minimal ProductionResult with pre-computed oil daily rates (Rates_Oil)."""
    return ProductionResult(
        oil_daily_series={2027: 8.5, 2028: 12.0, 2029: 9.25},
    )


def test_discounted_ncf_dataset_identity_and_template() -> None:
    ds = discounted_ncf_dataset(_cr_ncf_with_disc_series())
    template = CHART_TEMPLATES["DISCOUNTED_NCF"]

    assert isinstance(ds, ChartDataset)
    assert ds.dataset_id == "PROJECT_DISCOUNTED_NCF"
    assert ds.title == template.title
    assert ds.x_label == template.x_label
    assert ds.y_label == template.y_label
    assert ds.metadata["source"] == "CrNcfResult"
    assert ds.metadata["template_id"] == "DISCOUNTED_NCF"


def test_discounted_ncf_dataset_projects_dto_series_only() -> None:
    cr = _cr_ncf_with_disc_series()
    ds = discounted_ncf_dataset(cr)

    assert len(ds.series) == 2
    annual, cumulative = ds.series

    assert isinstance(annual, ChartSeries)
    assert annual.key == "annual_discounted_ncf"
    assert annual.label == "Annual discounted contractor NCF"
    assert list(annual.x) == cr.years
    assert list(annual.y) == [cr.disc_contractor_ah[y] for y in cr.years]

    assert cumulative.key == "cumulative_discounted_ncf"
    assert cumulative.label == "Cumulative discounted contractor NCF"
    assert list(cumulative.x) == cr.years
    assert list(cumulative.y) == [cr.disc_cncf_ai[y] for y in cr.years]


def test_discounted_ncf_dataset_missing_year_yields_none() -> None:
    """Builder uses .get — missing year maps to None, does not invent values."""
    cr = CrNcfResult(
        years=[2027, 2028],
        disc_contractor_ah={2027: 1.0},
        disc_cncf_ai={2027: 1.0},
    )
    ds = discounted_ncf_dataset(cr)
    assert list(ds.series[0].y) == [1.0, None]
    assert list(ds.series[1].y) == [1.0, None]


def test_discounted_ncf_dataset_empty_years() -> None:
    ds = discounted_ncf_dataset(CrNcfResult())
    assert list(ds.series[0].x) == []
    assert list(ds.series[0].y) == []
    assert list(ds.series[1].x) == []
    assert list(ds.series[1].y) == []


def test_economic_limit_dataset_identity_and_template() -> None:
    """1. Template / chart identity."""
    ds = economic_limit_dataset(_cr_ncf_with_disc_series(), _production_with_oil_rates())
    template = CHART_TEMPLATES["ECONOMIC_LIMIT"]

    assert isinstance(ds, ChartDataset)
    assert ds.dataset_id == "ECONOMIC_LIMIT"
    assert ds.title == template.title == "Economic Limit"
    assert ds.x_label == template.x_label
    assert ds.y_label == template.y_label
    assert ds.metadata["source"] == "CrNcfResult+ProductionResult"
    assert ds.metadata["template_id"] == "ECONOMIC_LIMIT"


def test_economic_limit_dataset_projects_dto_series_only() -> None:
    """2. Exact DTO-to-series projection (Cum_DNCF / Annual_DNCF / Rates_Oil)."""
    cr = _cr_ncf_with_disc_series()
    prod = _production_with_oil_rates()
    ds = economic_limit_dataset(cr, prod)

    assert len(ds.series) == 3
    cumulative, annual, oil_rate = ds.series

    assert cumulative.key == "cumulative_discounted_ncf"
    assert list(cumulative.x) == cr.years
    assert list(cumulative.y) == [cr.disc_cncf_ai[y] for y in cr.years]

    assert annual.key == "annual_discounted_ncf"
    assert list(annual.x) == cr.years
    assert list(annual.y) == [cr.disc_contractor_ah[y] for y in cr.years]

    assert isinstance(oil_rate, ChartSeries)
    assert oil_rate.key == "oil_production_rate"
    assert oil_rate.label == "Oil production rate"
    assert list(oil_rate.x) == cr.years
    assert list(oil_rate.y) == [prod.oil_daily_series[y] for y in cr.years]


def test_economic_limit_dataset_shared_year_keys() -> None:
    """3. All three series use the same year keys (cr_ncf.years)."""
    cr = _cr_ncf_with_disc_series()
    ds = economic_limit_dataset(cr, _production_with_oil_rates())

    x0 = list(ds.series[0].x)
    assert x0 == list(cr.years)
    for s in ds.series:
        assert list(s.x) == x0
        assert len(s.y) == len(x0)


def test_economic_limit_dataset_missing_year_yields_none() -> None:
    """4. Missing map keys → None (same .get pattern as discounted_ncf_dataset)."""
    cr = CrNcfResult(
        years=[2027, 2028],
        disc_contractor_ah={2027: 1.0},
        disc_cncf_ai={2027: 1.0},
    )
    prod = ProductionResult(oil_daily_series={2027: 8.5})
    ds = economic_limit_dataset(cr, prod)
    cumulative, annual, oil_rate = ds.series
    assert list(cumulative.y) == [1.0, None]
    assert list(annual.y) == [1.0, None]
    assert list(oil_rate.y) == [8.5, None]


def test_economic_limit_dataset_empty_input() -> None:
    """5. Empty years / empty production maps → empty series."""
    ds = economic_limit_dataset(CrNcfResult(), ProductionResult())
    assert len(ds.series) == 3
    for s in ds.series:
        assert list(s.x) == []
        assert list(s.y) == []


def test_economic_limit_dataset_preserves_source_values_exactly() -> None:
    """6. No recalculation — source floats preserved; DTO maps unchanged."""
    cr = CrNcfResult(
        years=[2027, 2028],
        disc_contractor_ah={2027: -10.125, 2028: 3.0 / 7.0},
        disc_cncf_ai={2027: -10.125, 2028: -10.125 + 3.0 / 7.0},
    )
    prod = ProductionResult(oil_daily_series={2027: 8.5, 2028: 0.0})
    ah_before = dict(cr.disc_contractor_ah)
    ai_before = dict(cr.disc_cncf_ai)
    oil_before = dict(prod.oil_daily_series)

    ds = economic_limit_dataset(cr, prod)
    cumulative, annual, oil_rate = ds.series

    assert list(annual.y) == [-10.125, 3.0 / 7.0]
    assert list(cumulative.y) == [-10.125, -10.125 + 3.0 / 7.0]
    assert list(oil_rate.y) == [8.5, 0.0]
    # builders must not mutate source DTOs
    assert cr.disc_contractor_ah == ah_before
    assert cr.disc_cncf_ai == ai_before
    assert prod.oil_daily_series == oil_before


def _costs_with_streams() -> CostsResult:
    """Minimal CostsResult with oil/gas undiscounted maps (plus decoy disc maps)."""
    oil = StreamCostResult(
        years=[2027, 2028, 2029],
        exploration={2027: 1.1, 2028: 0.0, 2029: 0.0},
        capex_wells={2027: 20.0, 2028: 15.0, 2029: 5.0},
        capex_facilities={2027: 30.0, 2028: 10.0, 2029: 0.0},
        opex={2027: 2.5, 2028: 3.0, 2029: 3.5},
        disc_capex={2027: 999.0, 2028: 999.0, 2029: 999.0},
        disc_opex={2027: 888.0, 2028: 888.0, 2029: 888.0},
    )
    gas = StreamCostResult(
        years=[2027, 2028],
        exploration={2027: 0.5, 2028: 0.0},
        capex_wells={2027: 8.0, 2028: 4.0},
        capex_facilities={2027: 12.0, 2028: 6.0},
        opex={2027: 1.0, 2028: 1.5},
        disc_capex={2027: 777.0, 2028: 777.0},
        disc_opex={2027: 666.0, 2028: 666.0},
    )
    return CostsResult(oil=oil, gas=gas)


def test_cost_profile_oil_mapping() -> None:
    """1. Oil stream mapping / identity."""
    costs = _costs_with_streams()
    ds = cost_profile_dataset(costs, "oil")
    template = CHART_TEMPLATES["COST_PROFILE"]

    assert isinstance(ds, ChartDataset)
    assert ds.dataset_id == "OIL_COST_PROFILE"
    assert ds.title == "Oil Cost Profile"
    assert ds.x_label == template.x_label
    assert ds.y_label == template.y_label
    assert ds.metadata["template_id"] == "COST_PROFILE"
    assert ds.metadata["stream"] == "oil"
    assert len(ds.series) == 4
    assert [s.key for s in ds.series] == [
        "exploration",
        "capex_wells",
        "capex_facilities",
        "opex",
    ]
    assert all("Oil" in s.label for s in ds.series)

    oil = costs.oil
    assert list(ds.series[0].y) == [oil.exploration[y] for y in oil.years]
    assert list(ds.series[1].y) == [oil.capex_wells[y] for y in oil.years]
    assert list(ds.series[2].y) == [oil.capex_facilities[y] for y in oil.years]
    assert list(ds.series[3].y) == [oil.opex[y] for y in oil.years]


def test_cost_profile_gas_mapping() -> None:
    """2. Gas stream mapping / identity."""
    costs = _costs_with_streams()
    ds = cost_profile_dataset(costs, "gas")

    assert ds.dataset_id == "GAS_COST_PROFILE"
    assert ds.title == "Gas Cost Profile"
    assert ds.metadata["stream"] == "gas"
    assert all("Gas" in s.label for s in ds.series)

    gas = costs.gas
    assert list(ds.series[0].x) == gas.years
    assert list(ds.series[0].y) == [gas.exploration[y] for y in gas.years]
    assert list(ds.series[1].y) == [gas.capex_wells[y] for y in gas.years]
    assert list(ds.series[2].y) == [gas.capex_facilities[y] for y in gas.years]
    assert list(ds.series[3].y) == [gas.opex[y] for y in gas.years]


def test_cost_profile_preserves_dto_values_exactly() -> None:
    """3. Exact DTO value preservation (no aggregation)."""
    oil = StreamCostResult(
        years=[2027, 2028],
        exploration={2027: 1.0 / 3.0, 2028: 0.0},
        capex_wells={2027: 20.125, 2028: 0.0},
        capex_facilities={2027: 0.0, 2028: 7.5},
        opex={2027: 2.0, 2028: 2.0 + 1.0 / 7.0},
    )
    costs = CostsResult(oil=oil)
    ds = cost_profile_dataset(costs, "oil")
    assert list(ds.series[0].y) == [1.0 / 3.0, 0.0]
    assert list(ds.series[1].y) == [20.125, 0.0]
    assert list(ds.series[2].y) == [0.0, 7.5]
    assert list(ds.series[3].y) == [2.0, 2.0 + 1.0 / 7.0]


def test_cost_profile_shared_year_keys() -> None:
    """4. All four series share stream.years as x-axis."""
    costs = _costs_with_streams()
    for stream in ("oil", "gas"):
        ds = cost_profile_dataset(costs, stream)
        stream_years = list(getattr(costs, stream).years)
        x0 = list(ds.series[0].x)
        assert x0 == stream_years
        for s in ds.series:
            assert list(s.x) == x0
            assert len(s.y) == len(x0)


def test_cost_profile_missing_keys_yield_none() -> None:
    """5. Missing map keys → None."""
    oil = StreamCostResult(
        years=[2027, 2028],
        exploration={2027: 1.0},
        capex_wells={2027: 2.0},
        capex_facilities={2027: 3.0},
        opex={2027: 4.0},
    )
    ds = cost_profile_dataset(CostsResult(oil=oil), "oil")
    assert list(ds.series[0].y) == [1.0, None]
    assert list(ds.series[1].y) == [2.0, None]
    assert list(ds.series[2].y) == [3.0, None]
    assert list(ds.series[3].y) == [4.0, None]


def test_cost_profile_empty_stream() -> None:
    """6. Empty stream years → empty series."""
    ds = cost_profile_dataset(CostsResult(), "oil")
    assert len(ds.series) == 4
    for s in ds.series:
        assert list(s.x) == []
        assert list(s.y) == []


def test_cost_profile_does_not_mutate_source() -> None:
    """7. Source DTO maps are not mutated."""
    costs = _costs_with_streams()
    oil = costs.oil
    snapshots = {
        "years": list(oil.years),
        "exploration": dict(oil.exploration),
        "capex_wells": dict(oil.capex_wells),
        "capex_facilities": dict(oil.capex_facilities),
        "opex": dict(oil.opex),
        "disc_capex": dict(oil.disc_capex),
        "disc_opex": dict(oil.disc_opex),
    }
    cost_profile_dataset(costs, "oil")
    assert list(oil.years) == snapshots["years"]
    assert oil.exploration == snapshots["exploration"]
    assert oil.capex_wells == snapshots["capex_wells"]
    assert oil.capex_facilities == snapshots["capex_facilities"]
    assert oil.opex == snapshots["opex"]
    assert oil.disc_capex == snapshots["disc_capex"]
    assert oil.disc_opex == snapshots["disc_opex"]


def test_cost_profile_does_not_use_discounted_fields() -> None:
    """8. disc_capex / disc_opex are never projected into series y-values."""
    costs = _costs_with_streams()
    for stream in ("oil", "gas"):
        stream_result = getattr(costs, stream)
        ds = cost_profile_dataset(costs, stream)
        for s in ds.series:
            for v in s.y:
                assert v not in stream_result.disc_capex.values()
                assert v not in stream_result.disc_opex.values()

    # Implementation body must not read discounted maps as data sources
    body = inspect.getsource(datasets_mod.cost_profile_dataset).split(
        "return ChartDataset", 1
    )[0]
    assert ".disc_capex" not in body
    assert ".disc_opex" not in body


def test_cost_profile_invalid_stream_raises() -> None:
    with pytest.raises(ValueError, match="stream must be"):
        cost_profile_dataset(CostsResult(), "combined")


def _flgt_with_take_series() -> FlgtResult:
    """Minimal FlgtResult with chart23 AA–AG maps (+ decoy excluded fields)."""
    years = [2027, 2028, 2029]
    return FlgtResult(
        years=years,
        bonuses={2027: 5.0, 2028: 0.0, 2029: 0.0},
        oil_royalty_mm={2027: 1.0, 2028: 2.0, 2029: 3.0},
        gas_royalty_mm={2027: 0.5, 2028: 0.6, 2029: 0.7},
        price_royalty_mm={2027: 0.1, 2028: 0.2, 2029: 0.3},
        rentals={2027: 0.05, 2028: 0.05, 2029: 0.05},
        hcdt_oil={2027: 0.2, 2028: 0.3, 2029: 0.4},
        nddc_oil={2027: 0.15, 2028: 0.25, 2029: 0.35},
        # excluded decoys — must never appear in projected series
        flgt_total={2027: 999.0, 2028: 999.0, 2029: 999.0},
        royalty_sum={2027: 888.0, 2028: 888.0, 2029: 888.0},
        err_annual={2027: 0.99, 2028: 0.99, 2029: 0.99},
        nddc_gas={2027: 777.0, 2028: 777.0, 2029: 777.0},
        oil_revenue={2027: 666.0, 2028: 666.0, 2029: 666.0},
        gas_revenue={2027: 555.0, 2028: 555.0, 2029: 555.0},
        total_revenue={2027: 444.0, 2028: 444.0, 2029: 444.0},
    )


def test_flgt_take_dataset_identity_and_template() -> None:
    """1. Template / chart identity."""
    ds = flgt_take_dataset(_flgt_with_take_series())
    template = CHART_TEMPLATES["FLGT_TAKE"]

    assert isinstance(ds, ChartDataset)
    assert ds.dataset_id == "FLGT_TAKE"
    assert ds.title == template.title
    assert ds.x_label == template.x_label
    assert ds.y_label == template.y_label
    assert ds.metadata["source"] == "FlgtResult"
    assert ds.metadata["template_id"] == "FLGT_TAKE"
    assert len(ds.series) == 7
    assert [s.key for s in ds.series] == list(_FLGT_SERIES_KEYS)


def test_flgt_take_dataset_projects_all_seven_series() -> None:
    """2. Exact DTO-to-series projection for all seven AA–AG series."""
    flgt = _flgt_with_take_series()
    ds = flgt_take_dataset(flgt)
    by_key = {s.key: s for s in ds.series}

    expected = {
        "bonuses": flgt.bonuses,
        "oil_royalty_mm": flgt.oil_royalty_mm,
        "gas_royalty_mm": flgt.gas_royalty_mm,
        "price_royalty_mm": flgt.price_royalty_mm,
        "rentals": flgt.rentals,
        "hcdt_oil": flgt.hcdt_oil,
        "nddc_oil": flgt.nddc_oil,
    }
    for key, src_map in expected.items():
        series = by_key[key]
        assert isinstance(series, ChartSeries)
        assert list(series.x) == flgt.years
        assert list(series.y) == [src_map[y] for y in flgt.years]

    assert by_key["bonuses"].label == "Bonuses"
    assert by_key["oil_royalty_mm"].label == "Oil royalty"
    assert by_key["gas_royalty_mm"].label == "Gas royalty"
    assert by_key["price_royalty_mm"].label == "Price royalty"
    assert by_key["rentals"].label == "Rentals"
    assert by_key["hcdt_oil"].label == "HCDT oil"
    assert by_key["nddc_oil"].label == "NDDC oil"


def test_flgt_take_dataset_shared_year_keys() -> None:
    """3. All seven series share flgt.years as x-axis."""
    flgt = _flgt_with_take_series()
    ds = flgt_take_dataset(flgt)
    x0 = list(ds.series[0].x)
    assert x0 == list(flgt.years)
    for s in ds.series:
        assert list(s.x) == x0
        assert len(s.y) == len(x0)


def test_flgt_take_dataset_missing_year_yields_none() -> None:
    """4. Missing map keys → None."""
    flgt = FlgtResult(
        years=[2027, 2028],
        bonuses={2027: 1.0},
        oil_royalty_mm={2027: 2.0},
        gas_royalty_mm={2027: 3.0},
        price_royalty_mm={2027: 4.0},
        rentals={2027: 5.0},
        hcdt_oil={2027: 6.0},
        nddc_oil={2027: 7.0},
    )
    ds = flgt_take_dataset(flgt)
    for s in ds.series:
        assert list(s.y)[0] is not None
        assert list(s.y)[1] is None


def test_flgt_take_dataset_empty_years() -> None:
    """5. Empty years → empty series."""
    ds = flgt_take_dataset(FlgtResult())
    assert len(ds.series) == 7
    for s in ds.series:
        assert list(s.x) == []
        assert list(s.y) == []


def test_flgt_take_dataset_preserves_values_exactly() -> None:
    """6. Exact numeric preservation (no summation)."""
    flgt = FlgtResult(
        years=[2027, 2028],
        bonuses={2027: 1.0 / 3.0, 2028: 0.0},
        oil_royalty_mm={2027: 2.125, 2028: 3.0 / 7.0},
        gas_royalty_mm={2027: 0.0, 2028: 0.5},
        price_royalty_mm={2027: 0.1, 2028: 0.2},
        rentals={2027: 0.05, 2028: 0.05},
        hcdt_oil={2027: 0.25, 2028: 0.0},
        nddc_oil={2027: 0.0, 2028: 1.0 / 8.0},
    )
    ds = flgt_take_dataset(flgt)
    by_key = {s.key: list(s.y) for s in ds.series}
    assert by_key["bonuses"] == [1.0 / 3.0, 0.0]
    assert by_key["oil_royalty_mm"] == [2.125, 3.0 / 7.0]
    assert by_key["gas_royalty_mm"] == [0.0, 0.5]
    assert by_key["price_royalty_mm"] == [0.1, 0.2]
    assert by_key["rentals"] == [0.05, 0.05]
    assert by_key["hcdt_oil"] == [0.25, 0.0]
    assert by_key["nddc_oil"] == [0.0, 1.0 / 8.0]


def test_flgt_take_dataset_does_not_mutate_source() -> None:
    """7. Source DTO maps remain unmodified."""
    flgt = _flgt_with_take_series()
    snapshots = {
        key: dict(getattr(flgt, key))
        for key in (*_FLGT_SERIES_KEYS, *_FLGT_EXCLUDED_ATTRS)
    }
    years_before = list(flgt.years)
    flgt_take_dataset(flgt)
    assert list(flgt.years) == years_before
    for key, before in snapshots.items():
        assert getattr(flgt, key) == before


def test_flgt_take_dataset_excludes_non_chart_fields() -> None:
    """8. Excluded fields are not exposed as series keys or y-values."""
    flgt = _flgt_with_take_series()
    ds = flgt_take_dataset(flgt)
    keys = {s.key for s in ds.series}
    for attr in _FLGT_EXCLUDED_ATTRS:
        assert attr not in keys

    decoy_values = {
        v
        for attr in _FLGT_EXCLUDED_ATTRS
        for v in getattr(flgt, attr).values()
    }
    for s in ds.series:
        for v in s.y:
            assert v not in decoy_values

    body = inspect.getsource(datasets_mod.flgt_take_dataset).split(
        "return ChartDataset", 1
    )[0]
    for attr in _FLGT_EXCLUDED_ATTRS:
        assert f".{attr}" not in body


def _production_with_summary_streams() -> ProductionResult:
    """Minimal ProductionResult with oil/gas Prod_Summary maps."""
    return ProductionResult(
        oil_daily_series={2027: 8.5, 2028: 12.0, 2029: 9.25},
        oil_annual_series={2027: 3.1, 2028: 4.4, 2029: 3.4},
        oil_cum_series={2027: 3.1, 2028: 7.5, 2029: 10.9},
        gas_daily_series={2027: 20.0, 2028: 18.0},
        gas_annual_series={2027: 7.3, 2028: 6.6},
        gas_cum_series={2027: 7.3, 2028: 13.9},
        # PP maps present as decoys — must not be used by production summary builder
        pp_rate_by_year={2027: 999.0, 2028: 999.0},
        pp_ag_rate_by_year={2027: 888.0, 2028: 888.0},
    )


def test_production_summary_oil_mapping() -> None:
    """1. Oil stream identity and DTO mapping (Annual, Cum, Rates)."""
    prod = _production_with_summary_streams()
    ds = production_summary_dataset(prod, "oil")
    template = CHART_TEMPLATES["PRODUCTION_SUMMARY"]

    assert isinstance(ds, ChartDataset)
    assert ds.dataset_id == "OIL_PRODUCTION_SUMMARY"
    assert ds.title == "Oil Production Summary"
    assert ds.x_label == template.x_label
    assert ds.y_label == template.y_label
    assert ds.metadata["stream"] == "oil"
    assert ds.metadata["template_id"] == "PRODUCTION_SUMMARY"
    assert [s.key for s in ds.series] == ["annual", "cumulative", "rate"]
    assert all("Oil" in s.label for s in ds.series)

    years = sorted(
        set(prod.oil_daily_series)
        | set(prod.oil_annual_series)
        | set(prod.oil_cum_series)
    )
    by_key = {s.key: s for s in ds.series}
    assert list(by_key["annual"].y) == [prod.oil_annual_series[y] for y in years]
    assert list(by_key["cumulative"].y) == [prod.oil_cum_series[y] for y in years]
    assert list(by_key["rate"].y) == [prod.oil_daily_series[y] for y in years]


def test_production_summary_gas_mapping() -> None:
    """2. Gas stream identity and DTO mapping (Cum, Annual, Rates — GM order)."""
    prod = _production_with_summary_streams()
    ds = production_summary_dataset(prod, "gas")

    assert ds.dataset_id == "GAS_PRODUCTION_SUMMARY"
    assert ds.title == "Gas Production Summary"
    assert ds.metadata["stream"] == "gas"
    assert [s.key for s in ds.series] == ["cumulative", "annual", "rate"]
    assert all("Gas" in s.label for s in ds.series)

    years = sorted(
        set(prod.gas_daily_series)
        | set(prod.gas_annual_series)
        | set(prod.gas_cum_series)
    )
    by_key = {s.key: s for s in ds.series}
    assert list(by_key["cumulative"].y) == [prod.gas_cum_series[y] for y in years]
    assert list(by_key["annual"].y) == [prod.gas_annual_series[y] for y in years]
    assert list(by_key["rate"].y) == [prod.gas_daily_series[y] for y in years]


def test_production_summary_shared_year_keys() -> None:
    """3. All series share the same year spine within a stream."""
    prod = _production_with_summary_streams()
    for stream in ("oil", "gas"):
        ds = production_summary_dataset(prod, stream)
        x0 = list(ds.series[0].x)
        for s in ds.series:
            assert list(s.x) == x0
            assert len(s.y) == len(x0)


def test_production_summary_missing_year_yields_none() -> None:
    """4. Missing map keys → None."""
    prod = ProductionResult(
        oil_daily_series={2027: 8.5},
        oil_annual_series={2027: 3.1, 2028: 4.0},
        oil_cum_series={2027: 3.1},
    )
    ds = production_summary_dataset(prod, "oil")
    years = list(ds.series[0].x)
    assert years == [2027, 2028]
    by_key = {s.key: list(s.y) for s in ds.series}
    assert by_key["annual"] == [3.1, 4.0]
    assert by_key["cumulative"] == [3.1, None]
    assert by_key["rate"] == [8.5, None]


def test_production_summary_empty_stream() -> None:
    """5. Empty production maps → empty series."""
    ds = production_summary_dataset(ProductionResult(), "oil")
    assert len(ds.series) == 3
    for s in ds.series:
        assert list(s.x) == []
        assert list(s.y) == []


def test_production_summary_preserves_values_exactly() -> None:
    """6. Exact numeric preservation — no re-cumulation."""
    prod = ProductionResult(
        oil_daily_series={2027: 8.5, 2028: 0.0},
        oil_annual_series={2027: 1.0 / 3.0, 2028: 2.125},
        oil_cum_series={2027: 1.0 / 3.0, 2028: 1.0 / 3.0 + 2.125},
    )
    ds = production_summary_dataset(prod, "oil")
    by_key = {s.key: list(s.y) for s in ds.series}
    assert by_key["rate"] == [8.5, 0.0]
    assert by_key["annual"] == [1.0 / 3.0, 2.125]
    assert by_key["cumulative"] == [1.0 / 3.0, 1.0 / 3.0 + 2.125]


def test_production_summary_does_not_mutate_source() -> None:
    """7. Source DTO maps remain unmodified."""
    prod = _production_with_summary_streams()
    snaps = {
        "oil_daily_series": dict(prod.oil_daily_series),
        "oil_annual_series": dict(prod.oil_annual_series),
        "oil_cum_series": dict(prod.oil_cum_series),
        "gas_daily_series": dict(prod.gas_daily_series),
        "gas_annual_series": dict(prod.gas_annual_series),
        "gas_cum_series": dict(prod.gas_cum_series),
        "pp_rate_by_year": dict(prod.pp_rate_by_year),
    }
    production_summary_dataset(prod, "oil")
    production_summary_dataset(prod, "gas")
    for key, before in snaps.items():
        assert getattr(prod, key) == before


def test_production_summary_uses_prod_summary_maps_not_pp() -> None:
    """8. Uses Prod_Summary T/U/V/W/X/Y maps only — not PP design maps."""
    prod = _production_with_summary_streams()
    for stream in ("oil", "gas"):
        ds = production_summary_dataset(prod, stream)
        for s in ds.series:
            for v in s.y:
                assert v not in prod.pp_rate_by_year.values()
                assert v not in prod.pp_ag_rate_by_year.values()

    body = inspect.getsource(datasets_mod.production_summary_dataset).split(
        "return ChartDataset", 1
    )[0]
    assert "pp_rate_by_year" not in body
    assert "pp_ag_rate_by_year" not in body
    assert "pp_annual_by_year" not in body


def test_production_summary_invalid_stream_raises() -> None:
    with pytest.raises(ValueError, match="stream must be"):
        production_summary_dataset(ProductionResult(), "combined")
