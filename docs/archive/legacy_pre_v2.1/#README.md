# Elonify Petroleum Economics Modeling System (PEMS)

**Version:** 2.0  
**Status:** Active Development  
**Architecture:** Enterprise Desktop Application  
**Language:** Python  
**Primary Platform:** Windows Desktop (Cross-platform Ready)

---

# Overview

Elonify Petroleum Economics Modeling System (PEMS) is an enterprise-grade petroleum economics application developed from a validated Microsoft Excel model.

The objective is to preserve the business integrity and calculation fidelity of the Excel workbook while transforming it into a maintainable, scalable and extensible desktop application built using modern software engineering practices.

PEMS is designed for petroleum economists, reservoir engineers, asset managers, financial analysts and decision makers involved in upstream oil and gas investment evaluation.

---

# Vision

Develop the industry's most flexible and extensible petroleum economics platform capable of supporting:

- Economic evaluation
- Fiscal modelling
- Production forecasting
- Development planning
- Investment analysis
- Scenario evaluation
- Sensitivity analysis
- Monte Carlo simulation
- Portfolio economics
- Executive reporting
- Engineering dashboards

The application is intended to evolve beyond a workbook replacement into a comprehensive decision-support platform.

---

# Guiding Principles

The project is governed by the following principles:

- The Excel workbook is the validated business specification.
- The Python application is the software implementation.
- Business logic is independent of the user interface.
- Every implementation is validated against the workbook.
- Architecture governs implementation.
- Documentation evolves with the software.
- Correctness takes precedence over optimisation.

---

# Repository Structure

```text
PEMS/

│
├── README.md
├── ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md
├── SYSTEM_DESIGN.md
├── VALIDATION_FRAMEWORK.md
├── CLAUDE.md
├── CODING_AGENT_WORKFLOW.md
├── PROJECT_ROADMAP.md
│
├── docs/
│     ├── module_specs/
│     ├── decisions/
│     └── references/
│
├── src/
│     └── EEM_Project/
│
├── tests/
│
├── validation/
│
├── workbook/
│
└── resources/
```

---

# Documentation Hierarchy

The project documentation is organised as follows:

| Document | Purpose |
|-----------|---------|
| ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md | Single Source of Truth (SSOT) governing architecture and implementation |
| SYSTEM_DESIGN.md | Technical design and software structure |
| VALIDATION_FRAMEWORK.md | Validation methodology and engineering quality assurance |
| CLAUDE.md | Operational instructions for AI coding agents |
| CODING_AGENT_WORKFLOW.md | Standard development workflow |
| PROJECT_ROADMAP.md | Project milestones and future direction |
| README.md | Project overview and entry point |

---

# Development Workflow

Every module follows the same engineering lifecycle.

```text
Workbook

↓

Business Analysis

↓

Architecture Review

↓

Module Specification

↓

Implementation

↓

Unit Testing

↓

Validation

↓

Documentation Update

↓

Git Commit
```

No stage is skipped.

---

# Development Principles

Each implementation must satisfy the following:

- Single responsibility.
- Modular design.
- Strong typing.
- Reusable business objects.
- Automated testing.
- Workbook validation.
- Complete documentation.
- Traceability.

---

# Project Architecture

The application is organised into layered components.

```text
Presentation

↓

Application

↓

Business Services

↓

Calculation Engine

↓

Domain Model

↓

Persistence

↓

Infrastructure
```

Business logic is isolated from the presentation layer to maximise maintainability and testability.

---

# Validation Philosophy

The Excel workbook serves as the Golden Master.

Every implemented feature is compared against the workbook to ensure calculation fidelity.

Validation includes:

- Formula validation
- Cell validation
- Module validation
- Integration validation
- Regression testing

No module is considered complete until all required validation activities have passed.

---

# Coding Standards

The project follows these engineering standards:

- SOLID principles
- Type hints
- Comprehensive docstrings
- Modular design
- Dependency injection where appropriate
- Automated unit testing
- Automated regression testing
- Consistent exception handling

---

# Branch Strategy

Recommended Git branches:

```text
main

develop

feature/<module>

release/<version>

hotfix/<issue>
```

Only validated code is merged into `main`.

---

# Definition of Ready

A feature is ready for implementation when:

- Workbook analysis is complete.
- Architecture has been reviewed.
- Inputs and outputs are defined.
- Dependencies are identified.
- Validation strategy has been documented.

---

# Definition of Done

A feature is complete only when:

- Implementation is complete.
- Unit tests pass.
- Validation against Excel passes.
- Documentation is updated.
- Regression tests pass.
- Changes are committed to version control.

---

# Current Development Status

The project is progressing through the following stages:

- Documentation
- Workbook analysis
- Input declaration
- Calculation engine implementation
- Validation
- Business object layer
- Chart engine
- Reporting engine
- Dashboard
- Packaging

Each stage must satisfy its defined exit criteria before the next stage begins.

---

# Future Enhancements

The architecture supports future capabilities including:

- Multi-country fiscal regimes
- Portfolio management
- Carbon economics
- ESG analysis
- AI-assisted decision support
- Risk analysis
- Cloud collaboration
- Plugin architecture
- REST API integration
- Advanced reporting

These capabilities are accommodated within the architecture without requiring major redesign.

---

# Contributing

All contributors, whether human or AI-assisted, shall follow the project documentation in the prescribed order of authority.

Contributions should:

- Preserve workbook fidelity.
- Maintain architectural integrity.
- Include validation.
- Include tests.
- Update documentation where required.

---

# License

Project-specific licensing terms shall be defined by the project owner.

Until then, all project assets, documentation and business logic remain proprietary.

---

# Contact

**Project Owner:**  
Dr. Emmanuel Onwuka

---

# Acknowledgements

This project builds upon years of petroleum economics modelling experience and aims to combine validated engineering calculations with modern software engineering practices to deliver a professional decision-support platform for upstream oil and gas economic evaluation.