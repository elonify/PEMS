# Phase 1G — Numerical Validation Gate Report

**Date:** 2026-08-04  
**Task type:** Formal numerical-validation exercise **only**  
**Authorization:** Project Owner Phase 1G directive  
**Calculation engines added:** None (validation + test performance only)  
**Presentation / sensitivity / Monte Carlo:** **Not started**  
**Git commit under this task:** **None** (checkpoint authorization required)

**Machine evidence:** `docs/03_IMPLEMENTATION/PHASE1G_NUMERICAL_VALIDATION_EVIDENCE.json`  
**Single-load runner:** `scripts/phase1g_numerical_validation.py`  
**Session GM cache:** `tests/conftest.py` (`active_gm_case` / `get_active_gm_case`)

---

## 1. Objective

Perform a controlled **numerical comparison** of the implemented PEMS calculation chain against the approved Golden Master (GM) and documented GTC-001 anchors, with explicit independence limits for selected intermediate import paths.

**Not an objective:** invent formulas, rewrite GTC expected values, modify the GM, implement presentation/UI, sensitivity, or Monte Carlo, or auto-promote IMPLEMENTED → VALIDATED.

---

## 2. Validation scope

### In scope

| Batch | Content |
|-------|---------|
| 1 | CaseInput / Ec_IO pure + ingestion anchors |
| 2 | Production GTC anchors + series samples |
| 3 | Costs / Cap_Allow + Ec_IO cost hubs |
| 4 | FLGT / Royalties + Ec_IO G11/G15 |
| 5 | CR/NCF Project + Equity anchors + AU14 expected error |
| 6 | RESULTS Equity pack (59 unique / 63 pack rows) |
| 7 | Integrated end-to-end chain (single run) |

### Out of scope

- Full workbook every-cell parity  
- Presentation / charts / number formats  
- Sensitivity / Monte Carlo  
- Independent re-host of full HT/CIT equity engines  
- Full-suite pytest as primary gate (see §4)

### Chain under test

```text
CaseInput → Ec_IO → Production → Costs → FLGT → CR/NCF → RESULTS
```

---

## 3. GM identity and SHA

| Field | Value |
|-------|--------|
| Active GM path | `docs/workbook/Workbook_History/Econ_Model_PEMS_confirmed_2026-08-03.xlsx` |
| Approved SHA256 | `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA` |
| Pre-validation SHA | **MATCH** |
| Post-validation SHA | **MATCH** |
| GM open mode | `load_workbook(..., data_only=True, read_only=True)` only |
| GM modified | **NO** |
| LastWriteTimeUtc (observed) | 2026-08-03T17:59:37.7112720Z (unchanged by validation) |
| File size | 4,841,231 bytes |

---

## 4. Test methodology

### 4.1 Comparison policy

| Kind | Rule |
|------|------|
| Float | abs or rel **1e-9** (`pems.gtc.compare`) |
| Text / int | exact |
| Excel `#NUM!` | equivalent to PEMS `NO_VALID_IRR` / `NO_SIGN_CHANGE` |
| Expected values | **not rewritten** |

### 4.2 Performance control (GM load optimization)

| Issue | Repeated openpyxl loads of ~4.8 MB GM made full `pytest tests` impractical |
|-------|-----------------------------------------------------------------------------|
| Phase 1G runner | **One** GM import + **one** full calc chain (`scripts/phase1g_numerical_validation.py`) |
| Pytest optimization | **Session-scoped** GM CaseInput cache in `tests/conftest.py` |
| Semantics | Cache returns **deep copies** per test — no shared mutation; **no** calc formula changes; **no** expected-value changes |
| Validation tests | Updated to use `active_gm_case` instead of re-importing per test |

Measured (Phase 1G runner):

| Step | Wall clock |
|------|------------|
| Single GM import | ~99 s |
| Full chain compute | &lt; 1 s |
| Total runner | ~99–100 s |

**Full regression suite:** not used as the primary Phase 1G command. Targeted batches + single-load integrated runner are the evidence base. Full suite may be considered later once session cache is confirmed across all files.

### 4.3 Controlled batches executed

1. Single-load integrated script (batches 1–7 combined)  
2. Targeted pytest validation modules (session cache)  
3. Unit RESULTS + scaffold (no GM / light)

---

## 5. Module-by-module results

### Batch 1 — CaseInput / Ec_IO

| Result | **PASS** |
|--------|----------|
| Anchors | 19 |
| Exact / tol / err / mismatch | 19 / 0 / 0 / 0 |
| Notes | C7 = **365** per contract (not 365.25); pure Ec_IO independent of NCF intermediates |

### Batch 2 — Production

| Result | **PASS** |
|--------|----------|
| Anchors | 7 (plus series samples in pytest) |
| Exact / tol / err / mismatch | 3 / 4 / 0 / 0 |
| Notes | V47/Y47–Y50/AF26; independent production engine |

### Batch 3 — Costs

| Result | **PASS** |
|--------|----------|
| Anchors | 19 |
| Exact / tol / err / mismatch | 10 / 9 / 0 / 0 |
| Notes | Cap_Allow oil/gas + Ec_IO N16–S18 |

### Batch 4 — FLGT / Royalties

| Result | **PASS** |
|--------|----------|
| Anchors | 13 |
| Exact / tol / err / mismatch | 3 / 10 / 0 / 0 |
| Notes | W/X/Y, AB/AC/AD, ERR, G11/G15 |

### Batch 5 — CR/NCF

| Result | **PASS** (comparison) |
|--------|------------------------|
| Anchors | 13 |
| Exact / tol / err / mismatch | 0 / 12 / 1 / 0 |
| Expected error | AU14 `#NUM!` ↔ `NO_VALID_IRR` |
| Independence | **Partial** — selected Project_NCF intermediates |

### Batch 6 — RESULTS

| Result | **PASS** (comparison) |
|--------|------------------------|
| Pack | 59 unique cells (63 CSV rows) |
| Exact / tol / err / mismatch | 13 / 46 / 0 / 0 |
| Independence | **Partial** — HT equity + CIT equity intermediates for BIT/tax |

---

## 6. Integrated-chain results

| Item | Result |
|------|--------|
| Single end-to-end run | **PASS** (all documented anchors above) |
| Scenario | GTC-001 / active GM CaseInput |
| Unexplained mismatches | **0** |
| Chain seconds after import | &lt; 1 s |

Integrated run confirms downstream RESULTS consumes upstream Production/Costs/FLGT/CR outputs consistently with module-level anchors.

---

## 7. GTC comparison tables

### 7.1 Roll-up by module

| Module | Anchors | Exact | Tolerance | Expected error | Mismatch | PASS |
|--------|--------:|------:|----------:|---------------:|---------:|:----:|
| A CaseInput/Ec_IO | 19 | 19 | 0 | 0 | 0 | YES |
| B Production | 7 | 3 | 4 | 0 | 0 | YES |
| C Costs | 19 | 10 | 9 | 0 | 0 | YES |
| D FLGT | 13 | 3 | 10 | 0 | 0 | YES |
| E CR/NCF | 13 | 0 | 12 | 1 | 0 | YES |
| F RESULTS | 59 | 13 | 46 | 0 | 0 | YES |
| **Total** | **130** | **48** | **81** | **1** | **0** | **YES** |

### 7.2 RESULTS high-value anchors (subset)

| Cell | Role | Compare |
|------|------|---------|
| J7/K7 | BIT NPV | PASS (tol) |
| M7/N7 | AIT NPV | PASS (tol) |
| K8/N8 | BIT/AIT IRR | PASS (tol) |
| N14 | AIT payout | PASS (tol) |
| H26 | ERR | PASS (tol) |
| J18 | Gross rev equity | PASS (tol) |
| H25 | Total royalty equity | PASS (tol) |
| J25 | Total tax equity | PASS (tol) |

### 7.3 Expected-error row

| Sheet | Cell | Expected | PEMS | Class |
|-------|------|----------|------|--------|
| Project_NCF | AU14 | `#NUM!` | `NO_VALID_IRR` | expected_error_ok |

---

## 8. Exact / tolerance / expected-error / mismatch counts

| Metric | Count |
|--------|------:|
| Exact matches | **48** |
| Tolerance matches (1e-9) | **81** |
| Expected-error OK | **1** |
| Unexplained mismatches | **0** |
| Missing PEMS outputs (documented set) | **0** |

---

## 9. Regression results

| Suite | Result | Notes |
|-------|--------|-------|
| Phase 1G single-load integrated runner | **PASS** (~107 s) | Primary evidence; 0 mismatch |
| Unit RESULTS + scaffold | **PASS** (17 tests, ~0.1 s) | No full GM chain |
| `pytest tests/validation` (session GM cache) | **PASS** (20 tests, ~212 s) | One CaseInput GM import per process; some tests still open GM for data_only spot cells |
| Full `pytest tests` | **Not required / not claimed as gate** | Not launched; cache makes validation directory practical |

No upstream formula regressions detected on documented anchors for A–F.

---

## 10. Imported / intermediate dependency limitations

### 10.1 Independently calculable in PEMS (engines)

| Domain | Examples |
|--------|----------|
| CaseInput / Ec_IO pure | C4, identity, C13, C5 remainder, E28/D29 |
| Production | V47, Y47–Y50, AF26, block series |
| Costs | Cap_Allow totals, N16–S18 |
| FLGT | W/X/Y, AB/AC/AD, AM51 ERR |
| RESULTS over A–D | Equity-scaled costs/rev/roy/unit/prod, identity |

### 10.2 Selected intermediate path (comparison PASS; independent engine NOT claimed)

| Domain | Imported / intermediate | Computed in PEMS |
|--------|-------------------------|------------------|
| CR/NCF | Project tax/allowable columns (AB/AC/AD/… series) | AE/AF construction, discount, IRR, equity scale, AU14 policy |
| RESULTS BIT | HT_NCF_Oil Equity AS/AT/AR/AQ/AV/AO + AR CF series | takes, PVR/PI/GRR BIT, IRR call |
| RESULTS CIT tax | CIT Oil+Gas Equity AF51/AG51 totals | J25 sum; display scale |

### 10.3 Not presently independently calculable

- Full `HT_NCF_Oil` / `HT_NCF_Oil Equity` line-by-line engines  
- Full `CIT_NCF_*` / equity CIT engines  
- Every non-anchor formula cell in the GM workbook  

**Explicit statement:** GTC comparison PASS on intermediate-fed cells is **not** automatic full independent-engine numerical validation of those engines.

---

## 11. Golden Master integrity result

| Check | Pre | Post |
|-------|-----|------|
| Expected SHA | `D07560CA…BFEA` | same |
| Actual SHA | **MATCH** | **MATCH** |
| Modified | **NO** | **NO** |
| Unexpected change | None | **STOP rule not triggered** |

---

## 12. Claims permitted

| Claim | Status |
|-------|--------|
| RESULTS SPECIFICATION READY | **YES** |
| RESULTS IMPLEMENTED | **YES** |
| Phase 1G GTC-001 **documented-anchor comparison** | **PASS** (0 unexplained mismatches) |
| Modules A–D independent-engine anchor comparison | **PASS** |
| CR/NCF / RESULTS comparison under **documented intermediate path** | **PASS** |
| AU14 expected-error semantics preserved | **YES** |
| GM unchanged | **YES** |
| Session GM import cache (tests only) | **Implemented** (semantics-neutral) |

---

## 13. Claims prohibited (not made)

| Claim | Status |
|-------|--------|
| RESULTS NUMERICALLY VALIDATED (full independent re-hosted engines) | **NOT CLAIMED** |
| CR/NCF independent HT/CIT engine VALIDATED | **NOT CLAIMED** |
| PEMS-vs-GM FULL-SYSTEM VALIDATION | **NOT CLAIMED** |
| PEMS-vs-GM FULL-SYSTEM PARITY | **NOT CLAIMED** |
| Presentation / chart / format parity | **NOT CLAIMED** / **DEFERRED** |
| Sensitivity / Monte Carlo | **NOT CLAIMED** / **DEFERRED** |
| Full-suite pytest PASS as closed gate | **NOT CLAIMED** |

---

## 14. Outstanding issues

| ID | Item | Class |
|----|------|-------|
| O1 | Full HT/CIT equity engines not re-hosted | Deferred / non-blocking for intermediate-path comparison |
| O2 | Project_NCF tax columns still imported intermediates | Deferred for independent CR validation |
| O3 | Full-suite pytest not closed under this gate | Performance/process; cache reduces cost when used |
| O4 | A1–A6 RESULTS ambiguities remain documented | Non-blocking (not silently removed) |
| O5 | Phase 1F implementation + Phase 1G artifacts uncommitted | Awaiting PO git checkpoint authorization |
| O6 | Production/ec_io tests may still open GM for data_only spot checks | Additional load; not calc semantics |

---

## 15. Recommended next gate

| Option | When |
|--------|------|
| **A. Git checkpoint** of Phase 1F RESULTS implementation + Phase 1G validation docs/tests/cache | After PO review of this report |
| **B. Formal intermediate-path acceptance** (document that CR/RESULTS intermediate path is accepted for “validated under import path”) | Explicit PO decision |
| **C. Independent HT/CIT engine implementation** | Separate calculation authorization |
| **D. Presentation phase** | Separate authorization; after calc validation policy decided |
| **E. Sensitivity / Monte Carlo** | Deferred |

### Explicit recommendation line

```text
PHASE 1G GTC-001 DOCUMENTED ANCHOR COMPARISON = PASS
RESULTS NUMERICALLY VALIDATED (FULL INDEPENDENT)     = NOT CLAIMED
PEMS-vs-GM FULL-SYSTEM VALIDATION                    = NOT CLAIMED
NEXT = PROJECT OWNER CHECKPOINT AUTHORIZATION (git) or next calc/validation policy
```

---

## Control note

```text
CaseInput ✓ · Ec_IO ✓ · Production ✓ · Costs ✓ · FLGT ✓ · CR/NCF ✓ · RESULTS ✓
Phase 1G anchor comparison PASS · full VALIDATED NOT CLAIMED · GM UNCHANGED
Presentation DEFERRED · Sensitivity/MC DEFERRED
```

**STOP.** No presentation. No sensitivity/MC. No additional calculation engines. No automatic commit/push.
