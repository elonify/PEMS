"""Immutable presentation data structures and ChartDataset builders.

Builders project calculation Result DTOs only — no economic re-calculation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from pems.presentation.charts.templates import CHART_TEMPLATES


@dataclass(frozen=True)
class ChartSeries:
    """One ordered chart series."""

    key: str
    label: str
    x: Sequence[int | float | str]
    y: Sequence[int | float | None]


@dataclass(frozen=True)
class ChartDataset:
    """Presentation-ready chart dataset.

    This layer contains no economic calculations. It receives already-computed
    values from calculation Result DTOs and exposes them in a renderer-neutral
    form.
    """

    dataset_id: str
    title: str
    x_label: str
    y_label: str
    series: Sequence[ChartSeries]
    metadata: Mapping[str, str] = field(default_factory=dict)


def discounted_ncf_dataset(cr_ncf: Any) -> ChartDataset:
    """Build the Project Discounted NCF dataset from CrNcfResult.

    The calculation module already provides both annual discounted contractor
    NCF and its running cumulative value. This function only projects those
    values into the renderer-neutral presentation contract.
    """
    template = CHART_TEMPLATES["DISCOUNTED_NCF"]

    years = list(cr_ncf.years)
    annual = [cr_ncf.disc_contractor_ah.get(year) for year in years]
    cumulative = [cr_ncf.disc_cncf_ai.get(year) for year in years]

    return ChartDataset(
        dataset_id="PROJECT_DISCOUNTED_NCF",
        title=template.title,
        x_label=template.x_label,
        y_label=template.y_label,
        series=(
            ChartSeries(
                key="annual_discounted_ncf",
                label="Annual discounted contractor NCF",
                x=years,
                y=annual,
            ),
            ChartSeries(
                key="cumulative_discounted_ncf",
                label="Cumulative discounted contractor NCF",
                x=years,
                y=cumulative,
            ),
        ),
        metadata={
            "source": "CrNcfResult",
            "template_id": template.template_id,
        },
    )


def economic_limit_dataset(
    cr_ncf: Any,
    production: Any,
) -> ChartDataset:
    """Build the Economic Limit dataset from CrNcfResult + ProductionResult.

    Golden Master Ec_IO chart1 series (named ranges → DTO maps):
      Cum_DNCF    → cr_ncf.disc_cncf_ai
      Annual_DNCF → cr_ncf.disc_contractor_ah
      Rates_Oil   → production.oil_daily_series (Prod_Summary col T, mb/d)

    Presentation only — no economic re-calculation or FILTER/TAKE logic.
    Year spine is cr_ncf.years (project NCF calendar); production rates are
    looked up by year with None when absent.
    """
    template = CHART_TEMPLATES["ECONOMIC_LIMIT"]

    years = list(cr_ncf.years)
    cumulative = [cr_ncf.disc_cncf_ai.get(year) for year in years]
    annual = [cr_ncf.disc_contractor_ah.get(year) for year in years]
    oil_rate = [production.oil_daily_series.get(year) for year in years]

    return ChartDataset(
        dataset_id="ECONOMIC_LIMIT",
        title=template.title,
        x_label=template.x_label,
        y_label=template.y_label,
        series=(
            ChartSeries(
                key="cumulative_discounted_ncf",
                label="Cumulative discounted contractor NCF",
                x=years,
                y=cumulative,
            ),
            ChartSeries(
                key="annual_discounted_ncf",
                label="Annual discounted contractor NCF",
                x=years,
                y=annual,
            ),
            ChartSeries(
                key="oil_production_rate",
                label="Oil production rate",
                x=years,
                y=oil_rate,
            ),
        ),
        metadata={
            "source": "CrNcfResult+ProductionResult",
            "template_id": template.template_id,
            "gm_named_ranges": "Cum_DNCF|Annual_DNCF|Rates_Oil|Years_Prod",
        },
    )


def cost_profile_dataset(costs: Any, stream: str) -> ChartDataset:
    """Build Oil or Gas Cost Profile from CostsResult stream maps.

    Golden Master Cost Profile charts (oil chart4/21, gas chart5/22):
      Expl_Appr. / Gas_Expl_Appr. → stream.exploration
      Wells_CAP  / Gas_Wells_CAP  → stream.capex_wells
      Fac_CAP    / Gas_Fac_CAP    → stream.capex_facilities
      OPEX       / Gas_OPEX       → stream.opex

    Undiscounted maps only — disc_capex / disc_opex are not used.
    ``stream`` must be exactly ``\"oil\"`` or ``\"gas\"``.
    """
    if stream not in ("oil", "gas"):
        raise ValueError(f"stream must be 'oil' or 'gas', got {stream!r}")

    template = CHART_TEMPLATES["COST_PROFILE"]
    stream_result = costs.oil if stream == "oil" else costs.gas
    stream_label = "Oil" if stream == "oil" else "Gas"
    dataset_id = "OIL_COST_PROFILE" if stream == "oil" else "GAS_COST_PROFILE"

    years = list(stream_result.years)
    exploration = [stream_result.exploration.get(year) for year in years]
    wells = [stream_result.capex_wells.get(year) for year in years]
    facilities = [stream_result.capex_facilities.get(year) for year in years]
    opex = [stream_result.opex.get(year) for year in years]

    return ChartDataset(
        dataset_id=dataset_id,
        title=f"{stream_label} {template.title}",
        x_label=template.x_label,
        y_label=template.y_label,
        series=(
            ChartSeries(
                key="exploration",
                label=f"{stream_label} exploration / appraisal",
                x=years,
                y=exploration,
            ),
            ChartSeries(
                key="capex_wells",
                label=f"{stream_label} wells CAPEX",
                x=years,
                y=wells,
            ),
            ChartSeries(
                key="capex_facilities",
                label=f"{stream_label} facilities CAPEX",
                x=years,
                y=facilities,
            ),
            ChartSeries(
                key="opex",
                label=f"{stream_label} OPEX",
                x=years,
                y=opex,
            ),
        ),
        metadata={
            "source": "CostsResult",
            "template_id": template.template_id,
            "stream": stream,
            "gm_named_ranges": (
                "Expl_Appr.|Wells_CAP|Fac_CAP|OPEX"
                if stream == "oil"
                else "Gas_Expl_Appr.|Gas_Wells_CAP|Gas_Fac_CAP|Gas_OPEX"
            ),
        },
    )


def flgt_take_dataset(flgt: Any) -> ChartDataset:
    """Build Front-Loaded Government Take dataset from FlgtResult.

    Golden Master chart23 series (FLGT cols AA–AG, categories A):
      AA bonuses
      AB oil_royalty_mm
      AC gas_royalty_mm
      AD price_royalty_mm
      AE rentals
      AF hcdt_oil
      AG nddc_oil

    Excludes flgt_total, royalty_sum, err_annual, nddc_gas, and revenue maps.
    Presentation projection only — no summation or re-calculation.
    """
    template = CHART_TEMPLATES["FLGT_TAKE"]

    years = list(flgt.years)
    bonuses = [flgt.bonuses.get(year) for year in years]
    oil_royalty = [flgt.oil_royalty_mm.get(year) for year in years]
    gas_royalty = [flgt.gas_royalty_mm.get(year) for year in years]
    price_royalty = [flgt.price_royalty_mm.get(year) for year in years]
    rentals = [flgt.rentals.get(year) for year in years]
    hcdt_oil = [flgt.hcdt_oil.get(year) for year in years]
    nddc_oil = [flgt.nddc_oil.get(year) for year in years]

    return ChartDataset(
        dataset_id="FLGT_TAKE",
        title=template.title,
        x_label=template.x_label,
        y_label=template.y_label,
        series=(
            ChartSeries(
                key="bonuses",
                label="Bonuses",
                x=years,
                y=bonuses,
            ),
            ChartSeries(
                key="oil_royalty_mm",
                label="Oil royalty",
                x=years,
                y=oil_royalty,
            ),
            ChartSeries(
                key="gas_royalty_mm",
                label="Gas royalty",
                x=years,
                y=gas_royalty,
            ),
            ChartSeries(
                key="price_royalty_mm",
                label="Price royalty",
                x=years,
                y=price_royalty,
            ),
            ChartSeries(
                key="rentals",
                label="Rentals",
                x=years,
                y=rentals,
            ),
            ChartSeries(
                key="hcdt_oil",
                label="HCDT oil",
                x=years,
                y=hcdt_oil,
            ),
            ChartSeries(
                key="nddc_oil",
                label="NDDC oil",
                x=years,
                y=nddc_oil,
            ),
        ),
        metadata={
            "source": "FlgtResult",
            "template_id": template.template_id,
            "gm_columns": "A|AA|AB|AC|AD|AE|AF|AG",
        },
    )


def production_summary_dataset(production: Any, stream: str) -> ChartDataset:
    """Build Oil or Gas Production Summary from ProductionResult maps.

    Golden Master Prod_Summary charts (oil chart19/2, gas chart20/3):
      Rates_Oil / Rates_Gas   → oil_daily_series / gas_daily_series   (T / W)
      Annual_Oil / Annual_Gas → oil_annual_series / gas_annual_series (U / X)
      Cum_Oil / Cum_Gas       → oil_cum_series / gas_cum_series       (V / Y)

    Year spine is the sorted union of the three stream map keys (Years_Prod).
    ``stream`` must be exactly ``\"oil\"`` or ``\"gas\"``.
    Presentation only — no volume re-calculation or running-sum invention.
    """
    if stream not in ("oil", "gas"):
        raise ValueError(f"stream must be 'oil' or 'gas', got {stream!r}")

    template = CHART_TEMPLATES["PRODUCTION_SUMMARY"]
    stream_label = "Oil" if stream == "oil" else "Gas"
    dataset_id = (
        "OIL_PRODUCTION_SUMMARY" if stream == "oil" else "GAS_PRODUCTION_SUMMARY"
    )

    if stream == "oil":
        rate_map = production.oil_daily_series
        annual_map = production.oil_annual_series
        cum_map = production.oil_cum_series
        gm_names = "Years_Prod|Annual_Oil|Cum_Oil|Rates_Oil"
        # GM chart19 series order: Annual, Cum, Rates
        series_specs = (
            ("annual", f"{stream_label} annual production", annual_map),
            ("cumulative", f"{stream_label} cumulative production", cum_map),
            ("rate", f"{stream_label} production rate", rate_map),
        )
    else:
        rate_map = production.gas_daily_series
        annual_map = production.gas_annual_series
        cum_map = production.gas_cum_series
        gm_names = "Years_Prod|Cum_Gas|Annual_Gas|Rates_Gas"
        # GM chart20 series order: Cum, Annual, Rates
        series_specs = (
            ("cumulative", f"{stream_label} cumulative production", cum_map),
            ("annual", f"{stream_label} annual production", annual_map),
            ("rate", f"{stream_label} production rate", rate_map),
        )

    years = sorted(set(rate_map) | set(annual_map) | set(cum_map))
    series = tuple(
        ChartSeries(
            key=key,
            label=label,
            x=years,
            y=[src.get(year) for year in years],
        )
        for key, label, src in series_specs
    )

    return ChartDataset(
        dataset_id=dataset_id,
        title=f"{stream_label} {template.title}",
        x_label=template.x_label,
        y_label=template.y_label,
        series=series,
        metadata={
            "source": "ProductionResult",
            "template_id": template.template_id,
            "stream": stream,
            "gm_named_ranges": gm_names,
        },
    )


def production_profile_dataset(production: Any, stream: str) -> ChartDataset:
    """Build Oil or AG Production Profile from ProductionResult PP maps.

    Golden Master chart15 (oil/primary) and chart16 (associated gas):
      Rates_Charts / AG rates → pp_rate_by_year / pp_ag_rate_by_year  (D / G)
      Chart_Cum / AG_Chart_Cum → pp_cum_by_year / pp_ag_cum_by_year   (F / I)

    Year spine is the sorted union of rate and cum map keys (Years_Charts).
    ``stream`` must be exactly ``\"oil\"`` or ``\"gas\"`` (gas = associated gas).
    Presentation only — no running-sum or rate recalculation.
    """
    if stream not in ("oil", "gas"):
        raise ValueError(f"stream must be 'oil' or 'gas', got {stream!r}")

    template = CHART_TEMPLATES["PRODUCTION_PROFILE"]

    if stream == "oil":
        stream_label = "Oil"
        dataset_id = "OIL_PRODUCTION_PROFILE"
        rate_map = production.pp_rate_by_year
        cum_map = production.pp_cum_by_year
        gm_names = "Years_Charts|Rates_Charts|Chart_Cum"
        series_specs = (
            ("rate", f"{stream_label} production rate", rate_map),
            ("cumulative", f"{stream_label} cumulative production", cum_map),
        )
    else:
        stream_label = "Associated gas"
        dataset_id = "GAS_PRODUCTION_PROFILE"
        rate_map = production.pp_ag_rate_by_year
        cum_map = production.pp_ag_cum_by_year
        gm_names = "Years_Charts|AG_Chart_Rates|AG_Chart_Cum"
        series_specs = (
            ("rate", f"{stream_label} production rate", rate_map),
            ("cumulative", f"{stream_label} cumulative production", cum_map),
        )

    years = sorted(set(rate_map) | set(cum_map))
    series = tuple(
        ChartSeries(
            key=key,
            label=label,
            x=years,
            y=[src.get(year) for year in years],
        )
        for key, label, src in series_specs
    )

    return ChartDataset(
        dataset_id=dataset_id,
        title=f"{stream_label} {template.title}",
        x_label=template.x_label,
        y_label=template.y_label,
        series=series,
        metadata={
            "source": "ProductionResult",
            "template_id": template.template_id,
            "stream": stream,
            "gm_named_ranges": gm_names,
        },
    )
