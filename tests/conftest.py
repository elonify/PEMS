"""Shared pytest fixtures — performance only; no calculation semantics changes.

Phase 1G: session-scoped Golden Master CaseInput import cache.

Why: each validation test previously called import_case_input_from_active_gm(),
re-opening the ~4.8 MB GM via openpyxl (~90–100 s per load). Session cache loads
once per pytest process and returns deep copies so tests cannot mutate shared state.

Does not:
- change expected GTC values
- open GM in write mode
- alter calculation modules
"""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from pems.domain.case_input import CaseInput
from pems.infrastructure.excel_import import import_case_input_from_active_gm
from pems.infrastructure.golden_master import verify_active_gm

ROOT = Path(__file__).resolve().parents[1]

# Process-level cache (also usable outside fixtures if needed carefully)
_GM_CASE_CACHE: CaseInput | None = None


def get_active_gm_case(repo_root: Path | None = None) -> CaseInput:
    """Return a deep copy of the session-cached GM CaseInput (read-only GM import)."""
    global _GM_CASE_CACHE
    root = repo_root or ROOT
    if _GM_CASE_CACHE is None:
        verify_active_gm(root)
        _GM_CASE_CACHE = import_case_input_from_active_gm(root)
    return copy.deepcopy(_GM_CASE_CACHE)


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def _session_gm_case() -> CaseInput:
    """Session master instance — tests must use active_gm_case (deep copy).

    Uses package ROOT constant (not a fixture) so module-scoped repo_root
    overrides in individual test modules cannot cause ScopeMismatch.
    """
    verify_active_gm(ROOT)
    return import_case_input_from_active_gm(ROOT)


@pytest.fixture
def active_gm_case(_session_gm_case: CaseInput) -> CaseInput:
    """Per-test deep copy of GM CaseInput (safe mutation isolation)."""
    return copy.deepcopy(_session_gm_case)
