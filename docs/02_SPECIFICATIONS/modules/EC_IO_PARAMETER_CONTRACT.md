# Ec_IO Parameter Contract — Implementation Readiness

**Status:** **READY** (parameter / input contract only — not calculation VALIDATED)  
**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Module:** M-CP-01 / M01 Input-Control — Ec_IO hub + Equity Dash share interface  
**GM modified:** **No**  
**Calculation implementation:** **Not started** (out of scope for this document)

**Do not reopen:** Equity Share INPUT · C5 DERIVED · Fiscal LAW TABLE · AU14 expected · 829/829 literals · Ec_IO unresolved = 0 · ADR-0010  

**Authoritative companions:**  
- `EQUITY_DASH_SHARE_INPUT.md`  
- `FISCAL_TERMS_PIA_LAW_TABLE.md`  
- `INPUT_SCHEMA_CRITICAL_PATH.md`  
- `docs/workbook/semantic_mapping/CRITICAL_PATH_LITERAL_REGISTER_FULL.csv`  
- `docs/workbook/catalogue/` + GTC-001  

---

## 0. Scope of READY

| In scope | Out of scope |
|----------|----------------|
| Canonical PEMS parameters for **base-case** Ec_IO drivers | Sensitivity tables (oil-price / discount-rate data tables) — **PRESENTATION / DEFERRED** with Analysis |
| Equity Dash **C4** share INPUT interface | Full Equity Dash loan/amort block (PARTIAL elsewhere) |
| Interface **to** Fiscal Terms law layer (selectors only) | Duplicating Fiscal Terms_PIA rates as Ec_IO inputs |
| Manual + import paths into **one** input model | Separate calc engines per input path |
| GTC **comparison contract** (cells/points) | Claiming PEMS-vs-GM numerical VALIDATED |

---

## 1. Architecture

```text
Manual UI  ──┐
             ├──► Canonical PEMS CaseInput model ──► calc modules ──► GTC compare points
Excel import ┘         (single validation path)
                              │
                              ├── equity_share_company_1  ← Equity Dash!C4
                              ├── Ec_IO scenario drivers  ← Ec_IO!C* / G*
                              └── fiscal_selectors        → FiscalTermsLawTable (read-only)
```

- Ec_IO Excel sheet is both **input surface** and **results hub** (many formulas pull Cap_Allow / NCF / FLGT).  
- PEMS must **not** treat every Ec_IO formula cell as an input.  
- Only parameters listed in §3 enter the CaseInput model as user/importable state.

---

## 2. Classification legend (implementation)

| Class | Meaning for PEMS |
|-------|------------------|
| `CONFIRMED_INPUT` | User/scenario input (PO closed) |
| `ASSUMPTION` | Scenario assumption; user/importable; drives base case |
| `DEFAULT_STRUCTURAL` | Structural default / seed; user may change; not free-invented |
| `FORMULA_COEFFICIENT` | Coefficient used in calc; usually importable; not primary UI |
| `CASE_ATTRIBUTE_TEXT` | Text/enumeration case identity (terrain, regime, field, …) |
| `DERIVED` | Computed from other inputs — **not** independent input |
| `HUB_OUTPUT` | Formula result displayed on Ec_IO — **not** CaseInput |
| `PRESENTATION` | Sensitivity / mirror / table — deferred |

Critical-path register: all Ec_IO numeric literals **RESOLVED** (0 UNRESOLVED).  
Where register class differs from consumption-based implementation role, this contract states the **implementation role** and cites evidence (label + formula consumers).

---

## 3. Parameter catalogue (implementation-relevant)

### 3.1 Equity share (closed INPUT — not on Ec_IO sheet)

| Field | Value |
|-------|--------|
| **PEMS parameter** | `equity_share_company_1` |
| Excel | `Equity Dash!C4` |
| GM value | **0.49** |
| Semantic meaning | Company 1 equity holding / working-interest fraction |
| Classification | **CONFIRMED_INPUT** |
| Unit | unitless fraction |
| Data type | `float` |
| Required | **Yes** |
| Default | No code default — use GTC/GM **0.49** only for baseline case load |
| Validation | Required; numeric; finite; **workbook does not encode min/max list** — recommend (0, 1] **pending domain confirmation** of exclusive bounds |
| Manual | Yes — equity share control |
| Import | Map `Equity Dash!C4` (or named equivalent if present) |
| Downstream | Equity NCF sheets, RESULTS Equity; scales equity economics |
| Dependency | Drives **derived** `equity_share_company_2` = `project_equity_total − equity_share_company_1` where `project_equity_total` = `Equity Dash!C6` (GM **1**); Excel `C5=C6-C4` |
| GTC compare | `Equity Dash!C4` expected **0.49**; do not recompute C4 |
| Trace | `EQUITY_DASH_SHARE_INPUT.md` |

| Field | Value |
|-------|--------|
| **PEMS parameter** | `equity_share_company_2` |
| Excel | `Equity Dash!C5` |
| GM | formula `=C6-C4` → **0.51** |
| Classification | **DERIVED** |
| Manual / import as input | **No** — compute only |
| GTC | Optional consistency check cached 0.51 |

| Field | Value |
|-------|--------|
| **PEMS parameter** | `project_equity_total` |
| Excel | `Equity Dash!C6` |
| GM value | **1** |
| Classification | DEFAULT_STRUCTURAL (project total holding on GM) |
| Manual/import | Optional structural; if omitted, GM **1** for baseline |
| Validation | Numeric; finite — bounds **not evidenced** beyond GM |

**Interface rule:** CaseInput exposes `equity_share_company_1` only as the share INPUT. Calc consumers of equity scaling receive this parameter; they must **not** accept independent Company 2 share input.

---

### 3.2 Ec_IO — base-case numeric drivers

| PEMS name | Cell | GM value | Labels (evidence) | Class (impl / register) | Unit | Type | Req | Default | Manual | Import | Downstream (evidence) | GTC point |
|-----------|------|----------|-------------------|---------------------------|------|------|-----|---------|--------|--------|----------------------|-----------|
| `project_start_year` | `Ec_IO!C5` | 2027 | B5 Project Start Year | ASSUMPTION / ASSUMPTION | year | int | Yes | GTC 2027 on baseline load | Yes | Yes | 849+ formulas via `$C$5` (Prod_Summary, Royalties, Cap_Allow, NCF…) | `Ec_IO!C5` |
| `production_days_per_year` | `Ec_IO!C7` | 365 | B7 Production days in a year | ASSUMPTION / ASSUMPTION | days/year | int/float | Yes | GTC 365 | Yes | Yes | Analysis + calendar scaling (catalogue) | `Ec_IO!C7` |
| `oil_price_usd_bbl` | `Ec_IO!C12` | 50 | B12 Crude Oil Price, $/bbl | ASSUMPTION / register DEFAULT_STRUCTURAL | $/bbl | float | Yes | GTC 50 | Yes | Yes | Royalties `$C$12` (42); oil revenue path | `Ec_IO!C12` |
| `price_escalator` | `Ec_IO!C14` | 0 | B14 Escalator | DEFAULT_STRUCTURAL | fraction (0 → Real) | float | Yes | 0 | Yes | Yes | Price format `C13=IF(C14=0%,"Real","Nominal")` | `Ec_IO!C14` |
| `hurdle_rate` | `Ec_IO!C15` | 0.15 | B15 Hurdle Rate | ASSUMPTION / ASSUMPTION | fraction/yr | float | Yes | GTC 0.15 | Yes | Yes | 1291+ refs `$C$15` Cap_Allow, HT/CIT/Project NCF, Ec_IO metrics | `Ec_IO!C15` |
| `gas_price_usd_mscf` | `Ec_IO!C17` | 2.18 | B17 Gas Price, $/Mscf | **ASSUMPTION** / register said PRESENTATION† | $/Mscf | float | Yes | GTC 2.18 | Yes | Yes | FLGT `$C$17` (42); multi-sheet revenue path | `Ec_IO!C17` |
| `gas_flare_penalty_usd_mscf` | `Ec_IO!C18` | 0.5 | B18 Gas Flare Penalty, $/Mscf | FORMULA_COEFFICIENT | $/Mscf | float | Yes | GTC 0.5 | Yes | Yes | Flare penalty consumers (catalogue) | `Ec_IO!C18` |
| `dom_gas_fraction` | `Ec_IO!C19` | 0.5 | B19 Dom_Gas | FORMULA_COEFFICIENT | fraction | float | Yes | GTC 0.5 | Yes | Yes | Dom gas path (catalogue) | `Ec_IO!C19` |
| `duties_rate` | `Ec_IO!C20` | 0 | B20 Duties | DEFAULT_STRUCTURAL | fraction | float | Yes | 0 | Yes | Yes | Cost/fiscal path | `Ec_IO!C20` |
| `vat_rate` | `Ec_IO!C21` | 0 | B21 VAT | DEFAULT_STRUCTURAL | fraction | float | Yes | 0 | Yes | Yes | Cost/fiscal path | `Ec_IO!C21` |
| `asset_salvage_frac_of_retention` | `Ec_IO!C22` | 0 | B22 Asset Salvage… | DEFAULT_STRUCTURAL | fraction | float | Yes | 0 | Yes | Yes | Decom/salvage path | `Ec_IO!C22` |
| `nag_crl` | `Ec_IO!C23` | 0 | B23 NAG CRL | DEFAULT_STRUCTURAL | fraction | float | Yes | 0 | Yes | Yes | NAG fiscal coefficients | `Ec_IO!C23` |
| `nag_ita` | `Ec_IO!C24` | 0.1 | B24 NAG ITA | FORMULA_COEFFICIENT | fraction | float | Yes | 0.1 | Yes | Yes | NAG fiscal coefficients | `Ec_IO!C24` |
| `nag_min_tax_rate` | `Ec_IO!C25` | 0.005 | B25 NAG Min. Tax Rate | ASSUMPTION | fraction | float | Yes | 0.005 | Yes | Yes | NAG min tax | `Ec_IO!C25` |
| `nag_cpr` | `Ec_IO!C26` | 0 | B26 NAG CPR | DEFAULT_STRUCTURAL | fraction | float | Yes | 0 | Yes | Yes | NAG fiscal | `Ec_IO!C26` |
| `history_year` | `Ec_IO!D28` | 2002 | C28 History | ASSUMPTION | year | int | Optional‡ | GTC 2002 | Yes | Yes | Timeline construction | `Ec_IO!D28` |
| `complete_year` | `Ec_IO!D30` | 2002 | C30 Complete | ASSUMPTION | year | int | Optional‡ | GTC 2002 | Yes | Yes | Timeline construction | `Ec_IO!D30` |

† **C17 implementation-role refinement:** Critical-path register marked PRESENTATION (MEDIUM, results-side heuristic). Formula catalogue shows **direct consumption** (`Ec_IO!$C$17` in FLGT and multi-sheet paths). Label B17 and BASE CASE INPUTS block B11 establish scenario driver role. **For CaseInput, treat as ASSUMPTION.** Does not reopen UNRESOLVED count.

‡ History/Complete years support analysis-type timeline; not every calc module may require them on day-1 — include in model for import parity.

**Derived on Ec_IO (not CaseInput):**

| Excel | Formula / source | PEMS | Class |
|-------|------------------|------|-------|
| `C6` Project Life | `=Prod_Summary!AF26` | `project_life_years` | **HUB_OUTPUT / upstream-derived** — not manual if production model supplies life |
| `C13` Price Format | `=IF(C14=0%,"Real","Nominal")` | `price_format` | **DERIVED** from `price_escalator` |
| `E28`, `D29`, `E29`, `E30`, `D22` | timeline formulas | calendar helpers | **DERIVED** |

---

### 3.3 Ec_IO — case attribute text / enumerations

| PEMS name | Cell | GM value | Label | Class | Type | Req | DV evidence | Manual | Import | Downstream | GTC |
|-----------|------|----------|-------|-------|------|-----|-------------|--------|--------|------------|-----|
| `asset_analysis_type` | `Ec_IO!C4` | Forecast | B4 Asset Analysis Type | CASE_ATTRIBUTE_TEXT | enum/text | Yes | DV list `$C$28:$C$30` → History, Forecast, Complete | Yes | Yes | Timeline / mode | `Ec_IO!C4` |
| `block_field_oil` | `Ec_IO!G18` | Ebiya Field | F18 Block/Field (Oil) | CASE_ATTRIBUTE_TEXT | str | Yes | none | Yes | Yes | Prod_Summary, Block_Oil, Oil Input refs | `Ec_IO!G18` |
| `block_field_gas` | `Ec_IO!G19` | =G18 | F19 Block/Field (Gas) | DERIVED default (=oil field) | str | — | — | Prefer derive; allow override only if import has distinct value | Import may set | Gas block identity | `Ec_IO!G19` |
| `terrain` | `Ec_IO!G20` | Shallow Water (<200m water depth) | F20 Terrain | CASE_ATTRIBUTE_TEXT | str/enum | Yes | none in workbook beyond free text | Yes | Yes | Royalties, RESULTS, **fiscal tier selection** | `Ec_IO!G20` |
| `gas_utilization` | `Ec_IO!G21` | In-Country (Dom Gas) | F21 Gas Utilization | CASE_ATTRIBUTE_TEXT | str | Yes | none | Yes | Yes | NCF / Royalties paths | `Ec_IO!G21` |
| `licence_lease_status` | `Ec_IO!G22` | New Acreage | F22 Licence/Lease Status | CASE_ATTRIBUTE_TEXT | str/enum | Yes | none | Yes | Yes | **CR Econ / fiscal** `$G$22` (270+) | `Ec_IO!G22` |
| `cost_mode_field` | `Ec_IO!G23` | =G18 | F23 Cost Mode | DERIVED (=field) on GM | str | — | — | See G18 | Import | Cost mode bridge | `Ec_IO!G23` |
| `pfs_contract_type` | `Ec_IO!G24` | PSC/SC | F24 PFS | CASE_ATTRIBUTE_TEXT | enum | Yes | DV `"R/T (SR), PSC/SC"` on G24:H24 | Yes | Yes | **CR Econ** `$G$24` (46+) | `Ec_IO!G24` |
| `country` | `Ec_IO!G25` | Nigeria | F25 Country | CASE_ATTRIBUTE_TEXT | str | Yes | none | Yes | Yes | RESULTS identity (`R2`) | `Ec_IO!G25` |
| `fiscal_regime_label` | `Ec_IO!G26` | PIA 2021 | F26 Fiscal Regime | CASE_ATTRIBUTE_TEXT | str | Yes | none | Yes | Yes | RESULTS identity; **selects law package** not rates | `Ec_IO!G26` |

**Not CaseInput:** Navigation labels (A-column sheet jumps), Metric Systems labels, KPI formula mirrors (G3–G15, P/Q/S/T result blocks) = **HUB_OUTPUT**.

---

### 3.4 Explicitly excluded from CaseInput (PRESENTATION / deferred)

| Area | Cells (examples) | Class | Reason |
|------|------------------|-------|--------|
| Oil price sensitivity axis | C69–C79 | DEFAULT_STRUCTURAL / PRESENTATION mix | Sensitivity table seeds — deferred with Analysis |
| Sensitivity NPV / payout | D70–D79, F70–F79 | PRESENTATION | Not base-case inputs |
| Discount-rate sensitivity | D82–D100, E82–E100 | ASSUMPTION axis / PRESENTATION results | Deferred Phase 10 / Analysis |
| Dashboard KPI formulas | G3–G15, N7–N26, P7–T24, … | HUB_OUTPUT | Results mirrored on Ec_IO; compare via KPI pack / consumer sheets |

---

## 4. Dual input mechanisms (same model)

### 4.1 Manual entry

| Rule | Contract |
|------|----------|
| UI fields | Bind 1:1 to CaseInput parameters in §3.1–3.3 |
| DERIVED fields | Display-only (C5 share, price_format, project_life if computed) |
| LAW TABLE | Not editable as Ec_IO fields — separate read-only fiscal browser |
| Validation | Run §5 **once** on CaseInput before calc |
| Persist | Scenario/project store (ADR persistence) — not dual schemas |

### 4.2 Excel import

| Rule | Contract |
|------|----------|
| Source workbook | User-selected .xlsx; **baseline** maps to confirmed GM sheet layout |
| Reader | openpyxl (ADR-0010) — formulas as text; values via data_only cache when available |
| Mapping | Sheet+cell → CaseInput field (§3 tables) |
| Transform | Type coercion only (int/float/str); **no silent business transforms** unless documented |
| Missing cell | Error if **required**; else use explicit optional default or fail closed |
| Extra sheets | Ignore hidden for input scope |
| Post-import | Same validator as manual → same CaseInput |
| Equity | Always map C4; never treat C5 as imported independent input |
| Fiscal Terms_PIA | Import as **law-table package identity/checksum**, not as Ec_IO parameters |

#### Import field map (summary)

| Source | Destination | Transform | Validation | Missing |
|--------|-------------|-----------|------------|---------|
| `Equity Dash!C4` | `equity_share_company_1` | float | required numeric | **Error** |
| `Equity Dash!C5` | (ignore as input) | — | may verify ≈ C6−C4 | Warning if inconsistent |
| `Equity Dash!C6` | `project_equity_total` | float | numeric | default 1 if absent on non-GM files **only if domain confirms**; else error for strict mode |
| `Ec_IO!C5` | `project_start_year` | int | required year-like | **Error** |
| `Ec_IO!C7` | `production_days_per_year` | float | required >0 **if evidenced** — only “365” on GM; strict: numeric required | **Error** |
| `Ec_IO!C12` | `oil_price_usd_bbl` | float | required numeric | **Error** |
| `Ec_IO!C14` | `price_escalator` | float | numeric | **Error** if strict base case |
| `Ec_IO!C15` | `hurdle_rate` | float | required numeric | **Error** |
| `Ec_IO!C17` | `gas_price_usd_mscf` | float | required numeric | **Error** |
| `Ec_IO!C18`…`C26` | matching params | float | numeric | **Error** for base GTC parity import |
| `Ec_IO!C4` | `asset_analysis_type` | str | enum in {History, Forecast, Complete} if DV applied | **Error** |
| `Ec_IO!G18`…`G26` | case attributes | str | non-empty if required | **Error** |
| `Ec_IO!G19`,`G23` | derived prefer | — | if present and ≠ G18, store override + flag | Warning |

Error handling: structured validation errors (field id, cell, message); no partial calc start on required-field failure.

---

## 5. Validation categories

| Category | Applied to | Evidence-based rule |
|----------|------------|---------------------|
| required | All Req=Yes in §3 | Must be present before calc |
| numeric | All float/int params | Parse as number; reject non-numeric |
| text | Case attributes | Non-empty string if required |
| percentage / fraction | hurdle_rate, escalator, NAG rates, duties, VAT, salvage, equity share | Stored as Excel serial fraction (0.15 = 15%); **display % is UI only** |
| currency | oil/gas prices, flare penalty | Numeric; unit from label only |
| date / year | start/history/complete years | Integer year; **no Excel date serial evidenced** for C5 |
| enumeration | `asset_analysis_type` | DV: History / Forecast / Complete |
| enumeration | `pfs_contract_type` | DV: `R/T (SR)` \| `PSC/SC` |
| non-negative | prices, days, duties, VAT (GM ≥0) | **Suggested** non-negative — **domain confirmation** if negatives ever valid |
| bounded numeric | equity share | **Suggested** (0,1] — **not workbook-enforced**; mark domain confirmation |
| dependency | price_format | Derived from escalator == 0 → Real else Nominal |
| dependency | company_2 share | = total − company_1 |
| dependency | fiscal law selection | terrain + licence + price + production + pfs → law table rows (interface only) |
| conditional | Analysis type History vs Forecast | Timeline helpers D28–E30; full rules **partial** — implement minimal: store type + years |

**Uncertain (must not invent hard fails without domain confirm):**

- Strict min/max for oil/gas price  
- Whether escalator may be negative  
- Whether equity share may be 0 or >1  
- Complete enumeration lists for terrain / gas utilization / licence (free text on GM)

---

## 6. Fiscal Terms_PIA interface (not Ec_IO inputs)

```text
CaseInput.fiscal_regime_label  (Ec_IO!G26)  ──┐
CaseInput.terrain              (Ec_IO!G20)  ──┤
CaseInput.licence_lease_status (Ec_IO!G22)  ──┼──► FiscalTermsService.select(law_table, attrs)
CaseInput.pfs_contract_type    (Ec_IO!G24)  ──┤         │
CaseInput.oil_price / production (elsewhere) ─┘         ▼
                                              Royalties / FLGT / CR / NCF
```

| Rule | Detail |
|------|--------|
| Law table data | Loaded from `Fiscal Terms_PIA` per GM SHA — **LAW_TABLE** |
| Ec_IO does **not** store royalty rates, CA rates, bonuses as inputs | |
| PEMS provides read API for law rows + selector using case attributes | |
| GTC | Compare **consumer** outputs, not re-entry of law cells as inputs |

See `FISCAL_TERMS_PIA_LAW_TABLE.md`.

---

## 7. GTC comparison contract (ingestion proof — not numerical VALIDATED claim)

### 7.1 Input-state compare (after manual or import)

| CaseInput field | GM cell | GTC-001 expected (as-saved) |
|-----------------|---------|-----------------------------|
| equity_share_company_1 | Equity Dash!C4 | 0.49 |
| project_start_year | Ec_IO!C5 | 2027 |
| production_days_per_year | Ec_IO!C7 | 365 |
| oil_price_usd_bbl | Ec_IO!C12 | 50 |
| price_escalator | Ec_IO!C14 | 0 |
| hurdle_rate | Ec_IO!C15 | 0.15 |
| gas_price_usd_mscf | Ec_IO!C17 | 2.18 |
| gas_flare_penalty… | Ec_IO!C18 | 0.5 |
| dom_gas_fraction | Ec_IO!C19 | 0.5 |
| duties_rate … nag_cpr | Ec_IO!C20–C26 | 0,0,0,0,0.1,0.005,0 |
| history_year / complete_year | D28 / D30 | 2002 / 2002 |
| asset_analysis_type | C4 | Forecast |
| block_field_oil … fiscal_regime_label | G18–G26 | Ebiya Field … PIA 2021 |

**PASS (ingestion):** PEMS CaseInput matches these values within type-equality rules after load.  
**Not yet:** full formula engine match.

### 7.2 Consumer path (for later calc validation)

```text
INPUT (CaseInput)
  → PEMS parameter
  → calculation consumer (Cap_Allow / Royalties / FLGT / NCF / RESULTS)
  → expected GM comparison point (GTC-001 formula caches / KPI pack)
```

| Parameter | Primary consumers (sheets) | Later GM compare examples |
|-----------|---------------------------|---------------------------|
| hurdle_rate C15 | Cap_Allow*, HT/CIT/Project NCF | Discounted NPV KPI pack (RESULTS Equity N7 etc.) |
| oil_price C12 | Royalties | FLGT revenues, RESULTS |
| gas_price C17 | FLGT | Gas revenue KPIs |
| start_year C5 | Prod_Summary, Royalties, Cap_Allow | Timeline-aligned series |
| licence G22 / pfs G24 | CR Econ | CR / NCF fiscal branches |
| equity C4 | Equity NCF, RESULTS Equity | Equity NPV/IRR KPI pack |
| fiscal_regime G26 | identity + law package | RESULTS L3 PIA 2021 |

KPI pack: `Validation_Datasets/expected_outputs/GTC-001_kpi_and_intermediates.csv` (102 rows).  
Full formula goldens: `formula_cached_results_all.csv` (86,973) — post-implementation.

---

## 8. Traceability pattern

```text
Excel cell/range
    → semantic meaning (label + §3)
    → PEMS parameter name
    → input mechanism (manual | import | derived)
    → calculation consumer (sheet/module)
    → GTC comparison point
```

Artefacts: this contract · `INPUT_SCHEMA_CRITICAL_PATH.md` · catalogue CSV · GTC-001 · `DOCUMENTATION_TRACEABILITY_MATRIX.md`.

---

## 9. Downstream dependency summary

| From | To modules |
|------|------------|
| Ec_IO drivers | Production (timing), Costs/Cap_Allow (discount), Royalties/FLGT (price), CR/NCF (fiscal selectors + rates), RESULTS (identity + KPIs) |
| Equity C4 | Equity NCF + RESULTS Equity |
| Fiscal selectors | FiscalTermsLawTable → Royalties/FLGT/CR/NCF |
| Upstream into Ec_IO hub | Prod_Summary (life), Cap_Allow/FLGT/NCF (displayed KPIs) — **outputs**, not CaseInput |

---

## 10. Readiness test checklist

| # | Criterion | Met? |
|---|-----------|------|
| 1 | All implementation-relevant parameters identified | **Yes** §3 |
| 2 | Semantically classified | **Yes** |
| 3 | Source cells/ranges mapped | **Yes** |
| 4 | Units documented | **Yes** (from labels) |
| 5 | Data types documented | **Yes** |
| 6 | Manual-entry contract | **Yes** §4.1 |
| 7 | Import contract | **Yes** §4.2 |
| 8 | Validation rules or explicitly marked uncertain | **Yes** §5 |
| 9 | Equity Dash Share correctly represented | **Yes** §3.1 |
| 10 | Fiscal Terms_PIA interface defined | **Yes** §6 |
| 11 | Downstream dependencies identified | **Yes** §9 |
| 12 | GTC comparison points identified | **Yes** §7 |
| 13 | Traceability complete | **Yes** §8 |
| 14 | No unresolved Ec_IO literals (register) | **Yes** (0 UNRESOLVED) |
| 15 | No undocumented implementation-critical ambiguity | **Yes** — residual bounds marked domain confirmation; C17 role refined with evidence |

### Status

# **EC_IO = READY**

**Means:** Input/parameter contract is sufficient to implement CaseInput + import/manual + validation + GTC ingestion compare.  
**Does not mean:** fiscal/production/cost engines READY, or PEMS numerically VALIDATED vs GM.
