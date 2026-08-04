# FORMULA / CELL CATALOGUE — ACTIVE BASELINE

**Status:** **ACTIVE**  
**Authoritative workbook:** `docs/workbook/Workbook_History/Econ_Model_PEMS_confirmed_2026-08-03.xlsx`  
**Version label:** Confirmed-2026-08-03  
**SHA256 (ACTIVE):** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**PREVIOUS DOCUMENTED GM HASH — SUPERSEDED BY RE-FREEZE:** `87EF7439A8F19C52B5B948D379D1752B327144CCDBC36758A780A93EC71121FB`  
**Extracted:** see `extraction_summary.json` (re-extract after re-freeze)  
**Script:** `_extract_gm_readonly.py` (refuses extract if SHA ≠ active)  
**GM modified by extraction:** **No**

**Historical (STALE):** `catalogue/historical_intake_F6A1992F/` — SHA `F6A1992F…3006`

---

## Inventory (active)

| Metric | Count |
|--------|------:|
| Worksheets | **38** |
| Non-empty cells | **109,157** |
| Formula cells | **86,973** |
| Formulas with cached value | **86,973** |
| Formulas without cache | **0** |
| Literal numeric/date/bool candidates | **10,470** |
| Data validations | **178** |
| Defined names (openpyxl) | **192** |

---

## Artifacts (all tagged with active SHA256)

| File | Role |
|------|------|
| `formula_catalogue.csv` | All formulas + cache + precedents |
| `cell_catalogue_all_nonempty.csv` | All non-empty cells |
| `sheet_summary.csv` | Per-sheet counts |
| `data_validations.csv` | DV / dropdowns |
| `defined_names.csv` | Defined names |
| `extraction_summary.json` | Machine summary + sheet list |
| `ACTIVE_VS_HISTORICAL_DIFF.json` | Diff vs intake catalogue |
| `ACTIVE_VS_HISTORICAL_FORMULA_DIFF.csv` | Added/removed/changed formulas |
| `ACTIVE_BASELINE.md` | Active marker |
| `REEXTRACT_REPORT.json` | Re-extract rollup |

---

## Diff vs historical intake catalogue

| Metric | Value |
|--------|------:|
| Formulas added | **1,714** |
| Formulas removed | **2,232** |
| Formulas changed (same sheet+cell, different formula text) | **401** |
| Worksheets added | **Project_NCF** |
| Worksheets removed | **Project_NCF_Con (2)**, **Sheet1** |

---

## Unresolved items (active extract)

| Item | Status |
|------|--------|
| `Project_NCF!AU14` `#NUM!` | OPEN — see WORKBOOK_ERROR_STATUS |
| 10,471 literals | UNCLASSIFIED (input vs constant) |
| 18 Analysis DataTableFormula cells | Constructs — not auto-errors |
| Full dependency order proven | No |

---

## Fidelity claim

**Formula-level implementation fidelity: UNCLAIMED**
