# Critical-Path Module Readiness

**GM identity SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**UPDATED:** Final pre-implementation reconciliation  
**Note:** READY = implementation-ready semantics (not PEMS numerical VALIDATED)

Closed domain decisions (do not reopen):
- Equity Dash Share **C4** = **INPUT**
- Fiscal Terms_PIA = **LAW TABLE**

---

## Ec_IO / Parameters (M-CP-01)

| Criterion | Status |
|-----------|--------|
| Formula groups | Hub roles UNDERSTOOD; full formula-group engine still later modules |
| Inputs | **READY** — full CaseInput contract (`EC_IO_PARAMETER_CONTRACT.md`); equity **INPUT** closed |
| Outputs | Hub outputs identified (not CaseInput) |
| Dependencies | Documented (consumers + fiscal interface) |
| Units | From sheet labels |
| Business rules | Input/validation/import only; no calc invention |
| Edge cases | Sensitivity PRESENTATION deferred; bounds flagged for domain confirmation |
| GM comparison points | **YES** — §7 ingestion + KPI consumer map |
| Spec | `EC_IO_PARAMETER_CONTRACT.md` + `INPUT_SCHEMA_CRITICAL_PATH.md` |
| Implementation (Phase 1A) | **IMPLEMENTED** pure CaseInput derivations + dual-path CaseInput; hub HUB_OUTPUT deferred — see `PHASE1A_EC_IO_IMPLEMENTATION.md` |
| GTC (Phase 1A subset) | **PASS** 35 exact / 0 mismatch (GTC-001) |
| **Status** | Spec **READY**; pure path **IMPLEMENTED**; full-sheet / system **VALIDATED NOT CLAIMED** |

---

## Fiscal Terms_PIA (M-CP-01 / Fiscal)

| Criterion | Status |
|-----------|--------|
| Semantics | **UNDERSTOOD** as LAW TABLE |
| Inputs | N/A as user inputs — **LAW TABLE** |
| Outputs | Rule parameters for fiscal layer |
| Dependencies | Downstream Royalties/FLGT/CR/NCF |
| Units | Documented on sheet labels |
| Business rules | Rule blocks documented in FISCAL_TERMS_PIA_LAW_TABLE.md |
| Edge cases | Tier selection by terrain/production/price |
| GM comparison points | Via consumer outputs + table identity vs GM SHA |
| **Status** | **READY** (for implementing regime/reference data load & read API — not full fiscal engine alone) |

---

## Production Profile → Prod_Summary (M-CP-02)

| Criterion | Status |
|-----------|--------|
| Semantics | **UNDERSTOOD** — decline/build-up/plateau groups + block annualization |
| Inputs | Linked to Ec_IO CaseInput (field, days, analysis type, history) |
| Outputs | Prod_Summary V47/Y47–Y50/AF26 documented |
| Dependencies | → Royalties/FLGT/Cap_Allow/RESULTS; ← Ec_IO, STOIIP/GIIP interface |
| Units | mb/d, mmbbls, mmscf/d, bscf, mmboe |
| Edge cases | Zero rate, History window, STOIIP vs GIIP mode |
| GM comparison points | **YES** — contract §9 |
| Spec | `PRODUCTION_PROFILE_CONTRACT.md` |
| Unresolved literals | 0 |
| Implementation (Phase 1B) | **PASSED / IMPLEMENTED** G1–G5 — `PHASE1B_PRODUCTION_IMPLEMENTATION.md` + `PHASE1B_GATE_ACKNOWLEDGEMENT.md`; G6 deferred |
| GTC (Phase 1B subset) | **PASS** 22 pts (20 exact / 2 tol / 0 mismatch) |
| **Status** | Spec **READY**; G1–G5 **IMPLEMENTED** (gate PASSED); full-sheet / system **VALIDATED NOT CLAIMED** |

---

## Costs / Cap_Allow (M-CP-03)

| Criterion | Status |
|-----------|--------|
| Semantics | **UNDERSTOOD** — TC categories + Cap_Allow discount/CA groups |
| Formula groups | G1–G6 documented (`COSTS_PARAMETER_CONTRACT.md`) |
| Inputs/outputs/deps | Linked to Ec_IO + Production; hub N16–S18 |
| Units | $mm; CA rates fraction |
| GM comparison | **YES** — FI/FK/FL/FP/FQ + Ec_IO N16–S18 |
| Spec | `COSTS_PARAMETER_CONTRACT.md` |
| Phase 1C plan | **READY** — `PHASE1C_COSTS_IMPLEMENTATION_GATE.md` |
| Implementation | **IMPLEMENTED** G1–G8 — `PHASE1C_COSTS_IMPLEMENTATION.md` |
| GTC (Phase 1C subset) | **PASS** 19 pts (10 exact / 9 tol / 0 mismatch) |
| **Status** | Spec **READY**; G1–G8 **IMPLEMENTED**; full-sheet / system **VALIDATED NOT CLAIMED** |

---

## FLGT / Royalties (M-CP-04)

| Criterion | Status |
|-----------|--------|
| Semantics | **UNDERSTOOD** — rate engine + FLGT $mm application |
| Law rates | Fiscal Terms_PIA LAW TABLE only (no duplicate) |
| Volume/price/cost bases | Prod_Summary + Ec_IO + Block_TC/Cap_Allow Gas |
| GM comparison | **YES** — AB51/AC51/AD51/AM51/W51/X51 + Ec_IO G11/G15 |
| Spec | `FLGT_ROYALTIES_CONTRACT.md` |
| **Status** | **READY** (spec — not numerical VALIDATED) |

---

## CR/NCF visible (M-CP-05)

| Criterion | Status |
|-----------|--------|
| Semantics | **UNDERSTOOD** — CR Econ + HT/CIT + Project/Equity NCF groups |
| Edge cases | AU14 no-sign-change IRR **EXPECTED** |
| Equity scaling | Equity Dash C4 **INPUT** only |
| GM comparison | **YES** — AG51/AH51/AB–AD/AG58/AU14 + equity AG/AH |
| Spec | `CR_NCF_CONTRACT.md` |
| **Status** | **READY** (spec — not numerical VALIDATED) |

---

## RESULTS (M-CP-06)

| Criterion | Status |
|-----------|--------|
| Semantics | **UNDERSTOOD** — RESULTS Equity KPI inventory |
| Role | Output/consumer layer (no CaseInput on sheet) |
| Equity | C4 scale; closed INPUT |
| IRR | N8/K8 numeric goldens; Project_NCF AU14 **NO_VALID_IRR** |
| GM comparison | **YES** — GTC-001 RESULTS Equity KPI pack (63 rows) |
| Spec | `RESULTS_PARAMETER_CONTRACT.md` |
| **Status** | **READY** (spec — not numerical VALIDATED) |

---

## Summary

| Module | Status |
|--------|--------|
| Ec_IO / Parameters | **READY** (`EC_IO_PARAMETER_CONTRACT.md`) |
| Fiscal Terms_PIA (law table load) | **READY** |
| Production | **READY** (`PRODUCTION_PROFILE_CONTRACT.md`) |
| Costs | **READY** (`COSTS_PARAMETER_CONTRACT.md`) |
| FLGT/Royalties | **READY** (`FLGT_ROYALTIES_CONTRACT.md`) |
| CR/NCF | **READY** (`CR_NCF_CONTRACT.md`) |
| RESULTS | **READY** (`RESULTS_PARAMETER_CONTRACT.md`) |

**All critical-path calculation module specifications:** **READY** (implementation + numerical VALIDATED still separate gates).  
**First implementable slice:** Fiscal Terms law-table package load (**READY**), after path integrity fixed.
