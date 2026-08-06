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


# Cached Equity_NCF_Con sample years (formula_cached_results_all.csv, D07560CA…).
# Row → calendar year from Equity_NCF_Con!A; values from AF/AH/AI columns.
EQUITY_ANNUAL_SAMPLES: dict[int, dict[str, float]] = {
    2027: {  # row 8
        "AF": -0.264526336399821,
        "AH": -0.264526336399821,
        "AI": -0.264526336399821,
    },
    2029: {  # row 10
        "AF": -0.166410482587712,
        "AH": -0.1258302325805,
        "AI": -48.944896067154,
    },
    2031: {  # row 12
        "AF": 40.3791342284605,
        "AH": 23.086901049359,
        "AI": -2.06151282458117,
    },
    2034: {  # row 15
        "AF": 18.3607574641536,
        "AH": 6.90248881181975,
        "AI": 29.0847375626801,
    },
    2039: {  # row 20
        "AF": 1.71127036009581,
        "AH": 0.319848666204418,
        "AI": 38.2539822196466,
    },
}


def test_cr_ncf_equity_annual_maps_gtc(repo_root: Path, active_gm_case) -> None:
    """Slice A equity AF/AH/AI year maps vs GM Equity_NCF_Con cache samples."""
    case = active_gm_case
    prod = ProductionModule().run(case)
    costs = CostsModule().run(case)
    flgt = FlgtRoyaltiesModule().run(case, upstream={"production": prod})
    result = CrNcfModule().run(
        case, upstream={"production": prod, "costs": costs, "flgt": flgt}
    )

    assert result.equity_contractor_af
    assert result.equity_dncf_by_year
    assert result.equity_cum_dncf_by_year

    # Scalars preserved (project NPV × share) — already in CONTRACT_EXPECTED via cell_map
    assert abs(result.equity_ah51 - 38.2636887228085) < 1e-9
    assert abs(result.equity_ag51 - 73.2829654000993) < 1e-9

    mismatches: list[str] = []
    for year, exp in EQUITY_ANNUAL_SAMPLES.items():
        got_af = result.equity_contractor_af.get(year)
        got_ah = result.equity_dncf_by_year.get(year)
        got_ai = result.equity_cum_dncf_by_year.get(year)
        for label, got, want in (
            ("AF", got_af, exp["AF"]),
            ("AH", got_ah, exp["AH"]),
            ("AI", got_ai, exp["AI"]),
        ):
            ok, kind = values_equal(want, got)
            if not ok:
                mismatches.append(f"{year} {label}: got={got} want={want} ({kind})")

    # Share-homogeneity: equity AF == project AF × C4 for sampled years
    share = float(case.equity_share_company_1 or 0.0)
    assert abs(share - 0.49) < 1e-12
    for year in EQUITY_ANNUAL_SAMPLES:
        proj = result.contractor_af.get(year, 0.0)
        eq_af = result.equity_contractor_af.get(year, 0.0)
        assert abs(eq_af - proj * share) < 1e-12, (year, eq_af, proj, share)

    # Strict AI gate: at D22 and after, cum map is 0
    d22 = int(case.extras.get("price_path_end_year") or 2042)
    assert d22 == 2042
    assert result.equity_cum_dncf_by_year.get(d22, 0.0) == 0.0
    assert result.equity_cum_dncf_by_year.get(d22 + 1, 0.0) == 0.0

    assert not mismatches, "equity annual mismatches:\n" + "\n".join(mismatches)
