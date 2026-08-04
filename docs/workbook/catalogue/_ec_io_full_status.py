import csv
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\Emmanuel Onwuka\Desktop\PEMS")
full = ROOT / "docs/workbook/semantic_mapping/CRITICAL_PATH_LITERAL_REGISTER_FULL.csv"
rows = [r for r in csv.DictReader(full.open(encoding="utf-8")) if r["worksheet"] == "Ec_IO"]
print("Ec_IO full rows", len(rows))
print("status", Counter(r["status"] for r in rows))
print("class", Counter(r["classification"] for r in rows))
unres = [r for r in rows if r["status"] == "UNRESOLVED" or r["classification"] == "UNRESOLVED"]
print("unresolved-like", len(unres))
for r in rows:
    if r["classification"] not in ("PRESENTATION",) and int("".join(ch for ch in r["cell"] if ch.isdigit()) or 0) < 40:
        print(
            r["cell"],
            r.get("literal_value") or r.get("value"),
            r["classification"],
            r["status"],
            (r.get("surrounding_context") or r.get("nearby_labels") or "")[:50],
        )

# data validations
print("--- DV ---")
with (ROOT / "docs/workbook/catalogue/data_validations.csv").open(encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["worksheet"] == "Ec_IO":
            print(dict(r))

# layout core
print("--- layout ---")
cells = {}
with (ROOT / "docs/workbook/catalogue/cell_catalogue_all_nonempty.csv").open(encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["worksheet"] == "Ec_IO" and int(r["row"]) <= 35:
            cells[r["cell"]] = r
for row in range(1, 36):
    for col in "ABCDEFGHIJKLMNOPQRST":
        c = f"{col}{row}"
        if c in cells:
            r = cells[c]
            v = (r.get("formula") or r["cached_value"])[:60]
            print(c, r["cell_class"][:12], v)
