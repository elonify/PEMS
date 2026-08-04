# API_SPECIFICATION.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Specification (v1 desktop-first; external API deferred)  

---

## 1. Purpose

Defines application-facing interfaces for PEMS.

For Documentation Baseline v2.1 and the workbook-parity product line (**2.x**), PEMS is a **desktop application**. A public HTTP REST API is a **future** capability (roadmap 3.x–6.x / plugin era), not a v1 delivery requirement.

This document still specifies:

1. **Internal application API** (services used by UI and agents of the system)  
2. **Future external API** boundaries so design does not paint the architecture into a corner  

---

## 2. Internal Service API (v1 required)

UI and application layer call services; they do not call calculation modules ad hoc.

### 2.1 ProjectService

| Operation | Description |
|-----------|-------------|
| create_project | Create project from template or blank |
| open_project | Load from persistence |
| save_project | Persist |
| save_as | Clone project |
| list_recent | Recent projects |

### 2.2 Input / ImportService

| Operation | Description |
|-----------|-------------|
| validate_inputs | Run input validation rules |
| import_excel | Excel import path |
| import_csv | CSV import path |
| import_clipboard | Paste path |
| apply_template | Project template |

All import operations return domain objects + ImportAuditRecord + ValidationResult.

### 2.3 ScenarioService

create/clone scenario; set active scenario; run scenario.

### 2.4 Calculation façade (EconomicsService / orchestrator)

`run_full_evaluation(scenario_id) -> RunResult`  
Orchestrates calculation pipeline; never invoked with unvalidated inputs.

### 2.5 ValidationService

`compare_to_workbook(...)`, `run_regression_suite(...)`, `export_validation_report(...)`.

### 2.6 ChartService / ReportingService / ExportService

Build ChartDataset/ReportDataset from RunResult; render/export only.

---

## 3. Contracts

- Inputs/outputs are domain objects (DATA_MODEL), not DataFrames leaked to UI.  
- Errors are typed (validation vs calculation vs persistence).  
- Operations are side-effect explicit (save vs pure run).  

---

## 4. Future External API (non-v1)

If/when exposed:

- REST or equivalent over local/remote host  
- Authn/z required  
- Same domain contracts as internal services  
- No alternate calculation path  

Illustrative resource map (not implemented in v1):

```text
POST /projects
GET  /projects/{id}
POST /projects/{id}/import/excel
POST /scenarios/{id}/run
GET  /runs/{id}/metrics
GET  /runs/{id}/charts/{type}
```

---

## 5. API Versioning (future)

URL or header versioning; breaking changes only in major product versions.

---

## 6. Non-Requirements for v1

- Public cloud multi-tenant API  
- Third-party OAuth  
- GraphQL  

---

## 7. Consistency

Internal APIs must obey layer rules in SYSTEM_DESIGN and must not bypass VALIDATION_FRAMEWORK.
