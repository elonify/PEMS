# MASTER_IMPLEMENTATION_DIRECTIVE.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Highest software-implementation authority  
**Supersedes:** All pre-v2.1 architecture and governance instructions  

---

## 1. Purpose

This directive is the highest software-implementation authority for PEMS.

It defines:

- documentation authority hierarchy
- non-negotiable engineering principles
- implementation constraints for humans and AI coding agents
- the relationship between the Excel Golden Master and the software

It does **not** replace the Excel Golden Master as the source of validated business calculation behaviour.

---

## 2. Documentation Baseline

The active documentation suite is:

**PEMS Documentation Baseline v2.1**

Version 2.1 supersedes Version 2.0 and all earlier EEM-era documentation.

Active documents live only under:

- `README.md` (repository root)
- `docs/00_GOVERNANCE/`
- `docs/01_ARCHITECTURE/`
- `docs/02_SPECIFICATIONS/`
- `docs/03_IMPLEMENTATION/`
- `docs/04_QUALITY/`
- `docs/05_PROJECT_CONTROL/`

Archived material under `docs/archive/` is **legacy** and has no authority.

---

## 3. Authority Hierarchy

No lower-level document may silently override a higher-level document.

| Rank | Authority | Scope |
|------|-----------|--------|
| 1 | **Excel Golden Master** | Validated business calculation behaviour and expected numeric results |
| 2 | **MASTER_IMPLEMENTATION_DIRECTIVE.md** | Software implementation authority, principles, constraints |
| 3 | **ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md** | System architecture and implementation structure |
| 4 | **Technical specifications** (`docs/02_SPECIFICATIONS/`, design docs in `01_ARCHITECTURE/`, quality docs in `04_QUALITY/`) | Detailed requirements |
| 5 | **Module specifications** (created from template when implementing) | Module-level detail |
| 6 | **Tests and validation results** | Evidence of conformity |

### Supporting process documents

- `CODING_AGENT_WORKFLOW.md` / `AI_AGENT_BOOTSTRAP.md` — process SOPs (must not contradict this directive)
- `IMPLEMENTATION_SEQUENCE.md` / `IMPLEMENTATION_TRACKER.md` — schedule and status (not business truth)
- `ARCHITECTURAL_DECISIONS.md` — recorded technology and design choices

### Agent adapter files

Root-level agent files (e.g. `CLAUDE.md`) are **adapters only**. They must point to this hierarchy and must not invent competing architecture.

---

## 4. Non-Negotiable Principles

1. **Excel is the business specification** for calculations and expected results.  
2. **Architecture governs software structure** — the workbook does not dictate UI or package layout.  
3. **Validation before completion** — implemented, tested, Excel-validated, documented.  
4. **Modularity** — single responsibility; clean interfaces.  
5. **Business objects, not worksheets** — charts, reports, dashboards, and APIs consume domain objects.  
6. **Deterministic calculations** — identical inputs → identical outputs.  
7. **Correctness over performance** — never sacrifice fidelity for speed.  
8. **Traceability** — every calculation traces workbook → rule → code → test → validation.  
9. **No invented business logic** — ambiguous Excel behaviour must be escalated, not guessed.  
10. **PEMS naming only** in active docs and code packages — `EEM` / `EEM_Project` are legacy terms only.

---

## 5. Excel Golden Master Policy

- The Golden Master is **read-only** for implementers.  
- It is the authoritative source for validated business calculation behaviour.  
- Implementation chain:

```text
Excel workbook
→ worksheet
→ cell / formula / rule
→ business rule
→ domain model / service
→ application calculation
→ unit / integration test
→ Excel comparison
→ regression validation
```

- Workbook updates require: register version → diff → impact analysis → update mapping & specs → update validation datasets → implement → re-validate.  
- The application never becomes the source of truth for business calculations while a Golden Master is in force.

Physical placement: `docs/workbook/Econ_Model_PEMS.xlsx` (Excel Golden Master), with `docs/workbook/WORKBOOK_MANIFEST.md` (name, version, date, SHA256, approver). History under `docs/workbook/Workbook_History/`.  
Active identity and residual Excel errors: see `docs/workbook/semantic_mapping/WORKBOOK_ERROR_STATUS.md` (must match manifest SHA256).  

**Hidden worksheets:** ignore for input/literal classification and implementation readiness; **do not modify** them. Catalogue retains them for fidelity. See `docs/workbook/semantic_mapping/SCOPE_VISIBLE_SHEETS_ONLY.md`.

---

## 6. Implementation Constraints

### Must

- Follow `IMPLEMENTATION_SEQUENCE.md` unless the project owner approves a deviation.  
- Create a module specification from `MODULE_IMPLEMENTATION_TEMPLATE.md` before coding a module.  
- Pass unit, integration, regression, and workbook comparison gates.  
- Keep calculation code free of UI, chart, and report generation side effects.  
- Route all inputs (manual, Excel, CSV, paste, templates) through the same validation and domain layer.

### Must not

- Implement against an outdated workbook or architecture.  
- Duplicate validation logic for import vs manual entry.  
- Hard-code business rules that contradict the Golden Master.  
- Treat archived docs as authority.  
- Begin packaging/release without validation evidence.

---

## 7. Layer Separation (Mandatory)

| Concern | Responsibility |
|---------|----------------|
| Business logic / rules | Domain concepts and fiscal/economic rules from the workbook |
| Calculation engine | Deterministic computation only |
| Data / input layer | Acquisition, mapping, unit conversion, input validation |
| UI | Presentation and interaction only |
| Chart engine | Visualization from chart datasets; dynamic scaling & dual-axis zero alignment |
| Reporting | Presentation of validated results; no calculations |
| Validation | Comparison, tolerances, regression, audit trail |
| Infrastructure | Logging, DI, config loading, packaging, file I/O plumbing |

---

## 8. Definition of Ready (any module)

- Workbook analysed for the target sheet(s)  
- Architecture current  
- Module specification completed from template  
- Inputs, outputs, dependencies, formula groups documented  
- Validation strategy and datasets identified  
- Package / service placement known  

---

## 9. Definition of Done (any module)

- Code implemented under approved structure  
- Unit tests pass  
- Integration tests pass where applicable  
- Formula-level traceability recorded  
- Cell-level / module workbook validation pass  
- Regression suite pass  
- Documentation and tracker updated  
- Changelog updated for user-visible / architectural change  
- Ready for commit / merge  

---

## 10. Change Control Summary

All material changes follow:

```text
Requirement / workbook change
→ Architecture review
→ Spec update
→ Implementation
→ Validation
→ Documentation
→ Tracker / changelog
→ Release gate (if releasing)
```

Details: `GOVERNANCE.md` and `VALIDATION_FRAMEWORK.md`.

---

## 11. Ready for Implementation

Implementation of application modules may begin only when:

1. This directive and the 25 core v2.1 documents are in place.  
2. Technology decisions required for the current phase are recorded in `ARCHITECTURAL_DECISIONS.md` / `TECHNOLOGY_STACK.md` (or explicitly deferred with ADR).  
3. Golden Master is available or Phase 0 workbook intake is the first task.  
4. Agents bootstrap from `AI_AGENT_BOOTSTRAP.md`.

---

## 12. Final Statement

PEMS is an enterprise petroleum economics platform. It preserves Golden Master calculation fidelity while applying modern software architecture. Every implementation decision must remain traceable, validated, and subordinate to this directive and the Excel Golden Master.
