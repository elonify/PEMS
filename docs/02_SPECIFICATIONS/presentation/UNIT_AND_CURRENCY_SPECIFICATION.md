# Unit and Currency Specification

**Status:** **READY** (presentation metadata)  
**Source GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Evidence:** visible labels + RESULTS/Ec_IO/Block_TC/Prod_Summary contracts  
**GM modified:** **No**

---

## 1. Currency

| Convention | Evidence | PEMS requirement |
|------------|----------|------------------|
| **USD `$`** | Number formats `[$$-409]…`, `"$"* #,##0.00`; labels `$mm`, `$MM`, `$/bbl` | Primary currency is US dollar presentation |
| **Scale $mm / $MM** | Block_TC/Cap_Allow/FLGT/CR/NCF/RESULTS labels | Most cashflow economics in **millions of dollars** |
| **Absolute `$` on RESULTS cost/revenue lines** | RESULTS H16–J18 currency formats + `$MM` column labels | Display currency accounting; label indicates $MM scale for those blocks |
| **No multi-currency FX** | Not evidenced as CaseInput | Do not invent FX conversion |

**Negative money:** accounting minus or parentheses; some formats **red** negatives (`[Red]`).

---

## 2. Units catalogue (visible GM)

| Displayed unit | Meaning | Example sources |
|----------------|---------|-----------------|
| `$mm` / `$MM` | Million USD | Block_TC B3, FLGT W4, CR Econ E4, RESULTS labels |
| `$/bbl` | USD per barrel | Ec_IO B12 “Crude Oil Price, $/bbl” |
| `$/Mscf` | USD per thousand scf | Ec_IO B17 “Gas Price, $/Mscf” |
| `mb/d` | Thousand barrels per day | Prod_Summary / Block_Oil / Royalties |
| `mmbbls` | Million barrels | Annual/cum oil |
| `mmscf/d` | Million scf per day | Gas daily |
| `bscf` | Billion scf | Annual/cum gas |
| `Mmboe` / `S/Boe` | Million boe; $/boe unit costs | RESULTS N23, H19 labels |
| `%` | Percent / rate | Equity, hurdle, royalties, take stats |
| `Years` / `yrs` | Time | Payout, life, decline t1/t2 |
| `Days` | Days/year | Ec_IO C7, PP C9 |
| `BOPD` / `Mscf/d` | Production Profile rate labels | Production Profile D12 etc. |
| `scf/bbl` | GOR | Production Profile G5 |

**Do not invent conversions** (e.g. boe factors) beyond workbook formulas (e.g. Prod_Summary Y48=5.804).

---

## 3. Scale rules for PEMS UI

| Domain | Internal model (from module contracts) | Label on GM |
|--------|----------------------------------------|-------------|
| NCF / tax / royalty totals | $mm numeric | $mm |
| RESULTS unit costs | $ per boe (absolute currency format) | Unit CAPEX/OPEX/TC, S/Boe |
| Oil price | $/bbl | Ec_IO |
| Gas price | $/Mscf | Ec_IO |
| Rates | fraction 0–1 | shown as % |

---

## 4. LEVEL classification

| Rule | Level |
|------|-------|
| Unit and $mm vs $/bbl vs fraction meaning | **L1 Semantic** |
| Showing unit next to field | **L2 Functional** |
| Exact Excel accounting format string | **L3 Visual** |
