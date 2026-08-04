# PROJECT_ROADMAP.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Product roadmap and milestones  
**Note:** Detailed coding order is owned by IMPLEMENTATION_SEQUENCE.md. This document owns vision, milestones, and release strategy.  

---

## 1. Vision

Enterprise-grade petroleum economics platform supporting economic evaluation, fiscal analysis, production forecasting, scenarios, sensitivity, Monte Carlo, portfolio economics, executive reporting, and engineering dashboards.

---

## 2. Objectives

- Reproduce all validated Excel calculations  
- Support enterprise-scale projects and multiple fiscal systems/scenarios  
- Professional reports and publication-quality charts (including dual-axis zero alignment)  
- Standalone desktop application  
- Extensible architecture  

---

## 3. Development Philosophy

Incremental engineering. Each milestone requires architecture compliance, implementation, validation, and documentation before the next major milestone.

---

## 4. Product Lifecycle

```text
Business specification (Golden Master)
→ Architecture & documentation baseline
→ Implementation
→ Validation
→ Testing
→ Release
→ Maintenance
→ Enhancement
```

---

## 5. Release Strategy

| Type | Scope |
|------|--------|
| Major | Architecture shifts, major functionality, breaking changes |
| Minor | New modules, reports, performance |
| Patch | Bug fixes, validation corrections, documentation |

Semantic Versioning.

---

## 6. Milestone Map (aligned to IMPLEMENTATION_SEQUENCE)

| Milestone | Sequence phases (summary) | Exit criteria |
|-----------|---------------------------|---------------|
| M0 Foundation | Phase 0–1 | Repo, docs v2.1, skeleton, app starts |
| M1 Inputs & domain | Phase 2–3 | Projects load; validated inputs; domain objects |
| M2 Core economics | Phase 4–9 | Production→economics match workbook |
| M3 Risk | Phase 10–11 | Sensitivity & Monte Carlo validated |
| M4 Visualization & reporting | Phase 12–14 | Charts (incl. zero alignment), reports, dashboard |
| M5 Quality & ship | Phase 15–18 | Continuous validation, polish, installer, release |

---

## 7. Phase Narratives (product view)

### Foundation

Architecture, documentation baseline, coding standards, validation framework skeleton, DI/logging/config.

### Workbook analysis (continuous + early intensive)

Worksheet inventory, named ranges, formula catalogue, dependency map, mapping document population.

### Input declaration

Manual entry, Excel/CSV/paste/templates, unit conversion, common validation path.

### Calculation engine

Production, revenue, CAPEX/OPEX/abandonment, royalties, taxes, cash flow, discounting, metrics, economic limit.

### Validation

Formula, cell, module, integration, regression, Golden Test Cases.

### Business object consumption layer

Stable domain objects for charts/reports/dashboard.

### Chart engine

Templates, dynamic scaling, **automatic dual-axis zero alignment**, export, themes.

### Reporting & dashboard

Business-object-driven reports and KPIs.

### Export & packaging

Multi-format export; Windows installer; portable build; validation package.

### Long-term versions

| Line | Focus |
|------|--------|
| 2.x | Workbook parity |
| 3.x | Portfolio economics |
| 4.x | Cloud collaboration |
| 5.x | AI-assisted modelling |
| 6.x | Enterprise deployment |

---

## 8. Future Modules

Portfolio management, carbon economics, ESG, reserves, ranking, optimisation, risk, screening, AI assistant, plugins, REST API / web services.

---

## 9. Quality Gates

No milestone complete without: implementation + validation + documentation + testing + architecture current.

---

## 10. Success Criteria

Software reproduces Golden Master; modular architecture; current docs; validation every release; maintainable enterprise-ready platform.

---

## 11. Maintenance

```text
Requirement → Architecture review → Implementation → Validation → Documentation → Release
```

No direct implementation without architectural review for material changes.
