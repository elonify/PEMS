# CLAUDE.md — Agent Adapter

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Agent configuration adapter only — **not** architectural authority  

---

## Authority

This file does **not** define architecture or business rules.

Follow this hierarchy:

1. Excel Golden Master (business calculations / expected results)  
2. `docs/00_GOVERNANCE/MASTER_IMPLEMENTATION_DIRECTIVE.md`  
3. `docs/01_ARCHITECTURE/ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md`  
4. Technical specifications under `docs/01_ARCHITECTURE/`, `docs/02_SPECIFICATIONS/`, `docs/04_QUALITY/`  
5. Module specifications (`docs/02_SPECIFICATIONS/modules/`)  
6. Tests and validation results  

**Mandatory bootstrap:** `docs/00_GOVERNANCE/AI_AGENT_BOOTSTRAP.md`  
**Mandatory workflow:** `docs/00_GOVERNANCE/CODING_AGENT_WORKFLOW.md`

Do **not** use `docs/archive/` as requirements.

---

## Non-Negotiables

- Do not modify the Excel Golden Master.  
- Do not invent business logic; escalate ambiguity.  
- Package name is **`pems`**, not `EEM_Project`.  
- All inputs (manual and import) share one validation path.  
- Calculations stay free of UI/chart/report side effects.  
- Dual-axis charts: align zeros per `docs/02_SPECIFICATIONS/CHART_SPECIFICATION.md`.  
- Module not done until unit, integration (as applicable), regression (as applicable), and workbook validation pass.  

---

## Quick Commands for Agents

| Intent | Document |
|--------|----------|
| Start any task | AI_AGENT_BOOTSTRAP + MASTER_IMPLEMENTATION_DIRECTIVE |
| Sequence | `docs/03_IMPLEMENTATION/IMPLEMENTATION_SEQUENCE.md` |
| Status | `docs/05_PROJECT_CONTROL/IMPLEMENTATION_TRACKER.md` |
| Module template | `docs/03_IMPLEMENTATION/MODULE_IMPLEMENTATION_TEMPLATE.md` |
| Validation | `docs/04_QUALITY/VALIDATION_FRAMEWORK.md` |
| Stack | `docs/01_ARCHITECTURE/TECHNOLOGY_STACK.md` |
| ADRs | `docs/00_GOVERNANCE/ARCHITECTURAL_DECISIONS.md` |

---

## Coding Defaults

- Python, type hints, SOLID, deterministic calculations  
- Conventional commits: `type(scope): summary`  
- Update tracker and mapping when modules complete  

If this adapter conflicts with Baseline v2.1 documents, **v2.1 documents win**.
