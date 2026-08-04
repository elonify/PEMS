# Phase 1A — CaseInput + Ec_IO Implementation Report

**Date:** 2026-08-04  
**Directive:** PHASE 1 CALCULATION IMPLEMENTATION — Phase 1A gate  
**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**GM modified:** **No** (read-only openpyxl `data_only` / SHA verified pre- and post-tests)  
**GTC case:** GTC-001  
**Numerical validation claim:** **NOT CLAIMED** for full Ec_IO sheet or full-system PEMS-vs-GM  

---

## 1. Deliverables

| # | Item | Path / status |
|---|------|----------------|
| 1 | CaseInput typed structure | `src/pems/domain/case_input.py` — **IMPLEMENTED** |
| 2 | Validation (single path) | `src/pems/validation/case_input_validator.py` — **IMPLEMENTED** |
| 3 | Manual input pathway | `src/pems/domain/manual_input.py` — **IMPLEMENTED** |
| 4 | Excel / import pathway | `src/pems/infrastructure/excel_import.py` — **IMPLEMENTED** |
| 5 | Provenance map | `src/pems/domain/provenance.py` — **IMPLEMENTED** |
| 6 | Ec_IO pure calculations | `src/pems/calculations/modules/ec_io.py` — **IMPLEMENTED** (pure CaseInput groups only) |
| 7 | Ec_IO unit tests | `tests/unit/test_ec_io.py` — **PASS** |
| 8 | CaseInput unit tests | `tests/unit/test_case_input.py` — **PASS** |
| 9 | Ec_IO GTC comparison | `tests/validation/test_ec_io_gtc.py` + `src/pems/gtc/compare.py` — **PASS (subset)** |
| 10 | Discrepancy report | This document §5 — **0 mismatches** on Phase 1A cell set |
| 11 | Implementation tracker | `docs/05_PROJECT_CONTROL/IMPLEMENTATION_TRACKER.md` — **UPDATED** |
| 12 | Changelog | `docs/05_PROJECT_CONTROL/CHANGELOG.md` — **UPDATED** |
| 13 | Traceability | `docs/DOCUMENTATION_TRACEABILITY_MATRIX.md` — **UPDATED** |

Manual-entry and import pathways converge on the **same** `CaseInput` type; no dual calculation logic.

---

## 2. CaseInput status

| Attribute | Status |
|-----------|--------|
| Typed parameter structure | **IMPLEMENTED** |
| Manual pathway | **IMPLEMENTED** (`manual_input_from_mapping` → `CaseInput`) |
| Excel / GM import pathway | **IMPLEMENTED** (`import_case_input_from_active_gm`) |
| Shared validation | **IMPLEMENTED** (enums, fractions, years, finiteness) |
| Defaults (documented) | **IMPLEMENTED** where contract specifies (e.g. equity total 1.0 structural) |
| Currency / unit metadata | Via `FieldProvenance.unit` |
| Source sheet/cell traceability | Via `CASE_INPUT_PROVENANCE` |
| Deterministic serialization | `CaseInput.to_serializable()` sorted keys |
| Gate | **IMPLEMENTED** (Phase 1A) — not full multi-scenario GTC expansion |

---

## 3. Ec_IO formula groups implemented (pure CaseInput)

| Group | Formula (spec) | GM cell | Status |
|-------|----------------|---------|--------|
| Price format | IF(escalator=0,"Real","Nominal") | Ec_IO!C13 | **IMPLEMENTED** |
| Equity company 2 | total − company_1 | Equity Dash!C5 | **IMPLEMENTED** |
| Field gas default | G18 | Ec_IO!G19 | **IMPLEMENTED** |
| Cost mode default | G18 | Ec_IO!G23 | **IMPLEMENTED** |
| History end | C5−1 | Ec_IO!E28 | **IMPLEMENTED** |
| Forecast anchor | E28+1 | Ec_IO!D29 | **IMPLEMENTED** |
| Project end | C5+C6 if life known | Ec_IO!E29 | **IMPLEMENTED** (life from import cache / upstream) |

**Pass-through inputs** (imported → cell_map for GTC): Equity C4/C6; Ec_IO C4–C7, C12, C14–C15, C17–C26, D28, D30, G18, G20–G22, G24–G26.

### Deferred (HUB_OUTPUT — not Phase 1A pure gate)

| Item | Reason |
|------|--------|
| Ec_IO KPI hub G3–G15 | Downstream NCF / FLGT |
| Ec_IO cost hub N16–S18 | Cap_Allow |
| Ec_IO revenue hub P16–P18 | FLGT |
| Sensitivity tables | PRESENTATION / DEFERRED scope |

These remain **NOT IMPLEMENTED** by design. Contract classifies them as HUB_OUTPUT.

---

## 4. Tests

| Suite | Result |
|-------|--------|
| Phase 0 scaffold | 6 passed |
| CaseInput unit | 4 passed |
| Ec_IO unit | 6 passed |
| Ec_IO GTC validation | 3 passed |
| **Total** | **19 passed, 0 failed** (pytest 2026-08-04) |

Commands: `python -m pytest tests -v`

---

## 5. GTC-001 comparison (Phase 1A cell subset)

| Metric | Count |
|--------|------:|
| Cells compared | 35 |
| Exact match | **35** |
| Tolerance match (1e-9) | **0** |
| Expected Excel error OK | **0** (none in this subset; AU14 policy still coded in compare) |
| Mismatch | **0** |
| Missing PEMS | **0** |
| Missing expected | **0** |
| Unresolved discrepancy | **0** |

Compared set = all keys in `EcIoResult.cell_map()` that have GTC/GM expected values for GTC-001 (literals + formula caches + data_only text attributes).

### Discrepancy classification

| Class | Count | Notes |
|-------|------:|-------|
| Unexplained mismatch | 0 | — |
| Expected deferred hub | 4 groups | Not compared; not claimed |
| Spec ambiguity | 0 | None stopped implementation |

**Do not interpret 35/35 as full Ec_IO sheet VALIDATED.** Hub KPIs and full-sheet formula inventory are out of scope for Phase 1A.

---

## 6. Numerical validation status

| Claim | Status |
|-------|--------|
| Specification READY (Ec_IO contract) | Yes (pre-existing) |
| CaseInput implementation complete (Phase 1A) | **Yes** |
| Ec_IO pure-group implementation complete | **Yes** |
| GTC subset comparison PASS | **Yes** |
| Ec_IO module **VALIDATED** (full sheet) | **NOT CLAIMED** |
| PEMS-vs-GM **VALIDATED** (system) | **NOT CLAIMED** |

---

## 7. Golden Master protection

| Check | Result |
|-------|--------|
| ACTIVE SHA constant | `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA` |
| On-disk SHA verification | **MATCH** |
| GTC-001 manifest SHA bound | **MATCH** |
| Workbook written / re-saved | **No** |
| openpyxl mode | `read_only=True`, `data_only=True` for import/compare only |

---

## 8. Implementation gate decision (Phase 1A)

| Gate criterion | Met? |
|----------------|:----:|
| Specified pure formula groups implemented | Yes |
| Required CaseInput inputs wired | Yes |
| Dependencies correct for pure path | Yes |
| Units preserved via provenance | Yes |
| Unit + GTC tests pass | Yes |
| GTC executed with classified outcomes | Yes |
| Discrepancies resolved or classified | Yes (0 open) |
| No unsupported invented logic | Yes |
| Hub HUB_OUTPUT deferred (not hidden) | Yes |

**Phase 1A CaseInput + Ec_IO pure path:** **IMPLEMENTED** (gate met for pure subset).  

**Promotion to VALIDATED:** **blocked** until hub consumers exist and full GTC/module comparison is authorized.  

**Production module:** **not started** — do not proceed until this gate is acknowledged.

---

## 9. Next controlled step

1. User acknowledges Phase 1A gate.  
2. Implement **Production** from `PRODUCTION_PROFILE_CONTRACT.md`.  
3. Production unit tests + GTC → gate.  
4. Then Costs → Fiscal interface → FLGT → CR/NCF → RESULTS.  
5. Presentation remains **DEFERRED** until calculation numerical validation.
