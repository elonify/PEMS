# Phase 0 Implementation Scaffold

**Status:** **PREPARED**  
**Package version:** `0.0.0`  
**Package name:** `pems`  
**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  

---

## What Phase 0 includes

| Area | Location | Status |
|------|----------|--------|
| Package layout | `src/pems/` | Scaffold |
| CaseInput shell | `domain/case_input.py` | Structure only |
| Validation shell | `validation/case_input_validator.py` | Structural checks |
| GM path + SHA verify | `infrastructure/golden_master.py` | Read-only verify |
| Excel import stub | `infrastructure/excel_import.py` | Raises until mapped |
| Calc modules stubs | `calculations/modules/*` | `NotImplementedCalculationError` |
| Dependency order | `calculations/dependency_order.py` | Declared sequence |
| GTC compare stub | `gtc/compare.py` | Raises until outputs exist |
| Results DTO | `domain/results_dto.py` | Structure only |
| Audit log | `application/audit_log.py` | stdlib logging |
| Presentation policy | `presentation/` | **Deferred** after calc VALIDATED |
| UI | `ui/` | Placeholder |
| Tests | `tests/unit/test_phase0_scaffold.py` | Smoke only |
| Build | `pyproject.toml` | Python 3.12, openpyxl, PySide6, matplotlib |

---

## What Phase 0 explicitly does **not** include

- Invented economic formulas  
- Implemented Production/Costs/FLGT/CR/NCF/RESULTS engines  
- Claim of numerical VALIDATED  
- Full presentation/formatting UI  
- Modification of Golden Master  

---

## Commands

```text
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pytest
python -m pems
```

---

## Spec freeze

See `docs/03_IMPLEMENTATION/SPECIFICATION_FREEZE_AUDIT.md`.

Presentation specs remain authoritative under `docs/02_SPECIFICATIONS/presentation/` but are **not** implemented in Phase 0 beyond policy flags.
