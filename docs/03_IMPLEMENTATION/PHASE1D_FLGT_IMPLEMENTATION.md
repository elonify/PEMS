# Phase 1D — FLGT / Royalties Implementation Report

**Date:** 2026-08-04  
**Gate:** `docs/03_IMPLEMENTATION/PHASE1D_FLGT_IMPLEMENTATION_GATE.md`  
**Gate status:** **PASSED / ACKNOWLEDGED** — see `PHASE1D_GATE_ACKNOWLEDGEMENT.md`  
**Authority:** `docs/02_SPECIFICATIONS/modules/FLGT_ROYALTIES_CONTRACT.md`  
**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**GM modified:** **No**  
**GTC case:** GTC-001  

---

## 1. Implementation status

| Claim | Value |
|-------|--------|
| FLGT / Royalties **IMPLEMENTED** | **YES** (R-G1…R-G5, F-G1…F-G11) |
| FLGT GTC subset | **PASS** |
| FLGT **NUMERICALLY VALIDATED** | **NOT CLAIMED** |
| PEMS-vs-GM FULL-SYSTEM VALIDATION | **NOT CLAIMED** |
| Ec_IO FULL VALIDATION | **NOT CLAIMED** |

---

## 2–3. Groups R-G1…R-G5 and F-G1…F-G11

| Group | Status |
|-------|--------|
| R-G1 Volume/time spine | **IMPLEMENTED** |
| R-G2 Oil rates I/J/K/L sliding + terrain | **IMPLEMENTED** |
| R-G3 Gas rate Dom/Out | **IMPLEMENTED** |
| R-G4 Oil price path P/Q/R | **IMPLEMENTED** |
| R-G5 Price royalty S | **IMPLEMENTED** |
| F-G1/F-G2 Timeline + rate map | **IMPLEMENTED** (in-module years + rates) |
| F-G3 Revenues W/X/Y | **IMPLEMENTED** |
| F-G4…F-G6 AB/AC/AD $mm | **IMPLEMENTED** |
| F-G7 Rentals AE | **IMPLEMENTED** |
| F-G8 HCDT Z/AF | **IMPLEMENTED** (lag opex × law rate) |
| F-G9 NDDC AG/AH | **IMPLEMENTED** |
| F-G10 Bonuses AA | **IMPLEMENTED** (core GTC path = 0) |
| F-G11 AI / AL / ERR AM | **IMPLEMENTED** |
| F-G12 Loan AN–AP | **DEFERRED** |

Code: `src/pems/calculations/modules/flgt_royalties.py`

---

## 4. Inputs and upstream interfaces

- **CaseInput:** terrain, gas_utilization, oil/gas prices, escalator, start year, life, block production series, Cap_Allow cost series, Analysis N12/N13/N15 and D22/D29 via `extras`
- **Production:** `ProductionModule` series via `upstream={"production": …}`
- **Costs:** oil/gas TC category series already on CaseInput from Cap_Allow import
- **Single validation path** retained (no second input system)

---

## 5. Fiscal-law interface

- `FiscalLawParams` holds LAW_TABLE rates (tiers, gas Dom/Out, HCDT/NDDC, rentals, price bands)
- Import loads key cells from `Fiscal Terms_PIA` into `case.extras["fiscal_law"]` (not CaseInput scenario fields)
- Defaults match GM GTC when law not supplied
- **Does not re-host** as ordinary CaseInput parameters

---

## 6. Units and timing

| Item | Convention |
|------|------------|
| Oil | mb/d, mmbbls, $/bbl, $mm |
| Gas | mmscf/d, bscf, $/mscf, $mm |
| Rates / ERR | fraction |
| Time | Annual production spine; no FLGT discounting |

---

## 7. Outputs / consumers

| Output | Consumer |
|--------|----------|
| AB/AC/AD, AL, AM | Ec_IO G11/G15, CR/NCF, RESULTS (later) |
| W/X/Y | Ec_IO revenue hub path, NCF |
| AI, Z, AE–AH | NCF / RESULTS paths |
| J5/N5 sample rates | Rate-engine GTC |

---

## 8–12. GTC comparison

| Metric | Count |
|--------|------:|
| Comparison points (mandatory + optional) | **18** |
| Exact | **4** |
| Tolerance 1e-9 | **14** |
| Mismatch | **0** |
| Unresolved | **0** |

Mandatory anchors: J5, N5, W51, X51, Y51, AB51, AC51, AD51, AI51, AL51, AM51, Ec_IO G11, G15.  
Optional: Z51, AE51, AF51, AG51, AH51.

Framework: `pems.gtc.compare` — expected values from contract/gate, **not rewritten**.

---

## 13–14. Tests

| Suite | Result |
|-------|--------|
| FLGT unit | **12 passed** |
| FLGT GTC | **3 passed** |
| Full regression | **70 passed / 0 failed** |

---

## 15. Deferred items

F-G12 loan · full bonus matrix · presentation · sensitivity UI · Monte Carlo · multi-scenario GTC · CR/NCF · RESULTS · full-system VALIDATED

---

## 16. Non-blocking ambiguities

- Full per-row catalogue formula text used via group implementation  
- HCDT lag uses Cap_Allow year-keyed opex (matches GTC)  
- Deep terrain labels partial-match  

---

## 17–18. GM integrity

| Check | Result |
|-------|--------|
| Expected SHA | `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA` |
| Actual | **MATCH** (pre- and post-implementation) |
| GM modified | **NO** |

---

## 19. Claims discipline

| Claim | Status |
|-------|--------|
| **FLGT = IMPLEMENTED** | **YES** |
| **FLGT GTC SUBSET = PASS** | **YES** |
| **FLGT NUMERICALLY VALIDATED** | **NOT CLAIMED** |

---

## 20. Next gate

**PHASE 1D FLGT IMPLEMENTATION → formal GTC gate acknowledgement**  

Then (separate authorization): **CR/NCF readiness/implementation**.  

Do **not** auto-start CR/NCF.
