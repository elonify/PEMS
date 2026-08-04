"""FLGT/Royalties GTC-001 comparison — Phase 1D mandatory anchors."""

from __future__ import annotations

from pathlib import Path

import pytest

from pems.calculations.modules.flgt_royalties import FlgtRoyaltiesModule
from pems.calculations.modules.production import ProductionModule
from pems.gtc.compare import (
    assert_gtc_bound_to_active_sha,
    compare_cell_map,
)
from pems.infrastructure.excel_import import import_case_input_from_active_gm
from pems.infrastructure.golden_master import ACTIVE_GM_SHA256, verify_active_gm
from pems.validation.case_input_validator import validate_case_input

ROOT = Path(__file__).resolve().parents[2]

# Contract / gate expected values (authoritative — do not rewrite)
CONTRACT_EXPECTED: dict[tuple[str, str], float] = {
    ("Royalties", "J5"): 0.05,
    ("Royalties", "N5"): 0.025,
    ("FLGT", "W51"): 1099.88947281873,
    ("FLGT", "X51"): 55.0351504205685,
    ("FLGT", "Y51"): 1154.9246232393,
    ("FLGT", "AB51"): 61.3138177169515,
    ("FLGT", "AC51"): 1.37587876051421,
    ("FLGT", "AD51"): 0.0,
    ("FLGT", "AL51"): 62.6896964774657,
    ("FLGT", "AM51"): 0.0542803358903504,
    ("FLGT", "AI51"): 93.5101437605859,
    ("Ec_IO", "G11"): 0.0542803358903504,
    ("Ec_IO", "G15"): 62.6896964774657,
    # optional
    ("FLGT", "AE51"): 0.935147461723997,
    ("FLGT", "AF51"): 10.501599910698099,
    ("FLGT", "AG51"): 16.0950999106981,
    ("FLGT", "AH51"): 1.7009999999999994,
    ("FLGT", "Z51"): 1.5875999999999995,
}


@pytest.fixture(scope="module")
def repo_root() -> Path:
    return ROOT


def test_gm_sha(repo_root: Path) -> None:
    verify_active_gm(repo_root)
    assert_gtc_bound_to_active_sha(repo_root)
    assert ACTIVE_GM_SHA256 == "D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA"


def test_import_for_flgt(repo_root: Path) -> None:
    case = import_case_input_from_active_gm(repo_root)
    assert validate_case_input(case) == []
    assert "Shallow" in (case.terrain or "")
    assert case.gas_utilization and "Dom" in case.gas_utilization
    assert case.oil_block_daily and case.oil_tc_opex


def test_flgt_gtc_mandatory_anchors(repo_root: Path) -> None:
    case = import_case_input_from_active_gm(repo_root)
    prod = ProductionModule().run(case)
    result = FlgtRoyaltiesModule().run(case, upstream={"production": prod})
    pems = result.cell_map()
    keys = [k for k in CONTRACT_EXPECTED if k in pems]
    res = compare_cell_map({k: pems[k] for k in keys}, {k: CONTRACT_EXPECTED[k] for k in keys})
    mismatches = [d for d in res.details if d["status"] == "mismatch"]
    assert res.mismatch == 0, f"mismatches={mismatches}; exact={res.exact} tol={res.tolerance}"
    assert res.exact + res.tolerance >= 13
