# Fiscal Terms_PIA — Law / Regulatory Fiscal Rule Source

**Status:** Domain decision **CLOSED — LAW TABLE**  
**Classification:** `LAW_TABLE` / regulatory fiscal rule source  
**Not:** ordinary user-entered project inputs  
**GM:** Confirmed-2026-08-03 SHA `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Sheet:** `Fiscal Terms_PIA` (visible)  
**Authority:** `SCOPE_DECISIONS.md` §D  

**Do not modify the Golden Master.**

---

## 1. Table / rule identity

| Field | Value |
|-------|--------|
| Identity | **PIA (Petroleum Industry Act 2021) fiscal terms tables** |
| Workbook sheet | `Fiscal Terms_PIA` |
| PEMS representation | Authoritative **fiscal-rule / regime reference data** for the fiscal calculation layer |
| User input? | **No** — not ordinary case inputs |
| Change control | Regime/version update process only (controlled load), not free-form scenario typing |

---

## 2. Documented rule blocks (from workbook labels — EXTRACTED)

The following blocks are **present as labeled tables** on the sheet. Rates/thresholds below are **as stored in the Golden Master** for documentation/traceability, not invented.

### 2.1 Rentals — License/Lease by terrain (S1–X14 area)

| License | Terrain examples | Initial / extended duration (yrs) | Area notes |
|---------|------------------|-----------------------------------|------------|
| PEL | Onshore, Shallow, Deep Offshore, Frontier | 3/3, 3/3, 5/5, … | sqKm columns |
| PPL | Onshore, Shallow, Deep Offshore, Frontier | 3/3 … | area e.g. 350–1500 sqKm |
| PML | Onshore, Shallow, Deep Offshore, Frontier | 20 yrs | 40% of PPL notes |

### 2.2 Oil royalties (S16+)

| Terrain | Production band (BOPD) | PIA rate | Mechanism |
|---------|------------------------|----------|-----------|
| Onshore | 0–5000 / 5001–10000 / Above 10000 | 0.05 / 0.075 / 0.15 | Sliding |
| Shallow Water (&lt;200m) | 0–5000 / 5001–10000 / Above 10000 | 0.05 / 0.075 / 0.125 | Sliding |
| Deep Offshore (&gt;200m) | 0–50000 / Above 50000 | 0.05 / 0.075 | Sliding |
| Frontier Basin | (flat) | 0.075 | Flat |

### 2.3 Gas royalties (S28+)

| Terrain | Out-Country | In-Country (Dom Gas) | Pre-PIA (where shown) |
|---------|-------------|----------------------|------------------------|
| Onshore | 0.05 | 0.025 | 0.07 |
| Shallow Water | 0.05 | 0.025 | 0.05 |
| Deep Offshore | 0.05 | 0.025 | 0.05 |

### 2.4 Price royalties (S34+)

| 2020 price level $/bbl (MIN–MAX) | PIA rate | Mechanism notes |
|----------------------------------|----------|--------|-----------------|
| 0–50 | 0 | Linear interpolation bands / pre-PIA notes |
| 51–100 | 0.05 | |
| 101–150 | 0.1 | |
| Frontier | No royalty by price | |
| Price escalation | 0.02 | |

### 2.5 Production allowances (S42+)

Terrain-based allowances e.g. min($8/Bbl, 20% of Price) vs cum. production thresholds (50 / 100 / 500 MMbbl bands); converted OML allowance min($2.5/Bbl, 20% of Price).

### 2.6 Dual tier taxation (S53+)

| Tax | Before appraisal | Upon appraisal / discovery | Upon development / production |
|-----|------------------|----------------------------|-------------------------------|
| HT | 0 | 0.15 | 0.3 |
| CIT | 0.3 | 0.3 | 0.3 |

### 2.7 PSC cost oil & profit oil (S58+)

| Item | Values (as labeled) |
|------|---------------------|
| Cost recovery limit | New Acreage 0.7; Converted OML 0.6 |
| HG profit oil share vs cum. production (mmbbls) | Tiers ≤50→0.05 … &gt;1500→0.45 (New Acreage table) |

### 2.8 Other salient provisions (S69+)

| Provision | Parameter (as labeled) |
|-----------|------------------------|
| Cost price ratio | 0.65 of gross revenue |
| Cost consolidation | Across all terrains |
| HCDT | 0.03 of preceding year OPEX |
| NDDC | 0.03 of total annual budget |
| NC | 0.01 of every contract |
| Education tax | 0.04 of assessable profit |
| Capital allowance | Y1–4: 0.2; Y5: 0.19 (+ retention note) |
| Bonus types | Signature, Production, Renewal |

---

## 3. Selection / application logic (UNDERSTOOD at interface level)

Application of rows depends on **case attributes** from elsewhere (e.g. Ec_IO terrain / acreage type / production rate / price), not on re-typing the law table:

```text
Case attributes (INPUT / case setup)
        ↓
Select applicable Fiscal Terms_PIA row(s) / tier(s)
        ↓
Royalties, FLGT, CR Econ, HT/CIT NCF (consumers)
```

Exact formula-level selection remains in the **formula catalogue** for each consumer cell (EXTRACTED); full VALIDATED application is post-implementation.

---

## 4. Calculations that consume the rules (downstream)

| Consumer sheet (visible critical path) | Use |
|----------------------------------------|-----|
| Royalties | Oil/gas/price royalty rates & mechanisms |
| FLGT | Front-end government take using royalty-related results |
| CR Econ | Cost recovery limit, profit oil splits (refs Fiscal Terms) |
| HT_NCF_Oil / CIT_NCF_* / Project_NCF / equity NCF | Tax stages, allowances, NCF fiscal components |
| RESULTS Equity | Aggregated royalty/tax KPIs |

Hidden NCF sheets may also reference tables; hidden sheets remain out of input scope.

---

## 5. Source traceability

| Artefact | Role |
|----------|------|
| `Fiscal Terms_PIA` worksheet | Source of truth for rates/thresholds on approved GM |
| Formula catalogue | Cell-level formulas referencing the sheet |
| GTC-001 | Expected outputs of **consumers**, not re-entry of law table as inputs |
| This document | Law-table semantic identity for PEMS |

---

## 6. PEMS architecture mapping

| Layer | Responsibility |
|-------|----------------|
| Domain | `FiscalRegime` / law-table entities (immutable for a GM version) |
| Configuration / resources | Load versioned PIA tables from approved package |
| Input UI | **Do not** present full Fiscal Terms_PIA as ordinary case form fields |
| Calculation | Fiscal engine **reads** law tables + case attributes |
| Validation | Compare fiscal outputs to GM; table identity matches GM SHA |

---

## 7. Understanding levels

| Aspect | Level |
|--------|-------|
| Sheet identity as LAW TABLE | **UNDERSTOOD** (PO closed) |
| Labeled rule blocks & rates as stored | **EXTRACTED** / documented |
| Full formula application graph | **EXTRACTED** (catalogue); not fully UNDERSTOOD group-by-group |
| VALIDATED vs PEMS | **Not yet** |

**Do not reopen:** LAW TABLE vs ordinary INPUT decision.
