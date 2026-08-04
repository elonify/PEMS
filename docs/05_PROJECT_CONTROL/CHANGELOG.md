# CHANGELOG.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  

All significant changes to Elonify PEMS are recorded here.  
The project follows Semantic Versioning.

---

## [Unreleased]

### Added

- **Phase 1G numerical validation gate** (2026-08-04): single-GM-load chain runner `scripts/phase1g_numerical_validation.py`; session GM CaseInput cache `tests/conftest.py` (deep-copy isolation; no calc/expected-value changes); documented anchors A–F **0 unexplained mismatches** (48 exact / 81 tol / 1 expected_error AU14); evidence JSON + report `PHASE1G_NUMERICAL_VALIDATION.md` (15 sections); **GTC anchor comparison PASS**; CR/RESULTS intermediate-path independence **NOT full VALIDATED**; **RESULTS NUMERICALLY VALIDATED NOT CLAIMED**; **FULL-SYSTEM VALIDATED NOT CLAIMED**; GM SHA `D07560CA…BFEA` MATCH  
- **Phase 1F — RESULTS IMPLEMENTED** (2026-08-04): RESULTS Equity KPI aggregation (`ResultsModule`); groups R-ID…R-PROD incl. BIT/AIT NPV/IRR/take, equity scale C4, unit-cost Excel order, ERR, royalties/tax/production; HT equity + CIT equity **selected intermediate import** path; unit **11** + GTC **3** PASS; RESULTS Equity pack **0 unexplained mismatches**; targeted CR/scaffold regression PASS; report `PHASE1F_RESULTS_IMPLEMENTATION.md`; **NUMERICALLY VALIDATED NOT CLAIMED**; presentation/MC deferred; GM SHA `D07560CA…BFEA` MATCH  
- **Phase 1F RESULTS readiness READY** (2026-08-04): report `PHASE1F_RESULTS_READINESS.md`; RESULTS Equity inventory (62 formulas / 63 GTC KPI rows); CaseInput = Equity C4 only; upstream 1A–1E mapped; ambiguities BIT/AIT, unit-cost/C4, dual hub non-blocking; **IMPLEMENTED NOT STARTED**; **VALIDATED NOT CLAIMED**; **RESULTS IMPLEMENTATION NOT YET AUTHORIZED**; GM SHA `D07560CA…BFEA` MATCH  
- **Phase 1E CR/NCF gate PASSED / ACKNOWLEDGED** (2026-08-04): `PHASE1E_GATE_ACKNOWLEDGEMENT.md`; targeted 10/10; GTC 13 pts PASS; full regression **NOT CLOSED/INTERRUPTED** (not a PASS); **VALIDATED NOT CLAIMED**; RESULTS not started; GM SHA `D07560CA…BFEA` MATCH  
- **Phase 1E CR/NCF controlled completion** (2026-08-04): implementation report finalized with explicit regression limitation; gate ack file `PHASE1E_GATE_ACKNOWLEDGEMENT.md` = **PENDING ACK**; targeted tests 10/10 PASS; GTC 13 pts PASS; full regression **NOT CLOSED/INTERRUPTED** (not converted to PASS); **VALIDATED NOT CLAIMED**; RESULTS not started; GM SHA `D07560CA…BFEA` MATCH  
- **Phase 1E — CR/NCF IMPLEMENTED** (2026-08-04): CR Econ bridge; Project AE/AF/AG/AH/AJ/IRR; Equity × C4; AU14 `NO_VALID_IRR`; HT/CIT intermediates import path; GTC **13 pts (12 tol + 1 expected error / 0 mismatch)**; report `PHASE1E_CR_NCF_IMPLEMENTATION.md`; **NUMERICALLY VALIDATED NOT CLAIMED**; RESULTS not started; GM SHA `D07560CA…BFEA` MATCH  
- **Phase 1E CR/NCF readiness READY** (2026-08-04): report `PHASE1E_CR_NCF_READINESS.md`; parameter contract `CR_NCF_PARAMETER_CONTRACT.md`; companion `CR_NCF_CONTRACT.md` reconfirmed; checklist PASS; GTC anchors (AG51/AH51/AU14 `#NUM!`/…); **no CR/NCF calculation code**; **IMPLEMENTED NOT STARTED**; **VALIDATED NOT CLAIMED**; GM SHA `D07560CA…BFEA` MATCH  
- **Phase 1D FLGT implementation gate PASSED / ACKNOWLEDGED** (2026-08-04): record `PHASE1D_GATE_ACKNOWLEDGEMENT.md`; GTC 18 pts (4 exact / 14 tol / 0 mismatch); suite 70 passed; GM SHA `D07560CA…BFEA` MATCH; **FLGT NUMERICALLY VALIDATED NOT CLAIMED**; **full-system VALIDATED NOT CLAIMED**; CR/NCF **not authorized**  
- **Phase 1D — FLGT/Royalties R-G1…F-G11 IMPLEMENTED** (2026-08-04): law-table application (oil sliding, gas Dom/Out, price bands, HCDT/NDDC, rentals); revenues W/X/Y; AB/AC/AD; AI/AL/ERR; Ec_IO G11/G15; F-G12 deferred; unit 12 + GTC 3; full suite **70 passed**; GTC **18 pts (4 exact / 14 tol / 0 mismatch)**; report `PHASE1D_FLGT_IMPLEMENTATION.md`; **NUMERICALLY VALIDATED NOT CLAIMED**; GM SHA `D07560CA…BFEA` MATCH  
- **Phase 1D FLGT/Royalties readiness READY FOR IMPLEMENTATION** (2026-08-04): gate `PHASE1D_FLGT_IMPLEMENTATION_GATE.md` — inputs, law-table interface, R-G1…F-G11 groups, units/timing, 13+ GTC anchors, test plan, deferred scope; checklist **15/15 PASS**; **no FLGT calculation code**; **IMPLEMENTED/VALIDATED NOT CLAIMED**; GM SHA `D07560CA…BFEA` MATCH  
- **Phase 1C — Costs G1–G8 IMPLEMENTED** (2026-08-04): Cap_Allow selected-path schedules; G3 undisc (FP/FQ/FN/FO); G4 discount FK/FL at Ec_IO C15; G5 CA rates FR5:FR9; G6 Ec_IO N16:S18; G7 escalate_opex + history; G8 SLN/Acq series surface + expensed CAPEX; unit 16 + GTC 4; full suite **55 passed**; GTC **19 pts (10 exact / 9 tol / 0 mismatch)**; report `PHASE1C_COSTS_IMPLEMENTATION.md`; **NUMERICALLY VALIDATED NOT CLAIMED**; GM SHA `D07560CA…BFEA` MATCH  
- **Phase 1B gate PASSED / ACKNOWLEDGED** (2026-08-04): Production G1–G5 **IMPLEMENTED**; GTC 22 pts (20 exact / 2 tol / 0 mismatch); validation boundary preserved (**NUMERICALLY VALIDATED NOT CLAIMED**); GM SHA `D07560CA…BFEA` MATCH / unmodified; record `PHASE1B_GATE_ACKNOWLEDGEMENT.md`  
- **Phase 1C Costs implementation gate/plan READY** (2026-08-04): `PHASE1C_COSTS_IMPLEMENTATION_GATE.md` — CaseInput map, G1–G8 groups, GTC FI48/FL48/FK48/FP48/FQ48 + gas + Ec_IO N16–S18 expected values, deferred items, test/harness criteria, IMPLEMENTED vs VALIDATED separation; **no Costs calculation code**; contract remains **READY** on SHA `D07560CA…BFEA`  
- **Phase 1B — Production G1–G5 IMPLEMENTED** (2026-08-04): CaseInput production parameters + selected-field block series import; Production Profile UR/design (a1/a3/t3/Np/F17), PP series + GOR AG, block annualization/selection, Prod_Summary V47/Y47–Y50/AF26 + Ec_IO C6 life interface; G6 sensitivity deferred; unit + GTC tests; full suite **35 passed**; Production GTC **22 pts (20 exact / 2 tol / 0 mismatch)**; report `docs/03_IMPLEMENTATION/PHASE1B_PRODUCTION_IMPLEMENTATION.md`; **Production NUMERICALLY VALIDATED NOT CLAIMED**; GM SHA `D07560CA…BFEA` verified unchanged  
- **Phase 1A gate ACKNOWLEDGED PASSED** (2026-08-04): CaseInput + Ec_IO pure path authorized IMPLEMENTED; 35/35 GTC; hubs remain deferred  
- **Phase 1A — CaseInput + Ec_IO pure path IMPLEMENTED** (2026-08-04): typed `CaseInput`, provenance, manual + Excel import (same model), validation, pure Ec_IO derivations (C13, Equity C5, G19/G23, E28/D29/E29), GTC compare harness (exact/tolerance/`#NUM!`↔`NO_VALID_IRR`); unit + GTC-001 subset tests **19 passed**; GTC cells **35 exact / 0 tolerance / 0 mismatch**; report `docs/03_IMPLEMENTATION/PHASE1A_EC_IO_IMPLEMENTATION.md`; hub KPIs deferred; **PEMS-vs-GM VALIDATED NOT CLAIMED**; GM read-only SHA `D07560CA…BFEA` verified  
- **Phase 0 scaffold PREPARED:** package `pems` under `src/pems/` (CaseInput shell, GM SHA verify, calc stubs, GTC stub); `docs/03_IMPLEMENTATION/PHASE_0_SCAFFOLD.md` + `SPECIFICATION_FREEZE_AUDIT.md`; **no economic formulas implemented**  
- **Specification freeze COMPLETE** for Ec_IO→RESULTS + Presentation  
- **Presentation specification READY:** `docs/02_SPECIFICATIONS/presentation/` — GM presentation audit (typography, number formats, units/currency, I/O visual language); L1/L2/L3 separation; GM read-only  
- **RESULTS PARTIAL → READY:** `RESULTS_PARAMETER_CONTRACT.md` — RESULTS Equity KPI inventory, equity scale, IRR/NO_VALID_IRR, GTC pack (not numerical VALIDATED); **all calc module specs READY**  
- **CR/NCF PARTIAL → READY:** `CR_NCF_CONTRACT.md` — CR Econ CRL/profit oil, HT/CIT/Project/Equity NCF, AU14 expected, GTC AG51/AH51/AG58 (not numerical VALIDATED)  
- **FLGT/Royalties PARTIAL → READY:** `FLGT_ROYALTIES_CONTRACT.md` — law-table rate application, FLGT components, ERR, GTC AB51/AM51/W51 (not numerical VALIDATED)  
- **Costs PARTIAL → READY:** `COSTS_PARAMETER_CONTRACT.md` — Block_TC categories, Cap_Allow discount/CA/SLN/Acq, escalated OPEX, fiscal interfaces, Ec_IO N16–S18 GTC points (not numerical VALIDATED)  
- **Formal Golden Master approval CLOSED** — Project Owner **Dr Emmanuel Ifeanyichukwu Onwuka**, 3 August 2026 WAT; approved SHA `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA` (`GOLDEN_MASTER_APPROVAL.md`); GM read-only thereafter  
- **Production PARTIAL → READY:** `PRODUCTION_PROFILE_CONTRACT.md` — profile/block/summary groups, CaseInput links, oil/gas streams, GTC V47/Y47/AF26 (not numerical VALIDATED)  
- **Ec_IO PARTIAL → READY:** `EC_IO_PARAMETER_CONTRACT.md` — full CaseInput parameter catalogue, manual+import dual path, validation, equity/fiscal interfaces, GTC ingestion comparison points (not numerical VALIDATED)  
- **2026-08-03 GM re-freeze:** ACTIVE Golden Master SHA `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA` (confirmed snapshot); prior documented SHA `87EF7439…21FB` retained as **PREVIOUS DOCUMENTED GM HASH — SUPERSEDED BY RE-FREEZE** (`GM_FREEZE_RECORD.md`)  
- Catalogue + GTC-001 full re-extract against ACTIVE SHA (86,973 formulas; 10,470 literals)  
- Path integrity disposition **CLOSED — NON-SUBSTANTIVE CURRENT-WORKBOOK DIFFERENCE**  
- PEMS Documentation Baseline **v2.1** full suite (25 core documents) under `docs/`  
- Authority hierarchy with MASTER_IMPLEMENTATION_DIRECTIVE  
- TECHNOLOGY_STACK, DIRECTORY_STRUCTURE, CHART_SPECIFICATION (dual-axis zero alignment), BUILD_AND_DEPLOYMENT  
- DOCUMENTATION_TRACEABILITY_MATRIX  
- Legacy pre-v2.1 documents archived under `docs/archive/legacy_pre_v2.1/`  
- **Excel Golden Master intake:** `docs/workbook/Econ_Model_PEMS.xlsx` (SHA256 registered)  
- Intake history snapshot under `docs/workbook/Workbook_History/`  
- Worksheet inventory (39 sheets) in WORKBOOK_MAPPING_SPECIFICATION  
- `GOLDEN_MASTER_INTAKE_AND_RECONCILIATION_UPDATE.md` control analysis  
- **Formula/cell catalogue** (87,491 formulas; 110,267 non-empty cells) under `docs/workbook/catalogue/`  
- **GTC-001** Golden Test Case + expected outputs (87,431 formula caches; KPI pack) under `docs/workbook/Validation_Datasets/`  
- **Semantic mapping phase:** module maps M01–M09/M99, dependency edges, literal register (10,727), CR Econ/no-cache analysis, charts/VBA inventory, #REF! register under `docs/workbook/semantic_mapping/`  
- **Workbook error confirmation (2026-08-03):** `WORKBOOK_ERROR_STATUS.md` + inventory CSV/JSON  
- **Active catalogue + GTC-001 re-extract** against ACTIVE SHA `D07560CA…` (86,973 formulas; full cache); prior extract on `87EF7439…` superseded  
- Historical intake catalogue/GTC archived under `*/historical_intake_F6A1992F/`  
- `PROJECT_NCF_AU14_INVESTIGATION` evidence pack  
- Active vs historical formula diff (+1714 / −2232 / 401 changed)  

### Changed

- Product naming standardized to PEMS; package name **`pems`** (retired `EEM_Project` from active authority)  
- Validation hierarchy standardized to **six levels**  
- Implementation tracker accuracy reset to reflect documentation-only state  
- Canonical GM path documented as `Econ_Model_PEMS.xlsx` (not a separate `Golden_Master.xlsx` filename)  
- Directory structure / Master Directive / README / tracker updated for GM presence  
- **Active GM identity** SHA `D07560CA…` (Confirmed-2026-08-03 re-freeze); intake `F6A1992F…` historical only; prior `87EF7439…` SUPERSEDED BY RE-FREEZE  
- Error status: START `#REF!` / CR Econ empty caches **CLOSED**; **`Project_NCF!AU14` `#NUM!` → EXPECTED / ACCEPTED IRR NO-SIGN-CHANGE**  
- Catalogue / GTC-001 **ACTIVE** on SHA `D07560CA…`  
- VALIDATION_FRAMEWORK §16.1 + architecture/data-model IRR no-sign-change contract  
- **Scope:** ignore all **hidden** sheets for literal classification & readiness; do not modify them (`SCOPE_VISIBLE_SHEETS_ONLY.md`); ~3,827 visible literals in scope  
- Pre-implementation closure: SCOPE_DECISIONS, GOLDEN_MASTER_APPROVAL (pending PO on NEW SHA), ADRs 0007–0014 accepted, GTC_FRAMEWORK, CRITICAL_PATH_* maps, PRE_IMPLEMENTATION_READINESS_REVIEW  
- **GM path integrity:** calc/semantic match conf vs live; disposition **CLOSED — NON-SUBSTANTIVE CURRENT-WORKBOOK DIFFERENCE** (Equity Dash prior residual closed)  
- **Domain decisions CLOSED:** Equity Dash Share → **INPUT** (C4; C5 derived); Fiscal Terms_PIA → **LAW TABLE** with full rule-source doc  
- Module specs: `EQUITY_DASH_SHARE_INPUT.md`, `FISCAL_TERMS_PIA_LAW_TABLE.md`, `INPUT_SCHEMA_CRITICAL_PATH.md`  
- Critical-path literal register: **829/829 resolved** (0 unresolved); Ec_IO sensitivity residuals → PRESENTATION  
- GTC_COMPARISON_FRAMEWORK.md; readiness review regenerated after re-freeze  
 

### Removed (from active authority)

- Competing root-level v2.0 documentation as sources of truth  
- Hash-prefixed active doc filenames  
- Loose Golden Master at repository root (moved to `docs/workbook/`)  

---

## [2.0.0] — Documentation-only (historical)

Recorded for migration history. Content lived in pre-v2.1 flat files (now archived).

### Added (historical)

- Enterprise architecture draft  
- Validation framework draft  
- System design draft  
- Coding agent workflow draft  
- Project roadmap draft  
- Module specification templates  
- ADR template  
- Validation report template  
- Implementation checklist  

### Notes

- Workbook version was not completed in 2.0 materials  
- Structure conflicted with later v2.1 baseline layout  

---

## Release Notes Template

### Known Issues

### Validation Status

### Workbook Version

### Git Tag
