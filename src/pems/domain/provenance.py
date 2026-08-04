"""Golden Master provenance for CaseInput fields."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FieldProvenance:
    """Traceability from PEMS field to GM cell."""

    module: str
    sheet: str
    cell: str
    parameter_name: str
    classification: str
    unit: str | None
    downstream: str | None = None


# Authoritative map from EC_IO_PARAMETER_CONTRACT + EQUITY_DASH_SHARE_INPUT
CASE_INPUT_PROVENANCE: dict[str, FieldProvenance] = {
    "equity_share_company_1": FieldProvenance(
        "equity",
        "Equity Dash",
        "C4",
        "equity_share_company_1",
        "CONFIRMED_INPUT",
        "fraction",
        "equity NCF / RESULTS",
    ),
    "project_equity_total": FieldProvenance(
        "equity",
        "Equity Dash",
        "C6",
        "project_equity_total",
        "DEFAULT_STRUCTURAL",
        "fraction",
        "equity C5 derived",
    ),
    "project_start_year": FieldProvenance(
        "ec_io", "Ec_IO", "C5", "project_start_year", "ASSUMPTION", "year", "timeline"
    ),
    "production_days_per_year": FieldProvenance(
        "ec_io", "Ec_IO", "C7", "production_days_per_year", "ASSUMPTION", "days/year", "production"
    ),
    "oil_price_usd_bbl": FieldProvenance(
        "ec_io", "Ec_IO", "C12", "oil_price_usd_bbl", "ASSUMPTION", "$/bbl", "royalties/revenue"
    ),
    "price_escalator": FieldProvenance(
        "ec_io", "Ec_IO", "C14", "price_escalator", "DEFAULT_STRUCTURAL", "fraction", "price_format"
    ),
    "hurdle_rate": FieldProvenance(
        "ec_io", "Ec_IO", "C15", "hurdle_rate", "ASSUMPTION", "fraction/yr", "discount"
    ),
    "gas_price_usd_mscf": FieldProvenance(
        "ec_io", "Ec_IO", "C17", "gas_price_usd_mscf", "ASSUMPTION", "$/Mscf", "FLGT/revenue"
    ),
    "gas_flare_penalty_usd_mscf": FieldProvenance(
        "ec_io", "Ec_IO", "C18", "gas_flare_penalty_usd_mscf", "FORMULA_COEFFICIENT", "$/Mscf", None
    ),
    "dom_gas_fraction": FieldProvenance(
        "ec_io", "Ec_IO", "C19", "dom_gas_fraction", "FORMULA_COEFFICIENT", "fraction", None
    ),
    "duties_rate": FieldProvenance(
        "ec_io", "Ec_IO", "C20", "duties_rate", "DEFAULT_STRUCTURAL", "fraction", "costs"
    ),
    "vat_rate": FieldProvenance(
        "ec_io", "Ec_IO", "C21", "vat_rate", "DEFAULT_STRUCTURAL", "fraction", "costs"
    ),
    "asset_salvage_frac_of_retention": FieldProvenance(
        "ec_io",
        "Ec_IO",
        "C22",
        "asset_salvage_frac_of_retention",
        "DEFAULT_STRUCTURAL",
        "fraction",
        None,
    ),
    "nag_crl": FieldProvenance(
        "ec_io", "Ec_IO", "C23", "nag_crl", "DEFAULT_STRUCTURAL", "fraction", None
    ),
    "nag_ita": FieldProvenance(
        "ec_io", "Ec_IO", "C24", "nag_ita", "FORMULA_COEFFICIENT", "fraction", None
    ),
    "nag_min_tax_rate": FieldProvenance(
        "ec_io", "Ec_IO", "C25", "nag_min_tax_rate", "ASSUMPTION", "fraction", None
    ),
    "nag_cpr": FieldProvenance(
        "ec_io", "Ec_IO", "C26", "nag_cpr", "DEFAULT_STRUCTURAL", "fraction", None
    ),
    "history_year": FieldProvenance(
        "ec_io", "Ec_IO", "D28", "history_year", "ASSUMPTION", "year", "history filter"
    ),
    "complete_year": FieldProvenance(
        "ec_io", "Ec_IO", "D30", "complete_year", "ASSUMPTION", "year", "history filter"
    ),
    "asset_analysis_type": FieldProvenance(
        "ec_io",
        "Ec_IO",
        "C4",
        "asset_analysis_type",
        "CASE_ATTRIBUTE_TEXT",
        None,
        "history mode",
    ),
    "block_field_oil": FieldProvenance(
        "ec_io", "Ec_IO", "G18", "block_field_oil", "CASE_ATTRIBUTE_TEXT", None, "field select"
    ),
    "terrain": FieldProvenance(
        "ec_io", "Ec_IO", "G20", "terrain", "CASE_ATTRIBUTE_TEXT", None, "royalty law select"
    ),
    "gas_utilization": FieldProvenance(
        "ec_io", "Ec_IO", "G21", "gas_utilization", "CASE_ATTRIBUTE_TEXT", None, "gas royalty"
    ),
    "licence_lease_status": FieldProvenance(
        "ec_io", "Ec_IO", "G22", "licence_lease_status", "CASE_ATTRIBUTE_TEXT", None, "CRL"
    ),
    "pfs_contract_type": FieldProvenance(
        "ec_io", "Ec_IO", "G24", "pfs_contract_type", "CASE_ATTRIBUTE_TEXT", None, "PSC branch"
    ),
    "country": FieldProvenance(
        "ec_io", "Ec_IO", "G25", "country", "CASE_ATTRIBUTE_TEXT", None, "identity"
    ),
    "fiscal_regime_label": FieldProvenance(
        "ec_io", "Ec_IO", "G26", "fiscal_regime_label", "CASE_ATTRIBUTE_TEXT", None, "law package"
    ),
    # Production Profile (PRODUCTION_PROFILE_CONTRACT)
    "pp_mode": FieldProvenance(
        "production", "Production Profile", "B2", "pp_mode", "ASSUMPTION", "enum", "UR path"
    ),
    "stoiip_inplace": FieldProvenance(
        "production",
        "Production Profile",
        "C2",
        "stoiip_inplace",
        "DERIVED",
        "MMbbls",
        "oil UR",
    ),
    "giip_inplace": FieldProvenance(
        "production", "Production Profile", "F2", "giip_inplace", "DERIVED", "Bscf", "gas UR"
    ),
    "oil_rf": FieldProvenance(
        "production", "Production Profile", "C3", "oil_rf", "FORMULA_COEFFICIENT", "fraction", "UR"
    ),
    "gas_rf": FieldProvenance(
        "production", "Production Profile", "F3", "gas_rf", "FORMULA_COEFFICIENT", "fraction", "UR"
    ),
    "gor_scf_bbl": FieldProvenance(
        "production", "Production Profile", "F5", "gor_scf_bbl", "ASSUMPTION", "scf/bbl", "AG gas"
    ),
    "prod_start_lag_years": FieldProvenance(
        "production",
        "Production Profile",
        "C7",
        "prod_start_lag_years",
        "DEFAULT_STRUCTURAL",
        "years",
        "timing",
    ),
    "year_end_anchor": FieldProvenance(
        "production", "Production Profile", "C8", "year_end_anchor", "ASSUMPTION", "year", "calendar"
    ),
    "pp_days_in_year": FieldProvenance(
        "production",
        "Production Profile",
        "C9",
        "pp_days_in_year",
        "FORMULA_COEFFICIENT",
        "days",
        "annualization",
    ),
    "eff_decline_rate": FieldProvenance(
        "production",
        "Production Profile",
        "L7",
        "eff_decline_rate",
        "ASSUMPTION",
        "fraction/yr",
        "a3 term ×0 on GM",
    ),
    "qi_buildup": FieldProvenance(
        "production",
        "Production Profile",
        "C12",
        "qi_buildup",
        "FORMULA_COEFFICIENT",
        "BOPD or Mscf/d",
        "build-up",
    ),
    "qp_plateau": FieldProvenance(
        "production",
        "Production Profile",
        "C13",
        "qp_plateau",
        "FORMULA_COEFFICIENT",
        "BOPD or Mscf/d",
        "plateau",
    ),
    "qel_end": FieldProvenance(
        "production",
        "Production Profile",
        "I13",
        "qel_end",
        "FORMULA_COEFFICIENT",
        "BOPD or Mscf/d",
        "decline",
    ),
    "t1_buildup_yrs": FieldProvenance(
        "production",
        "Production Profile",
        "C14",
        "t1_buildup_yrs",
        "DEFAULT_STRUCTURAL",
        "years",
        "build-up",
    ),
    "t2_plateau_yrs": FieldProvenance(
        "production",
        "Production Profile",
        "F14",
        "t2_plateau_yrs",
        "DEFAULT_STRUCTURAL",
        "years",
        "plateau",
    ),
    "gas_boe_factor": FieldProvenance(
        "production",
        "Prod_Summary",
        "Y48",
        "gas_boe_factor",
        "DEFAULT_STRUCTURAL",
        "boe/bscf-class",
        "Y49",
    ),
    "analysis_oil_scale": FieldProvenance(
        "production", "Analysis", "N8", "analysis_oil_scale", "DEFAULT_STRUCTURAL", "fraction", "CT/CU"
    ),
    "analysis_gas_scale": FieldProvenance(
        "production", "Analysis", "N9", "analysis_gas_scale", "DEFAULT_STRUCTURAL", "fraction", "CO/CP"
    ),
    "oil_block_daily": FieldProvenance(
        "production",
        "Block_Oil Data",
        "selected",
        "oil_block_daily",
        "INPUT",
        "mb/d",
        "Prod_Summary T",
    ),
    "oil_block_annual": FieldProvenance(
        "production",
        "Block_Oil Data",
        "selected",
        "oil_block_annual",
        "DERIVED",
        "mmbbls",
        "Prod_Summary U",
    ),
    "gas_block_daily": FieldProvenance(
        "production",
        "Block_Gas Data",
        "selected",
        "gas_block_daily",
        "INPUT",
        "mmscf/d",
        "Prod_Summary W",
    ),
    "gas_block_annual": FieldProvenance(
        "production",
        "Block_Gas Data",
        "selected",
        "gas_block_annual",
        "INPUT",
        "bscf",
        "Prod_Summary X",
    ),
    "cost_mode_field": FieldProvenance(
        "costs", "Ec_IO", "G23", "cost_mode_field", "CASE_ATTRIBUTE_TEXT", None, "Block_TC select"
    ),
    "oil_tc_exploration": FieldProvenance(
        "costs", "Cap_Allow", "FF", "oil_tc_exploration", "ASSUMPTION", "$mm", "FK/FP"
    ),
    "oil_tc_capex_wells": FieldProvenance(
        "costs", "Cap_Allow", "FG", "oil_tc_capex_wells", "ASSUMPTION", "$mm", "FK/FQ"
    ),
    "oil_tc_capex_facilities": FieldProvenance(
        "costs", "Cap_Allow", "FH", "oil_tc_capex_facilities", "ASSUMPTION", "$mm", "FK/FQ"
    ),
    "oil_tc_opex": FieldProvenance(
        "costs", "Cap_Allow", "FI", "oil_tc_opex", "DERIVED", "$mm", "FL FI48"
    ),
    "ca_rates": FieldProvenance(
        "costs", "Cap_Allow", "FR5:FR9", "ca_rates", "ASSUMPTION", "fraction", "CA surface"
    ),
    "opex_escalation_rate": FieldProvenance(
        "costs", "Block_TC", "FW3", "opex_escalation_rate", "FORMULA_COEFFICIENT", "fraction", "G7"
    ),
    "oil_sln_by_year": FieldProvenance(
        "costs", "Cap_Allow", "GX", "oil_sln_by_year", "DERIVED", "$mm", "CR/HT"
    ),
    "oil_acq_allowance_by_year": FieldProvenance(
        "costs", "Cap_Allow", "HC", "oil_acq_allowance_by_year", "DERIVED", "$mm", "CR/HT"
    ),
    "acquisition_cost": FieldProvenance(
        "costs", "Cap_Allow", "HB", "acquisition_cost", "ASSUMPTION", "$mm", "HC"
    ),
}
