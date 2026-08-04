# Phase 1E — CR/NCF Implementation Report

**Date:** 2026-08-04  
**Authority:** `CR_NCF_PARAMETER_CONTRACT.md` · `CR_NCF_CONTRACT.md` · `PHASE1E_CR_NCF_READINESS.md`  
**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**GM modified:** **No**  
**GTC case:** GTC-001  
**Formal gate acknowledgement:** **PASSED / ACKNOWLEDGED** — see `PHASE1E_GATE_ACKNOWLEDGEMENT.md`  

---

## Explicit status block (authoritative)

| Status | Value |
|--------|--------|
| **CR/NCF SPECIFICATION READY** | **YES** |
| **CR/NCF IMPLEMENTED** | **YES**, subject to the documented full-regression limitation below |
| **CR/NCF TARGETED TESTS** | **PASS** (10/10) |
| **CR/NCF GTC SUBSET** | **PASS** (13 anchors; 0 mismatches) |
| **FULL REGRESSION** | **NOT CLOSED / INTERRUPTED** (~90%; repeated GM openpyxl I/O; force-stopped; not a PASS) |
| **CR/NCF NUMERICALLY VALIDATED** | **NOT CLAIMED** |
| **PEMS-vs-GM FULL-SYSTEM VALIDATION** | **NOT CLAIMED** |
| **RESULTS** | **NOT STARTED** (`ResultsModule` remains `UnimplementedModule`) |
| **GOLDEN MASTER MODIFIED** | **NO** |

---

## 1. Implementation scope

| Item | Status |
|------|--------|
| CR Econ bridge (CR-G1…CR-G4) | Implemented from FLGT + Costs + LAW CRL/profit oil |
| Project NCF AE/AF/AG/AH/AI/AJ | Computed from GM formulas + imported tax/allowable intermediates |
| IRR AG58 / AU12 | Implemented (`numpy_financial` / Newton fallback) |
| AU14 no-valid IRR | `NO_VALID_IRR` ↔ GTC `#NUM!` |
| Equity NCF × C4 | Implemented |
| HT/CIT full cell engines | **Partial** — annual intermediates imported (catalogue path); not line-by-line HT/CIT rewrite |
| RESULTS | **Not implemented** |

Code: `src/pems/calculations/modules/cr_ncf.py`  
Import support: `src/pems/infrastructure/excel_import.py` (Project_NCF intermediates, law, Equity L-by-year)

---

## 2. Source specifications

- `docs/02_SPECIFICATIONS/modules/CR_NCF_PARAMETER_CONTRACT.md`
- `docs/02_SPECIFICATIONS/modules/CR_NCF_CONTRACT.md`
- `docs/03_IMPLEMENTATION/PHASE1E_CR_NCF_READINESS.md`

---

## 3–10. Groups, inputs, dependencies, metrics

See readiness report and parameter contract. Summary dependency:

```text
CaseInput → Production → Costs → FLGT → CrNcfModule → (RESULTS later)
```

Fiscal Terms_PIA remains LAW TABLE (consume only). Equity Dash C4 remains INPUT; C5 derived.

---

## 11. GTC comparison results

| Metric | Count |
|--------|------:|
| Comparison points | **13** |
| Exact matches | **0** |
| Tolerance matches (1e-9) | **12** |
| Expected-error matches (AU14) | **1** |
| Mismatches | **0** |
| Unresolved discrepancies | **0** |

Anchors: Project_NCF AG51, AH51, AJ51, AE51, AF51, AB51, AC51, AD51, AG58, AU12, AU14; Equity_NCF_Con AG51, AH51.

Expected values from contract/GTC-001 — **not rewritten**.

---

## 12. Targeted test results

| Suite | Result |
|-------|--------|
| `tests/unit/test_cr_ncf.py` | **7 passed** |
| `tests/validation/test_cr_ncf_gtc.py` | **3 passed** |
| **Combined CR/NCF** | **10 passed / 0 failed** |

Runtime is elevated because each GTC path opens the active GM read-only via openpyxl (not because of workbook mutation).

---

## 13. Full-suite regression status

| Item | Status |
|------|--------|
| Command | `python -m pytest tests -q` |
| Outcome | **INTERRUPTED** at approximately **90%** progress |
| Reason | Excessive wall-clock from **repeated full Golden Master loads** across many validation tests |
| Evidence of progress | Log advanced to `[90%]` with active CPU before controlled force-stop |
| Converted to PASS? | **No** |
| Used as gate evidence? | **No** |
| Re-run in this completion directive? | **No** (explicitly not instructed) |

---

## 14. Deferred items

- Full HT/CIT line-by-line engines (intermediates path for GTC)
- Hidden NCF sheets as primary surfaces
- RESULTS implementation
- Presentation / sensitivity / Monte Carlo
- Full-suite regression closure (optional offline later)

---

## 15–16. Integrity and validation claims

| Check | Result |
|-------|--------|
| Active GM SHA | `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA` |
| SHA verification | **MATCH** |
| GM file write/save | **None** |
| GM LastWriteTime | 2026-08-03 (unchanged relative to freeze) |

**Permitted claims:** SPEC READY; IMPLEMENTED (with regression limitation); targeted tests PASS; GTC subset PASS.  
**Prohibited claims:** NUMERICALLY VALIDATED; full-system VALIDATED; full regression PASS; RESULTS done.

---

## 17. Final gate status

**Phase 1E CR/NCF implementation work = complete within authorized scope.**  
**Formal Project Owner gate acknowledgement = PASSED / ACKNOWLEDGED** (`PHASE1E_GATE_ACKNOWLEDGEMENT.md`).

### Sequence

```text
CaseInput ✓ → Ec_IO ✓ → Production ✓ → Costs ✓ → FLGT ✓ → CR/NCF ✓ (1E PASSED) → STOP
```

**Do not auto-start RESULTS.** Next: **PHASE 1F — RESULTS** (separate authorization).
