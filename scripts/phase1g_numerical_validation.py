"""Phase 1G — controlled numerical validation (single GM load).

Loads the approved Golden Master once, runs the implemented chain once,
compares documented GTC anchors, and classifies independent vs intermediate-
dependent outputs.

Read-only GM. Does not rewrite expected values.
"""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pems.calculations.modules.costs import CostsModule
from pems.calculations.modules.cr_ncf import CrNcfModule
from pems.calculations.modules.ec_io import EcIoModule
from pems.calculations.modules.flgt_royalties import FlgtRoyaltiesModule
from pems.calculations.modules.production import ProductionModule
from pems.calculations.modules.results import ResultsModule
from pems.gtc.compare import (
    CompareResult,
    assert_gtc_bound_to_active_sha,
    compare_cell_map,
    values_equal,
)
from pems.infrastructure.excel_import import import_case_input_from_active_gm
from pems.infrastructure.golden_master import ACTIVE_GM_SHA256, sha256_file, verify_active_gm
from pems.validation.case_input_validator import validate_case_input

# --- Documented module GTC anchors (do not rewrite) ---

EC_IO_EXPECTED: dict[tuple[str, str], Any] = {
    ("Equity Dash", "C4"): 0.49,
    ("Equity Dash", "C6"): 1.0,
    ("Equity Dash", "C5"): 0.51,
    ("Ec_IO", "C5"): 2027,
    ("Ec_IO", "C7"): 365,  # EC_IO_PARAMETER_CONTRACT GTC 365 (not 365.25)
    ("Ec_IO", "C12"): 50.0,
    ("Ec_IO", "C13"): "Real",
    ("Ec_IO", "C14"): 0.0,
    ("Ec_IO", "C15"): 0.15,
    ("Ec_IO", "C17"): 2.18,
    ("Ec_IO", "G18"): "Ebiya Field",
    ("Ec_IO", "G19"): "Ebiya Field",
    ("Ec_IO", "G20"): "Shallow Water (<200m water depth)",
    ("Ec_IO", "G22"): "New Acreage",
    ("Ec_IO", "G24"): "PSC/SC",
    ("Ec_IO", "G25"): "Nigeria",
    ("Ec_IO", "G26"): "PIA 2021",
    ("Ec_IO", "E28"): 2026,
    ("Ec_IO", "D29"): 2027,
}

PROD_EXPECTED: dict[tuple[str, str], Any] = {
    ("Production Profile", "B2"): "STOIIP",
    ("Prod_Summary", "V47"): 21.9977894563747,
    ("Prod_Summary", "Y47"): 25.2454818442975,
    ("Prod_Summary", "Y49"): 4.34966951142272,
    ("Prod_Summary", "Y50"): 26.3474589677974,
    ("Prod_Summary", "AF26"): 15.0,
    ("Ec_IO", "C6"): 15.0,
}

COSTS_EXPECTED: dict[tuple[str, str], float] = {
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

FLGT_EXPECTED: dict[tuple[str, str], float] = {
    ("Royalties", "J5"): 0.05,
    ("Royalties", "N5"): 0.025,
    ("FLGT", "W51"): 1099.88947281873,
    ("FLGT", "X51"): 55.0351504205685,
    ("FLGT", "Y51"): 1154.9246232393,
    ("FLGT", "AB51"): 61.3138177169515,
    ("FLGT", "AC51"): 1.37587876051421,
    ("FLGT", "AD51"): 0.0,
    ("FLGT", "AL51"): 62.6896964774657,
    ("FLGT", "AM51"): 0.0542803358903504,
    ("FLGT", "AI51"): 93.5101437605859,
    ("Ec_IO", "G11"): 0.0542803358903504,
    ("Ec_IO", "G15"): 62.6896964774657,
}

CR_EXPECTED: dict[tuple[str, str], float | str] = {
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

# RESULTS cells that depend on HT/CIT selected intermediate import (not full engines)
RESULTS_INTERMEDIATE_DEPENDENT = {
    "J7",
    "K7",
    "K8",
    "J12",
    "K12",
    "K14",
    "J22",
    "J23",
    "J24",
    "J25",  # sum includes intermediate tax
    # PVR/PI/GRR BIT use K7 intermediate NPV
    "K9",
    "K10",
    "K11",
    "J13",
    "K13",  # disc take BIT from intermediate NPVs
}

# CR uses project_ncf_intermediates for tax/allowable columns
CR_INTERMEDIATE_DEPENDENT = {
    ("Project_NCF", "AG51"),
    ("Project_NCF", "AH51"),
    ("Project_NCF", "AJ51"),
    ("Project_NCF", "AE51"),
    ("Project_NCF", "AF51"),
    ("Project_NCF", "AB51"),
    ("Project_NCF", "AC51"),
    ("Project_NCF", "AD51"),
    ("Project_NCF", "AG58"),
    ("Project_NCF", "AU12"),
    ("Project_NCF", "AU14"),
    ("Equity_NCF_Con", "AG51"),
    ("Equity_NCF_Con", "AH51"),
}


def load_results_expected() -> dict[tuple[str, str], Any]:
    path = (
        ROOT
        / "docs/workbook/Validation_Datasets/expected_outputs/GTC-001_kpi_and_intermediates.csv"
    )
    expected: dict[tuple[str, str], Any] = {}
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("worksheet") != "RESULTS Equity":
                continue
            cell = row["cell"]
            raw = row["expected_value"]
            vtype = (row.get("value_type") or "").lower()
            key = ("RESULTS Equity", cell)
            if key in expected:
                continue  # first row wins for duplicates
            expected[key] = float(raw) if vtype == "float" else raw
    return expected


def summarize(res: CompareResult) -> dict[str, Any]:
    mismatches = [d for d in res.details if d.get("status") == "mismatch"]
    return {
        "exact": res.exact,
        "tolerance": res.tolerance,
        "expected_error_ok": res.expected_error_ok,
        "mismatch": res.mismatch,
        "missing_pems": res.missing_pems,
        "compared": res.total_compared,
        "mismatches": mismatches,
    }


def compare_module(
    name: str,
    pems: dict[tuple[str, str], Any],
    expected: dict[tuple[str, str], Any],
    *,
    au14_special: bool = False,
) -> dict[str, Any]:
    keys = [k for k in expected if k in pems]
    missing = [k for k in expected if k not in pems]
    pems_f = {k: pems[k] for k in keys}
    exp_f = {k: expected[k] for k in keys}
    res = compare_cell_map(pems_f, exp_f)
    if au14_special:
        mismatches = [d for d in res.details if d["status"] == "mismatch"]
        au = [d for d in mismatches if d.get("cell") == "AU14"]
        if au:
            ok, kind = values_equal("#NUM!", pems.get(("Project_NCF", "AU14")))
            if ok and kind == "expected_error":
                mismatches = [d for d in mismatches if d.get("cell") != "AU14"]
                res.mismatch = len(mismatches)
                res.expected_error_ok += 1
                res.details = [d for d in res.details if d.get("cell") != "AU14"]
    out = summarize(res)
    out["module"] = name
    out["missing_pems_keys"] = [f"{s}!{c}" for s, c in missing]
    out["anchor_count"] = len(expected)
    out["pass"] = out["mismatch"] == 0 and len(missing) == 0
    return out


def classify_results(pems: dict[tuple[str, str], Any], expected: dict[tuple[str, str], Any]) -> dict:
    independent: list[str] = []
    intermediate: list[str] = []
    for (_s, cell), exp in expected.items():
        if cell in RESULTS_INTERMEDIATE_DEPENDENT:
            intermediate.append(cell)
        else:
            independent.append(cell)
    ind_keys = {("RESULTS Equity", c) for c in independent if ("RESULTS Equity", c) in pems}
    int_keys = {("RESULTS Equity", c) for c in intermediate if ("RESULTS Equity", c) in pems}
    ind_res = compare_cell_map(
        {k: pems[k] for k in ind_keys},
        {k: expected[k] for k in ind_keys},
    )
    int_res = compare_cell_map(
        {k: pems[k] for k in int_keys},
        {k: expected[k] for k in int_keys},
    )
    return {
        "independent_cells": sorted(independent),
        "intermediate_dependent_cells": sorted(intermediate),
        "independent_compare": summarize(ind_res),
        "intermediate_compare": summarize(int_res),
    }


def main() -> int:
    t0 = time.perf_counter()
    report: dict[str, Any] = {
        "phase": "1G",
        "expected_gm_sha": ACTIVE_GM_SHA256,
    }

    gm_path = verify_active_gm(ROOT)
    actual = sha256_file(gm_path)
    report["actual_gm_sha"] = actual
    report["gm_match"] = actual == ACTIVE_GM_SHA256
    report["gm_modified"] = False
    assert_gtc_bound_to_active_sha(ROOT)

    t_import = time.perf_counter()
    case = import_case_input_from_active_gm(ROOT)  # SINGLE GM load
    report["import_seconds"] = round(time.perf_counter() - t_import, 2)
    report["case_validation_errors"] = validate_case_input(case)
    report["intermediates_present"] = {
        "project_ncf_intermediates": bool(case.extras.get("project_ncf_intermediates")),
        "ht_ncf_oil_equity_intermediates": bool(case.extras.get("ht_ncf_oil_equity_intermediates")),
        "cit_ncf_equity_totals": bool(case.extras.get("cit_ncf_equity_totals")),
        "flgt_loan_an_ao_ap": bool(case.extras.get("flgt_an")),
    }

    # Single chain run
    t_run = time.perf_counter()
    ec = EcIoModule().run(case)
    prod = ProductionModule().run(case)
    if case.project_life_years is None and prod.project_life_years is not None:
        case.project_life_years = float(prod.project_life_years)
    costs = CostsModule().run(case)
    flgt = FlgtRoyaltiesModule().run(case, upstream={"production": prod})
    cr = CrNcfModule().run(case, upstream={"production": prod, "costs": costs, "flgt": flgt})
    results = ResultsModule().run(
        case,
        upstream={"production": prod, "costs": costs, "flgt": flgt, "cr_ncf": cr, "ec_io": ec},
    )
    report["chain_run_seconds"] = round(time.perf_counter() - t_run, 2)

    # Module compares
    modules: list[dict[str, Any]] = []

    # A. Ec_IO
    ec_map = ec.cell_map()
    # C6 life may come from production path after life fill
    if ("Ec_IO", "C6") not in ec_map and case.project_life_years is not None:
        ec_map[("Ec_IO", "C6")] = case.project_life_years
    modules.append(compare_module("A_CaseInput_Ec_IO", ec_map, EC_IO_EXPECTED))

    # B. Production
    prod_map = prod.cell_map()
    if case.project_life_years is not None:
        prod_map[("Ec_IO", "C6")] = case.project_life_years
    modules.append(compare_module("B_Production", prod_map, PROD_EXPECTED))

    # C. Costs
    modules.append(compare_module("C_Costs", costs.cell_map(), COSTS_EXPECTED))

    # D. FLGT
    modules.append(compare_module("D_FLGT", flgt.cell_map(), FLGT_EXPECTED))

    # E. CR/NCF
    cr_map = cr.cell_map()
    modules.append(compare_module("E_CR_NCF", cr_map, CR_EXPECTED, au14_special=True))

    # F. RESULTS
    res_expected = load_results_expected()
    res_map = results.cell_map()
    modules.append(compare_module("F_RESULTS", res_map, res_expected))

    report["modules"] = modules

    # G. Integrated classification
    report["results_classification"] = classify_results(res_map, res_expected)
    report["cr_intermediate_note"] = (
        "CR/NCF Project AE/AF construction uses selected Project_NCF intermediate "
        "columns (AB/AC/AD/tax/allowable) imported from GM; IRR/discount/equity scale "
        "are computed in PEMS over those series."
    )
    report["results_intermediate_note"] = (
        "RESULTS BIT KPIs (HT equity AS/AT/AR/AQ/AV/AO) and CIT equity tax totals "
        "use selected intermediate import; pure aggregation (C4 scale, unit costs, "
        "ERR, AIT ratios, identity) is computed in PEMS."
    )

    # Independence rollup
    independent_modules = ["A_CaseInput_Ec_IO", "B_Production", "C_Costs", "D_FLGT"]
    report["independent_engine_modules_pass"] = all(
        m["pass"] for m in modules if m["module"] in independent_modules
    )
    report["intermediate_path_modules"] = {
        "E_CR_NCF": next(m for m in modules if m["module"] == "E_CR_NCF"),
        "F_RESULTS": next(m for m in modules if m["module"] == "F_RESULTS"),
        "F_RESULTS_independent_subset": report["results_classification"]["independent_compare"],
        "F_RESULTS_intermediate_subset": report["results_classification"]["intermediate_compare"],
    }

    all_pass = all(m["pass"] for m in modules)
    report["all_documented_anchors_pass"] = all_pass
    report["unexplained_mismatches_total"] = sum(m["mismatch"] for m in modules)
    report["totals"] = {
        "exact": sum(m["exact"] for m in modules),
        "tolerance": sum(m["tolerance"] for m in modules),
        "expected_error_ok": sum(m["expected_error_ok"] for m in modules),
        "mismatch": sum(m["mismatch"] for m in modules),
    }

    # Claim discipline (script recommendation — formal report decides)
    report["claims"] = {
        "RESULTS_SPECIFICATION_READY": "YES",
        "RESULTS_IMPLEMENTED": "YES",
        "GTC_ANCHOR_COMPARISON_PASS": "YES" if all_pass else "NO",
        "INDEPENDENT_ENGINE_MODULES_A_D": (
            "COMPARISON_PASS" if report["independent_engine_modules_pass"] else "FAIL"
        ),
        "CR_NCF_INDEPENDENT_ENGINE": "NOT CLAIMED — selected Project_NCF intermediates",
        "RESULTS_INDEPENDENT_ENGINE_FULL": "NOT CLAIMED — HT/CIT equity intermediates for BIT/tax",
        "RESULTS_NUMERICALLY_VALIDATED_FULL": "NOT CLAIMED",
        "PEMS_vs_GM_FULL_SYSTEM_VALIDATION": "NOT CLAIMED",
        "PRESENTATION": "DEFERRED",
        "SENSITIVITY_MONTE_CARLO": "DEFERRED",
        "GOLDEN_MASTER": "UNCHANGED",
    }

    report["elapsed_seconds"] = round(time.perf_counter() - t0, 2)

    out_path = ROOT / "docs/03_IMPLEMENTATION/PHASE1G_NUMERICAL_VALIDATION_EVIDENCE.json"
    out_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps({k: report[k] for k in (
        "gm_match", "import_seconds", "chain_run_seconds", "elapsed_seconds",
        "all_documented_anchors_pass", "unexplained_mismatches_total", "totals", "claims",
    )}, indent=2))
    print("--- modules ---")
    for m in modules:
        print(
            f"{m['module']}: pass={m['pass']} exact={m['exact']} tol={m['tolerance']} "
            f"err={m['expected_error_ok']} mismatch={m['mismatch']} missing={m['missing_pems_keys']}"
        )
    print(f"Evidence written: {out_path}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
