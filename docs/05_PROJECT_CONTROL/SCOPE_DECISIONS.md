# SCOPE DECISIONS — Consolidated Record

**Project:** PEMS  
**Documentation Baseline:** v2.1  
**Active GM (authoritative identity):** Confirmed-2026-08-03 SHA `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**PREVIOUS DOCUMENTED GM HASH — SUPERSEDED BY RE-FREEZE:** `87EF7439A8F19C52B5B948D379D1752B327144CCDBC36758A780A93EC71121FB`  
**Last updated:** 2026-08-03 (re-freeze)  
**Purpose:** Single place for scope decisions A–E. Do not scatter new answers elsewhere without updating this file.

---

## A. Analysis / 18 Excel data tables

| Field | Value |
|-------|--------|
| Evidence | 18 `DataTableFormula` cells on **Analysis** (visible); documented in `ANALYSIS_DATA_TABLES.md` |
| Affects | Sensitivity presentation / what-if surfaces; not classified as workbook errors |
| Decision | **DEFERRED BY SCOPE for first calculation modules** — not required to start Ec_IO→RESULTS calc path |
| Status | **DEFERRED BY SCOPE** |
| Owner | Project Owner / implementation lead |
| Implementation phase | Phase 10 (Sensitivity) or later |
| Action if needed later | Map tables only after PO confirms Analysis in v1 |

---

## B. @Risk / Monte Carlo

| Field | Value |
|-------|--------|
| Evidence | Defined names include `_AtRisk_*` settings; no vbaProject; Monte Carlo listed as future sequence phase |
| Decision | **DEFERRED BY SCOPE for v1 calculation parity path** — do not reverse-engineer @Risk in first modules |
| Status | **DEFERRED BY SCOPE** |
| Owner | Project Owner |
| Implementation phase | Phase 11 (Monte Carlo) after core NCF/RESULTS parity |
| PENDING if reopened | Whether any @Risk name is required for base-case GTC-001 (current GTC is as-saved deterministic case) |

---

## C. Equity Dash share cell(s)

| Field | Value |
|-------|--------|
| Evidence (Confirmed snapshot) | Label **EQUITY HOLDING** / Company 1; **C4 = 0.49** (float literal). Peer company share cells follow same pattern. Heavily referenced by equity NCF sheets and RESULTS |
| **Decision (PO/domain)** | Treat Equity Dash **Share cell(s)** as a **user/input variable**, **not** a derived value |
| Classification | **`CONFIRMED_INPUT`** / **INPUT** |
| Status | **CLOSED — INPUT** |
| Owner | Project Owner (decision recorded) |
| Implementation | Manual entry + import must supply equity share(s); validation required; do not recompute share from other fields unless workbook later shows a formula driver |
| Notes | Non-share cells on Equity Dash (e.g. acquisition cost, loan blocks) retain separate classification — this decision is specifically for **share** cell(s) |

---

## D. Fiscal Terms_PIA (visible sheet)

| Field | Value |
|-------|--------|
| Evidence | Visible sheet; few formulas (~5), many labels + numeric tables; consumed by Royalties, FLGT, CR Econ, NCF; Model Map: PIA 2021 |
| **Decision (PO/domain)** | Treat **Fiscal Terms_PIA** as a **law/regulatory table**, **not** as ordinary user inputs |
| Classification | **`LAW_TABLE` / `LOOKUP_TABLE_CONSTANT` (regulatory)** — not `CONFIRMED_INPUT` |
| Status | **CLOSED — LAW TABLE** |
| Owner | Project Owner (decision recorded) |
| Implementation | Load as reference data / configuration of fiscal regime tables; not presented as free-form case inputs; changes only via controlled regime/version updates |
| Notes | Sheet remains **in critical path** as dependency of royalties/FLGT/CR/NCF; values are authoritative table constants for the approved GM regime |

---

## E. Hidden NCF versus visible NCF

| Field | Value |
|-------|--------|
| Evidence | Hidden: HT_NCF, CIT_NCF, Project_NCF_Con. Visible: HT_NCF_Oil, CIT_NCF_Oil/Gas, Project_NCF, equity NCF, RESULTS |
| Policy | **SCOPE_VISIBLE_SHEETS_ONLY** — ignore hidden for input/UI/readiness; do not modify |
| Decision established by policy | Implementation surface & validation KPIs prefer **visible** NCF/RESULTS; hidden remain catalogue/dependency evidence |
| Status | **CLOSED by scope policy** (PO-005) |
| Owner | Project control |
| Note | Visible formulas may reference hidden sheets; engine must still reproduce **visible outcomes** |

---

## Related closed baseline (do not reopen)

| Item | Status |
|------|--------|
| Hidden-sheet literal classification | CLOSED out of scope |
| AU14 `#NUM!` | EXPECTED / ACCEPTED no-sign-change IRR |
| Active catalogue / GTC-001 on `D07560CA…` | CLOSED (re-extracted after re-freeze; path integrity CLOSED non-substantive) |

---

## Summary board

| ID | Topic | Status |
|----|-------|--------|
| A | Analysis data tables | DEFERRED BY SCOPE |
| B | @Risk / Monte Carlo | DEFERRED BY SCOPE |
| C | Equity Dash share | **CLOSED — INPUT** |
| D | Fiscal Terms_PIA | **CLOSED — LAW TABLE** |
| E | Hidden vs visible NCF | **CLOSED** by visible-only policy |
