# Phase 1E — CR/NCF Readiness Report

**Date:** 2026-08-04  
**Task type:** Specification / readiness analysis **only**  
**Calculation code written:** **None**  
**Module stub remains:** `src/pems/calculations/modules/cr_ncf.py` → `UnimplementedModule`  

**Authority:**  
- `docs/02_SPECIFICATIONS/modules/CR_NCF_CONTRACT.md`  
- `docs/02_SPECIFICATIONS/modules/CR_NCF_PARAMETER_CONTRACT.md`  
- GM SHA `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
- Evidence: `CR_NCF_EVIDENCE_EXTRACT.json` · GTC-001 · `PROJECT_NCF_AU14_INVESTIGATION`  

**Upstream gates (closed):** Phase 1A–1D **PASSED** (CaseInput, Ec_IO pure, Production, Costs, FLGT)  

---

## 1. Executive status

| Field | Value |
|-------|--------|
| **Final disposition** | **CR/NCF = READY** |
| Spec contracts | **READY** |
| Implementation | **NOT STARTED** |
| Numerically VALIDATED | **NOT CLAIMED** |
| Full-system VALIDATED | **NOT CLAIMED** |
| Implementation authorized by this report | **NO** — requires separate Phase 1E implementation directive |

---

## 2. Governance / integrity

| Check | Result |
|-------|--------|
| Pre-work GM SHA | **MATCH** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA` |
| Post-work GM SHA | **MATCH** (re-verified) |
| GM modified | **NO** (read-only inspection) |
| Closed decisions reopened | **NO** (Equity INPUT, LAW TABLE, AU14 expected) |
| CR/NCF calc code | **None written** |

---

## 3. CR/NCF workbook map

| Sheet | Visibility | Role |
|-------|------------|------|
| CR Econ | visible | CRL / profit oil / cost recovery bridge |
| HT_NCF_Oil | visible | Hydrocarbon tax path → Project AD |
| CIT_NCF_Oil / CIT_NCF_Gas | visible | CIT + education tax by stream → Project AB/AC/B |
| Project_NCF | visible | Host/contractor NCF, disc., IRR, payout |
| * Equity / Equity_NCF_Con | visible | × Equity Dash C4 |
| HT_NCF, CIT_NCF, Project_NCF_Con | hidden | Out of input scope; catalogue peers only |

---

## 4. Parameter / input contract status

**Document:** `CR_NCF_PARAMETER_CONTRACT.md`  

| Category | Status |
|----------|--------|
| CaseInput selectors (G22, G24, C15, C5, C4, …) | **Mapped** |
| Upstream DERIVED (FLGT rev/royalties, Cap_Allow costs) | **Mapped** — not dual inputs |
| LAW_TABLE (CRL, profit oil, HT/CIT) | **Mapped** — consume only |
| Classification INPUT/DERIVED/LAW/PRESENTATION | **Complete** for implementation-critical items |

---

## 5. Formula-group map

| Group | Purpose | Status |
|-------|---------|--------|
| CR-G1…CR-G4 | Bridge, costs, CRL/profit oil, contractor oil | **Documented** |
| HT-G1 | HT oil NCF | **Documented** (detail → catalogue) |
| CIT-G1/G2 | CIT oil/gas | **Documented** (detail → catalogue) |
| PN-G1…PN-G5 | Project NCF, disc., IRR incl. AU14 | **Documented** |
| EQ-G1 | Equity scale | **Documented** |

Full line formulas: catalogue — **not** invented in this report.

---

## 6. Dependency map

```text
CaseInput + Fiscal LAW load
  → Production
  → Costs (Cap_Allow FP/FI/GX/HC)
  → FLGT (W/X/Y, AB–AD, AE–AH, Z, AN/AO/AP)
  → CR Econ
  → HT_NCF_Oil ‖ CIT_NCF_Oil ‖ CIT_NCF_Gas
  → Project_NCF
  → Equity_* × C4 → Equity_NCF_Con
  → RESULTS / Ec_IO hubs (consumers)
```

Upstream modules **IMPLEMENTED** — interfaces exist for controlled CR/NCF implementation.

---

## 7. Revenue interface

| Feed | Source | CR/NCF use |
|------|--------|------------|
| Oil/gas/total revenue | FLGT W/X/Y | CR B/C/D; CIT B; Project B |
| Royalties | FLGT AB+AC+AD | CR E |
| FL govt | FLGT AE–AH, Z | CR F; Project allowable block |

---

## 8. Cost interface

| Feed | Source | CR/NCF use |
|------|--------|------------|
| Expensed CAPEX | Cap_Allow FP | CR G |
| SLN + Acq allowance | Cap_Allow GX+HC | CR H |
| OPEX | Cap_Allow FI | CR I |
| CAPEX tangible/intangible | Cap_Allow / Project W–X | Project CAPEX; AF |

---

## 9. Fiscal-law interface

**Fiscal Terms_PIA = LAW TABLE** (unchanged).

| Law use | Application point |
|---------|-------------------|
| CRL T59/T60/U60 | CR L via G22 |
| Profit oil tiers | CR R |
| PSC/SC branch | CR U via G24 |
| HT / CIT rates | HT_NCF / CIT_NCF sheets |
| CA rates | Already applied in Costs; CR consumes GX/HC outputs |

Do **not** re-host law rates as CaseInput.

---

## 10. NCF construction (workbook perspectives)

### 10.1 CR Econ (recovery / profit oil)

```text
Revenue D − Royalties E → CRL L = rate×(D−E)
Profit oil M = D−E−L
Eligible costs K = F+H+I+G+J
Carry / ECR N–P; contractor oil T = S×P; gov oil U if PSC/SC
```

### 10.2 Project_NCF (project host vs contractor)

```text
Revenue B (CIT oil+gas)
− Host fiscal stack → AE Host Govt undisc. NCF
Contractor AF = (B − AE − CAPEX − costs − FLGT loan terms − Equity L) × (A≤D22)
Disc. AG/AH at hurdle C15 (± Analysis N14)
IRR on AF series; payout on AI/AJ
```

### 10.3 Equity NCF

```text
Project / stream NCF × Equity Dash!C4 (INPUT)
C5 = C6 − C4 (DERIVED)
```

**Do not collapse** host, contractor, and equity views into one generic NCF.

---

## 11. Economic metrics

| Metric | GM location | Notes |
|--------|-------------|-------|
| Disc. host NCF sum | Project_NCF AG51 | GTC **149.557…** |
| Disc. contractor NCF sum | Project_NCF AH51 | GTC **78.089…** (NPV-like) |
| Host/contractor undisc. | AE51 / AF51 | GTC mapped |
| CIT / EDT / Htax totals | AB51 / AC51 / AD51 | GTC mapped |
| Payout | AJ51 | GTC **5.139…** |
| IRR (valid) | AG58, AU12 | ~**0.3486** |
| IRR (no valid) | **AU14** | **`#NUM!` EXPECTED** → PEMS `NO_VALID_IRR` |
| Equity disc. host/contractor | Equity_NCF_Con AG51/AH51 | GTC mapped |
| ERR | FLGT AM (upstream) | Not recomputed in CR |

**IRR algorithm:** Excel `IRR` on documented ranges; **never invent** numeric IRR for AU14/AK series.

---

## 12. GTC comparison points

| Count class | Cells |
|-------------|--------|
| Project_NCF mandatory pack | AG51, AH51, AJ51, AE51, AF51, AB51, AC51, AD51, AG58, AU12, AU14 |
| Equity pack | AG51, AH51 |
| HT pack | AS51, AL51, AV51 |
| CR sample | G8, H8, I8 |

Tolerance: **1e-9** float; AU14 **expected_error** (`#NUM!` ↔ `NO_VALID_IRR`).  
Source: GM as-saved + contract §11 — **not rewritten**.

---

## 13. Error / edge-case handling

| Condition | Treatment |
|-----------|-----------|
| AU14 no sign change | **EXPECTED** `#NUM!` / `NO_VALID_IRR` |
| Valid IRR AG58/AU12 | Numeric match |
| Negative AF years | Allowed |
| Zero revenue/production | Cascade zeros / IF guards |
| A > D22 | Cashflow terms zeroed |
| PSC vs non-PSC | G24 branch on CR U |

---

## 14. Deferred items

| Item | Bound |
|------|-------|
| Hidden NCF sheets as primary UI | DEFERRED |
| Analysis data tables / Monte Carlo | DEFERRED |
| RESULTS presentation implementation | Separate phase |
| Full HT/CIT prose rewrite of every cell | Catalogue at implement time |
| F-G12 redesign | DEFERRED; AF still includes FLGT AN–AP per GM |

---

## 15. Readiness checklist

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Parameter contract complete | **PASS** |
| 2 | Inputs mapped | **PASS** |
| 3 | Derived fields identified | **PASS** |
| 4 | Formula groups mapped | **PASS** |
| 5 | Dependencies mapped | **PASS** |
| 6 | Timing rules established | **PASS** |
| 7 | Units established | **PASS** ($mm, years, fraction) |
| 8 | Fiscal interfaces established | **PASS** |
| 9 | Revenue interfaces established | **PASS** |
| 10 | Cost interfaces established | **PASS** |
| 11 | NCF construction established | **PASS** (multi-perspective) |
| 12 | Economic metric logic established | **PASS** (incl. AU14) |
| 13 | GTC anchors established | **PASS** |
| 14 | Error handling established | **PASS** |
| 15 | Deferred items bounded | **PASS** |
| 16 | No material unresolved calculation ambiguity | **PASS** (catalogue-scoped detail only) |
| 17 | Upstream modules IMPLEMENTED | **PASS** (1A–1D) |
| 18 | No CR/NCF calculation code in this phase | **PASS** |

---

## 16. Final disposition

# **CR/NCF = READY**

### Meaning

Specification readiness gate is **READY**. Parameter contract + logic contract + GTC anchors + upstream interfaces are sufficient for a **future** controlled implementation.

### Explicit non-claims

| Claim | Status |
|-------|--------|
| CR/NCF **IMPLEMENTED** | **NO** |
| CR/NCF **NUMERICALLY VALIDATED** | **NOT CLAIMED** |
| PEMS-vs-GM full-system validation | **NOT CLAIMED** |
| Implementation authorized | **NO** — requires separate Phase 1E **implementation** authorization |

### Statement for project control

> **CR/NCF specification readiness gate = READY.**  
> **Implementation requires a separate Phase 1E implementation authorization.**

**STOP.** Do not implement CR/NCF or RESULTS under this task.
