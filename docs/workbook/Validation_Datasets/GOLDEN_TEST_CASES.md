# GOLDEN TEST CASES — ACTIVE BASELINE

**Status:** **ACTIVE**  
**GTC-001** from active Golden Master (confirmed snapshot)  
**SHA256 (ACTIVE):** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**PREVIOUS DOCUMENTED GM HASH — SUPERSEDED BY RE-FREEZE:** `87EF7439A8F19C52B5B948D379D1752B327144CCDBC36758A780A93EC71121FB`  
**Version label:** Confirmed-2026-08-03  

**Historical (STALE):** `Validation_Datasets/historical_intake_F6A1992F/` — SHA `F6A1992F…3006`

---

## GTC-001 — As-saved baseline (active)

| Field | Value |
|-------|--------|
| Manifest | `scenarios/GTC-001_manifest.json` |
| Formula expected outputs | `expected_outputs/formula_cached_results_all.csv` — **86,973** rows |
| Literals baseline | `expected_outputs/literal_values_all.csv` — **10,470** rows |
| KPI / intermediates | `expected_outputs/GTC-001_kpi_and_intermediates.csv` |
| Input/parameter cells | `scenarios/GTC-001_input_and_parameter_cells.csv` |

### Expected Excel error / no-IRR conditions (accepted)

| Sheet | Cell | Formula | Expected | Classification |
|-------|------|---------|----------|----------------|
| Project_NCF | **AU14** | `=IRR(AK5:AK49)` | **`#NUM!`** | **EXPECTED / ACCEPTED IRR NO-SIGN-CHANGE** |

**AK5:AK49 sign pattern (confirmed):** entirely blank — 0 positive, 0 negative, 0 zero; **no qualifying sign change**.

**GTC PASS for AU14:** PEMS reports **no defined IRR** (equivalent to Excel `#NUM!`).  
**GTC FAIL for AU14:** PEMS invents any numeric IRR.

Do **not** treat AU14 as a genuine workbook defect. See `semantic_mapping/WORKBOOK_ERROR_STATUS.md` EXP-001.

### Tolerance (numeric cells)

- Exact: integers, booleans, text  
- Float: abs ≤ 1e-9 or rel ≤ 1e-9 (binary representation only)  
- Accepted Excel error conditions: **exact match on condition** (no-IRR / `#NUM!`), not float tolerance  

---

## Fidelity

**Formula-level implementation fidelity: UNCLAIMED**
