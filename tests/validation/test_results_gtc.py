"""RESULTS Equity GTC-001 comparison — 63 KPI points (Phase 1F implementation gate)."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from pems.calculations.modules.costs import CostsModule
from pems.calculations.modules.cr_ncf import CrNcfModule
from pems.calculations.modules.flgt_royalties import FlgtRoyaltiesModule
from pems.calculations.modules.production import ProductionModule
from pems.calculations.modules.results import ResultsModule
from pems.gtc.compare import assert_gtc_bound_to_active_sha, compare_cell_map
from pems.infrastructure.golden_master import ACTIVE_GM_SHA256, verify_active_gm
from pems.validation.case_input_validator import validate_case_input

# Session-cached GM CaseInput (tests/conftest.py) — no per-test openpyxl reload
from tests.conftest import get_active_gm_case

ROOT = Path(__file__).resolve().parents[2]
GTC_CSV = (
    ROOT
    / "docs/workbook/Validation_Datasets/expected_outputs/GTC-001_kpi_and_intermediates.csv"
)


@pytest.fixture(scope="module")
def repo_root() -> Path:
    return ROOT


@pytest.fixture(scope="module")
def results_run(repo_root: Path):
    """One GM import (session cache) + upstream chain + RESULTS."""
    verify_active_gm(repo_root)
    case = get_active_gm_case(repo_root)
    assert validate_case_input(case) == []
    assert case.extras.get("ht_ncf_oil_equity_intermediates")
    assert case.extras.get("cit_ncf_equity_totals")
    prod = ProductionModule().run(case)
    costs = CostsModule().run(case)
    flgt = FlgtRoyaltiesModule().run(case, upstream={"production": prod})
    cr = CrNcfModule().run(
        case, upstream={"production": prod, "costs": costs, "flgt": flgt}
    )
    if case.project_life_years is None and prod.project_life_years is not None:
        case.project_life_years = float(prod.project_life_years)
    result = ResultsModule().run(
        case,
        upstream={
            "production": prod,
            "costs": costs,
            "flgt": flgt,
            "cr_ncf": cr,
        },
    )
    return case, result


def _load_results_expected() -> dict[tuple[str, str], float | str]:
    expected: dict[tuple[str, str], float | str] = {}
    with GTC_CSV.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("worksheet") != "RESULTS Equity":
                continue
            cell = row["cell"]
            raw = row["expected_value"]
            vtype = (row.get("value_type") or "").lower()
            key = ("RESULTS Equity", cell)
            if vtype == "float":
                expected[key] = float(raw)
            else:
                expected[key] = raw
    return expected


def test_gm_sha(repo_root: Path) -> None:
    verify_active_gm(repo_root)
    assert_gtc_bound_to_active_sha(repo_root)
    assert ACTIVE_GM_SHA256 == "D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA"


def test_results_gtc_63_points(results_run) -> None:
    _case, result = results_run
    pems = result.cell_map()
    expected = _load_results_expected()
    assert len(expected) >= 59  # 63 rows may include duplicate cells

    # Only compare cells present in expected pack
    pems_f = {k: pems[k] for k in expected if k in pems}
    missing = [k for k in expected if k not in pems]
    assert not missing, f"missing PEMS outputs for {missing}"

    res = compare_cell_map(pems_f, {k: expected[k] for k in pems_f})
    mismatches = [d for d in res.details if d["status"] == "mismatch"]
    assert res.mismatch == 0, (
        f"mismatches={mismatches}; exact={res.exact} tol={res.tolerance} "
        f"compared={res.total_compared}"
    )
    # unique expected keys compared
    assert res.exact + res.tolerance + res.expected_error_ok == len(pems_f)
    assert len(pems_f) >= 59


def test_results_high_value_anchors(results_run) -> None:
    _case, result = results_run
    m = result.cell_map()
    anchors = {
        ("RESULTS Equity", "N7"): 38.2636887228085,
        ("RESULTS Equity", "M7"): 73.2829654000993,
        ("RESULTS Equity", "J7"): 37.2107219837393,
        ("RESULTS Equity", "K7"): 73.018201942495,
        ("RESULTS Equity", "N8"): 0.348601049838934,
        ("RESULTS Equity", "K8"): 0.504693506064976,
        ("RESULTS Equity", "N14"): 5.13925728744526,
        ("RESULTS Equity", "H26"): 0.0542803358903504,
        ("RESULTS Equity", "J18"): 565.913065387258,
        ("RESULTS Equity", "H25"): 30.7179512739582,
        ("RESULTS Equity", "J25"): 106.475779799086,
    }
    res = compare_cell_map({k: m[k] for k in anchors}, anchors)
    assert res.mismatch == 0, [d for d in res.details if d["status"] == "mismatch"]
