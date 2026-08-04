# Critical-Path Dependency Order (Implementation)

**Active GM identity:** Confirmed-2026-08-03 SHA `D07560CA…BFEA`  
**Claim level:** Sufficient for **first-module sequencing** — **not** a proven complete workbook-wide graph.

Sources: active catalogue sheet edges (prior extract), RESULTS/FLGT/CR Econ formula references, visible-only scope.

---

## Target chain

```text
INPUT / PARAMETERS (visible)
  Ec_IO, Equity Dash, Fiscal Terms_PIA
        ↓
PRODUCTION
  Production Profile, Block_Oil Data, Block_Gas Data → Prod_Summary
        ↓
COSTS / CAPITAL ALLOWANCE
  Block_TC, Block_TC_Gas → Cap_Allow, Cap_Allow Gas
        ↓
ROYALTY / FLGT
  Royalties → FLGT
        ↓
FISCAL BRIDGE / NCF (visible)
  CR Econ → HT_NCF_Oil, CIT_NCF_Oil, CIT_NCF_Gas → Project_NCF
  Equity scaling (Equity Dash) → HT/CIT/Equity_NCF_Con
        ↓
RESULTS
  RESULTS Equity (KPIs)
```

---

## Evidenced transitions

| From | To | Evidence |
|------|-----|----------|
| Ec_IO | Cap_Allow*, NCF, RESULTS | High formula ref counts; RESULTS links Ec_IO labels/rates |
| Equity Dash | Equity NCF sheets, RESULTS | High refs (e.g. equity scale); C4 share literal |
| Fiscal Terms_PIA | Royalties, FLGT, CR Econ | Formula refs to fiscal tables |
| Block_Oil/Gas / Prod | Royalties, FLGT, RESULTS | Prod_Summary aggregates in RESULTS |
| Block_TC* | Cap_Allow* | Very high ref counts |
| Cap_Allow*, FLGT, CIT_NCF_Oil | CR Econ | CR Econ headers/formulas |
| CR Econ | HT/CIT/Project NCF families | Downstream refs in prior graph |
| HT_NCF_Oil Equity, Equity_NCF_Con, FLGT, Prod_Summary | RESULTS Equity | Direct formula links in KPI pack |
| AF series on Project_NCF | AU12 IRR numeric | Sign change present |
| AK series on Project_NCF | AU14 `#NUM!` | Blank series — expected no-IRR |

---

## Unresolved dependencies (recorded)

| Item | Status |
|------|--------|
| Hidden sheet intermediates still referenced by visible formulas | Catalogue retained; not input scope |
| Exact cell-level order inside Cap_Allow / Block_TC arrays | Not fully proven — implement by validated formula groups |
| Analysis sensitivity feedback into Royalties/FLGT | DEFERRED with Analysis scope |
| Full workbook-wide acyclic order | **Not claimed** |

---

## Implementation module order (first wave)

1. Foundation / domain base (no economics)  
2. Input parameters object model (Ec_IO + Equity Dash + Fiscal Terms tables as data)  
3. Production → Prod_Summary  
4. Costs → Cap_Allow  
5. Royalties → FLGT  
6. CR Econ → visible NCF  
7. Economic metrics / RESULTS KPIs (incl. no-sign-change IRR)  

Each step requires module READY gate before coding that step’s economics.
