# UI_ARCHITECTURE.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** UI architecture specification  

---

## 1. Purpose

Defines presentation-layer architecture for the PEMS desktop application.

GUI toolkit is **open** (ADR-0007). This document constrains structure and behaviour independent of toolkit.

---

## 2. Principles

- Presentation contains **no business calculations**.  
- UI talks to Application / Services only.  
- All edits flow through validation before domain commit.  
- Charts and reports are views over datasets, not calculation hosts.  
- Accessibility and clear validation messages are required.  

---

## 3. Application Shell

Typical regions:

| Region | Content |
|--------|---------|
| Menu / ribbon | File, Project, Run, Validate, Reports, Tools, Help |
| Navigation | Project explorer: project → scenarios → modules |
| Workspace | Editors, grids, results tables |
| Chart pane | Chart views bound to ChartDataset |
| Status bar | Validation state, workbook version, run time |
| Dashboard home | KPIs, recent projects, scenario summary |

---

## 4. Primary UI Flows

### 4.1 Project lifecycle

New Project (template) → Enter/import data → Validate → Run → Review results → Export/Report.

### 4.2 Input

- Form-based manual entry  
- Grid editors for schedules  
- Import Wizard (Excel/CSV)  
- Paste into grids  
- Unit selectors with conversion feedback  

### 4.3 Run

Run active scenario; progress indication for long Monte Carlo; cancel policy TBD at implementation without losing saved inputs.

### 4.4 Validation UI

Show workbook compare summary; drill into failed cells; link to module.

---

## 5. View Models

UI uses view models / DTOs projected from domain objects — not raw worksheets.

Bindings:

- Input screens ↔ draft domain objects + ValidationResult  
- Results grids ↔ CashFlow / metrics  
- Charts ↔ ChartDataset  
- Reports ↔ ReportDataset  

---

## 6. Theming & UX

- Theme settings via configuration  
- Keyboard shortcuts (documented in user help later)  
- Undo/redo for input edits (Phase 16 polish)  
- Context help / tooltips on fiscal and economic fields  

---

## 7. Error Presentation

Validation errors inline + summary panel. Fatal errors dialog + log. Never silent fail.

---

## 8. Chart Hosting

Chart widgets host renderer from Chart Engine. Axis policy (including dual-axis zero alignment) is **engine responsibility**, not ad-hoc UI code.

---

## 9. Independence

Swapping GUI toolkit must not require rewriting calculation engine or domain model (TECHNOLOGY_STACK / SYSTEM_DESIGN).

---

## 10. Out of Scope for pure UI doc

Business formulas, fiscal algorithms, Excel cell addresses (belong in mapping / modules).
