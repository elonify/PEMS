# Input Schema — Critical Path

**GM SHA (ACTIVE):** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Status:** **Ec_IO / CaseInput READY** for implementation of input layer (not calc VALIDATED)  
**Authoritative detail:** `modules/EC_IO_PARAMETER_CONTRACT.md`

---

## Canonical model principle

Manual entry and Excel import populate the **same** `CaseInput` object.  
One validation path. One calculation consumer interface.

---

## A. Closed domain inputs

| Field ID | Source | Type | Required | Classification | Notes |
|----------|--------|------|----------|----------------|-------|
| `equity_share_company_1` | Equity Dash **C4** | float | Yes | **CONFIRMED_INPUT** | GTC-001 = **0.49** |
| `equity_share_company_2` | Equity Dash **C5** | float | — | **DERIVED** | `=C6-C4`; never independent input |
| `project_equity_total` | Equity Dash **C6** | float | Optional* | DEFAULT_STRUCTURAL | GM = **1** |

\*Required for strict equity parity import if multi-party cases expand.

---

## B. Not ordinary inputs

| Data | Classification | Load path |
|------|----------------|-----------|
| Fiscal Terms_PIA table set | **LAW_TABLE** | Regime package / read-only; selectors from Ec_IO case attributes |

---

## C. Ec_IO CaseInput fields (summary)

Full field dictionary, validation, import map, GTC points: **`EC_IO_PARAMETER_CONTRACT.md` §3–7**.

| Group | Examples | Classification |
|-------|----------|----------------|
| Timing | `project_start_year` C5, `production_days_per_year` C7 | ASSUMPTION |
| Prices / rates | oil C12, gas C17, escalator C14, hurdle C15 | ASSUMPTION / DEFAULT_STRUCTURAL |
| Fiscal coefficients | C18–C26 (flare, Dom_Gas, duties, VAT, NAG*) | COEFFICIENT / DEFAULT / ASSUMPTION |
| Case attributes | C4 analysis type; G18–G26 field/terrain/licence/PFS/country/regime | CASE_ATTRIBUTE_TEXT |
| Excluded | Sensitivity tables C69+, D70+, D82+ | PRESENTATION / DEFERRED |

---

## D. Validation hooks (minimum)

| Field | Rule |
|-------|------|
| equity_share_company_1 | required, numeric; suggested (0,1] — bounds **domain confirmation** |
| hurdle_rate, prices | required, numeric |
| asset_analysis_type | enum History \| Forecast \| Complete (DV) |
| pfs_contract_type | enum R/T (SR) \| PSC/SC (DV) |
| Fiscal law tables | integrity by GM version / SHA, not per-scenario free edit |

---

## E. GTC-001 ingestion compare (not full validation)

After load, CaseInput must match as-saved GM cells listed in `EC_IO_PARAMETER_CONTRACT.md` §7.1.  
Numerical engine compare uses KPI pack + formula caches **after** implementation.
