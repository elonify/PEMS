# MODULE_IMPLEMENTATION_TEMPLATE.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Standard template  
**Supersedes:** pre-v2.1 MODULE_IMPLEMENTATION_TEMPLATE and MODULE SPECIFICATION templates  

---

## Usage

Copy this file to:

`docs/02_SPECIFICATIONS/modules/<module_name>.md`

Fill every section before coding. Do not manufacture empty module files in bulk.

---

## Module Information

| Field | Value |
|-------|--------|
| Module Name | |
| Module ID | |
| Workbook Worksheet(s) | |
| Workbook Version | |
| Python Package | `pems....` |
| Python Module | |
| Implementation Status | Draft \| Ready \| Implementing \| Validating \| Validated \| Released |
| Developer | |
| Date Started | |
| Date Completed | |

---

## Business Purpose

Describe the business objective (e.g. production forecasting, royalty calculation).

---

## Scope

**This module is responsible for:**

...

**This module does NOT perform:**

...

---

## Workbook Mapping

- Worksheet  
- Named Ranges  
- Tables  
- Charts  
- Reports  
- Formula Blocks  
- Hidden Logic  
- External References  

---

## Dependencies

- Upstream modules  
- Downstream modules  
- Shared services  
- Configuration  
- Validation datasets  

---

## Inputs

| Input | Type | Units | Required | Validation |
|-------|------|-------|----------|------------|

---

## Outputs

| Output | Type | Units | Destination |
|--------|------|-------|-------------|

---

## Business Rules

Every rule shall reference the workbook (sheet/cell/formula group).

1.  
2.  
3.  

---

## Calculation Sequence

```text
Input → Validation → Calculation A → Calculation B → Output
```

---

## Domain Objects

List objects used (ProductionProfile, FiscalTerms, …).

---

## Services

Services used or provided.

---

## Algorithms

Formula groups, iteration, interpolation, lookups, discounting, array operations, special cases.

---

## Formula Catalogue

| Cell | Formula | Description | Python equivalent |
|------|---------|-------------|-------------------|

---

## Edge Cases

Zero production, negative cash flow, zero price, high inflation, high CAPEX/OPEX, economic limit, abandonment year, missing data, invalid units, boundary values.

**IRR / no-sign-change (if module computes IRR):** when the NCF series has no qualifying sign change (including empty/blank series), Excel returns `#NUM!`. PEMS must return **no-IRR** — never invent a rate. Active GM: `Project_NCF!AU14`. See VALIDATION_FRAMEWORK §16.1.

---

## Validation

- Workbook cells compared  
- Expected tolerance  
- Golden Test Cases / scenarios  
- Expected results location  
- Regression tests  

---

## Unit Tests

Normal, edge, boundary, invalid inputs, performance as needed.

---

## Integration Tests

Upstream/downstream modules, chart datasets, reports.

---

## Performance Targets

Calculation time, memory, scalability.

---

## Error Handling

Possible errors, user messages, logging, recovery.

---

## Implementation Checklist (mandatory)

- [ ] Latest workbook obtained; version recorded  
- [ ] Worksheet purpose, I/O, named ranges, formulas, deps documented  
- [ ] Architecture placement confirmed  
- [ ] Code implemented with type hints and docstrings  
- [ ] Unit tests pass  
- [ ] Formula validation pass  
- [ ] Cell validation pass  
- [ ] Module validation pass  
- [ ] Integration tests pass  
- [ ] Regression tests pass  
- [ ] WORKBOOK_MAPPING updated  
- [ ] IMPLEMENTATION_TRACKER updated  
- [ ] CHANGELOG updated if required  
- [ ] Ready for review  

---

## Documentation Touched

List files updated.

---

## Lessons Learned

Implementation notes, known issues, future improvements.

---

## Approval

| Role | Name | Date |
|------|------|------|
| Engineer | | |
| Reviewer | | |
| Validation | | |
