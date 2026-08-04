# CODING_AGENT_WORKFLOW.md

Version: 2.0
Status: Standard Operating Procedure (SOP)
Project: Elonify Petroleum Economics Modeling System (PEMS)

---

# 1. Purpose

This document defines the mandatory workflow for all AI coding agents and human developers contributing to Elonify PEMS.

It ensures every implementation is:

- Repeatable
- Traceable
- Validated
- Documented
- Consistent

This workflow applies to:

- Claude Code
- Codex
- Cursor
- GitHub Copilot
- Gemini CLI
- OpenHands
- Human Developers
- Other Coding Agents

Every contributor shall follow the same engineering process.

---

# 2. Engineering Philosophy

The objective is NOT to convert Excel into Python.

The objective is to engineer a professional petroleum economics platform while preserving the validated business logic contained in the Excel workbook.

The workbook defines the business specification.

The software implements that specification.

---

# 3. Order of Authority

Every coding agent shall consult documents in the following order:

1. Latest Approved Excel Workbook

↓

2. ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md

↓

3. SYSTEM_DESIGN.md

↓

4. VALIDATION_FRAMEWORK.md

↓

5. Module Specification

↓

6. Source Code

If conflicting information exists, the higher authority prevails.

---

# 4. Development Workflow

Every implementation shall follow this sequence.

Project

↓

Workbook Analysis

↓

Architecture Review

↓

Module Specification

↓

Implementation

↓

Validation

↓

Documentation Update

↓

Git Commit

↓

Next Module

No stage may be skipped.

---

# 5. Step 1 – Receive Task

Before writing code:

Identify:

- Workbook Version
- Target Worksheet(s)
- Business Objective
- Target Module
- Expected Outputs

Do not begin coding immediately.

---

# 6. Step 2 – Analyse Workbook

Review the worksheet thoroughly.

Identify:

Purpose

Inputs

Outputs

Named Ranges

Formula Groups

Dependencies

Hidden Logic

Validation Rules

Assumptions

Edge Cases

Charts (if present)

Reports (if present)

Document findings before coding.

---

# 7. Step 3 – Review Architecture

Review:

ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md

Determine:

Target package

Target service

Target domain object

Dependencies

Validation strategy

Do not bypass architecture.

---

# 8. Step 4 – Prepare Module Specification

For every module document:

Module Name

Business Purpose

Inputs

Outputs

Dependencies

Interfaces

Validation Requirements

Completion Criteria

Only then proceed.

---

# 9. Step 5 – Implement

Implementation requirements:

Single responsibility

Small reusable functions

No duplicated logic

Strong typing

Meaningful names

Comprehensive docstrings

Clear exception handling

Avoid shortcuts.

---

# 10. Step 6 – Unit Testing

Create tests covering:

Normal cases

Boundary conditions

Invalid inputs

Missing data

Extreme values

Unit tests must pass before validation.

---

# 11. Step 7 – Workbook Validation

Compare outputs against Excel.

Validation levels:

Formula

↓

Cell

↓

Module

↓

Integration

↓

Regression

Generate validation report.

---

# 12. Step 8 – Documentation

Determine whether implementation affects:

Architecture

System Design

Validation Framework

Module Specification

README

Update only affected documentation.

---

# 13. Step 9 – Commit

Commit only one logical feature.

Commit message format:

type(scope): summary

Examples

feat(cashflow): implement discounted cash flow engine

fix(fiscal): correct royalty calculation

test(validation): add regression scenario

docs(system): update domain model

---

# 14. Workbook Change Workflow

Whenever the workbook changes:

Receive workbook

↓

Compare with previous version

↓

Identify impacted modules

↓

Update architecture

↓

Update specifications

↓

Implement

↓

Validate

↓

Commit

Workbook changes shall never be ignored.

---

# 15. Coding Standards

Every implementation shall:

Use type hints

Follow SOLID principles

Avoid global state

Avoid duplicated algorithms

Avoid hidden dependencies

Separate business logic from presentation

Keep modules independently testable

---

# 16. Dependency Rules

Presentation

↓

Application

↓

Services

↓

Calculation Engine

↓

Domain Objects

↓

Infrastructure

Dependencies shall never point upward.

---

# 17. Business Objects

Business objects represent petroleum economics concepts.

Examples

Project

Scenario

Field

Reservoir

ProductionProfile

FiscalRegime

CashFlow

EconomicMetrics

ChartDataset

ReportDataset

Business objects shall not contain UI code.

---

# 18. Calculation Rules

Calculation modules shall:

Receive validated inputs

Produce structured outputs

Remain deterministic

Avoid side effects

Avoid UI interaction

Avoid report generation

Avoid chart manipulation

---

# 19. Validation Rules

No implementation is complete until:

Formula validation passed

Cell validation passed

Module validation passed

Regression passed

Documentation updated

Validation reports archived

---

# 20. Charts

Charts are implemented only after:

Calculation Engine

Business Objects

Validation Framework

have been completed.

Charts consume ChartDataset only.

They shall never consume worksheet structures.

---

# 21. Reports

Reports consume ReportDataset objects only.

Reports contain no business logic.

Reports perform no calculations.

---

# 22. Dashboard

Dashboard components display validated data only.

They shall never execute calculations.

They shall never modify business objects.

---

# 23. Error Handling

Every module shall:

Validate inputs

Provide meaningful exceptions

Avoid silent failures

Log recoverable errors

Stop execution for unrecoverable errors

---

# 24. Refactoring Policy

Refactoring is permitted only if:

Behaviour remains unchanged

Regression tests pass

Workbook validation passes

Documentation remains accurate

---

# 25. Performance Policy

Priority order:

1. Correctness

2. Validation

3. Readability

4. Maintainability

5. Performance

Performance optimisation shall never compromise correctness.

---

# 26. Definition of Ready

Implementation begins only when:

✓ Workbook analysed

✓ Architecture reviewed

✓ Module identified

✓ Dependencies documented

✓ Validation strategy prepared

✓ Module specification approved

---

# 27. Definition of Done

A module is complete only when:

✓ Code implemented

✓ Unit tests passed

✓ Validation passed

✓ Regression passed

✓ Documentation updated

✓ Git committed

✓ Ready for integration

---

# 28. Continuous Improvement

Every completed module should improve:

Maintainability

Readability

Performance (where appropriate)

Reusability

Documentation

Validation coverage

Avoid introducing technical debt.

---

# 29. Engineering Traceability

Every implementation shall trace back to:

Workbook Version

↓

Worksheet

↓

Business Requirement

↓

Architecture Section

↓

Module Specification

↓

Python Module

↓

Class

↓

Function

↓

Unit Test

↓

Validation Report

↓

Git Commit

No orphaned implementation shall exist.

---

# 30. Final Engineering Principle

Every coding agent is expected to act as a software engineer rather than a code generator.

Every decision shall preserve:

- Workbook fidelity
- Architectural integrity
- Validation traceability
- Long-term maintainability
- Enterprise software quality

The goal is to deliver a professional petroleum economics platform whose implementation is fully traceable, validated and extensible.