"""Costs GTC-001 comparison — COSTS_PARAMETER_CONTRACT §10 anchors."""

from __future__ import annotations

from pathlib import Path

import pytest

from pems.calculations.modules.costs import CostsModule
from pems.gtc.compare import (
    assert_gtc_bound_to_active_sha,
    compare_cell_map,
    load_formula_cached_expected,
    load_literal_expected,
)
from pems.infrastructure.excel_import import import_case_input_from_active_gm
from pems.infrastructure.golden_master import ACTIVE_GM_SHA256, verify_active_gm
from pems.validation.case_input_validator import validate_case_input

ROOT = Path(__file__).resolve().parents[2]

# Contract §10.1–10.3 mandatory anchors
COMPARE_CELLS = [
    ("Cap_Allow", "FI48"),
    ("Cap_Allow", "FL48"),
    ("Cap_Allow", "FK48"),
    ("Cap_Allow", "FP48"),
    ("Cap_Allow", "FQ48"),
    ("Cap_Allow", "FR5"),
    ("Cap_Allow", "FR6"),
    ("Cap_Allow", "FR7"),
    ("Cap_Allow", "FR8"),
    ("Cap_Allow", "FR9"),
    ("Cap_Allow Gas", "FI48"),
    ("Cap_Allow Gas", "FL48"),
    ("Cap_Allow Gas", "FK48"),
    ("Ec_IO", "N16"),
    ("Ec_IO", "S16"),
    ("Ec_IO", "N17"),
    ("Ec_IO", "S17"),
    ("Ec_IO", "N18"),
    ("Ec_IO", "S18"),
]

# Contract expected values (authoritative)
CONTRACT_EXPECTED: dict[tuple[str, str], float] = {
    ("Cap_Allow", "FI48"): 361.503330356603,
    ("Cap_Allow", "FL48"): 185.584322008296,
    ("Cap_Allow", "FK48"): 142.902934166187,
    ("Cap_Allow", "FP48"): 35.0,
    ("Cap_Allow", "FQ48"): 140.0,
    ("Cap_Allow", "FR5"): 0.2,
    ("Cap_Allow", "FR6"): 0.2,
    ("Cap_Allow", "FR7"): 0.2,
    ("Cap_Allow", "FR8"): 0.2,
    ("Cap_Allow", "FR9"): 0.19,
    ("Cap_Allow Gas", "FI48"): 56.7,
    ("Cap_Allow Gas", "FL48"): 25.4185178187494,
    ("Cap_Allow Gas", "FK48"): 0.0,
    ("Ec_IO", "N16"): 211.002839827046,
    ("Ec_IO", "S16"): 418.203330356603,
    ("Ec_IO", "N17"): 142.902934166187,
    ("Ec_IO", "S17"): 175.0,
    ("Ec_IO", "N18"): 353.905773993233,
    ("Ec_IO", "S18"): 593.203330356603,
}


@pytest.fixture(scope="module")
def repo_root() -> Path:
    return ROOT


def test_gm_sha_intact(repo_root: Path) -> None:
    verify_active_gm(repo_root)
    assert_gtc_bound_to_active_sha(repo_root)
    assert ACTIVE_GM_SHA256 == "D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA"


def test_import_cost_schedules(repo_root: Path, active_gm_case) -> None:
    case = active_gm_case  # session-cached GM import (tests/conftest.py)
    assert validate_case_input(case) == []
    assert case.hurdle_rate == 0.15
    assert abs((case.duties_rate or 0) - 0.0) < 1e-15
    assert case.oil_tc_opex and len(case.oil_tc_opex) >= 10
    assert case.gas_tc_opex and len(case.gas_tc_opex) >= 1
    assert case.ca_rates == [0.2, 0.2, 0.2, 0.2, 0.19]
    assert case.cost_mode_field == "Ebiya Field" or case.block_field_oil == "Ebiya Field"


def test_costs_gtc_mandatory_anchors(repo_root: Path, active_gm_case) -> None:
    case = active_gm_case  # session-cached GM import (tests/conftest.py)
    result = CostsModule().run(case)
    pems = {k: result.cell_map()[k] for k in COMPARE_CELLS if k in result.cell_map()}

    # Prefer catalogue formula cache / literals; fall back to contract expected
    expected_f = load_formula_cached_expected(repo_root, COMPARE_CELLS)
    expected_l = load_literal_expected(repo_root, COMPARE_CELLS)
    expected = {**CONTRACT_EXPECTED, **expected_l, **expected_f}
    # Contract overrides only when catalogue missing
    for k, v in CONTRACT_EXPECTED.items():
        if k not in expected or expected[k] is None:
            expected[k] = v

    compare_keys = [k for k in pems if k in expected and expected[k] is not None]
    res = compare_cell_map(
        {k: pems[k] for k in compare_keys},
        {k: expected[k] for k in compare_keys},
    )
    mismatches = [d for d in res.details if d["status"] == "mismatch"]
    assert res.mismatch == 0, f"mismatches={mismatches}; exact={res.exact} tol={res.tolerance}"
    assert res.exact + res.tolerance >= 15


def test_costs_contract_expected_direct(repo_root: Path, active_gm_case) -> None:
    """Hard contract anchors (no catalogue rewrite)."""
    case = active_gm_case  # session-cached GM import (tests/conftest.py)
    pems = CostsModule().run(case).cell_map()
    res = compare_cell_map(
        {k: pems[k] for k in CONTRACT_EXPECTED if k in pems},
        CONTRACT_EXPECTED,
    )
    assert res.mismatch == 0, res.details
    assert res.exact + res.tolerance == len(CONTRACT_EXPECTED)
