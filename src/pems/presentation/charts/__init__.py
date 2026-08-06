"""Chart presentation package — datasets and templates (no economic calc)."""

from pems.presentation.charts.datasets import (
    ChartDataset,
    ChartSeries,
    cost_profile_dataset,
    discounted_ncf_dataset,
    economic_limit_dataset,
    equity_cashflow_dataset,
    flgt_take_dataset,
    production_profile_dataset,
    production_summary_dataset,
)
from pems.presentation.charts.templates import CHART_TEMPLATES, ChartTemplate, ChartType

__all__ = [
    "CHART_TEMPLATES",
    "ChartDataset",
    "ChartSeries",
    "ChartTemplate",
    "ChartType",
    "cost_profile_dataset",
    "discounted_ncf_dataset",
    "economic_limit_dataset",
    "equity_cashflow_dataset",
    "flgt_take_dataset",
    "production_profile_dataset",
    "production_summary_dataset",
]
