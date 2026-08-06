# Phase 1H — Chart Presentation  
**Status & Roadmap**  
*(as of commit e07c9d7 / 0a6d456)*

## 1. Executive Summary

Phase 1H has successfully delivered a presentation-only chart dataset layer for the five authorized families.  
The architectural boundary (no calculation in presentation) has been preserved.  
Further chart progress is now gated by calculation-layer DTO gaps and a separate UI charting authorization.

**Overall progress: ~7.5 / 10**

## 2. What Is Complete

| Milestone | Status | Notes |
|-----------|--------|-------|
| A. Architecture | Done | Pure DTO projection, isolated package |
| B. Semantic mapping | Done (5 families) | Workbook → DTO mappings established |
| C. Authorization | Done | 12 rows `implementation_authorized=YES` |
| D. Implementation | Done (5 families) | Builders + 49 unit tests committed |

**Committed families**
- ECONOMIC_LIMIT
- PRODUCTION_SUMMARY (oil & gas)
- COST_PROFILE (oil & gas)
- FLGT_TAKE (7 series — hcdt_gas / nddc_gas correctly excluded)
- PROJECT_DISCOUNTED_NCF

## 3. Current Architecture Snapshot

```
RunService → RunBundle (DTOs)
                ↓
        build_presentation()
                ↓
        PresentationBundle  ←  (ChartDatasets not yet attached)
                ↓
        PySide6 UI (tables only)
```

Chart builders exist and are tested but are not yet called by the presentation or UI layers.

## 4. Open Gaps (Priority Order)

### 4.1 Calculation-layer DTO gaps (Milestone E)

| Gap | Impact | Size | Prerequisite |
|-----|--------|------|--------------|
| PP cumulative maps (`pp_cum_by_year`, `pp_ag_cum_by_year`) | Unlocks Production Profile charts 15/16 | Small | PO calc authorization + GTC |
| Equity year-keyed DNCF maps | Unlocks Equity CashFlow chart 40 | Medium | PO calc authorization + GM formula confirmation |

Both remain correctly blocked from presentation work.

### 4.2 UI chart wiring (Milestone F)

Smallest safe next step:
1. Attach the five authorized `ChartDataset`s inside `build_presentation`
2. Expose a read-only “Charts (data)” page or section showing dataset metadata + series
3. Keep actual plot rendering / dual-axis engine under a separate later gate

### 4.3 Still deferred / blocked

- STOIIP / GIIP sensitivity (8 charts)
- OML123 scenario
- Prod_Summary chart #1 (column C)
- Full Analysis / Monte Carlo family (15 charts)
- Actual chart rendering engine

## 5. Recommended Next Sequence

1. **Immediate (low risk)**  
   Wire the five existing datasets into `PresentationBundle` + simple data view in UI  
   (requires light UI authorization)

2. **Calc-layer ticket (when authorized)**  
   Add `pp_cum_by_year` / `pp_ag_cum_by_year` to `ProductionResult`  
   (formulas now known: running sum of annual with zero-annual gate)

3. **Later**  
   Equity DNCF maps → Equity CashFlow builder  
   Full chart rendering (dual-axis, zero-alignment, etc.)

## 6. Explicit Non-Claims

- Workbook chart-series parity is **not** claimed
- UI chart rendering is **not** implemented
- No calculation or discounting was introduced in presentation
- Remaining 28 audit rows stay unauthorized

## 7. Key Commits

| Commit   | Content                                      |
|----------|----------------------------------------------|
| 0a6d456  | Five ChartDataset builders + audit authorization |
| e07c9d7  | Canonical handoff update                     |

---

*Document generated as part of Phase 1H controlled progression.*  
*Architectural rule remains in force: presentation projects; it does not calculate.*
