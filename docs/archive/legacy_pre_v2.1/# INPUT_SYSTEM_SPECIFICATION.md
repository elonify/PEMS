# INPUT_SYSTEM_SPECIFICATION.md

Version: 2.1

Status: Approved

Project: Elonify Petroleum Economics Modeling System (PEMS)

---

# 1. Purpose

This document defines the official data input architecture for Elonify Petroleum Economics Modeling System (PEMS).

The Input System provides all mechanisms through which business data enters the application.

Regardless of source, every input shall pass through the Validation Framework before becoming available to the Calculation Engine.

---

# 2. Design Objectives

The Input System shall be

- Flexible
- User-friendly
- Enterprise-ready
- Fully validated
- Traceable
- Extensible
- Independent of calculations

The Input System shall support multiple data acquisition methods while maintaining identical business behaviour.

---

# 3. Input Architecture

```
                  Input Manager

                         │

 ┌───────────────┬───────────────┬───────────────┐

 │               │               │               │

Manual      Excel Import     CSV Import     Project Template

 │               │               │               │

Copy/Paste   Database*        API*       Previous Project

                         │

                  Validation Engine

                         │

                  Domain Objects

                         │

                Calculation Engine
```

(*Future Releases)

---

# 4. Supported Input Methods

PEMS shall support the following input methods.

## Manual Entry

Primary method.

Users enter information using validated forms.

Examples

- Project information
- Reservoir properties
- Production assumptions
- Cost assumptions
- Fiscal parameters
- Economic assumptions

Manual entry shall include

- Drop-down lists
- Tooltips
- Input masks
- Range validation
- Required field validation
- Unit selection
- Immediate feedback

---

## Excel Workbook Import

PEMS shall import data directly from Excel workbooks.

Supported imports include

- Official PEMS workbook
- Named ranges
- Worksheets
- Tables
- Selected datasets

Workflow

```
Select Workbook

↓

Analyse Workbook

↓

Recognise Structure

↓

Validate

↓

Preview

↓

Import
```

The application shall recognise the official Golden Master workbook automatically whenever possible.

---

## Smart Workbook Recognition

The Input System shall detect

- Workbook version
- Worksheet structure
- Named ranges
- Hidden worksheets
- Protected worksheets
- Formula dependencies

Users shall not be required to manually map standard PEMS workbooks.

---

## Generic Excel Import

For non-standard workbooks.

Workflow

```
Select Workbook

↓

Preview

↓

Column Mapping

↓

Validation

↓

Import
```

Users shall map spreadsheet columns to PEMS fields.

Mappings may be saved for future reuse.

---

## CSV Import

Supported datasets include

- Production forecasts
- Historical production
- Price decks
- CAPEX schedules
- OPEX schedules
- Monte Carlo inputs

The CSV importer shall validate

- Headers
- Units
- Data types
- Missing values
- Duplicate records

---

## Copy and Paste

Users may copy directly from Excel.

Workflow

```
Excel

↓

Copy

↓

Paste

↓

Automatic Validation

↓

Import
```

Supported paste operations include

- Single cells
- Tables
- Entire schedules

---

## Project Templates

PEMS shall provide reusable templates.

Examples

- Nigeria PIA
- PSC
- Concession
- Marginal Field
- Deepwater Development

Templates populate default assumptions while allowing user modification.

---

## Existing Project Import

Users may duplicate existing projects.

Workflow

```
Open Project

↓

Save As

↓

Modify

↓

Run
```

This supports rapid scenario development.

---

## Database Import (Future)

Future versions may import directly from

- SQLite
- SQL Server
- PostgreSQL
- Oracle

Database connections shall remain optional.

---

## API Import (Future)

Future versions may support integration with

- Petrel
- OFM
- NUPRC
- Internal corporate databases

API integrations shall use dedicated adapters.

---

# 5. Input Validation

All input methods shall pass through a common Validation Engine.

```
Manual Entry

Excel

CSV

Copy/Paste

Database

API

↓

Validation Engine

↓

Domain Objects

↓

Calculation Engine
```

No calculation shall execute using unvalidated input.

---

# 6. Validation Rules

The Input System shall validate

- Required fields
- Data type
- Units
- Value ranges
- Enumerations
- Cross-field consistency
- Duplicate records
- Missing records

Validation errors shall clearly identify the affected field and recommended correction.

---

# 7. Units Management

The Input System shall support automatic unit conversion.

Examples

- bbl/day ↔ m³/day
- MMscf ↔ m³
- USD ↔ Local Currency (where applicable)

Conversions shall occur before calculations begin.

---

# 8. Import Wizard

The application shall provide a guided Import Wizard.

Workflow

```
Step 1

Select Source

↓

Step 2

Analyse Data

↓

Step 3

Preview

↓

Step 4

Map Fields

↓

Step 5

Validate

↓

Step 6

Import

↓

Step 7

Generate Import Report
```

---

# 9. Error Handling

Import errors shall never terminate the application unexpectedly.

Users shall receive

- Error description
- Location
- Suggested correction
- Severity
- Import summary

---

# 10. Audit Trail

Every imported dataset shall record

- Source
- Date
- User
- Workbook version
- Import method
- Validation status

This ensures complete traceability.

---

# 11. Performance Targets

Target performance

Manual Entry

Immediate response

Workbook Import

<5 seconds

CSV Import

<2 seconds

Paste Operation

<1 second

Validation

Real-time

---

# 12. Future Expansion

The Input System is designed to support

- Cloud storage
- SharePoint
- OneDrive
- Corporate databases
- REST APIs
- AI-assisted data extraction
- OCR for scanned reports

without requiring architectural redesign.

---

# 13. Final Principle

The Input System is the gateway through which all business data enters Elonify PEMS.

Regardless of origin, every dataset shall be validated, traceable and transformed into domain objects before reaching the Calculation Engine.

This guarantees that calculations remain accurate, reproducible and fully consistent with the Golden Master workbook while providing users with flexible, enterprise-grade data acquisition capabilities.