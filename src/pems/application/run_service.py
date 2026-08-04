"""Application run service — orchestrates calculation modules for presentation.

UI and presentation packages call this layer only; they must not re-host
economic formulas or open Excel as a live calc engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pems.calculations.modules.costs import CostsModule, CostsResult
from pems.calculations.modules.cr_ncf import CrNcfModule, CrNcfResult
from pems.calculations.modules.ec_io import EcIoModule, EcIoResult
from pems.calculations.modules.flgt_royalties import FlgtRoyaltiesModule, FlgtResult
from pems.calculations.modules.production import ProductionModule, ProductionResult
from pems.calculations.modules.results import ResultsModule, ResultsResult
from pems.domain.case_input import CaseInput
from pems.infrastructure.excel_import import import_case_input_from_active_gm
from pems.validation.case_input_validator import validate_case_input


@dataclass
class RunBundle:
    """Authoritative calculation outputs for presentation projection."""

    case: CaseInput
    ec_io: EcIoResult
    production: ProductionResult
    costs: CostsResult
    flgt: FlgtResult
    cr_ncf: CrNcfResult
    results: ResultsResult
    validation_errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


class RunService:
    """Run existing calc chain; no presentation formatting here."""

    def run(self, case: CaseInput) -> RunBundle:
        errors = validate_case_input(case)
        # Soft-fail: still attempt run if non-empty case; UI surfaces errors
        notes: list[str] = []
        if errors:
            notes.append(f"validation: {len(errors)} issue(s)")

        ec = EcIoModule().run(case)
        prod = ProductionModule().run(case)
        if case.project_life_years is None and prod.project_life_years is not None:
            # display life for GRR path already used by ResultsModule
            case.project_life_years = float(prod.project_life_years)
        costs = CostsModule().run(case)
        flgt = FlgtRoyaltiesModule().run(case, upstream={"production": prod})
        cr = CrNcfModule().run(
            case, upstream={"production": prod, "costs": costs, "flgt": flgt}
        )
        results = ResultsModule().run(
            case,
            upstream={
                "production": prod,
                "costs": costs,
                "flgt": flgt,
                "cr_ncf": cr,
                "ec_io": ec,
            },
        )
        return RunBundle(
            case=case,
            ec_io=ec,
            production=prod,
            costs=costs,
            flgt=flgt,
            cr_ncf=cr,
            results=results,
            validation_errors=list(errors),
            notes=notes + list(results.notes or []),
        )

    def run_from_active_gm(self, repo_root: Path | None = None) -> RunBundle:
        case = import_case_input_from_active_gm(repo_root)
        return self.run(case)
