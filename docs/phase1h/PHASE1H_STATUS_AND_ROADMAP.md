# Phase 1H — Chart Presentation  
**Status & Roadmap**  
*(as of HEAD `6c2b41d`)*

## 1. Executive Summary

Phase 1H has delivered presentation-only chart datasets for **six** authorized families, with audit authorization (**14** rows YES).  

Calc-layer **PP cumulative maps** are implemented (`pp_cum_by_year` / `pp_ag_cum_by_year`). **Production Profile** builders and audit authorization are complete. **`PresentationBundle.chart_datasets`** carries **9** dataset IDs (including oil/gas production profile).  

**Equity CashFlow** is fully diagnosed (GM AH/AI formulas; Medium ticket). Equity **calc implementation** is still blocked. Plot rendering remains deferred.

**Overall progress: ~8.5–8.7 / 10**

## 2. What Is Complete

| Milestone | Status | Notes |
|-----------|--------|-------|
| A. Architecture | Done | Pure DTO projection |
| B. Semantic mapping | Done (6 families) | Incl. Production Profile |
| C. Authorization | Done | **14** rows YES |
| D. Implementation | Done (6 families) | Incl. `production_profile_dataset` |
| E. Model/DTO (PP) | Done | `dc361e3` PP cum maps |
| F. UI data wiring | **Partial** | Datasets on bundle; **no plot UI** |

**Implemented families**
- ECONOMIC_LIMIT  
- PRODUCTION_SUMMARY (oil & gas)  
- COST_PROFILE (oil & gas)  
- FLGT_TAKE (7 series)  
- PROJECT_DISCOUNTED_NCF  
- **PRODUCTION_PROFILE (oil & AG)**  

**Attached dataset IDs (9):**  
`PROJECT_DISCOUNTED_NCF`, `ECONOMIC_LIMIT`,  
`OIL_PRODUCTION_SUMMARY`, `GAS_PRODUCTION_SUMMARY`,  
`OIL_PRODUCTION_PROFILE`, `GAS_PRODUCTION_PROFILE`,  
`OIL_COST_PROFILE`, `GAS_COST_PROFILE`, `FLGT_TAKE`.

## 3. Current Architecture Snapshot

```
RunService → RunBundle (DTOs, incl. pp_cum_by_year / pp_ag_cum_by_year)
                ↓
        build_presentation()
                ↓
        PresentationBundle
           · tables
           · chart_datasets (9 authorized IDs)
                ↓
        PySide6 UI (tables only; plot engine deferred)
```

## 4. Open Gaps (Priority Order)

### 4.1 Equity DNCF maps (Milestone E remainder)

| Gap | Impact | Size | Status |
|-----|--------|------|--------|
| Equity annual/cum DNCF (`equity_dncf_by_year`, `equity_cum_dncf_by_year`) | Chart 40 Equity CashFlow | **Medium** | **Design + GM formulas ready** (`TICKET_EQUITY_DNCF_MAPS.md`). Not project×share. Needs equity AF stack. **Await calc authorization.** |

### 4.2 UI chart rendering (rest of Milestone F)

- Optional Charts (data) page  
- Plot / dual-axis zero-alignment engine (separate gate)

### 4.3 Still deferred / blocked

- Equity CashFlow builder (until equity maps land)  
- STOIIP / GIIP, OML123, Prod_Summary #1  
- Analysis / Monte Carlo (15 charts)  
- Plot rendering engine  

## 5. Recommended Next Sequence

1. **Equity calc (when PO authorizes)**  
   Implement `docs/phase1h/TICKET_EQUITY_DNCF_MAPS.md`  
   → GTC vs AH/AI → audit YES → `equity_cashflow_dataset`.

2. **Optional UI**  
   Read-only Charts (data) page for `pres.chart_datasets`.

3. **Later**  
   Full plot rendering (dual-axis, etc.) · remaining deferred charts only with DTOs + audit YES.

## 6. Explicit Non-Claims

- Workbook chart-series parity is **not** claimed  
- UI **plot** rendering is **not** implemented  
- Presentation does not recompute economics  
- **26** audit rows remain unauthorized  
- Equity maps are **not** implemented (design only)

## 7. Key Commits

| Commit | Content |
|--------|---------|
| 0a6d456 | Five ChartDataset builders + audit YES (12) |
| 19b4ca8 | Attach ChartDatasets to PresentationBundle |
| dc361e3 | PP cumulative maps on ProductionResult |
| 09a2ded | Audit YES Production Profile (14 total) |
| 8518056 | `production_profile_dataset` oil & gas |
| 2a14d76 / 6c2b41d | Equity DNCF design ticket (+ GM formulas) |

## 8. Tests

```text
pytest tests/unit/test_chart_datasets.py tests/unit/test_presentation.py -q
59 passed, 1 pre-existing @pytest.mark.slow warning
```

---

*Document refreshed to HEAD `6c2b41d`.*  
*Architectural rule: presentation projects; it does not calculate.*
