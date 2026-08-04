# FLGT / Royalties Contract — Implementation Readiness

**Status:** **READY** (fiscal application specification only — not calculation VALIDATED)  
**Active GM SHA (approved):** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Module:** M-CP-04 / M06 Royalty + Front-End Loaded Government Take  
**GM modified:** **No**  
**Calculation code under this task:** **None**

**Do not reopen:** GM approval CLOSED · Equity INPUT · Fiscal LAW TABLE · Ec_IO/Production/Costs READY · 829/829 · AU14 · ADR-0010  

**Upstream contracts:**  
- `EC_IO_PARAMETER_CONTRACT.md`  
- `PRODUCTION_PROFILE_CONTRACT.md`  
- `COSTS_PARAMETER_CONTRACT.md`  
- `FISCAL_TERMS_PIA_LAW_TABLE.md` (**authoritative rates/tiers**)  

**Evidence:** catalogue · `FLGT_ROYALTIES_EVIDENCE_EXTRACT.json` · GTC-001  

**Sheets:** `Royalties` (visible) · `FLGT` (visible)  

---

## 0. What READY means

| Includes | Excludes |
|----------|----------|
| Royalty rate application groups (oil/gas/price) | Writing PEMS royalty engine code |
| FLGT front-end take surface (AB–AI, ERR) | Re-defining Fiscal Terms_PIA tables |
| CaseInput / Production / Costs interfaces | Full CR/NCF tax engine READY |
| GTC comparison for royalty/$mm / ERR | Claiming PEMS-vs-GM VALIDATED |
| Analysis sensitivity cells as **formula refs only** | Promoting Analysis to CaseInput |

---

## 1. Architecture (evidenced)

```text
Fiscal Terms_PIA (LAW TABLE — rates, tiers, HCDT/NDDC %, rentals)
        │
        ▼  (lookup / match only — do not rewrite tables)
┌───────────────────┐     CaseInput: terrain G20, gas util G21,
│ Royalties sheet   │     oil price C12, escalator C14, years C5/D22/D29
│ rate engine       │◄──── Production: Prod_Summary volumes/years
│ oil I/J/K/L       │     Analysis!$N$12,$N$15 (sensitivity multipliers —
│ gas N             │       not CaseInput; present in GM formulas)
│ price S on R      │
└─────────┬─────────┘
          │ rates / price series (380 FLGT←Royalties refs)
          ▼
┌───────────────────┐
│ FLGT sheet        │◄──── Costs: Block_TC / Cap_Allow Gas (HCDT/NDDC bases)
│ revenues W/X/Y    │
│ royalties AB/AC/AD│
│ rentals AE        │
│ HCDT/NDDC Z–AH    │
│ ERR AM = AL/Y     │
└─────────┬─────────┘
          ▼
   Ec_IO G11/G15 · CR Econ · HT/CIT/Project NCF · RESULTS
```

**Boundary:** All **rate values and tier thresholds** originate in **Fiscal Terms_PIA**. Royalties/FLGT only **select and apply** them.

---

## 2. Fiscal law interface

```text
Fiscal Terms_PIA
   ↓  terrain / production / price / gas-utilization match
applicable rate or tier parameters (LAW_TABLE cells)
   ↓
Royalties rate formulas (I/J/K/L, N, S)
   ↓
FLGT $mm application (rate × revenue base)
   ↓
CR/NCF / RESULTS / Ec_IO
```

| Law area (PIA sheet) | Consumer | Application pattern |
|----------------------|----------|---------------------|
| Oil royalty tiers T18–W26 | Royalties I/J/K/L | Match Ec_IO!G20 terrain; sliding on daily oil B* (mb/d) vs V*/1000 |
| Gas royalty U29–V30 | Royalties N* | Match Ec_IO!G21 Dom vs Out; rates 0.05 / 0.025 |
| Price royalty U36–U38 + 0.02 escalator notes | Royalties S* | Nominal price R* vs escalated band thresholds |
| HCDT 0.03 (T72) | FLGT Z*, AF* | × cost bases Block_TC / Gas |
| NDDC 0.03 (T73) | FLGT AG*, AH* | × cost bases / Cap_Allow Gas |
| Concession rental Z11/Z12 | FLGT AE* | When production present |
| Cost recovery / profit oil / HT-CIT dual tier | **Not FLGT core** | Downstream CR/NCF (PARTIAL modules) |

**Do not** store royalty rates as ordinary CaseInput. CaseInput supplies **selectors** (terrain, gas util, prices).

---

## 3. Royalties sheet — calculation groups

### 3.1 Volume / stream inputs (DERIVED from Production)

| Col | Label | Source | Unit |
|-----|-------|--------|------|
| A | Year | Prod_Summary!S* | year |
| B | Daily oil | Prod_Summary!T* | mb/d |
| C | Annual oil | Prod_Summary!U* | mmbbls |
| D | Cum oil | Prod_Summary!V* | mmbbls |
| E | Daily gas | Prod_Summary!W* | mmscf/d |
| F | Annual gas | Prod_Summary!X* | bscf |
| G | Cum gas | Prod_Summary!Y* | bscf |

### 3.2 Selectors (CaseInput)

| Cell / series | Source | Meaning |
|---------------|--------|---------|
| I3 | Ec_IO!G20 | Terrain for oil royalty |
| N3 | Ec_IO!G21 | Gas utilization (In-Country Dom vs Out) |
| Oil price path | Ec_IO!C12, C14, C5, D22, D29 | Real/nominal price construction |
| S4 | Ec_IO!C14 | Escalation factor feed for price royalty bands |

### 3.3 Oil production royalty rates (I/J/K/L)

| Col | Terrain column | Law match | Semantics |
|-----|----------------|-----------|-----------|
| I | Onshore | Fiscal Terms_PIA T18/V18–V20/W18–W20 | Sliding average rate on daily oil B* (zero if B=0) |
| J | Shallow | T21/V21–V23/W21–W23 | Same structure (GTC sample J5→0.05) |
| K | Deep | T24/V24–V25/W24–W25 | Two-band deep offshore |
| L | Frontier | T26/W26 | Flat when terrain matches |

**Classification:** rates = **LAW_TABLE application (FORMULA)**; not user INPUT.  
**Exact I5** (Onshore pattern) — full formula in catalogue; uses progressive band average when production crosses thresholds.

### 3.4 Gas royalty rate (N)

`N5=IF(E5=0,0,IF(Ec_IO!$G$21='Fiscal Terms_PIA'!$U$29,'Fiscal Terms_PIA'!$U$30,'Fiscal Terms_PIA'!$V$30))`  
→ Out-Country **0.05** vs In-Country **0.025** (LAW_TABLE). Zero if no daily gas.

### 3.5 Price royalty rate (S) on nominal oil price (R)

| Step | Cell | Formula role |
|------|------|--------------|
| Real oil price | P* | `Ec_IO!$C$12*(1+Analysis!$N$12)` (zero if no oil and year≠D29) |
| Escalation factor | Q* | `((1+Ec_IO!$C$14*(1+Analysis!$N$15))^(A-Ec_IO!$C$5))*(A<Ec_IO!$D$22)` |
| Nominal oil price | R* | `P*Q` |
| Price royalty rate | S* | Bands vs Fiscal Terms_PIA U36/U38 escalated from 2020; 0 / interpolate / 10% |

**Analysis!$N$12 / $N$15:** sensitivity multipliers present in GM — **not** Ec_IO CaseInput. Base GTC uses as-saved Analysis values. Implementation: optional sensitivity layer; default identity (0 adder) only if catalogue shows zero — **do not invent**; import as-saved for GTC parity.

### 3.6 Royalties outputs

Royalties sheet primarily outputs **rates and price series** consumed by FLGT (not $mm royalty totals).  
$mm application is on **FLGT** (rate × revenue).

---

## 4. FLGT sheet — calculation groups

### 4.1 Timeline

| Rows | Role |
|------|------|
| A5–A7 | Lead years (A5=A6-1…) before Prod_Summary alignment |
| A8+ | `A8=Prod_Summary!S5` … production-aligned years |
| Rates | `I8=Royalties!I5`, `J8=Royalties!J5`, … (offset map) |

### 4.2 Revenues

| Col | Label | Formula pattern | Unit |
|-----|-------|-----------------|------|
| R | Nominal oil price | from Royalties path / parallel | $/bbl |
| U | Nominal gas price | Ec_IO gas price path (C17 + Analysis N13 pattern) | $/mscf |
| W | Nominal Oil Revenue | `W=R*C` (price × annual oil mmbbls) | $mm |
| X | Nominal Gas Revenue | `X=U*F` | $mm |
| Y | Nominal Total Revenue | `Y=W+X` | $mm |

### 4.3 Front-loaded government take components (annual)

| Col | Label (row 3) | Application (evidenced) | Law / cost source |
|-----|---------------|-------------------------|-------------------|
| Z | HCDT Fund Gas S.263(1)(h) | `IF(AH=0,0,Block_TC_Gas!FX* * Fiscal!$T$72)` | LAW 0.03 × gas cost base |
| AA | Bonuses | (series; SUM AA51=0 on GTC) | Law bonus tables when triggered |
| AB | Oil Royalty S.263(1)(b) | Terrain-select I/J/K/L rate × **W** oil revenue | Rates from Royalties←LAW |
| AC | Gas Royalty S.263(1)(b) | `N*X` gas rate × gas revenue | Royalties N←LAW |
| AD | Price Royalty S.263(1)(b) | `S*W` price rate × oil revenue | Royalties S←LAW |
| AE | Concession rentals S.263(1)(a) | Rental × Q when B≠0 | Fiscal Z11/Z12 |
| AF | HCDT Fund Oil | `(Block_TC!GB+ET)*T72` when AB≠0 | LAW 0.03 × oil cost |
| AG | NDDC Oil | `T73 * (Block_TC FY+FZ+GA+GB+ET…)` | LAW 0.03 × cost sum |
| AH | NDDC Gas | `T73 * Cap_Allow Gas!FJ*` | LAW 0.03 × gas allow base |
| AI | Total front-loaded | `SUM(Z:AH)` | DERIVED |
| AL | Royalty $mm sum | `AB+AC+AD` | DERIVED |
| AM | **ERR** | `AL/Y` effective royalty rate | DERIVED |
| AN–AP | Loan / PPMT / IPMT | Equity Dash loan bridge (peripheral to base royalty) | Equity Dash |

### 4.4 Totals (GTC-critical)

| Cell | Meaning | GTC expected |
|------|---------|--------------|
| W51 | Sum oil revenue | 1099.88947281873 |
| X51 | Sum gas revenue | 55.0351504205685 |
| Y51 | Sum total revenue | 1154.9246232393 |
| AB51 | Sum oil royalty $mm | 61.3138177169515 |
| AC51 | Sum gas royalty $mm | 1.37587876051421 |
| AD51 | Sum price royalty $mm | 0 |
| AL51 | Sum AB+AC+AD | 62.6896964774657 |
| AM51 | ERR = AL51/Y51 | 0.0542803358903504 |
| AI51 | Total FLGT components | 93.5101437605859 |
| AE51 / AF51 / AG51 / AH51 / Z51 | Rentals, HCDT, NDDC sums | as-saved (catalogue) |

---

## 5. Classification summary

| Item | Class |
|------|-------|
| Fiscal Terms_PIA rates/tiers | **LAW_TABLE** |
| Ec_IO terrain, gas util, prices, escalator, years | **INPUT / ASSUMPTION** (CaseInput) |
| Prod_Summary volumes | **DERIVED** (Production) |
| Block_TC / Cap_Allow Gas cost bases for HCDT/NDDC | **DERIVED** (Costs) |
| Royalty rates I/J/K/L/N/S | **FORMULA** applying LAW_TABLE |
| Revenues W/X/Y | **DERIVED** |
| Royalty $mm AB/AC/AD, ERR AM | **OUTPUT / DERIVED** |
| Analysis N12/N13/N15 | **Sensitivity (not CaseInput)** — import for GTC parity |

---

## 6. Upstream interfaces

| Upstream | Provides | FLGT/Royalties use |
|----------|----------|-------------------|
| Ec_IO | G20 terrain, G21 gas util, C12 oil price, C17 gas price, C14 escalator, C5 start, D22/D29 | Selectors & price construction |
| Production | Prod_Summary S–Y series | Volumes & years |
| Costs | Block_TC escalated/OPEX/ET, Cap_Allow Gas FJ, Block_TC_Gas FX | HCDT/NDDC bases |
| Fiscal Terms_PIA | All rates/tiers/T72/T73/Z11/Z12 | Law parameters only |
| Analysis | N12/N15 (oil), N13 (gas path) | Sensitivity multipliers in price formulas |
| Equity Dash | M4/R4 loan; C4 scales RESULTS royalties display | Not royalty rate engine |

### Dependency order

```text
Ec_IO
  ↓
Production
  ↓
Costs ─────────────────────────┐
  ↓                            │
Fiscal Terms_PIA (law load)    │
  ↓                            │
Royalties (rates)              │
  ↓                            │
FLGT (apply rates + FLGT items)◄┘ cost bases
  ↓
CR / NCF (PARTIAL)
  ↓
RESULTS
```

**Circularity:** Ec_IO displays FLGT!AM51 / AB+AC+AD (G11/G15) — **hub presentation**, not CaseInput. No calc-loop for base royalty if Ec_IO drivers are inputs and FLGT is downstream.

---

## 7. Units and timing

| Stream | Daily | Annual | Money |
|--------|-------|--------|-------|
| Oil | mb/d | mmbbls | $mm revenue / royalty |
| Gas | mmscf/d | bscf | $mm |
| Price | $/bbl, $/mscf | — | |
| Rates | fraction | — | |
| Time | Annual project years aligned to Prod_Summary from FLGT A8 | Lead years A5–A7 pre-align | |

**No invented unit conversions** beyond workbook formulas (e.g. law V*/1000 vs mb/d).

---

## 8. Edge conditions (evidenced only)

| Condition | Evidence |
|-----------|----------|
| Zero oil production | B=0 → oil royalty rates 0; related AB path 0 |
| Zero gas production | E=0 → gas rate 0; AC=0 |
| Zero/blank price / no oil year | P formula forces 0 when B=0 (except D29 special) |
| Terrain mismatch | Non-matching I/J/K/L branches → 0 |
| Gas util Dom vs Out | N selects U30 vs V30 |
| Price below royalty band | S→0% |
| HCDT/NDDC when no royalty/cost | IF guards (AB=0, AH=0) |
| ERR when Y=0 | IFERROR(AL/Y,0) |
| Analysis sensitivity | Nonzero N12/N15 would scale prices — GTC uses as-saved |

---

## 9. Downstream consumers

| Consumer | What it takes |
|----------|----------------|
| Ec_IO G11 | ERR = FLGT!AM51 |
| Ec_IO G15 | Total royalty $mm = AB51+AC51+AD51 |
| Ec_IO G8 / revenues | FLGT W51/X51 (oil/gas revenue) |
| CR Econ | FLGT annual series (323 refs) |
| HT_NCF / CIT_NCF / Project_NCF | FLGT royalties & FLGT items (hundreds of refs) |
| RESULTS Equity | Royalty displays; production×equity for some labels |
| Block_TC | Few reverse refs from Royalties (37) — timing/coupling in catalogue |

---

## 10. GTC comparison contract

| GM cell | Expected | Meaning | PEMS target |
|---------|----------|---------|-------------|
| FLGT!AB51 | 61.3138177169515 | Oil royalty $mm total | Royalty oil output sum |
| FLGT!AC51 | 1.37587876051421 | Gas royalty $mm total | Royalty gas output sum |
| FLGT!AD51 | 0 | Price royalty $mm total | Price royalty sum |
| FLGT!AL51 | 62.6896964774657 | AB+AC+AD | Combined royalty $mm |
| FLGT!AM51 | 0.0542803358903504 | ERR | Effective royalty rate |
| FLGT!W51 | 1099.88947281873 | Oil revenue | Gross oil revenue |
| FLGT!X51 | 55.0351504205685 | Gas revenue | Gross gas revenue |
| FLGT!Y51 | 1154.9246232393 | Total revenue | Gross total revenue |
| FLGT!AI51 | 93.5101437605859 | Total FLGT AI | Front-loaded take total |
| Ec_IO!G11 | 0.0542803358903504 | =FLGT!AM51 | Hub ERR |
| Ec_IO!G15 | 62.6896964774657 | =AB+AC+AD | Hub royalties |
| Royalties!J5 | 0.05 | Sample shallow oil rate | Rate engine check |
| Royalties!N5 | 0.025 | Dom gas rate | Rate engine check |

Annual series: `formula_cached_results_all.csv` for Royalties!* and FLGT!*.  
**Do not claim VALIDATED** until PEMS run matches.

---

## 11. Traceability

```text
Excel cell/range
  → LAW_TABLE cell or CaseInput / Production / Costs
  → Royalties rate group or FLGT component
  → OUTPUT $mm / ERR
  → NCF / RESULTS / Ec_IO hub
  → GTC point (§10)
```

---

## 12. Remaining gaps (scoped)

| Gap | Handling |
|-----|----------|
| Full text of every year-row formula | Catalogue authority; groups documented |
| Bonus triggers AA* | SUM=0 on GTC; law bonus tables when applicable — implement via catalogue |
| Loan AN–AP | Equity Dash peripheral; not core royalty READY scope |
| Analysis sensitivity semantics | Import as-saved; not primary CaseInput |
| Production allowance tables on Fiscal Terms | May affect other fiscal paths; royalty formulas above are production/price sliding as written |

**No unresolved critical-path literals** blocking FLGT (register essentially clean).

---

## 13. Readiness gate

| # | Criterion | Met? |
|---|-----------|------|
| 1 | Implementation-relevant FLGT/Royalties parameters identified | **Yes** |
| 2 | Fiscal-law interfaces completely mapped | **Yes** §2 |
| 3 | Fiscal Terms_PIA remains authoritative | **Yes** |
| 4 | Royalty logic mapped | **Yes** §3 |
| 5 | FLGT logic mapped | **Yes** §4 |
| 6 | Inputs vs derived distinguished | **Yes** §5 |
| 7 | Volume dependencies mapped | **Yes** |
| 8 | Price dependencies mapped | **Yes** |
| 9 | Cost-base dependencies mapped | **Yes** (HCDT/NDDC) |
| 10 | Units documented | **Yes** §7 |
| 11 | Timing documented | **Yes** |
| 12 | Downstream consumers documented | **Yes** §9 |
| 13 | Dependency order documented | **Yes** §6 |
| 14 | GTC comparison points established | **Yes** §10 |
| 15 | No unresolved implementation-critical ambiguity | **Yes** (§12 scoped) |
| 16 | No calculation code written | **Yes** |

# **FLGT / ROYALTIES = READY**

**Means:** Spec sufficient to implement royalty rate application + FLGT front-end take against law table + upstream contracts.  
**Does not mean:** CR/NCF/RESULTS READY or numerical VALIDATED.
