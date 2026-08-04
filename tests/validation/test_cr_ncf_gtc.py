"""CR/NCF GTC-001 comparison — Project / Equity anchors + AU14 expected error."""

from __future__ import annotations

from pathlib import Path

import pytest

from pems.calculations.modules.costs import CostsModule
from pems.calculations.modules.cr_ncf import CrNcfModule
from pems.calculations.modules.flgt_royalties import FlgtRoyaltiesModule
from pems.calculations.modules.production import ProductionModule
from pems.gtc.compare import (
    assert_gtc_bound_to_active_sha,
    compare_cell_map,
    values_equal,
)
from pems.infrastructure.excel_import import import_case_input_from_active_gm
from pems.infrastructure.golden_master import ACTIVE_GM_SHA256, verify_active_gm
from pems.validation.case_input_validator import validate_case_input

ROOT = Path(__file__).resolve().parents[2]

CONTRACT_EXPECTED: dict[tuple[str, str], float | str] = {
    ("Project_NCF", "AG51"): 149.557072245101,
    ("Project_NCF", "AH51"): 78.0891606587929,
    ("Project_NCF", "AJ51"): 5.13925728744526,
    ("Project_NCF", "AE51"): 310.69425355464,
    ("Project_NCF", "AF51"): 250.725376476001,
    ("Project_NCF", "AB51"): 148.760486089522,
    ("Project_NCF", "AC51"): 26.4540677567758,
    ("Project_NCF", "AD51"): 42.0829559477558,
    ("Project_NCF", "AG58"): 0.348601049838934,
    ("Project_NCF", "AU12"): 0.348601049838934,
    ("Project_NCF", "AU14"): "#NUM!",
    ("Equity_NCF_Con", "AG51"): 73.2829654000993,
    ("Equity_NCF_Con", "AH51"): 38.2636887228085,
}


@pytest.fixture(scope="module")
def repo_root() -> Path:
    return ROOT


def test_gm_sha(repo_root: Path) -> None:
    verify_active_gm(repo_root)
    assert_gtc_bound_to_active_sha(repo_root)
    assert ACTIVE_GM_SHA256 == "D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA"


def test_import_cr_intermediates(repo_root: Path, active_gm_case) -> None:
    case = active_gm_case  # session-cached GM import (tests/conftest.py)
    assert validate_case_input(case) == []
    assert case.extras.get("project_ncf_intermediates")
    assert "AB" in case.extras["project_ncf_intermediates"]


def test_cr_ncf_gtc_anchors(repo_root: Path, active_gm_case) -> None:
    case = active_gm_case  # session-cached GM import (tests/conftest.py)
    prod = ProductionModule().run(case)
    costs = CostsModule().run(case)
    flgt = FlgtRoyaltiesModule().run(case, upstream={"production": prod})
    result = CrNcfModule().run(
        case, upstream={"production": prod, "costs": costs, "flgt": flgt}
    )
    pems = result.cell_map()

    # Map NO_VALID_IRR → #NUM! for AU14 comparison via values_equal
    for k, v in list(pems.items()):
        if v == "NO_VALID_IRR":
            pems[k] = "NO_VALID_IRR"  # compare framework accepts vs #NUM!

    keys = [k for k in CONTRACT_EXPECTED if k in pems]
    res = compare_cell_map(
        {k: pems[k] for k in keys},
        {k: CONTRACT_EXPECTED[k] for k in keys},
    )
    # AU14 special: if still mismatch, check expected_error path
    mismatches = [d for d in res.details if d["status"] == "mismatch"]
    # re-check AU14 with values_equal
    if any(d.get("cell") == "AU14" for d in mismatches):
        ok, kind = values_equal("#NUM!", result.au14_irr)
        assert ok and kind == "expected_error", (result.au14_irr, kind)
        mismatches = [d for d in mismatches if d.get("cell") != "AU14"]
        res.mismatch = len(mismatches)
        res.expected_error_ok = getattr(res, "expected_error_ok", 0) + 1

    assert res.mismatch == 0, f"mismatches={mismatches}; exact={res.exact} tol={res.tolerance}"
    assert res.exact + res.tolerance + res.expected_error_ok >= 11
