"""Read-only Production Profile evidence extract. Does not modify GM."""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\Emmanuel Onwuka\Desktop\PEMS")
OUT = ROOT / "docs/workbook/semantic_mapping/PRODUCTION_EVIDENCE_EXTRACT.json"
CAT = ROOT / "docs/workbook/catalogue"
VAL = ROOT / "docs/workbook/Validation_Datasets"
SEM = ROOT / "docs/workbook/semantic_mapping"
SHEETS = [
    "Production Profile",
    "Prod_Summary",
    "Block_Oil Data",
    "Block_Gas Data",
]
# OML123_Oil_S1 hidden — inventory only
ALL = SHEETS + ["OML123_Oil_S1"]


def main() -> None:
    cells = defaultdict(list)
    with (CAT / "cell_catalogue_all_nonempty.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] in ALL:
                cells[r["worksheet"]].append(r)

    formulas = defaultdict(list)
    with (CAT / "formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] in ALL:
                formulas[r["worksheet"]].append(
                    {
                        "cell": r["cell"],
                        "formula": r["formula"][:200],
                        "cached": r["cached_value"][:80],
                        "nf": r.get("number_format", ""),
                    }
                )

    # Production Profile layout rows 1-30 all nonempty
    pp = {r["cell"]: r for r in cells["Production Profile"]}
    layout = []
    for row in range(1, 35):
        for col_i in range(1, 40):
            # A=1
            col = ""
            n = col_i
            while n:
                n, rem = divmod(n - 1, 26)
                col = chr(65 + rem) + col
            c = f"{col}{row}"
            if c in pp:
                r = pp[c]
                layout.append(
                    {
                        "cell": c,
                        "class": r["cell_class"],
                        "v": (r.get("formula") or r["cached_value"])[:100],
                    }
                )

    # Prod_Summary key labels + formulas sample
    ps = {r["cell"]: r for r in cells["Prod_Summary"]}
    ps_layout = []
    for row in range(1, 51):
        for col in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            c = f"{col}{row}"
            if c in ps:
                r = ps[c]
                ps_layout.append(
                    {
                        "cell": c,
                        "class": r["cell_class"],
                        "v": (r.get("formula") or r["cached_value"])[:120],
                    }
                )
            for col2 in "AA AB AC AD AE AF AG AH AI AJ".split():
                c = f"{col2}{row}"
                if c in ps:
                    r = ps[c]
                    ps_layout.append(
                        {
                            "cell": c,
                            "class": r["cell_class"],
                            "v": (r.get("formula") or r["cached_value"])[:120],
                        }
                    )

    # register
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
                        "ctx": (r.get("surrounding_context") or "")[:80],
                        "status": r["status"],
                    }
                )

    # GTC KPIs production related
    kpis = []
    with (VAL / "expected_outputs/GTC-001_kpi_and_intermediates.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ws = r.get("worksheet") or ""
            fml = r.get("formula") or ""
            if ws in ("Prod_Summary", "Production Profile") or "Prod_Summary" in fml or "Production" in (
                r.get("metric_label_source") or ""
            ):
                kpis.append(
                    {
                        "ws": ws,
                        "cell": r.get("cell"),
                        "exp": r.get("expected_value"),
                        "fml": fml[:100],
                        "label": (r.get("metric_label_source") or "")[:60],
                    }
                )

    # consumers of Prod_Summary and Production Profile
    needles = [
        "Prod_Summary!",
        "Production Profile!",
        "Block_Oil Data!",
        "Block_Gas Data!",
        "Ec_IO!C5",
        "Ec_IO!$C$5",
        "Ec_IO!C7",
    ]
    cons = defaultdict(Counter)
    with (CAT / "formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            fml = r["formula"] or ""
            for n in needles:
                if n in fml:
                    cons[n][r["worksheet"]] += 1

    # Ec_IO refs from production sheets
    ec_refs = Counter()
    for ws in SHEETS:
        for r in formulas[ws]:
            fml = r["formula"]
            if "Ec_IO" in fml:
                # crude extract
                import re

                for m in re.findall(r"Ec_IO!?[A-Z$]+\d+", fml):
                    ec_refs[m] += 1
                for m in re.findall(r"Ec_IO!\$[A-Z]+\$\d+", fml):
                    ec_refs[m] += 1

    # sample first formula patterns on Production Profile by row groups
    pp_forms = formulas["Production Profile"]
    # Block oil row 1-15 labels
    bo_layout = []
    bo = {r["cell"]: r for r in cells["Block_Oil Data"]}
    for row in range(1, 16):
        for col in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["AA", "AB", "AC", "AD", "AE"]:
            c = f"{col}{row}"
            if c in bo:
                r = bo[c]
                bo_layout.append(
                    {
                        "cell": c,
                        "class": r["cell_class"][:10],
                        "v": (r.get("formula") or r["cached_value"])[:80],
                    }
                )

    bg_layout = []
    bg = {r["cell"]: r for r in cells["Block_Gas Data"]}
    for row in range(1, 16):
        for col in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["AA", "AB", "AC", "AD", "AE"]:
            c = f"{col}{row}"
            if c in bg:
                r = bg[c]
                bg_layout.append(
                    {
                        "cell": c,
                        "class": r["cell_class"][:10],
                        "v": (r.get("formula") or r["cached_value"])[:80],
                    }
                )

    # data validations production
    dvs = []
    with (CAT / "data_validations.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] in ALL:
                dvs.append(dict(r))

    report = {
        "sheets": {s: len(cells[s]) for s in ALL},
        "formulas": {s: len(formulas[s]) for s in ALL},
        "production_profile_layout": layout,
        "prod_summary_layout": ps_layout[:200],
        "block_oil_header": bo_layout,
        "block_gas_header": bg_layout,
        "register": reg,
        "register_class_counts": {
            f"{a}|{b}": c for (a, b), c in Counter((r["ws"], r["class"]) for r in reg).items()
        },
        "kpis": kpis,
        "consumers": {k: dict(v) for k, v in cons.items()},
        "ec_io_refs_from_production": dict(ec_refs),
        "data_validations": dvs,
        "pp_formula_sample": pp_forms[:80],
        "ps_formula_sample": formulas["Prod_Summary"][:60],
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Wrote", OUT)
    print("PP layout", len(layout), "PS layout", len(ps_layout), "reg", len(reg), "kpis", len(kpis))
    print("consumers Prod_Summary", dict(cons["Prod_Summary!"]))
    print("ec refs", dict(ec_refs.most_common(20)))
    print("--- PP layout ---")
    for x in layout:
        print(x["cell"], x["class"][:8], x["v"][:70])


if __name__ == "__main__":
    main()
