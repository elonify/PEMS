# Project_NCF!AU14 — Investigation & Disposition

**Active GM SHA256:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Disposition date:** 2026-08-03  
**Classification:** **EXPECTED / ACCEPTED IRR NO-SIGN-CHANGE CONDITION**  
**Not a workbook defect.** Excel formula **not** modified.

---

## Cell

| Field | Value |
|-------|--------|
| Address | `Project_NCF!AU14` |
| Formula | `=IRR(AK5:AK49)` |
| Excel result | `#NUM!` |
| Golden expected behaviour | **`#NUM!` / no defined IRR** |

---

## Confirmed sign pattern — AK5:AK49

| Metric | Count |
|--------|------:|
| Cells in range | 45 (AK5:AK49) |
| Non-blank formula-view cells | **0** |
| Cached positive values | **0** |
| Cached negative values | **0** |
| Cached zero values | **0** |
| Cached empty (`None`) | **45** |
| Qualifying sign change | **None** |

**Pattern summary:** The IRR input series is **entirely blank** on the active Golden Master. There is **no** sequence of mixed-sign net cash flows. Under standard Excel `IRR` rules, **`#NUM!` is expected**.

---

## Corroboration (same economic sheet)

| Cell | Formula | Series sign pattern | Result |
|------|---------|---------------------|--------|
| AU12 | `=IRR(AF5:AF40)` | AF: + and − present | Numeric ~**34.86%** |
| AG58 | `=IRR(AF5:AF49)` | AF: + and − present | Numeric ~**34.86%** |
| AU14 | `=IRR(AK5:AK49)` | AK: empty / no sign change | **`#NUM!`** |

---

## Disposition

| Item | Decision |
|------|----------|
| Workbook defect? | **No** |
| Modify Excel? | **No** |
| Accept `#NUM!` as Golden expected? | **Yes** |
| Prior option mapping | **B** — PO/domain accepts expected behaviour |
| Invent numeric IRR in PEMS? | **Forbidden** |

---

## PEMS implementation requirement

When the NCF series for IRR has no qualifying sign change (including all-empty, all-non-negative, or all-non-positive non-zero patterns as defined in VALIDATION_FRAMEWORK / calculation specs):

- Return **no IRR** / error condition aligned with Excel `#NUM!`  
- **Do not** invent or force a rate  

---

## Fidelity

Documenting this condition does **not** prove formula-level fidelity.
