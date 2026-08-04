# SYSTEM_DESIGN.md

Version: 2.0
Status: Engineering Design Specification
Project: Elonify Petroleum Economics Modeling System (PEMS)

---

# 1. Purpose

This document defines the technical design of Elonify PEMS.

While the Excel workbook defines the business specification and
ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md defines the software architecture,
this document defines how the software is engineered.

It specifies:

- System decomposition
- Domain model
- Layer responsibilities
- Component interactions
- Data flow
- Dependency rules
- Service architecture
- Event flow
- Extensibility strategy

This document does not describe implementation details of individual modules.

---

# 2. Design Philosophy

The software shall be engineered as an enterprise application.

The workbook is the business specification.

The application is not an Excel replica.

Business logic shall be separated completely from presentation.

Every component shall have a single responsibility.

Every module shall remain independently testable.

---

# 3. System Layers

Presentation Layer

↓

Application Layer

↓

Business Services

↓

Calculation Engine

↓

Domain Model

↓

Persistence Layer

↓

Infrastructure

Each layer may only communicate with adjacent layers.

---

# 4. Layer Responsibilities

## Presentation Layer

Responsible for:

- User Interface
- Forms
- Dialogs
- Dashboards
- Charts
- Reports

Contains no business logic.

---

## Application Layer

Responsible for:

- Workflow orchestration
- Commands
- Requests
- Navigation
- Session management

Coordinates business services.

---

## Business Services

Responsible for:

- Project creation
- Scenario execution
- Fiscal evaluation
- Economic evaluation
- Report generation
- Export coordination

Business services orchestrate calculations but never perform calculations.

---

## Calculation Engine

Responsible for:

- Production forecasting
- Revenue calculations
- Fiscal calculations
- Discounting
- Economic metrics
- Sensitivity analysis
- Monte Carlo analysis

The engine shall be deterministic.

---

## Domain Layer

Contains business objects.

Examples

Project

Scenario

Reservoir

Field

ProductionProfile

CashFlow

FiscalRegime

EconomicMetrics

No UI logic exists here.

---

## Persistence Layer

Responsible for:

Saving

Loading

Configuration

Project files

Scenario files

Templates

---

## Infrastructure

Responsible for:

Logging

Configuration

Dependency Injection

Caching

File handling

External integrations

---

# 5. High-Level Architecture

Workbook

↓

Input Manager

↓

Calculation Engine

↓

Domain Objects

↓

Application Services

↓

Charts

Reports

Dashboard

Exports

The workbook is never accessed directly by presentation components.

---

# 6. Domain Model

Primary business entities

Project

Field

Reservoir

DevelopmentPlan

Scenario

ProductionProfile

CostProfile

FiscalRegime

Royalty

HydrocarbonTax

CorporateTax

CashFlow

DiscountedCashFlow

EconomicMetrics

EconomicLimit

SensitivityCase

MonteCarloSimulation

Portfolio

Each object represents a petroleum economics concept.

---

# 7. Core Services

ProjectService

ScenarioService

ProductionService

FiscalService

EconomicsService

ValidationService

ChartService

ReportingService

ExportService

ConfigurationService

Services communicate through domain objects.

---

# 8. Dependency Rules

Presentation

may depend upon

Application

Application

may depend upon

Business Services

Business Services

may depend upon

Calculation Engine

Calculation Engine

may depend upon

Domain Objects

Domain Objects

shall depend upon nothing.

Dependencies shall always point downward.

---

# 9. Data Flow

User Input

↓

Validation

↓

Domain Objects

↓

Calculation Engine

↓

Results

↓

Business Objects

↓

Reports

Charts

Dashboard

Exports

No shortcuts permitted.

---

# 10. Event Flow

Typical workflow

Create Project

↓

Load Inputs

↓

Validate Inputs

↓

Run Calculations

↓

Validate Outputs

↓

Generate Results

↓

Refresh Dashboard

↓

Export

---

# 11. Calculation Pipeline

Inputs

↓

Production

↓

Revenue

↓

Royalty

↓

Hydrocarbon Tax

↓

Corporate Tax

↓

Cash Flow

↓

Discounting

↓

Economic Metrics

↓

Economic Limit

↓

Sensitivity

↓

Monte Carlo

Each stage shall expose structured outputs.

---

# 12. Chart Engine (Architecture Only)

The Chart Engine shall remain independent of workbook structures.

Architecture

ChartFactory

↓

ChartBuilder

↓

ChartRenderer

↓

ChartExporter

Supported charts include

Production

Cash Flow

Revenue

Fiscal Take

NPV

IRR

Economic Limit

Sensitivity

Monte Carlo

Tornado

Spider

Waterfall

Charts consume ChartDataset objects only.

---

# 13. Reporting Engine

Reports shall consume ReportDataset objects.

Supported reports

Executive Summary

Technical Report

Fiscal Report

Economic Report

Sensitivity Report

Portfolio Report

No calculations occur during report generation.

---

# 14. Dashboard

Dashboard components display business objects only.

Dashboard widgets include

KPIs

Tables

Charts

Scenario Summary

Project Summary

Recent Runs

Dashboard components never execute calculations.

---

# 15. Export Engine

Supported formats

Excel

PDF

Word

PowerPoint

CSV

JSON

PNG

SVG

Exports consume validated business objects.

---

# 16. Validation Integration

Every calculation request passes through

ValidationService

Validation occurs

Before calculation

After calculation

Before export

Before report generation

---

# 17. Configuration

Configuration files contain

Application settings

Fiscal defaults

Unit preferences

Theme settings

Tolerance values

File paths

Configuration shall never contain business logic.

---

# 18. Error Handling

Errors classified as

Validation

Calculation

Configuration

Persistence

System

Recoverable

Fatal

All errors shall be logged.

---

# 19. Performance

The application shall support

Large projects

Multiple scenarios

Large Monte Carlo simulations

Long production forecasts

Caching shall be applied only where deterministic behaviour is preserved.

---

# 20. Extensibility

Future modules shall include

Portfolio Economics

Carbon Economics

ESG

AI Assistant

Economic Optimisation

Cloud Collaboration

Plugin Marketplace

The architecture shall support these additions without redesign.

---

# 21. Technology Principles

Business logic shall remain independent of

GUI framework

Chart library

Database

Export format

Operating system

This ensures portability.

---

# 22. Design Constraints

Business logic must not

Import GUI libraries

Manipulate charts

Write reports

Access workbook cells

Presentation must not

Perform calculations

Modify domain objects directly

Bypass validation

---

# 23. Traceability

Every component shall trace to

Workbook

↓

Business Requirement

↓

Architecture

↓

Service

↓

Class

↓

Method

↓

Validation

↓

Regression Test

---

# 24. Engineering Goal

The final software shall function as a professional petroleum economics platform rather than an Excel automation tool.

Every design decision shall support maintainability, scalability, validation fidelity and future expansion.
