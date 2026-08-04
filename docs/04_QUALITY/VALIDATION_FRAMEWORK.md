# VALIDATION_FRAMEWORK.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Mandatory engineering standard  
**Supersedes:** pre-v2.1 VALIDATION_FRAMEWORK (including 4-level-only summaries)  

---

## 1. Purpose

Defines validation methodology for PEMS.

No feature is complete until successfully validated against the corresponding Excel Golden Master behaviour.

---

## 2. Philosophy

- Excel workbook = Golden Master for business calculations and expected results  
- Python application = software implementation  
- Demonstrate reproduction of business logic and outputs within approved tolerances  
- Continuous activity, not a one-time event  

---

## 3. Objectives

Preserve calculation fidelity; detect errors early; prevent regression; maintain release confidence; ensure reproducibility; support independent verification; provide auditable quality records.

---

## 4. Validation Hierarchy (six levels — authoritative)

```text
Level 1 – Workbook Structure Validation
Level 2 – Formula Validation
Level 3 – Cell Validation
Level 4 – Module Validation
Level 5 – System Integration Validation
Level 6 – Regression Validation
```

Each level must pass before treating the next as complete for a given scope.

**Note:** Pre-v2.1 architecture documents that listed only four levels are superseded by this model.

---

## 5. Required Validation Types

| Type | Requirement |
|------|-------------|
| Unit testing | Mandatory per module |
| Integration testing | Mandatory where modules interact |
| Regression testing | Mandatory on change / release |
| Workbook comparison | Mandatory for calculation modules |
| Cell-level validation | Where applicable to critical cells |
| Formula-level traceability | Mandatory before coding formulas |
| Golden Test Cases | Mandatory scenario library |
| Tolerance definitions | Central configuration |
| Auditability | Reports archived |
| Reproducibility | Fixed workbook version + inputs |

A module is not complete merely because code runs.

---

## 6. Workbook Version Control

Every validation workbook uniquely identified:

Name, version, revision date, author, checksum (SHA256), location, approval status.

Only approved versions are Golden Masters.

---

## 7. Workbook Analysis (pre-implementation)

Document: worksheet name, purpose, inputs, outputs, named ranges, formula groups, lookups, hidden calculations, dependencies, validation rules, charts, reports, assumptions.

---

## 8. Formula Validation

Before coding, capture:

Cell reference, formula, business meaning, precedents, dependents, expected output, Python equivalent, reviewer, approval.

No formula implemented without documentation.

---

## 9. Cell Validation

Compare critical cells:

| Workbook Cell | Excel Value | PEMS Value | Difference | Tolerance | PASS/FAIL |

Examples: production, revenue, royalty, hydrocarbon tax, CIT, capital allowance, OPEX, CAPEX, NCF, DCF, NPV, IRR, PI, POT, economic limit.

---

## 10. Module Validation Checklist

- Inputs validated  
- Formula validation complete  
- Cell validation complete  
- Unit tests passed  
- Workbook comparison passed  
- Documentation updated  
- Approved  

---

## 11. Integration Validation

Full workflow example:

```text
Inputs → Production → Revenue → Royalty → Hydrocarbon Tax
→ CIT → Cash Flow → Economic Metrics → Reports → Charts
```

Complete workflow must match Excel within tolerances.

---

## 12. Regression Validation

Run when: formula changes, workbook changes, new module, bug fix, refactor, release candidate.

No release bypasses regression.

---

## 13. Golden Test Cases

Minimum scenario set (extend as model evolves):

Base Case, High Price, Low Price, High CAPEX, High OPEX, Low Production, High Production, Marginal Field, Negative Cash Flow, Economic Limit.

For each store: inputs, expected outputs, intermediate results, final metrics; charts/reports later.

---

## 14. Dataset Repository

```text
docs/workbook/Validation_Datasets/
  scenarios/
  expected_outputs/
  regression/
```

Tests may mirror fixtures under `tests/validation/`.

---

## 15. Automated Validation Engine

```text
Workbook Loader → Scenario Loader → Calculation Engine
→ Comparison Engine → Tolerance Checker → Validation Report Generator
```

Manual-only comparison is not the target state.

---

## 16. Tolerance Policy

| Class | Policy |
|-------|--------|
| Integers | Exact (0) unless documented |
| Financial values | Configurable |
| Percentages | Configurable |
| Other floats | Configurable |

Central config: CONFIGURATION.md / tolerances file.

---

## 16.1 Excel error strings and IRR no-sign-change (mandatory)

Distinguish:

| Class | Example | Validation treatment |
|-------|---------|----------------------|
| **Genuine workbook defect** | Unexpected `#REF!` on active GM | Tracked in WORKBOOK_ERROR_STATUS; not a PEMS pass target until fixed or reclassified |
| **Expected / accepted Excel condition** | `#NUM!` from `IRR` when NCF has no qualifying sign change | **Golden expected behaviour** — PEMS must match |

### IRR no-sign-change rule (GTC / PEMS)

Excel `IRR` returns `#NUM!` when the cash-flow series has **no qualifying sign change** (e.g. all blank, all non-negative, or all non-positive non-zero flows — no mix of + and − that allows a conventional IRR).

**Active Golden Master example (SHA `D07560CA…BFEA`):**

- `Project_NCF!AU14` `=IRR(AK5:AK49)` → `#NUM!`  
- `AK5:AK49` entirely blank (0 positive, 0 negative, 0 zero stored) → **no sign change**  
- Classification: **EXPECTED / ACCEPTED IRR NO-SIGN-CHANGE CONDITION** (not a workbook defect)  
- Authority: `docs/workbook/semantic_mapping/WORKBOOK_ERROR_STATUS.md`

**Validation PASS criteria for such cells:**

- Expected result recorded as Excel error / no-IRR (`#NUM!`)  
- PEMS reports **no defined IRR** for the same series (explicit no-IRR / error outcome)  
- PEMS **must not invent** a numeric IRR  

**FAIL if PEMS manufactures a rate where Excel returns `#NUM!` under this condition.**

Documented in GTC-001 (`use_as_numeric_golden` semantics: match error/no-IRR, not a float).

---

## 17. Validation Report Content

Date, workbook version, module, scenario, cells compared, passed, failed, max/avg difference, status, reviewer.

Archive under quality records (e.g. `docs/04_QUALITY/validation_reports/` when created).

### Report template fields

Validation ID, PASS/FAIL summary, formula/cell/module/regression sections, critical/major/minor failures, recommendations, approval signatures.

---

## 18. Error Classification

Critical (blocks), Major, Minor, Informational.

---

## 19. Continuous Validation

After every module; before merge; before release; after workbook updates; after major refactoring.

---

## 20. Definition of Ready / Done

**Ready:** workbook analysed, formulas captured, deps documented, validation dataset prepared, expected outputs recorded.

**Done:** implementation complete; unit/formula/cell/module/integration/regression pass; docs updated; git commit ready.

---

## 21. Traceability

```text
Workbook Version → Worksheet → Business Requirement → Application Module
→ Python Class → Function → Unit Test → Regression Test → Validation Report
```

---

## 22. Workbook Change Management

1. Register workbook version  
2. Compare to previous  
3. Identify impacted modules  
4. Update architecture if needed  
5. Update module specifications  
6. Update validation datasets  
7. Re-run regression  
8. Archive reports  

---

## 23. Release Gate

- All regression tests pass  
- No critical validation failures  
- Documentation current  
- Workbook version recorded  
- Validation reports archived  

---

## 24. Conclusion

Success is measured by demonstrable equivalence with the validated Excel business specification, not only by functional software.
