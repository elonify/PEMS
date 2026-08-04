"""Ec_IO module — pure derivations from CaseInput.

Authority: docs/02_SPECIFICATIONS/modules/EC_IO_PARAMETER_CONTRACT.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pems.domain.case_input import CaseInput


@dataclass
class EcIoResult:
    """Ec_IO pure outputs + CaseInput for GTC cell mapping."""

    price_format: str | None = None
    equity_share_company_2: float | None = None
    block_field_gas_effective: str | None = None
    cost_mode_field_effective: str | None = None
    history_end_year_e28: int | None = None
    forecast_anchor_d29: int | None = None
    project_end_year_e29: int | None = None
    case: CaseInput | None = None
    deferred_hub_outputs: list[str] = field(default_factory=list)

    def cell_map(self) -> dict[tuple[str, str], Any]:
        assert self.case is not None
        c = self.case
        m: dict[tuple[str, str], Any] = {
            ("Equity Dash", "C4"): c.equity_share_company_1,
            ("Equity Dash", "C6"): c.project_equity_total
            if c.project_equity_total is not None
            else 1.0,
            ("Equity Dash", "C5"): self.equity_share_company_2,
            ("Ec_IO", "C4"): c.asset_analysis_type,
            ("Ec_IO", "C5"): c.project_start_year,
            ("Ec_IO", "C7"): c.production_days_per_year,
            ("Ec_IO", "C12"): c.oil_price_usd_bbl,
            ("Ec_IO", "C13"): self.price_format,
            ("Ec_IO", "C14"): c.price_escalator,
            ("Ec_IO", "C15"): c.hurdle_rate,
            ("Ec_IO", "C17"): c.gas_price_usd_mscf,
            ("Ec_IO", "C18"): c.gas_flare_penalty_usd_mscf,
            ("Ec_IO", "C19"): c.dom_gas_fraction,
            ("Ec_IO", "C20"): c.duties_rate,
            ("Ec_IO", "C21"): c.vat_rate,
            ("Ec_IO", "C22"): c.asset_salvage_frac_of_retention,
            ("Ec_IO", "C23"): c.nag_crl,
            ("Ec_IO", "C24"): c.nag_ita,
            ("Ec_IO", "C25"): c.nag_min_tax_rate,
            ("Ec_IO", "C26"): c.nag_cpr,
            ("Ec_IO", "D28"): c.history_year,
            ("Ec_IO", "D30"): c.complete_year,
            ("Ec_IO", "G18"): c.block_field_oil,
            ("Ec_IO", "G19"): self.block_field_gas_effective,
            ("Ec_IO", "G20"): c.terrain,
            ("Ec_IO", "G21"): c.gas_utilization,
            ("Ec_IO", "G22"): c.licence_lease_status,
            ("Ec_IO", "G23"): self.cost_mode_field_effective,
            ("Ec_IO", "G24"): c.pfs_contract_type,
            ("Ec_IO", "G25"): c.country,
            ("Ec_IO", "G26"): c.fiscal_regime_label,
            ("Ec_IO", "E28"): self.history_end_year_e28,
            ("Ec_IO", "D29"): self.forecast_anchor_d29,
        }
        if self.project_end_year_e29 is not None:
            m[("Ec_IO", "E29")] = self.project_end_year_e29
        if c.project_life_years is not None:
            m[("Ec_IO", "C6")] = c.project_life_years
        return m


class EcIoModule:
    name = "ec_io"
    contract_path = "docs/02_SPECIFICATIONS/modules/EC_IO_PARAMETER_CONTRACT.md"

    DEFERRED_HUB = [
        "Ec_IO KPI hub G3–G15 (downstream NCF/FLGT)",
        "Ec_IO cost hub N16–S18 (Cap_Allow)",
        "Ec_IO revenue hub P16–P18 (FLGT)",
        "Sensitivity tables (PRESENTATION)",
    ]

    def run(self, case: CaseInput, upstream: dict[str, Any] | None = None) -> EcIoResult:
        upstream = upstream or {}
        life = case.project_life_years
        if life is None and upstream.get("project_life_years") is not None:
            life = float(upstream["project_life_years"])

        price_format = None
        if case.price_escalator is not None:
            price_format = "Real" if float(case.price_escalator) == 0.0 else "Nominal"

        total = 1.0 if case.project_equity_total is None else float(case.project_equity_total)
        equity_2 = None
        if case.equity_share_company_1 is not None:
            equity_2 = total - float(case.equity_share_company_1)

        field_oil = case.block_field_oil
        field_gas = case.block_field_gas if case.block_field_gas is not None else field_oil

        e28 = d29 = e29 = None
        if case.project_start_year is not None:
            e28 = int(case.project_start_year) - 1
            d29 = e28 + 1
            if life is not None:
                e29 = int(case.project_start_year) + int(float(life))

        case_out = case
        if life is not None and case.project_life_years != life:
            d = {**case.__dict__, "project_life_years": life}
            case_out = CaseInput(**d)

        return EcIoResult(
            price_format=price_format,
            equity_share_company_2=equity_2,
            block_field_gas_effective=field_gas,
            cost_mode_field_effective=field_oil,
            history_end_year_e28=e28,
            forecast_anchor_d29=d29,
            project_end_year_e29=e29,
            case=case_out,
            deferred_hub_outputs=list(self.DEFERRED_HUB),
        )
