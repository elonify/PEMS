# Phase 1H — Presentation / UI Readiness Report

**Date:** 2026-08-04  
**Task type:** Specification / readiness / implementation-gate analysis **only**  
**Presentation / GUI / chart / dashboard code written:** **None**  
**Calculation engines modified:** **None**  
**Git commit under this task:** **None** (separate authorization required)

**Authority:**  
- Project Owner Phase 1H readiness directive  
- `docs/02_SPECIFICATIONS/presentation/*` (master + siblings)  
- `UI_ARCHITECTURE.md`, `CHART_SPECIFICATION.md`, `REPORT_SPECIFICATION.md`  
- Module contracts Ec_IO…RESULTS; Phase 1A–1G implementation evidence  
- `docs/workbook/semantic_mapping/CHARTS_AND_VBA.md`  
- GTC / RESULTS Equity pack  

**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**GM modified:** **No**

**Upstream calc path:** CaseInput → Ec_IO → Production → Costs → FLGT → CR/NCF → RESULTS **IMPLEMENTED**; Phase 1G GTC anchor comparison **PASS** with intermediate-path limitations **preserved**.

---

## 0. Executive decision

| Field | Value |
|-------|--------|
| **PRESENTATION SPECIFICATION READY** | **YES** (reconfirmed; presentation suite already marked READY) |
| **PRESENTATION IMPLEMENTATION READY** | **YES — controlled first slice** (see §13); full Excel chart-for-chart parity **not** claimed ready |
| **PRESENTATION IMPLEMENTED** | **NO — NOT STARTED** |
| **PRESENTATION NUMERICALLY VALIDATED** | **NOT CLAIMED** |
| **PO implementation authorized by this report** | **NO** — requires subsequent implementation directive |
| **Sensitivity / Monte Carlo** | **DEFERRED** (unchanged) |

**Do not equate:** presentation specs READY · calc IMPLEMENTED · presentation IMPLEMENTED · full-system VALIDATED.

---

## 1. Objective

Establish the **contract** between calculation engines, derived/output data, presentation models, and eventual UI/dashboard/reporting — so Phase 1H implementation (when authorized) **consumes** authoritative PEMS outputs and **does not** re-host economics.

```text
CALCULATION ENGINES (implemented)
        ↓
DERIVED / OUTPUT DATA (module Results / cell_map / CaseInput)
        ↓
PRESENTATION MODEL (ViewModels / ChartDataset / ReportDataset)  ← this gate defines
        ↓
UI / DASHBOARD / REPORTING  ← NOT implemented in Phase 1H
```

---

## 2. Validation / claim boundary (calc vs presentation)

| Claim | Status (must preserve) |
|-------|------------------------|
| RESULTS SPECIFICATION READY | **YES** |
| RESULTS IMPLEMENTED | **YES** |
| GTC-001 ANCHOR COMPARISON | **PASS** |
| PHASE 1G INTEGRATED CHAIN | **PASS** |
| RESULTS FULL INDEPENDENT NUMERICAL VALIDATION | **NOT CLAIMED** |
| PEMS-vs-GM FULL-SYSTEM VALIDATION/PARITY | **NOT CLAIMED** |
| PRESENTATION | **NOT STARTED** (this phase readiness only) |
| SENSITIVITY | **DEFERRED** |
| MONTE CARLO | **DEFERRED** |
| GOLDEN MASTER | **UNCHANGED** |

Presentation readiness is **not** granted merely because RESULTS is implemented; it rests on presentation specs + workbook evidence + data contracts below.

---

## 3. Existing workbook presentation inventory

### 3.1 Visible surfaces (30) — evidence: `PEMS_PRESENTATION_SPECIFICATION.md` §2

| Sheet | Presentation role | Evidence class |
|-------|-------------------|----------------|
| START, Checklist, Master, END | Navigation / QA / labels | L2 shell |
| Ec_IO | Case dashboard + assumptions + KPI hub | Primary **input + hub** |
| Equity Dash | Equity INPUT (C4) + loan UI | Primary **input** |
| Fiscal Terms_PIA | LAW TABLE (read-only reference) | Law browser |
| STOIIP / GIIP | Reservoir volume interface | Partial / interface |
| Production Profile, Block_Oil/Gas Data, Prod_Summary | Production schedules & summary | Schedule grids |
| Block_TC / Block_TC_Gas, Cap_Allow / Cap_Allow Gas | Cost schedules & allowances | Schedule grids |
| Royalties, FLGT | Royalty rates & front-end take | Fiscal tables |
| CR Econ | Cost recovery bridge | Detail table |
| HT_NCF_Oil, CIT_NCF_Oil, CIT_NCF_Gas, Project_NCF | Tax / NCF detail (project) | Detail schedules |
| HT/CIT Equity sheets, Equity_NCF_Con | Equity NCF detail | Detail schedules |
| **RESULTS Equity** | **Executive KPI dashboard** | Primary **output** |
| Analysis | Sensitivity presentation | **DEFERRED** (scope) |

**Hidden (8):** not user input surface — catalogue-only (`Oil Input`, `Gas Input`, `HT_NCF`, `CIT_NCF`, `Project_NCF_Con`, …).

### 3.2 Layout patterns (evidence-backed)

| Pattern | Source | PEMS implication |
|---------|--------|------------------|
| Label left / value right | Ec_IO B/C; RESULTS G / H–N | Form + KPI grid |
| Year as row axis | FLGT, Cap_Allow, NCF, Block_TC | Annual tables |
| Unit row ($mm) | Block_TC row 3 | Table header unit band |
| Multi-field column blocks | Block_Oil / Block_TC | Field selector + grid |
| Freeze panes | Ec_IO, Project_NCF, RESULTS, FLGT | Sticky headers (L2) |
| BIT vs AIT column groups | RESULTS Equity | Column grouping mandatory L1/L2 |

### 3.3 Charts (package inventory)

| Metric | Evidence |
|--------|----------|
| Chart count | **41** (`CHARTS_AND_VBA.md`, openpyxl `_charts`) |
| Analysis | 15 (sensitivity — **DEFERRED** with Analysis scope) |
| Ec_IO | 6 |
| STOIIP / GIIP | 4 each |
| Prod_Summary | 3 |
| Production Profile | 2 |
| Block_TC / Gas | 2 / 1 |
| FLGT | 1 |
| NCF Con sheets | 1 each |

**Policy:** Charts are **PRESENTATION** (series bound to ranges). Dual-axis zero alignment is **PEMS chart-engine** requirement (`CHART_SPECIFICATION.md`). Chart caches are **not** calculation authority.  
**Gap:** `WORKBOOK_MAPPING_SPECIFICATION.md` §8 still marks deep chart→template inventory as **Pending** — blocks **full** chart parity implementation, not executive KPI/table presentation.

### 3.4 VBA

No `vbaProject.bin` — no macros to port. @Risk named ranges → Monte Carlo **DEFERRED**.

---

## 4. Presentation data contract (calc → display)

### 4.1 Architecture rule

```text
UI / ViewModel
  → Application Services (validate, run, project DTOs)
    → CaseInput + module Results (ProductionResult, CostsResult, … ResultsResult)
      → cell_map / typed fields
```

- **No** openpyxl live workbook as UI model.  
- **No** reimplementation of production/costs/FLGT/CR/RESULTS formulas in UI.  
- Presentation-only transforms allowed: format fraction→%, label assembly, filter/sort view, series packaging for charts.

### 4.2 Core presentation IDs (executive / RESULTS surface)

| Pres. ID | Display name | Source module | Source field / cell | Unit | Perspective | Class |
|----------|--------------|---------------|---------------------|------|-------------|-------|
| P-ID-L2 | Country | CaseInput / Ec_IO | country / RESULTS L2 | text | case | A identity |
| P-ID-L3 | Fiscal regime | CaseInput | fiscal_regime_label | text | case | A |
| P-ID-C5 | Field | CaseInput | block_field_oil | text | case | A |
| P-ID-C8 | Equity share text | CaseInput | equity_share_company_1 | % text | equity | A |
| P-H7 | Hurdle | CaseInput | hurdle_rate | fraction→% | case | A |
| P-J7/K7 | Host/Contractor BIT NPV | ResultsResult | j7/k7 | $mm | equity BIT | A KPI |
| P-M7/N7 | Host/Contractor AIT NPV | ResultsResult | m7/n7 | $mm | equity AIT | A KPI |
| P-K8/N8 | IRR BIT/AIT | ResultsResult | k8/n8 | fraction or NO_VALID_IRR | equity | A KPI |
| P-K9–K11/N9–N11 | PVR/PI/GRR | ResultsResult | … | ratio / % | equity | B |
| P-J12–N13 | Take stats | ResultsResult | … | fraction | BIT/AIT | B |
| P-K14/N14 | Disc. payout | ResultsResult | k14/n14 | years | BIT/AIT | A |
| P-H15 | FLI | ResultsResult | h15 | fraction | AIT | B |
| P-H16–M18 | Equity costs | ResultsResult | … | $ (label $MM) | equity | A/B |
| P-J16–J18 | Equity revenues | ResultsResult | … | $ (label $MM) | equity | A |
| P-H19–M21 | Unit costs | ResultsResult | … | $/boe | equity | B |
| P-H22–H26 | Royalties / ERR | ResultsResult | … | $mm / % | equity | A/B |
| P-J22–J25 | Taxes | ResultsResult | … | $mm | equity | A/B |
| P-N22–N24 | Production equity | ResultsResult | … | MMbbls / Mmboe | equity | A |
| P-M23 | Gas Bscf text | ResultsResult | m23 | text | equity | C |

Full RESULTS cell catalogue: `RESULTS_PARAMETER_CONTRACT.md` §2–3 + Phase 1F/1G evidence.

### 4.3 Module annual tables (presentation consumers)

| Surface | Source DTO | Series examples | Unit |
|---------|------------|-----------------|------|
| Production | ProductionResult | oil_daily/annual, gas_*, V47/Y47–Y50 | mb/d, mmbbls, bscf, Mmboe |
| Costs | CostsResult | opex/capex streams, FI/FL/FK hubs | $mm |
| FLGT | FlgtResult | W/X/Y, AB/AC/AD, ERR AM | $mm, fraction |
| CR/NCF | CrNcfResult | AE/AF/AG/AH annual, AJ, IRR | $mm, years, IRR |
| Ec_IO pure | EcIoResult / CaseInput | drivers C4–C26, G18–G26 | mixed |

---

## 5. KPI inventory (classification)

| KPI / group | Example cells | Classification | Rationale |
|-------------|---------------|----------------|-----------|
| Identity strip | L2,L3,C5–C8,L5 | **A** Primary dashboard | Always on RESULTS Equity |
| Hurdle | H7 | **A** | Context for NPV |
| NPV BIT/AIT host/contractor | J7,K7,M7,N7 | **A** | Core economics |
| IRR BIT/AIT | K8,N8 | **A** | Core; error-state aware |
| Payout BIT/AIT | K14,N14 | **A** | Core |
| Gross revenue equity | J18 | **A** | Headline |
| Total royalty / ERR | H25,H26 | **A** / **B** | Fiscal headline |
| Total tax | J25 | **A** | Fiscal headline |
| Equity prod oil/gas/total | N22–N24 | **A** | Volume headline |
| PVR / PI / GRR | K9–K11,N9–N11 | **B** Secondary | On RESULTS; less primary than NPV/IRR |
| Take undisc/disc | J12–N13 | **B** | Fiscal detail |
| FLI | H15 | **B** | Ratio |
| PV/undisc OPEX/CAPEX/TC | H16–M18 | **B** | Cost block |
| Oil/gas revenue lines | J16,J17 | **B** | Supporting revenue |
| Unit costs | H19–M21 | **B** | Unit economics |
| Royalty components | H22–H24 | **C** Detailed | Table/detail |
| Tax components HT/CIT/Etx | J22–J24 | **C** Detailed | Table/detail |
| Gas Bscf text | M23 | **C** | Supporting text |
| Project_NCF full annual AE/AF | Project_NCF cols | **C** / **D** | Cash-flow view / chart series |
| Production annual rates | Prod_Summary T/W | **C** / **D** | Schedule + charts |
| Ec_IO hub G3–G15 | Ec_IO | **E** / **B** | Hub mirrors; prefer RESULTS as primary executive |
| Analysis tornado / data tables | Analysis | **F** Not required now | **DEFERRED** sensitivity |
| Monte Carlo distributions | @Risk heritage | **F** | **DEFERRED** |

**BIT vs AIT:** preserve workbook labels and column groups; do not rename for convenience (A1 non-blocking ambiguity retained).

---

## 6. Chart inventory

### 6.1 Mandatory framework (not optional when charts ship)

| Requirement | Source |
|-------------|--------|
| ChartDataset-only data path | CHART_SPECIFICATION |
| Dual-axis zero alignment algorithm | CHART_SPECIFICATION §6 (L1/L2) |
| No economics inside chart code | CHART_SPECIFICATION § constraints |
| Dynamic rescale on data change | CHART_SPECIFICATION §5 |

### 6.2 Evidence-backed families (GM package)

| Chart family | Approx. count / sheets | Mandatory now? | Notes |
|--------------|------------------------|----------------|-------|
| Sensitivity / Analysis | 15 on Analysis | **Deferred** | Bound to Analysis scope + SCOPE register |
| Ec_IO I/O | 6 | **Optional first-slice** after series map | Presentation only |
| Reservoir STOIIP/GIIP | 8 | **Deferred** if reservoir partial | Interface readiness limited |
| Production | Prod_Summary 3 + PP 2 | **Candidate** post series map | Production engine ready |
| Costs Block_TC | 3 | **Candidate** post series map | Costs ready |
| FLGT | 1 | **Candidate** | FLGT ready |
| NCF Con | ~3 | **Candidate** | CR/NCF ready with intermediate path note |

### 6.3 Per-chart template fields (to complete at implementation)

For each chart when mapped from `CHART_INVENTORY.csv` / openpyxl:

- chart_id, purpose, x-axis, y-axis (primary/secondary), series, units, granularity, project/equity, BIT/AIT, oil/gas, source DTO path, filters, annual/cumulative, mandatory vs deferred, dual-axis flag.

**Do not invent charts** “because useful.” Only map evidenced Excel charts or REPORT/UI template requirements.

### 6.4 Chart readiness gap (non-blocking for KPI UI)

Deep series-reference mapping and ChartDataset builders are **not** complete in WORKBOOK_MAPPING.  
→ **Chart implementation** requires a sub-gate inventory completion; **RESULTS KPI dashboard** does not.

---

## 7. Table inventory

| Table ID | Purpose | Rows | Columns | Units | Perspective | Source |
|----------|---------|------|---------|-------|-------------|--------|
| T-CASE | Case assumptions form | fields | label, value, unit | mixed | case | CaseInput / Ec_IO |
| T-LAW | Fiscal law rates | law rows | label, rate | % | law (read-only) | Fiscal Terms_PIA |
| T-PROD-ANN | Annual production | years | oil/gas daily & annual, cum | mb/d, mmbbls, bscf | project | ProductionResult |
| T-PROD-SUM | Production summary KPIs | scalars | V47,Y47–Y50,AF26 | mmbbls, Mmboe, years | project | ProductionResult |
| T-COST-ANN | Annual costs | years | OPEX/CAPEX categories | $mm | project | CostsResult / schedules |
| T-COST-HUB | Cost hubs | scalars | N16–S18, FI/FL/FK | $mm | project | CostsResult |
| T-FLGT-ANN | Annual fiscal | years | rev, royalties, take | $mm | project | FlgtResult |
| T-FLGT-TOT | Fiscal totals | scalars | W51…AM51 | $mm / % | project | FlgtResult |
| T-CR | CR Econ bridge sample | years | G–U style | $mm | project | CrNcfResult.cr_years |
| T-NCF | Project NCF annual | years | B, AE–AJ | $mm / years | project | CrNcfResult |
| T-EQ-NCF | Equity NCF summary | scalars | AG51,AH51,AJ51 | $mm / years | equity | CrNcfResult |
| T-RESULTS-KPI | Executive KPI matrix | KPI rows | BIT/AIT cols | mixed | equity | ResultsResult |
| T-VALIDATION | GTC compare summary | cells | expected/actual/status | — | QA | gtc.compare (later UI) |

**Order:** year ascending calendar (workbook A-column order). Totals row where GM has row 51 style totals.

---

## 8. User input / selector contract

### 8.1 Calculation inputs (CaseInput — not invented)

| Control | Source | Type |
|---------|--------|------|
| Equity share company 1 | Equity Dash!C4 | INPUT % |
| Asset analysis type | Ec_IO C4 | enum DV |
| Project start year | Ec_IO C5 | year |
| Production days | Ec_IO C7 | days |
| Oil / gas prices, escalator, hurdle | Ec_IO C12–C17 | drivers |
| Terrain, gas util, licence, PFS, country, regime | Ec_IO G20–G26 | enums / text |
| Block field oil | Ec_IO G18 | field selector |
| PP mode, rates, RF, GOR, … | Production Profile | PP params |
| Cost schedules / CA rates | Cap_Allow / Block_TC | schedules |
| Project equity total C6 | Equity Dash | structural |

**C5 equity remainder = DERIVED** — display only, not independent input.

### 8.2 Presentation filters / view controls (no new CaseInput)

| Control | Nature |
|---------|--------|
| Active scenario / run selection | View over saved runs |
| Module navigation (Prod / Costs / Fiscal / Results) | Shell navigation |
| Project vs equity view toggle | **View projection** over existing DTOs (do not recalculate) |
| BIT vs AIT column visibility | View filter on RESULTS groups |
| Year range zoom on tables/charts | View filter |
| Field selection for multi-field grids | Maps to existing block_field / cost_mode_field |
| Import vs manual entry path | Same CaseInput validation path |

**Do not add CaseInput fields for UI convenience.**

---

## 9. Presentation vs calculation boundary

### MUST NOT be calculated in UI

Production, costs, royalties, FLGT, CR/NCF, taxes, NPV, IRR, payout, unit economics, ERR, take statistics, equity scaling economics (except display of already-scaled ResultsResult fields).

### Allowed presentation transforms

| Transform | Example |
|-----------|---------|
| Format | fraction → `0.00%`, $mm accounting 2 dp |
| Label compose | “Equity Share =49%” from C4 |
| Series package | ChartDataset from annual maps |
| Filter/sort | Year window |
| Error token display | `NO_VALID_IRR` → unavailable UI state |
| Projection | Project NPV × display equity **only if** using already-validated DTO fields — prefer precomputed ResultsResult |

---

## 10. Error / edge-case presentation contract

| Condition | Display behavior (spec; not implemented) |
|-----------|------------------------------------------|
| `NO_VALID_IRR` / `#NUM!` | Explicit unavailable/error state; **never** 0% success |
| Zero production / revenue | Show 0 with unit; ERR/unit-cost may be undefined — show unavailable if div-by-zero |
| Negative cash flow | Accounting minus/parentheses; red optional L3 |
| Missing series | Empty chart/table with message; no fabricated points |
| Intermediate-path BIT/CIT | May display PEMS Results values; UI should not claim “independent HT engine” |
| Deferred Analysis/MC | Hide or disable with “not in scope” — do not fake charts |
| Validation failures | Block run / show ValidationResult (UI_ARCHITECTURE §7) |

---

## 11. Units / formatting contract

Authoritative: `UNIT_AND_CURRENCY_SPECIFICATION.md`, `NUMBER_FORMAT_SPECIFICATION.md`.

| Domain | Store | Display |
|--------|-------|---------|
| Money economics | $mm numeric | Accounting 2 dp; zero as `-` where Excel does |
| RESULTS cost/revenue lines | numeric | `$` accounting + $MM labels |
| Unit costs | $/boe | currency 2 dp |
| Oil price | $/bbl | number |
| Gas price | $/Mscf | number |
| Rates / IRR / take / ERR | fraction | `0%` / `0.0%` / `0.00%` per field class |
| PVR / PI | number | `0.00` |
| Payout | years | `#,##0.00` |
| Production | mb/d, mmbbls, bscf, Mmboe | labels mandatory |
| Currency | USD only | no FX invent |

**L1 semantic** units/scales; **L3** exact Excel format strings optional.

---

## 12. Navigation / information architecture

### Recommended structure (best supported by 30 visible sheets + UI_ARCHITECTURE)

```text
1. Home / Dashboard          ← RESULTS Equity KPI surface + recent runs
2. Case / Assumptions        ← Ec_IO + Equity C4 + enums
3. Law Table (read-only)     ← Fiscal Terms_PIA
4. Production                ← Profile / Block / Prod_Summary
5. Costs                     ← Block_TC / Cap_Allow
6. Fiscal / Royalties        ← Royalties + FLGT
7. Economics / Cash Flow     ← CR Econ + Project_NCF (+ equity detail)
8. Results                   ← RESULTS Equity (full KPI)
9. Validation / Compare      ← GTC / run validation (QA)
10. Reports (export)         ← REPORT_SPEC templates
```

**Deferred nodes:** Analysis (sensitivity), Monte Carlo, multi-project portfolio.

### Alternatives considered

| Alternative | Why not primary |
|-------------|-----------------|
| Excel sheet-for-sheet clone | L3 pixel parity out of scope; toolkit open |
| Single-page only | Contradicts multi-sheet evidence |
| Analysis-first IA | Scope deferred |

---

## 13. Implementation readiness

### READY for controlled first-slice implementation (when PO authorizes)

1. Application shell + navigation (§12)  
2. CaseInput forms (Ec_IO + Equity C4) with INPUT/DERIVED/LAW visual language  
3. RESULTS Equity KPI dashboard from `ResultsResult.cell_map` / DTO  
4. Annual tables for Production, Costs, FLGT, Project NCF from module DTOs  
5. Format/unit/error presentation per §10–11  
6. Services-only access (UI_ARCHITECTURE)  

### NOT READY / deferred without further work

| Item | Status |
|------|--------|
| Full 41-chart series→template map | Pending deep inventory |
| Analysis / sensitivity UI | DEFERRED |
| Monte Carlo UI | DEFERRED |
| Reservoir STOIIP/GIIP full product | Interface partial |
| Pixel-perfect Excel theme/fonts | L3 optional |
| Full-system presentation parity claim | NOT CLAIMED |

### Blocking for “full presentation product complete”

None for **first-slice** KPI+forms+tables.  
**Chart sub-gate** required before shipping dual-axis production/NCF charts as complete.

### Decision

# **PRESENTATION SPECIFICATION READY = YES**  
# **READY FOR IMPLEMENTATION (FIRST SLICE) = YES** — subject to **separate PO implementation authorization**  
# **PRESENTATION IMPLEMENTED = NO**

---

## 14. Presentation test strategy (plan only)

| ID | Test | Purpose |
|----|------|---------|
| PT01 | Output-to-UI identity | RESULTS/Case fields map 1:1 to DTO |
| PT02 | Unit/format | fraction vs %; $mm vs $/boe |
| PT03 | Selector propagation | Field/enum edits hit CaseInput only |
| PT04 | Error-state | NO_VALID_IRR not shown as 0% |
| PT05 | Annual-series integrity | Year order and lengths match DTO |
| PT06 | Chart-source integrity | ChartDataset values == DTO series (when charts built) |
| PT07 | KPI source traceability | Each A/B KPI has module field id |
| PT08 | No-calc-in-UI | Static/lint or architecture test: UI layer imports no calc modules for economics |
| PT09 | Regression | Prior calc GTC still pass (targeted; session GM cache) |
| PT10 | GM presentation compare | Optional L2: format tokens / labels vs audit extract — not full-suite mandatory |

**Do not** require full `pytest tests` solely for presentation readiness.

---

## 15. Traceability matrix (material)

| Presentation requirement | Trace source |
|--------------------------|--------------|
| RESULTS KPI dashboard | RESULTS_PARAMETER_CONTRACT; RESULTS Equity sheet; Phase 1F/1G |
| Equity C4 INPUT | EQUITY_DASH_SHARE_INPUT; INPUT_OUTPUT_VISUAL_LANGUAGE |
| Law table non-editable | FISCAL_TERMS_PIA_LAW_TABLE |
| $mm / % / $/boe conventions | UNIT_AND_CURRENCY; NUMBER_FORMAT |
| Dual-axis zero align | CHART_SPECIFICATION §6 |
| No calc in UI | UI_ARCHITECTURE §2; CHART_SPEC constraints |
| 30 visible sheets | PEMS_PRESENTATION_SPECIFICATION §2; PRESENTATION_AUDIT_EXTRACT |
| 41 charts inventory | CHARTS_AND_VBA.md |
| Analysis deferred | SCOPE / PERIPHERAL_SCOPE_REGISTER; Analysis data tables |
| AU14 / NO_VALID_IRR display | DATA_MODEL; RESULTS/CR contracts; GTC EXP-001 |
| Report types | REPORT_SPECIFICATION |
| Module tables | Production/Costs/FLGT/CR contracts + cell_map |

---

## 16. Deferred items (explicit)

| Item | Bound |
|------|-------|
| Sensitivity / Analysis UI & 15 Analysis charts | DEFERRED |
| Monte Carlo / @Risk | DEFERRED |
| Full chart-for-chart parity before series map | Deferred / sub-gate |
| Unsupported scenario controls | Out of scope |
| New calculation engines | Out of scope |
| Advanced viz not in GM | Out of scope |
| Presentation code in this phase | **None** |

Ambiguities retained: theme colour hex instability; openpyxl DV gaps; BIT/AIT naming (A1); intermediate-path calc claims (Phase 1G).

---

## 17. Three-state control (end state)

| State | Value |
|-------|--------|
| **PRESENTATION SPECIFICATION READY** | **YES** |
| **PRESENTATION IMPLEMENTED** | **NO** |
| **PRESENTATION NUMERICALLY VALIDATED** | **NOT CLAIMED** |
| RESULTS IMPLEMENTED | **YES** |
| RESULTS validation claim | **Phase 1G limitation preserved** (GTC anchor PASS; full independent NOT CLAIMED) |
| GOLDEN MASTER | **UNCHANGED** |

---

## 18. Golden Master integrity

| Check | Result |
|-------|--------|
| Expected SHA | `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA` |
| Pre-readiness | **MATCH** |
| Post-readiness | **MATCH** (docs only; GM not opened for write) |
| GM modified | **NO** |

---

## 19. Recommended next gate

| Gate | Authorization required |
|------|------------------------|
| **Phase 1H presentation implementation (first slice)** | Explicit PO directive |
| Chart series mapping sub-gate | Before full chart delivery |
| Sensitivity / Monte Carlo | Separate deferred authorizations |
| Git checkpoint of Phase 1H docs | Optional separate PO instruction |

---

## 20. STOP

```text
PRESENTATION SPEC READY = YES
PRESENTATION IMPLEMENTED = NO
PRESENTATION VALIDATED = NOT CLAIMED
No GUI · No charts code · No sensitivity · No MC · No calc changes · No GM change · No commit
```

**STOP.** Await Project Owner implementation or checkpoint authorization.
