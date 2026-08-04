# DATA_MODEL.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Domain data model specification (living; refine against Golden Master)  

---

## 1. Purpose

Defines domain entities, relationships, and field-level contracts for PEMS.

Until the Golden Master is fully mapped, entities and fields below reflect consolidated pre-v2.1 domain lists plus structural requirements. **Workbook mapping always wins** for calculation fields.

---

## 2. Modelling Rules

- Model petroleum economics concepts, not worksheet grids.  
- All persisted/calculated quantities carry **units** where applicable.  
- Inputs become domain objects only after validation.  
- Results are immutable snapshots per scenario run where feasible.  
- Identifiers are stable UUIDs or project-scoped keys.  

---

## 3. Entity Relationship (logical)

```text
Project 1──* Scenario
Project 1──* Field 1──* Reservoir
Scenario 1──1 ProductionProfile
Scenario 1──1 CostProfile
Scenario 1──1 PriceDeck
Scenario 1──1 FiscalTerms / FiscalRegime
Scenario 1──1 EconomicParameters
Scenario 1──0..1 RiskParameters
Scenario 1──* RunResult
RunResult 1──1 CashFlow
RunResult 1──1 EconomicMetrics
RunResult 0──* ChartDataset
RunResult 0──* ReportDataset
SensitivityCase and MonteCarloSimulation reference Scenario + parameters
Portfolio 1──* Project (future)
```

---

## 4. Core Entities

### 4.1 Project

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | |
| name | string | yes | |
| description | string | no | |
| country | string | no | |
| fiscal_regime_key | string | no | template key |
| created_at / updated_at | datetime | yes | |
| workbook_source_ref | string | no | import audit |
| base_currency | string | yes | e.g. USD |
| unit_system | enum | yes | field / metric preferences |

### 4.2 Scenario

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | |
| project_id | UUID | yes | |
| name | string | yes | Base, High Price, … |
| is_baseline | bool | yes | |
| notes | string | no | |

### 4.3 Field / Reservoir

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | yes | |
| name | string | yes | |
| properties | map | no | porosity, etc. as mapped from workbook |

### 4.4 ProductionProfile

Time series of oil, gas, NGL, water; GOR; water cut; plateau/decline parameters as required by Golden Master.

| Field | Type | Notes |
|-------|------|-------|
| timeline | date[] or year index | Align to workbook time base |
| oil_rate | float[] | units: bbl/d or as configured |
| gas_rate | float[] | |
| ngl_rate | float[] | |
| water_cut | float[] | |
| gor | float[] | |
| cumulative_* | float[] | if workbook computes |

### 4.5 PriceDeck

| Field | Type | Notes |
|-------|------|-------|
| oil_price | float or series | |
| gas_price | float or series | |
| ngl_price | float or series | |
| price_units | string | |

### 4.6 CostProfile

CAPEX, OPEX, abandonment, inflation/escalation schedules per Golden Master.

### 4.7 FiscalRegime / FiscalTerms

Royalty scales, hydrocarbon tax, CIT, education tax/levies, allowances — structure driven by workbook and jurisdiction templates (Nigeria PIA, PSC, Concession, Marginal Field, Deepwater).

### 4.8 EconomicParameters

Discount rates, economic limit rules, depreciation methods as mapped.

### 4.9 CashFlow / DiscountedCashFlow

Period net cash flow, discounted cash flow, financing/working capital components if present in workbook.

### 4.10 EconomicMetrics

NPV, IRR, PI, POT/payout, NPVI, EMV, government take, contractor take — exact set from Golden Master.

**IRR field contract:**

| Situation | Representation |
|-----------|----------------|
| Qualifying sign change present | Numeric IRR (and unit/fraction convention per workbook) |
| No qualifying sign change (Excel `#NUM!`) | Explicit **no-IRR** / undefined state — **not** a fake number |

PEMS must not invent IRR when Excel correctly returns `#NUM!` (see VALIDATION_FRAMEWORK §16.1; GTC-001 `Project_NCF!AU14`).

### 4.11 EconomicLimit

Limit year/flag and truncation rules per workbook.

### 4.12 SensitivityCase / MonteCarloSimulation

Parameter variations; distributions; P10/P50/P90; iteration results.

### 4.13 ChartDataset / ReportDataset

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | |
| chart_or_report_type | string | |
| series | structured | labels, values, axis roles |
| metadata | map | units, titles |
| source_run_id | UUID | |

### 4.14 ImportAuditRecord

Source, date, user, workbook version, method, validation status.

---

## 5. Cross-Cutting Types

- **Money:** amount + currency  
- **Quantity:** value + unit  
- **TimeIndex:** year or period key matching workbook  
- **ValidationResult:** field, severity, message  

---

## 6. Units

Supported conversions (INPUT_SYSTEM): e.g. bbl/day ↔ m³/day, MMscf ↔ m³, currency conversions where applicable. Canonical storage unit per field defined at implementation against workbook; conversion before calculation.

---

## 7. Persistence View

Persistence format open (ADR-0009). Logical aggregates:

- Project file contains project + scenarios + profiles + fiscal terms + last run summaries  
- Templates clone default fiscal/cost/production assumptions  

---

## 8. Traceability

Each calculated field maps to workbook cells via WORKBOOK_MAPPING_SPECIFICATION and module specs.

---

## 9. Evolution

When Golden Master analysis fills real sheets, update this model and ADRs if structural change is required. Do not invent fiscal formulas here — only structure.
