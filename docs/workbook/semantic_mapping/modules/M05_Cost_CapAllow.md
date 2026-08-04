# M05 — Cost / Capital Allowance

**Status:** **READY** for implementation of cost services per contract (not PEMS numerical VALIDATED)  
**Sheets:** Block_TC, Block_TC_Gas, Cap_Allow, Cap_Allow Gas  
**Authoritative contract:** `docs/02_SPECIFICATIONS/modules/COSTS_PARAMETER_CONTRACT.md`  
**Upstream:** Ec_IO READY · Production READY · Fiscal LAW TABLE (CA rates)

---

## Evidence summary

| Sheet | Role |
|-------|------|
| Block_TC / Block_TC_Gas | Per-field annual $mm: Exploration, CAPEX Wells/Facilities, OPEX, Abandonment |
| Cap_Allow / Cap_Allow Gas | Copy/select streams; discount at Ec_IO C15; CA rates FR; hub totals FI/FK/FL/FP/FQ |

**Downstream:** Ec_IO N16–S18, CR Econ, HT/CIT/Project NCF, FLGT, RESULTS unit costs.

---

## Ready for implementation?

| Slice | Status |
|-------|--------|
| Costs parameter + Cap_Allow contract | **READY** |
| Full multi-field cost GUI | Deferred (import + selected field) |
| Numerical VALIDATED vs GM | **Not yet** |
