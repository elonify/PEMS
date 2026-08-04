# Phase 1C — Costs Implementation Report

**Date:** 2026-08-04  
**Gate plan:** `docs/03_IMPLEMENTATION/PHASE1C_COSTS_IMPLEMENTATION_GATE.md`  
**Authority:** `docs/02_SPECIFICATIONS/modules/COSTS_PARAMETER_CONTRACT.md`  
**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**GM modified:** **No**  
**GTC case:** GTC-001  

---

## 1. Implementation status

| Claim | Value |
|-------|--------|
| Costs **IMPLEMENTED** | **YES** (G1–G8 Phase 1C scope) |
| Costs GTC subset | **PASS** (mandatory anchors) |
| Costs **NUMERICALLY VALIDATED** | **NOT CLAIMED** |
| PEMS-vs-GM FULL-SYSTEM VALIDATION | **NOT CLAIMED** |
| Ec_IO FULL VALIDATION | **NOT CLAIMED** |

---

## 2. G1–G8 status

| Group | Status | Notes |
|-------|--------|-------|
| G1 TC schedule | **IMPLEMENTED** | Selected Cap_Allow path import (FF–FI oil/gas); multi-field GUI deferred |
| G2 Field selection | **IMPLEMENTED** | Via CaseInput `cost_mode_field` / G18–G19 + import of selected consolidated series |
| G3 Undiscounted aggregation | **IMPLEMENTED** | FN/FO/FP/FQ formulas; FI48/FP48/FQ48 totals |
| G4 Discounting | **IMPLEMENTED** | FK/FL with Ec_IO C15; base = first FE year |
| G5 CA rates | **IMPLEMENTED** | FR5:FR9 surface (0.2×4, 0.19); law-aligned, not second Fiscal Terms host |
| G6 Ec_IO cost hub | **IMPLEMENTED** | N16:S18 = oil+gas Cap_Allow totals |
| G7 Escalated OPEX | **IMPLEMENTED** | `escalate_opex` + history mask; GTC uses pre-escalated FI import (FW3=0) |
| G8 SLN / Acq / Expensed CAPEX | **IMPLEMENTED** | FP=FF; GX/HC series surface for CR/HT hand-off (array bodies deferred) |

---

## 3. CaseInput integration

Single `CaseInput` path (manual + Excel import). New fields (not dual input systems):

- `cost_mode_field`, oil/gas TC category series, `ca_rates`, `opex_escalation_rate`
- `oil_sln_by_year`, `oil_acq_allowance_by_year`, gas counterparts, `acquisition_cost`
- Consumes existing: `hurdle_rate`, `duties_rate`, `vat_rate`, fields, history, start year

Provenance in `src/pems/domain/provenance.py`.

---

## 4. Formula / dependency mapping

```text
CaseInput schedules (Cap_Allow FF–FI selected path)
  → G3: FP=FF; FN=(FG+FH)*C20; FO=(FF+FG+FH)*C21; FQ=FG+FH+FN+FO
  → G4: FK=(FF+FG+FH)/(1+C15)^(FE−FE0); FL=FI/(1+C15)^(…)
  → G5: FR rates surface
  → G6: N16=FL48_o+FL48_g; S16=FI48_o+FI48_g; N17=FK48_o+FK48_g;
        S17=FP48+FQ48 oil+gas; N18=N16+N17; S18=S16+S17
  → G8: GX/HC series + HB acquisition cost → CR/HT interfaces (later gates)
```

Units: **$mm** annual throughout.

---

## 5. Unit / timing treatment

| Topic | Treatment |
|-------|-----------|
| Cost units | $mm (no silent conversion) |
| Discount base | First year of Cap_Allow FE block |
| Hurdle | Ec_IO C15 / CaseInput `hurdle_rate` |
| Escalation | Block_TC FW3 factor; not inflation CaseInput |
| Equity | Does not scale costs |

---

## 6. Test results

| Suite | Result |
|-------|--------|
| Costs unit (`tests/unit/test_costs.py`) | **16 passed** |
| Costs GTC (`tests/validation/test_costs_gtc.py`) | **4 passed** |
| Full suite (incl. Phase 0/1A/1B) | **55 passed / 0 failed** |

Coverage: undisc aggregation, discount, hurdle sensitivity, oil/gas stacks, history, field mode, CA rates, escalated OPEX, SLN/Acq, Ec_IO hub, determinism, empty schedule, duties/VAT.

---

## 7. GTC comparison results (mandatory anchors)

| Metric | Count |
|--------|------:|
| Comparison points | **19** |
| Exact | **10** |
| Tolerance (1e-9) | **9** |
| Mismatch | **0** |
| Unresolved | **0** |

Anchors: Cap_Allow FI48/FL48/FK48/FP48/FQ48, FR5:FR9, Cap_Allow Gas FI48/FL48/FK48, Ec_IO N16:S18.

---

## 8. Discrepancy resolution

None open on mandatory anchors at gate completion.

---

## 9. GM SHA verification

| Check | Result |
|-------|--------|
| Active SHA | `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA` |
| On-disk verify | **MATCH** |
| GM modified | **No** (read-only openpyxl) |

---

## 10. Deferred items

- Full multi-field Block_TC GUI  
- GX/HC full array-formula reimplementation (series surface provided)  
- Transport/processing categories  
- Generic inflation CaseInput  
- FLGT, CR/NCF, RESULTS engines  
- Ec_IO P16–P18 revenue hub; NCF KPI hub G3–G15  
- Presentation / formatting  

---

## 11–12. Claims

| Claim | Status |
|-------|--------|
| **COSTS = IMPLEMENTED** | **YES** |
| **COSTS GTC SUBSET = PASS** | **YES** |
| **COSTS NUMERICALLY VALIDATED** | **NOT CLAIMED** |

---

## 13. Next gate

**PHASE 1D — FLGT / Royalties** per `FLGT_ROYALTIES_CONTRACT.md`  

Sequence:

```text
CaseInput ✓ → Ec_IO pure ✓ → Production ✓ → Costs ✓
  → FLGT → CR/NCF → RESULTS → full-system GTC → numerical parity → presentation
```

Do not proceed to FLGT until Phase 1C is acknowledged.
