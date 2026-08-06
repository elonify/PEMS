"""Semantic chart template definitions.

Templates describe presentation semantics only. They do not calculate values
and do not read Excel workbooks.
"""

from dataclasses import dataclass
from enum import Enum


class ChartType(str, Enum):
    LINE = "line"
    AREA = "area"
    BAR = "bar"
    SCATTER = "scatter"


@dataclass(frozen=True)
class ChartTemplate:
    """Semantic definition of a chart."""

    template_id: str
    title: str
    chart_type: ChartType
    x_label: str
    y_label: str


# First controlled template set. Analysis/sensitivity charts remain deferred.
CHART_TEMPLATES: dict[str, ChartTemplate] = {
    "ECONOMIC_LIMIT": ChartTemplate(
        template_id="ECONOMIC_LIMIT",
        title="Economic Limit",
        chart_type=ChartType.AREA,
        x_label="Year",
        y_label="Net cash flow / production",
    ),
    "COST_PROFILE": ChartTemplate(
        template_id="COST_PROFILE",
        title="Cost Profile",
        chart_type=ChartType.BAR,
        x_label="Cost category",
        y_label="Cost",
    ),
    "DISCOUNTED_NCF": ChartTemplate(
        template_id="DISCOUNTED_NCF",
        title="Project Discounted NCF",
        chart_type=ChartType.AREA,
        x_label="Year",
        y_label="Discounted NCF",
    ),
    "EQUITY_CASHFLOW": ChartTemplate(
        template_id="EQUITY_CASHFLOW",
        title="Equity CashFlow",
        chart_type=ChartType.BAR,
        x_label="Year",
        y_label="Equity cash flow",
    ),
    "FLGT_TAKE": ChartTemplate(
        template_id="FLGT_TAKE",
        title="Front-Loaded Government Take",
        chart_type=ChartType.BAR,
        x_label="Year",
        y_label="Government take",
    ),
    "PRODUCTION_SUMMARY": ChartTemplate(
        template_id="PRODUCTION_SUMMARY",
        title="Production Summary",
        chart_type=ChartType.LINE,
        x_label="Year",
        y_label="Production rate / volume",
    ),
    "PRODUCTION_PROFILE": ChartTemplate(
        template_id="PRODUCTION_PROFILE",
        title="Production Profile",
        chart_type=ChartType.LINE,
        x_label="Year",
        y_label="Production rate / cumulative",
    ),
}
