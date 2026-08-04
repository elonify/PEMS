import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\Emmanuel Onwuka\Desktop\PEMS")
keys = [
    "Ec_IO!C5",
    "Ec_IO!C7",
    "Ec_IO!C12",
    "Ec_IO!C14",
    "Ec_IO!C15",
    "Ec_IO!C17",
    "Ec_IO!C18",
    "Ec_IO!C19",
    "Ec_IO!C20",
    "Ec_IO!C21",
    "Ec_IO!C22",
    "Ec_IO!C23",
    "Ec_IO!C24",
    "Ec_IO!C25",
    "Ec_IO!C26",
    "Ec_IO!G18",
    "Ec_IO!G20",
    "Ec_IO!G21",
    "Ec_IO!G22",
    "Ec_IO!G24",
    "Ec_IO!G25",
    "Ec_IO!G26",
    "Ec_IO!$C$5",
    "Ec_IO!$C$12",
    "Ec_IO!$C$15",
    "Ec_IO!$C$17",
    "Ec_IO!$G$22",
    "Ec_IO!$G$24",
    "'Equity Dash'!C4",
    "Equity Dash!C4",
]
refs = defaultdict(list)
with (ROOT / "docs/workbook/catalogue/formula_catalogue.csv").open(encoding="utf-8") as f:
    for r in csv.DictReader(f):
        fml = r["formula"] or ""
        for k in keys:
            if k in fml:
                refs[k].append(f"{r['worksheet']}!{r['cell']}")

for k in sorted(refs, key=lambda x: -len(refs[x])):
    v = refs[k]
    sheets = sorted({x.split("!")[0] for x in v})
    print(f"{k}\tcount={len(v)}\tsheets={sheets[:12]}")

# broader patterns
for needle in ["C12", "C17", "C15", "C5", "G22", "G24"]:
    n = 0
    sheets = set()
    with (ROOT / "docs/workbook/catalogue/formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            fml = r["formula"] or ""
            if "Ec_IO" in fml and needle in fml:
                n += 1
                sheets.add(r["worksheet"])
    print(f"broad Ec_IO+{needle}: {n} formulas sheets={sorted(sheets)[:20]}")
