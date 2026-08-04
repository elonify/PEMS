# CLAUDE.md

Version: 2.0
Status: Operational Instructions
Project: Elonify Petroleum Economics Modeling System (PEMS)

---

# Purpose

This document defines the operating rules for Claude Code (and compatible AI coding agents) working on Elonify PEMS.

Its purpose is to ensure that every implementation is:

- Consistent
- Traceable
- Validated
- Modular
- Enterprise-grade

Claude shall treat this document as operational policy.

---

# Project Mission

Develop Elonify PEMS into an enterprise-grade petroleum economics platform by faithfully implementing the validated Excel workbook while applying modern software engineering principles.

The objective is not to reproduce Excel.

The objective is to reproduce the validated business logic using professional software architecture.

---

# Project Authority

Development shall follow the following order of authority.

1. Latest Approved Excel Workbook (Business Specification)

↓

2. ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md (SSOT)

↓

3. SYSTEM_DESIGN.md

↓

4. VALIDATION_FRAMEWORK.md

↓

5. Module Specifications

↓

6. Source Code

If a conflict exists, the higher authority prevails.

---

# Primary Responsibilities

Claude shall:

- Analyse before coding.
- Understand business intent.
- Preserve calculation fidelity.
- Maintain modular architecture.
- Produce readable code.
- Produce maintainable code.
- Validate every implementation.
- Update documentation where required.

Claude shall never implement features that bypass the approved architecture.

---

# Engineering Principles

Claude shall always:

- Think before coding.
- Prefer clarity over cleverness.
- Prefer composition over inheritance.
- Minimise coupling.
- Maximise cohesion.
- Keep modules independent.
- Preserve deterministic calculations.
- Avoid hidden assumptions.

---

# Workbook Synchronisation

Whenever a new workbook is supplied:

Claude shall:

1. Analyse the workbook.

2. Compare with previous workbook.

3. Identify:

- New worksheets
- Deleted worksheets
- Changed formulas
- Changed assumptions
- Changed workflows

4. Determine impacted modules.

5. Update architecture if required.

6. Continue implementation.

No implementation shall continue against an outdated workbook.

---

# Before Writing Code

Before implementing any module:

Claude shall identify:

Business Purpose

Inputs

Outputs

Dependencies

Formula Groups

Validation Rules

Expected Outputs

Edge Cases

Only then shall implementation begin.

---

# Implementation Rules

Every module shall:

Have one responsibility.

Expose a clean interface.

Avoid circular dependencies.

Avoid duplicated code.

Remain independently testable.

Not depend upon UI.

Not depend upon charts.

Not depend upon reports.

Business logic shall remain independent.

---

# Coding Standards

Python Version

Latest approved project version.

Use:

- Type hints
- Dataclasses or Pydantic where appropriate
- Docstrings
- Logging
- Exception handling
- Dependency Injection where applicable

Avoid:

- Global variables
- Hard-coded constants
- Hidden state
- Duplicate algorithms

---

# Calculation Rules

Calculation modules shall:

Accept structured inputs.

Return structured outputs.

Never access GUI components.

Never manipulate charts.

Never generate reports.

Never read spreadsheet cells directly.

Calculations must remain deterministic.

---

# Business Objects

Claude shall use domain objects.

Examples

Project

Scenario

ProductionProfile

FiscalRegime

CashFlow

EconomicMetrics

ChartDataset

ReportDataset

Business objects shall be reusable.

---

# Validation Requirements

Every implementation shall be validated.

Validation order:

Formula Validation

↓

Cell Validation

↓

Module Validation

↓

Regression Testing

↓

Documentation Update

No module is complete without validation.

---

# Testing Requirements

Every module shall include:

Unit Tests

Integration Tests (where applicable)

Regression Tests

Validation Dataset

Expected Outputs

Tests shall be automated.

---

# Documentation Requirements

Whenever implementation changes:

Claude shall determine whether documentation requires updating.

Documentation includes:

Architecture

Validation Framework

System Design

Module Specification

README

Only update documentation affected by the implementation.

---

# Git Workflow

One logical change per commit.

Commit messages shall follow:

type(scope): description

Examples

feat(fiscal): implement royalty calculation

fix(cashflow): correct depreciation sequence

test(validation): add regression scenario

docs(architecture): update module mapping

---

# Definition of Ready

Claude shall not begin implementation until:

Workbook analysed

Architecture current

Module identified

Inputs documented

Outputs documented

Dependencies understood

Validation strategy defined

---

# Definition of Done

Implementation is complete only when:

✓ Code complete

✓ Unit tests pass

✓ Validation passes

✓ Regression passes

✓ Documentation updated

✓ Ready for commit

---

# Error Handling

Claude shall:

Detect errors early.

Fail gracefully.

Produce meaningful messages.

Avoid silent failures.

Log recoverable errors.

Raise exceptions for unrecoverable conditions.

---

# Performance

Optimise only after correctness.

Correctness has higher priority than speed.

Avoid premature optimisation.

---

# Security

Do not expose internal implementation details.

Validate all external inputs.

Never trust user input.

Protect configuration.

Avoid storing secrets in source code.

---

# Refactoring

Claude may refactor only when:

Behaviour remains unchanged.

Regression tests pass.

Validation passes.

Architecture remains consistent.

---

# Charts

Charts are not implemented during the current development phase.

Claude shall only prepare the architecture necessary for future chart implementation.

Charts shall consume business objects rather than workbook structures.

---

# Reports

Reports shall not contain business logic.

Reports consume validated business objects only.

---

# Dashboard

Dashboard implementation occurs only after:

Calculation Engine

Validation

Business Objects

have been completed.

---

# Decision Making

Whenever multiple implementation choices exist:

Claude shall choose the solution that:

Improves maintainability.

Improves readability.

Improves extensibility.

Preserves validation fidelity.

Reduces technical debt.

---

# Escalation

Claude shall request clarification whenever:

Business rules are ambiguous.

Workbook behaviour is inconsistent.

Architecture conflicts arise.

Validation cannot be completed.

No assumptions shall be made about business rules without explicit justification.

---

# Final Principle

Claude is not merely a code generator.

Claude is an engineering partner responsible for preserving the integrity, traceability, and long-term maintainability of Elonify PEMS.

Every implementation decision shall support the project's objective of delivering a professional, enterprise-grade petroleum economics platform that faithfully reproduces the validated Excel business specification.