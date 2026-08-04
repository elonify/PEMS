"""Read-only FLGT/Royalties evidence. Does not modify GM."""
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\Emmanuel Onwuka\Desktop\PEMS")
OUT = ROOT / "docs/workbook/semantic_mapping/FLGT_ROYALTIES_EVIDENCE_EXTRACT.json"
CAT = ROOT / "docs/workbook/catalogue"
VAL = ROOT / "docs/workbook/Validation_Datasets"
SHEETS = ["Royalties", "FLGT"]


def main() -> None:
    cells = defaultdict(dict)
    with (CAT / "cell_catalogue_all_nonempty.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] in SHEETS:
                cells[r["worksheet"]][r["cell"]] = r

    def layout(ws, max_row=20, max_col=30):
        out = []
        d = cells[ws]
        for row in range(1, max_row + 1):
            for col_i in range(1, max_col + 1):
                col = ""
                n = col_i
                while n:
                    n, rem = divmod(n - 1, 26)
                    col = chr(65 + rem) + col
                c = f"{col}{row}"
                if c in d:
                    r = d[c]
                    out.append(
                        {
                            "cell": c,
                            "class": r["cell_class"][:10],
                            "v": (r.get("formula") or r["cached_value"])[:140],
                        }
                    )
        return out

    # Labels only
    labels = defaultdict(list)
    for ws in SHEETS:
        for c, r in cells[ws].items():
            if r["cell_class"] == "label_or_text":
                labels[ws].append({"cell": c, "v": r["cached_value"][:90]})

    # Key formulas sample - first rows + known KPI cells
    key_want = {
        "Royalties": set(),
        "FLGT": {
            "AB51",
            "AC51",
            "AD51",
            "AM51",
            "W51",
            "X51",
            "AB5",
            "AC5",
            "AD5",
            "W5",
            "X5",
        },
    }
    # collect row 1-8 formulas for both
    samples = defaultdict(list)
    refs = defaultdict(Counter)
    with (CAT / "formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] not in SHEETS:
                continue
            fml = r["formula"] or ""
            row = int("".join(ch for ch in r["cell"] if ch.isdigit()) or 0)
            if row <= 8 or r["cell"] in key_want.get(r["worksheet"], set()) or row in (
                51,
                50,
                49,
            ):
                samples[r["worksheet"]].append(
                    {
                        "cell": r["cell"],
                        "f": fml[:200],
                        "c": r["cached_value"][:50],
                    }
                )
            for m in re.findall(
                r"(?:Ec_IO|Prod_Summary|Fiscal Terms_PIA|Block_TC|Cap_Allow|Royalties|FLGT|Analysis)!?\$?[A-Z]+\$?\d+",
                fml,
            ):
                refs[r["worksheet"]][m] += 1

    # consumers of FLGT and Royalties
    consumers = Counter()
    with (CAT / "formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            fml = r["formula"] or ""
            if "FLGT!" in fml and r["worksheet"] not in SHEETS:
                consumers["FLGT→" + r["worksheet"]] += 1
            if "Royalties!" in fml and r["worksheet"] not in SHEETS:
                consumers["Royalties→" + r["worksheet"]] += 1

    # GTC
    kpis = []
    with (VAL / "expected_outputs/GTC-001_kpi_and_intermediates.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            blob = " ".join(
                [r.get("worksheet") or "", r.get("formula") or "", r.get("metric_label_source") or ""]
            )
            if any(x in blob for x in ("FLGT", "Royalty", "Royalt", "ERR")):
                kpis.append(
                    {
                        "ws": r.get("worksheet"),
                        "cell": r.get("cell"),
                        "exp": r.get("expected_value"),
                        "fml": (r.get("formula") or "")[:140],
                        "label": (r.get("metric_label_source") or "")[:60],
                    }
                )

    # expected formula results for key FLGT cells
    gtc_cells = []
    want_cells = [
        ("FLGT", "AB51"),
        ("FLGT", "AC51"),
        ("FLGT", "AD51"),
        ("FLGT", "AM51"),
        ("FLGT", "W51"),
        ("FLGT", "X51"),
        ("Ec_IO", "G11"),
        ("Ec_IO", "G15"),
        ("RESULTS Equity", "N22"),
        ("RESULTS Equity", "N23"),
        ("RESULTS Equity", "N24"),
        ("RESULTS Equity", "N25"),
    ]
    with (VAL / "expected_outputs/formula_cached_results_all.csv").open(encoding="utf-8") as f:
        idx = {(r["worksheet"], r["cell"]): r for r in csv.DictReader(f)}
    for ws, cell in want_cells:
        r = idx.get((ws, cell))
        if r:
            gtc_cells.append(
                {
                    "ws": ws,
                    "cell": cell,
                    "exp": r.get("expected_value"),
                    "fml": (r.get("formula") or "")[:160],
                }
            )

    # Royalties all labels + row 1-5 full
    roy_layout = layout("Royalties", 15, 29)
    flgt_layout = layout("FLGT", 12, 40)

    # FLGT literals
    flgt_lit = []
    for c, r in cells["FLGT"].items():
        if r["cell_class"] == "constant_or_input_value":
            flgt_lit.append(
                {
                    "cell": c,
                    "v": r["cached_value"][:40],
                    "nf": r.get("number_format", ""),
                }
            )

    report = {
        "royalties_labels": labels["Royalties"],
        "flgt_labels": labels["FLGT"],
        "royalties_layout": roy_layout,
        "flgt_layout": flgt_layout,
        "samples": dict(samples),
        "refs": {k: dict(v.most_common(40)) for k, v in refs.items()},
        "consumers": dict(consumers.most_common(30)),
        "kpis": kpis,
        "gtc_cells": gtc_cells,
        "flgt_literals": flgt_lit[:100],
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Wrote", OUT)
    print("Roy labels", len(labels["Royalties"]), "FLGT labels", len(labels["FLGT"]))
    print("consumers", dict(consumers.most_common(20)))
    print("refs Royalties top", list(refs["Royalties"].most_common(15)))
    print("refs FLGT top", list(refs["FLGT"].most_common(20)))
    print("=== GTC ===")
    for g in gtc_cells:
        print(g["ws"], g["cell"], g["exp"], g["fml"][:100])
    print("=== Roy layout ===")
    for x in roy_layout[:80]:
        print(x["cell"], x["class"], x["v"][:90])
    print("=== FLGT labels ===")
    for x in labels["FLGT"]:
        print(x["cell"], x["v"])
    print("=== FLGT samples key ===")
    for x in samples["FLGT"]:
        if x["cell"] in key_want["FLGT"] or x["cell"].endswith("51") or x["cell"][-1] in "123456" and int(
            "".join(ch for ch in x["cell"] if ch.isdigit()) or 0
        ) <= 6:
            print(x["cell"], x["f"][:120], "=>", x["c"][:30])


if __name__ == "__main__":
    main()
