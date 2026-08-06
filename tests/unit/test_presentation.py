"""Phase 1H presentation tests PT01–PT10 (targeted; no full GUI required)."""

from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

from pems.application.run_service import RunBundle, RunService
from pems.calculations.modules.costs import CostsResult
from pems.calculations.modules.cr_ncf import CrNcfResult
from pems.calculations.modules.ec_io import EcIoResult
from pems.calculations.modules.flgt_royalties import FlgtResult
from pems.calculations.modules.production import ProductionResult
from pems.calculations.modules.results import ResultsResult
from pems.domain.manual_input import case_input_from_mapping
from pems.presentation.formats import format_percent, is_unavailable
from pems.presentation.view_models import _irr_row, build_presentation

ROOT = Path(__file__).resolve().parents[2]


def _minimal_bundle(*, irr_bit="NO_VALID_IRR", irr_ait="NO_VALID_IRR") -> RunBundle:
    case = case_input_from_mapping(
        {
            "country": "Nigeria",
            "fiscal_regime_label": "PIA 2021",
            "pfs_contract_type": "PSC/SC",
            "block_field_oil": "Ebiya Field",
            "licence_lease_status": "New Acreage",
            "terrain": "Shallow Water (<200m water depth)",
            "equity_share_company_1": 0.49,
            "hurdle_rate": 0.15,
            "project_life_years": 15.0,
            "project_start_year": 2027,
            "oil_price_usd_bbl": 50.0,
            "gas_price_usd_mscf": 2.18,
        }
    )
    res = ResultsResult(
        l2_country="Nigeria",
        l3_regime="PIA 2021",
        c5_field="Ebiya Field",
        l5_pfs="PSC/SC",
        c6_licence="New Acreage",
        c7_terrain="Shallow Water (<200m water depth)",
        c8_equity_text="Equity Share =49%",
        h7_hurdle=0.15,
        j7_host_npv_bit=10.0,
        k7_contractor_npv_bit=20.0,
        m7_host_npv_ait=12.0,
        n7_contractor_npv_ait=8.0,
        k8_irr_bit=irr_bit,
        n8_irr_ait=irr_ait,
        k9_pvr_bit=0.4,
        n9_pvr_ait=0.2,
        k10_pi_bit=1.4,
        n10_pi_ait=1.2,
        k11_grr_bit=0.177,
        n11_grr_ait=0.165,
        k14_payout_bit=5.0,
        n14_payout_ait=5.1,
        j18_gross_rev_eq=100.0,
        h25_total_royalty_eq=5.0,
        h26_err=0.05,
        j25_total_tax_eq=20.0,
        n22_oil_prod_eq=10.0,
        n23_gas_mmboe_eq=2.0,
        n24_total_mmboe_eq=12.0,
        m23_gas_bscf_text="(12.37 Bscf)",
        h21_unit_pv_tc=13.4,
    )
    cr = CrNcfResult(au14_irr="NO_VALID_IRR", ag58_irr=0.35, years=[2027], contractor_af={2027: 1.0})
    return RunBundle(
        case=case,
        ec_io=EcIoResult(case=case),
        production=ProductionResult(
            oil_eur_or_max_cum=22.0,
            gas_max_cum=25.0,
            gas_mmboe=4.0,
            total_mmboe=26.0,
            project_life_years=15.0,
            oil_annual_series={2027: 1.0},
            gas_annual_series={2027: 0.5},
        ),
        costs=CostsResult(pv_opex_combined=1.0, undisc_opex_combined=2.0),
        flgt=FlgtResult(w51=100.0, x51=10.0, y51=110.0, ab51=5.0, am51=0.05),
        cr_ncf=cr,
        results=res,
    )


def test_pt01_identity_display() -> None:
    pres = build_presentation(_minimal_bundle())
    labels = {r.id: r.display for r in pres.results_kpi_rows}
    assert labels["id_country"] == "Nigeria"
    assert labels["id_field"] == "Ebiya Field"
    assert "49%" in labels["id_equity"]


def test_pt02_formatting_percent_money() -> None:
    assert format_percent(0.15) == "15.00%"
    assert format_percent("NO_VALID_IRR") == "UNAVAILABLE"
    assert "0%" != format_percent("NO_VALID_IRR")
    assert is_unavailable("#NUM!")


def test_pt03_case_controls_from_caseinput_only() -> None:
    pres = build_presentation(_minimal_bundle())
    ids = {r.id for r in pres.case_rows}
    assert "equity_c4" in ids
    assert "oil_price" in ids
    # no invented field
    assert "made_up_ui_only" not in ids


def test_pt04_error_states_irr_unavailable_shows_grr() -> None:
    """IRR = NO_VALID_IRR → UNAVAILABLE; GRR displayed; never 0%."""
    row = _irr_row(
        row_id="irr_bit",
        label="IRR (BIT)",
        irr="NO_VALID_IRR",
        grr=0.177,
        irr_cell="RESULTS Equity!K8",
        grr_cell="RESULTS Equity!K11",
    )
    assert row.display == "UNAVAILABLE"
    assert row.status == "unavailable"
    assert "0%" not in row.display
    assert "GRR" in row.note
    assert "17.70%" in row.note or "0.177" in row.note or "17.7" in row.note
    assert "K11" in row.source

    pres = build_presentation(_minimal_bundle(irr_bit="NO_VALID_IRR", irr_ait="#NUM!"))
    irr_bit = next(r for r in pres.results_kpi_rows if r.id == "irr_bit")
    irr_ait = next(r for r in pres.results_kpi_rows if r.id == "irr_ait")
    assert irr_bit.display == "UNAVAILABLE"
    assert irr_ait.display == "UNAVAILABLE"
    assert "0.00%" not in irr_bit.display
    grr = next(r for r in pres.results_kpi_rows if r.id == "grr_bit")
    assert grr.display.endswith("%")
    assert grr.display != "0.00%" or grr.raw == 0  # real zero only if raw is zero


def test_pt04b_mirr_not_invented() -> None:
    pres = build_presentation(_minimal_bundle())
    mirr = next(r for r in pres.results_kpi_rows if r.id == "mirr_note")
    assert mirr.status == "deferred"
    assert "not invented" in mirr.note.lower() or "Not available" in mirr.display


def test_pt05_series_integrity_tables() -> None:
    pres = build_presentation(_minimal_bundle())
    assert len(pres.production_table.rows) >= 5
    assert pres.production_table.columns[0]
    assert any("2027" in row[0] for row in pres.production_table.rows)
    assert len(pres.cashflow_table.rows) >= 5


def test_pt06_kpi_source_traceability() -> None:
    pres = build_presentation(_minimal_bundle())
    for r in pres.results_kpi_rows:
        if r.id.startswith("npv") or r.id.startswith("irr"):
            assert r.source
            assert "RESULTS" in r.source or "N/A" in r.source or "K11" in r.source


def test_pt07_deferred_banners() -> None:
    pres = build_presentation(_minimal_bundle())
    text = " ".join(pres.deferred_banners).lower()
    assert "monte carlo" in text
    assert "sensitivity" in text or "analysis" in text
    assert "chart" in text


def test_pt08_no_calc_modules_imported_by_presentation() -> None:
    """Static: presentation package must not import calculation modules."""
    pres_root = ROOT / "src" / "pems" / "presentation"
    for path in pres_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith(
                    "pems.calculations"
                ), f"{path} imports {node.module}"
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith("pems.calculations")


def test_pt08b_ui_does_not_import_calc_modules() -> None:
    ui_root = ROOT / "src" / "pems" / "ui"
    for path in ui_root.rglob("*.py"):
        src = path.read_text(encoding="utf-8")
        assert "pems.calculations" not in src, f"{path} must not import calculations"


def test_pt09_numeric_irr_still_formats() -> None:
    row = _irr_row(
        row_id="irr",
        label="IRR",
        irr=0.3486,
        grr=0.165,
        irr_cell="N8",
        grr_cell="N11",
    )
    assert row.status == "ok"
    assert "34.86%" in row.display
    assert row.display != "UNAVAILABLE"


def test_pt10_build_presentation_uses_existing_dto_fields() -> None:
    """No UI calculation of NPV: raw equals ResultsResult field."""
    b = _minimal_bundle()
    pres = build_presentation(b)
    npv = next(r for r in pres.results_kpi_rows if r.id == "npv_con_ait")
    assert npv.raw == b.results.n7_contractor_npv_ait


def test_pt11_authorized_chart_datasets_attached() -> None:
    """Five authorized families appear as ChartDatasets on PresentationBundle."""
    from pems.calculations.modules.costs import StreamCostResult

    b = _minimal_bundle()
    # Enrich DTOs so series are non-empty (still projection-only).
    b.cr_ncf.years = [2027, 2028]
    b.cr_ncf.disc_contractor_ah = {2027: -1.0, 2028: 2.0}
    b.cr_ncf.disc_cncf_ai = {2027: -1.0, 2028: 1.0}
    b.production.oil_daily_series = {2027: 8.0, 2028: 7.0}
    b.production.oil_annual_series = {2027: 3.0, 2028: 2.5}
    b.production.oil_cum_series = {2027: 3.0, 2028: 5.5}
    b.production.gas_daily_series = {2027: 1.0}
    b.production.gas_annual_series = {2027: 0.4}
    b.production.gas_cum_series = {2027: 0.4}
    b.costs.oil = StreamCostResult(
        years=[2027],
        exploration={2027: 1.0},
        capex_wells={2027: 2.0},
        capex_facilities={2027: 3.0},
        opex={2027: 0.5},
    )
    b.costs.gas = StreamCostResult(
        years=[2027],
        exploration={2027: 0.1},
        capex_wells={2027: 0.2},
        capex_facilities={2027: 0.3},
        opex={2027: 0.05},
    )
    b.flgt.years = [2027]
    b.flgt.bonuses = {2027: 1.0}
    b.flgt.oil_royalty_mm = {2027: 0.5}

    pres = build_presentation(b)
    expected_ids = {
        "PROJECT_DISCOUNTED_NCF",
        "ECONOMIC_LIMIT",
        "OIL_PRODUCTION_SUMMARY",
        "GAS_PRODUCTION_SUMMARY",
        "OIL_COST_PROFILE",
        "GAS_COST_PROFILE",
        "FLGT_TAKE",
    }
    assert expected_ids <= set(pres.chart_datasets.keys())
    assert len(pres.chart_datasets) == 7
    for ds_id, ds in pres.chart_datasets.items():
        assert ds.dataset_id == ds_id
        assert len(ds.series) >= 1
    # Values projected from DTO (no recompute)
    ncf = pres.chart_datasets["PROJECT_DISCOUNTED_NCF"]
    annual = next(s for s in ncf.series if s.key == "annual_discounted_ncf")
    assert list(annual.y) == [-1.0, 2.0]


@pytest.mark.slow
def test_integration_run_service_from_gm_optional() -> None:
    """Optional GM path — skip if too heavy in quick loops; still valid PT."""
    gm = ROOT / "docs/workbook/Workbook_History/Econ_Model_PEMS_confirmed_2026-08-03.xlsx"
    if not gm.is_file():
        pytest.skip("GM missing")
    bundle = RunService().run_from_active_gm(ROOT)
    pres = build_presentation(bundle)
    assert any(r.id == "npv_con_ait" for r in pres.results_kpi_rows)
    # AU14 class: project path may be NO_VALID_IRR
    assert is_unavailable(bundle.cr_ncf.au14_irr) or isinstance(bundle.cr_ncf.au14_irr, float)
