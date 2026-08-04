# GOLDEN_MASTER_INTAKE_AND_RECONCILIATION_UPDATE.md

**Last updated:** 2026-08-03  
**Phase:** Active baseline re-extract + AU14 investigation  

---

## Active vs historical identity

| | **Active** | Historical only |
|--|------------|-----------------|
| Label | Confirmed-2026-08-03 | Intake-2026-08-01 |
| SHA256 | **`D07560CA…BFEA`** | `F6A1992F…3006` |
| Snapshot | `…confirmed_2026-08-03.xlsx` | `…intake_2026-08-01.xlsx` |
| Sheets | **38** | 39 |
| Catalogue/GTC | **ACTIVE re-extract** | STALE archive |

**GM modified by agents:** **No**

---

## Re-extract status (action 1) — COMPLETE

| Item | Result |
|------|--------|
| Formula/cell catalogue | **Re-extracted** to `docs/workbook/catalogue/` with active SHA on every row |
| GTC-001 | **Rebuilt** under `Validation_Datasets/` with active SHA |
| Historical artefacts | Preserved under `*/historical_intake_F6A1992F/` — not deleted |
| Worksheets | 38 verified |
| Formulas | 86,973 (all with cache) |
| Non-empty cells | 109,158 |
| Formula expected outputs | 86,973 |
| Diff vs historical formulas | +1,714 added / −2,232 removed / 401 changed |
| Sheets added | Project_NCF |
| Sheets removed | Project_NCF_Con (2), Sheet1 |

---

## Project_NCF!AU14 — DISPOSITION UPDATED

| Item | Result |
|------|--------|
| Formula / cache | `=IRR(AK5:AK49)` → `#NUM!` |
| AK5:AK49 sign pattern | **Entirely blank** (pos=0, neg=0, zero=0, empty=45) — **no qualifying sign change** |
| Corroborating IRR | AU12 / AG58 on AF series → ~0.3486 (sign change present) |
| Classification | **EXPECTED / ACCEPTED IRR NO-SIGN-CHANGE CONDITION** |
| Workbook defect? | **No** |
| Excel modified? | **No** |
| Golden expected | Preserve **`#NUM!` / no-IRR** |
| PEMS | Must not invent IRR; match no-IRR condition |

Authoritative: `semantic_mapping/WORKBOOK_ERROR_STATUS.md` EXP-001

---

## Error / condition board

| Issue | Status |
|-------|--------|
| START `#REF!` | **CLOSED** |
| CR Econ empty caches | **CLOSED** |
| `Project_NCF!AU14` `#NUM!` | **EXPECTED / ACCEPTED** (not a defect) |
| Analysis 18 data tables | **Not errors** — constructs documented |
| Open genuine defects | **None** |

---

## Gap board

| Gap | Status |
|-----|--------|
| Active catalogue/GTC for D07560CA… | **CLOSED** |
| AU14 disposition | **CLOSED** as expected no-sign-change |
| Literal classification | **OPEN** — **visible sheets only (~3,827)**; hidden (~6,644) **ignored** |
| Hidden sheets | **Out of scope** for input/readiness; not modified |
| Full dependency proven | OPEN |
| PO stamp / ADRs | OPEN |
| Formula-level fidelity | **UNCLAIMED** (documenting AU14 ≠ fidelity proven) |

---

## Next

- Continue semantic mapping on **active** catalogue  
- Implement IRR no-sign-change contract when economics module is built  
- Do not claim formula-level parity until PEMS vs GM comparison passes  
