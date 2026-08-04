# ARCHITECTURAL_DECISIONS.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Decision log (living)  

---

## 1. Purpose

Record significant architectural and technology decisions (ADRs) and their consequences.

Template for new decisions is included below. Accepted decisions must stay consistent with TECHNOLOGY_STACK.md, SYSTEM_DESIGN.md, UI_ARCHITECTURE.md, CHART_SPECIFICATION.md, and BUILD_AND_DEPLOYMENT.md.

---

## 2. Decision Log Index

| ID | Title | Status | Date |
|----|-------|--------|------|
| ADR-0001 | Product identity and package naming (PEMS) | Accepted | 2026-08-01 |
| ADR-0002 | Excel Golden Master as calculation authority | Accepted | 2026-08-01 |
| ADR-0003 | Layered desktop architecture | Accepted | 2026-08-01 |
| ADR-0004 | Documentation Baseline v2.1 structure | Accepted | 2026-08-01 |
| ADR-0005 | Language and runtime baseline (Python) | Accepted | 2026-08-01 |
| ADR-0006 | Packaging approach (PyInstaller-class desktop bundle) | Accepted | 2026-08-01 |
| ADR-0007 | GUI framework selection | **Accepted** | 2026-08-03 |
| ADR-0008 | Chart library selection | **Accepted** | 2026-08-03 |
| ADR-0009 | Project file persistence format | **Accepted** | 2026-08-03 |
| ADR-0010 | Excel I/O library for import and validation | **Accepted** | 2026-08-03 |
| ADR-0011 | Python version pin (3.12) | **Accepted** | 2026-08-03 |
| ADR-0012 | Test framework (pytest) | **Accepted** | 2026-08-03 |
| ADR-0013 | Logging (stdlib logging) | **Accepted** | 2026-08-03 |
| ADR-0014 | Dependency management (pip + lock/requirements) | **Accepted** | 2026-08-03 |

Open UI/chart *implementation* may begin only in their sequence phases; decisions above close pre-implementation architecture gates.

---

## 3. Accepted Decisions

### ADR-0001 — Product identity and package naming (PEMS)

**Status:** Accepted  

**Context:** Pre-v2.1 materials used `EEM_Project` and mixed EEM/PEMS naming.  

**Decision:** Product name is **Elonify Petroleum Economics Modeling System (PEMS)**. Python package root is **`pems`**. Legacy term EEM may appear only in archive notes or migration history.  

**Consequences:** All active docs and new code use PEMS/`pems`.  

---

### ADR-0002 — Excel Golden Master as calculation authority

**Status:** Accepted  

**Context:** Application must reproduce validated petroleum economics calculations.  

**Decision:** Approved Excel workbook is the Golden Master for business calculation behaviour and expected results. Software implements; software does not redefine those rules without a workbook change process.  

**Consequences:** Cell-level comparison, formula traceability, regression against Golden Test Cases are mandatory.  

---

### ADR-0003 — Layered desktop architecture

**Status:** Accepted  

**Context:** Need maintainability, testability, and separation of UI from calculations.  

**Decision:** Layered architecture: Presentation → Application → Business Services → Calculation Engine → Domain → Persistence/Infrastructure. Validation is a cross-cutting quality concern with a dedicated validation subsystem for Excel comparison. Charts and reports consume domain-derived datasets only.  

**Consequences:** No calculation logic in UI; no UI imports in calculation packages.  

---

### ADR-0004 — Documentation Baseline v2.1 structure

**Status:** Accepted  

**Context:** Competing flat v2.0 layouts and hash-prefixed filenames caused authority conflicts.  

**Decision:** Single suite under `docs/00_GOVERNANCE` … `docs/05_PROJECT_CONTROL` plus root README; 25 core documents; archive for legacy.  

**Consequences:** Pre-v2.1 docs archived; agents bootstrap from v2.1 only.  

---

### ADR-0005 — Language and runtime baseline (Python)

**Status:** Accepted  

**Context:** All pre-v2.1 and v2.1 materials specify Python.  

**Decision:** Implementation language is **Python** (project-approved CPython version to be pinned in TECHNOLOGY_STACK / environment files when scaffolding). Type hints required; dataclasses or Pydantic allowed for structured models.  

**Consequences:** Stack choices must be Python-ecosystem compatible.  

---

### ADR-0006 — Packaging approach

**Status:** Accepted (direction)  

**Context:** IMPLEMENTATION_SEQUENCE and roadmap require Windows installer / portable executable.  

**Decision:** Desktop packaging uses a **PyInstaller-class** freeze/bundle approach (or equivalent approved later), with installer and portable variants as described in BUILD_AND_DEPLOYMENT.  

**Consequences:** Avoid runtime designs that cannot be frozen without Project Owner approval.  

---

## 4. Decisions closed for pre-implementation (2026-08-03)

### ADR-0007 — GUI framework

**Status:** Accepted  

**Decision:** **PySide6** (Qt for Python) for the desktop presentation layer.  

**Alternatives:** PyQt6 (licensing); Tk/customtkinter (weaker enterprise desktop); Streamlit (not selected — v2.1 architecture is **desktop application**, not web-first).  

**Rationale:** Matches desktop target, solid widgets/forms, free LGPL-friendly packaging path with care; business logic remains GUI-free.  

**Consequences:** UI package may import PySide6; `pems.calculations` / domain must not.

---

### ADR-0008 — Chart library

**Status:** Accepted  

**Decision:** **matplotlib** as the primary chart engine for PEMS, including dual-axis **zero-alignment** algorithm (CHART_SPECIFICATION). Export PNG/SVG via matplotlib.  

**Alternatives:** Plotly (interactive-first; deferred as optional later enhancement, not dual-stack default).  

**Rationale:** Deterministic axis limit control for zero alignment; freezes cleanly with PyInstaller; consistent with scientific Python stack.  

**Consequences:** Chart engine implements range policy in PEMS code, not Excel.

---

### ADR-0009 — Project file persistence format

**Status:** Accepted  

**Decision:** **JSON** project documents (versioned schema) for project/scenario persistence. Optional SQLite later via new ADR only.  

**Rationale:** Transparent, diff-friendly, sufficient for desktop single-user v1; no server required.  

---

### ADR-0010 — Excel I/O library and comparison mechanism

**Status:** Accepted  

**Decision:** **openpyxl** for all PEMS Excel read paths (import, catalogue-style extract, GTC comparison). Excel is **not** the runtime calculation engine.

#### Comparison mechanism (normative)

| Concern | Specification |
|---------|----------------|
| How workbook data is read | `openpyxl.load_workbook(path, data_only=False)` for formulas; second load `data_only=True` for cached values |
| Formulas vs cached values | Formula text from formula workbook; **expected numeric/text results** from value cache unless cell is an **accepted error condition** |
| Expected outputs extraction | GTC CSVs generated from active GM SHA; re-extract on GM change |
| PEMS vs expected compare | Cell-keyed map: `(sheet, coord) → expected`; PEMS emits same keys for implemented set |
| Excel errors representation | Store Excel error strings (e.g. `#NUM!`) as expected **condition**; PEMS emits semantic enum + optional Excel-compatible token |
| Expected `#NUM!` (AU14) | Map to PEMS `NO_VALID_IRR` / `NO_SIGN_CHANGE`; **PASS** on condition match; **FAIL** if numeric IRR invented |
| Tolerances | VALIDATION_FRAMEWORK: exact int/bool/text; float abs/rel 1e-9 unless config tightens |
| Reports | JSON/Markdown validation report: SHA, PEMS version, pass/fail counts, max diff, error-condition results |

**Alternatives:** xlwings/Excel COM (rejected for headless CI reproducibility); pandas-only (insufficient formula access).

---

### ADR-0011 — Python version pin

**Status:** Accepted  

**Decision:** **CPython 3.12.x** for development and packaging targets.  

---

### ADR-0012 — Test framework

**Status:** Accepted  

**Decision:** **pytest** (+ coverage plugin optional). Unit / integration / validation tests under `tests/`.  

---

### ADR-0013 — Logging

**Status:** Accepted  

**Decision:** Python **stdlib `logging`**.  

---

### ADR-0014 — Dependency management

**Status:** Accepted  

**Decision:** **pip** with `pyproject.toml` and locked/pinned requirements for reproducible installs. CI runs pytest on lockfile install.  

**Packaging:** remains ADR-0006 PyInstaller-class.  

---

## 5. ADR Template (for new entries)

```markdown
### ADR-XXXX — Title

Status: Proposed | Accepted | Superseded | Deprecated

Date:

Context:
Decision:
Alternatives considered:
Rationale:
Consequences:
Related documents:
```

---

## 6. Supersession

When a decision is superseded, mark Status = Superseded, link the replacement ADR, and update TECHNOLOGY_STACK.md the same day.
