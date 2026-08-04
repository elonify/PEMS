# GTC Comparison Framework (Pre-Implementation Complete Spec)

**Baseline case:** GTC-001  
**Authoritative GM identity SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Library:** openpyxl (ADR-0010)  
**Status:** Framework **specified** — execution deferred until PEMS modules implemented  

**Implementation readiness ≠ VALIDATED parity.**

---

## 1. Comparison inputs

| Input | Source |
|-------|--------|
| Expected formula results | `Validation_Datasets/expected_outputs/formula_cached_results_all.csv` |
| Expected literals | `…/literal_values_all.csv` |
| KPI pack | `…/GTC-001_kpi_and_intermediates.csv` |
| Case inputs | `…/scenarios/GTC-001_input_and_parameter_cells.csv` |
| Equity share INPUT | Equity Dash C4 = 0.49 |
| Fiscal law tables | Fiscal Terms_PIA (LAW TABLE, not inputs) |
| GM SHA | Must match confirmed identity before run |

---

## 2. Expected outputs

- Cell-keyed: `(worksheet, cell) → expected_value, formula, use_as_numeric_golden`  
- Implemented PEMS modules emit the same keys for their scope  

---

## 3. Excel error semantics

| Excel | PEMS semantic | Compare |
|-------|---------------|---------|
| `#NUM!` IRR no sign change (AU14) | `NO_VALID_IRR` / `NO_SIGN_CHANGE` | Condition match |
| Other Excel errors | Preserve string / enum | Exact unless reclassified |
| Numeric | float | Tolerance below |

---

## 4. Tolerances

| Type | Rule |
|------|------|
| int, bool, text | Exact |
| float | abs ≤ 1e-9 **or** rel ≤ 1e-9 |
| Accepted error conditions | Exact semantic match |

---

## 5. Cell/range mapping

- Primary: exact cell addresses from GTC CSVs  
- Module specs list comparison cells for each READY module  
- Do not invent ranges  

---

## 6. Test execution method

```text
1. Verify GM path hash == confirmed SHA (fail if not)
2. Load GTC expected set for module scope
3. Load PEMS inputs (incl. equity share INPUT)
4. Load fiscal LAW TABLE from approved package
5. Run PEMS module under test
6. Compare outputs to expected
7. Write validation report
```

Tooling: **pytest** + `pems.validation` harness (Phase 0 skeleton later).

---

## 7. Report format

JSON/Markdown: timestamp, GM SHA, PEMS version, module, cells compared, passed, failed, max abs/rel diff, error-condition results, list of failures.

---

## 8. Pass/fail criteria

| Result | Criterion |
|--------|-----------|
| PASS | All in-scope cells within tolerance or accepted error condition |
| FAIL | Any numeric mismatch, invented IRR, missing required output |
| ERROR | Path hash mismatch, missing GTC, uncaught exception |

---

## 9. Not yet VALIDATED

No PEMS-vs-GM run has been executed. Status remains **NOT YET VALIDATED** until after implementation.
