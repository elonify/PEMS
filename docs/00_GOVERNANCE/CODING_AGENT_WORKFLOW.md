# CODING_AGENT_WORKFLOW.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Standard Operating Procedure (SOP)  
**Supersedes:** pre-v2.1 CODING_AGENT_WORKFLOW and overlapping CLAUDE operational policy  

---

## 1. Purpose

Mandatory workflow for all AI coding agents and human developers contributing to PEMS.

Ensures every implementation is repeatable, traceable, validated, documented, and consistent.

---

## 2. Engineering Philosophy

The objective is **not** to clone Excel’s UI.

The objective is to engineer a professional petroleum economics platform while preserving validated business logic from the Excel Golden Master.

- Workbook = business calculation specification  
- Software = engineering implementation  

---

## 3. Order of Authority

1. Latest approved Excel Golden Master  
2. MASTER_IMPLEMENTATION_DIRECTIVE.md  
3. ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md  
4. SYSTEM_DESIGN.md, TECHNOLOGY_STACK.md, DIRECTORY_STRUCTURE.md, and `docs/02_SPECIFICATIONS/*`  
5. VALIDATION_FRAMEWORK.md  
6. Module specification (from MODULE_IMPLEMENTATION_TEMPLATE)  
7. Source code  

If conflicts exist, the higher authority prevails. Escalate unresolved conflicts.

---

## 4. End-to-End Workflow

```text
Project / task
→ Workbook analysis
→ Architecture review
→ Module specification
→ Implementation
→ Unit testing
→ Workbook validation
→ Integration / regression
→ Documentation update
→ Tracker / changelog update
→ Git commit
→ Next module
```

No stage may be skipped.

---

## 5. Step Detail

### Step 1 — Receive task

Identify: workbook version, target worksheet(s), business objective, target module, expected outputs.

Do not code immediately.

### Step 2 — Analyse workbook

Document: purpose, inputs, outputs, named ranges, formula groups, dependencies, hidden logic, validation rules, assumptions, edge cases, charts/reports if present.

### Step 3 — Review architecture

Determine package, service, domain objects, dependencies, validation strategy. Do not bypass layer rules.

### Step 4 — Module specification

Complete a copy of `docs/03_IMPLEMENTATION/MODULE_IMPLEMENTATION_TEMPLATE.md` for the module (store under `docs/02_SPECIFICATIONS/modules/` when created).

### Step 5 — Implement

Single responsibility; typed; documented; no duplicated logic; no UI/chart/report coupling in calculation code.

### Step 6 — Unit testing

Normal, boundary, invalid, missing, extreme cases.

### Step 7 — Workbook validation

Formula → cell → module → integration → regression as applicable. Produce validation evidence per VALIDATION_FRAMEWORK.

### Step 8 — Documentation

Update only affected docs: mapping, architecture (if needed), tracker, changelog.

### Step 9 — Commit

One logical feature. Message format: `type(scope): summary`

Examples:

- `feat(cashflow): implement discounted cash flow engine`
- `fix(fiscal): correct royalty calculation`
- `test(validation): add regression scenario`
- `docs(system): update domain model`

---

## 6. Workbook Change Workflow

```text
Receive new workbook
→ Register version + checksum
→ Diff previous Golden Master
→ Identify impacted modules
→ Update WORKBOOK_MAPPING and specs
→ Update validation datasets
→ Implement
→ Full regression
→ Archive validation reports
→ Commit
```

Workbook changes must never be ignored.

---

## 7. Dependency Direction

```text
Presentation / UI
→ Application
→ Business services
→ Calculation engine
→ Domain objects
→ Infrastructure
```

Dependencies never point upward. Domain objects do not depend on UI or infrastructure frameworks.

---

## 8. Calculation Rules

Calculation modules shall:

- receive validated inputs  
- produce structured outputs  
- remain deterministic  
- avoid side effects  
- avoid UI, report generation, and chart manipulation  
- never read spreadsheet cells at runtime for business results (validation tooling may read Excel for comparison only)

---

## 9. Charts and Reports Timing

Charts and reports consume `ChartDataset` / `ReportDataset` only — never worksheet structures.

Chart engine includes dynamic scaling and **primary/secondary Y-axis zero alignment** (see CHART_SPECIFICATION).

Implement charts only after calculation + business objects for the relevant series exist (see IMPLEMENTATION_SEQUENCE).

Reports contain no business calculations.

---

## 10. Error Handling

- Validate inputs early  
- Meaningful exceptions  
- No silent failures  
- Log recoverable errors  
- Fail closed on unrecoverable errors  

---

## 11. Refactoring Policy

Allowed only if behaviour unchanged, regression and workbook validation pass, and documentation remains accurate.

---

## 12. Performance Policy

Priority: (1) Correctness (2) Validation (3) Readability (4) Maintainability (5) Performance.

---

## 13. Definition of Ready / Done

See MASTER_IMPLEMENTATION_DIRECTIVE.md sections 8–9. Agents shall not start without Ready criteria; shall not claim Done without Done criteria.

---

## 14. Traceability Chain

```text
Workbook version → Worksheet → Business requirement → Architecture section
→ Module specification → Python module → Class → Function
→ Unit test → Validation report → Git commit
```

No orphaned implementation.

---

## 15. Contribution Rules (humans and agents)

Every contribution must:

- follow architecture  
- preserve workbook fidelity  
- include validation and tests  
- update documentation when required  
- pass regression when in scope  

Code style: PEP 8, type hints, docstrings, cohesive modules.

---

## 16. Final Principle

Every agent is an engineering partner responsible for integrity, traceability, and maintainability of PEMS — not a bulk code generator.
