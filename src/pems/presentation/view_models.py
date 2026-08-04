"""Presentation view models — project RunBundle → display rows.

Does not recompute NPV/IRR/production/costs/FLGT/CR/RESULTS.
IRR failure: preserve NO_VALID_IRR; surface GRR from ResultsResult (K11/N11).
MIRR: not present on RESULTS Equity surface — not invented here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pems.application.run_service import RunBundle
from pems.presentation.formats import (
    format_currency_usd,
    format_money_mm,
    format_number,
    format_percent,
    format_text,
    format_years,
    is_unavailable,
)


@dataclass
class DisplayRow:
    """Single presentation row."""

    id: str
    label: str
    display: str
    unit: str = ""
    raw: Any = None
    status: str = "ok"  # ok | unavailable | deferred
    note: str = ""
    source: str = ""  # trace e.g. RESULTS Equity!K8


@dataclass
class TableModel:
    title: str
    columns: list[str]
    rows: list[list[str]]
    notes: list[str] = field(default_factory=list)


@dataclass
class PresentationBundle:
    nav_title: str
    case_rows: list[DisplayRow]
    law_rows: list[DisplayRow]
    results_kpi_rows: list[DisplayRow]
    production_table: TableModel
    costs_table: TableModel
    fiscal_table: TableModel
    cashflow_table: TableModel
    validation_rows: list[DisplayRow]
    reports_rows: list[DisplayRow]
    deferred_banners: list[str]
    notes: list[str] = field(default_factory=list)


def _irr_row(
    *,
    row_id: str,
    label: str,
    irr: Any,
    grr: Any,
    irr_cell: str,
    grr_cell: str,
) -> DisplayRow:
    """Primary IRR + alternative GRR when IRR unavailable (Phase 1H requirement)."""
    if is_unavailable(irr) or (isinstance(irr, str) and "NO_VALID" in irr.upper()):
        alt = format_percent(grr) if grr is not None and not is_unavailable(grr) else "—"
        note = (
            f"Primary IRR = NO_VALID_IRR / UNAVAILABLE. "
            f"Alternative return KPI GRR ({grr_cell}) = {alt}. "
            f"MIRR not mapped on RESULTS Equity surface (not invented)."
        )
        return DisplayRow(
            id=row_id,
            label=label,
            display="UNAVAILABLE",
            unit="%",
            raw=irr if irr is not None else "NO_VALID_IRR",
            status="unavailable",
            note=note,
            source=f"{irr_cell}; alt {grr_cell}",
        )
    return DisplayRow(
        id=row_id,
        label=label,
        display=format_percent(irr),
        unit="%",
        raw=irr,
        status="ok",
        note=f"GRR also available: {format_percent(grr)} ({grr_cell})" if grr is not None else "",
        source=irr_cell,
    )


def build_presentation(bundle: RunBundle) -> PresentationBundle:
    c = bundle.case
    r = bundle.results
    prod = bundle.production
    costs = bundle.costs
    flgt = bundle.flgt
    cr = bundle.cr_ncf

    case_rows = [
        DisplayRow("equity_c4", "Equity share (company 1)", format_percent(c.equity_share_company_1, 0), "%", c.equity_share_company_1, source="Equity Dash!C4"),
        DisplayRow("field", "Field", format_text(c.block_field_oil), "", c.block_field_oil, source="Ec_IO!G18"),
        DisplayRow("terrain", "Terrain", format_text(c.terrain), "", c.terrain, source="Ec_IO!G20"),
        DisplayRow("licence", "Licence / lease", format_text(c.licence_lease_status), "", c.licence_lease_status, source="Ec_IO!G22"),
        DisplayRow("pfs", "PFS / contract", format_text(c.pfs_contract_type), "", c.pfs_contract_type, source="Ec_IO!G24"),
        DisplayRow("country", "Country", format_text(c.country), "", c.country, source="Ec_IO!G25"),
        DisplayRow("regime", "Fiscal regime", format_text(c.fiscal_regime_label), "", c.fiscal_regime_label, source="Ec_IO!G26"),
        DisplayRow("start_year", "Project start year", format_text(c.project_start_year), "", c.project_start_year, source="Ec_IO!C5"),
        DisplayRow("life", "Project life", format_number(c.project_life_years or prod.project_life_years, 0), "years", c.project_life_years, source="Ec_IO!C6 / Prod AF26"),
        DisplayRow("oil_price", "Oil price", format_number(c.oil_price_usd_bbl, 2), "$/bbl", c.oil_price_usd_bbl, source="Ec_IO!C12"),
        DisplayRow("gas_price", "Gas price", format_number(c.gas_price_usd_mscf, 2), "$/Mscf", c.gas_price_usd_mscf, source="Ec_IO!C17"),
        DisplayRow("hurdle", "Hurdle rate", format_percent(c.hurdle_rate), "%", c.hurdle_rate, source="Ec_IO!C15"),
        DisplayRow("gas_util", "Gas utilization", format_text(c.gas_utilization), "", c.gas_utilization, source="Ec_IO!G21"),
        DisplayRow("asset_type", "Asset analysis type", format_text(c.asset_analysis_type), "", c.asset_analysis_type, source="Ec_IO!C4"),
    ]

    law = (c.extras or {}).get("fiscal_law") or {}
    law_rows = [
        DisplayRow("law_note", "Fiscal Terms_PIA", "LAW TABLE (read-only)", "", status="ok", note="Not CaseInput", source="Fiscal Terms_PIA"),
        DisplayRow("crl_new", "CRL new acreage", format_percent(law.get("crl_new_acreage", 0.7)), "%", law.get("crl_new_acreage"), source="Fiscal Terms_PIA law"),
        DisplayRow("hcdt", "HCDT rate", format_percent(law.get("hcdt_rate", 0.03), 0), "%", law.get("hcdt_rate"), source="Fiscal Terms_PIA!T72"),
        DisplayRow("nddc", "NDDC rate", format_percent(law.get("nddc_rate", 0.03), 0), "%", law.get("nddc_rate"), source="Fiscal Terms_PIA!T73"),
        DisplayRow("gas_dom", "Gas royalty Dom", format_percent(law.get("gas_rate_dom", 0.025)), "%", law.get("gas_rate_dom"), source="law table"),
        DisplayRow("gas_out", "Gas royalty Out", format_percent(law.get("gas_rate_out", 0.05)), "%", law.get("gas_rate_out"), source="law table"),
    ]

    kpi: list[DisplayRow] = [
        DisplayRow("id_country", "Country", format_text(r.l2_country), source="RESULTS Equity!L2"),
        DisplayRow("id_regime", "Fiscal regime", format_text(r.l3_regime), source="RESULTS Equity!L3"),
        DisplayRow("id_field", "Field", format_text(r.c5_field), source="RESULTS Equity!C5"),
        DisplayRow("id_pfs", "PFS", format_text(r.l5_pfs), source="RESULTS Equity!L5"),
        DisplayRow("id_licence", "Licence", format_text(r.c6_licence), source="RESULTS Equity!C6"),
        DisplayRow("id_terrain", "Terrain", format_text(r.c7_terrain), source="RESULTS Equity!C7"),
        DisplayRow("id_equity", "Equity share", format_text(r.c8_equity_text), source="RESULTS Equity!C8"),
        DisplayRow("hurdle", "Discount rate", format_percent(r.h7_hurdle), "%", r.h7_hurdle, source="RESULTS Equity!H7"),
        DisplayRow("npv_host_bit", "Host Govt BIT NPV", format_money_mm(r.j7_host_npv_bit), "$mm", r.j7_host_npv_bit, source="RESULTS Equity!J7"),
        DisplayRow("npv_con_bit", "Contractor BIT NPV", format_money_mm(r.k7_contractor_npv_bit), "$mm", r.k7_contractor_npv_bit, source="RESULTS Equity!K7"),
        DisplayRow("npv_host_ait", "Host Govt AIT NPV", format_money_mm(r.m7_host_npv_ait), "$mm", r.m7_host_npv_ait, source="RESULTS Equity!M7"),
        DisplayRow("npv_con_ait", "Contractor AIT NPV", format_money_mm(r.n7_contractor_npv_ait), "$mm", r.n7_contractor_npv_ait, source="RESULTS Equity!N7"),
        _irr_row(
            row_id="irr_bit",
            label="IRR (BIT)",
            irr=r.k8_irr_bit,
            grr=r.k11_grr_bit,
            irr_cell="RESULTS Equity!K8",
            grr_cell="RESULTS Equity!K11",
        ),
        _irr_row(
            row_id="irr_ait",
            label="IRR (AIT)",
            irr=r.n8_irr_ait,
            grr=r.n11_grr_ait,
            irr_cell="RESULTS Equity!N8",
            grr_cell="RESULTS Equity!N11",
        ),
        DisplayRow("grr_bit", "GRR (BIT)", format_percent(r.k11_grr_bit), "%", r.k11_grr_bit, source="RESULTS Equity!K11"),
        DisplayRow("grr_ait", "GRR (AIT)", format_percent(r.n11_grr_ait), "%", r.n11_grr_ait, source="RESULTS Equity!N11"),
        DisplayRow("pvr_bit", "PVR (BIT)", format_number(r.k9_pvr_bit), "", r.k9_pvr_bit, source="RESULTS Equity!K9"),
        DisplayRow("pvr_ait", "PVR (AIT)", format_number(r.n9_pvr_ait), "", r.n9_pvr_ait, source="RESULTS Equity!N9"),
        DisplayRow("pi_bit", "PI (BIT)", format_number(r.k10_pi_bit), "", r.k10_pi_bit, source="RESULTS Equity!K10"),
        DisplayRow("pi_ait", "PI (AIT)", format_number(r.n10_pi_ait), "", r.n10_pi_ait, source="RESULTS Equity!N10"),
        DisplayRow("payout_bit", "Disc. payout BIT", format_years(r.k14_payout_bit), "years", r.k14_payout_bit, source="RESULTS Equity!K14"),
        DisplayRow("payout_ait", "Disc. payout AIT", format_years(r.n14_payout_ait), "years", r.n14_payout_ait, source="RESULTS Equity!N14"),
        DisplayRow("rev_gross", "Gross revenue (equity)", format_currency_usd(r.j18_gross_rev_eq), "$ (label $MM)", r.j18_gross_rev_eq, source="RESULTS Equity!J18"),
        DisplayRow("roy_tot", "Total royalty (equity)", format_money_mm(r.h25_total_royalty_eq), "$mm", r.h25_total_royalty_eq, source="RESULTS Equity!H25"),
        DisplayRow("err", "ERR", format_percent(r.h26_err), "%", r.h26_err, source="RESULTS Equity!H26"),
        DisplayRow("tax_tot", "Total tax (equity)", format_money_mm(r.j25_total_tax_eq), "$mm", r.j25_total_tax_eq, source="RESULTS Equity!J25"),
        DisplayRow("prod_oil", "Oil production (equity)", format_number(r.n22_oil_prod_eq, 3), "MMbbls", r.n22_oil_prod_eq, source="RESULTS Equity!N22"),
        DisplayRow("prod_gas", "Gas (equity Mmboe)", format_number(r.n23_gas_mmboe_eq, 3), "Mmboe", r.n23_gas_mmboe_eq, source="RESULTS Equity!N23"),
        DisplayRow("prod_tot", "Total Mmboe (equity)", format_number(r.n24_total_mmboe_eq, 3), "Mmboe", r.n24_total_mmboe_eq, source="RESULTS Equity!N24"),
        DisplayRow("gas_bscf", "Gas Bscf text", format_text(r.m23_gas_bscf_text), "", r.m23_gas_bscf_text, source="RESULTS Equity!M23"),
        DisplayRow("unit_tc", "Unit TC PV", format_currency_usd(r.h21_unit_pv_tc), "$/boe", r.h21_unit_pv_tc, source="RESULTS Equity!H21"),
        DisplayRow("mirr_note", "MIRR", "Not available on RESULTS Equity", "", status="deferred", note="No RESULTS MIRR cell in parameter contract — not invented", source="N/A"),
    ]

    # Production summary table
    prod_rows = [
        ["Oil EUR / max cum (V47)", format_number(prod.oil_eur_or_max_cum, 4), "MMbbls"],
        ["Gas max cum (Y47)", format_number(prod.gas_max_cum, 4), "Bscf"],
        ["Gas Mmboe (Y49)", format_number(prod.gas_mmboe, 4), "Mmboe"],
        ["Total Mmboe (Y50)", format_number(prod.total_mmboe, 4), "Mmboe"],
        ["Project life (AF26)", format_number(prod.project_life_years, 0), "years"],
        ["Path", format_text(prod.path_used), ""],
    ]
    # sample annual years
    years_p = sorted(prod.oil_annual_series.keys())[:12]
    for y in years_p:
        prod_rows.append(
            [
                str(y),
                f"oil {format_number(prod.oil_annual_series.get(y), 4)} / gas {format_number(prod.gas_annual_series.get(y), 4)}",
                "mmbbls / bscf",
            ]
        )
    production_table = TableModel(
        "Production summary & sample years",
        ["Item / Year", "Value", "Unit"],
        prod_rows,
        notes=["Full series available in DTO; sample first years shown"],
    )

    costs_rows = [
        ["PV OPEX N16", format_money_mm(costs.pv_opex_combined), "$mm"],
        ["Undisc OPEX S16", format_money_mm(costs.undisc_opex_combined), "$mm"],
        ["PV CAPEX N17", format_money_mm(costs.pv_capex_combined), "$mm"],
        ["Undisc CAPEX S17", format_money_mm(costs.undisc_capex_combined), "$mm"],
        ["PV TC N18", format_money_mm(costs.pv_tc_combined), "$mm"],
        ["Undisc TC S18", format_money_mm(costs.undisc_tc_combined), "$mm"],
        ["Oil FI48 OPEX undisc", format_money_mm(costs.oil.opex_undisc_total), "$mm"],
        ["Oil FL48 OPEX disc", format_money_mm(costs.oil.opex_disc_total), "$mm"],
        ["Oil FK48 CAPEX disc", format_money_mm(costs.oil.capex_disc_total), "$mm"],
    ]
    costs_table = TableModel("Costs / Cap_Allow hubs", ["Metric", "Value", "Unit"], costs_rows)

    fiscal_rows = [
        ["Oil revenue W51", format_money_mm(flgt.w51), "$mm"],
        ["Gas revenue X51", format_money_mm(flgt.x51), "$mm"],
        ["Total revenue Y51", format_money_mm(flgt.y51), "$mm"],
        ["Oil royalty AB51", format_money_mm(flgt.ab51), "$mm"],
        ["Gas royalty AC51", format_money_mm(flgt.ac51), "$mm"],
        ["Price royalty AD51", format_money_mm(flgt.ad51), "$mm"],
        ["Royalty sum AL51", format_money_mm(flgt.al51), "$mm"],
        ["ERR AM51", format_percent(flgt.am51), "%"],
        ["FLGT total AI51", format_money_mm(flgt.ai51), "$mm"],
    ]
    fiscal_table = TableModel("FLGT / Royalties totals", ["Metric", "Value", "Unit"], fiscal_rows)

    # Cash flow: Project NCF scalars + sample AF years
    cf_rows = [
        ["Host undisc AE51", format_money_mm(cr.ae51), "$mm"],
        ["Contractor undisc AF51", format_money_mm(cr.af51), "$mm"],
        ["Host disc AG51", format_money_mm(cr.ag51), "$mm"],
        ["Contractor disc AH51", format_money_mm(cr.ah51), "$mm"],
        ["Payout AJ51", format_years(cr.aj51), "years"],
        ["Project IRR AG58", format_percent(cr.ag58_irr) if not is_unavailable(cr.ag58_irr) else "UNAVAILABLE", "%"],
        ["AU14 IRR", "UNAVAILABLE" if is_unavailable(cr.au14_irr) else format_percent(cr.au14_irr), "%"],
        ["Equity AG51", format_money_mm(cr.equity_ag51), "$mm"],
        ["Equity AH51", format_money_mm(cr.equity_ah51), "$mm"],
    ]
    years_cf = list(cr.years)[:10] if cr.years else sorted(cr.contractor_af.keys())[:10]
    for y in years_cf:
        cf_rows.append(
            [
                f"AF {y}",
                format_money_mm(cr.contractor_af.get(y)),
                "$mm",
            ]
        )
    cashflow_table = TableModel(
        "CR / Project NCF (scalars + sample AF)",
        ["Metric", "Value", "Unit"],
        cf_rows,
        notes=["AU14 expected NO_VALID_IRR on GTC-001 path"],
    )

    val_rows = [
        DisplayRow("val_count", "Case validation issues", str(len(bundle.validation_errors)), source="validator"),
    ]
    for i, e in enumerate(bundle.validation_errors[:20]):
        val_rows.append(DisplayRow(f"err_{i}", "Issue", e, status="unavailable"))
    if not bundle.validation_errors:
        val_rows.append(DisplayRow("val_ok", "Status", "No CaseInput validation errors", status="ok"))
    val_rows.append(
        DisplayRow(
            "gtc_note",
            "GTC / full-system",
            "Phase 1G anchor comparison PASS; full independent VALIDATED NOT CLAIMED",
            status="ok",
            source="PHASE1G",
        )
    )

    reports_rows = [
        DisplayRow("rep_exec", "Executive summary", "Uses RESULTS KPIs from last run", source="REPORT_SPEC"),
        DisplayRow("rep_tech", "Technical / production", "Uses Production DTO", source="REPORT_SPEC"),
        DisplayRow("rep_fiscal", "Fiscal", "Uses FLGT DTO", source="REPORT_SPEC"),
        DisplayRow("rep_export", "Export", "Deferred (PDF/Word) — first slice shows dataset only", status="deferred"),
    ]

    deferred = [
        "Charts (41 Excel / dual-axis engine) — separate sub-gate",
        "Sensitivity / Analysis UI — DEFERRED",
        "Monte Carlo — DEFERRED",
        "MIRR — not on RESULTS Equity contract (not invented)",
    ]

    return PresentationBundle(
        nav_title="PEMS — Petroleum Economics Modeling System",
        case_rows=case_rows,
        law_rows=law_rows,
        results_kpi_rows=kpi,
        production_table=production_table,
        costs_table=costs_table,
        fiscal_table=fiscal_table,
        cashflow_table=cashflow_table,
        validation_rows=val_rows,
        reports_rows=reports_rows,
        deferred_banners=deferred,
        notes=list(bundle.notes),
    )
