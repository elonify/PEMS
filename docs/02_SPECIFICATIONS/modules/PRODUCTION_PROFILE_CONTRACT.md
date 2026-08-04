# Production Profile Contract — Implementation Readiness

**Status:** **READY** (production specification / interface contract only — not calculation VALIDATED)  
**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Module:** M-CP-02 / M04 Production  
**GM modified:** **No**  
**Calculation code under this task:** **None**

**Do not reopen:** GM identity · Equity INPUT · Fiscal LAW TABLE · Ec_IO READY · 829/829 · AU14 expected · ADR-0010  

**Companions:**  
- `EC_IO_PARAMETER_CONTRACT.md` (CaseInput — READY)  
- `docs/workbook/catalogue/` (formula/cell extract)  
- `docs/workbook/semantic_mapping/PRODUCTION_EVIDENCE_EXTRACT.json`  
- GTC-001 KPI / formula caches  

**Visible scope sheets (implementation surface):**  
`Production Profile` · `Block_Oil Data` · `Block_Gas Data` · `Prod_Summary`  

**Hidden (ignored for input readiness; do not modify):** `OML123_Oil_S1` — still appears as formula source into Prod_Summary (catalogue-only).

---

## 0. What READY means

| Includes | Excludes |
|----------|----------|
| Parameter catalogue for production drivers | Writing PEMS production engine code |
| Logic **groups** with exact GM formulas (core) | Claiming PEMS-vs-GM numerical VALIDATED |
| CaseInput → Production interface | Re-opening Ec_IO or Fiscal |
| Oil vs gas streams kept distinct | Inventing decline rules beyond GM formulas |
| GTC comparison **contract** | Full line-by-line Block field matrix as UI inputs |
| Dependency order to Costs/FLGT/NCF | Reservoir STOIIP/GIIP engine READY (interface only) |

---

## 1. Architecture (evidenced)

```text
CaseInput (Ec_IO READY)
  · block_field_oil / gas (G18/G19)
  · asset_analysis_type (C4)
  · project_start_year (C5), history/complete years
  · production_days_per_year (C7)  ← PEMS-facing days
        │
        ▼
┌───────────────────┐     ┌────────────────────┐
│ Production Profile│     │ STOIIP / GIIP      │
│ decline / build-up│◄────│ in-place × RF → UR │
└─────────┬─────────┘     └────────────────────┘
          │ rate & annual series (D/E/G/H)
          ▼
┌───────────────────┐     ┌────────────────────┐
│ Block_Oil Data    │     │ Block_Gas Data     │
│ multi-field mb/d  │     │ multi-field mmscf/d│
│ annual mmbbls      │     │ annual bscf        │
└─────────┬─────────┘     └─────────┬──────────┘
          └──────────┬──────────────┘
                     ▼
              Prod_Summary
           (oil + gas timelines,
            life AF26, totals V47/Y*)
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   Royalties/FLGT  Cap_Allow   RESULTS / Ec_IO life
```

**GM note:** Named range `Production_Days` → `'Oil Input'!$G$2` (**hidden** sheet). PEMS CaseInput uses **`production_days_per_year` ← Ec_IO!C7** (READY). For GTC parity, confirm Oil Input G2 equals C7 on baseline (both 365-class values on active GM path) — do not invent a second days source in CaseInput.

---

## 2. CaseInput → Production parameter map

| CaseInput (Ec_IO contract) | GM source | Production use | Class |
|----------------------------|-----------|----------------|-------|
| `block_field_oil` | Ec_IO!G18 | Selects oil field column / total in Block_Oil (`CU*` nested IF vs field headers) | CASE_ATTRIBUTE |
| `block_field_gas` | Ec_IO!G19 | Selects gas field in Block_Gas (`CO*`/`CP*`) | CASE_ATTRIBUTE |
| `asset_analysis_type` | Ec_IO!C4 | Prod_Summary T/U/W series History window vs full VLOOKUP | CASE_ATTRIBUTE |
| `project_start_year` | Ec_IO!C5 | Timeline / Ec_IO calendar; production year headers from Block_TC!A* | ASSUMPTION |
| `history_year` / `complete_year` | Ec_IO!D28 / D30 (+ E28 formulas) | History filter bounds on Prod_Summary | ASSUMPTION |
| `production_days_per_year` | Ec_IO!C7 | Annualization intent in PEMS; GM also uses `Production_Days` name | ASSUMPTION |

**Not Production CaseInput:** Fiscal law rates, equity share (equity scales **results**, not block rates), Ec_IO oil/gas **prices** (revenue layer).

**Derived into Ec_IO from Production (hub):**  
`Ec_IO!C6` = `Prod_Summary!AF26` → **project life years** (HUB_OUTPUT / upstream-derived).

---

## 3. Parameter / item catalogue (implementation-relevant)

### 3.1 Production Profile — mode & reservoir interface

| PEMS name | GM cell | GM value / form | Meaning | Class | Unit | Type |
|-----------|---------|-----------------|---------|-------|------|------|
| `pp_mode` | Production Profile!B2 | STOIIP (text) | Oil (STOIIP) vs gas (GIIP) profile mode | ASSUMPTION / switch | enum | str |
| `stoiip_inplace` | C2 formula | `=IF(B2="STOIIP",STOIIP!D10*STOIIP!D11,F2)` | In-place oil when mode STOIIP | DERIVED from reservoir | MMbbls | float |
| `giip_inplace` | F2 | `=GIIP!D10*GIIP!D11` | In-place gas | DERIVED from reservoir | Bscf | float |
| `oil_rf` | C3 | 0.35 | Recovery factor oil | FORMULA_COEFFICIENT | fraction | float |
| `gas_rf` | F3 | 0.75 | Recovery factor gas | FORMULA_COEFFICIENT | fraction | float |
| `oil_ur` | C4 | `=IF(B2="STOIIP",C2*C3,F2*F3)` | Ultimate recovery oil path | DERIVED | MMbbls | float |
| `gas_ur` | F4 | `=F2*F3` | Ultimate recovery gas | DERIVED | Bscf | float |
| `gor_scf_bbl` | F5 | 2000 | GOR for associated gas | ASSUMPTION | scf/bbl | float |

### 3.2 Production Profile — schedule / decline drivers

| PEMS name | GM cell | GM value | Meaning | Class | Unit |
|-----------|---------|----------|---------|-------|------|
| `prod_start_lag_years` | C7 | 1 | “Production start = … Year/s later” | DEFAULT_STRUCTURAL | years |
| `year_end_anchor` | C8 | 2026 | Calendar year end anchor for series B23… | ASSUMPTION | year |
| `pp_days_in_year` | C9 | 365 | Days used inside PP annualization | FORMULA_COEFFICIENT | days |
| `eff_decline_rate` | L7 | 0.125 | Effective decline rate d | ASSUMPTION | fraction/yr |
| `qi_buildup` | C12 | 1000 | Initial rate build-up | FORMULA_COEFFICIENT | BOPD or Mscf/d by mode |
| `qp_plateau` | C13 | 6000 | Plateau rate | FORMULA_COEFFICIENT | same |
| `qel_end` | I13 | 500 | Economic limit rate (decline) | FORMULA_COEFFICIENT | same |
| `t1_buildup_yrs` | C14 | 2 | Build-up duration | DEFAULT_STRUCTURAL | years |
| `t2_plateau_yrs` | F14 | 3 | Plateau duration | DEFAULT_STRUCTURAL | years |
| `a1_buildup` | C15 | `=LN(C12/C13)/C14` | Build-up exponent a | DERIVED | 1/yr |
| `np1` / `np2` / `np3` | C16 / F16 / I16 | formulas §4 | Phase cumulatives | DERIVED | MMbbls/Bscf |
| `t3_decline_yrs` | I14 | `=1/I15*(LN(I12/I13))` | Decline duration | DERIVED | years |
| `a3_decline` | I15 | complex formula §4 | Decline exponent | DERIVED | 1/yr |
| `field_time_total` | F17 | `=C7+C14+F14+I14` | Total field time | DERIVED | years |

**Excluded from base Production CaseInput (PRESENTATION on PP sheet):**  
AB6–AM6 sensitivity toggles; AC7 Tax 0.3; AC8 OPEX 0.1; AC9 Oil Price 70; AC10 Disc. Rate 0.15 and scaled AB/AD columns — **local PP sensitivity**, not Ec_IO CaseInput (prices/hurdle already on Ec_IO).

### 3.3 Block streams (pattern, not every field column as CaseInput)

| Item | GM evidence | Class | Notes |
|------|-------------|-------|-------|
| Field headers | Block_Oil!B1, E1, H1, … CE1, CH1… | LABEL | Many OML 123 fields |
| Daily oil rate per field-year | e.g. B7, E7, … | INPUT or COEFFICIENT per register | Multi-column series |
| Annual oil | C4 style `=(B4*Production_Days)/1000` | DERIVED | mmbbls from mb/d |
| Selected oil series | CU* / CT* via Ec_IO!G18 match | DERIVED selection | Nested IF field picker |
| Daily gas / annual gas | Block_Gas analogous; mmscf/d → bscf | same pattern | Selected via Ec_IO!G19 |
| Year column | A* `=Block_TC!A*` | DERIVED from cost timeline | Shared calendar |
| Production Profile feed | K/L columns `=IF(...Production Profile!D/E…)` | DERIVED | Oil from PP rates; Gas from PP oil or gas columns by mode |

**Implementation rule:** CaseInput does **not** require every field column as a first-class UI field for v1.  
v1 production service must support:  
1) **Analytical profile path** (Production Profile parameters), and/or  
2) **Selected field annual series** driven by `block_field_oil/gas` + imported block rates for GTC parity.  
Full multi-field editor = later scope (document gap, not blocker for contract READY).

### 3.4 Prod_Summary outputs (canonical production results)

| PEMS name | GM cell | Formula / value | Unit | Class | Downstream |
|-----------|---------|-----------------|------|-------|------------|
| `summary_mode_flag` | R1 | `=Production Profile!B2` | text | DERIVED | AF21 |
| `oil_daily_series` | T5:T* | History-aware VLOOKUP from oil block | mb/d | DERIVED | life, royalties |
| `oil_annual_series` | U5:U* | VLOOKUP col 3 | mmbbls | DERIVED | cum, revenue path |
| `oil_cum_series` | V5:V* | running sum | mmbbls | DERIVED | V47 |
| `gas_daily_series` | W5:W* | gas VLOOKUP | mmscf/d | DERIVED | |
| `gas_annual` / cum | X/Y | | bscf | DERIVED | Y47 |
| `oil_eur_or_max_cum` | V47 | `=MAX(V5:V36)` | mmbbls | DERIVED | RESULTS N22 path |
| `gas_max_cum` | Y47 | `=MAX(Y5:Y46)` | bscf | DERIVED | RESULTS |
| `gas_boe_factor` | Y48 | **5.804** literal | boe/bscf-class | DEFAULT_STRUCTURAL | Y49 |
| `gas_mmboe` | Y49 | `=MAX(Y5:Y46)/$Y$48` | mmboe | DERIVED | RESULTS N23 |
| `total_mmboe` | Y50 | `=V47+Y49` | mmboe | DERIVED | unit costs / Ec_IO N19… |
| `project_life_years` | AF26 | COUNTIF positive oil or gas rates | years | DERIVED | **Ec_IO!C6** |

---

## 4. Production logic groups (evidenced)

### G1 — In-place & ultimate recovery

| Field | Content |
|-------|---------|
| Purpose | STOIIP/GIIP × RF → UR; mode B2 switches oil vs gas labels |
| Formulas | C2, F2, C3/F3 literals, C4, F4 |
| Units | MMbbls / Bscf |
| Downstream | Np targets C6/F6; decline volume balance I16 |

### G2 — Build-up / plateau / decline design

| Field | Content |
|-------|---------|
| Purpose | Three-phase analytical rate design |
| Build-up | qi→qp over t1; `a1=LN(qi/qp)/t1`; `Np1=(qi-qp)*days/a1/1e6` |
| Plateau | rate qp for t2 years; `Np2=qp*days*t2/1e6` |
| Decline | to qel; `a3` from I15; `t3=LN(qi_decl/qel)/a3`; `Np3=UR−Np1−Np2` |
| Exact a3 | `I15=((I12-I13)*$C$9/I16/1000000)+-LN(1-L7)*0` (second term ×0 on GM) |
| Labels | B11 build-up; E11 plateau; H11 decline |

### G3 — Annual time series (rate & annual production)

| Field | Content |
|-------|---------|
| Purpose | Year-by-year rate (D) and annual volume (E); associated gas G/H when oil mode |
| Calendar | B23=`C8`, B24=B23+1…; time index C23 from year end & field time F17 |
| **Rate D23 (exact GM)** |  
`=(IF(AND(C23>=$C$7,C23<($C$14+$C$7)),$C$12*EXP(-$C$15*(C23-$C$7)),IF(AND(C23>=($C$14+$C$7),C23<($C$14+$C$7+$F$14)),$F$12,IF(C23<=$C$7,0,$I$12*EXP(-$I$15*(C23-($C$14+$F$14+$C$7))))))*(B23<=($C$8+$C$7+$F$17)))/1000` |
| Semantics | Build-up exponential → plateau constant → decline exponential; zero before start; cut after field life |
| Annual E23 | Difference of rates × days / a (phase-dependent); full formula in catalogue |
| AG gas | `G23=IF(B2="GIIP",0,D23*F5)/1000`; `H23=IF(B2="GIIP",0,F5*E23/1000)` |
| Edge | Zero rate → zero annual/cum (IF guards) |

### G4 — Block field annualization & selection

| Field | Content |
|-------|---------|
| Purpose | Per-field daily → annual; pick active field from CaseInput name |
| Annualization | `C4=(B4*Production_Days)/1000` (oil mb/d→mmbbls); gas analogous /1000 to bscf |
| Selection | `CU4=IF(Ec_IO!$G$18=$CH$1,CI4,IF(Ec_IO!$G$18=$CE$1,CF4,…))` pattern (full chain in catalogue) |
| Gas | `CO4`/`CP4` vs Ec_IO!$G$19 |
| PP bridge | Oil K/L from Production Profile D/E when mode≠GIIP; Gas K/L from D/E if GIIP else G/H |

### G5 — Prod_Summary assembly & life

| Field | Content |
|-------|---------|
| Purpose | Unified oil/gas year table for fiscal & results |
| Oil/gas blocks | B/C/D/E from Block_Oil CS–CV; G/H/I/J from Block_Gas CN–CQ |
| History mode | T5/U5/W5 multiply by year∈[D28,E28] when C4="History" |
| Life AF26 | Count years with oil rate>0 if AF21 in {Oil,AG}, else gas rate>0 |
| Totals | V47, Y47–Y50 as §3.4 |

### G6 — Local PP sensitivity (deferred)

Tax/OPEX/price/disc columns AB–AM — **PRESENTATION**; not required for production stream READY.

---

## 5. Time and schedule

| Topic | Evidence |
|-------|----------|
| Project start year | Ec_IO!C5 (CaseInput); PP year_end C8=2026 on GM |
| Production commencement | C7 lag years after design; series zero until C23≥C7 |
| Annual periods | Integer years B23…; Block_TC!A shared year index |
| Days/year | PP C9; CaseInput C7; named `Production_Days`→Oil Input G2 hidden |
| Decline/profile | G2–G3 formulas |
| Oil timeline | Prod_Summary T/U/V; Block_Oil |
| Gas timeline | Prod_Summary W/X/Y; Block_Gas; AG from GOR when oil mode |
| Ec_IO C5/C7 relation | C5/C4/D28 drive History filter; C7 is PEMS days; life AF26 feeds Ec_IO C6 |

---

## 6. Oil and gas streams (kept separate)

| Stream | Daily unit | Annual unit | Cum unit | Source path | Consumers |
|--------|------------|-------------|----------|-------------|-----------|
| Oil | mb/d (Block); Mbopd (PP D/1000 scale) | mmbbls | mmbbls | Block_Oil + PP oil mode | Royalties, FLGT oil rev, V47, RESULTS oil |
| NAG / gas | mmscf/d | bscf | bscf | Block_Gas + PP GIIP mode or AG from GOR | FLGT gas, Y47–Y49, RESULTS gas |
| AG (associated) | from oil×GOR | bscf | bscf | PP G/H when B2≠GIIP | Gas stream when oil mode |

**Do not** merge into one generic `production` scalar in PEMS domain model.

---

## 7. Dependencies

| From | To | Nature |
|------|-----|--------|
| Ec_IO CaseInput | Production | Field names, analysis type, days, history bounds |
| STOIIP / GIIP | Production Profile | In-place volumes (interface; reservoir module not READY) |
| Production Profile | Block_Oil/Gas | Rate/annual bridge columns |
| Block_TC years | Block oil/gas A column | Calendar |
| Production | Prod_Summary | Assembly |
| Prod_Summary | Royalties, FLGT | Volumes (309 / 307 formula refs to Prod_Summary!) |
| Prod_Summary | Cap_Allow / Block_TC | Throughput / timing (99 / 45…) |
| Prod_Summary | RESULTS Equity | V47, Y47, Y49, Y50 unit costs |
| Prod_Summary AF26 | Ec_IO C6 | Project life |
| Fiscal Terms_PIA | Production | **No direct** — fiscal uses production **outputs** via royalty engines |
| Equity C4 | Production rates | **No** — scales results only |

### Implementation dependency order

1. CaseInput (Ec_IO READY) + law table load (Fiscal READY)  
2. **Production** (this contract)  
3. Costs / Cap_Allow (PARTIAL)  
4. FLGT / Royalties (PARTIAL)  
5. CR / NCF (PARTIAL)  
6. RESULTS (PARTIAL)

---

## 8. Edge conditions (evidenced only)

| Condition | Evidence |
|-----------|----------|
| Zero production | Rate formulas force 0 before start / after life; annual IF(D=0) |
| Inactive years | History filter zeros outside [D28,E28]; VLOOKUP IFERROR→0 |
| Commencement | C7 lag; C23≥C7 for nonzero build-up |
| Cessation | `B23<=($C$8+$C$7+$F$17)` gate on rate; COUNTIF life |
| Oil-only / gas-only | B2 STOIIP vs GIIP; G/H forced 0 when GIIP; AF26 oil vs gas COUNTIF |
| Missing field match | Nested IF falls through — exact default in full CU formula (catalogue); IFERROR 0 on VLOOKUP |
| Hidden OML123 series | Still linked in Prod_Summary L–O — out of **input** scope; implement via formula parity or defer with explicit gap flag if v1 omits |

---

## 9. GTC comparison contract

### 9.1 Ingestion / intermediate production points

| PEMS output | GM cell | GTC-001 expected (as-saved) |
|-------------|---------|------------------------------|
| oil max cum | Prod_Summary!V47 | **21.9977894563747** |
| gas max cum | Prod_Summary!Y47 | **25.2454818442975** |
| gas boe factor | Prod_Summary!Y48 | **5.804** |
| project life | Prod_Summary!AF26 | **15** (feeds Ec_IO!C6) |
| PP mode | Production Profile!B2 | STOIIP |
| oil RF / gas RF | C3 / F3 | 0.35 / 0.75 |
| GOR | F5 | 2000 |
| qi / qp / qel | C12 / C13 / I13 | 1000 / 6000 / 500 |
| t1 / t2 | C14 / F14 | 2 / 3 |
| days | C9 | 365 |
| year end | C8 | 2026 |
| start lag | C7 | 1 |

### 9.2 Consumer path (later engine validation)

```text
CaseInput field names + days
  → Production series
  → Prod_Summary V47/Y47/Y50/AF26
  → Royalties/FLGT/Cap_Allow/RESULTS KPIs (GTC KPI pack)
```

KPI pack already includes RESULTS cells using `Prod_Summary!$Y$50`, `V47`, `Y47`, `Y49`.  
Full series: `formula_cached_results_all.csv` filtered by worksheet.

**Do not claim VALIDATED** until PEMS engine run matches.

---

## 10. Traceability

```text
Excel cell/range
  → semantic meaning (§3–4)
  → PEMS parameter / series
  → CaseInput link or DERIVED
  → calc group G1–G5
  → consumer sheet
  → GTC point (§9)
```

Artefacts: this contract · catalogue CSVs · `EC_IO_PARAMETER_CONTRACT.md` · GTC-001 · readiness matrix.

---

## 11. Remaining gaps (documented — not READY blockers for contract)

| Gap | Handling |
|-----|----------|
| Named `Production_Days` on hidden Oil Input | PEMS uses CaseInput C7; document GM name mapping for import parity checks |
| Full nested IF field lists | EXTRACTED in catalogue; implement selector from field header table |
| OML123_Oil_S1 hidden series | Out of input scope; engine may need formula-faithful pull for full GTC |
| Reservoir STOIIP/GIIP internal | Interface only until M03 READY |
| Truncation-free every Block formula | Catalogue is authority; contract cites groups |

**No unresolved critical-path Production literals** in register (all RESOLVED).

---

## 12. Readiness gate

| # | Criterion | Met? |
|---|-----------|------|
| 1 | Implementation-relevant parameters identified | **Yes** |
| 2 | GM cells/ranges mapped | **Yes** |
| 3 | Inputs linked to Ec_IO | **Yes** §2 |
| 4 | Derived values identified | **Yes** |
| 5 | Units documented | **Yes** |
| 6 | Time basis documented | **Yes** §5 |
| 7 | Production logic groups documented | **Yes** G1–G5 (+G6 deferred) |
| 8 | Oil/gas streams mapped | **Yes** §6 |
| 9 | Dependencies documented | **Yes** §7 |
| 10 | Downstream consumers documented | **Yes** |
| 11 | GTC comparison points established | **Yes** §9 |
| 12 | Traceability complete | **Yes** §10 |
| 13 | No unresolved implementation-critical ambiguity | **Yes** (gaps §11 scoped) |
| 14 | No calculation code written | **Yes** |

# **PRODUCTION = READY**

**Means:** Specification sufficient to implement production services against GM formulas and CaseInput.  
**Does not mean:** Costs/FLGT/NCF READY or numerical VALIDATED.
