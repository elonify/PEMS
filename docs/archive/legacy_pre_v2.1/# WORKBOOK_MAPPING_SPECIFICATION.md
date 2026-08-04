# WORKBOOK_MAPPING_SPECIFICATION.md

Version: 2.1

Status: Living Document

Project: Elonify Petroleum Economics Modeling System (PEMS)

---

# 1. Purpose

This document is the permanent mapping between the Excel Golden Master workbook and the PEMS application.

It records how every worksheet, table, chart, named range, formula group and report is implemented inside the software.

It is updated continuously throughout implementation.

---

# 2. Workbook Information

Workbook Name

Workbook Version

Date Approved

Checksum (SHA256)

Author

Number of Worksheets

Number of Named Ranges

Number of Tables

Number of Charts

Number of VBA Modules

---

# 3. Worksheet Inventory

| Worksheet | Status | Module | Validation |
|-----------|--------|--------|------------|
| Inputs | Planned | Input Module | Pending |
| Production | Planned | Production Engine | Pending |
| Revenue | Planned | Revenue Engine | Pending |
| Fiscal | Planned | Fiscal Engine | Pending |
| Cash Flow | Planned | Cash Flow Engine | Pending |

---

# 4. Worksheet Template

Every worksheet shall be documented using the following template.

---

Worksheet Name

Purpose

Business Function

Dependencies

Dependent Worksheets

Named Ranges

Excel Tables

Hidden Cells

Hidden Columns

Hidden Rows

Charts

Reports

External References

---

# 5. Formula Groups

Every major formula block shall be documented.

Example

Production Forecast

Location

B15:M240

Implemented By

ProductionService

Validation

Completed

---

# 6. Named Ranges

Example

OilPrice

Workbook Name

OilPrice

Application Object

PriceModel.oil_price

Validation

Completed

---

# 7. Excel Tables

Each table shall map to a Domain Object.

Example

tblProduction

↓

ProductionProfile

---

# 8. Charts

Each Excel chart maps to one Chart Template.

Example

Excel

Production Chart

↓

PEMS

ProductionChartTemplate

Validation

Completed

---

# 9. Reports

Workbook report

↓

Report Builder Template

Validation

Completed

---

# 10. Workbook Features

Record

Conditional Formatting

Data Validation

Merged Cells

Dynamic Arrays

Spill Ranges

Pivot Tables

Power Query

Macros

Named Formulas

LAMBDA Functions

Dynamic Charts

---

# 11. VBA Replacement

Every VBA macro shall record

Macro Name

Purpose

Replacement Service

Status

---

# 12. Validation

Each worksheet records

Implemented

Validated

Regression Tested

Approved

---

# 13. Traceability

Workbook

↓

Worksheet

↓

Formula Group

↓

Python Module

↓

Function

↓

Unit Test

↓

Validation Test

---

# 14. Change History

Workbook Version

↓

Application Change

↓

Validation Result

↓

Approval

---

# 15. Completion Dashboard

Worksheet

Implementation %

Validation %

Regression %

Documentation %

Status

---

# 16. Final Principle

Every workbook element shall have one—and only one—implementation inside PEMS.

Nothing in the workbook shall remain undocumented.

Nothing shall be implemented without traceability back to the workbook.