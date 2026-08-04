# Elonify Petroleum Economics Modeling System (PEMS)

**Documentation Baseline:** v2.1  
**Status:** Spec freeze complete; Phase 0 scaffold prepared; calculation engines not implemented; numerical VALIDATED not claimed  
**Architecture:** Enterprise desktop application  
**Language:** Python  
**Primary Platform:** Windows desktop (cross-platform ready)  
**Package name:** `pems`

---

## Overview

PEMS is an enterprise-grade petroleum economics application developed from a validated Microsoft Excel model (the **Excel Golden Master**).

The objective is to preserve business integrity and calculation fidelity of the Excel workbook while delivering a maintainable, scalable desktop application.

---

## Guiding Principles

- The Excel workbook is the validated business specification for calculations and expected results.  
- The Python application is the software implementation.  
- Business logic is independent of the user interface.  
- Every calculation module is validated against the workbook.  
- Architecture governs implementation.  
- Correctness takes precedence over optimisation.  

## Phase 0

```text
pip install -e ".[dev]"
pytest
python -m pems
```

See `docs/03_IMPLEMENTATION/PHASE_0_SCAFFOLD.md` and `SPECIFICATION_FREEZE_AUDIT.md`.  
Presentation specs under `docs/02_SPECIFICATIONS/presentation/` are authoritative but UI formatting is deferred until after calc GTC validation.  

---

## Documentation Baseline v2.1

Authoritative documentation lives under `docs/`:

| Area | Path |
|------|------|
| Governance | `docs/00_GOVERNANCE/` |
| Architecture | `docs/01_ARCHITECTURE/` |
| Specifications | `docs/02_SPECIFICATIONS/` |
| Implementation control | `docs/03_IMPLEMENTATION/` |
| Quality | `docs/04_QUALITY/` |
| Project control | `docs/05_PROJECT_CONTROL/` |

**Start here for humans:** `docs/00_GOVERNANCE/MASTER_IMPLEMENTATION_DIRECTIVE.md`  
**Start here for AI agents:** `docs/00_GOVERNANCE/AI_AGENT_BOOTSTRAP.md`

Control artifact: `docs/DOCUMENTATION_TRACEABILITY_MATRIX.md`  
Legacy materials: `docs/archive/` (**not authoritative**)

---

## Authority Hierarchy

1. Excel Golden Master  
2. MASTER_IMPLEMENTATION_DIRECTIVE.md  
3. ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md  
4. Technical specifications  
5. Module specifications  
6. Tests and validation results  

---

## Repository Structure (target)

See `docs/01_ARCHITECTURE/DIRECTORY_STRUCTURE.md` for the full tree (`src/pems`, `tests`, `docs`, `config`, `installer`, workbook assets, etc.).

---

## Development Workflow

```text
Workbook → Analysis → Architecture → Module Spec → Implementation
→ Unit Tests → Excel Validation → Docs/Tracker → Commit
```

Detailed SOP: `docs/00_GOVERNANCE/CODING_AGENT_WORKFLOW.md`  
Sequence: `docs/03_IMPLEMENTATION/IMPLEMENTATION_SEQUENCE.md`

---

## Validation

Six-level validation including formula, cell, module, integration, and regression testing.  
See `docs/04_QUALITY/VALIDATION_FRAMEWORK.md`.

---

## Input System

Manual entry **and** import (Excel, CSV, copy/paste, templates) share one validation and domain path.  
See `docs/02_SPECIFICATIONS/INPUT_SYSTEM_SPECIFICATION.md`.

---

## Charts

Dynamic scaling and **primary/secondary Y-axis zero alignment** are mandatory.  
See `docs/02_SPECIFICATIONS/CHART_SPECIFICATION.md`.

---

## Current Status

| Item | Status |
|------|--------|
| Documentation Baseline v2.1 | Complete |
| Application source | Not started |
| Golden Master | `docs/workbook/Econ_Model_PEMS.xlsx` |
| Active SHA256 | `87EF7439…21FB` (Confirmed-2026-08-03, 38 sheets) |
| Historical intake SHA | `F6A1992F…3006` (39 sheets) — archive only |
| Genuine Excel defects (active) | **None open** |
| Expected Excel condition | `Project_NCF!AU14` `#NUM!` = **accepted no-sign-change IRR** (AK blank) |
| Closed | START `#REF!`, CR Econ empty caches |
| Formula / cell catalogue | **ACTIVE** — `docs/workbook/catalogue/` |
| GTC-001 | **ACTIVE** — `docs/workbook/Validation_Datasets/` |
| Hidden sheets | **Ignored** for input classification/readiness; not modified |
| Literals in scope | ~3,827 on **visible** sheets (~6,644 hidden ignored) |
| Formula-level fidelity | **Not claimable** |
| Open tech ADRs | GUI, charts, persistence, Excel I/O |
| Formal PO GM stamp | Open |

Progress: `docs/05_PROJECT_CONTROL/IMPLEMENTATION_TRACKER.md`

---

## Contributing

Follow governance and coding agent workflow. Preserve workbook fidelity; include tests and validation; update documentation.

---

## License

Proprietary until the Project Owner defines licensing terms.

---

## Contact

**Project Owner:** Dr. Emmanuel Onwuka
