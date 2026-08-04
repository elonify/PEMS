# RESULTS Parameter / Output Contract — Implementation Readiness

**Status:** **READY** (dashboard/KPI presentation contract only — not calculation VALIDATED)  
**Active GM SHA (approved):** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Module:** M-CP-06 / M08 RESULTS Equity dashboard  
**GM modified:** **No**  
**Calculation code under this task:** **None**

**Do not reopen:** GM approval CLOSED · Equity C4 INPUT · C5 DERIVED · AU14 expected · all upstream READY modules · Fiscal LAW TABLE · ADR-0010  

**Upstream contracts:** Ec_IO · Production · Costs · FLGT/Royalties · CR/NCF · Fiscal Terms_PIA  

**Evidence:** catalogue · `RESULTS_EVIDENCE_EXTRACT.json` · GTC-001 KPI pack · `DATA_MODEL.md` IRR contract · `GTC_FRAMEWORK.md`  

**Primary sheet:** `RESULTS Equity` (visible; 62 formulas / 107 nonempty on extract)  
**Related hub:** `Ec_IO` dashboard mirrors (consumer of Project_NCF / FLGT / Cap_Allow — not RESULTS inputs)

---

## 0. Role of RESULTS

RESULTS is primarily an **output / presentation / KPI aggregation layer**.

| Class | On RESULTS Equity |
|-------|-------------------|
| Genuine CaseInput | **None** (equity share displayed from Equity Dash!C4; not entered here) |
| Formula-derived KPI | Almost all metric cells |
| Labels / identity | Text headers, context fields |
| Display-only text | e.g. Equity Share =49%, gas Bscf text M23 |

Developers implement RESULTS as a **read model** over CR/NCF, FLGT, Production, Costs, Equity — not a second economic engine with independent business rules.

---

## 1. Architecture / dependency

```text
Ec_IO (identity, hurdle, life, cost hub N/S series)
Production (Prod_Summary V47/Y47/Y49/Y50)
Costs (via Ec_IO N16–S18 PV/undisc TC)
FLGT (AB51/AC51/AD51 royalties; revenues via Ec_IO P16/P17)
CR/NCF:
  · HT_NCF_Oil Equity (BIT NPV, IRR series, take, HT, payout)
  · CIT_NCF_* Equity (CIT, education tax)
  · Equity_NCF_Con (AIT NPV, IRR, take, payout)
Equity Dash!C4  ──share scale──┐
        ↓                      │
   RESULTS Equity  ◄───────────┘
```

**Indirect:** Production → volumes → FLGT/CR/NCF → RESULTS.  
**Direct:** Equity Dash!C4 multiplies many $MM and volume displays.

---

## 2. Context / identity outputs

| Cell | Formula / value | Meaning | Class | Unit/format |
|------|-----------------|---------|-------|-------------|
| L2 | `=Ec_IO!R2` | Country | DERIVED display | text |
| L3 | `=Ec_IO!R3` | Fiscal regime label | DERIVED | text |
| C5 | `=Ec_IO!I5` | Field name | DERIVED | text |
| L5 | `=Ec_IO!R5` | PFS / PSC-SC | DERIVED | text |
| C6 | `=Ec_IO!G22` | Licence / New Acreage | DERIVED | text |
| C7 | `=Ec_IO!G20` | Terrain | DERIVED | text |
| C8 | `="Equity Share ="&TEXT('Equity Dash'!$C$4,"0%")` | Equity share display | DERIVED from **INPUT** C4 | text % |

---

## 3. Economic KPI inventory (material)

### 3.1 NPV / discount (BIT vs AIT columns)

| Cell | Label context | Formula | GM value (GTC) | Unit / format | Upstream |
|------|---------------|---------|----------------|---------------|----------|
| H7 | Disc. rate | `=Ec_IO!C15` | 0.15 | 0.00% | Ec_IO hurdle |
| J7 | Host Govt BIT NPV | `='HT_NCF_Oil Equity'!AS51` | 37.2107219837393 | $mm, #,##0.00 | CR/NCF equity HT |
| K7 | Contractor BIT NPV | `='HT_NCF_Oil Equity'!AT51` | 73.018201942495 | $mm | CR/NCF equity HT |
| M7 | Host Govt AIT NPV | `=Equity_NCF_Con!AG51` | 73.2829654000993 | $mm | Equity NCF disc. host |
| N7 | Contractor AIT NPV | `=Equity_NCF_Con!AH51` | 38.2636887228085 | $mm | Equity NCF disc. contractor |

**Category:** project/equity economics · NPV  

### 3.2 IRR / profitability

| Cell | Label | Formula | GM value | Format | Upstream / notes |
|------|-------|---------|----------|--------|------------------|
| K8 | IRR (BIT) | `=IRR('HT_NCF_Oil Equity'!AR5:AR49)` | 0.504693506064976 | 0.00% | Equity HT CF series |
| N8 | IRR (AIT) | `=IRR(Equity_NCF_Con!AF5:AF49)` | 0.348601049838934 | 0.00% | Equity contractor CF |
| K9 | PVR BIT | `=K7/H18` | 0.421063315742914 | 0.00 | NPV / PV TC |
| N9 | PVR AIT | `=N7/H18` | 0.220649580756165 | 0.00 | |
| K10 | PI BIT | `=1+K9` | 1.42106331574291 | 0.00 | |
| N10 | PI AIT | `=1+N9` | 1.22064958075617 | 0.00 | |
| K11 | GRR BIT | `=K10^(1/(Ec_IO!$C$6))*(1+Ec_IO!$C$15)-1` | 0.177259134616414 | 0.00% | life C6, hurdle C15 |
| N11 | GRR AIT | `=N10^(1/(Ec_IO!$C$6))*(1+Ec_IO!$C$15)-1` | 0.165388086566337 | 0.00% | |

**Category:** IRR · PVR · PI · GRR  

### 3.3 Take statistics & payout & FLI

| Cell | Meaning | Formula | GM value | Format |
|------|---------|---------|----------|--------|
| J12 | Undisc. host take BIT | HT equity AQ/(AQ+AR) | 0.275365415622534 | 0.0% |
| K12 | Undisc. contractor take BIT | `=1-J12` | 0.724634584377466 | 0.0% |
| M12 | Undisc. host take AIT | Equity AE/(AE+AF) | 0.553408247477352 | 0.0% |
| N12 | Undisc. contractor AIT | `=1-M12` | 0.446591752522648 | 0.0% |
| J13 | Disc. host take BIT | `=J7/(J7+K7)` | 0.337576750804906 | 0.0% |
| K13 | Disc. contractor BIT | `=1-J13` | 0.662423249195094 | 0.0% |
| M13 | Disc. host AIT | `=M7/(M7+N7)` | 0.656971434744716 | 0.0% |
| N13 | Disc. contractor AIT | `=1-M13` | 0.343028565255284 | 0.0% |
| K14 | Disc. payout BIT | HT equity AV51 | 4.87387900694515 | years #,##0.00 |
| N14 | Disc. payout AIT | Equity_NCF_Con!AJ51 | 5.13925728744526 | years |
| H15 | FLI | `=M13/M12-1` | 0.187137050702524 | 0.00000 |

**Category:** fiscal take · payout · FLI  

### 3.4 Costs / revenues (equity-scaled)

| Cell | Meaning | Formula | GM value | Format |
|------|---------|---------|----------|--------|
| H16 | PV OPEX × equity | `=Ec_IO!N16*'Equity Dash'!$C$4` | 103.391391515252 | $ #,##0.00 |
| M16 | Undisc OPEX × equity | `=Ec_IO!S16*C4` | 204.919631874736 | $ |
| H17 | PV CAPEX × equity | `=Ec_IO!N17*C4` | 70.0224377414318 | $ |
| M17 | Undisc CAPEX × equity | `=Ec_IO!S17*C4` | 85.75 | $ |
| H18 | PV TC | `=H16+H17` | 173.413829256684 | $ |
| M18 | Undisc TC | `=M16+M17` | 290.669631874736 | $ |
| J16 | Oil revenue × equity | `=Ec_IO!P16*C4` | 538.94584168118 | $ |
| J17 | Gas revenue × equity | `=Ec_IO!P17*C4` | 26.9672237060786 | $ |
| J18 | Gross revenue | `=SUM(J16:J17)` | 565.913065387258 | $ |

Labels G16–G18 pull Ec_IO M16–M18 text (`PV@15% of …`).

### 3.5 Unit economics

| Cell | Meaning | Formula | GM value |
|------|---------|---------|----------|
| H19 | Unit CAPEX PV $/boe (equity path) | `=H16/Prod_Summary!$Y$50/'Equity Dash'!$C$4` | 8.00847019384067 |
| M19 | Unit CAPEX undisc | `=M16/Y50/C4` | 15.8726247896521 |
| H20 / M20 | Unit OPEX | H17/M17 over Y50/C4 | 5.423… / 6.642… |
| H21 / M21 | Unit TC | H18/M18 over Y50/C4 | 13.432… / 22.515… |

**Unit:** $/Boe (label “S/Boe”). **Scale:** absolute $ (Excel currency format), not $mm.

### 3.6 Royalties, taxes, production (equity-scaled)

| Cell | Meaning | Formula | GM value |
|------|---------|---------|----------|
| H22 | Oil royalty $MM | `=FLGT!AB51*C4` | 30.0437706813062 |
| H23 | Gas royalty $MM | `=FLGT!AC51*C4` | 0.674180592651965 |
| H24 | Price royalty $MM | `=FLGT!AD51*C4` | 0 |
| H25 | Total royalty $MM | `=SUM(H22:H24)` | 30.7179512739582 |
| H26 | ERR | `=H25/J18` | 0.0542803358903504 (0.00%) |
| J22 | HT $MM | HT_NCF_Oil Equity!AO51 | 20.6206484144003 |
| J23 | CIT $MM | CIT Oil+Gas Equity AF51 | 72.8926381838659 |
| J24 | Etx $MM | CIT Equity AG51 sum | 12.9624932008202 |
| J25 | Total tax $MM | `=SUM(J22:J24)` | 106.475779799086 |
| N22 | Oil prod MMbbls × equity | `=Prod_Summary!V47*C4` | 10.7789168336236 |
| N23 | Gas Mmboe × equity | `=Prod_Summary!Y49*C4` | 2.13133806059713 |
| M23 | Gas Bscf text | TEXT(Y47*C4) | "(12.37 Bscf)" |
| N24 | Total Mmboe | `=N22+N23` | 12.9102548942207 |

---

## 4. Equity treatment (closed)

| Rule | Specification |
|------|----------------|
| Share input | Equity Dash!C4 only (**INPUT**, GTC 0.49) |
| C5 | DERIVED = C6−C4 — not RESULTS input |
| RESULTS use | Multiply $MM fiscal/revenue/cost displays and volumes by C4; unit costs **divide** by C4 after scaling numerator (see H19) |
| Display | C8 text shows share percent |

---

## 5. IRR / expected-error semantics

| Location | Condition | PEMS representation |
|----------|-----------|---------------------|
| **Project_NCF!AU14** | `=IRR(AK5:AK49)` → Excel **`#NUM!`** when no sign change | **`NO_VALID_IRR`** / `NO_SIGN_CHANGE` (DATA_MODEL + GTC EXP-001) — **not** a numeric golden |
| RESULTS!N8 | `=IRR(Equity_NCF_Con!AF5:AF49)` | Numeric on GTC (~34.86%) when series valid |
| RESULTS!K8 | `=IRR(HT_NCF_Oil Equity!AR5:AR49)` | Numeric on GTC (~50.47%) when series valid |

**Rules:**

1. Do **not** invent IRR for AU14-class no-sign-change cases.  
2. Do **not** map `#NUM!` to 0, NaN-as-success, or blank success.  
3. RESULTS IRR cells that Excel evaluates numerically are ordinary float goldens (tolerance 1e-9 policy).  
4. If a RESULTS IRR series ever has no sign change, surface **NO_VALID_IRR** consistently with AU14 policy.

---

## 6. Units / currency / formats (observed Excel)

| Convention | Observed |
|------------|----------|
| Money KPIs (NPV, revenue, royalty, tax, costs) | Accounting formats `_("$"* #,##0.00_…)` or `_-* #,##0.00_-…` — **two decimal places** |
| Labels | Often “$ MM” / “$MM” for million dollars presentation |
| Rates (IRR, take, ERR, hurdle, GRR) | `0.00%` or `0.0%` or `0.00000` (FLI) |
| Ratios (PVR, PI) | `0.00` |
| Payout years | `#,##0.00` |
| Negatives | Accounting parentheses / minus per Excel format |
| Zeros | Format shows `"-"` placeholder in some accounting formats |
| Production | MMbbls, Mmboe, Bscf text |
| Unit costs | $/Boe, currency format |

PEMS UI should **match workbook presentation intent** (scale labels $MM where labeled; store SI/internal values consistently with CR/NCF $mm series).

---

## 7. Classification summary

| Kind | Examples |
|------|----------|
| **OUTPUT KPI** | J7–N14, H15–H26, J16–J25, H19–H21, N22–N24 |
| **DERIVED identity** | L2, L3, C5–C8, L5 |
| **LABEL** | G7–G26, column headers |
| **INPUT on RESULTS sheet** | **None** |
| **Upstream INPUT consumed** | Equity Dash!C4 |

---

## 8. GTC comparison points

### A. Ingestion (not RESULTS-owned)
CaseInput + equity C4 — see Ec_IO / Equity contracts.

### B. Module-level (RESULTS cells vs GM cache)
Primary pack: all **RESULTS Equity** rows in  
`Validation_Datasets/expected_outputs/GTC-001_kpi_and_intermediates.csv` (**63** KPI rows).

**Highest-value points:**

| Cell | Expected | Role |
|------|----------|------|
| N7 | 38.2636887228085 | Contractor AIT NPV |
| M7 | 73.2829654000993 | Host AIT NPV |
| J7 / K7 | 37.210… / 73.018… | BIT NPVs |
| N8 | 0.348601049838934 | AIT IRR |
| K8 | 0.504693506064976 | BIT IRR |
| N14 | 5.13925728744526 | AIT payout |
| H26 | 0.0542803358903504 | ERR |
| J18 | 565.913065387258 | Gross revenue equity |
| H25 | 30.7179512739582 | Total royalty equity |
| J25 | 106.475779799086 | Total tax equity |
| H18 / M18 | 173.414… / 290.670… | PV / undisc TC equity |
| H19–H21, M19–M21 | unit costs | Unit economics |

### C. End-to-end
Full engine run → compare RESULTS pack + Project_NCF AU14 condition + upstream GTC points.  
**Tolerance:** float abs/rel 1e-9; text exact; **AU14 exact NO_VALID_IRR / #NUM! condition**.  
**Status:** comparison **contract only** — validation **not claimed**.

---

## 9. Dependency order into RESULTS

```text
1. CaseInput + law table
2. Production
3. Costs
4. FLGT / Royalties
5. CR Econ → HT/CIT → Project_NCF
6. Equity-scaled NCF sheets (× C4)
7. Ec_IO hub cost/revenue aggregates (N16–S18, P16/P17)
8. RESULTS Equity formulas (pure aggregation / ratios / IRR on equity series)
```

**Circularity:** Ec_IO displays some Project_NCF/FLGT KPIs; RESULTS pulls Ec_IO cost labels/values. Implement as **post-NCF dashboard**, not iterative solve.  
**No proven circular requirement** for RESULTS-only cells beyond Excel formula graph.

---

## 10. Edge conditions

| Condition | RESULTS behavior |
|-----------|------------------|
| Zero gross revenue J18 | ERR H26 division — Excel may error/zero; match GM cache |
| Zero equity C4 | Many $MM → 0; unit costs divide by C4 — **avoid C4=0** or match Excel |
| IRR no sign change on equity series | Surface NO_VALID_IRR if Excel would #NUM! |
| Project AU14 | Not on RESULTS sheet; still GTC E2E condition |
| Missing upstream | Fail closed before RESULTS if CaseInput invalid |

---

## 11. Readiness gate

| # | Criterion | Met? |
|---|-----------|------|
| 1 | Outputs inventoried | **Yes** §2–3 |
| 2 | Output semantics documented | **Yes** |
| 3 | Upstream dependencies mapped | **Yes** §1 |
| 4 | Units documented | **Yes** §6 |
| 5 | Currency/scale documented | **Yes** |
| 6 | Number-format requirements documented | **Yes** §6 |
| 7 | Equity treatment documented | **Yes** §4 |
| 8 | IRR expected-error treatment documented | **Yes** §5 |
| 9 | GTC comparison points identified | **Yes** §8 |
| 10 | Derived/output classification complete | **Yes** §7 |
| 11 | Dependency order specified | **Yes** §9 |
| 12 | Ambiguities explicit | **Yes** §12 |
| 13 | No undocumented calc assumptions | **Yes** |
| 14 | No GM modification | **Yes** |
| 15 | Contract sufficient for controlled implementation | **Yes** |

# **RESULTS = READY** (specification readiness)

### Three-state distinction (do not conflate)

| State | Meaning | RESULTS status |
|-------|---------|----------------|
| **Specification READY** | Contract sufficient for controlled coding | **YES — READY** |
| **Implementation READY** | Python module coded and unit-tested | **NO — NOT STARTED** |
| **Numerical VALIDATED** | PEMS-vs-GM GTC compare passed | **NO — NOT CLAIMED** |

**Means:** Spec sufficient to implement RESULTS dashboard as KPI consumer of READY modules.  
**Does not mean:** numerical PEMS-vs-GM VALIDATED or calculation parity.  
**Does not auto-start** calculation implementation of RESULTS formulas beyond scaffold packages.

### Inventory counts (evidence extract)

| Item | Count |
|------|------:|
| Nonempty cells (RESULTS Equity) | 107 |
| Formula cells (formula groups / KPI formulas) | **62** |
| Label/text cells | 45 |
| CaseInput fields on RESULTS sheet | **0** |
| Upstream INPUT consumed | **1** (Equity Dash!C4) |
| GTC-001 KPI comparison points (RESULTS Equity) | **63** |

---

## 12. Ambiguities (scoped)

| Item | Note |
|------|------|
| BIT vs AIT naming | Workbook labels Host/Contractor BIT $MM vs AIT $MM; BIT←HT equity, AIT←Equity_NCF_Con |
| Unit cost formula divides by C4 after equity-scaling numerator | Preserve exact Excel formula order |
| Ec_IO dashboard vs RESULTS Equity | Two surfaces; RESULTS Equity is primary RESULTS module sheet |
| Full chart dual-axis | CHART_SPECIFICATION separate; not blocking RESULTS KPI contract |

---

## 13. Traceability

```text
RESULTS Equity cell
  → formula (catalogue)
  → upstream sheet/module (CR/NCF, FLGT, Ec_IO, Production, Equity)
  → category (§3)
  → GTC expected (KPI pack)
  → PEMS ResultsDTO field
```
