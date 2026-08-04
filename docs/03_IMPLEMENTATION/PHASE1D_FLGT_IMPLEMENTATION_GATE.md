# Phase 1D — FLGT / Royalties Implementation Gate

**Status:** **READY FOR IMPLEMENTATION** (specification / gate only — no calculation code under this document)  
**Date:** 2026-08-04  
**Authority:** `docs/02_SPECIFICATIONS/modules/FLGT_ROYALTIES_CONTRACT.md`  
**Law table:** `docs/02_SPECIFICATIONS/modules/FISCAL_TERMS_PIA_LAW_TABLE.md`  
**Evidence:** `docs/workbook/semantic_mapping/FLGT_ROYALTIES_EVIDENCE_EXTRACT.json` · catalogue · GTC-001  
**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**GM modified:** **No**  
**Baseline commit (pre-FLGT):** `264618eae0607fd61680b84eebd9bf5abb791e5c`  

**Prerequisite gates:** Phase 1A CaseInput+Ec_IO pure **PASSED** · Phase 1B Production **PASSED** · Phase 1C Costs **IMPLEMENTED**  

**Do not reopen:** Equity INPUT · Fiscal LAW TABLE · AU14 expected · ADR-0010 · GM identity  

**Calculation code under this gate document:** **None**  
**Module stub remains:** `src/pems/calculations/modules/flgt_royalties.py` → `UnimplementedModule` only  

---

## 0. Purpose

Determine whether FLGT/Royalties may enter controlled calculation implementation without inventing formulas, re-hosting fiscal law, or bypassing upstream CaseInput/Production/Costs.

This document is the **implementation gate/plan**. Authorization to write FLGT code is a **separate** directive.

---

## 1. Scope

### In scope (Phase 1D implementation when authorized)

| Surface | Sheet | Role |
|---------|-------|------|
| Royalty rate engine | `Royalties` | Apply LAW_TABLE + CaseInput selectors to annual oil/gas/price rates |
| Price path (oil/gas) | `Royalties` / `FLGT` | Real → escalated nominal prices for revenue |
| Revenues | `FLGT` W/X/Y | Price × Production volumes ($mm) |
| Front-loaded government take | `FLGT` Z–AI | Oil/gas/price royalties $mm, rentals, HCDT, NDDC, bonuses, total |
| ERR | `FLGT` AM | AL/Y effective royalty rate |
| Hub mirrors | Ec_IO G11, G15 (and G8 revenue refs) | Downstream of FLGT — **not** CaseInput |

### Out of scope (deferred / other gates)

| Item | Disposition |
|------|-------------|
| CR Econ / HT / CIT / Project NCF engines | Phase CR/NCF |
| RESULTS KPI composition | Phase RESULTS |
| Full Ec_IO NCF KPI hub G3–G15 beyond FLGT-fed cells | After FLGT + NCF |
| Presentation / charts / formatting | After calc validation |
| Sensitivity Monte Carlo / multi-scenario UI | DEFERRED |
| Loan AN–AP (Equity Dash PPMT/IPMT) | Peripheral to base royalty — not core FLGT READY scope |
| Cost recovery / profit oil / HT-CIT dual tier application | CR/NCF, not FLGT core |

---

## 2. Source documents

| Document | Role |
|----------|------|
| `FLGT_ROYALTIES_CONTRACT.md` | Primary module contract (**READY**) |
| `FISCAL_TERMS_PIA_LAW_TABLE.md` | Authoritative law rates/tiers (**CLOSED**) |
| `EC_IO_PARAMETER_CONTRACT.md` | CaseInput selectors & prices |
| `PRODUCTION_PROFILE_CONTRACT.md` | Prod_Summary volumes/years |
| `COSTS_PARAMETER_CONTRACT.md` | HCDT/NDDC cost bases |
| GTC comparison framework | `docs/04_QUALITY/GTC_COMPARISON_FRAMEWORK.md` |
| Evidence extract | `FLGT_ROYALTIES_EVIDENCE_EXTRACT.json` |
| Active GM | SHA `D07560CA…BFEA` read-only |

---

## 3. FLGT input contract

### 3.1 CaseInput (selectors / drivers — already IMPLEMENTED)

| PEMS field | GM | Class | FLGT use |
|------------|-----|-------|----------|
| `terrain` | Ec_IO!G20 | CASE_ATTRIBUTE | Oil royalty terrain branch I/J/K/L |
| `gas_utilization` | Ec_IO!G21 | CASE_ATTRIBUTE | Gas royalty Dom 0.025 vs Out 0.05 |
| `oil_price_usd_bbl` | Ec_IO!C12 | ASSUMPTION | Real oil price path |
| `gas_price_usd_mscf` | Ec_IO!C17 | ASSUMPTION | Gas price path |
| `price_escalator` | Ec_IO!C14 | DEFAULT_STRUCTURAL | Nominal oil price escalation |
| `project_start_year` | Ec_IO!C5 | ASSUMPTION | Escalation exponent base |
| `history_year` / complete / E28 helpers | D28/D29/D22/E28 | ASSUMPTION / DERIVED | Price path edge years |
| `asset_analysis_type` | C4 | CASE_ATTRIBUTE | Indirect via Production/Costs history (upstream) |

**Not CaseInput:** Fiscal royalty rates, HCDT/NDDC %, rental tables, Analysis sensitivity cells.

### 3.2 Production outputs (IMPLEMENTED)

| Series | GM | Unit | Use |
|--------|-----|------|-----|
| Year | Prod_Summary!S* → Royalties A* / FLGT A8+ | year | Timeline |
| Daily oil | T* | mb/d | Oil royalty sliding bands; zero guards |
| Annual oil | U* | mmbbls | Oil revenue W = R×C |
| Daily gas | W* | mmscf/d | Gas rate zero guard |
| Annual gas | X* | bscf | Gas revenue X = U×F |
| Cum oil/gas | V*/Y* | mmbbls/bscf | Pass-through where formulas reference |

### 3.3 Costs outputs (IMPLEMENTED interfaces)

| Source | Use |
|--------|-----|
| Block_TC escalated OPEX / category bases (GB, FY–GA, ET, …) | HCDT Oil AF*, NDDC Oil AG* |
| Block_TC_Gas FX* | HCDT Gas Z* |
| Cap_Allow Gas FJ* | NDDC Gas AH* |

Import selected annual cost bases for GTC parity if full field recompute not yet wired into FLGT (same pattern as Costs selected path).

### 3.4 Sensitivity (not CaseInput)

| Cell | Role | Handling |
|------|------|----------|
| Analysis!$N$12 | Oil price sensitivity multiplier | Import as-saved for GTC; not primary CaseInput |
| Analysis!$N$15 | Escalator sensitivity | Same |
| Analysis!$N$13 | Gas price path | Same |

---

## 4. Fiscal-law interface

**Authoritative source:** `Fiscal Terms_PIA` sheet = **LAW_TABLE**.  
FLGT/Royalties **select and apply** only. Do **not** re-host or re-author rates.

| Law area | GM (as documented) | Consumer |
|----------|--------------------|----------|
| Oil royalty tiers by terrain | T18–W26 bands (Onshore/Shallow/Deep/Frontier) | Royalties I/J/K/L |
| Gas royalty Dom vs Out | U29–V30 (0.05 / 0.025) | Royalties N* |
| Price royalty bands | U36–U38 + 0.02 escalator notes | Royalties S* |
| HCDT | T72 = 0.03 | FLGT Z*, AF* |
| NDDC | T73 = 0.03 | FLGT AG*, AH* |
| Concession rentals | Z11/Z12 | FLGT AE* |
| Bonus tables | Law bonus blocks | FLGT AA* when triggered (GTC AA51=0) |
| Cost recovery / profit oil / HT-CIT | Law tables | **Not FLGT core** → CR/NCF |

**PEMS law load:** controlled reference-data load API (Fiscal Terms READY for load/read) — rates remain law identity bound to GM SHA.

---

## 5. Royalty / FLGT calculation groups

| Group ID | Purpose | Source sheet/range | Upstream | CaseInput | Fiscal-law | Logic summary | Output | Unit | Timing | GTC anchor | Downstream | Status |
|----------|---------|-------------------|----------|-----------|------------|---------------|--------|------|--------|------------|------------|--------|
| R-G1 | Volume/time spine | Royalties A–G | Production S–Y | — | — | Copy Prod_Summary | series | mb/d, mmbbls, mmscf/d, bscf | Annual | series | R-G2… | READY |
| R-G2 | Oil royalty rates | Royalties I/J/K/L | R-G1 daily oil B | terrain G20 | Oil tiers T18–W26 | Terrain branch + sliding average on B (mb/d); 0 if B=0 | rate series | fraction | Annual | J5=0.05 | FLGT AB | READY |
| R-G3 | Gas royalty rate | Royalties N | R-G1 E | gas_utilization G21 | U30/V30 | Dom 0.025 vs Out 0.05; 0 if E=0 | rate | fraction | Annual | N5=0.025 | FLGT AC | READY |
| R-G4 | Oil price path | Royalties P/Q/R | Ec_IO C12/C14/C5/D22 | prices, escalator | — | Real P; Q escalation; R=P×Q; Analysis N12/N15 | $/bbl | Annual | — | FLGT W | READY |
| R-G5 | Price royalty rate | Royalties S | R-G4 R | — | U36–U38 bands | 0 / interpolate / 10% vs escalated bands | rate | fraction | Annual | AD51=0 | FLGT AD | READY |
| F-G1 | FLGT timeline | FLGT A5–A* | Production | — | — | Lead A5–A7; A8=Prod_Summary!S5… | years | year | Annual | — | all F | READY |
| F-G2 | Rate map | FLGT I–N,S offset | Royalties rates | — | — | Offset map e.g. I8=Royalties!I5 | rates | fraction | Annual | — | F-G4 | READY |
| F-G3 | Revenues | FLGT W/X/Y | R-G4, gas price, volumes | C12/C17 | — | W=R×C oil; X=U×F gas; Y=W+X | $mm | Annual | W51/X51/Y51 | Ec_IO G8, NCF | READY |
| F-G4 | Oil royalty $mm | FLGT AB | F-G2, F-G3 W | terrain | oil rates | Terrain-selected rate × W | $mm | Annual | AB51 | AL, NCF | READY |
| F-G5 | Gas royalty $mm | FLGT AC | N rate, X | gas util | gas rates | N×X | $mm | Annual | AC51 | AL, NCF | READY |
| F-G6 | Price royalty $mm | FLGT AD | S rate, W | — | price bands | S×W | $mm | Annual | AD51=0 | AL | READY |
| F-G7 | Rentals | FLGT AE | Production flag B | — | Z11/Z12 | Rental when production | $mm | Annual | AE51 | AI | READY |
| F-G8 | HCDT oil/gas | FLGT Z, AF | Costs bases | — | T72=0.03 | × cost base with IF guards | $mm | Annual | Z51/AF51 | AI | READY |
| F-G9 | NDDC oil/gas | FLGT AG, AH | Costs / Cap_Allow Gas | — | T73=0.03 | × cost sum / FJ | $mm | Annual | AG51/AH51 | AI | READY |
| F-G10 | Bonuses | FLGT AA | Law triggers | — | bonus tables | Catalogue when non-zero | $mm | Annual | AA51=0 GTC | AI | READY |
| F-G11 | Totals / ERR | FLGT AI, AL, AM | F-G4…F-G10 | — | — | AI=SUM(Z:AH); AL=AB+AC+AD; AM=AL/Y (IFERROR 0) | $mm / fraction | Annual | AI51/AL51/AM51 | Ec_IO G11/G15 | READY |
| F-G12 | Loan AN–AP | FLGT AN–AP | Equity Dash | — | — | PPMT/IPMT peripheral | $mm | Annual | — | Equity path | DEFERRED (core) |

**No BLOCKED — SPECIFICATION GAP** for core royalty/FLGT groups above; full per-row formula text lives in catalogue (implementation uses catalogue + GM, not invention).

---

## 6. Units

| Stream | Convention (GM) |
|--------|-----------------|
| Oil volume daily / annual | mb/d · mmbbls |
| Gas volume daily / annual | mmscf/d · bscf |
| Oil price | $/bbl |
| Gas price | $/mscf |
| Royalty rates | fraction |
| Revenues / royalties / FLGT $ | **$mm** |
| ERR | fraction (AL/Y) |
| Law production bands | BOPD in law table; application uses mb/d with V*/1000 as in workbook |

**No new unit conventions.** Align with Production ($mm volumes as mmbbls/bscf) and Costs ($mm).

---

## 7. Timing

| Topic | Treatment |
|-------|-----------|
| Basis | **Annual** project years |
| Production align | FLGT A8+ = Prod_Summary S5…; Royalties A* = Prod_Summary S* |
| Lead years | FLGT A5–A7 pre-production calendar |
| Price escalation base | Ec_IO C5 project start year |
| History/forecast | Via upstream Production/Costs; price path uses D22/D29 edge rules |
| Fiscal year | As workbook annual spine — no separate invent fiscal calendar |
| Discounting | **Not** in FLGT core (discount is Costs Cap_Allow) |

---

## 8. Outputs and downstream consumers

| Output | GM | Consumer |
|--------|-----|----------|
| Oil/gas/price royalty $mm annual + AB51/AC51/AD51 | FLGT | AL, CR/NCF, RESULTS |
| ERR AM51 | FLGT | Ec_IO G11 |
| Total royalty AB+AC+AD | FLGT | Ec_IO G15 |
| Revenues W51/X51/Y51 | FLGT | Ec_IO G8 path, NCF |
| AI51 total front-loaded | FLGT | NCF / RESULTS paths |
| Rate series I/J/K/L/N/S | Royalties | FLGT only (rates not CaseInput) |
| Annual FLGT component series Z–AH | FLGT | CR Econ (~323 refs), HT/CIT/Project NCF |

---

## 9. GTC comparison points (minimum set)

| # | Sheet | Cell | Expected (as-saved GTC-001) | Tol | Error |
|---|-------|------|------------------------------|-----|-------|
| 1 | FLGT | AB51 | 61.3138177169515 | 1e-9 | — |
| 2 | FLGT | AC51 | 1.37587876051421 | 1e-9 | — |
| 3 | FLGT | AD51 | 0 | exact | — |
| 4 | FLGT | AL51 | 62.6896964774657 | 1e-9 | — |
| 5 | FLGT | AM51 | 0.0542803358903504 | 1e-9 | — |
| 6 | FLGT | W51 | 1099.88947281873 | 1e-9 | — |
| 7 | FLGT | X51 | 55.0351504205685 | 1e-9 | — |
| 8 | FLGT | Y51 | 1154.9246232393 | 1e-9 | — |
| 9 | FLGT | AI51 | 93.5101437605859 | 1e-9 | — |
| 10 | Ec_IO | G11 | 0.0542803358903504 | 1e-9 | — |
| 11 | Ec_IO | G15 | 62.6896964774657 | 1e-9 | — |
| 12 | Royalties | J5 | 0.05 | exact/tol | — |
| 13 | Royalties | N5 | 0.025 | exact/tol | — |

**Minimum comparison-point count:** **13** mandatory anchors (+ optional AE51/AF51/AG51/AH51/Z51 and annual series from `formula_cached_results_all.csv`).

**Do not rewrite expected values.** Source: `FLGT_ROYALTIES_CONTRACT.md` §10 + GTC-001 + GM cache.

Framework: reuse `pems.gtc.compare` (exact / 1e-9 / expected-error / mismatch).

---

## 10. Test plan (define only — do not implement in this gate)

### 10.1 For FLGT = IMPLEMENTED

| ID | Test area |
|----|-----------|
| T01 | Oil royalty rate terrain selection (Onshore/Shallow/Deep/Frontier) |
| T02 | Sliding oil rate vs daily production bands (incl. zero oil → 0) |
| T03 | Gas royalty Dom vs Out + zero gas |
| T04 | Oil price path real/nominal + escalator |
| T05 | Price royalty bands (incl. AD=0 case) |
| T06 | Revenues W/X/Y = price × volume |
| T07 | AB/AC/AD $mm application |
| T08 | Rentals / HCDT / NDDC with cost bases + IF guards |
| T09 | AL, AM (ERR), AI totals |
| T10 | Ec_IO G11/G15 hub mapping |
| T11 | Law-table load identity (rates match FR-equivalent law cells) |
| T12 | Analysis multipliers as-saved import (no invented CaseInput) |
| T13 | Deterministic repeatability |
| T14 | GTC §9 anchors via `pems.gtc.compare` |
| T15 | Regression: CaseInput, Ec_IO pure, Production, Costs still pass |

### 10.2 For FLGT = NUMERICALLY VALIDATED (separate, later)

- Full agreed annual series coverage (Royalties + FLGT), not only §9 totals  
- Documented residual classification  
- Explicit project-control validation approval  
- Still **not** full-system PEMS-vs-GM VALIDATED  

---

## 11. Deferred scope

| Item | Reason |
|------|--------|
| Presentation / formatting | Post calc validation |
| Sensitivity UI / Monte Carlo | Scope DEFERRED |
| Multi-scenario GTC expansion | Later |
| Loan AN–AP | Equity peripheral; not core royalty |
| Full bonus trigger matrix beyond catalogue | GTC AA51=0; implement when non-zero paths needed |
| CR/NCF / RESULTS engines | Separate gates |
| Production allowance fiscal paths outside royalty formulas | Other fiscal modules |

---

## 12. Ambiguities

| # | Location | Reason | Impact | Blocking? |
|---|----------|--------|--------|-----------|
| A1 | Every year-row formula body text | Contract cites groups; full text in catalogue | Implementation must use catalogue/GM formulas | **Non-blocking** (catalogue authority) |
| A2 | Analysis N12/N13/N15 semantics | Sensitivity not CaseInput | Import as-saved for GTC | **Non-blocking** |
| A3 | Bonus AA* trigger conditions | GTC sum 0; full law trigger matrix deep | Optional for base GTC | **Non-blocking** for core GTC |
| A4 | Loan AN–AP | Peripheral | Exclude from core IMPLEMENTED criteria | **Non-blocking** (deferred) |

**No calculation-critical unresolved ambiguity** that blocks READY FOR IMPLEMENTATION.

---

## 13. Readiness checklist

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Scope defined | **PASS** |
| 2 | Inputs mapped | **PASS** |
| 3 | CaseInput dependencies mapped | **PASS** |
| 4 | Production dependencies mapped | **PASS** |
| 5 | Costs dependencies mapped | **PASS** |
| 6 | Fiscal law interface defined | **PASS** |
| 7 | Royalty logic groups identified | **PASS** (R-G1…R-G5, F-G1…F-G11) |
| 8 | Units defined | **PASS** |
| 9 | Timing defined | **PASS** |
| 10 | Outputs defined | **PASS** |
| 11 | Downstream interfaces defined | **PASS** |
| 12 | GTC points identified | **PASS** (13+ anchors) |
| 13 | Test strategy defined | **PASS** §10 |
| 14 | Ambiguities documented | **PASS** §12 non-blocking |
| 15 | No unresolved calculation-critical specification gaps | **PASS** |

### Gate decision

# **FLGT / ROYALTIES = READY FOR IMPLEMENTATION**

---

## 14. IMPLEMENTED criteria (future code phase)

Promote FLGT to **IMPLEMENTED** only when:

1. R-G1…R-G5 and F-G1…F-G11 coded from GM/catalogue (F-G12 optional/deferred).  
2. Law table consumed, not duplicated.  
3. CaseInput / Production / Costs wired; single validation path.  
4. Units $mm / fractions / volumes correct.  
5. Unit tests T01–T13 pass.  
6. GTC §9 executed with **0 unexplained mismatches**.  
7. Prior suite (Phase 0–1C) still green.  
8. GM SHA MATCH; GM unmodified.  
9. Report `PHASE1D_FLGT_IMPLEMENTATION.md` written.  
10. Tracker/changelog updated.  

---

## 15. NUMERICALLY VALIDATED criteria (separate)

Do **not** claim from IMPLEMENTED alone. Requires broader series parity + formal validation approval.  

**Default:** `FLGT NUMERICALLY VALIDATED = NOT CLAIMED`

---

## 16. Explicit implementation boundary

| Do | Do not |
|----|--------|
| Apply LAW_TABLE rates via selectors | Re-author PIA rates as CaseInput |
| Use Production volumes and Costs bases | Invent volumes/costs |
| Implement ERR and royalty $mm | Implement full HT/CIT/CR engines |
| Feed Ec_IO G11/G15 | Treat Ec_IO FLGT hubs as inputs |
| GTC against contract expected | Rewrite GTC expected values |
| Catalogue for full formula text | Invent petroleum “improvements” |

---

## 17. Control state (after this readiness task)

```text
CaseInput      IMPLEMENTED
Ec_IO pure     IMPLEMENTED
Production     IMPLEMENTED
Costs          IMPLEMENTED
FLGT           READY FOR IMPLEMENTATION (code NOT STARTED)
CR/NCF         NOT IMPLEMENTED
RESULTS        NOT IMPLEMENTED
Presentation   DEFERRED
```

**Next command required:** separate authorization to implement Phase 1D FLGT calculation code.
