# GTC Framework (Pre-Implementation)

**Active case:** GTC-001  
**Active GM SHA256:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Policy:** Do not invent approved economic scenarios. Framework must allow adding cases later.

---

## 1. Baseline case

| ID | Description | Source |
|----|-------------|--------|
| GTC-001 | As-saved Golden Master baseline | Active catalogue expected outputs + KPI pack + inputs |

Artifacts under `docs/workbook/Validation_Datasets/`.

---

## 2. Comparison architecture (requires ADR-0010)

```text
Golden Master (openpyxl read)
  → expected cells (formula cache / accepted error conditions)
PEMS calculation outputs
  → comparison engine (tolerance + error-condition match)
  → validation report
```

---

## 2.1 Ec_IO ingestion comparison points (pre-engine)

**Status:** Defined — input-state contract only (not full numerical VALIDATED).  
**Spec:** `docs/02_SPECIFICATIONS/modules/EC_IO_PARAMETER_CONTRACT.md` §7  

After manual entry or import into CaseInput, compare at minimum:

| PEMS field | GM cell | GTC-001 as-saved |
|------------|---------|------------------|
| equity_share_company_1 | Equity Dash!C4 | 0.49 |
| project_start_year | Ec_IO!C5 | 2027 |
| production_days_per_year | Ec_IO!C7 | 365 |
| oil_price_usd_bbl | Ec_IO!C12 | 50 |
| price_escalator | Ec_IO!C14 | 0 |
| hurdle_rate | Ec_IO!C15 | 0.15 |
| gas_price_usd_mscf | Ec_IO!C17 | 2.18 |
| C18–C26 coefficients | Ec_IO!C18:C26 | as-saved |
| case attributes | Ec_IO!C4, G18:G26 | as-saved |

Full engine compare later uses KPI pack + `formula_cached_results_all.csv`.

### 2.2 Production comparison points (pre-engine)

**Spec:** `docs/02_SPECIFICATIONS/modules/PRODUCTION_PROFILE_CONTRACT.md` §9  

| PEMS / meaning | GM cell | GTC-001 as-saved |
|----------------|---------|------------------|
| Oil max cum | Prod_Summary!V47 | 21.9977894563747 |
| Gas max cum | Prod_Summary!Y47 | 25.2454818442975 |
| Gas→boe factor | Prod_Summary!Y48 | 5.804 |
| Project life years | Prod_Summary!AF26 | 15 |
| PP mode / RF / GOR / qi,qp,qel | Production Profile key cells | as-saved (see contract) |

### 2.3 Costs comparison points (pre-engine)

**Spec:** `docs/02_SPECIFICATIONS/modules/COSTS_PARAMETER_CONTRACT.md` §8  

| Meaning | GM cell | GTC-001 as-saved |
|---------|---------|------------------|
| OPEX undisc (oil) | Cap_Allow!FI48 | 361.503330356603 |
| OPEX disc (oil) | Cap_Allow!FL48 | 185.584322008296 |
| CAPEX disc (oil) | Cap_Allow!FK48 | 142.902934166187 |
| PV OPEX combined | Ec_IO!N16 | 211.002839827046 |
| Undisc OPEX combined | Ec_IO!S16 | 418.203330356603 |
| PV CAPEX combined | Ec_IO!N17 | 142.902934166187 |
| Undisc CAPEX combined | Ec_IO!S17 | 175 |
| PV / undisc TC | Ec_IO!N18 / S18 | 353.905… / 593.203… |
| CA rates Y1–Y5 | Cap_Allow!FR5:FR9 | 0.2×4, 0.19 |

### 2.4 FLGT / Royalties comparison points (pre-engine)

**Spec:** `docs/02_SPECIFICATIONS/modules/FLGT_ROYALTIES_CONTRACT.md` §10  

| Meaning | GM cell | GTC-001 as-saved |
|---------|---------|------------------|
| Oil royalty $mm | FLGT!AB51 | 61.3138177169515 |
| Gas royalty $mm | FLGT!AC51 | 1.37587876051421 |
| Price royalty $mm | FLGT!AD51 | 0 |
| Combined royalty | FLGT!AL51 | 62.6896964774657 |
| ERR | FLGT!AM51 | 0.0542803358903504 |
| Oil / gas revenue | FLGT!W51 / X51 | 1099.889… / 55.035… |
| Hub ERR / royalties | Ec_IO!G11 / G15 | =AM51 / =AB+AC+AD |

### 2.5 CR / NCF comparison points (pre-engine)

**Spec:** `docs/02_SPECIFICATIONS/modules/CR_NCF_CONTRACT.md` §11  

| Meaning | GM cell | GTC-001 as-saved |
|---------|---------|------------------|
| Disc. host govt | Project_NCF!AG51 | 149.557072245101 |
| Disc. contractor / NPV-like | Project_NCF!AH51 | 78.0891606587929 |
| CIT / EDT / HT totals | AB51 / AC51 / AD51 | 148.760… / 26.454… / 42.083… |
| Project IRR | Project_NCF!AG58 | 0.348601049838934 |
| IRR no sign change | Project_NCF!AU14 | **#NUM!** (EXPECTED) |
| Equity disc. host/contractor | Equity_NCF_Con!AG51 / AH51 | 73.283… / 38.264… |

### 2.6 RESULTS comparison points (pre-engine)

**Spec:** `docs/02_SPECIFICATIONS/modules/RESULTS_PARAMETER_CONTRACT.md` §8  

Primary artifact: `GTC-001_kpi_and_intermediates.csv` rows with `worksheet=RESULTS Equity` (63 points), including NPV J7/K7/M7/N7, IRR K8/N8, payout K14/N14, ERR H26, revenues J16–J18, royalties H22–H25, taxes J22–J25, unit costs H19–H21.

---

## 3. Required condition handling

| Condition | Excel / GM | PEMS must |
|-----------|------------|-----------|
| Valid IRR | Numeric (e.g. AU12) | Match within float policy |
| **No-sign-change IRR** | **`#NUM!`** (AU14) | **`NO_VALID_IRR` / `NO_SIGN_CHANGE`** — **never invent rate** |
| Zero production | Per GTC cells when present | Match |
| Zero / + / − cash flows | Per series | Match; affect IRR eligibility |
| Missing input | Validation error before calc | Fail closed with message |
| Invalid input | Validation error | Fail closed |
| Fiscal boundary | Per fiscal tables | Match documented cells |
| Sensitivity / data tables | Only if in scope | DEFERRED for first modules |

### Explicit mapping — AU14

| Excel | PEMS semantic |
|-------|----------------|
| `#NUM!` on `IRR` with no qualifying sign change | `NO_VALID_IRR` / `NO_SIGN_CHANGE` |

PASS if PEMS reports no-IRR. FAIL if PEMS emits a fabricated numeric IRR.

---

## 4. Tolerances

| Type | Rule |
|------|------|
| int / bool / text | Exact |
| float | abs≤1e-9 or rel≤1e-9 (binary only) unless CONFIGURATION tightens |
| Accepted Excel errors | Exact condition match |

---

## 5. Adding future cases

New GTC-00N only when:

- New approved GM version, or  
- PO supplies distinct approved workbook state  

Register under `Validation_Datasets/scenarios/` with SHA identity.

---

## 6. Reports

Each run: workbook SHA, PEMS version, cells compared, pass/fail, max diff, error-condition results, timestamp.
