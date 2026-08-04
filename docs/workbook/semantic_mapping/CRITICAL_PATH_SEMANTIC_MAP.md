# Critical-Path Semantic Map

**GM:** Confirmed-2026-08-03 `D07560CA…BFEA`  
**Scope:** Visible critical path only  
**Levels:** EXTRACTED | UNDERSTOOD | VALIDATED  

**VALIDATED** = PEMS vs GM comparison passed — **none yet** (no calc code).

---

## Understanding levels

| Level | Meaning |
|-------|---------|
| EXTRACTED | Present in catalogue / GTC |
| UNDERSTOOD | Business role established from labels + structure + deps without inventing rules |
| VALIDATED | Implementation compared to GM — **not available pre-implementation** |

---

## Path blocks

### 1. Ec_IO — Economic Model Input/Output (+ Equity Dash share)

| Item | Content |
|------|---------|
| Sheet | Ec_IO (visible); Equity Dash share (visible) |
| Role | Hub for case identity, rates, bridges to results; **equity share is user INPUT** |
| EXTRACTED | Yes — formulas + literals in active catalogue |
| UNDERSTOOD | **Yes for CaseInput** — `EC_IO_PARAMETER_CONTRACT.md`; **Equity Dash Share = INPUT** (PO **CLOSED**) |
| VALIDATED | No (PEMS-vs-GM numerical not run) |
| Inputs/assumptions | Full parameter catalogue; register RESOLVED (0 UNRESOLVED); sensitivity PRESENTATION deferred |
| Outputs | Values consumed by Cap_Allow, NCF, RESULTS; hub KPI mirrors not CaseInput |
| Downstream | Cap_Allow*, FLGT, NCF, RESULTS Equity |
| Edge cases | I/O hub also reads results sheets — not pure input |
| Validation | Manual+import contract; GTC ingestion compare §7 |
| PEMS module | `pems` input/domain + configuration |
| Status | **READY** (input/parameter contract) |

### 2. Fiscal Terms_PIA

| Item | Content |
|------|---------|
| Sheet | Fiscal Terms_PIA |
| Role | PIA **law/regulatory table** (not ordinary user inputs) |
| EXTRACTED | Yes |
| UNDERSTOOD | **Yes (taxonomy)** — PO: **CLOSED — LAW TABLE** (`SCOPE_DECISIONS` §D) |
| VALIDATED | No |
| Downstream | Royalties, FLGT, CR Econ, NCF |
| PEMS module | FiscalTerms / domain as **reference regime data** |
| Status | **PARTIAL** (structure UNDERSTOOD; formula-group detail still incomplete) |

### 3. Production Profile → Prod_Summary

| Item | Content |
|------|---------|
| Sheets | Production Profile, Block_Oil/Gas Data, Prod_Summary (OML123 hidden — ignore for input) |
| Role | Production forecasts & aggregates |
| EXTRACTED | Yes |
| UNDERSTOOD | **Yes for contract** — `PRODUCTION_PROFILE_CONTRACT.md` |
| VALIDATED | No |
| Validation | GTC V47/Y47/Y48/AF26 + series caches |
| PEMS module | production |
| Status | **READY** (spec — not numerical VALIDATED) |

### 4. Costs / Cap_Allow

| Item | Content |
|------|---------|
| Sheets | Block_TC, Block_TC_Gas, Cap_Allow, Cap_Allow Gas |
| Role | Technical cost → capital allowance / depr / opex lines into CR Econ |
| EXTRACTED | Yes (large formula volume) |
| UNDERSTOOD | **Yes for contract** — `COSTS_PARAMETER_CONTRACT.md` |
| VALIDATED | No |
| Validation | GTC FI/FK/FL/FP/FQ + Ec_IO N16–S18 |
| PEMS module | costs / capital_allowance |
| Status | **READY** (spec — not numerical VALIDATED) |

### 5. Royalties → FLGT

| Item | Content |
|------|---------|
| Sheets | Royalties, FLGT |
| Role | Royalty & front-end government take (Model Map terms) |
| EXTRACTED | Yes |
| UNDERSTOOD | **Yes for contract** — `FLGT_ROYALTIES_CONTRACT.md` |
| VALIDATED | No |
| Validation | FLGT AB51–AD51, AM51, W51/X51; Ec_IO G11/G15 |
| PEMS module | fiscal.royalty / flgt |
| Status | **READY** (spec — not numerical VALIDATED) |

### 6. CR Econ → visible NCF

| Item | Content |
|------|---------|
| Sheets | CR Econ, HT_NCF_Oil, CIT_NCF_*, Project_NCF, equity NCF sheets |
| Role | Cost recovery / profit oil bridge → tax NCF → project/equity NCF |
| EXTRACTED | Yes |
| UNDERSTOOD | **Yes for contract** — `CR_NCF_CONTRACT.md` |
| VALIDATED | No |
| Edge cases | AU14 IRR no-sign-change **EXPECTED** |
| Validation | Project_NCF AG51/AH51/AB–AD/AG58/AU14; Equity_NCF AG/AH |
| PEMS module | fiscal.cr_econ, tax, cashflow |
| Status | **READY** (spec — not numerical VALIDATED) |

### 7. RESULTS Equity

| Item | Content |
|------|---------|
| Sheet | RESULTS Equity |
| Role | KPI dashboard (NPV, IRR, take, royalties, revenues, …) |
| EXTRACTED | Yes |
| UNDERSTOOD | **Yes for contract** — `RESULTS_PARAMETER_CONTRACT.md` |
| VALIDATED | No |
| Validation | GTC-001 RESULTS Equity KPI pack (63 rows) |
| PEMS module | economics.metrics / reporting datasets |
| Status | **READY** (spec — not numerical VALIDATED) |

---

## Aggregate critical-path status

| Level | Assessment |
|-------|------------|
| EXTRACTED | **Yes** — catalogue + GTC cover path |
| UNDERSTOOD | **Partial** — sheet roles and KPI labels; not all formula groups |
| VALIDATED | **No** |
| READY for first full-path implementation | **No** — see module readiness |

---

## Critical-path literal classification summary

From `CRITICAL_PATH_LITERAL_SUMMARY.json` (Confirmed snapshot):

| Class | Count |
|-------|------:|
| Total critical-path numeric literals classified | 829 |
| ASSUMPTION | 152 |
| DEFAULT_STRUCTURAL_VALUE | 62 |
| INPUT (strict evidence) | 0 |
| UNRESOLVED | 615 |

Full visible-sheet universe ~3,827; this pass focused **critical-path sheets** (829). Remaining visible off-path literals remain out of this wave or UNRESOLVED by default.
