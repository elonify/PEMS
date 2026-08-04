# ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md

Version: 2.0
Status: Single Source of Truth (SSOT)
Project: Elonify Petroleum Economics Modeling System (PEMS)
Author: Dr. Emmanuel Onwuka
Implementation Platform: Python
Target Platform: Cross-Platform Desktop Application

---

# 1. Executive Summary

## 1.1 Purpose

This document is the authoritative software architecture and implementation guide for Elonify Petroleum Economics Modeling System (PEMS).

It supersedes previous architecture documents and shall be regarded as the Single Source of Truth (SSOT) governing the design, implementation, validation, testing, and future evolution of the software.

The objective of Elonify PEMS is to transform a mature Microsoft Excel-based petroleum economics model into a modern, enterprise-grade engineering application while preserving the exact business logic, calculations, and outputs of the validated workbook.

The Excel workbook represents the validated business specification.

The software represents the engineering implementation of that specification.

---

# 2. Guiding Principles

The following principles govern every implementation decision.

## Principle 1 — Excel is the Business Specification

The Excel workbook defines the business rules.

It does not define the software architecture.

---

## Principle 2 — Architecture Governs Implementation

All software components shall conform to this architecture.

No implementation shall bypass the architecture.

---

## Principle 3 — Validation Before Completion

A feature is complete only when:

- implemented
- tested
- validated against Excel
- documented

---

## Principle 4 — Modularity

Every module shall have a single responsibility.

Modules shall communicate through well-defined interfaces.

---

## Principle 5 — Business Objects

Charts, reports, dashboards and APIs shall consume business objects.

They shall never consume worksheet structures.

---

## Principle 6 — Extensibility

The application shall be designed for future expansion without major architectural redesign.

---

# 3. Single Source of Truth (SSOT)

The documentation hierarchy shall be:

Workbook

↓

ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md

↓

Module Specifications

↓

Implementation

↓

Validation

↓

Release

This document governs every development activity.

Whenever the workbook changes, this document shall be reviewed before implementation continues.

---

# 4. Project Objectives

The software shall:

• reproduce Excel calculations exactly

• support multiple fiscal regimes

• support multiple countries

• support multiple projects

• support multiple scenarios

• support portfolio analysis

• support sensitivity analysis

• support Monte Carlo analysis

• support professional engineering reporting

• support enterprise dashboards

• support cross-platform deployment

---

# 5. Software Philosophy

The project shall not become an "Excel clone."

Instead it shall become a professional petroleum economics platform.

Excel remains the validation benchmark.

Software remains the implementation.

---

# 6. Development Lifecycle

Development shall proceed through the following phases.

Phase 1

Workbook Analysis

↓

Phase 2

Input Declaration

↓

Phase 3

Calculation Engine

↓

Phase 4

Excel Validation

↓

Phase 5

Business Object Layer

↓

Phase 6

Chart Engine

↓

Phase 7

Reporting

↓

Phase 8

Dashboard

↓

Phase 9

Packaging

↓

Phase 10

Release

No phase shall begin until the previous phase satisfies its exit criteria.

---

# 7. Workbook Analysis

Every worksheet shall be analysed to identify:

• Purpose

• Inputs

• Outputs

• Named Ranges

• Formula Groups

• Lookup Tables

• Validation Rules

• Hidden Calculations

• Dependencies

• Charts

• Reports

• Macros

• Assumptions

Every worksheet shall map to one or more application modules.

---

# 8. Workbook-to-Application Mapping

Each worksheet shall be documented as follows.

Worksheet Name

Business Purpose

Application Module

Dependencies

Input Objects

Output Objects

Validation Strategy

Implementation Status

No worksheet shall remain unmapped.

---

# 9. System Architecture

The application shall be organised into the following layers.

Presentation Layer

↓

Application Layer

↓

Business Services

↓

Calculation Engine

↓

Validation Engine

↓

Domain Objects

↓

Persistence Layer

↓

Configuration Layer

Each layer communicates only with adjacent layers.

---

# 10. Package Structure

src/

    EEM_Project/

        api/

        application/

        calculations/

        charts/

        configuration/

        core/

        dashboard/

        domain/

        exports/

        fiscal/

        infrastructure/

        persistence/

        production/

        reporting/

        services/

        ui/

        validation/

        utilities/

        tests/

Every package shall expose a clean public interface.

Internal implementation details shall remain encapsulated.

---

# 11. Domain Model

The application shall model petroleum economics concepts rather than workbook sheets.

Core domain objects include:

Project

Scenario

Reservoir

Field

ProductionProfile

CostProfile

FiscalRegime

RoyaltyResult

TaxResult

CashFlow

DiscountedCashFlow

EconomicLimit

SensitivityCase

MonteCarloSimulation

EconomicMetrics

ReportDataset

ChartDataset

Every domain object shall be reusable across modules.

---

# 12. Calculation Engine

The calculation engine is responsible for all business calculations.

Modules shall be independent.

The calculation sequence shall follow workbook dependencies.

No calculation module shall access UI controls.

No calculation module shall access chart objects.

No calculation module shall access reports.

The engine shall remain deterministic.

Given identical inputs, identical outputs shall always be produced.

---

# 13. Validation Framework

Validation is mandatory.

No module is complete until validated.

Validation shall occur at four levels.

Level 1

Formula Validation

Level 2

Cell Validation

Level 3

Module Validation

Level 4

Regression Validation

Validation reports shall be generated automatically.

---

# 14. Definition of Ready

Before implementation begins:

✓ Workbook analysed

✓ Formula captured

✓ Inputs identified

✓ Outputs identified

✓ Dependencies documented

✓ Module specification completed

Only then may implementation begin.

---

# 15. Definition of Done

A module is complete only when:

✓ Code implemented

✓ Unit tests passed

✓ Cell validation passed

✓ Workbook validation passed

✓ Regression tests passed

✓ Documentation updated

✓ Git committed

---

# 16. Coding Standards

All code shall:

- be modular
- be type hinted
- be documented
- avoid duplicated logic
- avoid circular dependencies
- favour composition over inheritance
- follow SOLID principles
- remain testable

---

# 17. Git Workflow

One logical change per commit.

Every commit shall reference:

Module

Workbook Sheet

Validation Status

Example:

feat(royalties): implement sliding scale royalty validation or linear interpolation or fixed scale validation against workbook as case may be

---

# 18. Future Modules

The architecture reserves support for:

- Portfolio Economics

- Carbon Economics

- ESG

- AI Decision Support

- Portfolio Ranking

- Economic Optimisation

- Cloud Collaboration

- Plugin Marketplace

Implementation of future modules shall not require redesign of the existing architecture.

---

# 19. Architecture Governance

Whenever the workbook changes:

1. Analyse workbook.

2. Compare against current architecture.

3. Update this document.

4. Update affected module specifications.

5. Implement.

6. Validate.

No implementation shall proceed against an outdated architecture.

---

# 20. Conclusion

This document governs the engineering implementation of Elonify Petroleum Economics Modeling System.

Its objectives are to preserve the integrity of the validated Excel model while providing a scalable, maintainable and extensible software architecture suitable for long-term enterprise use.

Every implementation decision shall remain traceable to the business specification, validated against the workbook and documented within this architecture.