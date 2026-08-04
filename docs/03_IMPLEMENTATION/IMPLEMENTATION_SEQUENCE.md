# IMPLEMENTATION_SEQUENCE.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Master implementation schedule  
**Supersedes:** pre-v2.1 IMPLEMENTATION_SEQUENCE  

---

## Purpose

Official implementation order for PEMS. Every AI coding agent shall follow this sequence. No module skipped unless Project Owner approves.

Aligned product milestones: PROJECT_ROADMAP.md.  
Live status: IMPLEMENTATION_TRACKER.md.

---

## Phase 0 – Project Initialization

**Objectives**

- Repository created  
- Documentation Baseline v2.1 committed  
- Golden Master workbook archived (when available)  
- Development environment configured  
- CI pipeline configured (when applicable)  
- Build system operational  

**Deliverables:** Repository, documentation, project skeleton, development environment  

**Status gate:** Complete before application module coding  

---

## Phase 1 – Foundation

Modules: Configuration system, logging, exception framework, project settings, dependency injection, domain base classes, validation framework skeleton, persistence layer skeleton, file management, theme system (as applicable).

**Deliverable:** Application starts successfully.

---

## Phase 2 – Input System

Project manager (create/load/save), manual data entry, Excel import, CSV import, copy/paste import, project templates, input validation, unit conversion, import wizard.

**Deliverable:** Users can create projects and populate **validated** input data via manual **and** import paths (same validation layer).

---

## Phase 3 – Domain Model

Project, Scenario, Production Profile, Price Deck, Fiscal Terms, Cost Model, Economic Parameters, Risk Parameters — as pure domain objects independent of Excel grid layout.

**Deliverable:** Engineering objects exist independently of Excel structures.

---

## Phase 4 – Production Module

Production profiles, plateau, decline, water cut, GOR, scheduling; validation vs workbook.

**Deliverable:** Production calculations match Excel.

---

## Phase 5 – Revenue Module

Oil, gas, NGL, other income, aggregation; validation.

**Deliverable:** Revenue module fully validated.

---

## Phase 6 – Cost Module

CAPEX, OPEX, abandonment, inflation, escalation, schedules; validation.

**Deliverable:** Costs match workbook.

---

## Phase 7 – Fiscal Module

Royalty, hydrocarbon tax, corporate income tax, education tax (if applicable), other levies, government take, contractor take; validation.

**Deliverable:** Fiscal outputs equal workbook (within tolerances).

---

## Phase 8 – Cash Flow Engine

Cash flow builder, discount factors, DCF, financing, working capital (as in workbook); validation.

**Deliverable:** Cash flow identical to workbook within tolerances.

---

## Phase 9 – Economic Analysis

NPV, IRR, NPVI, payout, profitability index, EMV, economic limit; validation.

**Deliverable:** Economics validated.

---

## Phase 10 – Sensitivity Analysis

Parameter variation, ranking, spider/tornado data; validation.

**Deliverable:** Sensitivity module operational.

---

## Phase 11 – Monte Carlo

Distributions, sampling, simulation engine, statistics, P10/P50/P90, histograms; validation.

**Deliverable:** Monte Carlo verified.

---

## Phase 12 – Chart Engine

Chart manager, templates, axis manager, **dynamic scaling**, **automatic dual-axis zero alignment**, zoom/pan, legends, export; validation.

**Deliverable:** Charts operational per CHART_SPECIFICATION.

---

## Phase 13 – Reporting

Executive, technical, fiscal, investment, validation reports; PDF/Word/PowerPoint/Excel export.

**Deliverable:** Reports generated from validated data only.

---

## Phase 14 – Dashboard

Executive/project dashboards, charts, KPIs, recent projects, scenario comparison.

**Deliverable:** Interactive dashboard completed.

---

## Phase 15 – Validation Engine Hardening

Workbook comparison automation, regression suite, benchmarking, performance tests, validation reports archive.

**Deliverable:** Continuous validation operational.

---

## Phase 16 – Application Polish

Icons, themes, shortcuts, context help, preferences, recent files, undo/redo.

**Deliverable:** Professional UX.

---

## Phase 17 – Installer

PyInstaller-class bundle, installer, portable version, digital signing (as required), auto-update future.

**Deliverable:** Deployable application.

---

## Phase 18 – Release

All modules validated; documentation updated; regression passed; workbook comparison passed; performance targets met.

**Deliverable:** PEMS production release.

---

## Definition of Done (every module)

- Code implemented  
- Unit tests pass  
- Integration tests pass  
- Workbook validation passes  
- Regression tests pass  
- Documentation updated  
- Changelog updated when required  
- Tracker updated  
- Ready for next phase  

---

## Final Principle

Progress is measured by **validated business capability**, not lines of code. Sequence shall be followed without silent deviation.
