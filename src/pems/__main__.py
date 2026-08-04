"""CLI / UI entry for PEMS."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="pems", description="Elonify PEMS")
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Launch Phase 1H first-slice presentation UI (PySide6)",
    )
    parser.add_argument(
        "--run-gm",
        action="store_true",
        help="Import active Golden Master CaseInput, run chain, print KPI summary (no UI)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root (default: cwd)",
    )
    args = parser.parse_args(argv)

    if args.ui:
        from pems.ui.main_window import run_app

        raise SystemExit(run_app(repo_root=args.root or Path.cwd()))

    if args.run_gm:
        from pems.application.run_service import RunService
        from pems.presentation.view_models import build_presentation

        root = args.root or Path.cwd()
        bundle = RunService().run_from_active_gm(root)
        pres = build_presentation(bundle)
        print("PEMS run-gm summary")
        print(f"validation_errors: {len(bundle.validation_errors)}")
        for row in pres.results_kpi_rows:
            if row.id.startswith("irr") or row.id.startswith("npv") or row.id in (
                "grr_bit",
                "grr_ait",
                "rev_gross",
                "err",
            ):
                print(f"  {row.label}: {row.display} [{row.status}] {row.note[:80] if row.note else ''}")
        return

    from pems import __numerical_validated__, __spec_status__, __version__

    print(f"pems {__version__}")
    print(f"status: {__spec_status__}")
    print(f"numerical_validated: {__numerical_validated__}")
    print("Use: python -m pems --ui   |   python -m pems --run-gm")


if __name__ == "__main__":
    main()
