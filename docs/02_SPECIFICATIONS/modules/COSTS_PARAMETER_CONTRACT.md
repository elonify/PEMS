# Costs / Capital Allowance Contract — Implementation Readiness

**Status:** **READY** (cost specification / interface contract only — not calculation VALIDATED)  
**Active GM SHA (approved):** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Module:** M-CP-03 / M05 Cost / Capital Allowance  
**GM modified:** **No**  
**Calculation code under this task:** **None**

**Do not reopen:** GM approval · Equity INPUT · Fiscal LAW TABLE · Ec_IO READY · Production READY · 829/829 · AU14 · ADR-0010  

**Upstream contracts:**  
- `EC_IO_PARAMETER_CONTRACT.md`  
- `PRODUCTION_PROFILE_CONTRACT.md`  
- `FISCAL_TERMS_PIA_LAW_TABLE.md` (capital allowance **rates** as law; Cap_Allow hosts application schedule)  

**Evidence:** `docs/workbook/catalogue/` · `COSTS_EVIDENCE_EXTRACT.json` · GTC-001  

**Visible sheets (implementation surface):**  
`Block_TC` · `Block_TC_Gas` · `Cap_Allow` · `Cap_Allow Gas`  

---

## 0. What READY means

| Includes | Excludes |
|----------|----------|
| Cost category model (oil & gas) | Writing PEMS cost engine code |
| CaseInput / Production interface | Claiming PEMS-vs-GM numerical VALIDATED |
| Cap_Allow aggregation + discounting groups | Re-typing full multi-field matrix as day-1 UI |
| Capital allowance rate schedule (evidenced) | Inventing PIA CA rules beyond GM/law table |
| GTC comparison contract for cost KPIs | Full CR Econ fiscal engine READY |

---

## 1. Architecture (evidenced)

```text
CaseInput (Ec_IO READY)
  · cost_mode_field / block_field (G23, G18/G19)
  · hurdle_rate (C15)
  · asset_analysis_type, history years (C4, D28, E28/E30)
  · duties / VAT (C20, C21)
  · project_start_year / life (C5, C6←Prod_Summary)
        │
        ▼
┌────────────────────┐     ┌─────────────────────┐
│ Block_TC (oil)     │     │ Block_TC_Gas        │
│ per-field $mm/yr:  │     │ parallel structure  │
│ Exploration        │     │                     │
│ CAPEX Wells        │     │                     │
│ CAPEX Facilities   │     │                     │
│ OPEX               │     │                     │
│ Abandonment        │     │                     │
└─────────┬──────────┘     └──────────┬──────────┘
          │ field names from Block_Oil/Gas
          ▼
┌────────────────────────────────────────┐
│ Cap_Allow / Cap_Allow Gas              │
│ · copy field streams from Block_TC*    │
│ · FE: year ← Prod_Summary              │
│ · FF–FH: Exploration / Wells / Fac.    │
│ · FI: OPEX  · FP/FQ: CAPEX components  │
│ · FK: DISC. CAPEX  · FL: DISC OPEX     │
│ · FR: Capital Allowance Rates (Y1–Y5)  │
│ · FN/FO: Duties / VAT                  │
└──────────────────┬─────────────────────┘
                   ▼
     Ec_IO N16/S16/N17/S17/N18/S18
     CR Econ · HT/CIT/Project NCF · FLGT · RESULTS unit costs
```

**Oil vs gas:** Keep **two parallel cost stacks** (Block_TC + Cap_Allow vs Block_TC_Gas + Cap_Allow Gas). Do not merge into a single generic cost vector without stream tags.

---

## 2. CaseInput / Production → Costs map

| Upstream | GM | Costs use | Class |
|----------|-----|-----------|-------|
| `hurdle_rate` | Ec_IO!C15 | Discount factor in Cap_Allow `FK*`, `FL*` | ASSUMPTION (CaseInput) |
| `cost_mode_field` / field | Ec_IO!G23 (and G18/G19) | Field selection / cost mode (very high ref count to `$G$23`) | CASE_ATTRIBUTE |
| `asset_analysis_type` | Ec_IO!C4 | History windowing with D28/E28 | CASE_ATTRIBUTE |
| `history_year` / complete helpers | Ec_IO!D28, E28, E30 | Timeline filters in cost sheets | ASSUMPTION / DERIVED |
| `project_start_year` | Ec_IO!C5 | Year indexing / discount base alignment | ASSUMPTION |
| `project_life_years` | Ec_IO!C6 ← Prod_Summary!AF26 | Horizon | DERIVED from Production |
| `duties_rate` / `vat_rate` | Ec_IO!C20 / C21 | Cap_Allow FN/FO duties & VAT columns | DEFAULT_STRUCTURAL / CaseInput |
| Production years | Prod_Summary!S* → Cap_Allow!FE* | Year axis for summary cost block | DERIVED from Production |
| Production volumes | Prod_Summary / Block oil-gas | OPEX variable components where formulas reference production (catalogue) | DERIVED |

**Not Costs CaseInput:** Fiscal royalty rates (LAW TABLE); equity share (scales RESULTS, not Block_TC rates).

---

## 3. Cost categories (material groups)

### 3.1 Per-field technical cost (Block_TC / Block_TC_Gas)

| Category | Header label (row 2) | Unit (row 3) | Role |
|----------|----------------------|--------------|------|
| Exploration | Exploration | $mm | Capital / front-end spend by year |
| CAPEX Wells | CAPEX Wells | $mm | Well CAPEX |
| CAPEX Facilities | CAPEX Facilities | $mm | Facilities CAPEX |
| OPEX | OPEX | $mm | Operating expenditure |
| Abandonment | Abandonment | $mm | Abandonment / decommissioning |

**Structure:**  
- Column A: year (A4=2023 seed; A5=A4+1 …)  
- Field name row 1: linked from `Block_Oil Data` / gas counterpart  
- Repeated 5-column blocks per field (B–F, H–L, …)  
- **Classification of year×field cells:** register mix of ASSUMPTION / FORMULA_COEFFICIENT / DEFAULT_STRUCTURAL — treat as **scenario cost schedule inputs** (importable), not inventing values  

**Fixed / variable OPEX (evidenced labels row 49–50):**  
- Labels **Fixed** / **Vopex** with coefficients (e.g. Block_TC K49=0.05 Fixed, AC50 Vopex) — **FORMULA_COEFFICIENT** for OPEX split; full formulas in catalogue  

### 3.2 Cap_Allow summary block (selected / consolidated)

| Col | Label (row 2) | Example formula / role | Unit |
|-----|---------------|------------------------|------|
| FE | Year | `FE5=Prod_Summary!S5` | year |
| FF | Exploration | pulled/aggregated | $mm |
| FG | CAPEX Wells | | $mm |
| FH | CAPEX Facilities | | $mm |
| FI | OPEX | e.g. `FI5=Block_TC!GB5` (field-selected path) | $mm undisc. |
| FK | DISC. CAPEX | `FK5=(FF5+FG5+FH5)/(1+Ec_IO!$C$15)^(FE5-$FE$5)` | $mm PV |
| FL | DISC OPEX | `FL5=FI5/(1+Ec_IO!$C$15)^(FE5-$FE$5)` | $mm PV |
| FN | Duties | linked to duties drivers | $mm |
| FO | VAT | linked to VAT drivers | $mm |
| FP | (CAPEX component undisc.) | `FP5=FF5` | $mm |
| FQ | (CAPEX+Duties/VAT roll) | `FQ5=(FG5+FH5+FN5+FO5)` | $mm |
| FR | Capital Allowance Rates | FR5–FR9 = 0.2, 0.2, 0.2, 0.2, 0.19 | fraction |

**Totals (GTC-critical):**

| Cell | Formula | GM cached (oil Cap_Allow) |
|------|---------|---------------------------|
| FI48 | `=SUM(FI5:FI46)` | 361.503330356603 |
| FL48 | `=SUM(FL5:FL46)` | 185.584322008296 |
| FK48 | `=SUM(FK5:FK46)` | 142.902934166187 |
| FP48 | `=SUM(FP5:FP46)` | 35 |
| FQ48 | `=SUM(FQ5:FQ46)` | 140 |

**Cap_Allow Gas** parallel totals: FI48=56.7, FL48=25.4185178187494, FK48=0 (as-saved).

### 3.3 Capital allowance rates

| Item | GM | Notes |
|------|-----|-------|
| Y1–Y4 rate | Cap_Allow!FR5:FR8 = **0.2** | Matches Fiscal Terms_PIA capital allowance schedule evidence |
| Y5 rate | FR9 = **0.19** | Same |
| Classification | ASSUMPTION on Cap_Allow sheet; **law-aligned** | Do not invent alternate schedules; prefer LAW_TABLE identity for rates when implementing fiscal CA engine |
| Application formulas | Further Cap_Allow columns (catalogue) | Group: CA base × rate by year-in-service — detail in formula catalogue, not re-derived here |

### 3.4 Category map (directive §4) — **only workbook-supported**

Do **not** invent categories. Mapping uses **header labels + Cap_Allow summary labels + consumers**.

| Requested class | GM support? | Evidence | PEMS mapping |
|-----------------|-------------|----------|--------------|
| Development costs | **Partial** — not a single header | No column literally named “Development”. Closest: multi-year **CAPEX Wells + CAPEX Facilities + Exploration** schedules | Treat as **composition of Exploration + CAPEX Wells + CAPEX Facilities** when reporting “development CAPEX”; do not invent a 6th Block_TC column |
| Capital expenditure | **Yes** | Headers **CAPEX Wells**, **CAPEX Facilities**; Cap_Allow **FF/FG/FH**, **FK DISC. CAPEX**, **FP Expensed CAPEX** | CAPEX wells/facilities + exploration as capital schedule; disc. CAPEX = FK |
| Operating expenditure | **Yes** | Header **OPEX**; Cap_Allow **FI OPEX**, **FL DISC OPEX**; Fixed/Vopex coeffs | OPEX undisc/disc |
| Abandonment / decommissioning | **Yes** | Header **Abandonment** (row 2) | Abandonment $mm/yr by field |
| Transportation / processing | **No separate column found** | No Block_TC/Cap_Allow header “Transport” or “Processing” in catalogue label scan | **Out of Costs contract as distinct category** unless later catalogue evidence appears |
| Other project costs | **Limited** | **Duties**, **VAT** (Cap_Allow FN/FO); **Acquisition Allowance** (HC); **SLN** (GX) | Map only these labeled columns |
| Timing / scheduling | **Yes** | Year spine A / FE; History filter; pre/post production years as zero/nonzero schedule cells | §3.5 / §5 timing |

**Rule:** Category membership is from **GM labels and formula roles**, not English synonym guessing.

### 3.5 Cap_Allow fiscal-facing cost outputs (labels evidenced)

| Col | Label | Consumer evidence |
|-----|-------|-------------------|
| FP | **Expensed CAPEX** | CR Econ `G*` ← FP; HT_NCF_Oil `K*` ← FP |
| FI | **OPEX** | CR Econ `I*` ← FI oil+gas |
| GX | **SLN** | CR Econ `H*` ← GX+HC; HT_NCF_Oil `W*` ← GX |
| HC | **Acquisition Allowance** | CR Econ `H*`; HT_NCF_Oil `AD*` ← HC |
| FJ | (catalogue — used in HT_NCF_Oil AR*) | HT_NCF_Oil tax base adjustments |

### 3.6 Escalation / indexation (evidenced)

| Evidence | Location | Handling |
|----------|----------|----------|
| Label **Escalated** + **OPEX** | Block_TC!GB1 / GB2 | **Escalated OPEX** block; GB5 uses History filter + VLOOKUP on FQ:FU schedule (`IF(Ec_IO!$C$4="History",…)`) |
| Cap_Allow FI path | e.g. `FI5=Block_TC!GB5` | Consolidated OPEX may pull **escalated** OPEX column, not only raw E-column OPEX |
| Discount (not inflation) | Cap_Allow FK/FL with Ec_IO!C15 | **Present-value discounting** at hurdle rate — not cost inflation |
| Ec_IO price escalator C14 | CaseInput | Revenue/price path; **not** proven as Block_TC $mm escalator CaseInput |
| Inflation | **No dedicated inflation CaseInput** found on cost sheets | Do not invent inflation engine |

### 3.7 Annualization / timing

| Topic | Evidence |
|-------|----------|
| Time basis | Annual calendar years (column A / FE) |
| Alignment to production | FE ← Prod_Summary!S*; Block_TC A shared with production year spine |
| Production-linked volumes | Prod_Summary T2/X2 referenced near escalated region (FY1/FZ1); Vopex coeffs |
| Discount base | First year of FE block (`$FE$5`) with hurdle C15 |
| Cost life | Years with non-zero schedule through SUM ranges (e.g. FI5:FI46) |
| Units | **$mm** throughout cost categories |

---

## 4. Parameter catalogue (implementation-relevant)

### 4.1 CaseInput (already READY — costs consumers)

| PEMS name | Cell | Role in Costs |
|-----------|------|----------------|
| `hurdle_rate` | Ec_IO!C15 | PV of CAPEX/OPEX |
| `duties_rate` | Ec_IO!C20 | Duties column |
| `vat_rate` | Ec_IO!C21 | VAT column |
| `cost_mode_field` / fields | G23, G18, G19 | Field / mode selection |
| `asset_analysis_type` | C4 | History filters |
| `project_start_year` | C5 | Timeline |
| `production_days_per_year` | C7 | Indirect via production annualization upstream |

### 4.2 Cost schedule inputs (Block_TC / Gas)

| PEMS concept | GM location | Class | Manual | Import |
|--------------|-------------|-------|--------|--------|
| `tc_year_spine` | Block_TC!A4:A* | ASSUMPTION / DERIVED series | Optional | Yes |
| `oil_exploration[field,year]` | Block_TC Exploration cols | ASSUMPTION / schedule | Field editor later | Yes |
| `oil_capex_wells[field,year]` | CAPEX Wells cols | same | | Yes |
| `oil_capex_facilities[field,year]` | CAPEX Facilities | same | | Yes |
| `oil_opex[field,year]` | OPEX cols | ASSUMPTION / formula | | Yes |
| `oil_abandonment[field,year]` | Abandonment | same | | Yes |
| Gas counterparts | Block_TC_Gas same headers | same | | Yes |
| `opex_fixed_coeff` / `opex_vopex_coeff` | Row 49–50 Fixed/Vopex | FORMULA_COEFFICIENT | Advanced | Yes |

**v1 implementation rule:** Support (1) **import of Block_TC / Cap_Allow schedules** for GTC parity, and (2) **selected-field consolidated path** used by Cap_Allow FE–FQ / FI–FL. Full multi-field GUI = later (same pattern as Production).

### 4.3 Capital allowance & discount outputs (DERIVED)

| PEMS name | GM | Class |
|-----------|-----|-------|
| `ca_rate_y1`…`ca_rate_y5` | Cap_Allow!FR5:FR9 | ASSUMPTION / LAW-aligned |
| `opex_undisc_total_oil` | Cap_Allow!FI48 | DERIVED |
| `opex_disc_total_oil` | Cap_Allow!FL48 | DERIVED |
| `capex_disc_total_oil` | Cap_Allow!FK48 | DERIVED |
| `capex_undisc_components_oil` | FP48, FQ48 | DERIVED |
| Gas stack totals | Cap_Allow Gas!FI48, FL48, FK48… | DERIVED |
| `pv_opex_combined` | Ec_IO!N16 | DERIVED hub |
| `undisc_opex_combined` | Ec_IO!S16 | DERIVED hub |
| `pv_capex_combined` | Ec_IO!N17 | DERIVED hub |
| `undisc_capex_combined` | Ec_IO!S17 | DERIVED hub |
| `pv_tc_combined` | Ec_IO!N18 = N16+N17 | DERIVED |
| `undisc_tc_combined` | Ec_IO!S18 = S16+S17 | DERIVED |

**Derived must not become independent user inputs.**

---

## 5. Logic groups (evidenced)

### G1 — Multi-field TC schedule (oil / gas)

Purpose: store annual $mm by category by field.  
Source: Block_TC / Block_TC_Gas.  
Downstream: Cap_Allow copy formulas `B4=Block_TC!B4`, etc.; production year spine; FLGT via Block_TC.

### G2 — Field / mode selection

Purpose: choose which field column feeds consolidated Cap_Allow summary (GB etc.).  
Drivers: Ec_IO G23 / G18 / G19 (catalogue formulas).  
Do not invent selection order — follow formula catalogue IF chains.

### G3 — Undiscounted category aggregation

Purpose: annual OPEX/CAPEX components FI, FF–FH, FP, FQ.  
Example: `FI5=Block_TC!GB5`, `FP5=FF5`, `FQ5=(FG5+FH5+FN5+FO5)`.

### G4 — Discounting at hurdle rate

Purpose: PV CAPEX and OPEX.  
Exact:  
`FK5=(FF5+FG5+FH5)/(1+Ec_IO!$C$15)^(FE5-$FE$5)`  
`FL5=FI5/(1+Ec_IO!$C$15)^(FE5-$FE$5)`  
Totals SUM to row 48.

### G5 — Capital allowance rate application

Purpose: apply FR rates (0.2×4, 0.19) to eligible CAPEX for fiscal consumers.  
Detail: remaining Cap_Allow columns in catalogue; rates align with Fiscal Terms law table.

### G6 — Hub export to Ec_IO / NCF

Purpose: expose combined oil+gas cost KPIs on Ec_IO; feed CR Econ / HT/CIT NCF.  
Ec_IO N16/S16/N17/S17/N18/S18 formulas as §4.3.

### G7 — Escalated OPEX path

Purpose: History-aware escalated OPEX series (Block_TC **Escalated/OPEX** GB*).  
Example pattern: `GB5=IF(Ec_IO!$C$4="History",(FX5>=Ec_IO!$D$28)*VLOOKUP(...)*(FX5<=Ec_IO!E28),…)`.  
Cap_Allow FI may reference GB (selected field).

### G8 — SLN / Acquisition allowance (to tax)

Purpose: Cap_Allow **GX SLN**, **HC Acquisition Allowance** feed CR Econ and HT_NCF.  
Formulas: array formulas on GM (catalogue); consumers CR Econ H*, HT_NCF_Oil W*/AD*.

---

## 6. Fiscal interface (directive §6)

**Do not duplicate Fiscal Terms_PIA inside Costs.** Law table remains the regulatory source.

| Fiscal area | Costs provides | Costs does **not** own |
|-------------|----------------|-------------------------|
| Fiscal Terms_PIA | Application surface for CA rates on Cap_Allow (FR mirrors law schedule 0.2/0.19) | Royalty tiers, HT/CIT rates, bonus tables |
| Royalties | Cost schedules may affect bases **only if** royalty formulas reference costs (primary royalty drivers are production/price) | Royalty rate tables |
| FLGT | Block_TC refs into FLGT (catalogue ~135 via Block_TC) | FLGT take algorithms |
| Hydrocarbon tax (HT) | Cap_Allow FP, GX, HC, FJ → HT_NCF_Oil (171 Cap_Allow refs) | HT rate law |
| CIT | Cap_Allow → CIT_NCF* (catalogue) | CIT rate law |
| CR Econ / NCF | FP (Expensed CAPEX), FI (OPEX), GX+HC (allowances) annual series | Profit oil / cost recovery **rules** (CR engine PARTIAL) |
| RESULTS | Unit costs use PV/undisc TC ÷ production (Y50) | KPI composition |

```text
Fiscal Terms_PIA (LAW TABLE) ──rates/structure──► fiscal engines
Block_TC / Cap_Allow (Costs) ──$mm series & CA application──► CR / HT / CIT / NCF
```

---

## 7. Dependency order (directive §8)

```text
Ec_IO (CaseInput READY)
   ↓
Production (READY) ──years/volumes──┐
   ↓                                 │
Costs (this contract) ◄──────────────┘
   ↓
Fiscal engines: Royalties / FLGT / CR-NCF (PARTIAL)
   ↓
RESULTS (PARTIAL)
```

**Independent / cross links (explicit):**

| Link | Nature |
|------|--------|
| Costs ← Fiscal LAW (CA rate identity) | Rates; not full law-table reimplementation |
| Costs → FLGT | Block_TC technical cost feeds (not only post-royalty) |
| Costs → Ec_IO hub | N16–S18 display KPIs (circular presentation only — not CaseInput) |
| Equity C4 | Does **not** scale Block_TC; scales RESULTS/equity NCF |

---

## 8. Edge conditions (directive §9 — evidenced only)

| Condition | Evidence |
|-----------|----------|
| Zero / blank cost | Many Block_TC cells 0; SUM of zeros |
| Zero production | OPEX may still be nonzero (fixed opex); production-linked Vopex formulas → 0 when volume 0 (catalogue) |
| Inactive / History periods | Escalated OPEX and other series gated by Ec_IO C4 + D28/E28 |
| Pre-production expenditure | Nonzero CAPEX/Exploration years before production start on schedule (year spine) |
| Post-production expenditure | Abandonment / late OPEX years on schedule where nonzero |
| Missing optional costs | Import missing field → selection IF / IFERROR → 0 |
| Escalation boundaries | History window on escalated OPEX; no invented inflation cap |
| Discount year 0 | `(FE−$FE$5)=0` → PV factor 1 |

**Not invented:** generic “cost escalation %” CaseInput; transport/processing categories; automatic OPEX=0 when production=0 without formula evidence.

---

## 9. Downstream consumers (outputs)

| Output class | GM examples | Consumers |
|--------------|-------------|-----------|
| Undisc OPEX / CAPEX totals | FI48, FP48, FQ48, Ec_IO S16/S17 | Ec_IO hub, RESULTS |
| Disc OPEX / CAPEX totals | FL48, FK48, Ec_IO N16/N17/N18 | Ec_IO hub, unit costs |
| Annual expensed CAPEX | Cap_Allow FP* | CR Econ G*, HT_NCF K* |
| Annual OPEX | Cap_Allow FI* | CR Econ I* |
| SLN / Acq. allowance | GX*, HC* | CR Econ H*, HT_NCF W*/AD* |
| Field TC streams | Block_TC categories | Cap_Allow, FLGT |
| CA rates applied | Cap_Allow CA columns | HT/CIT/CR (catalogue) |

---

## 10. GTC comparison contract (directive §7)

### 10.1 Cap_Allow oil totals

| Point | GM cell | Expected (as-saved) |
|-------|---------|---------------------|
| OPEX undisc sum | Cap_Allow!FI48 | 361.503330356603 |
| OPEX disc sum | Cap_Allow!FL48 | 185.584322008296 |
| CAPEX disc sum | Cap_Allow!FK48 | 142.902934166187 |
| FP48 / FQ48 | Cap_Allow!FP48 / FQ48 | 35 / 140 |
| CA rates | FR5:FR9 | 0.2,0.2,0.2,0.2,0.19 |

### 10.2 Cap_Allow Gas totals

| Point | GM cell | Expected |
|-------|---------|----------|
| FI48 | Cap_Allow Gas!FI48 | 56.7 |
| FL48 | Cap_Allow Gas!FL48 | 25.4185178187494 |
| FK48 | Cap_Allow Gas!FK48 | 0 |

### 10.3 Ec_IO hub (combined)

| Point | GM cell | Expected | Formula |
|-------|---------|----------|---------|
| PV OPEX | Ec_IO!N16 | 211.002839827046 | Cap_Allow!FL48+Gas!FL48 |
| Undisc OPEX | Ec_IO!S16 | 418.203330356603 | FI48+Gas!FI48 |
| PV CAPEX | Ec_IO!N17 | 142.902934166187 | FK48+Gas!FK48 |
| Undisc CAPEX | Ec_IO!S17 | 175 | FP+FQ oil+gas |
| PV TC | Ec_IO!N18 | 353.905773993233 | N16+N17 |
| Undisc TC | Ec_IO!S18 | 593.203330356603 | S16+S17 |

### 10.4 Later engine path

```text
CaseInput + Block_TC schedules
  → Cap_Allow G3–G5
  → Ec_IO N16–S18 / CR Econ / NCF
  → RESULTS unit cost KPIs (Y50 production divisor)
```

Full series: `formula_cached_results_all.csv` for Cap_Allow* / Block_TC*.  
**Do not claim VALIDATED** until PEMS run matches.

---

## 11. Traceability

```text
Excel cell/range
  → category / meaning (§3–3.4)
  → PEMS parameter or series (§4)
  → CaseInput / Production / DERIVED
  → logic group G1–G8
  → fiscal interface (§6) / consumer (§9)
  → GTC point (§10)
```

---

## 12. Remaining gaps (scoped — not READY blockers)

| Gap | Handling |
|-----|----------|
| Full multi-field UI | Import + selected-field path for v1 |
| Every Cap_Allow CA / SLN / HC formula body | Catalogue authority; groups G5/G8 documented |
| Transport/processing as categories | **Not evidenced** — excluded |
| Generic inflation CaseInput | **Not evidenced** — excluded |
| Variable OPEX exact volume formula per field | Catalogue per cell; Fixed/Vopex documented |

**Critical-path cost literals:** all RESOLVED in register (no UNRESOLVED).

---

## 13. Readiness gate (directive §10)

| # | Criterion | Met? |
|---|-----------|------|
| 1 | All implementation-relevant Costs parameters identified | **Yes** |
| 2 | All GM source cells/ranges mapped | **Yes** |
| 3 | Upstream Ec_IO/Production links established | **Yes** §2 |
| 4 | Inputs and derived values distinguished | **Yes** |
| 5 | Units documented | **Yes** ($mm, %) |
| 6 | Timing documented | **Yes** §3.7 / §8 |
| 7 | Cost categories documented | **Yes** §3 / §3.4 |
| 8 | Escalation/indexation documented where evidenced | **Yes** §3.6 |
| 9 | Fiscal interfaces documented | **Yes** §6 |
| 10 | Downstream consumers documented | **Yes** §9 |
| 11 | Dependencies documented | **Yes** §7 |
| 12 | GTC comparison points established | **Yes** §10 |
| 13 | Traceability complete | **Yes** §11 |
| 14 | No unresolved implementation-critical ambiguity | **Yes** (§12 scoped) |
| 15 | No calculation code written | **Yes** |

# **COSTS = READY**

**Means:** Specification sufficient to implement cost schedule import, Cap_Allow aggregation/discounting/CA application surface, fiscal hand-off, and GTC cost KPI compare.  
**Does not mean:** FLGT/CR/NCF/RESULTS READY or numerical PEMS-vs-GM VALIDATED.
