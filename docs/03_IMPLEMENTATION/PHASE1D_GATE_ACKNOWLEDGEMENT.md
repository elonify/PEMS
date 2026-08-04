# Phase 1D Gate Acknowledgement — FLGT / Royalties

**Status:** **PASSED / ACKNOWLEDGED**  
**Date:** 2026-08-04  
**Evidence report:** `docs/03_IMPLEMENTATION/PHASE1D_FLGT_IMPLEMENTATION.md`  
**Readiness gate:** `docs/03_IMPLEMENTATION/PHASE1D_FLGT_IMPLEMENTATION_GATE.md`  
**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**GM modified:** **No** (SHA verified MATCH at acknowledgement)  

---

## Decision

**PHASE 1D — FLGT / ROYALTIES IMPLEMENTATION GATE = PASSED / ACKNOWLEDGED**

This acknowledgement records that the controlled FLGT/Royalties calculation implementation has met its **implementation gate** (code + tests + GTC subset + regression + GM integrity). It does **not** record full numerical module validation or full-system PEMS-vs-GM validation.

---

## Evidence accepted

| Item | Evidence |
|------|----------|
| R-G1…R-G5 | Implemented |
| F-G1…F-G11 | Implemented |
| F-G12 loan | Explicitly **deferred** |
| GTC-001 comparison points | **18** |
| Exact matches | **4** |
| Tolerance matches (1e-9) | **14** |
| Mismatches | **0** |
| Unresolved discrepancies | **0** |
| FLGT unit tests | **12 passed** |
| FLGT GTC tests | **3 passed** |
| Full regression | **70 passed / 0 failed** |
| Phase 0–1C regressions | **None** |
| GM SHA (pre/post) | **MATCH** `D07560CA…BFEA` |
| GM modified | **NO** |

---

## Scope authorized by this acknowledgement

The following are authorized as **IMPLEMENTED** (with GTC subset / regression evidence as recorded for each phase):

| Component | Scope |
|-----------|--------|
| CaseInput | Dual path + validation + provenance |
| Ec_IO pure path | Pure CaseInput derivations (hubs remaining deferred where noted) |
| Production | G1–G5 (G6 deferred) |
| Costs | G1–G8 |
| FLGT / Royalties | R-G1…R-G5 |
| FLGT application | F-G1…F-G11 |
| Tests / GTC subsets | Phase 0–1D automated suite green as of acknowledgement |

---

## Not authorized by this acknowledgement

| Item | Status |
|------|--------|
| CR/NCF calculation implementation | **NOT AUTHORIZED** |
| RESULTS implementation | **NOT AUTHORIZED** |
| Presentation implementation | **NOT AUTHORIZED** |
| Sensitivity / Monte Carlo | **NOT AUTHORIZED** |
| F-G12 loan implementation | **DEFERRED** |
| Full bonus matrix beyond core GTC path | **DEFERRED** |
| FLGT **NUMERICALLY VALIDATED** | **NOT CLAIMED** |
| PEMS-vs-GM **FULL-SYSTEM VALIDATION** | **NOT CLAIMED** |
| Ec_IO **FULL VALIDATION** | **NOT CLAIMED** |

---

## Claim discipline (explicit)

| Statement | True? |
|-----------|:-----:|
| FLGT **IMPLEMENTATION GATE = PASSED** | **Yes** |
| FLGT **IMPLEMENTED** (R-G1…F-G11) | **Yes** |
| FLGT **NUMERICALLY VALIDATED = YES** | **No** |
| PEMS-vs-GM **FULL-SYSTEM VALIDATION = YES** | **No** |

---

## Next technical activity (requires separate authorization)

**PHASE 1E — CR/NCF READINESS / IMPLEMENTATION GATE**

Do **not** write CR/NCF calculation code under this acknowledgement.

Sequence remains:

```text
CaseInput ✓ → Ec_IO pure ✓ → Production ✓ → Costs ✓ → FLGT ✓ (1D PASSED)
  → CR/NCF (next, when authorized) → RESULTS → full-system GTC → numerical parity → presentation
```
