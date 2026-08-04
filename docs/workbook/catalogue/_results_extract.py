"""Read-only RESULTS Equity inventory. Does not modify GM."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(r"C:\Users\Emmanuel Onwuka\Desktop\PEMS")
OUT = ROOT / "docs/workbook/semantic_mapping/RESULTS_EVIDENCE_EXTRACT.json"
CAT = ROOT / "docs/workbook/catalogue"
VAL = ROOT / "docs/workbook/Validation_Datasets"


def main() -> None:
    cells = {}
    with (CAT / "cell_catalogue_all_nonempty.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] == "RESULTS Equity":
                cells[r["cell"]] = r

    inventory = []
    for c in sorted(cells, key=lambda x: (int("".join(ch for ch in x if ch.isdigit()) or 0), x)):
        r = cells[c]
        inventory.append(
            {
                "cell": c,
                "class": r["cell_class"],
                "formula": (r.get("formula") or "")[:200],
                "value": r["cached_value"][:80],
                "nf": r.get("number_format", ""),
            }
        )

    # GTC KPIs on RESULTS Equity
    kpis = []
    with (VAL / "expected_outputs/GTC-001_kpi_and_intermediates.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("worksheet") == "RESULTS Equity":
                kpis.append(
                    {
                        "cell": r.get("cell"),
                        "exp": r.get("expected_value"),
                        "fml": (r.get("formula") or "")[:160],
                        "label": (r.get("metric_label_source") or "")[:60],
                        "type": r.get("value_type"),
                        "numeric": r.get("use_as_numeric_golden"),
                    }
                )

    # Ec_IO hub metrics that mirror RESULTS
    ecio = []
    with (CAT / "formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] == "Ec_IO" and (
                "RESULTS" in (r["formula"] or "")
                or r["cell"]
                in {
                    "G3",
                    "G4",
                    "G5",
                    "G6",
                    "G7",
                    "G8",
                    "G9",
                    "G10",
                    "G11",
                    "G12",
                    "G13",
                    "G14",
                    "G15",
                    "T7",
                    "T8",
                    "S7",
                    "S13",
                }
            ):
                if len(ecio) < 40:
                    ecio.append(
                        {
                            "cell": r["cell"],
                            "f": r["formula"][:160],
                            "c": r["cached_value"][:50],
                        }
                    )

    report = {
        "nonempty": len(inventory),
        "formulas": sum(1 for x in inventory if x["class"] == "formula"),
        "inventory": inventory,
        "kpis": kpis,
        "ecio_hub_sample": ecio,
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Wrote", OUT, "cells", len(inventory), "kpis", len(kpis))
    for x in inventory:
        print(
            f"{x['cell']}|{x['class'][:8]}|{x['nf']}|{x['formula'][:90] or x['value'][:50]}|{x['value'][:40]}"
        )


if __name__ == "__main__":
    main()
