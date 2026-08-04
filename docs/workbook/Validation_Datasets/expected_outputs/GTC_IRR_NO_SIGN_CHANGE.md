# GTC — IRR no-sign-change expected condition

**Active SHA256:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`

| Field | Value |
|-------|--------|
| Cell | `Project_NCF!AU14` |
| Formula | `=IRR(AK5:AK49)` |
| Expected Excel result | `#NUM!` |
| Classification | EXPECTED / ACCEPTED IRR NO-SIGN-CHANGE CONDITION |
| Series | AK5:AK49 — entirely blank (pos=0, neg=0, zero=0) |
| GTC PASS | PEMS returns no-IRR / equivalent to `#NUM!` |
| GTC FAIL | PEMS invents a numeric IRR |
| Workbook defect | **No** |

Also listed in `formula_cached_results_all.csv` and `GTC-001_kpi_and_intermediates.csv` with `use_as_numeric_golden=NO` and expected_value `#NUM!`.
