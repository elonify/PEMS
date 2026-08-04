"""Golden Master path and SHA verification (read-only).

ADR-0010: openpyxl for import/compare only — never write the approved GM.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from pems.core.exceptions import GoldenMasterError

# Authoritative approved identity
ACTIVE_GM_SHA256 = (
    "D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA"
)
ACTIVE_GM_RELATIVE = (
    "docs/workbook/Workbook_History/Econ_Model_PEMS_confirmed_2026-08-03.xlsx"
)


def resolve_gm_path(repo_root: Path | None = None) -> Path:
    root = repo_root or Path.cwd()
    path = root / ACTIVE_GM_RELATIVE
    if not path.is_file():
        raise GoldenMasterError(f"Golden Master not found: {path}")
    return path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def verify_active_gm(repo_root: Path | None = None) -> Path:
    """Return path if SHA matches approved identity; raise otherwise."""
    path = resolve_gm_path(repo_root)
    digest = sha256_file(path)
    if digest != ACTIVE_GM_SHA256:
        raise GoldenMasterError(
            f"GM SHA mismatch: got {digest}, expected {ACTIVE_GM_SHA256}"
        )
    return path
