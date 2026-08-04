# VALIDATION_FRAMEWORK.md

Version: 2.0
Status: Mandatory Engineering Standard
Project: Elonify Petroleum Economics Modeling System (PEMS)

---

# 1. Purpose

This document defines the validation methodology for Elonify PEMS.

Validation is mandatory for every implemented module.

No feature shall be regarded as complete until it has been successfully validated against the corresponding Excel workbook.

---

# 2. Validation Philosophy

The Microsoft Excel workbook is the validated business specification (Golden Master).

The Python application is the software implementation.

The objective of validation is to demonstrate that the software reproduces the workbook's business logic and outputs within approved tolerances.

Validation is continuous throughout development and is not a one-time activity.

---

# 3. Validation Objectives

The framework shall:

- Preserve calculation fidelity.
- Detect implementation errors early.
- Prevent regression.
- Maintain confidence across releases.
- Ensure reproducibility.
- Support independent verification.
- Provide an auditable record of implementation quality.

---

# 4. Validation Hierarchy

Validation shall be performed at six levels.

Level 1 – Workbook Structure Validation

↓

Level 2 – Formula Validation

↓

Level 3 – Cell Validation

↓

Level 4 – Module Validation

↓

Level 5 – System Integration Validation

↓

Level 6 – Regression Validation

Each level must pass before progressing to the next.

---

# 5. Workbook Version Control

Every workbook used for validation shall be uniquely identified.

Example:

Workbook Name

Version

Revision Date

Author

Checksum

Location

Validation Status

Only approved workbook versions shall be used as Golden Masters.

---

# 6. Workbook Analysis

Before implementation, document:

- Worksheet name
- Business purpose
- Inputs
- Outputs
- Named ranges
- Formula groups
- Lookup tables
- Hidden calculations
- Dependencies
- Validation rules
- Charts
- Reports
- Assumptions

---

# 7. Formula Validation

Before coding:

Capture the original Excel formula.

Document:

Cell Reference

Formula

Business Meaning

Precedents

Dependents

Expected Output

Python Equivalent

Reviewer

Approval Status

No formula shall be implemented without documentation.

---

# 8. Cell Validation

Every critical calculation cell shall be compared.

Validation Record

Workbook Cell

Excel Value

Python Value

Difference

Tolerance

Status

PASS / FAIL

Examples include:

- Production
- Revenue
- Royalty
- Hydrocarbon Tax
- CIT
- Cap Allowance
- OPEX
- CAPEX
- Net Cash Flow
- Discounted Cash Flow
- NPV
- IRR
- PI
- POT
- Economic Limit

---

# 9. Module Validation

Each module shall have its own validation checklist.

Example

Production Module

□ Inputs validated

□ Formula validation complete

□ Cell validation complete

□ Unit tests passed

□ Workbook comparison passed

□ Documentation updated

□ Approved

Status

Validated

---

# 10. Integration Validation

After multiple modules are complete:

Validate complete project workflows.

Example workflow

Inputs

↓

Production

↓

Revenue

↓

Royalty

↓

Hydrocarbon Tax

↓

Company Income Tax

↓

Cash Flow

↓

Economic Metrics

↓

Reports

↓

Charts

The complete workflow shall match Excel.

---

# 11. Regression Validation

Regression tests shall be executed whenever:

- Formula changes
- Workbook changes
- New module added
- Bug fixed
- Refactoring completed
- Release candidate prepared

No release shall bypass regression testing.

---

# 12. Validation Dataset Repository

validation/

    workbook_versions/

    scenarios/

    expected_outputs/

    reports/

    regression/

Every approved workbook shall have corresponding validation datasets.

---

# 13. Test Scenarios

Every major workflow shall have multiple scenarios.

Minimum scenarios:

Base Case

High Price

Low Price

High CAPEX

High OPEX

Low Production

High Production

Marginal Field

Negative Cash Flow

Economic Limit

Additional scenarios shall be added as the model evolves.

---

# 14. Expected Outputs

For each scenario store:

Inputs

Expected Outputs

Intermediate Results

Final Metrics

Charts (future)

Reports (future)

This repository forms the regression baseline.

---

# 15. Automated Validation Engine

Validation shall be automated.

Architecture

Workbook Loader

↓

Scenario Loader

↓

Calculation Engine

↓

Comparison Engine

↓

Tolerance Checker

↓

Validation Report Generator

No manual comparison shall be required.

---

# 16. Tolerance Policy

Exact Match

Integer values

Tolerance = 0

Financial Values

Tolerance = configurable

Percentages

Tolerance = configurable

Floating Point Values

Tolerance = configurable

Configuration shall be maintained centrally.

---

# 17. Validation Reports

Every validation run shall produce a report.

Example

Validation Date

Workbook Version

Module

Scenario

Cells Compared

Passed

Failed

Maximum Difference

Average Difference

Status

Reviewer

Reports shall be archived.

---

# 18. Error Classification

Errors shall be classified.

Critical

Major

Minor

Informational

Critical validation failures block implementation.

---

# 19. Continuous Validation

Validation shall be executed:

After every module

Before every merge

Before every release

After workbook updates

After major refactoring

---

# 20. Definition of Ready

A module is Ready when:

✓ Workbook analysed

✓ Formula captured

✓ Dependencies documented

✓ Validation dataset prepared

✓ Expected outputs recorded

---

# 21. Definition of Done

A module is Done only when:

✓ Implementation complete

✓ Unit tests pass

✓ Formula validation passed

✓ Cell validation passed

✓ Module validation passed

✓ Integration validation passed

✓ Regression validation passed

✓ Documentation updated

✓ Git committed

---

# 22. Validation Traceability

Every validation result shall trace to:

Workbook Version

↓

Worksheet

↓

Business Requirement

↓

Application Module

↓

Python Class

↓

Python Function

↓

Unit Test

↓

Regression Test

↓

Validation Report

Nothing shall remain untraceable.

---

# 23. Workbook Change Management

Whenever the workbook changes:

1. Register workbook version.

2. Compare against previous version.

3. Identify impacted modules.

4. Update architecture.

5. Update module specifications.

6. Update validation datasets.

7. Re-run regression tests.

8. Archive validation reports.

---

# 24. Release Gate

A release shall not be approved unless:

✓ All regression tests pass

✓ No critical validation failures exist

✓ Documentation is current

✓ Workbook version is recorded

✓ Validation reports are archived

---

# 25. Conclusion

Validation is a core engineering activity within Elonify PEMS.

The success of the project is measured not only by functional software but by demonstrable equivalence with the validated Excel business specification.

Every implementation shall be supported by objective validation evidence.