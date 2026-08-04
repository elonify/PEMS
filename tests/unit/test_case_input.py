"""CaseInput validation and manual pathway tests."""

from __future__ import annotations

import pytest

from pems.domain.case_input import CaseInput
from pems.domain.manual_input import case_input_from_mapping
from pems.domain.provenance import CASE_INPUT_PROVENANCE
from pems.validation.case_input_validator import validate_case_input


def test_manual_mapping_and_serialize() -> None:
    case = case_input_from_mapping(
        {
            "equity_share_company_1": 0.49,
            "project_start_year": 2027,
            "hurdle_rate": 0.15,
            "oil_price_usd_bbl": 50,
            "gas_price_usd_mscf": 2.18,
            "price_escalator": 0,
            "production_days_per_year": 365,
            "asset_analysis_type": "Forecast",
            "terrain": "Shallow Water (<200m water depth)",
            "gas_utilization": "In-Country (Dom Gas)",
            "licence_lease_status": "New Acreage",
            "pfs_contract_type": "PSC/SC",
        }
    )
    assert case.source == "manual"
    assert case.is_complete_for_gtc001()
    ser = case.to_serializable()
    assert ser["equity_share_company_1"] == 0.49
    assert "hurdle_rate" in ser


def test_enum_validation() -> None:
    case = CaseInput(asset_analysis_type="Bad")
    errs = validate_case_input(case)
    assert any("asset_analysis_type" in e for e in errs)


def test_pfs_enum() -> None:
    case = CaseInput(pfs_contract_type="PSC/SC")
    assert validate_case_input(case) == []


def test_provenance_map() -> None:
    p = CASE_INPUT_PROVENANCE["equity_share_company_1"]
    assert p.sheet == "Equity Dash" and p.cell == "C4"
    assert p.classification == "CONFIRMED_INPUT"
