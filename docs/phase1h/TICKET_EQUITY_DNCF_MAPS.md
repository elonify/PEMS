# Ticket: Add Equity Annual & Cumulative DNCF Maps

**Status:** Design only — awaiting PO / calc-layer authorization  
**Priority:** High (unblocks Equity CashFlow chart 40)  
**Size:** Medium  
**Layer:** Calculation (likely ``cr_ncf.py`` / ``CrNcfResult``)  
**Related Phase:** Phase 1H

---

## 1. Objective

Add year-keyed equity discounted cash-flow maps so the Equity CashFlow chart can later be implemented as a pure projection.

| Proposed field (illustrative)     | GM location              | Purpose                    |
|-----------------------------------|--------------------------|----------------------------|
| ``equity_dncf_by_year``           | Equity_NCF_Con!AH        | Equity annual DNCF         |
| ``equity_cum_dncf_by_year``       | Equity_NCF_Con!AI        | Equity cumulative DNCF     |

---

## 2. Current state (evidence)

- ``CrNcfResult`` currently only has scalar equity totals:
  - ``equity_ag51`` = host NPV × equity share
  - ``equity_ah51`` = contractor NPV × equity share
- These map to sheet totals (AG51 / AH51), **not** the annual chart series.
- Project-level maps ``disc_contractor_ah`` / ``disc_cncf_ai`` exist but must **not** be scaled in presentation (acquisition timing / equity path may differ).

---

## 3. Workbook requirement (chart40)

From earlier evidence:

- Categories: Equity_NCF_Con!A5:A34
- Series 1: Equity_NCF_Con!AH5:AH34  (Equity DNCF)
- Series 2: Equity_NCF_Con!AI5:AI34  (Equity Cum DNCF)
- Title: “Equity CashFlow with Acquisition Cost”

---

## 4. Implementation notes (for future calc ticket)

1. Extract / confirm the exact GM formulas for Equity_NCF_Con AH and AI columns.
2. Populate year-keyed maps on the authoritative calc result (most likely ``CrNcfResult``).
3. Ensure acquisition cost / equity share timing is respected — do not simply multiply project DNCF by a constant share unless GM proves they are identical.
4. Add Golden Master comparison tests for the new maps.
5. Only after the maps exist and are validated:
   - Authorize the Equity CashFlow row in the audit
   - Implement ``equity_cashflow_dataset`` as pure projection

---

## 5. Explicit Non-Goals

- No presentation builder in this ticket
- No scaling of project ``disc_contractor_ah`` / ``disc_cncf_ai`` in presentation
- No audit authorization until maps are validated
- No UI / plotting work

---

## 6. Authorization Gate

Requires explicit calc-layer / PO authorization before any code is written.

---

*Design prepared from Phase 1H evidence. Ready for authorization decision.*
