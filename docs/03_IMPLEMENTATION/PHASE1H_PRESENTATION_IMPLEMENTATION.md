# Phase 1H — Presentation First-Slice Implementation Report

**Date:** 2026-08-04  
**Authorization:** Project Owner — Phase 1H presentation first-slice implementation  
**Controlling readiness:** `PHASE1H_PRESENTATION_READINESS.md`  
**Git commit under this task:** **None** (await checkpoint authorization)

**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**GM modified:** **No**

---

## A. Implementation claim

| Claim | Status |
|-------|--------|
| **PRESENTATION SPECIFICATION READY** | **YES** |
| **PRESENTATION FIRST SLICE IMPLEMENTED** | **YES** |
| **PRESENTATION NUMERICALLY VALIDATED** | **NOT CLAIMED** |
| **FULL WORKBOOK PRESENTATION PARITY** | **NOT CLAIMED** |
| **CHART PARITY** | **NOT CLAIMED** |
| Charts / Sensitivity / Monte Carlo | **NOT IMPLEMENTED** (deferred) |

---

## B. Architecture implemented

```text
UI (PySide6 MainWindow)
  → RunService (application)
    → Ec_IO / Production / Costs / FLGT / CR-NCF / Results modules
  → build_presentation(RunBundle)  # format + project only
  → widgets (tables / banners)
```

- **No** economic re-calculation in `pems.presentation` or `pems.ui`.  
- **No** live Excel calc host.  
- Static tests enforce no `pems.calculations` imports from presentation/ui.

---

## C. UI surfaces implemented

| Nav | Content |
|-----|---------|
| Home / RESULTS | Executive KPI table from ResultsResult |
| Case | CaseInput drivers + Equity C4 |
| Law | Read-only fiscal_law extras snapshot |
| Production | Summary + sample annual years |
| Costs | Cap_Allow / Ec_IO hub scalars |
| Fiscal | FLGT totals |
| Cash Flow | Project NCF scalars + sample AF + AU14 state |
| Results | Same RESULTS KPI set |
| Validation | CaseInput validation list + GTC claim note |
| Reports | Dataset labels only (export deferred) |

Toolbar: **Load GM case & Run** (read-only GM import via existing importer).

---

## D. IRR failure / alternative KPI

| Rule | Implementation |
|------|----------------|
| Primary IRR unavailable | Display **UNAVAILABLE** (never 0%) |
| Alternative | **GRR** from ResultsResult K11 (BIT) / N11 (AIT) — authoritative RESULTS contract |
| MIRR | **Not on RESULTS Equity** — deferred row; **not invented** |
| Trace | IRR source cells K8/N8; GRR K11/N11 recorded on DisplayRow |

---

## E. Files created / modified

### Created

| File | Role |
|------|------|
| `src/pems/application/run_service.py` | Run orchestration |
| `src/pems/presentation/formats.py` | Display formatters |
| `src/pems/presentation/view_models.py` | PresentationBundle / IRR→GRR |
| `src/pems/ui/main_window.py` | Shell + navigation |
| `src/pems/ui/widgets.py` | Tables / banners |
| `tests/unit/test_presentation.py` | PT01–PT10 style tests |
| `docs/03_IMPLEMENTATION/PHASE1H_PRESENTATION_IMPLEMENTATION.md` | This report |

### Modified

| File | Role |
|------|------|
| `src/pems/presentation/__init__.py` | Export first-slice API |
| `src/pems/ui/__init__.py` | Export MainWindow |
| `src/pems/__main__.py` | `--ui` / `--run-gm` |

Control docs (tracker/changelog/traceability) updated for first-slice IMPLEMENTED.

---

## F. Tests

| Suite | Result | Runtime |
|-------|--------|---------|
| `tests/unit/test_presentation.py` (excl. optional GM) | **12 passed** | ~0.13 s |
| Unit RESULTS + phase0 + presentation | Targeted pass | — |
| Optional GM integration (`--run-gm` / slow mark) | Manual/optional | ~GM import cost |

### Coverage map

| ID | Topic | Covered |
|----|-------|---------|
| PT01 | Identity | yes |
| PT02 | Formatting | yes |
| PT03 | Case controls | yes |
| PT04 | IRR unavailable + GRR | yes |
| PT05 | Series tables | yes |
| PT06 | Source trace | yes |
| PT07 | Deferred banners | yes |
| PT08 | No calc in presentation/UI | yes (AST + source scan) |
| PT09 | Numeric IRR format | yes |
| PT10 | DTO identity for NPV | yes |

---

## G. Golden Master integrity

| Check | Result |
|-------|--------|
| Expected SHA | `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA` |
| Before | MATCH |
| After | MATCH |
| Modified | **NO** |

---

## H. Deferred items

- 41 charts / dual-axis chart engine  
- Analysis / sensitivity UI  
- Monte Carlo  
- MIRR (no RESULTS mapping)  
- PDF/Word report export  
- Full Excel pixel parity  
- Full-system presentation validation claim  

---

## I. How to launch

```text
python -m pems --ui
python -m pems --run-gm
```

---

## J. STOP

No chart implementation. No sensitivity/MC. No calc engine changes beyond orchestration.  
No automatic commit/push.
