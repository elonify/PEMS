# Phase 1H — Chart Presentation Project Handoff

## Purpose

This document is the canonical continuation brief and compact project-memory artifact for migrating the Phase 1H chart implementation work into a new conversation without carrying the full historical chat.

The project is a presentation-layer chart dataset/building effort for the PEMS workbook/application. The central architectural rule is:

> Chart builders are presentation-only projections of authoritative DTO outputs. They must not invent, recalculate, aggregate, discount, recumulate, or otherwise recreate economics that belong in the calculation/model layer.

**Canonical path:** `docs/phase1h/PHASE1H_CHAT_HANDOFF.md`

---

## 1. Current project status

### Baseline commit

| Item | Value |
|------|--------|
| **HEAD / baseline** | **`6c2b41d`** |
| Message | `docs(phase1h): enrich Equity DNCF ticket with exact GM formulas` |
| Key stack | `0a6d456` → `19b4ca8` → `dc361e3` → `09a2ded` → `8518056` → equity ticket `2a14d76`/`6c2b41d` |
| Branch | `master` (local) |
| Push / tag | **not done** |

### Overall assessment

Approximate overall progress: **~8.5–8.7 / 10**.

**Six** chart families are implemented and audit-authorized: the original five plus **PRODUCTION_PROFILE** (oil & AG). Calc-layer `pp_cum_by_year` / `pp_ag_cum_by_year` landed (`dc361e3`); audit Production Profile YES (`09a2ded`); presentation `production_profile_dataset` committed (`8518056`). **`PresentationBundle.chart_datasets`** includes those datasets (9 IDs). Equity CashFlow is fully diagnosed with GM AH/AI formulas and a Medium design ticket — **calc not implemented**. Plot rendering still deferred.

### Current strengths

- Workbook chart inventory and semantic evidence investigated.
- 40-chart audit universe classified.
- Six chart families with presentation builders + DTO maps.
- Builders are projection-only; PP cum computed only in the **calculation** module.
- Unit coverage: chart datasets + production + presentation PT11 (9 chart IDs).
- Verification baseline:
  - **59 passed** (chart + presentation suite after profile builder)
  - **1 pre-existing unregistered `@pytest.mark.slow` warning**
- Chart **data** on presentation bundle; plot **UI** not started.
- Workbook parity has **not** been claimed as fully validated.
- Product scope: `docs/pems/PEMS_PRODUCT_SCOPE.md`.
### Important distinction

Keep these states separate:

> **Implemented** ≠ **Audit-authorized** ≠ **Workbook-parity validated**

Passing tests does not prove workbook parity. Commit does not claim full 40-chart coverage.

---

## 2. Authority and governance

### Primary audit authority

```text
docs/workbook/semantic_mapping/CHART_MAPPING_AUDIT.csv
```

Sole authority for chart semantic mapping and `implementation_authorized`.

Do not substitute code/tests for audit authorization.

### PO authorization

PO: **Dr Emmanuel Onwuka**.

Explicitly authorized Phase 1H chart families (see §6): original five plus Production Profile (after PP cum DTOs).

### Current audit counts

| Field | Count |
|-------|------:|
| Total chart rows | 40 |
| `implementation_authorized = YES` | **14** |
| `implementation_authorized = NO` | **26** |
| `mapping_status = REVIEW_REQUIRED` | **25** (includes authorized rows; status field not flipped) |
| `mapping_status = DEFERRED` | **15** (Analysis) |

### Authorized audit rows (14)

| Worksheet | Idx | Template | Family |
|-----------|-----|----------|--------|
| Ec_IO | 1 | ECONOMIC_LIMIT | ECONOMIC_LIMIT |
| Ec_IO | 2–3 | PRODUCTION_SUMMARY | PRODUCTION_SUMMARY oil/gas |
| Ec_IO | 4–5 | COST_PROFILE | COST_PROFILE oil/gas |
| Ec_IO | 6 | DISCOUNTED_NCF | PROJECT_DISCOUNTED_NCF |
| Prod_Summary | 2–3 | PRODUCTION_SUMMARY | PRODUCTION_SUMMARY oil/gas |
| Block_TC / Block_TC_Gas | 1 | COST_PROFILE | COST_PROFILE oil/gas |
| FLGT | 1 | FLGT_TAKE | FLGT_TAKE |
| Project_NCF | 1 | DISCOUNTED_NCF | PROJECT_DISCOUNTED_NCF |
| **Production Profile** | **1–2** | PENDING_SEMANTIC_MAP | **PRODUCTION_PROFILE** oil / AG |

**Not authorized:** Prod_Summary chart #1 (col C), Equity_NCF_Con, STOIIP/GIIP, OML123, all Analysis.

---

## 3. Architectural rules

### Presentation-only projection

Chart builders may:

- select an authoritative DTO map;
- select a year/key spine;
- align multiple existing year-keyed maps;
- emit `None` where a requested year is absent;
- preserve exact source float values;
- select the appropriate chart template and dataset ID;
- reject invalid stream arguments where applicable.

Chart builders must not:

- recalculate economics;
- discount cash flows;
- compute cumulative values from annual values when the required cumulative DTO is absent;
- sum or aggregate source maps to manufacture a chart series;
- recreate Excel formulas;
- perform Excel I/O;
- import/use `openpyxl`, `xlsx`, `xlrd`, NumPy, etc. for chart building;
- modify calculation modules unless a separately authorized model/DTO change is required;
- scale project economics to manufacture missing equity economics;
- infer scenario series without an authoritative scenario DTO.

### DTO authority

If the workbook chart requires a series that is not represented faithfully by an authoritative DTO field/map, stop and escalate that dependency.

Do not “make the chart work” by doing calculation work in presentation code.

---

## 4. Current package structure

```text
src/pems/presentation/charts/
    __init__.py
    datasets.py
    templates.py

tests/unit/test_chart_datasets.py

src/pems/presentation/__init__.py   # re-exports charts package
```

### Package surface

`charts/__init__.py` exports all builders, `ChartDataset`, `ChartSeries`, templates.

`datasets.py`: frozen `ChartSeries` / `ChartDataset` + builders (incl. `production_profile_dataset`).

`templates.py`: includes `PRODUCTION_PROFILE` and `EQUITY_CASHFLOW` placeholder (no equity builder yet).

`view_models.build_presentation` → `build_authorized_chart_datasets` → `chart_datasets`. PySide6 UI still **tables only**.

---

## 5. Current Git state

### Baseline stack (through `6c2b41d`)

| Commit | Content |
|--------|---------|
| `0a6d456` | Five ChartDataset builders + first audit YES (12 rows) |
| `19b4ca8` | `PresentationBundle.chart_datasets` wiring |
| **`dc361e3`** | **`pp_cum_by_year` / `pp_ag_cum_by_year` on ProductionResult** |
| **`09a2ded`** | **Audit YES for Production Profile rows (14 total YES)** |
| **`8518056`** | **`production_profile_dataset` (oil & gas)** |
| `2a14d76` / **`6c2b41d`** | Equity DNCF design ticket (+ GM AH/AI formulas) |

### Presentation wiring

```text
PresentationBundle.chart_datasets: dict[str, ChartDataset]
```

Official IDs (**9**):  
`PROJECT_DISCOUNTED_NCF`, `ECONOMIC_LIMIT`,  
`OIL_PRODUCTION_SUMMARY`, `GAS_PRODUCTION_SUMMARY`,  
`OIL_PRODUCTION_PROFILE`, `GAS_PRODUCTION_PROFILE`,  
`OIL_COST_PROFILE`, `GAS_COST_PROFILE`, `FLGT_TAKE`.

### PP cumulative (done in calc)

- Maps: `ProductionResult.pp_cum_by_year`, `pp_ag_cum_by_year`  
- GM: `IF(E=0,0,SUM(E first..n))` / same for H → I  
- Ticket: `docs/phase1h/TICKET_PP_CUMULATIVE_MAPS.md` (implemented)

### Equity DNCF (design only)

- Ticket: `docs/phase1h/TICKET_EQUITY_DNCF_MAPS.md`  
- AH/AI formulas recorded; Medium (upstream equity AF); **no code yet**

### Verification baseline

```text
pytest tests/unit/test_chart_datasets.py tests/unit/test_presentation.py -q
59 passed, 1 pre-existing @pytest.mark.slow warning
```

---

## 6. Completed chart families (implemented + authorized + committed)

Six families: DISCOUNTED_NCF, ECONOMIC_LIMIT, COST_PROFILE, FLGT_TAKE, PRODUCTION_SUMMARY, **PRODUCTION_PROFILE**.

## 6.1 PROJECT_DISCOUNTED_NCF

```python
discounted_ncf_dataset(cr_ncf)  # → PROJECT_DISCOUNTED_NCF
```

DTO `CrNcfResult`: `years`, `disc_contractor_ah`, `disc_cncf_ai`. Projection only.

Audit: Ec_IO 6, Project_NCF 1.

---

## 6.2 ECONOMIC_LIMIT

```python
economic_limit_dataset(cr_ncf, production)  # → ECONOMIC_LIMIT
```

| Series | DTO |
|--------|-----|
| Cum_DNCF | `cr_ncf.disc_cncf_ai` |
| Annual_DNCF | `cr_ncf.disc_contractor_ah` |
| Rates_Oil | `production.oil_daily_series` |
| x | `cr_ncf.years` |

Audit: Ec_IO 1.

---

## 6.3 COST_PROFILE

```python
cost_profile_dataset(costs, stream)  # stream in {"oil","gas"}
# → OIL_COST_PROFILE | GAS_COST_PROFILE
```

Undiscounted only: `exploration`, `capex_wells`, `capex_facilities`, `opex` on `costs.oil` / `costs.gas`. Invalid stream → `ValueError`. No `disc_capex` / `disc_opex`.

Audit: Ec_IO 4–5, Block_TC 1, Block_TC_Gas 1.

---

## 6.4 FLGT_TAKE

```python
flgt_take_dataset(flgt)  # → FLGT_TAKE
```

### Decision (evidence-backed): keep **7-series** builder

Authoritative evidence (`chart23.xml`, inventory clean, audit formulas):

- Categories: FLGT col **A**
- Series values: **AA, AB, AC, AD, AE, AF, AG only**

| Key | Label | Col |
|-----|-------|-----|
| bonuses | Bonuses | AA |
| oil_royalty_mm | Oil royalty | AB |
| gas_royalty_mm | Gas royalty | AC |
| price_royalty_mm | Price royalty | AD |
| rentals | Rentals | AE |
| hcdt_oil | HCDT oil | AF |
| nddc_oil | NDDC oil | AG |

**Excluded by chart evidence (do not add without new authorization):**

- `hcdt_gas` (DTO col Z)
- `nddc_gas` (DTO col AH)
- `flgt_total`, revenues, ERR, `royalty_sum`

FlgtResult still has `hcdt_gas` / `nddc_gas` maps for calc/totals use; they are **not** chart23 series.

Audit: FLGT 1 only.

---

## 6.5 PRODUCTION_SUMMARY

```python
production_summary_dataset(production, stream)  # oil | gas
```

Oil order: annual → cum → rate (`oil_annual_series`, `oil_cum_series`, `oil_daily_series`).  
Gas order: cum → annual → rate (`gas_cum_series`, `gas_annual_series`, `gas_daily_series`).  
x = sorted union of the three map keys. No re-cumulation; no PP maps.

Audit: Ec_IO 2–3, Prod_Summary 2–3. **Not** Prod_Summary chart #1.

---

## 7. ProductionResult series inventory

| Group | Field | GM col | Role |
|-------|--------|--------|------|
| PP | `pp_rate_by_year` | D | PP design rate |
| PP | `pp_annual_by_year` | E | PP annual |
| PP | `pp_ag_rate_by_year` | G | AG rate |
| PP | `pp_ag_annual_by_year` | H | AG annual |
| Prod_Summary | `oil_daily_series` | T | oil rate |
| Prod_Summary | `oil_annual_series` | U | annual oil |
| Prod_Summary | `oil_cum_series` | V | cum oil |
| Prod_Summary | `gas_daily_series` | W | gas rate |
| Prod_Summary | `gas_annual_series` | X | annual gas |
| Prod_Summary | `gas_cum_series` | Y | cum gas |

Do not confuse Prod_Summary cum maps with missing PP `Chart_Cum` / `AG_Chart_Cum` DTOs.

---

## 8. Remaining blockers (unchanged)

| Item | Status | Reason |
|------|--------|--------|
| **Production Profile** | **DONE** (calc DTOs + builder + audit YES) | `pp_cum_by_year` / `pp_ag_cum_by_year` + `production_profile_dataset` |
| **Equity CashFlow** (chart40) | **BLOCKED (calc)** | Design complete with GM AH/AI; need equity AF + year-keyed DNCF maps; do not scale project DNCF |
| **STOIIP / GIIP** (8 charts) | BLOCKED | No sensitivity-grid DTOs; reservoir engine deferred |
| **OML123_Oil_S1** | BLOCKED | Peripheral scenario; no scenario DTO |
| **Prod_Summary chart #1** / col C | BLOCKED | Semantics unresolved; not T/U/V/W/X/Y |
| **Analysis / MC** (15 charts) | DEFERRED | Audit `DEFERRED`; out of Phase 1H slice |
| **Plot rendering** | DEFERRED | Dual-axis engine / Charts plot page |

---

## 9. Next priorities (evidence-gated only)

1. Do **not** invent missing DTO/calculation outputs in presentation.
2. **Equity calc (when PO authorizes):** implement `TICKET_EQUITY_DNCF_MAPS.md` (Medium — equity AF stack + AH/AI maps) → GTC → audit YES → `equity_cashflow_dataset`.
3. **UI plot / dual-axis** — deferred; optional Charts (data) page under light UI authorization.
4. Prod_Summary #1, STOIIP/GIIP, OML123, Analysis — remain blocked/deferred.
5. Workbook-parity validation remains a **separate** claim — not made.

---

## 10. Explicit “do not” list

Do not:

- claim all 40 charts are implemented;
- claim workbook parity has been validated;
- treat passing tests as sufficient without audit authorization;
- add UI wiring without a separate UI authorization;
- calculate PP cumulative values in presentation;
- recalculate discounted NCF or FLGT economics in presentation;
- manufacture equity DNCF by scaling project DNCF;
- map OML123 to base-case production;
- map Prod_Summary column C into production_summary builder;
- invent STOIIP/GIIP sensitivity grids;
- broaden builders because chart numbers look adjacent;
- modify Excel/calculation modules merely to make a chart pass;
- add `hcdt_gas` / `nddc_gas` to FLGT builder against chart23 evidence that excludes them.

---

## 11. Control-command protocol

| Command | Meaning | Expected response |
|---------|---------|-------------------|
| `STATUS` | Current state | Implementation, audit, tests, Git, blockers, next action |
| `STATUS DELTA` | What changed | Only changes since last checkpoint |
| `NEXT` | Next action | One highest-priority evidence-backed action |
| `CHECKPOINT` | Capture state | Update handoff / project state |
| `HANDOFF` | Migrate chat | Latest Markdown handoff |
| `AUDIT` | Audit reconciliation | Compare work to CSV; do not infer authorization |
| `VERIFY` | Validation | Tests, compile, check, staging gaps |
| `BLOCKERS` | Blocking issues | Only blockers for next step |
| `DECISION` | Record decision | Decision, evidence, consequence |
| `DIFF` | Change review | Since previous checkpoint |
| `STOP` | Stop implementation | No further code; report state |

### Default response discipline

1. Do not restate full project history.
2. Use this handoff as baseline.
3. Report only what the current decision needs.
4. Preserve exact DTO/chart/audit names and paths.
5. Distinguish facts from inference.
6. If an authoritative artifact contradicts this handoff, flag it.
7. Do not repeat unchanged test output unless relevant.

### Information hierarchy

1. Explicit current PO direction  
2. Audit / specs / workbook evidence  
3. Current repository code and DTOs  
4. Tests and verification output  
5. This handoff  
6. Conversation history (working context only)

---

## 12. Success criteria (progress)

| Milestone | Description | Progress |
|-----------|-------------|----------|
| **A** Architecture | ChartDataset structures/templates/builders isolated | `██████████` done |
| **B** Semantic mapping | Workbook→DTO for core families | `█████████░` six families |
| **C** Authorization | Audit YES for intended rows | `██████████` **14 rows YES** |
| **D** Implementation | Builders + tests for authorized families | `██████████` incl. Production Profile |
| **E** Model/DTO completion | Missing DTOs for blocked charts | `██████░░░░` PP cum **done**; Equity **ticket only** |
| **F** UI integration | Consume ChartDataset in UI | `█████░░░░░` data on bundle; **plot UI deferred** |
| **G** Workbook parity | Validated vs GM chart evidence | `███░░░░░░░` **not claimed** |
| **H** Release | Full regression, docs, push as required | `████░░░░░░` local commits only |

**Overall: ~8.5–8.7 / 10**

---

## 13. Recommended continuation prompt

> Continue Phase 1H from `docs/phase1h/PHASE1H_CHAT_HANDOFF.md`. Baseline **`6c2b41d`**. Six authorized chart families; 14 audit YES rows; 9 `chart_datasets` on `PresentationBundle`. PP cum maps + `production_profile_dataset` done. Equity: `TICKET_EQUITY_DNCF_MAPS.md` (GM AH/AI; Medium; not coded). Presentation-only projection. No inventing DTOs. No parity claims. Plot UI deferred. Next: equity calc when PO authorizes, or optional Charts data page. Use `NEXT` / `STATUS DELTA` / `VERIFY`.

---

## 14. Canonical current state (checklist)

1. Phase 1H chart presentation/dataset work.
2. Audit authority: `CHART_MAPPING_AUDIT.csv`.
3. PO: Dr Emmanuel Onwuka; **six** families authorized (14 rows YES / 26 NO).
4. Commit baseline: **`6c2b41d`**.
5. Builders include Production Profile; **9** `chart_datasets` on `PresentationBundle`.
6. Tests: **59 passed** (chart+presentation suite), 1 slow-mark warning.
7. FLGT: **7-series**; no hcdt_gas/nddc_gas.
8. PP cum: **implemented in calc** (`dc361e3`); not in presentation.
9. Equity: design + GM formulas only (`6c2b41d`); calc blocked.
10. Blockers: Equity calc, STOIIP/GIIP, OML123, Prod_Summary #1, Analysis, plot UI.
11. Milestone F **partial** (data attached; plot deferred).
12. No full 40-chart claim; no workbook-parity claim.
13. Handoff: `docs/phase1h/PHASE1H_CHAT_HANDOFF.md`.
14. Product scope: `docs/pems/PEMS_PRODUCT_SCOPE.md`.
