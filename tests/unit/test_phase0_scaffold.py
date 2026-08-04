"""Phase 0 scaffold smoke tests — no economic assertions."""

from __future__ import annotations

import pytest

from pems import __numerical_validated__, __spec_status__, __version__
from pems.calculations import run_pipeline
from pems.calculations.dependency_order import MODULE_DEPENDENCY_ORDER
from pems.core.exceptions import NotImplementedCalculationError
from pems.domain.case_input import CaseInput
from pems.infrastructure.golden_master import ACTIVE_GM_SHA256, verify_active_gm
from pems.validation.case_input_validator import validate_case_input


def test_version_and_status() -> None:
    assert __version__ == "0.0.0"
    assert __spec_status__ == "PHASE_0_SCAFFOLD"
    assert __numerical_validated__ is False


def test_case_input_empty_not_gtc_complete() -> None:
    case = CaseInput()
    assert case.is_complete_for_gtc001() is False
    assert validate_case_input(case) == []


def test_pipeline_not_implemented() -> None:
    with pytest.raises(NotImplementedCalculationError):
        run_pipeline(CaseInput())


def test_dependency_order_includes_results() -> None:
    assert MODULE_DEPENDENCY_ORDER[0] == "case_input"
    assert MODULE_DEPENDENCY_ORDER[-1] == "results"
    assert "cr_ncf" in MODULE_DEPENDENCY_ORDER


def test_active_gm_sha_constant() -> None:
    assert ACTIVE_GM_SHA256.startswith("D07560CA")
    assert len(ACTIVE_GM_SHA256) == 64


def test_verify_active_gm_if_present() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    gm = root / "docs/workbook/Workbook_History/Econ_Model_PEMS_confirmed_2026-08-03.xlsx"
    if not gm.is_file():
        pytest.skip("GM file not present in workspace")
    path = verify_active_gm(root)
    assert path == gm
