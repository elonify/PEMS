# DIRECTORY_STRUCTURE.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Canonical repository layout  

---

## 1. Purpose

Single authoritative repository structure for PEMS. Supersedes conflicting trees in pre-v2.1 README / PEMS.md sketches / architecture package lists where they differ.

---

## 2. Top-Level Layout

```text
PEMS/
├── README.md
├── CLAUDE.md                          # optional agent adapter (not architecture SSOT)
├── pyproject.toml / requirements*     # when scaffolding exists
├── src/
│   └── pems/
│       ├── __init__.py
│       ├── api/
│       ├── application/
│       ├── calculations/
│       ├── charts/
│       ├── configuration/
│       ├── core/
│       ├── dashboard/
│       ├── domain/
│       ├── exports/
│       ├── fiscal/
│       ├── infrastructure/
│       ├── persistence/
│       ├── production/
│       ├── reporting/
│       ├── services/
│       ├── ui/
│       ├── validation/
│       └── utilities/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── regression/
│   └── validation/
├── docs/
│   ├── 00_GOVERNANCE/
│   ├── 01_ARCHITECTURE/
│   ├── 02_SPECIFICATIONS/
│   │   └── modules/                   # filled module specs (created when implementing)
│   ├── 03_IMPLEMENTATION/
│   ├── 04_QUALITY/
│   ├── 05_PROJECT_CONTROL/
│   ├── DOCUMENTATION_TRACEABILITY_MATRIX.md
│   ├── archive/                       # LEGACY only
│   ├── templates/                     # optional form templates
│   └── workbook/
│       ├── Econ_Model_PEMS.xlsx       # Excel Golden Master (read-only)
│       ├── WORKBOOK_MANIFEST.md
│       ├── Workbook_History/          # intake and prior GM snapshots
│       └── Validation_Datasets/
│           ├── scenarios/
│           ├── expected_outputs/
│           └── regression/
├── resources/                         # icons, static assets
├── config/                            # default configuration files
├── exports/                           # generated outputs (usually gitignored)
├── samples/                           # sample projects (non-secret)
└── installer/                         # packaging scripts and installer assets
```

---

## 3. Documentation Suite (active)

Exactly 25 core Markdown documents as listed in MASTER_IMPLEMENTATION_DIRECTIVE / baseline inventory:

| Path |
|------|
| `README.md` |
| `docs/00_GOVERNANCE/MASTER_IMPLEMENTATION_DIRECTIVE.md` |
| `docs/00_GOVERNANCE/AI_AGENT_BOOTSTRAP.md` |
| `docs/00_GOVERNANCE/CODING_AGENT_WORKFLOW.md` |
| `docs/00_GOVERNANCE/GOVERNANCE.md` |
| `docs/00_GOVERNANCE/ARCHITECTURAL_DECISIONS.md` |
| `docs/01_ARCHITECTURE/ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md` |
| `docs/01_ARCHITECTURE/SYSTEM_DESIGN.md` |
| `docs/01_ARCHITECTURE/TECHNOLOGY_STACK.md` |
| `docs/01_ARCHITECTURE/DIRECTORY_STRUCTURE.md` |
| `docs/01_ARCHITECTURE/PROJECT_ROADMAP.md` |
| `docs/02_SPECIFICATIONS/DATA_MODEL.md` |
| `docs/02_SPECIFICATIONS/INPUT_SYSTEM_SPECIFICATION.md` |
| `docs/02_SPECIFICATIONS/API_SPECIFICATION.md` |
| `docs/02_SPECIFICATIONS/UI_ARCHITECTURE.md` |
| `docs/02_SPECIFICATIONS/CONFIGURATION.md` |
| `docs/02_SPECIFICATIONS/CHART_SPECIFICATION.md` |
| `docs/02_SPECIFICATIONS/REPORT_SPECIFICATION.md` |
| `docs/02_SPECIFICATIONS/WORKBOOK_MAPPING_SPECIFICATION.md` |
| `docs/03_IMPLEMENTATION/IMPLEMENTATION_SEQUENCE.md` |
| `docs/03_IMPLEMENTATION/MODULE_IMPLEMENTATION_TEMPLATE.md` |
| `docs/04_QUALITY/VALIDATION_FRAMEWORK.md` |
| `docs/04_QUALITY/BUILD_AND_DEPLOYMENT.md` |
| `docs/05_PROJECT_CONTROL/IMPLEMENTATION_TRACKER.md` |
| `docs/05_PROJECT_CONTROL/CHANGELOG.md` |

Control artifact (not one of the 25): `docs/DOCUMENTATION_TRACEABILITY_MATRIX.md`.

---

## 4. Naming Rules

- Product: **PEMS**  
- Python package: **`pems`** (lowercase)  
- Do not create `EEM_Project`  
- Module specs: `docs/02_SPECIFICATIONS/modules/<module_name>.md`  

---

## 5. What Must Not Live in Active Authority Paths

- Hash-prefixed legacy filenames  
- Duplicate trackers at repo root  
- Competing architecture plans outside `docs/01_ARCHITECTURE/`  

Legacy copies: `docs/archive/legacy_pre_v2.1/` only.

---

## 6. Validation Dataset Paths

Canonical validation datasets: `docs/workbook/Validation_Datasets/`.

Automated tests may mirror fixtures under `tests/validation/` that reference or copy approved expected outputs — process owned by VALIDATION_FRAMEWORK.

---

## 7. Evolution

Structural changes require update to this document and ADR if significant.
