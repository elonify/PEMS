"""Read-only Ec_IO contract evidence extract. Does not modify GM."""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\Emmanuel Onwuka\Desktop\PEMS")
OUT = ROOT / "docs/workbook/semantic_mapping/EC_IO_EVIDENCE_EXTRACT.json"
CAT = ROOT / "docs/workbook/catalogue"
VAL = ROOT / "docs/workbook/Validation_Datasets"
SEM = ROOT / "docs/workbook/semantic_mapping"
NEW = "D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA"


def main() -> None:
    cells = []
    with (CAT / "cell_catalogue_all_nonempty.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] == "Ec_IO":
                cells.append(r)

    formulas = []
    with (CAT / "formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] == "Ec_IO":
                formulas.append(
                    {
                        "cell": r["cell"],
                        "formula": r["formula"],
                        "cached_value": r["cached_value"],
                        "number_format": r.get("number_format", ""),
                    }
                )

    literals = []
    labels = []
    for r in cells:
        if r["cell_class"] == "formula":
            continue
        item = {
            "cell": r["cell"],
            "row": int(r["row"]),
            "col": int(r["col"]),
            "cell_class": r["cell_class"],
            "value": r["cached_value"],
            "number_format": r.get("number_format", ""),
        }
        if r["cell_class"] == "label_or_text":
            labels.append(item)
        else:
            literals.append(item)

    cp = {}
    with (SEM / "CRITICAL_PATH_LITERAL_CLASSIFICATION.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] == "Ec_IO":
                cp[r["cell"]] = {
                    "value": r["value"],
                    "classification": r["classification"],
                    "understanding": r["understanding"],
                    "nearby_labels": r.get("nearby_labels", ""),
                    "evidence": r.get("evidence", ""),
                }

    gtc_inputs = []
    with (VAL / "scenarios/GTC-001_input_and_parameter_cells.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] == "Ec_IO":
                gtc_inputs.append(
                    {
                        "cell": r["cell"],
                        "cell_class": r["cell_class"],
                        "formula": r.get("formula", ""),
                        "value": r.get("value", ""),
                        "role": r.get("role", ""),
                    }
                )

    kpis = []
    with (VAL / "expected_outputs/GTC-001_kpi_and_intermediates.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("worksheet") == "Ec_IO":
                kpis.append(
                    {
                        "cell": r.get("cell"),
                        "formula": r.get("formula", ""),
                        "expected_value": r.get("expected_value", ""),
                        "metric_label_source": r.get("metric_label_source", ""),
                    }
                )

    # who consumes Ec_IO refs (sample from CROSS_SHEET if exists)
    consumers = defaultdict(set)
    edges = SEM / "CROSS_SHEET_DEPENDENCY_EDGES.csv"
    if edges.exists():
        with edges.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                # flexible column names
                src = r.get("source_sheet") or r.get("from_sheet") or r.get("precedent_sheet")
                dst = r.get("target_sheet") or r.get("to_sheet") or r.get("dependent_sheet")
                if src == "Ec_IO" and dst and dst != "Ec_IO":
                    consumers[dst].add(r.get("count") or r.get("edge_count") or 1)

    # Equity dash C4
    equity = []
    with (CAT / "cell_catalogue_all_nonempty.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] == "Equity Dash" and r["cell"] in {
                "C4",
                "C5",
                "C6",
                "A4",
                "A8",
                "B3",
                "B4",
            }:
                equity.append(
                    {
                        "cell": r["cell"],
                        "class": r["cell_class"],
                        "value": r["cached_value"],
                        "formula": r.get("formula", ""),
                    }
                )

    # Build label map by row for Ec_IO column B/C pairs
    by_coord = {r["cell"]: r for r in cells}
    param_candidates = []
    for lit in sorted(literals, key=lambda x: (x["row"], x["col"])):
        cell = lit["cell"]
        # nearby labels: same row col A/B, and row above
        row = lit["row"]
        nearby = []
        for c in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "M", "N", "O", "P", "Q", "R", "S", "T"):
            coord = f"{c}{row}"
            if coord in by_coord and by_coord[coord]["cell_class"] == "label_or_text":
                nearby.append(f"{coord}={by_coord[coord]['cached_value'][:80]}")
        param_candidates.append(
            {
                **lit,
                "cp": cp.get(cell),
                "nearby_labels": nearby,
            }
        )

    report = {
        "active_gm_sha256": NEW,
        "ec_io_nonempty": len(cells),
        "ec_io_formulas": len(formulas),
        "ec_io_literals": len(literals),
        "ec_io_labels": len(labels),
        "cp_classified_count": len(cp),
        "gtc_input_rows": len(gtc_inputs),
        "kpi_rows": len(kpis),
        "literals": param_candidates,
        "formulas": formulas,
        "cp_map": cp,
        "gtc_inputs": gtc_inputs,
        "kpis": kpis,
        "equity_dash_key_cells": equity,
        "consumer_sheets_from_edges": {k: list(v) if isinstance(v, set) else v for k, v in consumers.items()},
        "label_snapshot": [
            {"cell": x["cell"], "value": x["value"]}
            for x in sorted(labels, key=lambda z: (z["row"], z["col"]))
        ],
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Wrote", OUT)
    print("nonempty", len(cells), "formulas", len(formulas), "literals", len(literals), "cp", len(cp))
    print("--- CP classifications ---")
    for cell, r in sorted(cp.items(), key=lambda kv: (int("".join(filter(str.isdigit, kv[0])) or 0), kv[0])):
        print(cell, r["value"], r["classification"], "|", r["nearby_labels"][:70])
    print("--- All literals ---")
    for lit in param_candidates:
        print(lit["cell"], lit["value"], lit.get("cp", {}).get("classification") if lit.get("cp") else "NO_CP", lit["nearby_labels"][:2])
    print("--- Equity ---")
    for e in equity:
        print(e)
    print("--- KPIs ---")
    for k in kpis:
        print(k)


if __name__ == "__main__":
    main()
