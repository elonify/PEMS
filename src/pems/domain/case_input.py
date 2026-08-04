"""Canonical CaseInput model — single representation for manual and import paths.

Authority:
  docs/02_SPECIFICATIONS/modules/EC_IO_PARAMETER_CONTRACT.md
  docs/02_SPECIFICATIONS/INPUT_SCHEMA_CRITICAL_PATH.md
  docs/02_SPECIFICATIONS/modules/EQUITY_DASH_SHARE_INPUT.md
  docs/02_SPECIFICATIONS/modules/PRODUCTION_PROFILE_CONTRACT.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from typing import Any, Literal

from pems.domain.provenance import CASE_INPUT_PROVENANCE

InputProvenance = Literal["manual", "excel_import", "unknown"]


@dataclass
class CaseInput:
    """Scenario inputs shared by all calculation modules."""

    # Equity (CLOSED: C4 INPUT)
    equity_share_company_1: float | None = None
    project_equity_total: float | None = None  # Equity Dash C6; default structural

    # Ec_IO numeric drivers
    project_start_year: int | None = None
    production_days_per_year: float | None = None
    oil_price_usd_bbl: float | None = None
    price_escalator: float | None = None
    hurdle_rate: float | None = None
    gas_price_usd_mscf: float | None = None
    gas_flare_penalty_usd_mscf: float | None = None
    dom_gas_fraction: float | None = None
    duties_rate: float | None = None
    vat_rate: float | None = None
    asset_salvage_frac_of_retention: float | None = None
    nag_crl: float | None = None
    nag_ita: float | None = None
    nag_min_tax_rate: float | None = None
    nag_cpr: float | None = None
    history_year: int | None = None
    complete_year: int | None = None

    # Optional: project life from Production (Ec_IO C6 is HUB/upstream-derived)
    project_life_years: float | None = None

    # Case attributes
    asset_analysis_type: str | None = None
    terrain: str | None = None
    gas_utilization: str | None = None
    licence_lease_status: str | None = None
    pfs_contract_type: str | None = None
    country: str | None = None
    fiscal_regime_label: str | None = None
    block_field_oil: str | None = None
    # block_field_gas defaults to oil field when not independently set (GM G19=G18)
    block_field_gas: str | None = None

    # --- Production Profile parameters (PRODUCTION_PROFILE_CONTRACT §3) ---
    pp_mode: str | None = None  # STOIIP | GIIP
    stoiip_inplace: float | None = None  # MMbbls (interface; reservoir not READY)
    giip_inplace: float | None = None  # Bscf
    oil_rf: float | None = None
    gas_rf: float | None = None
    gor_scf_bbl: float | None = None
    prod_start_lag_years: float | None = None
    year_end_anchor: int | None = None
    pp_days_in_year: float | None = None
    eff_decline_rate: float | None = None
    qi_buildup: float | None = None
    qp_plateau: float | None = None
    qel_end: float | None = None
    t1_buildup_yrs: float | None = None
    t2_plateau_yrs: float | None = None
    gas_boe_factor: float | None = None  # Prod_Summary Y48 default 5.804

    # Analysis sensitivity scale on block rates (Analysis!N8/N9); GM GTC = 0
    analysis_oil_scale: float | None = None
    analysis_gas_scale: float | None = None

    # Selected field block series for GTC / block path: list of [year, value]
    # Oil daily mb/d; oil annual mmbbls; gas daily mmscf/d; gas annual bscf
    oil_block_daily: list[list[float]] | None = None
    oil_block_annual: list[list[float]] | None = None
    gas_block_daily: list[list[float]] | None = None
    gas_block_annual: list[list[float]] | None = None

    # --- Costs schedules (COSTS_PARAMETER_CONTRACT — selected Cap_Allow path) ---
    # Each series: list of [year, $mm]. Source = selected-field consolidated TC after G1/G2/G7.
    cost_mode_field: str | None = None  # Ec_IO G23 (typically = G18)
    oil_tc_exploration: list[list[float]] | None = None  # Cap_Allow FF / Block_TC FY
    oil_tc_capex_wells: list[list[float]] | None = None  # FG / FZ
    oil_tc_capex_facilities: list[list[float]] | None = None  # FH / GA
    oil_tc_opex: list[list[float]] | None = None  # FI escalated OPEX / GB
    oil_tc_abandonment: list[list[float]] | None = None  # Block_TC Abandonment (optional)
    gas_tc_exploration: list[list[float]] | None = None
    gas_tc_capex_wells: list[list[float]] | None = None
    gas_tc_capex_facilities: list[list[float]] | None = None
    gas_tc_opex: list[list[float]] | None = None
    gas_tc_abandonment: list[list[float]] | None = None
    # Capital allowance rates Y1–Y5 (Cap_Allow FR5:FR9) — LAW-aligned, not CaseInput invent
    ca_rates: list[float] | None = None
    # OPEX escalation rate Block_TC!FW3; factor (1+rate)^(year-base)
    opex_escalation_rate: float | None = None
    # G8 surfaces (array-formula bodies deferred; series imported for CR hand-off parity)
    oil_sln_by_year: list[list[float]] | None = None  # Cap_Allow GX
    oil_acq_allowance_by_year: list[list[float]] | None = None  # Cap_Allow HC
    gas_sln_by_year: list[list[float]] | None = None
    gas_acq_allowance_by_year: list[list[float]] | None = None
    acquisition_cost: float | None = None  # Cap_Allow HB

    # Provenance
    source: InputProvenance = "unknown"
    source_path: str | None = None
    extras: dict[str, Any] = field(default_factory=dict)

    def is_complete_for_gtc001(self) -> bool:
        required = (
            self.equity_share_company_1,
            self.project_start_year,
            self.production_days_per_year,
            self.hurdle_rate,
            self.oil_price_usd_bbl,
            self.gas_price_usd_mscf,
            self.price_escalator,
            self.asset_analysis_type,
            self.terrain,
            self.gas_utilization,
            self.licence_lease_status,
            self.pfs_contract_type,
        )
        return all(v is not None for v in required)

    def to_serializable(self) -> dict[str, Any]:
        """Deterministic dict for GTC / audit (no provenance objects)."""
        d = asdict(self)
        return {k: d[k] for k in sorted(d.keys())}

    @classmethod
    def field_names(cls) -> tuple[str, ...]:
        return tuple(
            f.name for f in fields(cls) if f.name not in ("extras", "source", "source_path")
        )

    def provenance_for(self, field_name: str):
        return CASE_INPUT_PROVENANCE.get(field_name)
