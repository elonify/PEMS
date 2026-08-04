# WORKBOOK_MAPPING_SPECIFICATION.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Living mapping document — Golden Master **registered**; formula/cell catalogue **extracted**; semantic module mapping still living  
**Supersedes:** pre-v2.1 WORKBOOK_MAPPING_SPECIFICATION  

---

## 1. Purpose

Permanent mapping between the Excel Golden Master and the PEMS application.

Records how every worksheet, table, chart, named range, formula group, and report is implemented.

Updated continuously during implementation. **Not a substitute for the Golden Master file itself.**

---

## 2. Workbook Identity

| Attribute | Value |
|-----------|--------|
| Workbook Name | Econ_Model_PEMS.xlsx |
| Canonical path | `docs/workbook/Econ_Model_PEMS.xlsx` |
| Workbook Version | **Confirmed-2026-08-03** (active) |
| Date Approved | Pending formal PO stamp |
| Checksum (SHA256) | **D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA** |
| Author / source | Project-supplied economic model |
| Number of Worksheets | **38** |
| Catalogue / GTC | **ACTIVE** re-extract against this SHA |
| Expected Excel condition | `Project_NCF!AU14` `#NUM!` — **EXPECTED / ACCEPTED IRR NO-SIGN-CHANGE** (AK5:AK49 blank) |
| Number of Named Ranges | 230 (includes tool/system names) |
| Number of Tables | TBD (requires deep scan) |
| Number of Charts | TBD (requires deep scan) |
| Number of VBA Modules | TBD (requires deep scan) |
| Manifest path | `docs/workbook/WORKBOOK_MANIFEST.md` |

---

## 3. Worksheet Inventory (from Golden Master)

Extracted from `Econ_Model_PEMS.xlsx` structure (sheet names and visibility).  
**Module / validation columns** are provisional mapping targets for PEMS — refine during Phase 2 workbook analysis.

| # | Worksheet | Visibility | Provisional PEMS module / role | Mapped | Implemented | Validated |
|---|-----------|------------|--------------------------------|:------:|:-----------:|:---------:|
| 1 | Oil Input | hidden | Input — oil assumptions | ☐ | ☐ | ☐ |
| 2 | Gas Input | hidden | Input — gas assumptions | ☐ | ☐ | ☐ |
| 3 | YTD Budget APN (2) | hidden | Input / budget (analyse) | ☐ | ☐ | ☐ |
| 4 | START | visible | Navigation / control | ☐ | ☐ | ☐ |
| 5 | Checklist | visible | Model QA checklist (process) | ☐ | ☐ | ☐ |
| 6 | Model Map | hidden | Workbook self-map (meta) | ☐ | ☐ | ☐ |
| 7 | Master | visible | Master controls / drivers | ☐ | ☐ | ☐ |
| 8 | Fiscal Terms_PIA | visible | Fiscal regime (PIA terms) | ☐ | ☐ | ☐ |
| 9 | Ec_IO | visible | Economics I/O bridge | ☐ | ☐ | ☐ |
| 10 | RESULTS Equity | visible | Results — equity view | ☐ | ☐ | ☐ |
| 11 | Analysis | visible | Analysis / metrics | ☐ | ☐ | ☐ |
| 12 | STOIIP | visible | Reservoir — oil in place | ☐ | ☐ | ☐ |
| 13 | GIIP | visible | Reservoir — gas in place | ☐ | ☐ | ☐ |
| 14 | Production Profile | visible | Production engine | ☐ | ☐ | ☐ |
| 15 | Block_Oil Data | visible | Block oil dataset | ☐ | ☐ | ☐ |
| 16 | Block_Gas Data | visible | Block gas dataset | ☐ | ☐ | ☐ |
| 17 | OML123_Oil_S1 | hidden | Scenario / asset oil series | ☐ | ☐ | ☐ |
| 18 | Prod_Summary | visible | Production summary | ☐ | ☐ | ☐ |
| 19 | Block_TC | visible | Technical cost — oil/block | ☐ | ☐ | ☐ |
| 20 | Block_TC_Gas | visible | Technical cost — gas | ☐ | ☐ | ☐ |
| 21 | Cap_Allow | visible | Capital allowance (oil) | ☐ | ☐ | ☐ |
| 22 | Cap_Allow Gas | visible | Capital allowance (gas) | ☐ | ☐ | ☐ |
| 23 | Royalties | visible | Royalty engine | ☐ | ☐ | ☐ |
| 24 | FLGT | visible | FLGT / fiscal levy (confirm) | ☐ | ☐ | ☐ |
| 25 | Equity Dash | visible | Dashboard — equity | ☐ | ☐ | ☐ |
| 26 | CR Econ | visible | Contractor economics | ☐ | ☐ | ☐ |
| 27 | HT_NCF | hidden | Hydrocarbon tax NCF (legacy/alt) | ☐ | ☐ | ☐ |
| 28 | CIT_NCF | hidden | CIT NCF (legacy/alt) | ☐ | ☐ | ☐ |
| 29 | HT_NCF_Oil | visible | HT NCF — oil | ☐ | ☐ | ☐ |
| 30 | CIT_NCF_Oil | visible | CIT NCF — oil | ☐ | ☐ | ☐ |
| 31 | Project_NCF_Con | hidden | Project NCF consolidated (alt) | ☐ | ☐ | ☐ |
| 32 | CIT_NCF_Gas | visible | CIT NCF — gas | ☐ | ☐ | ☐ |
| 33 | Project_NCF_Con (2) | visible | Project NCF consolidated | ☐ | ☐ | ☐ |
| 34 | END | visible | Navigation / end | ☐ | ☐ | ☐ |
| 35 | HT_NCF_Oil Equity | visible | HT NCF oil — equity | ☐ | ☐ | ☐ |
| 36 | CIT_NCF_Oil Equity | visible | CIT NCF oil — equity | ☐ | ☐ | ☐ |
| 37 | CIT_NCF_Gas Equity | visible | CIT NCF gas — equity | ☐ | ☐ | ☐ |
| 38 | Equity_NCF_Con | visible | Equity NCF consolidated | ☐ | ☐ | ☐ |
| 39 | Sheet1 | visible | Unclassified — analyse or retire | ☐ | ☐ | ☐ |

### 3.1 Provisional dependency themes (for sequencing)

Refine after formula-level analysis; for planning only:

```text
Inputs (Oil/Gas Input, Master, Fiscal Terms_PIA, Ec_IO)
  → STOIIP / GIIP / Production Profile / Block data / Prod_Summary
  → Block_TC / Block_TC_Gas / Cap_Allow*
  → Royalties / FLGT
  → HT_NCF* / CIT_NCF*
  → Project_NCF* / Equity_NCF* / RESULTS Equity / Analysis / CR Econ
  → Equity Dash (presentation)
```

Hidden sheets may still contain critical calculations — **do not skip** during mapping.

---

## 4. Worksheet Documentation Template

For every worksheet (deep pass):

```text
Worksheet Name
Purpose
Business Function
Dependencies
Dependent Worksheets
Named Ranges
Excel Tables
Hidden Cells / Columns / Rows
Charts
Reports
External References
Implementation Module
Validation Status
```

---

## 5. Formula Groups

**Machine catalogue (authoritative cell-level inventory):**

| Artifact | Location |
|----------|----------|
| Catalogue index | `docs/workbook/catalogue/FORMULA_CELL_CATALOGUE.md` |
| All formulas | `docs/workbook/catalogue/formula_catalogue.csv` (**87,491** rows) |
| All non-empty cells | `docs/workbook/catalogue/cell_catalogue_all_nonempty.csv` (**110,267** rows) |
| Sheet counts | `docs/workbook/catalogue/sheet_summary.csv` |
| No-cache formulas | `docs/workbook/catalogue/ambiguous_formulas_no_cached_value.csv` (**60**) |

Every major formula block for implementation still requires a human-completed group record:

```text
Name / Business meaning
Location (e.g. B15:M240)
Precedents / Dependents
Implemented By (service/function)
Python equivalent reference
Validation status
```

Formula-first, cell-by-cell implementation is mandatory for calculation modules.

**Status:** Cell/formula **inventory extracted** from GM; business “formula groups” and approved semantics **pending** module work.

---

## 6. Named Ranges

Total defined names in file: **230**.

Many names are system/tool related (e.g. `_AtRisk_*`, `__123Graph_*`, `___mds_*`). Business-relevant names must be filtered and mapped to domain fields during deep analysis.

| Excel name | Application object path | Validation |
|------------|-------------------------|------------|
| _TBD business names_ | _TBD_ | Pending |

---

## 7. Excel Tables → Domain

Pending deep scan. Pattern: Excel table → domain collection (e.g. production table → `ProductionProfile`).

---

## 8. Charts

Pending inventory. Each Excel chart → one Chart Template (see CHART_SPECIFICATION), including dual-axis behaviour flags.

---

## 9. Reports

Workbook result/dashboard sheets (RESULTS Equity, Analysis, Equity Dash, CR Econ, NCF sheets) map to Report/Dashboard builders — not reimplemented as live Excel.

---

## 10. Workbook Features to Inventory

Conditional formatting, data validation, merged cells, dynamic arrays, spill ranges, pivot tables, Power Query, macros, named formulas, LAMBDA, dynamic charts, **@Risk simulation settings** (defined names present — Monte Carlo path must account for @Risk heritage carefully).

---

## 11. VBA Replacement

| Macro | Purpose | Replacement Service | Status |
|-------|---------|---------------------|--------|
| TBD | | | Pending scan |

---

## 12. Traceability Chain

```text
Workbook → Worksheet → Formula Group → Python Module → Function
→ Unit Test → Validation Test
```

Every workbook element has exactly one implementation path in PEMS.

---

## 13. Change History

| Workbook Version | Application Change | Validation Result | Approval |
|------------------|--------------------|-------------------|----------|
| Intake-2026-08-01 | File registered; sheet inventory + catalogue/GTC | N/A (docs only) | Development intake |
| Confirmed-2026-08-03 | Active GM hash changed; error confirmation scan | 1× `#NUM!` IRR confirmed; prior #REF!/CR gaps cleared | Error confirmation |

---

## 14. Completion Dashboard

| Area | Implementation % | Validation % | Regression % | Documentation % | Status |
|------|------------------|--------------|--------------|-----------------|--------|
| Sheet inventory | 0 | 0 | 0 | ~40 | 39 sheets listed + counts |
| Formula catalogue | 0 | 0 | 0 | ~85 | **86,973** formulas on active SHA; semantics open |
| Golden Test Cases | 0 | 0 | 0 | ~80 | **ACTIVE** GTC-001; AU14 excluded from numeric golden |
| Named ranges (business) | 0 | 0 | 0 | ~20 | 192 names listed; not business-filtered |
| Charts | 0 | 0 | 0 | 0 | Not started |

---

## 15. Intake Procedure (status)

1. ~~Place approved file under `docs/workbook/`~~ **Done** — `Econ_Model_PEMS.xlsx`  
2. ~~Complete WORKBOOK_MANIFEST.md~~ **Done** (SHA256 + history copy)  
3. ~~Inventory all sheets~~ **Done** (names/visibility + nonempty counts)  
4. ~~Extract formula catalogue~~ **Done** on active SHA D07560CA…  
5. ~~GTC-001~~ **Done** on active SHA (see GOLDEN_TEST_CASES.md)  
6. Semantic formula-group / input classification — **Pending**  
7. ~~PO disposition of `Project_NCF!AU14`~~ **Done** — expected no-sign-change IRR / `#NUM!`  
8. Formal PO approval stamp of GM version — **CLOSED** (SHA `D07560CA…BFEA`, 3 Aug 2026 WAT)  

---

## 16. Final Principle

Nothing in the workbook remains undocumented. Nothing is implemented without traceability back to the workbook.
