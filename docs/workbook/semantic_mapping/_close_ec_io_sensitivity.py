import csv
import json
from collections import Counter
from pathlib import Path

OUT = Path(r"C:\Users\Emmanuel Onwuka\Desktop\PEMS\docs\workbook\semantic_mapping")
full = OUT / "CRITICAL_PATH_LITERAL_REGISTER_FULL.csv"
rows = list(csv.DictReader(full.open(encoding="utf-8")))
fields = list(rows[0].keys())
cells_sens = {
    "D76",
    "F76",
    "D77",
    "F77",
    "D78",
    "F78",
    "D79",
    "F79",
    "E89",
    "E90",
    "E91",
    "E92",
    "E93",
    "E95",
    "E96",
    "E97",
    "E98",
    "E99",
    "E100",
}
n = 0
for r in rows:
    if r["worksheet"] == "Ec_IO" and r["cell"] in cells_sens and r["status"] == "UNRESOLVED":
        r["classification"] = "PRESENTATION"
        r["proposed_classification"] = "PRESENTATION"
        r["evidence"] = (
            "Ec_IO oil-price / discount-rate sensitivity table residual "
            "(NPV / Disc. Payout) — presentation/scenario table, not case INPUT"
        )
        r["confidence"] = "HIGH"
        r["decision_required"] = "NONE"
        r["status"] = "RESOLVED"
        r["impact"] = "Sensitivity table seed; deferred with Analysis/sensitivity scope"
        r["surrounding_context"] = "Sensitivity table (Oil Price NPV/Payout or Discount Rate NPV)"
        n += 1

with full.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

unres = [r for r in rows if r["status"] == "UNRESOLVED"]
res = [r for r in rows if r["status"] == "RESOLVED"]
with (OUT / "CRITICAL_PATH_LITERALS_UNRESOLVED.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(unres)

md = [
    "# Critical-Path Unresolved Literals — Exact Location Register",
    "",
    "**GM SHA:** `87EF7439A8F19C52B5B948D379D1752B327144CCDBC36758A780A93EC71121FB`",
    f"**Total critical-path numeric literals:** {len(rows)}",
    f"**Resolved:** {len(res)}",
    f"**Still UNRESOLVED:** {len(unres)}",
    "",
]
if not unres:
    md.append("**None remaining.** All critical-path numeric literals classified or controlled.")
else:
    md += [
        "| Sheet | Cell | Value | Context | Module | Status |",
        "|-------|------|------:|---------|--------|--------|",
    ]
    for r in unres:
        md.append(
            f"| {r['worksheet']} | {r['cell']} | {r['literal_value']} | "
            f"{(r.get('surrounding_context') or '')[:50]} | {r['critical_path_module']} | UNRESOLVED |"
        )
(OUT / "CRITICAL_PATH_UNRESOLVED_LITERALS.md").write_text("\n".join(md) + "\n", encoding="utf-8")

summary = {
    "total": len(rows),
    "resolved": len(res),
    "unresolved": len(unres),
    "reclass_ec_io_sensitivity": n,
    "by_classification": dict(Counter(r["classification"] for r in rows)),
}
(OUT / "CRITICAL_PATH_LITERAL_RESOLUTION_SUMMARY.json").write_text(
    json.dumps(summary, indent=2), encoding="utf-8"
)
print(json.dumps(summary, indent=2))
