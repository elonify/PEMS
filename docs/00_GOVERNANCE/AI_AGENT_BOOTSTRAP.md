# AI_AGENT_BOOTSTRAP.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Mandatory first-read for all AI coding agents  

---

## 1. Purpose

Bootstrap instructions so every coding agent starts with the same authority model, constraints, and workflow.

Compatible agents include Claude Code, Codex, Cursor, Copilot, Gemini CLI, OpenHands, Grok Build, and others.

---

## 2. First Actions (Before Any Code)

1. Read `docs/00_GOVERNANCE/MASTER_IMPLEMENTATION_DIRECTIVE.md`.  
2. Read this file completely.  
3. Read `docs/00_GOVERNANCE/CODING_AGENT_WORKFLOW.md`.  
4. Confirm current phase from `docs/03_IMPLEMENTATION/IMPLEMENTATION_SEQUENCE.md` and `docs/05_PROJECT_CONTROL/IMPLEMENTATION_TRACKER.md`.  
5. Open the relevant architecture and specification documents for the assigned task.  
6. Do **not** treat `docs/archive/` as authority.  
7. Do **not** invent business rules from petroleum knowledge when the Golden Master is silent or ambiguous — escalate.

---

## 3. Authority Hierarchy (Agents)

1. Excel Golden Master  
2. MASTER_IMPLEMENTATION_DIRECTIVE.md  
3. ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md  
4. Technical specifications (architecture + `02_SPECIFICATIONS` + quality)  
5. Module specifications  
6. Tests / validation results  

Process SOPs (this file, CODING_AGENT_WORKFLOW) support implementation but cannot override 1–4.

Root `CLAUDE.md` (if present) is an **adapter** only.

---

## 4. Absolute Prohibitions

- Do not modify the Excel Golden Master.  
- Do not implement UI calculations that bypass the calculation engine.  
- Do not create separate validation paths for imported vs manual data.  
- Do not use package name `EEM_Project` — use `pems` (see DIRECTORY_STRUCTURE / TECHNOLOGY_STACK).  
- Do not use archived v2.0 / pre-v2.1 docs as requirements.  
- Do not skip workbook analysis, module specification, or validation for “speed”.  
- Do not assume missing workbook sheets or formulas — document gaps and stop for clarification.

---

## 5. Standard Module Workflow

```text
Receive task
→ Identify workbook version + worksheets
→ Analyse workbook (inputs, outputs, formulas, deps)
→ Review architecture placement
→ Fill MODULE_IMPLEMENTATION_TEMPLATE for the module
→ Implement under src/pems/...
→ Unit tests
→ Workbook / cell validation
→ Integration / regression as applicable
→ Update WORKBOOK_MAPPING, tracker, changelog if needed
→ Commit one logical change
```

No stage may be skipped.

---

## 6. Required Reading Map by Task Type

| Task type | Read first |
|-----------|------------|
| Any work | MASTER_IMPLEMENTATION_DIRECTIVE, this file, CODING_AGENT_WORKFLOW |
| Structure / packages | DIRECTORY_STRUCTURE, ARCHITECTURE_AND_IMPLEMENTATION_PLAN |
| Technology choice | TECHNOLOGY_STACK, ARCHITECTURAL_DECISIONS |
| Domain objects | DATA_MODEL, SYSTEM_DESIGN |
| Inputs / import | INPUT_SYSTEM_SPECIFICATION |
| Calculations | ARCHITECTURE plan, WORKBOOK_MAPPING, module template |
| Charts | CHART_SPECIFICATION (incl. dual-axis zero alignment) |
| Reports | REPORT_SPECIFICATION |
| UI | UI_ARCHITECTURE |
| Validation | VALIDATION_FRAMEWORK |
| Packaging | BUILD_AND_DEPLOYMENT |
| Sequence / status | IMPLEMENTATION_SEQUENCE, IMPLEMENTATION_TRACKER |

---

## 7. Coding Standards (Summary)

- Python with type hints  
- SOLID; composition over inheritance  
- Deterministic calculation modules  
- No GUI imports in calculation packages  
- Docstrings; meaningful exceptions; logging  
- One logical commit; conventional commit messages (`feat(scope): …`)  

Full detail: CODING_AGENT_WORKFLOW.md and TECHNOLOGY_STACK.md.

---

## 8. Validation Expectation

A module is **not** done when code “runs”. Done requires:

- unit tests  
- integration tests where applicable  
- regression tests where applicable  
- workbook comparison / cell-level checks  
- formula traceability  
- documentation and tracker updates  

---

## 9. Escalation

Request human clarification when:

- workbook behaviour is ambiguous or inconsistent  
- architecture conflicts appear  
- Golden Master is missing for a calculation task  
- technology choice is open (no ADR) and choice would bind the project  

---

## 10. Success Standard

Act as a software engineer preserving:

- workbook fidelity  
- architectural integrity  
- validation traceability  
- long-term maintainability  

Not as a code generator.
