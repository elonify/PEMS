# ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Consolidated system architecture (software SSOT under the Master Directive)  
**Supersedes:** pre-v2.1 ARCHITECTURE_AND_IMPLEMENTATION_PLAN (including EEM_Project packaging)  

---

## 1. Executive Summary

PEMS transforms a mature Microsoft Excel petroleum economics model into an enterprise-grade desktop application while preserving exact business calculation behaviour of the validated workbook (Golden Master).

- Excel workbook = validated business specification for calculations  
- Software = engineering implementation  

This document consolidates architecture and high-level implementation structure for Baseline v2.1.

---

## 2. Guiding Principles

1. Excel is the business calculation specification — not the software architecture.  
2. Architecture governs implementation.  
3. Validation before completion.  
4. Modularity and clear interfaces.  
5. Charts, reports, dashboards, APIs consume business objects — never worksheet structures.  
6. Extensibility without redesign.  
7. Package and product naming: **PEMS** / Python package **`pems`**.  

---

## 3. Project Objectives

The software shall:

- reproduce Excel calculations exactly (within approved tolerances)  
- support multiple fiscal regimes, countries, projects, scenarios  
- support portfolio, sensitivity, and Monte Carlo analysis (per roadmap)  
- support professional reporting and engineering dashboards  
- support cross-platform-ready desktop deployment (primary: Windows)  

---

## 4. Development Lifecycle (aligned with IMPLEMENTATION_SEQUENCE)

High-level product lifecycle:

```text
Workbook analysis → Input system → Domain model → Calculation modules
→ Validation hardening → Business object consumption → Charts → Reporting
→ Dashboard → Polish → Packaging → Release
```

Detailed ordered phases: `docs/03_IMPLEMENTATION/IMPLEMENTATION_SEQUENCE.md`.

No phase begins until prior exit criteria are met.

---

## 5. Workbook Analysis Requirements

Every worksheet shall be analysed for:

Purpose, inputs, outputs, named ranges, formula groups, lookup tables, validation rules, hidden calculations, dependencies, charts, reports, macros, assumptions.

Every worksheet maps to one or more application modules. No worksheet remains unmapped in WORKBOOK_MAPPING_SPECIFICATION.

---

## 6. Workbook-to-Application Mapping Record

For each worksheet document:

Worksheet name · Business purpose · Application module · Dependencies · Input objects · Output objects · Validation strategy · Implementation status  

Living detail: `WORKBOOK_MAPPING_SPECIFICATION.md`.

---

## 7. System Architecture Layers

```text
Presentation Layer (UI, dashboards, chart views, report views)
        ↓
Application Layer (workflows, commands, session, navigation)
        ↓
Business Services (project/scenario orchestration; no raw math)
        ↓
Calculation Engine (deterministic petroleum economics calculations)
        ↓
Domain Model (business objects)
        ↓
Persistence Layer (projects, scenarios, templates, config storage)
        ↓
Infrastructure (logging, DI, file handling, external adapters)
```

**Validation subsystem** is a quality/control capability used by services and CI: workbook loaders, comparison engine, tolerance checker, report generator. It does not place calculation logic in the UI.

Each layer communicates with adjacent layers only (dependency rule points downward).

---

## 8. Package Structure

```text
src/
  pems/
    api/                 # optional future external API adapters
    application/
    calculations/
    charts/
    configuration/
    core/
    dashboard/
    domain/
    exports/
    fiscal/
    infrastructure/
    persistence/
    production/
    reporting/
    services/
    ui/
    validation/
    utilities/
tests/
```

Every package exposes a clean public interface; internals stay encapsulated.

**Note:** Pre-v2.1 docs used `EEM_Project`. That name is **retired**.

---

## 9. Domain Model (summary)

Domain models petroleum economics concepts, not sheets. Core objects include:

Project, Scenario, Reservoir, Field, DevelopmentPlan, ProductionProfile, CostProfile, PriceDeck, FiscalRegime, RoyaltyResult, TaxResult, CashFlow, DiscountedCashFlow, EconomicLimit, SensitivityCase, MonteCarloSimulation, EconomicMetrics, ReportDataset, ChartDataset, Portfolio  

Field-level contracts: `DATA_MODEL.md`.

---

## 10. Calculation Engine

- Owns all business calculations.  
- Sequence follows workbook dependencies (not arbitrary).  
- No UI, chart, or report access.  
- Deterministic.  
- Modules: production, revenue, costs, fiscal (royalty, hydrocarbon tax, CIT, levies), cash flow, discounting, economic metrics, economic limit, sensitivity, Monte Carlo.  

Illustrative pipeline (must be refined against Golden Master):

```text
Inputs → Production → Revenue → Royalty → Hydrocarbon Tax
→ Corporate Tax → Cash Flow → Discounting → Economic Metrics
→ Economic Limit → Sensitivity → Monte Carlo
```

### IRR — no-sign-change condition (mandatory)

When the NCF series has **no qualifying sign change** (including all-blank, all-non-negative, or all-non-positive non-zero series under Excel `IRR` rules):

- Excel returns **`#NUM!`** — this is **expected behaviour**, not a model defect when documented.  
- PEMS **must not manufacture** an IRR.  
- PEMS **must** return an explicit **no-IRR / undefined** outcome equivalent to Excel `#NUM!`.  
- Active Golden Master example: `Project_NCF!AU14` `=IRR(AK5:AK49)` → `#NUM!` with **AK5:AK49 entirely blank** (SHA `D07560CA…`).  
- Authority: `docs/workbook/semantic_mapping/WORKBOOK_ERROR_STATUS.md` EXP-001; VALIDATION_FRAMEWORK §16.1.

---

## 11. Validation Framework (architecture view)

Validation is mandatory. Levels (authoritative detail in VALIDATION_FRAMEWORK.md):

1. Workbook structure  
2. Formula  
3. Cell  
4. Module  
5. System integration  
6. Regression  

Four-level summaries in older docs are superseded by this six-level model.

---

## 12. Definition of Ready / Done

See MASTER_IMPLEMENTATION_DIRECTIVE.md. Architecture requires: workbook analysed, formulas captured, inputs/outputs/deps documented, module specification completed before coding.

---

## 13. Coding Standards

Modular; type hinted; documented; no duplicated logic; no circular dependencies; composition over inheritance; SOLID; testable.

---

## 14. Git Workflow

One logical change per commit. Commits reference module, workbook sheet, and validation status when applicable.

---

## 15. Future Modules (reserved)

Portfolio economics, carbon economics, ESG, AI decision support, portfolio ranking, economic optimisation, cloud collaboration, plugin marketplace.

Must not force redesign of core layers.

---

## 16. Architecture Governance on Workbook Change

1. Analyse workbook  
2. Compare with architecture  
3. Update this plan if needed  
4. Update module specs and mapping  
5. Implement  
6. Validate  

No implementation against outdated architecture or workbook.

---

## 17. Conclusion

This plan governs engineering structure of PEMS under Baseline v2.1. Every implementation remains traceable to the business specification, validated against the Golden Master, and documented.
