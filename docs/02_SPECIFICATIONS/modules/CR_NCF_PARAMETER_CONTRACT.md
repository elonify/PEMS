# CR / NCF Parameter Contract

**Status:** **READY** (parameter / interface contract — not calculation VALIDATED; **not implemented**)  
**Companion logic contract:** `CR_NCF_CONTRACT.md` (formula groups, NCF construction, edges)  
**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Module:** M-CP-05 / M07  
**GM modified:** **No**  
**Calculation code under this document:** **None**  

**Upstream (IMPLEMENTED):** CaseInput · Ec_IO pure · Production G1–G5 · Costs G1–G8 · FLGT R-G1…F-G11  
**Law table:** `FISCAL_TERMS_PIA_LAW_TABLE.md` (CLOSED)  
**Closed:** Equity C4 **INPUT** · C5 **DERIVED** · AU14 `#NUM!` **EXPECTED** NO_VALID_IRR  

---

## 1. Scope surfaces (visible)

| Sheet | Role | Class of surface |
|-------|------|------------------|
| CR Econ | Cost recovery / profit oil / CRL bridge | **CORE CALC** |
| HT_NCF_Oil | Hydrocarbon tax NCF | **CORE CALC** |
| CIT_NCF_Oil / CIT_NCF_Gas | CIT NCF by stream | **CORE CALC** |
| Project_NCF | Project host/contractor NCF, disc., IRR, payout | **CORE CALC** |
| HT_NCF_Oil Equity, CIT_* Equity, Equity_NCF_Con | Equity-scaled views | **CORE CALC** (scale) |
| HT_NCF, CIT_NCF, Project_NCF_Con | Hidden peers | **DEFERRED** for input; catalogue-only |
| RESULTS Equity / Ec_IO hubs | Consumers of NCF KPIs | **PRESENTATION / RESULTS** (not CR engine core) |

---

## 2. CaseInput / ASSUMPTION parameters (CR consumers)

| Parameter | Sheet | Cell | Class | Unit | Type | Validation | Upstream | Downstream |
|-----------|-------|------|-------|------|------|------------|----------|------------|
| `licence_lease_status` | Ec_IO | G22 | CASE_ATTRIBUTE | text | str | enum (New Acreage, …) | CaseInput | CR Econ L CRL branch |
| `pfs_contract_type` | Ec_IO | G24 | CASE_ATTRIBUTE | text | str | R/T (SR) \| PSC/SC | CaseInput | CR Econ U gov oil |
| `hurdle_rate` | Ec_IO | C15 | ASSUMPTION | fraction/yr | float | finite ≥0 | CaseInput | Project AG/AH discount |
| `project_start_year` | Ec_IO | C5 | ASSUMPTION | year | int | [1900,2200] | CaseInput | Discount base year |
| `project_life_years` | Ec_IO | C6 | DERIVED | years | float | from Production | Production | Horizon |
| price path end | Ec_IO | D22 | DERIVED | year | int | — | Ec_IO pure | Project A≤D22 gates |
| `equity_share_company_1` | Equity Dash | C4 | CONFIRMED_INPUT | fraction | float | [0,1] flagged | CaseInput | Equity NCF scale |
| `project_equity_total` | Equity Dash | C6 | DEFAULT_STRUCTURAL | fraction | float | default 1 | CaseInput | C5 derived |
| Analysis N14 | Analysis | N14 | PRESENTATION / sensitivity | fraction | float | import as-saved | Analysis | Discount factor adj. |

**Not CaseInput:** CRL rates, profit-oil tiers, HT/CIT rates, royalty rates — **LAW_TABLE** or upstream DERIVED.

---

## 3. Upstream DERIVED interfaces (not re-input)

| Parameter / series | Source | Class | Unit | Downstream CR/NCF |
|--------------------|--------|-------|------|-------------------|
| Year spine | FLGT!A → CR Econ!A → Project!A | DERIVED | year | All annual series |
| Oil / gas / total revenue | FLGT W/X/Y → CR B/C/D | DERIVED | $mm | CR, CIT revenues |
| Royalties $mm | FLGT AB+AC+AD → CR E | DERIVED | $mm | CR K, Project allowable |
| FL govt payments | FLGT AE+AF+AG+AH+Z → CR F | DERIVED | $mm | CR K, Project |
| Expensed CAPEX | Cap_Allow FP (+gas) → CR G | DERIVED | $mm | CR K |
| CAPEX DEPR (SLN+Acq) | Cap_Allow GX+HC → CR H | DERIVED | $mm | CR K |
| OPEX | Cap_Allow FI (+gas) → CR I | DERIVED | $mm | CR K |
| Loan / PPMT items | FLGT AN/AO/AP | DERIVED | $mm | Project AF formula |
| Volumes (via FLGT) | Production → FLGT | DERIVED | mmbbls/bscf | CR Q, splits |

---

## 4. LAW_TABLE parameters (consume, do not re-host)

| Parameter | Fiscal Terms_PIA | Class | CR/NCF use |
|-----------|------------------|-------|------------|
| CRL New Acreage flag/rate | T59 / T60 | LAW_TABLE | CR L when G22 matches |
| CRL Converted OML rate | U60 | LAW_TABLE | CR L alternate |
| Profit oil tiers | T*–X* profit oil block | LAW_TABLE | CR R HG split |
| HT dual tier | S53+ block | LAW_TABLE | HT_NCF_Oil |
| CIT rates | Dual tier / CIT block | LAW_TABLE | CIT_NCF_* |
| Education tax pattern | via CIT sheets | LAW_TABLE / DERIVED | Project AC |
| CA rates | Cap_Allow FR (law-aligned) | ASSUMPTION on Cap_Allow | Already in Costs; CR uses GX/HC |

---

## 5. Formula groups (IDs for implementation)

| Group ID | Purpose | Primary sheet | GTC anchors |
|----------|---------|---------------|-------------|
| CR-G1 | Year / revenue / royalty / FL govt bridge | CR Econ A–F | sample years |
| CR-G2 | Cost feeds G/H/I (expensed, DEPR, OPEX) | CR Econ | G8/H8/I8 |
| CR-G3 | Eligible cost K; CRL L; profit oil M; carry N/O/P | CR Econ | L formula |
| CR-G4 | Profit oil split R/S; contractor/gov oil T/U | CR Econ | PSC branch |
| HT-G1 | HT assessable / tax / NCF oil path | HT_NCF_Oil | AS51, AT51, AV51 |
| CIT-G1 | CIT oil stream | CIT_NCF_Oil | → Project AB/AC/B |
| CIT-G2 | CIT gas stream | CIT_NCF_Gas | → Project AB/AC/B |
| PN-G1 | Project revenue + allowable cost block | Project_NCF B–S | — |
| PN-G2 | Assessable income / CAPEX / tax stack | Project_NCF T–AD | AB51–AD51 |
| PN-G3 | Host AE / Contractor AF undisc. NCF | Project_NCF | AE51, AF51 |
| PN-G4 | Disc. AG/AH; CNCF AI; payout AJ | Project_NCF | AG51, AH51, AJ51 |
| PN-G5 | IRR AG58, AU12; AU14 NO_VALID_IRR | Project_NCF | AG58, AU12, AU14 |
| EQ-G1 | Equity scale × C4 → Equity_NCF_Con | Equity sheets | AG51, AH51 |

Full formula text: catalogue. Do not invent algorithms.

---

## 6. Units

| Stream | Unit |
|--------|------|
| Money (rev, cost, tax, NCF, NPV-like sums) | **$mm** |
| Rates (tax, equity, IRR) | **fraction** |
| Time | **annual years**; payout **years** |
| Production for splits | **mmbbls** (CR Q) |

---

## 7. Timing

| Element | Rule |
|---------|------|
| Annual spine | CR ← FLGT ← Production |
| Discount base | Ec_IO C5 |
| Cashflow gate | `A ≤ Ec_IO!D22` |
| IRR windows | AF5:AF49; AF5:AF40; AK5:AK49 (error) |
| History | Upstream filters only |

---

## 8. GTC-001 minimum anchors

| Cell | Expected | Tol / error |
|------|----------|-------------|
| Project_NCF!AG51 | 149.557072245101 | 1e-9 |
| Project_NCF!AH51 | 78.0891606587929 | 1e-9 |
| Project_NCF!AJ51 | 5.13925728744526 | 1e-9 |
| Project_NCF!AE51 | 310.69425355464 | 1e-9 |
| Project_NCF!AF51 | 250.725376476001 | 1e-9 |
| Project_NCF!AB51 | 148.760486089522 | 1e-9 |
| Project_NCF!AC51 | 26.4540677567758 | 1e-9 |
| Project_NCF!AD51 | 42.0829559477558 | 1e-9 |
| Project_NCF!AG58 | 0.348601049838934 | 1e-9 |
| Project_NCF!AU12 | 0.348601049838934 | 1e-9 |
| Project_NCF!AU14 | **#NUM!** | expected_error / NO_VALID_IRR |
| Equity_NCF_Con!AG51 | ~73.283 | 1e-9 |
| Equity_NCF_Con!AH51 | ~38.264 | 1e-9 |
| HT_NCF_Oil!AS51 / AT51 / AV51 | as contract §11 | 1e-9 |

**Do not rewrite expected values.** Framework: `pems.gtc.compare`.

---

## 9. Deferred / non-core

| Item | Class |
|------|-------|
| Hidden NCF mirror sheets as primary surface | DEFERRED (use visible) |
| Analysis data tables / MC | DEFERRED |
| F-G12 full loan redesign | DEFERRED (include FLGT AN–AP terms in AF as GM) |
| RESULTS layout/presentation | Separate module |
| Full line-by-line HT/CIT in prose | Catalogue authority |

---

## 10. Readiness

See `docs/03_IMPLEMENTATION/PHASE1E_CR_NCF_READINESS.md`.

**Disposition:** parameter + logic contracts **READY** for implementation authorization.  
**Not:** IMPLEMENTED · NUMERICALLY VALIDATED · auto-authorize code.
