"""GTC comparison utilities.

Tolerance: exact for ints/bools/text; float abs/rel 1e-9.
EXP-001: #NUM! / NO_VALID_IRR equivalence.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from pems.infrastructure.golden_master import ACTIVE_GM_SHA256

FLOAT_ABS = 1e-9
FLOAT_REL = 1e-9


@dataclass
class CompareResult:
    exact: int = 0
    tolerance: int = 0
    mismatch: int = 0
    missing_pems: int = 0
    missing_expected: int = 0
    expected_error_ok: int = 0
    details: list[dict[str, Any]] = field(default_factory=list)

    @property
    def total_compared(self) -> int:
        return self.exact + self.tolerance + self.mismatch + self.expected_error_ok


def values_equal(expected: Any, actual: Any) -> tuple[bool, str]:
    """Return (match, kind) where kind is exact|tolerance|expected_error|mismatch."""
    if expected is None and actual is None:
        return True, "exact"

    # Expected Excel error
    exp_s = str(expected).strip() if expected is not None else ""
    if exp_s.startswith("#"):
        if actual is None:
            return False, "mismatch"
        act_s = str(actual).strip().upper()
        if act_s == exp_s.upper() or (
            exp_s.upper() == "#NUM!"
            and act_s in {"#NUM!", "NO_VALID_IRR", "NO_SIGN_CHANGE"}
        ):
            return True, "expected_error"
        return False, "mismatch"

    if isinstance(expected, bool) or isinstance(actual, bool):
        if expected == actual:
            return True, "exact"
        return False, "mismatch"

    # numeric
    try:
        e = float(expected)
        a = float(actual)
    except (TypeError, ValueError):
        if str(expected).strip() == str(actual).strip():
            return True, "exact"
        return False, "mismatch"

    if math.isnan(e) and math.isnan(a):
        return True, "exact"
    if e == a:
        return True, "exact"
    diff = abs(e - a)
    scale = max(abs(e), abs(a), 1e-15)
    if diff <= FLOAT_ABS or diff / scale <= FLOAT_REL:
        return True, "tolerance"
    return False, "mismatch"


def compare_cell_map(
    pems: dict[tuple[str, str], Any],
    expected: dict[tuple[str, str], Any],
) -> CompareResult:
    res = CompareResult()
    keys = sorted(set(pems) | set(expected), key=lambda x: (x[0], x[1]))
    for k in keys:
        if k not in pems:
            res.missing_pems += 1
            res.details.append(
                {"sheet": k[0], "cell": k[1], "status": "missing_pems", "expected": expected.get(k)}
            )
            continue
        if k not in expected:
            res.missing_expected += 1
            res.details.append(
                {"sheet": k[0], "cell": k[1], "status": "missing_expected", "pems": pems[k]}
            )
            continue
        ok, kind = values_equal(expected[k], pems[k])
        if ok and kind == "exact":
            res.exact += 1
        elif ok and kind == "tolerance":
            res.tolerance += 1
        elif ok and kind == "expected_error":
            res.expected_error_ok += 1
        else:
            res.mismatch += 1
            res.details.append(
                {
                    "sheet": k[0],
                    "cell": k[1],
                    "status": "mismatch",
                    "expected": expected[k],
                    "pems": pems[k],
                }
            )
    return res


def load_literal_expected(
    repo_root: Path,
    cells: Iterable[tuple[str, str]],
) -> dict[tuple[str, str], Any]:
    path = (
        repo_root
        / "docs/workbook/Validation_Datasets/expected_outputs/literal_values_all.csv"
    )
    want = set(cells)
    out: dict[tuple[str, str], Any] = {}
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["worksheet"], row["cell"])
            if key in want:
                out[key] = _parse_csv_value(row.get("expected_value", ""))
    return out


def load_formula_cached_expected(
    repo_root: Path,
    cells: Iterable[tuple[str, str]],
) -> dict[tuple[str, str], Any]:
    path = (
        repo_root
        / "docs/workbook/Validation_Datasets/expected_outputs/formula_cached_results_all.csv"
    )
    want = set(cells)
    out: dict[tuple[str, str], Any] = {}
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["worksheet"], row["cell"])
            if key in want:
                out[key] = _parse_csv_value(row.get("expected_value", ""))
    return out


def _parse_csv_value(s: str) -> Any:
    if s is None:
        return None
    t = s.strip()
    if t == "":
        return ""
    if t.startswith("#"):
        return t
    try:
        if "." not in t and "e" not in t.lower():
            return int(t)
        return float(t)
    except ValueError:
        return t


def gtc_manifest_sha(repo_root: Path) -> str:
    import json

    p = repo_root / "docs/workbook/Validation_Datasets/scenarios/GTC-001_manifest.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    return str(data.get("golden_master_sha256", "")).upper()


def assert_gtc_bound_to_active_sha(repo_root: Path) -> None:
    m = gtc_manifest_sha(repo_root)
    if m != ACTIVE_GM_SHA256:
        raise RuntimeError(f"GTC-001 SHA {m} != active GM {ACTIVE_GM_SHA256}")
