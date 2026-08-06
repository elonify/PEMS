# Ticket: Add PP Cumulative Maps to ProductionResult

**Status:** Design only — awaiting PO / calc-layer authorization  
**Priority:** High (unblocks Production Profile charts 15 & 16)  
**Size:** Small  
**Layer:** Calculation (`src/pems/calculations/modules/production.py`)  
**Related Phase:** Phase 1H (presentation remains blocked until this lands + audit authorization)

---

## 1. Objective

Add two year-keyed cumulative maps to ``ProductionResult`` so that the Production Profile charts can be implemented later as pure projections.

| Proposed field              | GM column / named range      | Purpose                          |
|-----------------------------|------------------------------|----------------------------------|
| ``pp_cum_by_year``          | Chart_Cum → F23…             | Oil / primary stream cumulative  |
| ``pp_ag_cum_by_year``       | AG_Chart_Cum → I23…          | Associated-gas cumulative        |

---

## 2. Authoritative Formulas (already extracted)

From ``formula_cached_results_all.csv`` (GM SHA D07560CA…):

**F (Chart_Cum)**  
```
F23 = IF(E23=0, 0, SUM(E$23:E23))
Fn  = IF(En=0, 0, SUM(E$23:En))
```

**I (AG_Chart_Cum)**  
```
I23 = IF(H23=0, 0, SUM(H$23:H23))
In  = IF(Hn=0, 0, SUM(H$23:Hn))
```

Zero-annual gate: when the annual value for that year is 0, the displayed cumulative is forced to 0.  
Later non-zero years still sum the full history (including intermediate zeros).

---

## 3. Implementation Notes (for the future calc ticket)

1. Populate **only** on the analytical PP path (same years as ``pp_rate_by_year`` / ``pp_annual_by_year``).
2. After the annual maps (E and H) are built, compute the cumulative maps in spine order.
3. Match the zero-annual display gate exactly.
4. Do **not** reuse ``oil_cum_series`` / ``gas_cum_series`` (different spine + different annual method).
5. GIIP mode: AG maps are already zeroed → ``pp_ag_cum_by_year`` will correctly be zero.
6. Block-path cases that leave PP maps empty should leave the new cumulative maps empty as well.

---

## 4. Suggested DTO addition (illustrative)

```python
@dataclass(frozen=True)
class ProductionResult:
    # ... existing fields ...
    pp_cum_by_year: dict[int, float] = field(default_factory=dict)
    pp_ag_cum_by_year: dict[int, float] = field(default_factory=dict)
```

---

## 5. Validation Requirements

- Golden Master comparison against cached F23… and I23… values
- Unit tests for the zero-annual gate behaviour
- Empty-map behaviour when analytical PP path did not run

---

## 6. Authorization Gate

This ticket requires **explicit calc-layer / PO authorization** before any code is written.

After the maps exist and are validated:

1. Update ``CHART_MAPPING_AUDIT.csv`` → set Production Profile rows to ``implementation_authorized=YES``
2. Only then implement ``production_profile_dataset`` in the presentation layer (pure projection)

---

## 7. Explicit Non-Goals

- No presentation builder in this ticket
- No changes to Prod_Summary cumulatives
- No assumption that Chart_Cum ≡ oil_cum_series
- No UI or plotting work

---

*Design prepared from Phase 1H evidence chain. Ready for authorization decision.*
