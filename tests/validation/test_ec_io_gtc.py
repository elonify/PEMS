"""Ec_IO GTC-001 comparison against approved Golden Master expected values."""

from __future__ import annotations

from pathlib import Path

import pytest
from openpyxl import load_workbook

from pems.calculations.modules.ec_io import EcIoModule
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

LITERAL_CELLS = [
    ("Equity Dash", "C4"),
    ("Equity Dash", "C6"),
    ("Ec_IO", "C5"),
    ("Ec_IO", "C7"),
    ("Ec_IO", "C12"),
    ("Ec_IO", "C14"),
    ("Ec_IO", "C15"),
    ("Ec_IO", "C17"),
    ("Ec_IO", "C18"),
    ("Ec_IO", "C19"),
    ("Ec_IO", "C20"),
    ("Ec_IO", "C21"),
    ("Ec_IO", "C22"),
    ("Ec_IO", "C23"),
    ("Ec_IO", "C24"),
    ("Ec_IO", "C25"),
    ("Ec_IO", "C26"),
    ("Ec_IO", "D28"),
    ("Ec_IO", "D30"),
]

FORMULA_CELLS = [
    ("Equity Dash", "C5"),
    ("Ec_IO", "C13"),
    ("Ec_IO", "C6"),
    ("Ec_IO", "E28"),
    ("Ec_IO", "D29"),
    ("Ec_IO", "E29"),
    ("Ec_IO", "G19"),
    ("Ec_IO", "G23"),
]

TEXT_CELLS = [
    ("Ec_IO", "C4"),
    ("Ec_IO", "G18"),
    ("Ec_IO", "G20"),
    ("Ec_IO", "G21"),
    ("Ec_IO", "G22"),
    ("Ec_IO", "G24"),
    ("Ec_IO", "G25"),
    ("Ec_IO", "G26"),
]


@pytest.fixture(scope="module")
def repo_root() -> Path:
    return ROOT


def _gm_data_only_values(repo_root: Path, cells: list[tuple[str, str]]):
    path = verify_active_gm(repo_root)
    wb = load_workbook(path, data_only=True, read_only=True)
    out = {}
    try:
        for sheet, cell in cells:
            out[(sheet, cell)] = wb[sheet][cell].value
    finally:
        wb.close()
    return out


def test_gm_sha(repo_root: Path) -> None:
    path = verify_active_gm(repo_root)
    assert path.is_file()
    assert_gtc_bound_to_active_sha(repo_root)
    assert ACTIVE_GM_SHA256.startswith("D07560CA")


def test_import_and_validate_from_gm(repo_root: Path, active_gm_case) -> None:
    case = active_gm_case  # session-cached GM import (tests/conftest.py)
    errs = validate_case_input(case, strict=True)
    assert errs == []
    assert case.equity_share_company_1 == 0.49
    assert case.project_start_year == 2027
    assert abs((case.hurdle_rate or 0) - 0.15) < 1e-12
    assert case.source == "excel_import"


def test_ec_io_gtc_literals_and_derived(repo_root: Path, active_gm_case) -> None:
    case = active_gm_case  # session-cached GM import (tests/conftest.py)
    result = EcIoModule().run(case)
    pems = result.cell_map()

    expected_lit = load_literal_expected(repo_root, LITERAL_CELLS)
    expected_f = load_formula_cached_expected(repo_root, FORMULA_CELLS)
    expected_text = _gm_data_only_values(repo_root, TEXT_CELLS)
    expected = {**expected_lit, **expected_f, **expected_text}

    compare_keys = [k for k in pems if k in expected and pems[k] is not None]
    pems_sub = {k: pems[k] for k in compare_keys}
    exp_sub = {k: expected[k] for k in compare_keys}

    res = compare_cell_map(pems_sub, exp_sub)
    mismatches = [d for d in res.details if d["status"] == "mismatch"]
    assert res.mismatch == 0, f"mismatches={mismatches}"
    assert res.exact + res.tolerance + res.expected_error_ok >= 20
