# Ticket: Add Equity Annual & Cumulative DNCF Maps

**Status:** Design only — awaiting PO / calc-layer authorization  
**Priority:** High (unlocks Equity CashFlow chart 40)  
**Size:** Medium  
**Layer:** Calculation (likely `cr_ncf.py` / `CrNcfResult`)  
**Related Phase:** Phase 1H  
**GM formulas source:** `docs/workbook/Validation_Datasets/expected_outputs/formula_cached_results_all.csv` (SHA D07560CA…, Confirmed-2026-08-03)

---

## 1. Objective

Add year-keyed equity discounted cash-flow maps so the Equity CashFlow chart can later be implemented as a pure projection.

| Proposed field (illustrative) | GM location | Purpose |
|-------------------------------|-------------|---------|
| `equity_dncf_by_year` | Equity_NCF_Con!AH | Equity annual DNCF |
| `equity_cum_dncf_by_year` | Equity_NCF_Con!AI | Equity cumulative DNCF |

---

## 2. Current state (evidence)

- `CrNcfResult` currently only has scalar equity totals:
  - `equity_ag51` = host NPV × equity share
  - `equity_ah51` = contractor NPV × equity share
- These map to sheet totals (AG51 / AH51), **not** the annual chart series.
- Project-level maps `disc_contractor_ah` / `disc_cncf_ai` exist but must **not** be scaled in presentation.

---

## 3. Workbook requirement (chart40)

- Categories: Equity_NCF_Con!A5:A34  
- Series 1: Equity_NCF_Con!AH5:AH34 (Equity DNCF)  
- Series 2: Equity_NCF_Con!AI5:AI34 (Equity Cum DNCF)  
- Title: “Equity CashFlow with Acquisition Cost”

---

## 4. Authoritative GM formulas (extracted)

### 4.1 AH — Equity annual DNCF

```text
AH5 = AF5/(1+Ec_IO!$C$15*(100%+Analysis!$N$14))^(A5-Ec_IO!$C$5)
AH6 = AF6/(1+Ec_IO!$C$15*(100%+Analysis!$N$14))^(A6-Ec_IO!$C$5)
AHn = AFn/(1+Ec_IO!$C$15*(100%+Analysis!$N$14))^(An-Ec_IO!$C$5)
```

Discount factor form matches project discounting (hurdle × (1+N14), base Ec_IO!C5), applied to **equity undisc contractor NCF (AF)** — not to project AF.

### 4.2 AI — Equity cumulative DNCF

```text
AI5 = SUM(AH$5:$AH5)*(A5<Ec_IO!$D$22)
AI6 = SUM(AH$5:$AH6)*(A6<Ec_IO!$D$22)
AIn = SUM(AH$5:$AHn)*(An<Ec_IO!$D$22)
```

### 4.3 Upstream AF (equity undisc contractor NCF) — required for AH

```text
AF5 = (B5-AE5-W5-X5-E5-J5
       -(FLGT!AO5+FLGT!AP5-FLGT!AN5)*'Equity Dash'!$C$4
       -'Equity Dash'!I1)
      *(A5<=Ec_IO!$D$22)
```

### 4.4 Total (KPI seed, not chart series)

```text
AH51 = SUM(AH5:AH49)   → RESULTS Equity!N7 (contractor AIT NPV)
```

---

## 5. Critical findings

| Finding | Detail |
|---------|--------|
| **AI gate** | Year gate **`An < Ec_IO!D22`** (strict **&lt;**). **Not** a zero-annual display gate (unlike PP Chart_Cum F). |
| **Not project × share** | Equity path is **not** `disc_contractor_ah × equity_share`. AH discounts **equity AF**. |
| **AF embeds share + acquisition** | Equity share `Equity Dash!$C$4` scales FLGT AN/AO/AP inside AF; acquisition `Equity Dash!I1` is subtracted in AF. |
| **Medium size justification** | AH/AI formulas themselves are small once AF exists; building year-keyed **equity AF** (and its CIT/FLGT/host stack) is non-trivial if those equity intermediates are not already on DTOs. |
| **Zero intermediate AH** | Still included in AI running SUM (no IF(AH=0,0,…) on AI). After D22 gate fails, AI = 0. |

---

## 6. Implementation notes (for future calc ticket)

1. Produce year-keyed **equity undisc contractor NCF (AF)** GM-faithfully (share + acquisition + equity CIT/FLGT inputs as required).
2. `equity_dncf_by_year[y] = AF[y] / DF(y)` with the AH discount formula above.
3. `equity_cum_dncf_by_year[y] = SUM(AH first..y) if year < D22 else 0`.
4. GTC / unit tests vs cached AH5…, AI5…, AH51.
5. Only after maps are validated:
   - Authorize Equity_NCF_Con chart row in `CHART_MAPPING_AUDIT.csv`
   - Implement `equity_cashflow_dataset` as pure projection

---

## 7. Explicit Non-Goals

- No presentation builder in this ticket  
- No scaling of project `disc_contractor_ah` / `disc_cncf_ai` in presentation  
- No audit authorization until maps are validated  
- No UI / plotting work  

---

## 8. Authorization Gate

Requires explicit calc-layer / PO authorization before any code is written.

---

*Design prepared from Phase 1H evidence. GM AH/AI formulas extracted and recorded. Ready for authorization decision.*
