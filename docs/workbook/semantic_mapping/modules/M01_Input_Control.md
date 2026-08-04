# M01 — Input / Control (Semantic Map)

**Status:** **Ec_IO CaseInput READY** for implementation of input layer; Oil/Gas Input grids remain out of visible-scope readiness  
**PEMS target module:** Input system / Project + Scenario configuration / Ec_IO hub  
**Sheets:** Oil Input, Gas Input, START, Checklist, Model Map, Master, Ec_IO, Equity Dash (share)  
**Authoritative contract:** `docs/02_SPECIFICATIONS/modules/EC_IO_PARAMETER_CONTRACT.md`

**Scope note:** **Oil Input**, **Gas Input**, and **Model Map** are **hidden** — **ignored** for literal/input classification and readiness (`SCOPE_VISIBLE_SHEETS_ONLY.md`). Do not modify. Focus input mapping on **visible** Ec_IO, Checklist, Master, START, Equity Dash share.

**CLOSED — Equity Dash Share = INPUT** (`C4`); **C5** = DERIVED `=C6-C4`. See `EQUITY_DASH_SHARE_INPUT.md`.

---

## 1. Excel worksheets

| Sheet | State | Role |
|-------|-------|------|
| Ec_IO | visible | Case drivers + results hub — **CaseInput READY** |
| Equity Dash | visible | Equity share INPUT C4 (+ loan block PARTIAL elsewhere) |
| START / Checklist / Master | visible | Navigation / QA / labels — not primary CaseInput |
| Oil/Gas Input | hidden | Ignored for readiness |

---

## 2–7. Inputs / outputs

- **CaseInput parameters:** full dictionary in `EC_IO_PARAMETER_CONTRACT.md` §3  
- **Fiscal Terms_PIA:** LAW TABLE — interface only (§6 of contract)  
- **Hub outputs:** KPI mirrors on Ec_IO (not inputs)  
- **Sensitivity tables:** PRESENTATION / DEFERRED  

---

## 8–15. Module / validation

- Manual + import → single CaseInput → single validation path  
- GTC-001 ingestion compare points defined (contract §7)  
- VALIDATED (numerical PEMS vs GM): **not yet**

---

## Ready for implementation?

| Slice | Status |
|-------|--------|
| Ec_IO + Equity share CaseInput | **READY** |
| Hidden Oil/Gas input grids | **NO** (out of scope) |
| Full economic calc | **NO** (other modules) |
