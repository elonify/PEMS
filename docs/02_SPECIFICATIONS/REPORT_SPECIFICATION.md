# REPORT_SPECIFICATION.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Reporting specification  

---

## 1. Purpose

Defines reporting architecture, report types, data contracts, and constraints.

---

## 2. Principles

- Reports consume **ReportDataset** (and embedded ChartDataset references) only.  
- **No business calculations** during report generation.  
- Reports use validated run results only.  
- Export formats are presentation concerns.  

---

## 3. Report Types

| Report | Audience | Typical contents |
|--------|----------|------------------|
| Executive Summary | Decision makers | KPIs, NPV/IRR, key charts |
| Technical Report | Engineers | Production, costs, assumptions |
| Fiscal Report | Fiscal analysts | Royalty, taxes, take statistics |
| Economic Report | Economists | Cash flow, metrics, limit |
| Sensitivity Report | Risk | Tornado/spider results |
| Portfolio Report | Management | Multi-project (future) |
| Scenario Report | Analysts | Scenario compare |
| Validation Report | QA | Workbook compare summary |

---

## 4. ReportDataset Contract

| Field | Description |
|-------|-------------|
| report_type | enum |
| title / subtitle | strings |
| project / scenario metadata | |
| tables | columnar data with units |
| metrics | key-value with units |
| chart_refs | ChartDataset ids or inline |
| assumptions | listed inputs snapshot |
| generated_at | timestamp |
| workbook_version | for audit |
| run_id | |

---

## 5. Pipeline

```text
RunResult (validated)
→ ReportBuilder (select template)
→ ReportDataset
→ ReportRenderer (PDF/Word/PPT/Excel/HTML)
→ ExportService
```

---

## 6. Templates

Each report type has a layout template. Templates define section order, not formulas.

---

## 7. Validation

Before generation: ensure RunResult validation status is acceptable per policy.  
Optional: include validation appendix.

---

## 8. Traceability

Workbook report areas map to report templates in WORKBOOK_MAPPING_SPECIFICATION.
