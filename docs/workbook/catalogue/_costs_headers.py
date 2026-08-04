import csv
from pathlib import Path

ROOT = Path(r"C:\Users\Emmanuel Onwuka\Desktop\PEMS")


def col_letter(i: int) -> str:
    col = ""
    n = i
    while n:
        n, rem = divmod(n - 1, 26)
        col = chr(65 + rem) + col
    return col


def load(ws: str):
    d = {}
    with (ROOT / "docs/workbook/catalogue/cell_catalogue_all_nonempty.csv").open(
        encoding="utf-8"
    ) as f:
        for r in csv.DictReader(f):
            if r["worksheet"] == ws:
                d[r["cell"]] = r
    return d


def main() -> None:
    cells = load("Block_TC")
    print("=== Block_TC rows 1-3 (nonempty) ===")
    for row in range(1, 4):
        for col_i in range(1, 100):
            c = f"{col_letter(col_i)}{row}"
            if c in cells:
                r = cells[c]
                v = (r.get("formula") or r["cached_value"])[:55]
                print(f"{c}|{r['cell_class'][:8]}|{v}")

    print("=== Block_TC sample formulas B4 C4 D4 ===")
    with (ROOT / "docs/workbook/catalogue/formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] == "Block_TC" and r["cell"] in {
                "B4",
                "C4",
                "D4",
                "E4",
                "B5",
                "GX4",
                "B48",
            }:
                print(r["cell"], r["formula"][:200], "=>", r["cached_value"][:40])

    ca = load("Cap_Allow")
    print("=== Cap_Allow labels row1-3 first 60 cols ===")
    for col_i in range(1, 80):
        for row in (1, 2, 3):
            c = f"{col_letter(col_i)}{row}"
            if c in ca and ca[c]["cell_class"] == "label_or_text":
                print(c, ca[c]["cached_value"][:70])

    print("=== Cap_Allow key formulas ===")
    want = {
        "B4",
        "C4",
        "FI5",
        "FK5",
        "FL5",
        "FP5",
        "FQ5",
        "FI48",
        "FK48",
        "FL48",
        "FP48",
        "FQ48",
        "GX5",
        "HC5",
    }
    with (ROOT / "docs/workbook/catalogue/formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] == "Cap_Allow" and r["cell"] in want:
                print(r["cell"], r["formula"][:200], "=>", r["cached_value"][:40])

    print("=== Ec_IO cost + RESULTS ===")
    with (ROOT / "docs/workbook/catalogue/formula_catalogue.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] in ("Ec_IO", "RESULTS Equity", "CR Econ") and "Cap_Allow" in (
                r["formula"] or ""
            ):
                if r["worksheet"] == "CR Econ" and r["cell"] not in {"D5", "E5", "FP5", "GX5"}:
                    continue
                print(r["worksheet"], r["cell"], r["formula"][:160], "=>", r["cached_value"][:30])

    print("=== Register ASSUMPTION top ===")
    with (
        ROOT / "docs/workbook/semantic_mapping/CRITICAL_PATH_LITERAL_REGISTER_FULL.csv"
    ).open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["worksheet"] in ("Block_TC", "Cap_Allow", "Block_TC_Gas", "Cap_Allow Gas"):
                if r["classification"] in ("ASSUMPTION", "FORMULA COEFFICIENT"):
                    print(
                        r["worksheet"],
                        r["cell"],
                        r["literal_value"],
                        r["classification"],
                        (r.get("surrounding_context") or "")[:50],
                    )


if __name__ == "__main__":
    main()
