# Phase 1F — RESULTS Readiness Report

**Date:** 2026-08-04  
**Task type:** Specification / readiness / implementation-gate analysis **only**  
**Calculation code written:** **None**  
**ResultsModule:** remains `UnimplementedModule` stub  

**Authority:**  
- `docs/02_SPECIFICATIONS/modules/RESULTS_PARAMETER_CONTRACT.md`  
- Upstream contracts (Ec_IO, Production, Costs, FLGT, CR/NCF)  
- GTC-001: `Validation_Datasets/expected_outputs/GTC-001_kpi_and_intermediates.csv`  
- Evidence: `RESULTS_EVIDENCE_EXTRACT.json`  

**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**GM modified:** **No**  

**Upstream gates:** Phase 1A–1E **IMPLEMENTED** and formally acknowledged where applicable.

---

## A. Executive status

| Field | Value |
|-------|--------|
| **RESULTS specification readiness** | **READY** |
| **RESULTS implementation** | **NOT STARTED** |
| **RESULTS numerically VALIDATED** | **NOT CLAIMED** |
| **Full-system VALIDATED** | **NOT CLAIMED** |
| **Implementation authorized by this report** | **NO** — requires subsequent PO **implementation** directive |
| **Recommendation** | Spec sufficient; **RESULTS IMPLEMENTATION = NOT YET AUTHORIZED** until separate implementation authorization |

---

## B. RESULTS specification readiness

Contract status reconfirmed: **READY** (`RESULTS_PARAMETER_CONTRACT.md`).

RESULTS is a **KPI / read-model aggregation layer**, not a second economic engine:

| Class | On RESULTS Equity |
|-------|-------------------|
| CaseInput entered on sheet | **None** |
| Formula-derived KPI | ~62 formula cells |
| Labels / identity | Present |
| Upstream INPUT consumed | Equity Dash!C4 only |

---

## C. Workbook / formula inventory

| Item | Count / location |
|------|------------------|
| Primary sheet | **RESULTS Equity** (visible) |
| Nonempty cells (extract) | **107** |
| Formula cells | **62** |
| Label/text cells | **45** |
| Related hub surface | Ec_IO dashboard mirrors (not RESULTS inputs) |
| Formula-bearing KPIs | §3.1–3.6 of RESULTS contract |

### Formula groups (mapped)

| Group ID | Purpose | Example cells |
|----------|---------|---------------|
| R-ID | Identity / context | L2, L3, C5–C8, L5 |
| R-NPV | BIT/AIT NPV | J7, K7, M7, N7; H7 hurdle display |
| R-IRR | BIT/AIT IRR, PVR, PI, GRR | K8–K11, N8–N11 |
| R-TAKE | Undisc/disc fiscal take | J12–N13, H15 FLI |
| R-PAYOUT | Disc. payout years | K14, N14 |
| R-COST | Equity-scaled PV/undisc OPEX/CAPEX/TC | H16–H18, M16–M18 |
| R-REV | Equity-scaled oil/gas/gross revenue | J16–J18 |
| R-UNIT | Unit CAPEX/OPEX/TC $/boe | H19–H21, M19–M21 |
| R-ROY | Equity-scaled royalties + ERR | H22–H26 |
| R-TAX | HT/CIT/Etx totals | J22–J25 |
| R-PROD | Equity-scaled production | N22–N24, M23 text |

---

## D. CaseInput inventory

### Upstream INPUT consumed by RESULTS

| Field | Source | Role |
|-------|--------|------|
| `equity_share_company_1` | Equity Dash!C4 | Multiplier on $MM / volumes; divisor in unit-cost formulas |

### Displayed from Ec_IO (CaseInput / case attributes — not re-entered on RESULTS)

| Display | Ec_IO / source |
|---------|----------------|
| Country, regime, field, PFS, licence, terrain | L2, L3, C5, L5, C6, C7 ← Ec_IO |
| Hurdle | H7 ← Ec_IO!C15 |
| Project life (GRR) | C6 in GRR formulas |

### Not RESULTS inputs

- All CR/NCF / FLGT / Costs / Production series (DERIVED upstream)
- Fiscal law rates
- Analysis sensitivity cells (unless already baked into upstream)
- C5 equity remainder (DERIVED; not used as RESULTS input)

**Do not invent new CaseInput fields for RESULTS.**

---

## E. Upstream dependency map

```text
CaseInput + Equity C4
  → Ec_IO (identity, C15, C6, N16–S18, P16/P17 hubs)
  → Production (V47, Y47, Y49, Y50)
  → Costs (via Ec_IO cost hubs)
  → FLGT (AB51/AC51/AD51 royalties)
  → CR/NCF:
       HT_NCF_Oil Equity (BIT NPV/IRR/take/payout/HT)
       CIT_NCF_* Equity (CIT, education tax)
       Equity_NCF_Con (AIT NPV/IRR/take/payout)
  → RESULTS Equity (aggregation / ratios / IRR on equity CF series)
```

| Upstream | IMPLEMENTED? | RESULTS dependency |
|----------|--------------|-------------------|
| CaseInput / Equity C4 | YES | Share scale |
| Ec_IO pure + cost hub N16–S18 | YES (cost hub via Costs G6) | H7, H16–H18, M16–M18, J16–J18 labels |
| Ec_IO revenue hub P16/P17 | **Partial** — hub may still be presentation-fed from FLGT; RESULTS formulas reference Ec_IO P16/P17 | J16/J17 path |
| Production V47/Y47/Y49/Y50 | YES | Unit costs, production KPIs |
| Costs | YES | Via Ec_IO hubs |
| FLGT AB51/AC51/AD51 | YES | H22–H25, ERR |
| CR/NCF Project + Equity sheets | YES (1E; HT equity intermediates may need import path similar to CR) | BIT/AIT NPV, IRR, take, tax, payout |

**Circularity:** Ec_IO hub mirrors some NCF/FLGT KPIs; RESULTS reads Ec_IO. Implement RESULTS as **post-NCF dashboard**, not iterative solve.

---

## F. Formula groups (logic summary)

| Group | Logic pattern | Units |
|-------|---------------|-------|
| Identity | Direct cell refs from Ec_IO / C4 text | text |
| BIT NPV | Pull HT_NCF_Oil Equity AS51/AT51 | $mm |
| AIT NPV | Pull Equity_NCF_Con AG51/AH51 | $mm |
| IRR | Excel IRR on equity CF ranges | fraction |
| PVR/PI/GRR | Ratios of NPV to PV TC; GRR uses life+hurdle | fraction / 0.00 |
| Take | Host/(host+contractor) undisc and disc | fraction |
| Cost/revenue equity scale | Ec_IO hub × C4 | $ (display $MM) |
| Unit costs | (equity-scaled cost) / Y50 / C4 | $/Boe |
| Royalties/tax | FLGT/HT/CIT totals × C4 or equity sheet sums | $mm |
| ERR | Total royalty / gross revenue J18 | fraction |

Full formula text: catalogue + RESULTS contract §3.

---

## G. GTC-001 comparison inventory

| Source | Count |
|--------|------:|
| RESULTS Equity rows in `GTC-001_kpi_and_intermediates.csv` | **63** |
| Highest-value subset documented in contract §8 | ~20 cells |

| Comparison type | Policy |
|-----------------|--------|
| Float KPIs | abs/rel **1e-9** |
| Text identity | exact |
| AU14 (E2E, not on RESULTS sheet) | expected_error `#NUM!` ↔ `NO_VALID_IRR` |
| RESULTS K8/N8 when numeric | float golden |

**Do not rewrite expected values.** Primary pack path:  
`docs/workbook/Validation_Datasets/expected_outputs/GTC-001_kpi_and_intermediates.csv` filtered to `worksheet == RESULTS Equity`.

---

## H. Output / KPI inventory (material)

| Category | Cells (representative) |
|----------|------------------------|
| NPV BIT/AIT | J7, K7, M7, N7 |
| IRR / PVR / PI / GRR | K8–K11, N8–N11 |
| Take / FLI / payout | J12–N14, H15 |
| Costs equity | H16–H18, M16–M18 |
| Revenues equity | J16–J18 |
| Unit economics | H19–H21, M19–M21 |
| Royalties + ERR | H22–H26 |
| Taxes | J22–J25 |
| Production equity | N22–N24, M23 |
| Identity | L2, L3, C5–C8, L5, H7 |

---

## I. Unit and timing semantics

| Item | Convention |
|------|------------|
| Money KPIs | Workbook $mm series × equity; Excel accounting formats |
| Unit costs | $/Boe; **preserve** formula order `H16/Y50/C4` |
| Rates | fraction (display as %) |
| Payout | years |
| Time | Totals / series already annual upstream; RESULTS is mostly **scalar KPI** aggregation |
| Production | MMbbls, Mmboe, Bscf text |

---

## J. Special / error handling

| Condition | Treatment |
|-----------|-----------|
| Project_NCF AU14 | E2E GTC condition; not a RESULTS cell |
| RESULTS IRR no sign change | Surface **NO_VALID_IRR** if Excel would `#NUM!` |
| C4 = 0 | Unit-cost division hazard — match Excel or reject CaseInput |
| J18 = 0 | ERR H26 — match GM cache |
| Missing upstream | Fail closed before RESULTS |

---

## K. Ambiguity register

| ID | Item | Classification | Note |
|----|------|----------------|------|
| A1 | BIT vs AIT naming | **Non-blocking** | BIT ← HT equity; AIT ← Equity_NCF_Con; preserve workbook labels |
| A2 | Unit-cost / C4 order | **Non-blocking** | Must keep Excel order `num/Y50/C4` |
| A3 | Dual Ec_IO hub vs RESULTS surface | **Non-blocking** | Two surfaces; RESULTS Equity is primary RESULTS module |
| A4 | Ec_IO P16/P17 revenue hub completeness | **Non-blocking for readiness** | Formulas reference Ec_IO; may source from FLGT W51/X51×equity if hub not yet fully wired — implement per catalogue at code time |
| A5 | HT_NCF_Oil Equity series for BIT IRR/NPV | **Non-blocking** | 1E used intermediates for Project; RESULTS may need equity HT series import/compute — catalogue path |
| A6 | Charts / dual-axis | **Deferred** | CHART_SPECIFICATION; not blocking KPI contract |

**No blocking ambiguity** preventing specification READY.

---

## L. Deferred items

| Item | Bound |
|------|-------|
| Presentation fonts/styles/colours/number formats | PRESENTATION phase |
| Charts / dashboards visual | PRESENTATION |
| Sensitivity / Monte Carlo UI | DEFERRED |
| Full-system numerical validation | Separate validation gate |
| Full HT Equity line-by-line if not already available | Catalogue at implement time |
| RESULTS visual layout matching Excel | Presentation specs |

---

## M. Implementation scope (when authorized later)

1. `ResultsModule` as pure aggregator over upstream Results/DTO series.  
2. Identity + all KPI groups R-ID … R-PROD.  
3. Equity C4 scaling rules.  
4. IRR with NO_VALID_IRR policy.  
5. GTC harness for 63 RESULTS Equity KPI rows (+ high-value subset first).  
6. Unit tests for ratios, equity scale, unit-cost order, ERR, take statistics.

---

## N. Implementation exclusions (this readiness phase and default until authorized)

- No RESULTS calculation code in Phase 1F readiness  
- No presentation formatting  
- No charts UI  
- No sensitivity / MC  
- No inventing formulas  
- No GM modification  
- No full-suite mandatory re-run for readiness  

---

## O. Tests required (planned)

| ID | Area |
|----|------|
| T01 | Identity fields map from CaseInput/Ec_IO |
| T02 | Equity C4 scaling on $mm KPIs |
| T03 | Unit-cost formula order |
| T04 | ERR = royalties / gross revenue |
| T05 | Take ratios (undisc/disc) |
| T06 | PVR/PI/GRR algebra |
| T07 | IRR numeric goldens K8/N8 |
| T08 | NO_VALID_IRR policy for empty/no-sign-change series |
| T09 | GTC 63-point pack compare |
| T10 | Regression: Phase 0–1E still pass |

---

## P. GTC harness plan

```text
import CaseInput from GM (read-only)
run Production → Costs → FLGT → CR/NCF
run ResultsModule (when implemented)
cell_map RESULTS Equity KPIs
compare vs GTC-001 KPI pack (worksheet == RESULTS Equity)
reuse pems.gtc.compare (exact / 1e-9 / expected_error)
```

Do **not** rewrite expected CSV values.

---

## Q. IMPLEMENTED criteria (future code phase)

RESULTS = **IMPLEMENTED** only when:

1. All material KPI groups coded from contract formulas  
2. Equity C4 rules correct  
3. Unit tests T01–T08 pass  
4. GTC RESULTS pack executed with **0 unexplained mismatches**  
5. Prior suite regression policy satisfied (or documented limitation accepted by PO)  
6. GM SHA MATCH; GM unmodified  
7. Implementation report written  

---

## R. VALIDATED criteria (separate)

RESULTS = **NUMERICALLY VALIDATED** only after formal numerical-validation criteria and broader evidence — **not** automatic from IMPLEMENTED + subset GTC.

Full-system VALIDATED remains separate and **NOT CLAIMED**.

---

## S. Golden Master integrity

| Check | Result |
|-------|--------|
| Expected SHA | `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA` |
| Actual (pre/post readiness) | **MATCH** |
| GM modified | **NO** |

---

## T. Phase 1F recommendation

| Three-state | Status |
|-------------|--------|
| **SPECIFICATION READY** | **YES — READY** |
| **IMPLEMENTED** | **NO — NOT STARTED** |
| **NUMERICALLY VALIDATED** | **NOT CLAIMED** |

### Explicit recommendation

# **RESULTS IMPLEMENTATION = NOT YET AUTHORIZED**

Specification readiness gate for RESULTS is **READY**.  

**Calculation implementation requires a subsequent Project Owner directive** that explicitly authorizes Phase 1F RESULTS coding (and defines GTC/regression expectations).

---

## Control note

```text
CaseInput ✓ · Ec_IO ✓ · Production ✓ · Costs ✓ · FLGT ✓ · CR/NCF ✓
RESULTS = SPEC READY · IMPLEMENTED NOT STARTED · VALIDATED NOT CLAIMED
```

**STOP.** No RESULTS calculation code. No presentation. No commit required under this readiness directive.
