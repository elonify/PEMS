# M07 — Hydrocarbon Tax / CIT / NCF Cashflow

**Status:** **READY** for implementation of CR/NCF services per contract (not PEMS numerical VALIDATED)  
**Authoritative contract:** `docs/02_SPECIFICATIONS/modules/CR_NCF_CONTRACT.md`  
**Visible sheets:** CR Econ, HT_NCF_Oil, CIT_NCF_Oil/Gas, Project_NCF, equity NCF sheets  
**Hidden:** HT_NCF, CIT_NCF, Project_NCF_Con — ignore for input; do not modify  

**Closed:** AU14 `#NUM!` EXPECTED no-sign-change IRR · Equity C4 INPUT  

---

## Sequence (evidenced)

```text
FLGT + Cap_Allow + Fiscal Terms
  → CR Econ (CRL, profit oil, cost recovery)
  → HT_NCF_Oil / CIT_NCF_Oil / CIT_NCF_Gas
  → Project_NCF
  → Equity_* × Equity Dash!C4
  → RESULTS / Ec_IO hub
```

---

## Ready for implementation?

| Slice | Status |
|-------|--------|
| CR/NCF contract | **READY** |
| RESULTS module | PARTIAL |
| Numerical VALIDATED vs GM | **Not yet** |
