# DOCUMENTATION_TRACEABILITY_MATRIX.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Control artifact (not one of the 25 core documents)  
**Purpose:** Prove requirements from audited/pre-v2.1 materials were not lost  

---

## Legend

| Status | Meaning |
|--------|---------|
| MIGRATED | Content integrated into final v2.1 document |
| NEW | Created to fill baseline gap |
| ARCHIVED | Source retained under `docs/archive/`; not authoritative |
| OPEN | Cannot fully resolve without Golden Master or Project Owner decision |

---

## A. Core suite inventory (25)

| # | Final PEMS Document | Path | Origin |
|---|---------------------|------|--------|
| 1 | README.md | `/README.md` | Rewritten from `#README.md` |
| 2 | MASTER_IMPLEMENTATION_DIRECTIVE.md | `docs/00_GOVERNANCE/` | NEW (authority + audit hierarchy) |
| 3 | AI_AGENT_BOOTSTRAP.md | `docs/00_GOVERNANCE/` | NEW (from CLAUDE/workflow + audit) |
| 4 | CODING_AGENT_WORKFLOW.md | `docs/00_GOVERNANCE/` | MIGRATED from root workflow + CLAUDE |
| 5 | GOVERNANCE.md | `docs/00_GOVERNANCE/` | NEW + CONTRIBUTING/RELEASE rules |
| 6 | ARCHITECTURAL_DECISIONS.md | `docs/00_GOVERNANCE/` | NEW + ADR_TEMPLATE |
| 7 | ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md | `docs/01_ARCHITECTURE/` | MIGRATED; EEM_Project removed |
| 8 | SYSTEM_DESIGN.md | `docs/01_ARCHITECTURE/` | MIGRATED |
| 9 | TECHNOLOGY_STACK.md | `docs/01_ARCHITECTURE/` | NEW (Python/PyInstaller confirmed; opens recorded) |
| 10 | DIRECTORY_STRUCTURE.md | `docs/01_ARCHITECTURE/` | NEW (reconciled trees) |
| 11 | PROJECT_ROADMAP.md | `docs/01_ARCHITECTURE/` | MIGRATED; aligned to sequence |
| 12 | DATA_MODEL.md | `docs/02_SPECIFICATIONS/` | NEW from domain lists |
| 13 | INPUT_SYSTEM_SPECIFICATION.md | `docs/02_SPECIFICATIONS/` | MIGRATED v2.1 input spec |
| 14 | API_SPECIFICATION.md | `docs/02_SPECIFICATIONS/` | NEW (internal API; REST future) |
| 15 | UI_ARCHITECTURE.md | `docs/02_SPECIFICATIONS/` | NEW from presentation layers |
| 16 | CONFIGURATION.md | `docs/02_SPECIFICATIONS/` | NEW from design/config notes |
| 17 | CHART_SPECIFICATION.md | `docs/02_SPECIFICATIONS/` | NEW + zero-alignment requirement |
| 18 | REPORT_SPECIFICATION.md | `docs/02_SPECIFICATIONS/` | NEW from report engine notes |
| 19 | WORKBOOK_MAPPING_SPECIFICATION.md | `docs/02_SPECIFICATIONS/` | MIGRATED; living map |
| 20 | IMPLEMENTATION_SEQUENCE.md | `docs/03_IMPLEMENTATION/` | MIGRATED v2.1 sequence |
| 21 | MODULE_IMPLEMENTATION_TEMPLATE.md | `docs/03_IMPLEMENTATION/` | MIGRATED + checklist + v1 module spec |
| 22 | VALIDATION_FRAMEWORK.md | `docs/04_QUALITY/` | MIGRATED; 6-level SSOT |
| 23 | BUILD_AND_DEPLOYMENT.md | `docs/04_QUALITY/` | NEW + release checklist + PyInstaller |
| 24 | IMPLEMENTATION_TRACKER.md | `docs/05_PROJECT_CONTROL/` | MIGRATED; false completeness fixed |
| 25 | CHANGELOG.md | `docs/05_PROJECT_CONTROL/` | MIGRATED + v2.1 entry |

---

## B. Source → Final mapping (requirements)

| SOURCE REQUIREMENT | SOURCE DOCUMENT (pre-v2.1 / audit) | FINAL PEMS DOCUMENT | SECTION | STATUS |
|--------------------|-------------------------------------|---------------------|---------|--------|
| Excel Golden Master authority | README, Architecture, Validation, CLAUDE, Workflow | MASTER_IMPLEMENTATION_DIRECTIVE; VALIDATION_FRAMEWORK | §5; §2 | MIGRATED |
| Workbook → code → test traceability | Architecture, Validation, Workflow | MASTER_IMPLEMENTATION_DIRECTIVE; VALIDATION_FRAMEWORK; WORKBOOK_MAPPING | hierarchy; §21; §12 | MIGRATED |
| Layered architecture | Architecture, System Design | ARCHITECTURE_AND_IMPLEMENTATION_PLAN; SYSTEM_DESIGN | layers | MIGRATED |
| Package structure | Architecture (`EEM_Project`) | DIRECTORY_STRUCTURE; ARCHITECTURE plan | `src/pems` | MIGRATED (renamed) |
| Domain entities | Architecture, System Design | DATA_MODEL; SYSTEM_DESIGN | entities | MIGRATED |
| Calculation pipeline / dependency order | System Design, Validation | SYSTEM_DESIGN; IMPLEMENTATION_SEQUENCE | pipeline; Phases 4–9 | MIGRATED |
| Fiscal / production / cost / revenue / CF / metrics | Roadmap, Sequence, Validation | IMPLEMENTATION_SEQUENCE; DATA_MODEL | Phases 4–9 | MIGRATED |
| Sensitivity / Monte Carlo | Roadmap, Sequence | IMPLEMENTATION_SEQUENCE | Phases 10–11 | MIGRATED |
| Formula-first / cell-by-cell | Validation, Module templates, Checklist | VALIDATION_FRAMEWORK; MODULE_IMPLEMENTATION_TEMPLATE; WORKBOOK_MAPPING | §8–9; formula catalogue | MIGRATED |
| Module-by-module implementation | Sequence, Tracker, Templates | IMPLEMENTATION_SEQUENCE; MODULE template; TRACKER | all | MIGRATED |
| Input: manual + Excel + CSV + paste + templates | INPUT_SYSTEM v2.1 | INPUT_SYSTEM_SPECIFICATION | §4 | MIGRATED |
| Unified validation for all inputs | INPUT_SYSTEM | INPUT_SYSTEM_SPECIFICATION; MASTER directive | §5; §6 | MIGRATED |
| Unit conversion | INPUT_SYSTEM | INPUT_SYSTEM; DATA_MODEL; CONFIGURATION | units | MIGRATED |
| Import wizard / audit trail | INPUT_SYSTEM | INPUT_SYSTEM | §8–10 | MIGRATED |
| Chart factory architecture | System Design | CHART_SPECIFICATION; SYSTEM_DESIGN | §2; chart engine | MIGRATED |
| Dynamic scaling / zero alignment | Roadmap, Sequence | CHART_SPECIFICATION | §5–6 | MIGRATED + specified |
| Dual-axis zero alignment algorithm | Reconciliation + audit gap | CHART_SPECIFICATION | §6 | NEW |
| Reporting no calc | System Design, Workflow | REPORT_SPECIFICATION; SYSTEM_DESIGN | principles | MIGRATED |
| Dashboard rules | System Design, CLAUDE | SYSTEM_DESIGN; UI_ARCHITECTURE; SEQUENCE Phase 14 | dashboard | MIGRATED |
| Six-level validation | Validation Framework | VALIDATION_FRAMEWORK | §4 | MIGRATED (SSOT) |
| Four-level validation (old) | Architecture §13 | VALIDATION_FRAMEWORK | superseded note | RESOLVED |
| Golden Test Cases / scenarios | Validation Framework | VALIDATION_FRAMEWORK | §13 | MIGRATED |
| Tolerances configurable | Validation, System Design | CONFIGURATION; VALIDATION_FRAMEWORK | tolerances | MIGRATED |
| Regression / release gates | Validation, Release checklist | VALIDATION_FRAMEWORK; BUILD_AND_DEPLOYMENT; GOVERNANCE | gates | MIGRATED |
| Workbook change management | Architecture, Validation, Workflow | MASTER directive; GOVERNANCE; VALIDATION | change | MIGRATED |
| AI agent workflow / DoR/DoD | CLAUDE, Workflow | AI_AGENT_BOOTSTRAP; CODING_AGENT_WORKFLOW; MASTER | all | MIGRATED |
| Agent adapter | CLAUDE.md | `/CLAUDE.md` | adapter | MIGRATED (demoted) |
| Implementation sequence 18 phases | IMPLEMENTATION_SEQUENCE v2.1 | IMPLEMENTATION_SEQUENCE | Phases 0–18 | MIGRATED |
| Implementation tracking | IMPLEMENTATION_TRACKER, MODULE TRACKER | IMPLEMENTATION_TRACKER | merged | MIGRATED |
| Module template + checklist | Module templates, IMPLEMENTATION_CHECKLIST | MODULE_IMPLEMENTATION_TEMPLATE | checklist | MIGRATED |
| ADR template | ADR_TEMPLATE | ARCHITECTURAL_DECISIONS | §5 | MIGRATED |
| Validation report fields | VALIDATION REPORT template | VALIDATION_FRAMEWORK | §17 | MIGRATED |
| Contributing rules | CONTRIBUTING | GOVERNANCE | §7 | MIGRATED |
| Release checklist | RELEASE_CHECKLIST | BUILD_AND_DEPLOYMENT | §7 | MIGRATED |
| Branch strategy | README | GOVERNANCE | §5 | MIGRATED |
| Technology: Python desktop | README, Architecture | TECHNOLOGY_STACK; ADR-0005 | confirmed | MIGRATED |
| Packaging PyInstaller | Sequence Phase 17 | TECHNOLOGY_STACK; BUILD_AND_DEPLOYMENT; ADR-0006 | confirmed | MIGRATED |
| GUI framework choice | (missing) | TECHNOLOGY_STACK; ADR-0007 | open | OPEN |
| Chart library choice | (missing) | TECHNOLOGY_STACK; ADR-0008 | open | OPEN |
| Persistence format | (missing) | TECHNOLOGY_STACK; ADR-0009 | open | OPEN |
| Excel I/O library | (missing) | TECHNOLOGY_STACK; ADR-0010 | open | OPEN |
| Physical Golden Master xlsx | Econ_Model_PEMS.xlsx (repo root → moved) | WORKBOOK_MANIFEST; `docs/workbook/Econ_Model_PEMS.xlsx` | intake | **CLOSED** |
| Workbook sheet name inventory | Econ_Model_PEMS.xlsx (39 sheets) | WORKBOOK_MAPPING_SPECIFICATION §3 | inventory | **CLOSED** (names/counts) |
| Populated cell/formula catalogue | openpyxl extraction 2026-08-02 | `docs/workbook/catalogue/*`; FORMULA_CELL_CATALOGUE.md | catalogue | **CLOSED as artifact** (semantics open) |
| Golden Test Cases / expected outputs | GM cached values GTC-001 | `Validation_Datasets/GOLDEN_TEST_CASES.md` + CSVs | validation datasets | **CLOSED as artifact** (multi-scenario open) |
| Golden Master intake reconciliation update | This intake + catalogue/GTC pass | GOLDEN_MASTER_INTAKE_AND_RECONCILIATION_UPDATE | analysis | UPDATED |
| Future API / DB import | INPUT_SYSTEM, Roadmap | API_SPECIFICATION; INPUT_SYSTEM | future | MIGRATED |
| Portfolio / carbon / ESG future | Architecture, Roadmap | ARCHITECTURE plan; ROADMAP | future | MIGRATED |
| Performance targets | Tracker | BUILD_AND_DEPLOYMENT; TRACKER | targets | MIGRATED |
| PEMS.md tree sketch | PEMS.md | DIRECTORY_STRUCTURE + baseline folders | adapted (03_IMPLEMENTATION, 04_QUALITY, 05_PROJECT_CONTROL) | MIGRATED |
| False “tech stack complete” claim | old Tracker | IMPLEMENTATION_TRACKER | corrected | RESOLVED |

---

## C. Archived sources

| Archived file | Disposition |
|---------------|-------------|
| `#README.md` | ARCHIVED → content → README.md |
| `#ARCHITECTURE_AND_IMPLEMENTATION_PLAN_1.md` | ARCHIVED → ARCHITECTURE plan |
| `SYSTEM_DESIGN.md` | ARCHIVED → SYSTEM_DESIGN |
| `VALIDATION_FRAMEWORK.md` | ARCHIVED → VALIDATION_FRAMEWORK |
| `CODING_AGENT_WORKFLOW.md` | ARCHIVED → CODING_AGENT_WORKFLOW |
| `# CLAUDE.md` | ARCHIVED → adapter CLAUDE.md + bootstrap/workflow |
| `PROJECT_ROADMAP.md` | ARCHIVED → PROJECT_ROADMAP |
| `# INPUT_SYSTEM_SPECIFICATION.md` | ARCHIVED → INPUT_SYSTEM |
| `# WORKBOOK_MAPPING_SPECIFICATION.md` | ARCHIVED → WORKBOOK_MAPPING |
| `# IMPLEMENTATION_SEQUENCE.md` | ARCHIVED → IMPLEMENTATION_SEQUENCE |
| `# IMPLEMENTATION_TRACKER.md` | ARCHIVED → IMPLEMENTATION_TRACKER |
| `# MODULE_IMPLEMENTATION_TEMPLATE.md` | ARCHIVED → MODULE template |
| `# MODULE SPECIFICATION.md` | ARCHIVED → merged into MODULE template |
| `# MODULE TRACKER.md` | ARCHIVED → merged into TRACKER |
| `IMPLEMENTATION_CHECKLIST.md` | ARCHIVED → MODULE template checklist |
| `ADR_TEMPLATE.md` | ARCHIVED → ARCHITECTURAL_DECISIONS |
| `# VALIDATION REPORT.md` | ARCHIVED → VALIDATION_FRAMEWORK §17 |
| `# CONTRIBUTING.md` | ARCHIVED → GOVERNANCE |
| `# RELEASE_CHECKLIST.md` | ARCHIVED → BUILD_AND_DEPLOYMENT |
| `# CHANGELOG.md` | ARCHIVED → CHANGELOG |
| `PEMS.md` | ARCHIVED → structure absorbed |

---

## D. Unresolved / blocked on evidence

1. ~~Physical Golden Master file~~ **Resolved 2026-08-01**.  
2. ~~Cell/formula inventory + GTC-001 expected caches~~ **Resolved 2026-08-02 as artifacts** — semantics/input classification still open.  
3. Business filtering of named ranges; charts; VBA (partial/not done).  
4. GUI, chart library, persistence format, Excel I/O library (Project Owner / ADR) — **OPEN**.  
5. Business rounding tolerances beyond float epsilon (optional policy).  
6. Pinned Python minor version (Phase 0 scaffolding).  
7. Formal Project Owner approval stamp on manifest — **OPEN**.  

These remaining items are recorded as OPEN, not silently invented.

---

## E. Golden Master identity notes

| Field | Historical intake | **Active confirmed** |
|-------|-------------------|----------------------|
| Path | history snapshot | Confirmed: `Workbook_History/Econ_Model_PEMS_confirmed_2026-08-03.xlsx` (ACTIVE GM); live working copy separate |
| SHA256 | F6A1992F…3006 | **D07560CA…BFEA** (complete: `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`) |
| Sheets | 39 | **38** |
| Catalogue/GTC | `*/historical_intake_F6A1992F/` STALE | **ACTIVE** re-extract |
| Errors / conditions | START #REF!; CR empty caches | **AU14 `#NUM!` = EXPECTED no-sign-change IRR**; no open defects |
| Equity Dash Share | SCOPE / domain | **CLOSED — INPUT** (`EQUITY_DASH_SHARE_INPUT.md`) |
| Fiscal Terms_PIA | SCOPE / domain | **CLOSED — LAW TABLE** (`FISCAL_TERMS_PIA_LAW_TABLE.md`) |
| Path integrity | Live vs confirmed | **CLOSED — NON-SUBSTANTIVE CURRENT-WORKBOOK DIFFERENCE** — ACTIVE GM `D07560CA…`; prior SHA SUPERSEDED BY RE-FREEZE |
| Critical-path literals | Classification register | **829 resolved / 0 unresolved** |
| Ec_IO CaseInput | Parameter contract | **READY** — `EC_IO_PARAMETER_CONTRACT.md` / `INPUT_SCHEMA_CRITICAL_PATH.md` |
| Production Profile | Parameter/logic contract | **READY** — `PRODUCTION_PROFILE_CONTRACT.md` |
| Costs / Cap_Allow | Parameter/logic contract | **READY** — `COSTS_PARAMETER_CONTRACT.md` |
| FLGT / Royalties | Parameter/logic contract | **READY** — `FLGT_ROYALTIES_CONTRACT.md` |
| CR / NCF | Parameter/logic contract | **READY** — `CR_NCF_CONTRACT.md` |
| RESULTS | KPI/output contract | **READY** — `RESULTS_PARAMETER_CONTRACT.md` |
| Presentation | Formatting / visual language | **READY** — `docs/02_SPECIFICATIONS/presentation/` |
| Spec freeze | Completeness audit | **COMPLETE** — `docs/03_IMPLEMENTATION/SPECIFICATION_FREEZE_AUDIT.md` |
| Phase 0 scaffold | Package `pems` | **PREPARED** — `docs/03_IMPLEMENTATION/PHASE_0_SCAFFOLD.md` |
| Phase 1A CaseInput + Ec_IO | Implementation + GTC subset | **IMPLEMENTED** pure path — `PHASE1A_EC_IO_IMPLEMENTATION.md`; GTC 35/35 exact; hub deferred; gate **ACKNOWLEDGED**; **VALIDATED NOT CLAIMED** |
| Phase 1B Production | Implementation + GTC subset | **PASSED / IMPLEMENTED** G1–G5 — `PHASE1B_PRODUCTION_IMPLEMENTATION.md` + `PHASE1B_GATE_ACKNOWLEDGEMENT.md`; GTC 22 pts; **VALIDATED NOT CLAIMED** |
| Phase 1C Costs | Implementation + GTC subset | **IMPLEMENTED** G1–G8 — `PHASE1C_COSTS_IMPLEMENTATION.md`; GTC 19 pts (10 exact / 9 tol); **VALIDATED NOT CLAIMED** |
| Phase 1D FLGT readiness | Spec/gate only | Gate `PHASE1D_FLGT_IMPLEMENTATION_GATE.md` |
| Phase 1D FLGT implementation | Code + GTC subset | **PASSED / IMPLEMENTED** R-G1…F-G11 — `PHASE1D_FLGT_IMPLEMENTATION.md` + `PHASE1D_GATE_ACKNOWLEDGEMENT.md`; GTC 18 pts; **VALIDATED NOT CLAIMED** |
| Phase 1E CR/NCF readiness | Spec readiness | **READY** — `PHASE1E_CR_NCF_READINESS.md` |
| Phase 1E CR/NCF implementation | Code + GTC subset | **PASSED / IMPLEMENTED** — `PHASE1E_CR_NCF_IMPLEMENTATION.md` + `PHASE1E_GATE_ACKNOWLEDGEMENT.md`; GTC 13 pts; full regression NOT CLOSED; **VALIDATED NOT CLAIMED** |
| Phase 1F RESULTS readiness | Spec readiness | **SPEC READY** — `PHASE1F_RESULTS_READINESS.md`; 63 GTC RESULTS Equity points; code NOT STARTED; **VALIDATED NOT CLAIMED** |
| Formal GM approval | `GOLDEN_MASTER_APPROVAL.md` | **CLOSED** — Dr Emmanuel Ifeanyichukwu Onwuka, 3 Aug 2026 WAT; SHA `D07560CA…BFEA` |
| Control | — | `WORKBOOK_ERROR_STATUS.md` EXP-001; `SCOPE_DECISIONS.md` |
