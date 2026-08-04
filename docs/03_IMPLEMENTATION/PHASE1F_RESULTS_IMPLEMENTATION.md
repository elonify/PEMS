# Phase 1F — RESULTS Implementation Report

**Date:** 2026-08-04  
**Task type:** Controlled RESULTS Equity **calculation / KPI aggregation** implementation  
**Presentation / charts / sensitivity / Monte Carlo:** **Not implemented**  
**Git commit:** **None** (separate checkpoint directive required)

**Authority:**  
- Project Owner **RESULTS IMPLEMENTATION AUTHORIZATION** (this phase)  
- `docs/02_SPECIFICATIONS/modules/RESULTS_PARAMETER_CONTRACT.md`  
- `docs/03_IMPLEMENTATION/PHASE1F_RESULTS_READINESS.md`  
- GTC-001 RESULTS Equity pack (63 rows)  

**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**GM modified:** **No**

---

## A. Authorization

| Item | Status |
|------|--------|
| Phase 1F readiness | **READY** (checkpoint `2244674`) |
| PO implementation authorization | **GRANTED** |
| Scope | RESULTS Equity KPI aggregation only |

---

## B. Scope

Implemented pure **read-model / aggregation** over:

```text
CaseInput + Equity C4
  → Ec_IO identity / hurdle / life
  → Production (V47, Y47, Y49, Y50)
  → Costs (Ec_IO N16–S18 hubs)
  → FLGT (W51/X51, AB51/AC51/AD51)
  → CR/NCF (Equity_NCF_Con AIT NPVs, undisc take, payout, AF-series IRR)
  → HT_NCF_Oil Equity intermediates (BIT path — selected import path)
  → CIT_NCF_* Equity totals (tax path — selected import path)
  → RESULTS Equity KPIs
```

**Not in scope:** presentation, charts, sensitivity, Monte Carlo, full HT/CIT line-by-line engines, full-system validation claim.

---

## C. Formula groups implemented

| Group | Status | Notes |
|-------|--------|-------|
| R-ID | **Yes** | L2/L3/L5/C5–C8/H7 from CaseInput |
| R-NPV | **Yes** | BIT ← HT equity intermediates; AIT ← CR equity AG/AH |
| R-IRR | **Yes** | BIT IRR on HT AR series; AIT IRR on equity-scaled AF; PVR/PI/GRR |
| R-TAKE | **Yes** | Undisc/disc BIT & AIT takes; FLI H15 |
| R-PAYOUT | **Yes** | K14 HT AV51; N14 Project/Equity AJ51 |
| R-COST | **Yes** | N/S hubs × C4 |
| R-REV | **Yes** | FLGT W/X as Ec_IO P16/P17 × C4 |
| R-UNIT | **Yes** | Excel order `eq_cost/Y50/C4` preserved |
| R-ROY | **Yes** | AB/AC/AD × C4; ERR H25/J18 |
| R-TAX | **Yes** | HT AO51; CIT Oil+Gas AF/AG; sum J25 |
| R-PROD | **Yes** | V47/Y49 × C4; M23 Bscf text; N24 |

Authorization text listed R-ID, R-NPV, R-IRR, R-ROY, R-TAX, R-PROD; readiness also mapped R-TAKE, R-PAYOUT, R-COST, R-REV, R-UNIT — **all implemented** as required for the RESULTS Equity GTC surface.

---

## D. Inputs and dependencies

| Input | Source |
|-------|--------|
| Equity C4 | `CaseInput.equity_share_company_1` |
| Identity | CaseInput country/regime/field/licence/terrain/PFS |
| Hurdle / life | CaseInput / Production AF26 |
| Cost hubs | `CostsResult` N16/N17/S16/S17 |
| Revenue hubs | `FlgtResult` W51/X51 (Ec_IO P16/P17 equivalent) |
| Royalties | `FlgtResult` AB51/AC51/AD51 |
| Production | `ProductionResult` V47/Y47/Y49/Y50 |
| AIT NCF | `CrNcfResult` equity_ag51/ah51, ae51/af51, aj51, contractor_af |
| BIT HT equity | `case.extras["ht_ncf_oil_equity_intermediates"]` (import) |
| CIT equity tax | `case.extras["cit_ncf_equity_totals"]` (import) |

**No new CaseInput fields invented.**

---

## E. Outputs / KPIs

`ResultsResult.cell_map()` exposes all material RESULTS Equity cells used by GTC-001 (59 unique cells; 63 pack rows including duplicate L5 context).

Representative: J7/K7/M7/N7 NPVs; K8/N8 IRR; K9–K11 / N9–N11; takes; H16–H26; J16–J25; N22–N24; identity.

---

## F. IRR / error semantics

| Path | Behavior |
|------|----------|
| BIT K8 | `excel_irr(HT equity AR5:AR49)`; no sign change → **`NO_VALID_IRR`** |
| AIT N8 | `excel_irr(equity-scaled Project AF)`; same policy |
| Project AU14 | Unchanged in CR/NCF; not a RESULTS cell |

Do not map `#NUM!` / `NO_VALID_IRR` to 0 or blank success.

---

## G. GTC mapping

| Item | Result |
|------|--------|
| Pack | `GTC-001_kpi_and_intermediates.csv` filtered `worksheet == RESULTS Equity` |
| Comparison points | **63 rows** / **59 unique cells** |
| Policy | float abs/rel **1e-9**; text exact |
| Expected values rewritten? | **No** |

---

## H. Unit tests

| ID | File | Result |
|----|------|--------|
| T01–T08 + helpers | `tests/unit/test_results.py` | **11 passed** |

Coverage: identity, C4 scale, unit-cost order, ERR, takes, PVR/PI/GRR, IRR numeric, NO_VALID_IRR, BIT/AIT distinction.

---

## I. GTC test results

| Test | Result |
|------|--------|
| `tests/validation/test_results_gtc.py` | **3 passed** |
| Unique RESULTS Equity cells vs pack | **0 mismatches** |
| High-value anchors (N7, M7, J7, K7, N8, K8, N14, H26, J18, H25, J25) | **PASS** |

---

## J. Discrepancy report

| Item | Status |
|------|--------|
| Unexplained GTC mismatches | **0** |
| Forced expected-value edits | **None** |
| Tolerance weakened | **No** |

**Implementation note (not a discrepancy):** BIT HT equity KPIs and CIT equity tax totals use **selected intermediate import** from GM (same class of path as Phase 1E HT/CIT project intermediates). Full HT/CIT equity engines remain deferred (A5). Formulas for pure aggregation (scale, ratios, ERR, unit costs, AIT from CR/NCF) are computed in PEMS.

---

## K. Deferred items

| Item | Bound |
|------|-------|
| Presentation formats / layout | PRESENTATION phase |
| Charts / dual-axis | PRESENTATION |
| Sensitivity / Monte Carlo | DEFERRED |
| Full HT_NCF_Oil Equity engine | Catalogue / later |
| Full CIT_NCF Equity engine | Catalogue / later |
| Full-system numerical validation | Separate gate |
| `run_pipeline` end-to-end wiring | Optional later |

Ambiguities **A1–A6** retained as documented (not silently removed).

---

## L. Performance notes

| Run | Wall clock (approx.) |
|-----|----------------------|
| RESULTS unit only | ~few seconds |
| RESULTS unit + GTC (1 GM load via module fixture) | ~103 s |
| Targeted RESULTS + CR unit + CR GTC + scaffold | ~312 s |

Single module-scoped GM import for RESULTS GTC. Full-suite regression **not** used as primary gate.

---

## M. Golden Master integrity

| Check | Result |
|-------|--------|
| Expected SHA | `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA` |
| Actual (pre/post) | **MATCH** |
| GM modified | **NO** |
| Open mode | read-only import only |

---

## N. IMPLEMENTED status

# **RESULTS = IMPLEMENTED**

Criteria met:

1. Authorized formula groups coded  
2. Interfaces via upstream modules + documented intermediates  
3. Unit tests T01–T08 PASS  
4. RESULTS GTC subset **0 unexplained mismatches**  
5. Expected-error IRR policy correct  
6. Targeted upstream CR/NCF + scaffold regression PASS  
7. GM SHA MATCH  

---

## O. NUMERICALLY VALIDATED status

# **NOT CLAIMED**

GTC implementation-gate PASS ≠ formal numerical VALIDATED promotion.

---

## P. Full-system validation status

# **NOT CLAIMED**

---

## Q. Next gate recommendation

| Item | Recommendation |
|------|----------------|
| RESULTS IMPLEMENTED | **YES** (this report) |
| RESULTS NUMERICALLY VALIDATED | Separate formal validation gate if required |
| Presentation | Deferred |
| Sensitivity / Monte Carlo | Deferred |
| Git checkpoint | **Separate PO authorization** — do not auto-commit |
| Full-suite regression | Optional offline; not required for this gate |

### Explicit three-state

```text
SPECIFICATION READY     = YES
IMPLEMENTED             = YES
NUMERICALLY VALIDATED   = NOT CLAIMED
```

**STOP.** No presentation. No sensitivity/MC. No commit/push under this directive.
