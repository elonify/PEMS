# FORMULA / CELL CATALOGUE

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Golden Master path:** `docs/workbook/Econ_Model_PEMS.xlsx`  
**Catalogue built against SHA256:** `F6A1992F6A3CC27EC587779ADE6CF667B246FB1587296EFD0CD14B47A6783006` (Intake-2026-08-01)  
**Active GM SHA256 (2026-08-03):** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Catalogue status vs active GM:** **STALE — re-extract required**  
**Extraction:** read-only via `catalogue/_extract_gm_readonly.py` (openpyxl)  
**Extracted at:** 2026-08-02 (see `extraction_summary.json`)  
**Policy:** No formulas invented; all formula text and values taken from the Golden Master file as stored.

> **Error confirmation 2026-08-03:** Active GM no longer shows START `#REF!` or CR Econ empty caches; residual **`Project_NCF!AU14` `#NUM!`**. See `../semantic_mapping/WORKBOOK_ERROR_STATUS.md`.

---

## 1. Purpose

Machine-readable catalogue of non-empty cells, formulas, data validations, and defined names from the registered Golden Master, with:

- worksheet + cell references  
- cell class (formula / constant_or_input_value / label_or_text)  
- formula text and Excel **cached** results where present  
- best-effort precedent references extracted from formula text  
- provisional PEMS module area from **worksheet name heuristics only**  
- ambiguity flags (no guessing of business meaning)

---

## 2. Artifact index

| Artifact | Description |
|----------|-------------|
| `formula_catalogue.csv` | **87,491** formula cells (full formula text + cache + precedents) |
| `cell_catalogue_all_nonempty.csv` | **110,267** non-empty cells (all classes) |
| `sheet_summary.csv` | Per-worksheet counts and dimensions |
| `data_validations.csv` | **178** data-validation rules (dropdowns / constraints) |
| `defined_names.csv` | **192** defined names (openpyxl enumeration) |
| `comments.csv` | Comment scan (0 cell comments recovered in this extraction) |
| `ambiguous_formulas_no_cached_value.csv` | **60** formulas with empty value cache |
| `extraction_summary.json` | Machine summary counts |
| `_extract_gm_readonly.py` | Reproducible extraction script (does not modify xlsx) |

---

## 3. Inspection coverage

| Metric | Count |
|--------|------:|
| Worksheets inspected | **39** / 39 |
| Non-empty cells catalogued | **110,267** |
| Formula cells | **87,491** |
| Formulas with cached value | **87,431** |
| Formulas without cached value | **60** |
| Label/text literals | (see sheet_summary) |
| Constant/input-candidate literals | **10,727** |
| Data validations | **178** |
| Defined names (extracted) | **192** |

Workbook manifest previously reported 230 defined names via workbook XML; openpyxl enumeration yields **192**. Difference is flagged as **AMBIGUOUS_DEFINED_NAME_COUNT** (tooling visibility), not resolved by invention.

---

## 4. Cell classification scheme (as stored)

| `cell_class` | Meaning |
|--------------|---------|
| `formula` | Cell value starts with `=` in formula view |
| `constant_or_input_value` | Numeric/date/bool literal (Excel does **not** mark input vs constant) |
| `label_or_text` | String literal |

### Ambiguity flags

| Flag | Meaning |
|------|---------|
| `NO_CACHED_VALUE` | Formula exists; `data_only` cache empty — expected numeric result not available without Excel recalculation |
| `INPUT_VS_CONSTANT_AMBIGUOUS` | Literal number/date/bool — cannot distinguish user input vs hard-coded constant without further model documentation |

### Structural / UI features

- **Data validation / dropdowns:** recorded in `data_validations.csv` (`type`, `sqref`, `formula1`/`formula2`).  
- **Openpyxl warnings:** some Data Validation **extensions** and Conditional Formatting **extensions** are not fully supported by openpyxl — may be incomplete vs Excel UI.  
- **Comments:** extraction recovered **0** comments; if comments exist in Excel, they require alternate tooling — flagged as coverage gap.  
- **Analysis sheet:** contains Excel data-table formulas and some `#REF!` cached results — flagged for human review; not “fixed” in catalogue.

---

## 5. Per-worksheet summary (formulas)

| Worksheet | State | Module area (heuristic) | Non-empty | Formulas | Constants | Labels | DV |
|-----------|-------|-------------------------|----------:|---------:|----------:|-------:|---:|
| Oil Input | hidden | Input / Control | 23541 | 16808 | 3085 | 3648 | 0 |
| Gas Input | hidden | Input / Control | 22590 | 17709 | 1234 | 3647 | 0 |
| YTD Budget APN (2) | hidden | Unclassified — needs human review | 4033 | 1053 | 2174 | 806 | 156 |
| START | visible | Input / Control | 96 | 30 | 1 | 65 | 1 |
| Checklist | visible | Input / Control | 87 | 35 | 16 | 36 | 0 |
| Model Map | visible/hidden* | Input / Control | 260 | 0 | 6 | 254 | 7 |
| Master | visible | Input / Control | 29 | 0 | 0 | 29 | 0 |
| Fiscal Terms_PIA | visible | Fiscal Terms | 303 | 5 | 124 | 174 | 0 |
| Ec_IO | visible | Input / Control | 227 | 91 | 17 | 119 | 3 |
| RESULTS Equity | visible | Results / Dashboard | 107 | 62 | 0 | 45 | 0 |
| Analysis | visible | Results / Dashboard | 4445 | 2066 | 2210 | 169 | 1 |
| STOIIP | visible | Reservoir | 573 | 267 | 270 | 36 | 0 |
| GIIP | visible | Reservoir | 573 | 267 | 270 | 36 | 0 |
| Production Profile | visible | Production | 400 | 310 | 28 | 62 | 1 |
| Block_Oil Data | visible | Production | 1889 | 1618 | 95 | 176 | 0 |
| Block_Gas Data | visible | Production | 1719 | 1463 | 112 | 144 | 0 |
| OML123_Oil_S1 | hidden | Production | 610 | 337 | 105 | 168 | 1 |
| Prod_Summary | visible | Production | 879 | 849 | 0 | 30 | 0 |
| Block_TC | visible | Cost / Capital Allowance | 3933 | 3356 | 242 | 335 | 1 |
| Block_TC_Gas | visible | Cost / Capital Allowance | 3633 | 3253 | 58 | 322 | 0 |
| Cap_Allow | visible | Cost / Capital Allowance | 8634 | 8136 | 163 | 335 | 1 |
| Cap_Allow Gas | visible | Cost / Capital Allowance | 8604 | 8103 | 163 | 338 | 0 |
| Royalties | visible | Fiscal / Royalty | 740 | 712 | 0 | 28 | 0 |
| FLGT | visible | Fiscal / Royalty | 1595 | 1435 | 90 | 70 | 0 |
| Equity Dash | visible | Results / Dashboard | 59 | 15 | 15 | 29 | 2 |
| CR Econ | visible | Results / Dashboard | 994 | 948 | 0 | 46 | 0 |
| HT_NCF | hidden | Cash Flow / Tax NCF | 2011 | 1901 | 21 | 89 | 0 |
| CIT_NCF | hidden | Cash Flow / Tax NCF | 1455 | 1391 | 0 | 64 | 0 |
| HT_NCF_Oil | visible | Cash Flow / Tax NCF | 2081 | 1960 | 23 | 98 | 0 |
| CIT_NCF_Oil | visible | Cash Flow / Tax NCF | 1553 | 1470 | 5 | 78 | 0 |
| Project_NCF_Con | hidden | Cash Flow / Tax NCF | 1725 | 1629 | 19 | 77 | 0 |
| CIT_NCF_Gas | visible | Cash Flow / Tax NCF | 1553 | 1454 | 21 | 78 | 0 |
| Project_NCF_Con (2) | visible | Cash Flow / Tax NCF | 1752 | 1615 | 57 | 80 | 0 |
| END | visible | Unclassified / Navigation | 1 | 0 | 1 | 0 | 0 |
| HT_NCF_Oil Equity | visible | Cash Flow / Tax NCF | 2216 | 2097 | 21 | 98 | 0 |
| CIT_NCF_Oil Equity | visible | Cash Flow / Tax NCF | 1769 | 1689 | 2 | 78 | 0 |
| CIT_NCF_Gas Equity | visible | Cash Flow / Tax NCF | 1821 | 1723 | 20 | 78 | 0 |
| Equity_NCF_Con | visible | Cash Flow / Tax NCF | 1682 | 1588 | 21 | 73 | 0 |
| Sheet1 | visible | Unclassified / Navigation | 95 | 46 | 38 | 11 | 0 |

\*Visibility as recorded in `sheet_summary.csv` / workbook state at extraction.

---

## 6. Formula catalogue columns

`worksheet, sheet_state, cell, row, col, cell_class, formula, cached_value, cached_value_type, number_format, precedents_extracted, precedent_count, module_area, data_type_openpyxl, ambiguity_flag, notes`

**Traceability key:** `(worksheet, cell)` → formula text → cached expected value (when present).

Precedents are **regex-extracted** from formula text (best-effort). They are not a full Excel calculation graph and may include false positives/negatives — flagged as tooling limitation, not business invention.

---

## 7. Unresolved / ambiguous mappings (counts)

| Category | Count | Notes |
|----------|------:|-------|
| Formulas with no cached expected value | **60** | All on **CR Econ** sheet — see `ambiguous_formulas_no_cached_value.csv` |
| Literals ambiguous as input vs constant | **10,727** | Requires model documentation / Model Map interpretation |
| Sheet module “Unclassified — needs human review” formulas | **1,053** | Primarily **YTD Budget APN (2)** |
| Sheet module “Unclassified / Navigation” formulas | **46** | Sheet1 etc. |
| Defined name count mismatch (XML 230 vs openpyxl 192) | **1 issue** | Tooling |
| Cell comments not recovered | **unknown** | 0 extracted |
| Analysis data tables / `#REF!` caches | **present** | Do not use `#REF!` cells as golden expected values |
| openpyxl DV/CF extension gaps | **unknown completeness** | Partial DV capture (178 rules) |

**Total discrete ambiguity flags of primary interest for implementation:**  
60 (no cache) + 10,727 (input vs constant) + module unclassified formula cells (1,053 + 46) = treat as **open mapping work**, not closed business interpretation.

---

## 8. Corresponding PEMS domain areas (provisional)

Module area is **name-heuristic only** (see extractor `module_for_sheet`). It is an implementation planning aid, **not** a claim that every cell belongs to that domain after business analysis.

Authoritative business placement still requires module specifications when coding begins.

---

## 9. Fidelity claim status

| Claim | Status |
|-------|--------|
| Formula **text** catalogue exists for all formula cells found | **Yes** |
| Cached **values** available for regression for most formulas | **Yes (87,431 / 87,491)** |
| Full dependency graph proven | **No** (precedent extraction best-effort only) |
| Every literal classified as input vs constant | **No** |
| Human-approved semantic mapping complete | **No** |
| **Formula-level implementation fidelity claimable** | **No — not yet** |

---

## 10. How to regenerate (read-only)

```text
python docs/workbook/catalogue/_extract_gm_readonly.py
```

Does not modify `Econ_Model_PEMS.xlsx`.


**Note:** Active GM re-frozen 2026-08-03 to SHA D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA. Prior documented active SHA 87EF7439A8F19C52B5B948D379D1752B327144CCDBC36758A780A93EC71121FB is SUPERSEDED BY RE-FREEZE.
