# Scope Rule — Visible Sheets Only (for classification & readiness)

**Decision date:** 2026-08-03  
**Active Golden Master SHA256:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Authority:** Project direction — hidden sheets ignored for literal/input classification and implementation readiness focus  

---

## Rule

1. **Ignore all hidden worksheets** for:
   - literal / input classification  
   - “Ready for Implementation” input gates  
   - user-facing input UI and manual-entry mapping  

2. **If a literal is on a hidden sheet, ignore it** for PEMS input classification (do not treat as `CONFIRMED_INPUT` / parameter candidate via that sheet).

3. **Do not modify** any hidden sheet (or the Golden Master).

4. Hidden-sheet content **remains in the formula/cell catalogue** for fidelity and dependency evidence; it is **not deleted**.

---

## Hidden sheets on active GM (do not modify)

| Worksheet | Role (name-level only) | Formulas (approx.) | Literals (const) |
|-----------|------------------------|-------------------:|-----------------:|
| Oil Input | Input grid | 16,808 | 3,085 |
| Gas Input | Input grid | 17,709 | 1,234 |
| YTD Budget APN (2) | Budget | 1,053 | 2,174 |
| Model Map | Nomenclature text | 0 | 6 |
| OML123_Oil_S1 | Production series | 337 | 105 |
| HT_NCF | Tax NCF (hidden) | 1,901 | 21 |
| CIT_NCF | Tax NCF (hidden) | 1,391 | 0 |
| Project_NCF_Con | Project NCF (hidden) | 1,629 | 19 |

**Count:** 8 hidden sheets  

---

## Literal classification impact (active catalogue)

| Scope | Unclassified literal candidates |
|-------|--------------------------------:|
| All sheets | 10,471 |
| **Hidden only (ignore)** | **6,644** |
| **Visible only (in scope)** | **3,827** |

Readiness and input work use the **visible-only** set (**3,827**), not 10,471.

---

## What “ignore” does *not* mean

- It does **not** authorize editing or deleting hidden sheets.  
- It does **not** remove catalogue rows.  
- Visible-sheet formulas that **reference** hidden sheets remain in force; those dependencies stay in the graph.  
- Calculation fidelity still requires reproducing **business results** validated on visible outputs (e.g. RESULTS Equity, FLGT, Project_NCF visible). How intermediate logic that currently lives only on a hidden sheet is re-homed in PEMS is an architecture concern — not “skip the economics.”  
- Model Map text may still be used as **documentation evidence** even though the sheet is hidden (read-only reference).

---

## Implementation readiness implication

- Module Ready gates for **inputs** only require classification of **visible-sheet** literals/parameters.  
- Modules whose **primary** workbook surface is hidden (e.g. Oil Input, Gas Input as UI) are **out of scope for manual-entry mapping** unless later re-opened by PO.  
- Prefer visible drivers: **Ec_IO**, **Fiscal Terms_PIA**, **Equity Dash**, **Production Profile**, **Analysis** (if in v1), etc.
