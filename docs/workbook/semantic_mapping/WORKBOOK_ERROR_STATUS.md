# WORKBOOK ERROR STATUS — AUTHORITATIVE

**Last updated:** 2026-08-03  
**Active Golden Master:** `docs/workbook/Econ_Model_PEMS.xlsx`  
**Active SHA256:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Version label:** Confirmed-2026-08-03  
**GM modified by agents:** **No**

**Historical (not active):** SHA `F6A1992F…3006` — intake_2026-08-01 (39 sheets)

---

## Classification legend

| Class | Meaning |
|-------|---------|
| **GENUINE_WORKBOOK_ERROR** | Defective reference/calc unexpected for the model design |
| **EXPECTED_ACCEPTED_CONDITION** | Excel result is valid behaviour for the input series; preserved as Golden expected behaviour |
| **CLOSED** | Not present on active GM / resolved |

---

## CLOSED — genuine or historical issues

| Issue | Status on active GM |
|-------|---------------------|
| START `#REF!` | **CLOSED** — not present; do not re-open unless active file contains `#REF!` |
| CR Econ empty formula caches (60) | **CLOSED** — not present |
| Analysis string `#REF!` as error | **CLOSED** — not observed |
| Other unexpected error types (`#DIV/0!`, `#VALUE!`, `#N/A`, `#NAME?` as defects) | **CLOSED** — none open as defects |

---

## EXPECTED / ACCEPTED (not a workbook defect)

| ID | Location | Formula | Excel result | Classification |
|----|----------|---------|--------------|----------------|
| **EXP-001** | **`Project_NCF!AU14`** | `=IRR(AK5:AK49)` | **`#NUM!`** | **EXPECTED / ACCEPTED IRR NO-SIGN-CHANGE CONDITION** |

### EXP-001 — confirmed sign pattern of AK5:AK49 (active GM)

| Check | Result |
|-------|--------|
| Range | `Project_NCF!AK5:AK49` (45 cells) |
| Formula-view content | **All blank** (0 formulas, 0 literals) |
| Cached numeric values | **0** |
| Positive values | **0** |
| Negative values | **0** |
| Zero values | **0** |
| Qualifying sign change (positive and negative non-zero cash flows) | **None** |
| IRR solvable under standard Excel IRR rules for this series | **No** |
| Excel `IRR` result | **`#NUM!`** — consistent with no qualifying sign change / empty series |

**Contrast (same sheet, working IRR):**

| Cell | Formula | Series | Sign pattern (cached) | Result |
|------|---------|--------|------------------------|--------|
| AU12 | `=IRR(AF5:AF40)` | AF | pos **11**, neg **4**, zero **30** (AF5:AF49) | **0.3486…** numeric |
| AG58 | `=IRR(AF5:AF49)` | AF | sign change present | **0.3486…** numeric |
| AU14 | `=IRR(AK5:AK49)` | AK | **empty / no sign change** | **`#NUM!`** |

### Disposition (authorized)

| Decision | Status |
|----------|--------|
| **Not** a workbook defect | **Confirmed** |
| Excel formula modified | **No** |
| `#NUM!` preserved as Golden Master expected behaviour | **Yes** |
| PO/domain acceptance of no-sign-change IRR → `#NUM!` | **Yes** (this disposition) |
| Disposition code | **EXPECTED / ACCEPTED IRR NO-SIGN-CHANGE CONDITION** (maps to prior option **B** — accepted expected behaviour) |

### PEMS / validation rules (mandatory)

1. PEMS **must not manufacture** an IRR when the NCF series has **no qualifying sign change**.  
2. PEMS **must** match Excel: return an explicit **no-IRR / undefined IRR** outcome equivalent to Excel `#NUM!` for this condition (not a fabricated rate).  
3. GTC-001 treats `Project_NCF!AU14` expected result as **`#NUM!`** / no-IRR — **PASS** when PEMS reports the same condition.  
4. Distinguish from **GENUINE_WORKBOOK_ERROR** (e.g. unexpected `#REF!`).  

See: `VALIDATION_FRAMEWORK.md`, `GOLDEN_TEST_CASES.md`, `PROJECT_NCF_AU14_INVESTIGATION.md`.

---

## Analysis data-table formulas (not errors)

| Item | Value |
|------|------:|
| Count | **18** |
| Sheet | Analysis |
| Class | Excel **DataTableFormula** constructs |
| Artifact | `ANALYSIS_DATA_TABLE_FORMULAS.md` / `.csv` |

Not listed as OPEN defects. Do not invent replacement formulas.

---

## OPEN genuine workbook defects

**None** on active Golden Master after EXP-001 acceptance.

---

## Fidelity claim

Documenting EXP-001 does **not** prove formula-level implementation fidelity. Fidelity remains **UNCLAIMED** until PEMS calculations are implemented and compared to the Golden Master.
