"""Read-only CR/NCF evidence extract. Does not modify GM."""
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\Emmanuel Onwuka\Desktop\PEMS")
OUT = ROOT / "docs/workbook/semantic_mapping/CR_NCF_EVIDENCE_EXTRACT.json"
CAT = ROOT / "docs/workbook/catalogue"
VAL = ROOT / "docs/workbook/Validation_Datasets"

VISIBLE = [
    "CR Econ",
    "HT_NCF_Oil",
    "CIT_NCF_Oil",
    "CIT_NCF_Gas",
    "Project_NCF",
    "HT_NCF_Oil Equity",
    "CIT_NCF_Oil Equity",
    "CIT_NCF_Gas Equity",
    "Equity_NCF_Con",
]
HIDDEN = ["HT_NCF", "CIT_NCF", "Project_NCF_Con"]
ALL = VISIBLE + HIDDEN


def main() -> None:
    cells = defaultdict(dict)
    with (CAT / "cell_catalogue_all_nonempty.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] in ALL:
                cells[r["worksheet"]][r["cell"]] = r

    # CR Econ labels row 1-10
    cr_layout = []
    d = cells["CR Econ"]
    for row in range(1, 12):
        for col_i in range(1, 28):
            col = ""
            n = col_i
            while n:
                n, rem = divmod(n - 1, 26)
                col = chr(65 + rem) + col
            c = f"{col}{row}"
            if c in d:
                r = d[c]
                cr_layout.append(
                    {
                        "cell": c,
                        "class": r["cell_class"][:10],
                        "v": (r.get("formula") or r["cached_value"])[:150],
                    }
                )

    # Project_NCF key labels and KPI-like cells
    pn_labels = []
    for c, r in cells["Project_NCF"].items():
        if r["cell_class"] == "label_or_text":
            pn_labels.append({"cell": c, "v": r["cached_value"][:80]})

    # KPI pack + expected for key cells
    kpi = []
    with (VAL / "expected_outputs/GTC-001_kpi_and_intermediates.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ws = r.get("worksheet") or ""
            fml = r.get("formula") or ""
            if any(
                x in ws or x in fml
                for x in (
                    "Project_NCF",
                    "HT_NCF",
                    "CIT_NCF",
                    "CR Econ",
                    "Equity",
                    "IRR",
                    "NPV",
                )
            ):
                kpi.append(
                    {
                        "ws": ws,
                        "cell": r.get("cell"),
                        "exp": r.get("expected_value"),
                        "fml": fml[:140],
                        "label": (r.get("metric_label_source") or "")[:50],
                    }
                )

    want = [
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
        ("Project_NCF", "AK5"),
        ("HT_NCF_Oil", "AS51"),
        ("HT_NCF_Oil", "AT51"),
        ("HT_NCF_Oil", "AS59"),
        ("HT_NCF_Oil", "AV51"),
        ("CIT_NCF", "U55"),
        ("CIT_NCF", "U56"),
        ("CIT_NCF", "U57"),
        ("CIT_NCF", "U58"),
        ("CIT_NCF", "U59"),
        ("CR Econ", "G8"),
        ("CR Econ", "H8"),
        ("CR Econ", "I8"),
        ("Equity_NCF_Con", "AG51"),
        ("Equity_NCF_Con", "AH51"),
    ]
    gtc = []
    with (VAL / "expected_outputs/formula_cached_results_all.csv").open(encoding="utf-8") as f:
        idx = {(r["worksheet"], r["cell"]): r for r in csv.DictReader(f)}
    for ws, cell in want:
        r = idx.get((ws, cell))
        if r:
            gtc.append(
                {
                    "ws": ws,
                    "cell": cell,
                    "exp": r.get("expected_value"),
                    "fml": (r.get("formula") or "")[:180],
                }
            )
        elif cell in cells.get(ws, {}):
            rr = cells[ws][cell]
            gtc.append(
                {
                    "ws": ws,
                    "cell": cell,
                    "exp": rr["cached_value"][:60],
                    "fml": (rr.get("formula") or "")[:180],
                    "src": "catalogue",
                }
            )

    # Cross refs into CR Econ and Project_NCF
    refs_in = defaultdict(Counter)
    consumers = Counter()
    with (CAT / "formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            fml = r["formula"] or ""
            if r["worksheet"] == "CR Econ":
                for m in re.findall(
                    r"(?:Ec_IO|FLGT|Cap_Allow|Prod_Summary|Fiscal Terms_PIA|Royalties|Block_TC)![A-Z$0-9]+",
                    fml,
                ):
                    refs_in["CR Econ"][m.split("!")[0]] += 1
            if r["worksheet"] == "Project_NCF":
                for m in re.findall(
                    r"(?:HT_NCF|CIT_NCF|CR Econ|FLGT|Cap_Allow|Ec_IO)![A-Z$0-9']+",
                    fml,
                ):
                    sheet = m.split("!")[0].replace("'", "")
                    refs_in["Project_NCF"][sheet] += 1
            if r["worksheet"] == "HT_NCF_Oil":
                for m in re.findall(r"(?:CR Econ|FLGT|Cap_Allow|Ec_IO)!", fml):
                    refs_in["HT_NCF_Oil"][m.replace("!", "")] += 1
            if "Project_NCF!" in fml and r["worksheet"] not in ("Project_NCF",):
                consumers["Project_NCF→" + r["worksheet"]] += 1
            if "CR Econ!" in fml and r["worksheet"] != "CR Econ":
                consumers["CR Econ→" + r["worksheet"]] += 1
            if "Equity Dash" in fml and "Equity" in r["worksheet"]:
                consumers["EquityDash→" + r["worksheet"]] += 1

    # CR Econ row 1-3 headers full width
    cr_labels = []
    for c, r in cells["CR Econ"].items():
        if r["cell_class"] == "label_or_text":
            cr_labels.append({"cell": c, "v": r["cached_value"][:90]})

    # Sample CR Econ formulas row 8 (first data year often)
    cr_f = []
    with (CAT / "formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] == "CR Econ" and r["cell"][1:] in "5678910" or (
                r["worksheet"] == "CR Econ"
                and r["cell"]
                in {
                    "A5",
                    "B5",
                    "C5",
                    "D5",
                    "E5",
                    "F5",
                    "G5",
                    "H5",
                    "I5",
                    "J5",
                    "K5",
                    "L5",
                    "M5",
                    "N5",
                    "O5",
                    "P5",
                    "Q5",
                    "R5",
                    "S5",
                    "T5",
                    "U5",
                    "G8",
                    "H8",
                    "I8",
                    "L1",
                    "U1",
                }
            ):
                cr_f.append(
                    {
                        "cell": r["cell"],
                        "f": r["formula"][:200],
                        "c": r["cached_value"][:40],
                    }
                )

    # Project_NCF labels near AG/AH/AJ
    pn_key = {}
    for c in [
        "AG1",
        "AH1",
        "AJ1",
        "AE1",
        "AF1",
        "AB1",
        "AC1",
        "AD1",
        "AK1",
        "AU1",
        "AG50",
        "AH50",
        "AJ50",
        "AG51",
        "AH51",
        "AJ51",
        "AG58",
        "AU12",
        "AU14",
        "A5",
        "B5",
    ]:
        if c in cells["Project_NCF"]:
            r = cells["Project_NCF"][c]
            pn_key[c] = {
                "class": r["cell_class"],
                "v": (r.get("formula") or r["cached_value"])[:160],
                "cached": r["cached_value"][:50],
            }

    # Equity scaling sample
    eq = []
    with (CAT / "formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] == "Equity_NCF_Con" and "Equity Dash" in (r["formula"] or ""):
                if len(eq) < 15:
                    eq.append({"cell": r["cell"], "f": r["formula"][:160], "c": r["cached_value"][:40]})

    # HT_NCF_Oil row headers A1-A20 style labels col A-B
    ht_lab = []
    for c, r in cells["HT_NCF_Oil"].items():
        if r["cell_class"] == "label_or_text" and c.startswith(("A", "B", "C")) and int(
            "".join(ch for ch in c if ch.isdigit()) or 0
        ) <= 15:
            ht_lab.append({"cell": c, "v": r["cached_value"][:80]})

    report = {
        "cr_layout": cr_layout,
        "cr_labels": sorted(cr_labels, key=lambda x: x["cell"])[:80],
        "cr_formulas_sample": cr_f[:80],
        "pn_labels_sample": sorted(pn_labels, key=lambda x: x["cell"])[:100],
        "pn_key": pn_key,
        "gtc_cells": gtc,
        "kpi_pack": kpi[:40],
        "refs_in": {k: dict(v.most_common(20)) for k, v in refs_in.items()},
        "consumers": dict(consumers.most_common(25)),
        "equity_samples": eq,
        "ht_labels": sorted(ht_lab, key=lambda x: x["cell"])[:60],
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Wrote", OUT)
    print("=== CR layout ===")
    for x in cr_layout[:60]:
        print(x["cell"], x["class"], x["v"][:100])
    print("=== GTC ===")
    for g in gtc:
        print(g["ws"], g["cell"], str(g["exp"])[:40], str(g.get("fml", ""))[:90])
    print("=== refs CR Econ ===", report["refs_in"].get("CR Econ"))
    print("=== refs Project_NCF ===", report["refs_in"].get("Project_NCF"))
    print("=== consumers ===", dict(list(consumers.most_common(15))))
    print("=== pn_key ===")
    for k, v in pn_key.items():
        print(k, v)


if __name__ == "__main__":
    main()
