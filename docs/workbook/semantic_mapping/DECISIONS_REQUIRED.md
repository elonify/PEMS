# DECISIONS REQUIRED (Domain / Project Owner)

Semantic mapping phase — items that **must not** be guessed by implementers.

---

## PO / governance

| ID | Decision | Blocks |
|----|----------|--------|
| PO-001 | Formal approval stamp of Golden Master **Confirmed-2026-08-03** ACTIVE SHA `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA` via `docs/workbook/GOLDEN_MASTER_APPROVAL.md` | **CLOSED** — Dr Emmanuel Ifeanyichukwu Onwuka, 3 August 2026 WAT |
| PO-006 | Path integrity live vs confirmed | **CLOSED — NON-SUBSTANTIVE CURRENT-WORKBOOK DIFFERENCE** (re-freeze accepted; not a calc blocker) |
| PO-002 | Scope of YTD Budget APN (2) sheet | **Superseded for input work** — sheet is **hidden**; ignore per visible-only scope (still do not modify) |
| PO-003 | Scope of dual Project_NCF_Con vs Project_NCF | Prefer **visible** `Project_NCF`; hidden `Project_NCF_Con` ignored for input/readiness (calc refs still in catalogue) |
| PO-004 | Hidden HT_NCF/CIT_NCF vs visible Oil/Gas NCF | **Hidden sheets ignored** for input/readiness; use **visible** HT_NCF_Oil / CIT_* / equity sheets as surface |
| **PO-005** | **Ignore all hidden sheets** for literal classification & implementation readiness; do not modify them | **ACCEPTED** — see `SCOPE_VISIBLE_SHEETS_ONLY.md` |

---

## Domain / fiscal

| ID | Decision | Blocks |
|----|----------|--------|
| DOM-001 | Fiscal Terms_PIA: law table vs scenario input | **CLOSED — LAW TABLE** (SCOPE_DECISIONS §D) |
| DOM-002 | Equity Dash share: input vs derived | **CLOSED — INPUT** (SCOPE_DECISIONS §C) |
| DOM-003 | PIA cost recovery / profit oil rules vs CR Econ columns | M07 |
| DOM-004 | Analysis sensitivity: in-scope for v1? | M09 |
| DOM-005 | @Risk names: ignore vs Monte Carlo requirement | Future MC |

---

## Technical ADRs (still open — not closed this phase)

| ADR | Topic |
|-----|--------|
| ADR-0007 | GUI framework |
| ADR-0008 | Chart library |
| ADR-0009 | Persistence format |
| ADR-0010 | **Excel I/O library** (import + validation compare) — **CLOSED** (see ARCHITECTURAL_DECISIONS) |

---

## Data / validation operations

| ID | Action | Status (2026-08-03) |
|----|--------|---------------------|
| VAL-001 | CR Econ empty caches | **CLOSED** on active GM |
| VAL-002 | Analysis data tables | Documented (18); not auto-errors; sensitivity scope open |
| VAL-003 | Literal classification workshop | **OPEN** — **visible sheets only** (~3,827); hidden-sheet literals (~6,644) **ignored** |
| VAL-004 | START `#REF!` | **CLOSED** on active GM |
| VAL-005 | Disposition of **`Project_NCF!AU14` `#NUM!`** | **CLOSED** — **EXPECTED / ACCEPTED IRR NO-SIGN-CHANGE**; preserve `#NUM!`; not a defect (option **B**) |
| VAL-006 | Re-extract catalogue + GTC-001 vs ACTIVE SHA `D07560CA…` | **CLOSED** (re-extracted after re-freeze 2026-08-03; prior `87EF7439…` SUPERSEDED BY RE-FREEZE) |
| VAL-007 | Ec_IO CaseInput parameter contract + GTC ingestion points | **CLOSED — READY** (`EC_IO_PARAMETER_CONTRACT.md`) |
| VAL-008 | Production Profile contract + GTC production points | **CLOSED — READY** (`PRODUCTION_PROFILE_CONTRACT.md`) |
| VAL-009 | Costs / Cap_Allow contract + GTC cost points | **CLOSED — READY** (`COSTS_PARAMETER_CONTRACT.md`) |
| VAL-010 | FLGT / Royalties contract + GTC royalty points | **CLOSED — READY** (`FLGT_ROYALTIES_CONTRACT.md`) |
| VAL-011 | CR / NCF contract + GTC NCF/IRR points | **CLOSED — READY** (`CR_NCF_CONTRACT.md`; AU14 expected) |
| VAL-012 | RESULTS KPI contract + GTC RESULTS Equity pack | **CLOSED — READY** (`RESULTS_PARAMETER_CONTRACT.md`) |
| VAL-013 | GM presentation & formatting audit | **CLOSED — READY** (`docs/02_SPECIFICATIONS/presentation/`) |
| VAL-014 | Specification freeze + Phase 0 scaffold | **CLOSED** — freeze audit complete; Phase 0 prepared; calc NOT IMPLEMENTED |
