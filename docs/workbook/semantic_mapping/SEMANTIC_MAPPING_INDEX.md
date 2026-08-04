# SEMANTIC MAPPING INDEX

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Phase:** Semantic Mapping (controlled)  
**Golden Master:** `docs/workbook/Econ_Model_PEMS.xlsx`  
**Active SHA256:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Historical intake SHA:** `F6A1992F…3006` — catalogue/GTC archived under `*/historical_intake_F6A1992F/`  
**Baselines:** **ACTIVE** catalogue + **ACTIVE** GTC-001 (re-extracted) + WORKBOOK_ERROR_STATUS  
**Claims:** Formula-level implementation fidelity **UNCLAIMED**. Parity **UNCLAIMED**.

### Scope (authoritative: SCOPE_VISIBLE_SHEETS_ONLY.md + SCOPE_DECISIONS.md)

| Rule | Status |
|------|--------|
| Ignore **all hidden sheets** for input/literal classification & readiness | **CLOSED** |
| Ignore literals on hidden sheets | **CLOSED** |
| Do not modify hidden sheets / GM | **Mandatory** |
| Visible-sheet literals in scope | **~3,827** |
| **Equity Dash Share** | **CLOSED — INPUT** (`EQUITY_DASH_SHARE_INPUT.md`) |
| **Fiscal Terms_PIA** | **CLOSED — LAW TABLE** (`FISCAL_TERMS_PIA_LAW_TABLE.md`) |

### Error / condition status (authoritative: WORKBOOK_ERROR_STATUS.md)

| Item | Status |
|------|--------|
| `Project_NCF!AU14` `#NUM!` | **EXPECTED / ACCEPTED IRR NO-SIGN-CHANGE** (AK blank; not a defect) |
| START `#REF!` | **CLOSED** |
| CR Econ empty caches | **CLOSED** |
| Analysis 18 data tables | **Not errors** — see ANALYSIS_DATA_TABLES.md |
| Open genuine defects | **None** |

---

## 1. Purpose

Map workbook evidence to PEMS domains **without** inventing business rules, alternate GTCs, or literal classifications lacking evidence.

---

## 2. Artifact inventory

| Artifact | Role |
|----------|------|
| `SEMANTIC_MAPPING_INDEX.md` | This index |
| `DEPENDENCY_GRAPH.md` | Cross-sheet graph (evidence-based, not fully proven) |
| `SCOPE_VISIBLE_SHEETS_ONLY.md` | **Ignore hidden sheets** for classification/readiness |
| `LITERAL_CLASSIFICATION_POLICY.md` | Classification rules (visible only) |
| `LITERAL_CLASSIFICATION_REGISTER.csv` | May be historical full extract — apply visible-only filter |
| `WORKBOOK_ERROR_STATUS.md` | **Authoritative error status** |
| `WORKBOOK_ERROR_STATUS.json` / `WORKBOOK_ERROR_INVENTORY.csv` | Machine + inventory |
| `PROJECT_NCF_AU14_INVESTIGATION.md` | AU14 evidence pack |
| `ANALYSIS_DATA_TABLES.md` | 18 Analysis data-table constructs |
| `CR_ECON_ANALYSIS.md` | CR Econ (empty-cache issue CLOSED on active) |
| `CROSS_SHEET_DEPENDENCY_EDGES.csv` | **212** directed sheet-edge types |
| `SHEET_UPSTREAM_SUMMARY.csv` | Per-sheet upstream list |
| `NAMED_RANGE_USAGE_TOP100.csv` | Substring usage of defined names |
| `CHART_INVENTORY.csv` | **41** charts (openpyxl) |
| `CHARTS_AND_VBA.md` | Chart/VBA findings |
| `SEMANTIC_PHASE_SUMMARY.json` | Machine summary |
| `modules/M01_Input_Control.md` … `M09_…` | Domain maps |
| `modules/M99_Unclassified.md` | YTD Budget, Sheet1, END |
| `DECISIONS_REQUIRED.md` | PO/domain decisions |
| `READINESS_MATRIX.md` | Ready vs not ready |
| `_build_semantic_phase.py` | Reproducible analysis (read-only) |

---

## 3. Calculation dependency chain (planning order)

Evidence-based order for **mapping** (not an implementation claim of completeness):

```text
M01 Input / Control (Ec_IO, Equity Dash, Oil/Gas Input, Master, START)
  + M02 Fiscal Terms_PIA
  → M03 Reservoir (STOIIP, GIIP)
  → M04 Production (Production Profile, Block_Oil/Gas, OML123, Prod_Summary)
  → M05 Cost / Cap Allow (Block_TC*, Cap_Allow*)
  → M06 Royalty / FLGT (Royalties → FLGT)
  → M07 Tax NCF / Cashflow (HT_*, CIT_*, Project_NCF_*, Equity_NCF_*, CR Econ)
  → M08 Results Economics (RESULTS Equity, Equity Dash, CR Econ KPIs)
  → M09 Sensitivity (Analysis)
```

Cross-links (Equity Dash scales many NCF equity sheets) create **bidirectional coupling** — full topological order is **not proven**.

---

## 4. Module readiness at a glance

| Module | Semantic map | Ready for implementation? |
|--------|--------------|---------------------------|
| M01 Input / Control | Partial | **No** |
| M02 Fiscal Terms | Partial | **No** |
| M03 Reservoir | Partial | **No** |
| M04 Production | Partial | **No** |
| M05 Cost / Cap Allow | Partial | **No** |
| M06 Royalty / FLGT | Partial | **No** |
| M07 Tax NCF / Cashflow | Partial | **No** |
| M08 Results Economics | Partial (best KPI labels) | **No** |
| M09 Sensitivity | Partial | **No** |
| M99 Unclassified | Inventory only | **No** |

**None** meet the bar: inputs, outputs, formulas, dependencies, units, and validation expectations all **sufficiently understood**.

---

## 5. Related control docs

- `docs/05_PROJECT_CONTROL/GOLDEN_MASTER_INTAKE_AND_RECONCILIATION_UPDATE.md`  
- `docs/workbook/catalogue/FORMULA_CELL_CATALOGUE.md`  
- `docs/workbook/Validation_Datasets/GOLDEN_TEST_CASES.md`  
