# SYSTEM_DESIGN.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Engineering design specification  
**Supersedes:** pre-v2.1 SYSTEM_DESIGN.md  

---

## 1. Purpose

Defines how PEMS is engineered: decomposition, domain model, layer responsibilities, interactions, data flow, dependency rules, services, events, and extensibility.

Does not replace module-level implementation detail.

Authority: subordinate to MASTER_IMPLEMENTATION_DIRECTIVE and ARCHITECTURE_AND_IMPLEMENTATION_PLAN.

---

## 2. Design Philosophy

- Enterprise application, not an Excel UI replica.  
- Workbook is business calculation specification.  
- Business logic fully separated from presentation.  
- Single responsibility; independently testable modules.  
- Package root: `pems`.  

---

## 3. System Layers

```text
Presentation
→ Application
→ Business Services
→ Calculation Engine
→ Domain Model
→ Persistence
→ Infrastructure
```

Adjacent-layer communication only. Dependencies point downward. Domain depends on nothing external.

---

## 4. Layer Responsibilities

### Presentation

UI, forms, dialogs, dashboards, chart views, report views. **No business calculations.**

### Application

Workflow orchestration, commands, requests, navigation, session management. Coordinates services.

### Business Services

Project creation, scenario execution, fiscal/economic evaluation orchestration, report/export coordination. **Orchestrate calculations; do not perform raw calculation math.**

### Calculation Engine

Production forecasting, revenue, fiscal, discounting, metrics, sensitivity, Monte Carlo. **Deterministic.**

### Domain

Business objects (Project, Scenario, ProductionProfile, CashFlow, FiscalRegime, EconomicMetrics, ChartDataset, ReportDataset, …). No UI logic.

### Persistence

Save/load projects, scenarios, templates, configuration stores.

### Infrastructure

Logging, configuration loading, DI, caching (only if determinism preserved), file handling, external integrations.

### Validation (subsystem)

Workbook comparison tooling, tolerance checks, validation reports. Used by services and automated tests; not a place for production business formulas.

---

## 5. High-Level Runtime Flow

```text
Workbook / User / CSV / Paste / Template
→ Input Manager
→ Validation Engine (input rules)
→ Domain Objects
→ Calculation Engine
→ Result domain objects
→ Application services
→ Charts / Reports / Dashboard / Exports
```

Presentation components never access the Golden Master for live business results.

---

## 6. Domain Model

Primary entities (see DATA_MODEL.md for fields):

Project, Field, Reservoir, DevelopmentPlan, Scenario, ProductionProfile, CostProfile, PriceDeck, FiscalRegime, Royalty, HydrocarbonTax, CorporateTax, CashFlow, DiscountedCashFlow, EconomicMetrics, EconomicLimit, SensitivityCase, MonteCarloSimulation, Portfolio, ChartDataset, ReportDataset.

---

## 7. Core Services

ProjectService, ScenarioService, ProductionService, FiscalService, EconomicsService, ValidationService, ChartService, ReportingService, ExportService, ConfigurationService, InputService / ImportService.

Services communicate through domain objects.

---

## 8. Dependency Rules

```text
Presentation → Application → Business Services → Calculation Engine → Domain
Infrastructure supports all; domain does not depend on infrastructure types in core logic.
```

---

## 9. Data Flow

```text
User/Import Input → Input validation → Domain objects → Calculation Engine
→ Results → Business objects → Reports / Charts / Dashboard / Exports
```

No shortcuts.

---

## 10. Event / Workflow Flow

```text
Create Project → Load Inputs → Validate Inputs → Run Calculations
→ Validate Outputs → Generate Results → Refresh Dashboard → Export
```

---

## 11. Calculation Pipeline

Must match Golden Master dependency order. Baseline conceptual pipeline:

```text
Inputs → Production → Revenue → Royalty → Hydrocarbon Tax
→ Corporate Tax → Cash Flow → Discounting → Economic Metrics
→ Economic Limit → Sensitivity → Monte Carlo
```

Each stage exposes structured outputs.

### IRR / no-sign-change contract

Economic metrics stage shall implement the same IRR edge case as Excel:

- **Input:** NCF time series  
- **If no qualifying sign change:** output **no IRR** (equivalent to Excel `#NUM!`), never a fabricated rate  
- **Golden Master reference:** `Project_NCF!AU14` on active SHA `D07560CA…` — expected `#NUM!` when `AK5:AK49` has no sign change (blank series on that baseline)  
- Full policy: VALIDATION_FRAMEWORK §16.1; WORKBOOK_ERROR_STATUS EXP-001  

---

## 12. Chart Engine (architecture)

Independent of workbook structures:

```text
ChartFactory → ChartBuilder → ChartRenderer → ChartExporter
```

Consumes **ChartDataset** only.

Supported chart families include: production, cash flow, revenue, fiscal take, NPV, IRR, economic limit, sensitivity, Monte Carlo, tornado, spider, waterfall.

**Mandatory behaviour:** dynamic scaling; when primary and secondary Y-axes both logically include zero, **zeros align**. Detail: CHART_SPECIFICATION.md. No VBA dependency.

---

## 13. Reporting Engine

Consumes **ReportDataset** only. No calculations during report generation.

Report types: Executive, Technical, Fiscal, Economic, Sensitivity, Portfolio, Scenario, Validation summary.

---

## 14. Dashboard

Displays validated business objects only: KPIs, tables, charts, scenario/project summaries, recent runs. Never executes calculations or mutates domain objects.

---

## 15. Export Engine

Formats: Excel, PDF, Word, PowerPoint, CSV, JSON, PNG, SVG. Consume validated business objects.

---

## 16. Validation Integration

ValidationService participates:

- before calculation (inputs)  
- after calculation (outputs / workbook compare when required)  
- before export and report generation when policy requires  

---

## 17. Configuration

Application settings, fiscal defaults, unit preferences, themes, **tolerance values**, file paths. Configuration never contains business calculation logic.

---

## 18. Error Handling

Classes: Validation, Calculation, Configuration, Persistence, System, Recoverable, Fatal. All logged.

---

## 19. Performance

Support large projects, multiple scenarios, Monte Carlo, long forecasts. Caching only where determinism preserved.

---

## 20. Extensibility

Portfolio, carbon, ESG, AI assistant, optimisation, cloud collaboration, plugins — without redesigning core layers.

---

## 21. Technology Principles

Business logic independent of GUI framework, chart library, database, export format, OS.

---

## 22. Design Constraints

**Business logic must not:** import GUI libraries; manipulate charts; write reports; access workbook cells for runtime results.

**Presentation must not:** perform calculations; modify domain objects directly; bypass validation.

---

## 23. Traceability

```text
Workbook → Business requirement → Architecture → Service → Class → Method
→ Validation → Regression test
```

---

## 24. Engineering Goal

Professional petroleum economics platform with maintainability, scalability, validation fidelity, and expansion capacity.
