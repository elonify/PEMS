# Phase 1H — Chart Presentation  
**Status & Roadmap**  
*(as of commit `8d2c1cc`; implementation stack `0a6d456` + `19b4ca8`)*

## 1. Executive Summary

Phase 1H has delivered a presentation-only chart dataset layer for the five authorized families, with audit authorization (12 rows YES) and pure-projection builders.  

**`PresentationBundle.chart_datasets`** now carries the seven official dataset IDs (five families; oil/gas doubled) via `build_authorized_chart_datasets` (`19b4ca8`). The PySide6 UI still shows **tables only** — plot rendering / dual-axis engine remains deferred.

Further chart families (e.g. Production Profile) are gated on **calculation-layer DTO work**. A design ticket for PP cumulative maps exists (`TICKET_PP_CUMULATIVE_MAPS.md`, `8d2c1cc`) and awaits calc-layer / PO authorization.

**Overall progress: ~8.0 / 10**

## 2. What Is Complete

| Milestone | Status | Notes |
|-----------|--------|-------|
| A. Architecture | Done | Pure DTO projection, isolated package |
| B. Semantic mapping | Done (5 families) | Workbook → DTO mappings established |
| C. Authorization | Done | 12 rows `implementation_authorized=YES` |
| D. Implementation | Done (5 families) | Builders + unit tests (`0a6d456`) |
| F. UI data wiring | **Partial** | Datasets on `PresentationBundle` (`19b4ca8`); no plot page |

**Committed families**
- ECONOMIC_LIMIT
- PRODUCTION_SUMMARY (oil & gas)
- COST_PROFILE (oil & gas)
- FLGT_TAKE (7 series — hcdt_gas / nddc_gas correctly excluded)
- PROJECT_DISCOUNTED_NCF

**Attached dataset IDs (7):**  
`PROJECT_DISCOUNTED_NCF`, `ECONOMIC_LIMIT`, `OIL_PRODUCTION_SUMMARY`, `GAS_PRODUCTION_SUMMARY`, `OIL_COST_PROFILE`, `GAS_COST_PROFILE`, `FLGT_TAKE`.

## 3. Current Architecture Snapshot

```
RunService → RunBundle (DTOs)
                ↓
        build_presentation()
                ↓
        PresentationBundle
           · tables (DisplayRow / TableModel)
           · chart_datasets: dict[str, ChartDataset]  ← authorized five families
                ↓
        PySide6 UI (tables only; plot engine deferred)
```

## 4. Open Gaps (Priority Order)

### 4.1 Calculation-layer DTO gaps (Milestone E)

| Gap | Impact | Size | Status |
|-----|--------|------|--------|
| PP cumulative maps (`pp_cum_by_year`, `pp_ag_cum_by_year`) | Unlocks Production Profile charts 15/16 | Small | **Design ticket ready** (`TICKET_PP_CUMULATIVE_MAPS.md`); GM F/I formulas known; **await calc authorization** |
| Equity year-keyed DNCF maps | Unlocks Equity CashFlow chart 40 | Medium | Gap analyzed; formal ticket optional; **blocked** |

Both remain correctly blocked from presentation builders until maps + audit YES.

### 4.2 UI chart rendering (rest of Milestone F)

Done: attach authorized datasets in presentation.  
Still open:
1. Optional read-only “Charts (data)” page (metadata / series tables)
2. Plot rendering / dual-axis zero-alignment engine (separate gate)

### 4.3 Still deferred / blocked

- STOIIP / GIIP sensitivity (8 charts)
- OML123 scenario
- Prod_Summary chart #1 (column C)
- Full Analysis / Monte Carlo family (15 charts)
- Actual chart **plot** rendering engine

## 5. Recommended Next Sequence

1. **Optional UI (low risk, light authorization)**  
   Read-only Charts (data) page listing `pres.chart_datasets` (no plots).

2. **Calc-layer (when PO authorizes)**  
   Implement `docs/phase1h/TICKET_PP_CUMULATIVE_MAPS.md`  
   → GTC vs F23…/I23… → audit YES for Production Profile rows  
   → then `production_profile_dataset` (presentation projection only).

3. **Later**  
   Equity DNCF maps → Equity CashFlow builder  
   Full chart rendering (dual-axis, zero-alignment, etc.)

## 6. Explicit Non-Claims

- Workbook chart-series parity is **not** claimed
- UI chart **plot** rendering is **not** implemented
- No calculation or discounting was introduced in presentation
- Remaining 28 audit rows stay unauthorized
- PP cumulative maps are **not** implemented (design only)

## 7. Key Commits

| Commit   | Content |
|----------|---------|
| 0a6d456  | Five ChartDataset builders + audit authorization |
| e07c9d7  | Canonical handoff (post-0a6d456) |
| 2cd09a3  | Status & Roadmap (initial) |
| b7a05ee  | Product scope → `docs/pems/PEMS_PRODUCT_SCOPE.md` |
| 19b4ca8  | Attach authorized ChartDatasets to PresentationBundle |
| 8d2c1cc  | Design ticket for PP cumulative maps (calc layer) |

## 8. Tests

```text
pytest tests/unit/test_chart_datasets.py tests/unit/test_presentation.py -q
50 passed, 1 pre-existing @pytest.mark.slow warning
```

---

*Document refreshed to HEAD `8d2c1cc` as part of Phase 1H controlled progression.*  
*Architectural rule remains in force: presentation projects; it does not calculate.*
