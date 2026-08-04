# CR / NCF Contract — Implementation Readiness

**Status:** **READY** (cashflow / tax application specification only — not calculation VALIDATED; **not IMPLEMENTED**)  
**Active GM SHA (approved):** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Module:** M-CP-05 / M07 CR Econ + HT/CIT NCF + Project/Equity NCF  
**GM modified:** **No**  
**Calculation code under this task:** **None**  
**Parameter companion:** `CR_NCF_PARAMETER_CONTRACT.md`  
**Phase 1E readiness:** `docs/03_IMPLEMENTATION/PHASE1E_CR_NCF_READINESS.md` → **READY** (implementation requires separate authorization)

**Do not reopen:** GM approval CLOSED · Equity C4 INPUT · C5 DERIVED · Fiscal LAW TABLE · AU14 expected · upstream **IMPLEMENTED** (1A–1D) · 829/829 · ADR-0010  

**Upstream contracts:**  
`EC_IO_PARAMETER_CONTRACT.md` · `PRODUCTION_PROFILE_CONTRACT.md` · `COSTS_PARAMETER_CONTRACT.md` · `FLGT_ROYALTIES_CONTRACT.md` · `FISCAL_TERMS_PIA_LAW_TABLE.md`  

**Evidence:** catalogue · `CR_NCF_EVIDENCE_EXTRACT.json` · GTC-001 · `PROJECT_NCF_AU14_INVESTIGATION`  

---

## 0. Scope (visible implementation surface)

| Sheet | State | Role |
|-------|-------|------|
| **CR Econ** | visible | Cost recovery / profit oil / CRL / expensed CAPEX / OPEX bridge |
| **HT_NCF_Oil** | visible | Hydrocarbon tax NCF (oil path) |
| **CIT_NCF_Oil** / **CIT_NCF_Gas** | visible | Companies Income Tax NCF by stream |
| **Project_NCF** | visible | Project consolidated NCF, taxes, disc. CF, IRR |
| **HT_NCF_Oil Equity**, **CIT_NCF_* Equity**, **Equity_NCF_Con** | visible | Equity-scaled NCF views |
| HT_NCF, CIT_NCF, Project_NCF_Con | **hidden** | Out of **input** scope; may still be formula peers — catalogue-only; do not modify |

---

## 1. Architecture (workbook-evidenced)

```text
Ec_IO (selectors, hurdle C15, licence G22, PFS G24, years)
   ↓
Production → volumes (via FLGT / CR year spine)
   ↓
Costs (Cap_Allow FP/FI/GX/HC …)
   ↓
FLGT / Royalties (revenues W/X/Y; royalties AB–AD; FL govt items)
   ↓
CR Econ  ──CRL / profit oil / cost recovery (LAW_TABLE params)
   ↓
HT_NCF_Oil · CIT_NCF_Oil · CIT_NCF_Gas
   ↓
Project_NCF  (project view: host/contractor NCF, disc., IRR)
   ↓
Equity_* sheets × Equity Dash!C4  → Equity_NCF_Con
   ↓
RESULTS Equity / Ec_IO hub KPIs
```

**Direct bypasses (documented):**

| Link | Nature |
|------|--------|
| Project_NCF ← FLGT | Royalties, FLGT items, loan PPMT/IPMT |
| Project_NCF ← Cap_Allow | CAPEX lines W/X paths (catalogue) |
| Project_NCF ← Ec_IO | Hurdle, D22 end year, C5 discount base |
| CR Econ ← Ec_IO G22/G24 | CRL acreage & PSC/SC branch |
| CR Econ ← CIT_NCF_Oil!Z | Eligible cost fragment |
| Equity sheets ← Equity Dash!C4 | Share scale (INPUT) |
| Ec_IO hub ← Project_NCF / CIT_NCF | Presentation KPIs only |

---

## 2. CR Econ — cost recovery / concessionary bridge

### 2.1 Headers (row 3, unit $mm unless noted)

| Col | Label / source | Role |
|-----|----------------|------|
| A | Year ← FLGT!A | Time |
| B | Oil revenue ← FLGT!W | Revenue |
| C | Gas revenue ← FLGT!X | Revenue |
| D | Total revenue ← FLGT!Y | Revenue |
| E | **Royalties** | `=SUM(FLGT!AB:AD)` |
| F | **FL Govt Pmt** | FLGT AE+AF+AG+AH+Z (rentals, HCDT, NDDC, …) |
| G | **Expensed CAPEX** | Cap_Allow!FP + Gas!FP |
| H | **CAPEX DEPR** | Cap_Allow GX+HC (+ gas) — SLN + Acquisition Allowance |
| I | **OPEX** | Cap_Allow!FI + Gas!FI |
| J | CIT_NCF_Oil!Z | Eligible cost adjunct |
| K | **Eligible Total Cost** | `F+H+I+G+J` |
| L | **Cost Recovery Limit** | LAW: if G22=New Acreage T59 → T60×(D−E) else U60×(D−E) |
| M | **Profit Oil** | `D−E−L` |
| N | Cost to Recover C/F | Carry logic |
| O | ECR | Excess cost recovery |
| P | Project Total Oil | O+M |
| Q | Cum production ← FLGT!D | mmbbls for split |
| R | **HG Profit Oil Split** | LAW profit-oil tiers vs Q |
| S | Contractor Profit Split | `1−R` |
| T | Contractor Oil $mm | `S×P` |
| U | Government Oil $mm | PSC/SC: `P−T` when G24="PSC/SC" else 0 |

**Selectors (CaseInput / LAW):**

| Driver | Source | Use |
|--------|--------|-----|
| Licence / acreage | Ec_IO!G22 | CRL branch T59/T60 vs U60 |
| PFS / contract | Ec_IO!G24 | PSC/SC government oil U |
| CRL & profit oil rates | Fiscal Terms_PIA T59–X* | **LAW_TABLE** — not CaseInput |

### 2.2 Classification

| Item | Class |
|------|-------|
| Revenues B–D | DERIVED ← FLGT |
| Royalties E, FL govt F | DERIVED ← FLGT |
| G/H/I cost feeds | DERIVED ← Costs |
| L/R splits | LAW_TABLE CONSUMER (FORMULA) |
| M/N/O/P/T/U | INTERMEDIATE / OUTPUT |

---

## 3. HT / CIT NCF streams (visible)

### 3.1 Role

| Sheet | Purpose (from labels / Model Map) |
|-------|-----------------------------------|
| HT_NCF_Oil | Hydrocarbon Tax cashflow path; feeds Project_NCF AD (Htax) |
| CIT_NCF_Oil / CIT_NCF_Gas | CIT by stream; revenues B, CIT AF, Education tax AG, etc. |
| Equity variants | Same structure × equity share |

**Detail formulas:** catalogue (thousands of cells). Implementation must follow sheet formulas; this contract defines **groups and interfaces**, not every line rewrite.

### 3.2 Documented interfaces into Project_NCF

| Project_NCF col | Label | Source pattern |
|-----------------|-------|----------------|
| B | Nominal Oil & Gas Revenue | CIT_NCF_Oil!B + CIT_NCF_Gas!B |
| AB | **CIT** | CIT_NCF_Oil!AF + CIT_NCF_Gas!AF |
| AC | **Education Tax/Devt Levy** | CIT_*!AG |
| AD | **Htax** | HT_NCF_Oil!AO |

---

## 4. Project_NCF — project cashflow structure

### 4.1 Material column groups (row 3 labels)

| Group | Columns | Meaning |
|-------|---------|---------|
| Revenue | B–D | Oil & gas / condensates / NGL revenues |
| Allowable deductions S.263 | E–S | Cost of prod, FLGT items, royalties, repairs, exploration wells, aband. fund, levies, reinjection, HCDT/NDDC links, **Total Allowable Cost S** |
| Assessable income | T–V | Adjusted oil profit, loss C/F, assessable oil profit |
| CAPEX | W–X | Intangible / Tangible CAPEX |
| CIT base / tax | Y–AA, AB–AD | Min tax, chargeable profit, **CIT, Education tax, Htax** |
| **AITX NET CASH FLOW** | **AE Host Govt**, **AF Contractor** | Undiscounted host / contractor NCF |
| Discounted | AG Host, AH Contractor | PV at hurdle (± Analysis N14) |
| Metrics | AI Contractor Disc. CNCF, AJ Payout | Disc. cumulative / payout years |
| IRR series | AF annual contractor CF; AG58=IRR(AF5:AF49); AU12=IRR(AF5:AF40); **AU14=IRR(AK5:AK49)→#NUM!** | |

### 4.2 Critical formula patterns (Project_NCF)

| Cell | Formula (evidenced) | Role |
|------|---------------------|------|
| A5 | `='CR Econ'!A5` | Year from CR |
| B5 | `=CIT_NCF_Oil!B5+CIT_NCF_Gas!B5` | Combined revenue |
| AE5 | Host govt CF = sum of fiscal takes (AD+AC+AB+R+…+F) gated by D22 | Host undisc. |
| AF5 | Contractor NCF = (B−AE−W−X−E−J−FLGT AO−AP+AN−Equity L)*(A≤D22) | Contractor undisc. |
| AG5 / AH5 | AE/AF discounted by `(1+C15×(1+Analysis!N14))^(A−C5)` | Disc. host/contractor |
| AJ5 | Payout period logic on AI | Years |
| AG51 / AH51 | SUM disc. host / contractor | GTC KPIs |
| AG58 | `=IRR(AF5:AF49)` | Project IRR ~34.86% |
| AU14 | `=IRR(AK5:AK49)` | **#NUM!** EXPECTED (blank series / no sign change) |

### 4.3 Sign conventions (preserve GM)

| Item | Convention on GM |
|------|------------------|
| Revenue B | Positive inflow |
| CAPEX W/X, costs, taxes in AE sum | Positive magnitudes subtracted in AF |
| Contractor AF | Can be negative (outflow years) or positive |
| Discounted AG/AH | Same sign as undisc. after discount factor |
| IRR | On AF series (contractor undisc. CF) |
| AU14 | Error string `#NUM!` — **not** a numeric IRR |

Do **not** flip signs for software convenience if that changes AF/IRR semantics.

---

## 5. Equity NCF

| Element | GM | Class |
|---------|-----|-------|
| Company 1 share | Equity Dash!C4 = **0.49** | **INPUT** (closed) |
| Company 2 share | C5=`=C6−C4` | **DERIVED** |
| Project total | C6 = 1 | DEFAULT_STRUCTURAL |
| Equity_NCF_Con / * Equity sheets | Scale project/CIT/HT lines by C4 (hundreds of refs) | DERIVED view |
| Equity_NCF_Con AG51 / AH51 | 73.283… / 38.264… | Disc. host/contractor equity view (GTC) |

**No second independent equity input.**

---

## 6. Tax / fiscal interfaces (application only)

| Interface | CR/NCF consumption | Law source |
|-----------|-------------------|------------|
| Royalties | CR E; Project G–I | FLGT ← Royalties ← LAW |
| FLGT front-end | CR F; Project F,O–R | FLGT ← LAW % + Costs |
| Capital allowance / SLN / Acq | CR H; Cap_Allow GX/HC | Costs + LAW CA rates |
| Expensed CAPEX | CR G ← Cap_Allow FP | Costs |
| OPEX | CR I ← Cap_Allow FI | Costs |
| CRL / profit oil | CR L,R | Fiscal Terms_PIA |
| HT | Project AD ← HT_NCF_Oil | LAW dual-tier HT |
| CIT | Project AB ← CIT_NCF | LAW CIT |
| Education tax | Project AC | LAW 0.04 pattern via CIT sheets |
| Hurdle discount | AG/AH | Ec_IO C15 (+ Analysis N14 sensitivity) |

**Fiscal Terms_PIA remains LAW TABLE.** CR/NCF only applies.

---

## 7. Time axis

| Element | Source |
|---------|--------|
| Year spine | CR Econ A ← FLGT A; Project A ← CR |
| Start / discount base | Ec_IO!C5 |
| End gate | Ec_IO!D22 (`A<=D22` on many Project lines) |
| Project life | Ec_IO!C6 ← Prod_Summary AF26 |
| History/Forecast | Ec_IO C4 + D28/E28 (upstream filters) |
| Annual periods | Rows 5–49 typical for SUM/IRR |

Single timeline owned by Ec_IO + Production; CR/NCF **consumes** it.

---

## 8. Dependency order

```text
1. CaseInput (Ec_IO) + Fiscal law load
2. Production volumes
3. Costs (Cap_Allow feeds)
4. FLGT / Royalties
5. CR Econ
6. HT_NCF_Oil + CIT_NCF_Oil/Gas  (parallel streams)
7. Project_NCF
8. Equity_* × C4 → Equity_NCF_Con
9. RESULTS / Ec_IO hub
```

**Iteration:** None required beyond Excel natural calc order for GTC as-saved.  
**Data tables:** Analysis sensitivity — deferred (not CR core).  
**Hidden sheets:** May mirror visible NCF; implementation prefers **visible** Project_NCF / CIT_NCF_Oil/Gas / HT_NCF_Oil / Equity_NCF_Con.

---

## 9. Edge conditions (evidenced)

| Condition | Handling |
|-----------|----------|
| Zero production / revenue | CR/FLGT zeros cascade; CRL/profit oil IF guards |
| Zero costs | Eligible cost K may be royalty/FLGT only |
| Negative contractor NCF | Allowed (AF negative years) |
| No sign change IRR | **AU14 #NUM!** EXPECTED — PEMS returns no-IRR / equivalent; **never invent** numeric IRR for AK5:AK49 |
| Valid IRR | AG58 / AU12 numeric ~0.3486 |
| PSC vs non-PSC | U government oil only if G24="PSC/SC" |
| Equity 0 / 1 | Scale factor C4; C5 derived remainder |
| Pre/post D22 | Cashflow lines zeroed when A>D22 |

---

## 10. Module interface (READY upstream)

| From | Into CR/NCF | Validation |
|------|-------------|------------|
| Ec_IO | G22, G24, C15, C5, D22, C6 | CaseInput contract |
| Production | Via FLGT volumes/years | Production contract |
| Costs | FP, FI, GX, HC (oil+gas) | Costs contract |
| FLGT/Royalties | W/X/Y, AB–AD, AE–AH, Z, AO/AP/AN | FLGT contract |
| Fiscal Terms_PIA | CRL, profit oil tiers, tax rates (via HT/CIT sheets) | LAW TABLE load |
| Equity Dash C4 | Equity NCF scale | INPUT closed |

---

## 11. GTC comparison contract

| GM cell | Expected | Meaning | PEMS target |
|---------|----------|---------|-------------|
| Project_NCF!AG51 | 149.557072245101 | Disc. Host Govt sum | Project disc. host |
| Project_NCF!AH51 | 78.0891606587929 | Disc. Contractor sum / NPV-like | Project disc. contractor |
| Project_NCF!AJ51 | 5.13925728744526 | Payout-related sum | Payout metric |
| Project_NCF!AE51 | 310.69425355464 | Host undisc. sum | Host NCF total |
| Project_NCF!AF51 | 250.725376476001 | Contractor undisc. sum | Contractor NCF total |
| Project_NCF!AB51 | 148.760486089522 | CIT total | CIT |
| Project_NCF!AC51 | 26.4540677567758 | Education tax total | EDT |
| Project_NCF!AD51 | 42.0829559477558 | Htax total | HT |
| Project_NCF!AG58 | 0.348601049838934 | IRR(AF5:AF49) | Project IRR |
| Project_NCF!AU12 | 0.348601049838934 | IRR(AF5:AF40) | IRR subset |
| Project_NCF!AU14 | **#NUM!** | IRR(AK5:AK49) | **NO_VALID_IRR / match #NUM!** |
| HT_NCF_Oil!AS51 / AT51 | 75.940… / 149.323… | BIT host/contractor style sums | HT path KPIs |
| HT_NCF_Oil!AV51 | 3.39443793901067 | Disc. payout related | HT payout |
| Equity_NCF_Con!AG51 / AH51 | 73.283… / 38.264… | Equity disc. host/contractor | Equity NCF |
| CR Econ G8/H8/I8 | 0 / 0.408… / 15.23 | Sample year cost feeds | CR cost bridge |

Tolerance: existing GTC float policy (abs/rel 1e-9); **AU14 exact error-condition match**.  
Full annual series: `formula_cached_results_all.csv`.  
**Do not claim VALIDATED** until PEMS run.

---

## 12. Remaining gaps (scoped)

| Gap | Handling |
|-----|----------|
| Full HT/CIT line-by-line algorithms | Catalogue formulas; groups + interfaces defined |
| Hidden HT_NCF/CIT_NCF/Project_NCF_Con | Prefer visible sheets; parity via GTC on visible Project_NCF |
| Condensates/NGL C/D columns | Present as labeled revenue lines — implement if formulas non-zero in catalogue |
| Analysis!N14 on discount | Sensitivity multiplier; import as-saved for GTC |
| Equity loan FLGT AN–AP in AF | Present in AF5 formula — include when implementing AF |

**No implementation-critical UNRESOLVED blocking CR/NCF contract.**

---

## 13. Readiness gate

| # | Criterion | Met? |
|---|-----------|------|
| 1 | Implementation-relevant CR/NCF parameters identified | **Yes** |
| 2 | Revenue streams mapped | **Yes** |
| 3 | Cost streams mapped | **Yes** |
| 4 | Fiscal interfaces mapped | **Yes** |
| 5 | Royalty interface mapped | **Yes** |
| 6 | FLGT interface mapped | **Yes** |
| 7 | Tax interfaces mapped | **Yes** |
| 8 | Project NCF mapped | **Yes** |
| 9 | Equity NCF mapped | **Yes** |
| 10 | Equity share interface mapped | **Yes** (C4 INPUT) |
| 11 | Time axis mapped | **Yes** |
| 12 | Sign conventions documented | **Yes** |
| 13 | Dependencies documented | **Yes** |
| 14 | Critical formula groups mapped | **Yes** |
| 15 | Units documented | **Yes** ($mm, years, fraction) |
| 16 | GTC comparison points established | **Yes** |
| 17 | Downstream RESULTS interfaces established | **Yes** (hub + equity KPIs) |
| 18 | Edge conditions documented | **Yes** (incl. AU14) |
| 19 | No unresolved implementation-critical ambiguity | **Yes** (§12 scoped) |
| 20 | No calculation code written | **Yes** |

# **CR/NCF = READY**

**Means:** Spec sufficient to implement CR Econ bridge + HT/CIT/Project/Equity NCF application against **IMPLEMENTED** upstream modules (1A–1D) and LAW TABLE.  
**Does not mean:** CR/NCF IMPLEMENTED, numerical PEMS-vs-GM VALIDATED, or RESULTS implementation.  
**Does not authorize** calculation code — Phase 1E readiness only; implementation requires a **separate** Phase 1E implementation authorization.
