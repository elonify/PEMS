"""Read-only Costs module evidence extract. Does not modify GM."""
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\Emmanuel Onwuka\Desktop\PEMS")
OUT = ROOT / "docs/workbook/semantic_mapping/COSTS_EVIDENCE_EXTRACT.json"
CAT = ROOT / "docs/workbook/catalogue"
VAL = ROOT / "docs/workbook/Validation_Datasets"
SEM = ROOT / "docs/workbook/semantic_mapping"
SHEETS = ["Block_TC", "Block_TC_Gas", "Cap_Allow", "Cap_Allow Gas"]


def main() -> None:
    cells = defaultdict(dict)
    with (CAT / "cell_catalogue_all_nonempty.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] in SHEETS:
                cells[r["worksheet"]][r["cell"]] = r

    # Headers / labels rows 1-8 for Block_TC sample columns
    def layout(ws: str, max_row: int = 12, max_col: int = 40):
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
                            "class": r["cell_class"][:12],
                            "v": (r.get("formula") or r["cached_value"])[:100],
                        }
                    )
        return out

    # Cap_Allow key summary rows - labels in col A/B and totals FI, FL, FK, FP etc
    key_cells = [
        "A1",
        "B1",
        "A2",
        "B2",
        "A3",
        "B3",
        "A4",
        "B4",
        "A5",
        "B5",
        "FI1",
        "FI48",
        "FK48",
        "FL48",
        "FP48",
        "FQ48",
        "GX1",
        "HC1",
    ]
    ca_keys = {}
    for ws in ("Cap_Allow", "Cap_Allow Gas"):
        ca_keys[ws] = {}
        for c in key_cells:
            if c in cells[ws]:
                r = cells[ws][c]
                ca_keys[ws][c] = {
                    "class": r["cell_class"],
                    "v": (r.get("formula") or r["cached_value"])[:150],
                    "cached": r["cached_value"][:60],
                }
        # scan col A labels all rows
        labels = []
        for row in range(1, 59):
            for col in ("A", "B", "C"):
                c = f"{col}{row}"
                if c in cells[ws] and cells[ws][c]["cell_class"] == "label_or_text":
                    labels.append({"cell": c, "v": cells[ws][c]["cached_value"][:80]})
        ca_keys[ws]["labels_ABC"] = labels[:80]

    # Register sample non-presentation
    reg = []
    with (SEM / "CRITICAL_PATH_LITERAL_REGISTER_FULL.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] in SHEETS:
                reg.append(
                    {
                        "ws": r["worksheet"],
                        "cell": r["cell"],
                        "val": r.get("literal_value"),
                        "class": r["classification"],
                        "ctx": (r.get("surrounding_context") or "")[:70],
                    }
                )

    # Formula samples - first 30 per sheet + those with Ec_IO or Prod
    samples = defaultdict(list)
    ec_refs = Counter()
    prod_refs = Counter()
    consumers = Counter()
    with (CAT / "formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            fml = r["formula"] or ""
            if r["worksheet"] in SHEETS:
                if len(samples[r["worksheet"]]) < 40:
                    samples[r["worksheet"]].append(
                        {
                            "cell": r["cell"],
                            "f": fml[:160],
                            "c": r["cached_value"][:40],
                        }
                    )
                for m in re.findall(r"Ec_IO!?\$?[A-Z]+\$?\d+", fml):
                    ec_refs[m] += 1
                for m in re.findall(
                    r"(?:Prod_Summary|Block_Oil Data|Block_Gas Data|Production Profile)![A-Z$]+\d+",
                    fml,
                ):
                    prod_refs[m.split("!")[0]] += 1
            # who consumes Cap_Allow
            if "Cap_Allow" in fml and r["worksheet"] not in SHEETS:
                consumers[r["worksheet"]] += 1
            if "Block_TC" in fml and r["worksheet"] not in SHEETS:
                consumers["via_Block_TC:" + r["worksheet"]] += 1

    # GTC KPIs related to capex/opex
    kpis = []
    with (VAL / "expected_outputs/GTC-001_kpi_and_intermediates.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            blob = " ".join(
                [
                    r.get("worksheet") or "",
                    r.get("formula") or "",
                    r.get("metric_label_source") or "",
                ]
            )
            if any(
                x in blob
                for x in (
                    "Cap_Allow",
                    "CAPEX",
                    "OPEX",
                    "TC",
                    "Technical Cost",
                    "Block_TC",
                )
            ):
                kpis.append(
                    {
                        "ws": r.get("worksheet"),
                        "cell": r.get("cell"),
                        "exp": r.get("expected_value"),
                        "fml": (r.get("formula") or "")[:120],
                        "label": (r.get("metric_label_source") or "")[:60],
                    }
                )

    # Ec_IO N16 etc references to Cap_Allow
    ec_io_cost = []
    with (CAT / "formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] == "Ec_IO" and "Cap_Allow" in (r["formula"] or ""):
                ec_io_cost.append(
                    {
                        "cell": r["cell"],
                        "f": r["formula"][:150],
                        "c": r["cached_value"][:40],
                    }
                )

    # Block_TC row labels col A and first few cost categories
    btc_a = []
    for row in range(1, 71):
        c = f"A{row}"
        if c in cells["Block_TC"]:
            r = cells["Block_TC"][c]
            btc_a.append(
                {
                    "cell": c,
                    "class": r["cell_class"][:10],
                    "v": (r.get("formula") or r["cached_value"])[:90],
                }
            )

    # named ranges cost-related
    names = []
    with (CAT / "defined_names.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            t = (r.get("attr_text") or "") + r["name"]
            if any(
                x in t
                for x in (
                    "Cap_Allow",
                    "Block_TC",
                    "OPEX",
                    "CAPEX",
                    "TC",
                    "Cost",
                    "Allow",
                )
            ):
                names.append({"name": r["name"], "ref": (r.get("attr_text") or "")[:120]})

    report = {
        "block_tc_layout": layout("Block_TC", 10, 20),
        "block_tc_gas_layout": layout("Block_TC_Gas", 10, 15),
        "block_tc_col_a": btc_a,
        "cap_allow_keys": ca_keys,
        "register": reg,
        "register_counts": dict(Counter(f"{r['ws']}|{r['class']}" for r in reg)),
        "formula_samples": dict(samples),
        "ec_refs_from_costs": dict(ec_refs.most_common(30)),
        "prod_refs_from_costs": dict(prod_refs),
        "downstream_consumers_count": dict(consumers.most_common(25)),
        "kpis": kpis,
        "ec_io_cost_formulas": ec_io_cost,
        "named_ranges": names[:40],
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Wrote", OUT)
    print("reg", len(reg), "kpis", len(kpis), "ec_io cost", len(ec_io_cost))
    print("ec refs", dict(ec_refs.most_common(15)))
    print("consumers", dict(consumers.most_common(15)))
    print("--- Block_TC A ---")
    for x in btc_a[:40]:
        print(x["cell"], x["class"], x["v"][:70])
    print("--- Cap_Allow keys ---")
    for c, v in ca_keys["Cap_Allow"].items():
        if c != "labels_ABC":
            print("CA", c, v)
    print("--- labels sample ---")
    for x in ca_keys["Cap_Allow"]["labels_ABC"][:40]:
        print(x)


if __name__ == "__main__":
    main()
