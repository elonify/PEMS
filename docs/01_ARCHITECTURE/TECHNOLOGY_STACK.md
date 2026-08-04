# TECHNOLOGY_STACK.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Technology baseline — aligned to ADRs as of 2026-08-03  

---

## 1. Purpose

Approved technology baseline. Only decisions recorded here and in ARCHITECTURAL_DECISIONS.md may be used in implementation.

---

## 2. Confirmed stack

| Layer | Choice | ADR / source |
|-------|--------|----------------|
| Language | **Python CPython 3.12.x** | ADR-0005, ADR-0011 |
| Package | **`pems`** | ADR-0001 |
| App type | Desktop (Windows primary) | Architecture |
| GUI | **PySide6** | ADR-0007 |
| Charts | **matplotlib** (+ PEMS zero-align) | ADR-0008 |
| Persistence | **JSON** project files | ADR-0009 |
| Excel I/O | **openpyxl** (read/import/compare only) | ADR-0010 |
| Calculations | Pure Python; NumPy/pandas only if later ADR | Domain purity |
| Typing | Type hints; dataclasses and/or Pydantic | ADR-0005 |
| Tests | **pytest** | ADR-0012 |
| Logging | **stdlib logging** | ADR-0013 |
| Dependencies | **pip** + `pyproject.toml` / pinned requirements | ADR-0014 |
| Packaging | **PyInstaller-class** | ADR-0006 |
| Validation | Golden Master compare via openpyxl + GTC | ADR-0002, ADR-0010 |
| VCS | Git | Practice |
| Versioning | SemVer | CHANGELOG |

---

## 3. Layer constraints

| Layer | Allowed | Forbidden |
|-------|---------|-----------|
| Domain / calculations | Pure Python (+ approved numeric libs) | GUI, matplotlib, openpyxl in calc core |
| Validation tooling | openpyxl | Excel as runtime calc engine |
| UI | PySide6 | Business formulas |
| Charts | matplotlib | VBA |
| Packaging | PyInstaller-class | Undocumented packagers |

---

## 4. Environment (Phase 0)

- Python 3.12 venv  
- `pip install -e .` / requirements  
- `pytest`  
- No economic modules in Phase 0  

---

## 5. Consistency

Must match SYSTEM_DESIGN, UI_ARCHITECTURE, CHART_SPECIFICATION, BUILD_AND_DEPLOYMENT, ARCHITECTURAL_DECISIONS.
