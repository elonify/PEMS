# WORKBOOK_MANIFEST.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Last updated:** 2026-08-03 (formal GM approval CLOSED)  

---

## Active Golden Master

| Attribute | Value |
|-----------|--------|
| File name | **Econ_Model_PEMS_confirmed_2026-08-03.xlsx** |
| Relative path | `docs/workbook/Workbook_History/Econ_Model_PEMS_confirmed_2026-08-03.xlsx` |
| Live working copy (not GM) | `docs/workbook/Econ_Model_PEMS.xlsx` |
| Version label | **Confirmed-2026-08-03** |
| **SHA256 (ACTIVE)** | **`D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`** |
| File size (bytes) | **4841231** |
| Worksheets | **38** |
| Freeze record | `docs/workbook/GM_FREEZE_RECORD.md` |
| Catalogue / GTC baseline | **ACTIVE** against this SHA (re-extracted 2026-08-03) |
| Formal PO approval | **CLOSED** — approved by **Dr Emmanuel Ifeanyichukwu Onwuka** (Project Owner), 3 August 2026 WAT (`GOLDEN_MASTER_APPROVAL.md`) |
| Policy | **READ-ONLY** after approval; any binary change → new SHA + new approval cycle |

### PREVIOUS DOCUMENTED GM HASH — SUPERSEDED BY RE-FREEZE

| Attribute | Value |
|-----------|--------|
| SHA256 | **`87EF7439A8F19C52B5B948D379D1752B327144CCDBC36758A780A93EC71121FB`** |
| Status | **SUPERSEDED BY RE-FREEZE** (retain historically; do not restore unless instructed) |

### Live working copy (implementation path)

| Attribute | Value |
|-----------|--------|
| Path | `docs/workbook/Econ_Model_PEMS.xlsx` |
| SHA256 (current) | `FFADB639A0EA2FD3D1981BE11FC495D013875193F30CEEA0454CDA27827C7F0F` |
| Role | Working copy — calc/semantic-equivalent to active GM; **not** byte-identical; **not** the frozen GM identity |
| Path integrity | **CLOSED — NON-SUBSTANTIVE CURRENT-WORKBOOK DIFFERENCE** |

### Expected Excel condition (not a defect)

| Cell | Result | Classification |
|------|--------|----------------|
| `Project_NCF!AU14` `=IRR(AK5:AK49)` | `#NUM!` | **EXPECTED / ACCEPTED IRR NO-SIGN-CHANGE** (AK5:AK49 blank; no sign change) |

See `docs/workbook/semantic_mapping/WORKBOOK_ERROR_STATUS.md` EXP-001. PEMS must not invent IRR for this case.

---

## Historical Golden Master (not active)

| Attribute | Value |
|-----------|--------|
| Snapshot | `Workbook_History/Econ_Model_PEMS_intake_2026-08-01.xlsx` |
| SHA256 | `F6A1992F6A3CC27EC587779ADE6CF667B246FB1587296EFD0CD14B47A6783006` |
| Worksheets | 39 |
| Catalogue/GTC | `catalogue/historical_intake_F6A1992F/`, `Validation_Datasets/historical_intake_F6A1992F/` — **STALE** |

---

## Validation datasets (active)

| Artifact | Path | SHA binding |
|----------|------|-------------|
| Formula expected | `Validation_Datasets/expected_outputs/formula_cached_results_all.csv` | **ACTIVE** `D07560CA…` |
| Literals | `…/literal_values_all.csv` | **ACTIVE** |
| KPI pack | `…/GTC-001_kpi_and_intermediates.csv` | **ACTIVE** |
| Inputs | `…/scenarios/GTC-001_input_and_parameter_cells.csv` | **ACTIVE** |
| Manifest | `…/scenarios/GTC-001_manifest.json` | **ACTIVE** |
| Catalogue | `docs/workbook/catalogue/` | **ACTIVE** |

---

## Access rules

1. Do not edit Golden Master to make tests pass.  
2. On workbook change: new SHA → history → re-extract catalogue/GTC → update this manifest.  
3. Active identity is the **confirmed snapshot** hash above — not the live path unless formally re-promoted.  
