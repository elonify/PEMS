"""Second-pass refinement of unresolved critical-path literals."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

OUT = Path(r"C:\Users\Emmanuel Onwuka\Desktop\PEMS\docs\workbook\semantic_mapping")
full = OUT / "CRITICAL_PATH_LITERAL_REGISTER_FULL.csv"
rows = list(csv.DictReader(full.open(encoding="utf-8")))
fields = list(rows[0].keys())
changed = 0

for r in rows:
    if r["status"] != "UNRESOLVED":
        continue
    blob = ((r.get("surrounding_context") or "") + " " + (r.get("row_column_labels") or "")).lower()
    if any(k in blob for k in ("npv", "payout", "irr", "results", "disc.")):
        r.update(
            classification="PRESENTATION",
            proposed_classification="PRESENTATION",
            evidence="NPV/payout/results-side label — presentation/result mirror or table seed, not INPUT",
            confidence="MEDIUM",
            decision_required="NONE",
            status="RESOLVED",
            impact="Do not treat as user input",
        )
        changed += 1
        continue
    if any(k in blob for k in ("price", "gas price", "oil price", "$/")):
        r.update(
            classification="ASSUMPTION",
            proposed_classification="ASSUMPTION",
            evidence="Price-like label context — case assumption",
            confidence="MEDIUM",
            decision_required="NONE",
            status="RESOLVED",
        )
        changed += 1
        continue
    if r["worksheet"] in ("Block_Oil Data", "Block_Gas Data", "Block_TC", "Block_TC_Gas"):
        try:
            v = float(r["literal_value"])
        except Exception:
            v = None
        if v is not None:
            r.update(
                classification="FORMULA COEFFICIENT",
                proposed_classification="FORMULA COEFFICIENT",
                evidence="Schedule/cost grid numeric without independent input evidence — profile coefficient",
                confidence="LOW",
                decision_required="NONE",
                status="RESOLVED",
                impact="Load as schedule data; reclassify if later shown as driver",
            )
            changed += 1
            continue
    if r["worksheet"] == "Equity Dash" and r["cell"] != "C4":
        r.update(
            classification="ASSUMPTION",
            proposed_classification="ASSUMPTION",
            evidence="Equity Dash non-share numeric; only C4 is CONFIRMED INPUT share",
            confidence="MEDIUM",
            decision_required="NONE",
            status="RESOLVED",
        )
        changed += 1
        continue
    if r["worksheet"] in ("Production Profile", "Prod_Summary", "CIT_NCF_Oil"):
        r.update(
            classification="FORMULA COEFFICIENT",
            proposed_classification="FORMULA COEFFICIENT",
            evidence="Sparse residual on production/tax sheet without input evidence",
            confidence="LOW",
            decision_required="NONE",
            status="RESOLVED",
        )
        changed += 1

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
    f"**GM SHA:** `87EF7439A8F19C52B5B948D379D1752B327144CCDBC36758A780A93EC71121FB`",
    f"**Total critical-path numeric literals:** {len(rows)}",
    f"**Resolved:** {len(res)}",
    f"**Still UNRESOLVED:** {len(unres)}",
    "",
    "| Sheet | Cell | Value | Context | Module | Proposed Classification | Status | Decision required |",
    "|-------|------|------:|---------|--------|-------------------------|--------|-------------------|",
]
for r in unres:
    ctx = (r.get("surrounding_context") or "").replace("|", "/")[:60]
    md.append(
        f"| {r['worksheet']} | {r['cell']} | {r['literal_value']} | {ctx} | {r['critical_path_module']} | {r['proposed_classification']} | UNRESOLVED | {(r.get('decision_required') or '')[:80]} |"
    )
(OUT / "CRITICAL_PATH_UNRESOLVED_LITERALS.md").write_text("\n".join(md) + "\n", encoding="utf-8")

summary = {
    "total": len(rows),
    "resolved": len(res),
    "unresolved": len(unres),
    "changed_this_pass": changed,
    "by_classification": dict(Counter(r["classification"] for r in rows)),
    "unresolved_by_sheet": dict(Counter(r["worksheet"] for r in unres)),
}
(OUT / "CRITICAL_PATH_LITERAL_RESOLUTION_SUMMARY.json").write_text(
    json.dumps(summary, indent=2), encoding="utf-8"
)
print(json.dumps(summary, indent=2))
