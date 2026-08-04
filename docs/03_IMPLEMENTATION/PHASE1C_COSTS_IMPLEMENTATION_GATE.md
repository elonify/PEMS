# Phase 1C — Costs Implementation Gate / Plan

**Status:** **EXECUTED — see PHASE1C_COSTS_IMPLEMENTATION.md** (this plan remains the gate definition)  
**Date:** 2026-08-04  
**Authority:** `docs/02_SPECIFICATIONS/modules/COSTS_PARAMETER_CONTRACT.md`  
**Companion evidence:** `docs/workbook/catalogue/` · `COSTS_EVIDENCE_EXTRACT.json` · GTC-001  
**Active GM SHA (approved, independent of this plan):**  
`D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**GM modified:** **No**  
**Calculation code under this document:** **None**

**Prerequisite gates:** Phase 1A (CaseInput + Ec_IO pure) **PASSED** · Phase 1B (Production G1–G5) **PASSED**

**Do not reopen:** Equity INPUT · Fiscal LAW TABLE · AU14 expected · ADR-0010 · GM identity

---

## 0. Contract readiness confirmation

| Check | Result |
|-------|--------|
| Costs contract path | `docs/02_SPECIFICATIONS/modules/COSTS_PARAMETER_CONTRACT.md` |
| Contract status | **READY** (spec only — not numerical VALIDATED) |
| Contract SHA binding | **Same active GM SHA** `D07560CA…BFEA` |
| SHA-independent of workbook modification | **Yes** — plan references approved GM only; no re-freeze |
| Visible implementation sheets | `Block_TC` · `Block_TC_Gas` · `Cap_Allow` · `Cap_Allow Gas` |
| Upstream | CaseInput (Ec_IO) **IMPLEMENTED**; Production years/volumes **IMPLEMENTED** |
| Downstream not in Phase 1C full engines | FLGT · CR/NCF · RESULTS (interfaces only) |

**Costs specification remains READY. Phase 1C may proceed only after this plan is used as the implementation gate.**

---

## 1. CaseInput / upstream inputs (exact)

### 1.1 Already on CaseInput (wire only — no second input system)

| PEMS field | GM | Costs use |
|------------|-----|-----------|
| `hurdle_rate` | Ec_IO!C15 | Discount FK*, FL* |
| `duties_rate` | Ec_IO!C20 | Cap_Allow FN* |
| `vat_rate` | Ec_IO!C21 | Cap_Allow FO* |
| `block_field_oil` / `block_field_gas` | G18 / G19 | Field selection |
| cost mode field | Ec_IO!G23 (= G18 on GM) | High-ref field/mode select |
| `asset_analysis_type` | Ec_IO!C4 | History window |
| `history_year` (+ E28 via Ec_IO pure) | D28 / E28 | Timeline filters |
| `project_start_year` | Ec_IO!C5 | Year / discount base alignment |
| `project_life_years` | Ec_IO!C6 ← Prod_Summary!AF26 | Horizon (from Production) |
| `production_days_per_year` | Ec_IO!C7 | Indirect via production upstream |

**Not Costs CaseInput:** royalty law rates; equity share (scales RESULTS only).

### 1.2 Cost schedule inputs (import path for GTC parity)

| Concept | GM | Class | Phase 1C approach |
|---------|-----|-------|-------------------|
| Year spine | Block_TC!A* / Cap_Allow!FE* ← Prod_Summary!S* | ASSUMPTION / DERIVED | Import or derive from Production years |
| Oil TC by category×year (selected field) | Block_TC 5-col blocks | ASSUMPTION / schedule | Import selected field: Exploration, CAPEX Wells, CAPEX Facilities, OPEX, Abandonment ($mm) |
| Gas TC counterparts | Block_TC_Gas | same | Parallel import |
| Escalated OPEX series | Block_TC!GB* (History-aware) | DERIVED / schedule | Import selected escalated OPEX **or** recompute only if formulas fully wired from catalogue |
| Fixed / Vopex coeffs | Block_TC row 49–50 | FORMULA_COEFFICIENT | Import coefficients if needed for recomputation |
| CA rates Y1–Y5 | Cap_Allow!FR5:FR9 | ASSUMPTION / LAW-aligned | 0.2, 0.2, 0.2, 0.2, 0.19 — prefer LAW_TABLE identity |

**v1 rule (contract §4.2):**  
(1) Import Block_TC / Cap_Allow schedules for GTC parity;  
(2) Selected-field consolidated path Cap_Allow FE–FQ / FI–FL.  
Full multi-field GUI = **later**.

### 1.3 Manual path

Same `CaseInput` (+ cost schedule structures) as import. **Single validation path.**

---

## 2. Formula / logic groups (implement in order)

| Group | Purpose | GM evidence | Phase 1C priority |
|-------|---------|-------------|-------------------|
| **G1** | Multi-field TC schedule oil/gas ($mm/yr categories) | Block_TC / Block_TC_Gas | Import + structure; not full multi-field editor |
| **G2** | Field / mode selection | Ec_IO G23/G18/G19 IF chains | Selected-field path (match Production pattern) |
| **G3** | Undiscounted aggregation | FI, FF–FH, FP, FQ | **Core** |
| **G4** | Discounting at hurdle | `FK=(FF+FG+FH)/(1+r)^(FE−FE5)`; `FL=FI/(1+r)^(…)` | **Core** |
| **G5** | Capital allowance rates application | FR5:FR9 + CA columns | Rates + surface; full CA body from catalogue as needed for GTC |
| **G6** | Hub export Ec_IO N16–S18 | Oil+gas combined | **Core GTC** — first completion of deferred Ec_IO **cost** hub only |
| **G7** | Escalated OPEX path | Block_TC GB* History filter | Required if FI uses GB (GTC oil path) |
| **G8** | SLN / Acquisition allowance | GX, HC | Implement if required for Costs GTC set; else classify as interface deferred to CR/NCF if no GTC point in §10 |

**Oil and gas remain parallel stacks — do not merge without stream tags.**

---

## 3. Units and scaling

| Rule | Evidence |
|------|----------|
| Category units | **$mm** throughout Block_TC / Cap_Allow |
| Time basis | **Annual** calendar years (A / FE) |
| Discount | Hurdle `hurdle_rate` (fraction/yr); year 0 factor = 1 when `(FE−$FE$5)=0` |
| Discount base year | First year of Cap_Allow FE block (`$FE$5`) |
| Escalation | Escalated OPEX path (G7) — **not** inventing generic inflation CaseInput |
| Price escalator C14 | Revenue path — **not** proven as Block_TC $mm escalator |
| Equity | Does **not** scale Block_TC |

---

## 4. GM comparison cells and GTC-001 expected values

### 4.1 Cap_Allow oil totals (mandatory)

| Point | Cell | Expected (as-saved) |
|-------|------|---------------------|
| OPEX undisc | Cap_Allow!FI48 | **361.503330356603** |
| OPEX disc | Cap_Allow!FL48 | **185.584322008296** |
| CAPEX disc | Cap_Allow!FK48 | **142.902934166187** |
| Expensed CAPEX sum | Cap_Allow!FP48 | **35** |
| CAPEX+Duties/VAT roll | Cap_Allow!FQ48 | **140** |
| CA rates | Cap_Allow!FR5:FR9 | **0.2, 0.2, 0.2, 0.2, 0.19** |

### 4.2 Cap_Allow Gas totals (mandatory)

| Point | Cell | Expected |
|-------|------|----------|
| OPEX undisc | Cap_Allow Gas!FI48 | **56.7** |
| OPEX disc | Cap_Allow Gas!FL48 | **25.4185178187494** |
| CAPEX disc | Cap_Allow Gas!FK48 | **0** |

### 4.3 Ec_IO cost hub (mandatory — completes deferred cost hub N16–S18 only)

| Point | Cell | Expected | Formula (GM) |
|-------|------|----------|--------------|
| PV OPEX | Ec_IO!N16 | **211.002839827046** | Cap_Allow!FL48 + Gas!FL48 |
| Undisc OPEX | Ec_IO!S16 | **418.203330356603** | FI48 + Gas!FI48 |
| PV CAPEX | Ec_IO!N17 | **142.902934166187** | FK48 + Gas!FK48 |
| Undisc CAPEX | Ec_IO!S17 | **175** | FP+FQ oil+gas (as GM) |
| PV TC | Ec_IO!N18 | **353.905773993233** | N16+N17 |
| Undisc TC | Ec_IO!S18 | **593.203330356603** | S16+S17 |

### 4.4 Optional intermediate samples (recommended)

- Cap_Allow FE5 / FI5 / FK5 / FL5 first production-aligned year  
- Selected Block_TC category cells for Ebiya (or active field) for one CAPEX and one OPEX year  
- Source: `formula_cached_results_all.csv` / GM `data_only` cache  

**Do not change expected GTC values to force pass.**

**Minimum comparison set for gate:** §4.1 + §4.2 + §4.3 = **oil 5 totals + 5 CA rates + gas 3 + Ec_IO 6 ≈ 19+ points** (exact count after cell_map finalization).

---

## 5. Upstream / downstream interfaces

### Upstream (required before/with Costs)

```text
CaseInput (hurdle, duties, VAT, fields, history, start year)
Production (year spine FE ← S*; life; volumes if Vopex formulas require)
Fiscal Terms_PIA LAW TABLE (CA rate identity only — load/read, not fiscal engine)
```

### Downstream (expose, do not implement engines)

| Output | Consumers (later gates) |
|--------|-------------------------|
| FI / FP / FQ annual series | CR Econ, HT_NCF |
| FK / FL totals and series | Ec_IO hub, RESULTS unit costs |
| GX SLN / HC Acquisition | CR Econ, HT_NCF |
| Block_TC category streams | FLGT (~135 refs) |
| Ec_IO N16–S18 | Display hub / RESULTS paths |

**Phase 1C does not implement:** FLGT take algorithms, CR profit-oil rules, HT/CIT rate law, RESULTS KPI composition, royalty engines.

---

## 6. Explicitly deferred (Phase 1C)

| Item | Handling |
|------|----------|
| Full multi-field cost GUI | Import + selected-field only |
| Transport / processing cost categories | **Not evidenced** — excluded |
| Generic inflation CaseInput | **Not evidenced** — excluded |
| Production G6 / presentation formatting | Still deferred |
| Ec_IO KPI hub G3–G15 (NCF/FLGT KPIs) | Still deferred (not cost hub) |
| Ec_IO revenue hub P16–P18 | Still deferred (FLGT) |
| Full CA / SLN / HC every array formula | Catalogue-driven; implement only as needed for GTC + CR hand-off surface |
| CR/NCF, FLGT, RESULTS calculation engines | Separate gates |

Do not invent formulas to “finish” deferred items.

---

## 7. Implementation architecture (controlled)

```text
CaseInput (+ cost schedule series on CaseInput or CostsInputs attached to same validation path)
        │
        ▼
CostsModule.run(case, upstream={production, fiscal_ca_rates?})
        │
        ├─ G1/G2: selected oil/gas TC schedules ($mm)
        ├─ G7: escalated OPEX if FI path requires
        ├─ G3: undisc FI, FF–FH, FP, FQ (+ FN/FO from duties/VAT rules as GM)
        ├─ G4: disc FK, FL series + row-48 totals
        ├─ G5: CA rates FR (+ application columns if GTC needs)
        ├─ G8: GX/HC if in comparison set
        └─ G6: Ec_IO N16–S18 combined hubs
        │
        ▼
CostsResult.cell_map() → GTC compare (reuse pems.gtc.compare)
```

**Patterns from Phase 1A/1B to reuse:**

- Single CaseInput representation  
- Provenance map for new fields  
- Excel import read-only (`data_only`, no workbook write)  
- `compare_cell_map` exact / 1e-9 / expected-error  
- Unit tests + `tests/validation/test_costs_gtc.py`  
- Report `PHASE1C_COSTS_IMPLEMENTATION.md` at completion  

---

## 8. Test suite definition

### 8.1 Unit tests (`tests/unit/test_costs.py`)

| Area | Assertions |
|------|------------|
| Discounting G4 | Year-0 PV factor 1; multi-year PV matches formula |
| Aggregation G3 | FI/FK/FL/FP/FQ series sums |
| Oil vs gas separation | Parallel stacks not cross-contaminated |
| Field selection | Selected field feeds consolidated path |
| History filter | Escalated OPEX / filters when C4=History |
| Zero costs | Blank/zero years → zero contribution |
| CA rates | FR5:FR9 identity |
| Hub G6 | N16=FL48_oil+FL48_gas etc. |
| Duties/VAT linkage | FN/FO use CaseInput rates only as GM requires |
| No equity scaling | Equity does not alter Block_TC |

### 8.2 GTC tests (`tests/validation/test_costs_gtc.py`)

| Test | Purpose |
|------|---------|
| GM SHA MATCH | `D07560CA…BFEA` |
| Import schedules from active GM | Selected field TC + Cap_Allow drivers |
| Compare §4.1–§4.3 cell_map | exact / tolerance / mismatch report |
| Prior suite still green | Phase 0 + 1A + 1B regression |

### 8.3 Determinism

- No wall-clock randomness  
- Stable serialization of schedules  
- Float compare via existing GTC framework (abs/rel 1e-9)

---

## 9. GTC comparison harness

Reuse `pems.gtc.compare`:

1. Import CaseInput + cost schedules from active GM (read-only).  
2. Run `CostsModule` (+ Production upstream if year spine required).  
3. Build `cell_map` for §4 cells.  
4. Load expected from `literal_values_all.csv` / `formula_cached_results_all.csv` / GM `data_only`.  
5. Report: total points, exact, tolerance, mismatch, expected_error_ok, unresolved.  
6. On mismatch: **TRACE → DIAGNOSE → CLASSIFY → CORRECT** (or stop for ambiguity).  
7. **Never** rewrite expected GTC values to pass.

---

## 10. Criteria: Costs = IMPLEMENTED

Promote Costs to **IMPLEMENTED** only when **all** of the following hold:

1. Contract groups in Phase 1C scope (G1 selected-path, G2, G3, G4, G6 mandatory; G5 rates; G7 if FI path needs; G8 if in GTC set) are coded from GM formulas/catalogue.  
2. All required CaseInput / schedule inputs wired; single validation path.  
3. Oil and gas stacks distinct; units $mm; discount timing correct.  
4. Unit tests for §8.1 pass.  
5. GTC comparison for §4.1–§4.3 executed with **0 unexplained mismatches**.  
6. Prior Phase 0/1A/1B tests still pass.  
7. Discrepancies resolved or formally classified (deferred vs ambiguity).  
8. No unsupported invented categories (no transport/processing; no generic inflation).  
9. Implementation report written (`PHASE1C_COSTS_IMPLEMENTATION.md`).  
10. Tracker / changelog / readiness updated.  
11. GM SHA still MATCH; GM not modified.

---

## 11. Criteria: Costs = NUMERICALLY VALIDATED (future — separate)

**Do not claim VALIDATED** from IMPLEMENTED alone.

Future **VALIDATED** would require (minimum):

- Full agreed Cap_Allow / Block_TC comparison coverage (not only row-48 hubs)  
- Series-level parity where consumers need annual FI/FP/FK/FL  
- Documented classification of any residual #REF!/empty cache cells  
- Explicit project-control approval of validation evidence  
- Still **not** the same as full-system PEMS-vs-GM VALIDATED

Until then:

| Claim | Status |
|-------|--------|
| Costs IMPLEMENTED | Eligible after §10 |
| Costs NUMERICALLY VALIDATED | **NOT CLAIMED** by default |
| PEMS-vs-GM FULL-SYSTEM VALIDATION | **NOT CLAIMED** |

---

## 12. Discipline (mandatory)

- Do **not** modify the approved Golden Master.  
- Do **not** alter the active GM SHA.  
- Do **not** reopen closed domain decisions.  
- Do **not** claim parity from partial GTC coverage beyond stated subset.  
- Do **not** substitute presentation work for calculation validation.  
- Do **not** invent missing workbook behavior.  
- Preserve provenance: GM cell → CaseInput/engine → output → GTC point.  
- Maintain deterministic tests.

---

## 13. Authorization state after this plan

| Item | State |
|------|-------|
| Phase 1B Production | **PASSED / IMPLEMENTED** (ack recorded) |
| Phase 1C Costs plan | **READY** |
| Phase 1C Costs calculation code | **NOT STARTED** (this document only) |
| Next action | Begin Costs implementation **only** when authorized to execute Phase 1C against this gate |

---

## 14. Traceability (plan level)

```text
COSTS_PARAMETER_CONTRACT.md (§1–10)
  → CaseInput fields (§1)
  → Logic groups G1–G8 (§2)
  → GM cells + GTC expected (§4)
  → Interfaces (§5)
  → Deferred (§6)
  → Tests + harness (§8–9)
  → IMPLEMENTED vs VALIDATED criteria (§10–11)
  → Active GM SHA D07560CA…BFEA (read-only)
```
