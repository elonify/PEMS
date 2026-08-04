# M04 — Production

**Status:** **READY** for implementation of production services per contract (not PEMS numerical VALIDATED)  
**Sheets:** Production Profile, Block_Oil Data, Block_Gas Data, Prod_Summary  
**Hidden (ignore for input):** OML123_Oil_S1  
**Authoritative contract:** `docs/02_SPECIFICATIONS/modules/PRODUCTION_PROFILE_CONTRACT.md`  
**Upstream CaseInput:** `EC_IO_PARAMETER_CONTRACT.md` (READY)

---

## Evidence summary

| Sheet | Role |
|-------|------|
| Production Profile | Analytical build-up / plateau / decline; STOIIP/GIIP mode; AG via GOR |
| Block_Oil / Block_Gas | Multi-field daily & annual series; field select via Ec_IO G18/G19 |
| Prod_Summary | Assembled oil/gas timelines; life AF26; totals V47/Y47–Y50 |

Consumers: Royalties, FLGT, Cap_Allow, RESULTS Equity, Ec_IO project life (C6).

---

## Ready for implementation?

| Slice | Status |
|-------|--------|
| Production profile + summary contract | **READY** |
| Full multi-field UI for every OML column | Deferred (selector + import parity) |
| Numerical VALIDATED vs GM | **Not yet** |
