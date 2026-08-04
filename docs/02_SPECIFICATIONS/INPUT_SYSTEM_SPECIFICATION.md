# INPUT_SYSTEM_SPECIFICATION.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Approved specification  
**Supersedes:** pre-v2.1 INPUT_SYSTEM_SPECIFICATION  

---

## 1. Purpose

Defines the official data input architecture for PEMS.

The Input System provides all mechanisms through which business data enters the application.

Regardless of source, every input **shall** pass through the **same** Validation Engine and Domain Object layer before the Calculation Engine.

---

## 2. Design Objectives

Flexible, user-friendly, enterprise-ready, fully validated, traceable, extensible, independent of calculations.

Multiple acquisition methods; identical business behaviour after validation.

---

## 3. Input Architecture

```text
                    Input Manager
                          │
    ┌──────────┬──────────┼──────────┬──────────┐
 Manual    Excel Import  CSV Import  Project Template
    │          │          │          │
 Copy/Paste  Database*   API*    Previous Project
                          │
                  Validation Engine
                          │
                   Domain Objects
                          │
                 Calculation Engine
```

(\* Future releases)

---

## 4. Supported Input Methods

### 4.1 Manual Entry (primary)

Validated forms for: project information, reservoir properties, production assumptions, cost assumptions, fiscal parameters, economic assumptions.

Includes: drop-downs, tooltips, input masks, range validation, required fields, unit selection, immediate feedback.

### 4.2 Excel Workbook Import

Import from Excel workbooks:

- Official PEMS / Golden Master structure recognition  
- Named ranges, worksheets, tables, selected datasets  

Workflow:

```text
Select Workbook → Analyse → Recognise Structure → Validate → Preview → Import
```

Recognise official Golden Master automatically when possible (version, structure, named ranges).

### 4.3 Smart Workbook Recognition

Detect: workbook version, worksheet structure, named ranges, hidden/protected sheets, formula dependencies (for mapping guidance — not for runtime calc).

Users should not manually map standard PEMS workbooks.

### 4.4 Generic Excel Import

Non-standard workbooks: Preview → Column mapping → Validation → Import. Mappings savable for reuse.

### 4.5 CSV Import

Datasets: production forecasts, historical production, price decks, CAPEX/OPEX schedules, Monte Carlo inputs.

Validate: headers, units, data types, missing values, duplicate records.

### 4.6 Copy and Paste

Copy from Excel → Paste → Automatic validation → Import.

Supports single cells, tables, entire schedules.

### 4.7 Project Templates

Examples: Nigeria PIA, PSC, Concession, Marginal Field, Deepwater Development.

Populate defaults; user may modify; all values re-validated.

### 4.8 Existing Project Import / Save As

Open → Save As → Modify → Run (rapid scenarios).

### 4.9 Future: Database / API

SQLite, SQL Server, PostgreSQL, Oracle; Petrel, OFM, NUPRC, corporate DBs — optional adapters later.

---

## 5. Unified Validation Path

```text
Manual | Excel | CSV | Paste | Template | DB* | API*
              ↓
      Validation Engine
              ↓
       Domain Objects
              ↓
    Calculation Engine
```

**No calculation shall execute on unvalidated input.**  
**No separate incompatible validation logic for import vs manual entry.**

---

## 6. Validation Rules

Required fields, data types, units, value ranges, enumerations, cross-field consistency, duplicates, missing records.

Errors identify field and recommended correction.

---

## 7. Units Management

Automatic unit conversion before calculations (e.g. bbl/day ↔ m³/day, MMscf ↔ m³, USD ↔ local currency where applicable).

---

## 8. Import Wizard

```text
Select Source → Analyse → Preview → Map Fields → Validate → Import → Import Report
```

---

## 9. Error Handling

Import errors must not crash the application. Provide description, location, suggestion, severity, summary.

---

## 10. Audit Trail

Every imported dataset records: source, date, user, workbook version, method, validation status.

---

## 11. Performance Targets

| Operation | Target |
|-----------|--------|
| Manual entry feedback | Immediate |
| Workbook import | < 5 s (typical) |
| CSV import | < 2 s (typical) |
| Paste | < 1 s (typical) |
| Validation | Real-time where interactive |

---

## 12. Future Expansion

Cloud storage, SharePoint, OneDrive, corporate DBs, REST APIs, AI-assisted extraction, OCR — without redesigning input architecture.

---

## 13. Critical-path input taxonomy (PO decisions — CLOSED)

| Source | Treatment | Spec |
|--------|-----------|------|
| **Equity Dash Share** (e.g. **C4**) | **INPUT** — user/input variable; **not** derived (C5 on GM is formula `=C6-C4` — derived) | `modules/EQUITY_DASH_SHARE_INPUT.md` |
| **Fiscal Terms_PIA** | **LAW TABLE** — regulatory fiscal rules; **not** ordinary user inputs | `modules/FISCAL_TERMS_PIA_LAW_TABLE.md` |
| **Hidden sheets** | Out of input classification scope | `SCOPE_VISIBLE_SHEETS_ONLY.md` |

**Schema sketch:** `INPUT_SCHEMA_CRITICAL_PATH.md`  

Must include equity share in: classification, schema, manual UI, Excel import mapping, validation, semantic mapping, module specs.

---

## 14. Final Principle

Input is the gateway to PEMS. Every dataset is validated, traceable, and transformed into domain objects before calculation — ensuring consistency with Golden Master behaviour and enterprise-grade acquisition flexibility.
