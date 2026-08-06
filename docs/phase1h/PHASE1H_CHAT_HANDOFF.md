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
| **HEAD / baseline** | **`8d2c1cc`** |
| Message | `docs(phase1h): design ticket for PP cumulative maps (calc layer)` |
| Key implementation commits | `0a6d456` (builders + audit) · `19b4ca8` (PresentationBundle.chart_datasets) · `8d2c1cc` (PP cum design ticket) |
| Branch | `master` (local) |
| Push / tag | **not done** |

### Overall assessment

Approximate overall progress: **8.0 / 10**.

Five authorized chart families are implemented, unit-tested, audit-authorized (12 rows), and **committed**. **`PresentationBundle.chart_datasets`** attaches the seven authorized dataset IDs (five families; oil/gas doubled) via pure builders (`19b4ca8`). Plot rendering / dual-axis UI remains deferred. PP cumulative maps are **designed** (`TICKET_PP_CUMULATIVE_MAPS.md`, `8d2c1cc`) but not implemented — await calc-layer authorization. Remaining chart families blocked on DTO gaps or deferred (Analysis).

### Current strengths

- Workbook chart inventory and semantic evidence investigated.
- 40-chart audit universe classified.
- Five core chart families have presentation dataset builders.
- DTO-to-chart mappings for those five families established.
- Builders are projection-only and isolated from Excel/calculation code.
- Unit coverage in place (`test_chart_datasets` + presentation PT including PT11).
- Verification baseline (post-wiring):
  - **50 passed**
  - **1 pre-existing unregistered `@pytest.mark.slow` warning**
  - `compileall src/pems/presentation` OK
- Chart **data** wired into presentation bundle; plot **UI** not started.
- Workbook parity has **not** been claimed as fully validated.
- Product scope continuity: `docs/pems/PEMS_PRODUCT_SCOPE.md`.
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

Explicitly authorized Phase 1H chart implementation for **five families** (see §6). Audit reconciled and committed in `0a6d456`.

### Current audit counts (post-commit)

| Field | Count |
|-------|------:|
| Total chart rows | 40 |
| `implementation_authorized = YES` | **12** |
| `implementation_authorized = NO` | **28** |
| `mapping_status = REVIEW_REQUIRED` | **25** (includes authorized rows; status field not flipped) |
| `mapping_status = DEFERRED` | **15** (Analysis) |

### Authorized audit rows (12)

| Worksheet | Idx | Template | Family |
|-----------|-----|----------|--------|
| Ec_IO | 1 | ECONOMIC_LIMIT | ECONOMIC_LIMIT |
| Ec_IO | 2 | PRODUCTION_SUMMARY | PRODUCTION_SUMMARY oil |
| Ec_IO | 3 | PRODUCTION_SUMMARY | PRODUCTION_SUMMARY gas |
| Ec_IO | 4 | COST_PROFILE | COST_PROFILE oil |
| Ec_IO | 5 | COST_PROFILE | COST_PROFILE gas |
| Ec_IO | 6 | DISCOUNTED_NCF | PROJECT_DISCOUNTED_NCF |
| Prod_Summary | 2 | PRODUCTION_SUMMARY | PRODUCTION_SUMMARY oil |
| Prod_Summary | 3 | PRODUCTION_SUMMARY | PRODUCTION_SUMMARY gas |
| Block_TC | 1 | COST_PROFILE | COST_PROFILE oil |
| Block_TC_Gas | 1 | COST_PROFILE | COST_PROFILE gas |
| FLGT | 1 | FLGT_TAKE | FLGT_TAKE |
| Project_NCF | 1 | DISCOUNTED_NCF | PROJECT_DISCOUNTED_NCF |

**Not authorized:** Prod_Summary chart #1 (col C), Production Profile, Equity_NCF_Con, STOIIP/GIIP, OML123, all Analysis.

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

`datasets.py`: frozen `ChartSeries` / `ChartDataset` + five builders.

`templates.py`: six templates including `EQUITY_CASHFLOW` placeholder (no builder).

`view_models.build_presentation` calls `build_authorized_chart_datasets(bundle)` and attaches results. PySide6 UI still renders **tables only** (no Charts page / no plots).

---

## 5. Current Git state

### Baseline stack (through `8d2c1cc`)

| Commit | Content |
|--------|---------|
| `0a6d456` | Five ChartDataset builders + audit authorization (12 rows YES) |
| `e07c9d7` | Canonical handoff (initial post-0a6d456) |
| `2cd09a3` | Status & Roadmap doc |
| `b7a05ee` | Product scope doc → `docs/pems/PEMS_PRODUCT_SCOPE.md` |
| **`19b4ca8`** | **`PresentationBundle.chart_datasets`** — five authorized families attached |
| **`8d2c1cc`** | Design ticket: PP cumulative maps (calc layer) |

### Presentation wiring (`19b4ca8`)

```text
PresentationBundle.chart_datasets: dict[str, ChartDataset]
```

Official IDs (7):  
`PROJECT_DISCOUNTED_NCF`, `ECONOMIC_LIMIT`,  
`OIL_PRODUCTION_SUMMARY`, `GAS_PRODUCTION_SUMMARY`,  
`OIL_COST_PROFILE`, `GAS_COST_PROFILE`, `FLGT_TAKE`.

Helper: `build_authorized_chart_datasets(bundle)` in `view_models.py`.  
Test: `test_pt11_authorized_chart_datasets_attached`.

### PP cumulative design (`8d2c1cc`)

```text
docs/phase1h/TICKET_PP_CUMULATIVE_MAPS.md
```

GM F/I formulas documented; **no calc code yet** — awaits explicit calc-layer / PO authorization.

### Verification baseline (post-wiring)

```text
pytest tests/unit/test_chart_datasets.py tests/unit/test_presentation.py -q
50 passed, 1 pre-existing @pytest.mark.slow warning

python -m compileall -q src/pems/presentation
OK
```

---

## 6. Completed chart families (implemented + authorized + committed)

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
| **Production Profile** (chart15/16) | BLOCKED | No dedicated PP cumulative DTO (`Chart_Cum` / `AG_Chart_Cum`); do not sum annuals in presentation |
| **Equity CashFlow** (chart40) | BLOCKED | No year-keyed equity AH/AI series; only `equity_ag51` / `equity_ah51` scalars; do not scale project DNCF |
| **STOIIP / GIIP** (8 charts) | BLOCKED | No sensitivity-grid DTOs; reservoir engine deferred |
| **OML123_Oil_S1** | BLOCKED | Peripheral scenario; no scenario DTO |
| **Prod_Summary chart #1** / col C | BLOCKED | Semantics unresolved; not T/U/V/W/X/Y |
| **Analysis / MC** (15 charts) | DEFERRED | Audit `DEFERRED`; out of Phase 1H slice |

---

## 9. Next priorities (evidence-gated only)

1. Do **not** invent missing DTO/calculation outputs in presentation.
2. **UI plot page / dual-axis engine** — still deferred; optional next is a read-only Charts (data) page only under light UI authorization.
3. **Calc-layer (when PO authorizes):** implement `TICKET_PP_CUMULATIVE_MAPS.md` (`pp_cum_by_year` / `pp_ag_cum_by_year`), GTC vs F23…/I23…, then audit YES for Production Profile, then `production_profile_dataset`.
4. **Equity CashFlow** — still needs year-keyed equity AH/AI maps (calc ticket not yet designed as formally as PP).
5. Prod_Summary #1, STOIIP/GIIP, OML123, Analysis — remain blocked/deferred.
6. Workbook-parity validation remains a **separate** claim — not made.

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
| **B** Semantic mapping | Workbook→DTO for core families | `█████████░` strong (core five) |
| **C** Authorization | Audit YES for intended rows | `██████████` **12 rows YES** |
| **D** Implementation | Builders + tests for authorized families | `██████████` **`0a6d456`** |
| **E** Model/DTO completion | Missing DTOs for blocked charts | `█████░░░░░` PP cum **ticket only** |
| **F** UI integration | Consume ChartDataset in UI | `█████░░░░░` **partial**: data on `PresentationBundle`; **plot UI deferred** |
| **G** Workbook parity | Validated vs GM chart evidence | `███░░░░░░░` **not claimed** |
| **H** Release | Full regression, docs, push as required | `████░░░░░░` local commits only |

**Overall: ~8.0 / 10**

---

## 13. Recommended continuation prompt

> Continue Phase 1H chart presentation from `docs/phase1h/PHASE1H_CHAT_HANDOFF.md`. Baseline **`8d2c1cc`**. Audit: 12 rows YES, five families. Builders committed (`0a6d456`); `PresentationBundle.chart_datasets` attached (`19b4ca8`); PP cum calc design ticket only (`8d2c1cc` / `TICKET_PP_CUMULATIVE_MAPS.md`). Presentation-only DTO projection. No inventing DTOs. No workbook-parity claims. Plot UI still deferred. Next: calc authorization for PP cum maps, or optional Charts data page under UI auth. Use `NEXT` / `STATUS DELTA` / `VERIFY`.

---

## 14. Canonical current state (checklist)

1. Phase 1H chart presentation/dataset work.
2. Audit authority: `CHART_MAPPING_AUDIT.csv`.
3. PO: Dr Emmanuel Onwuka; five families authorized.
4. Commit baseline: **`8d2c1cc`** (includes `0a6d456`, `19b4ca8`).
5. **12** audit rows YES; **28** still NO.
6. Five builders committed + unit-tested; **7** `chart_datasets` on `PresentationBundle`.
7. Tests: **50 passed**, 1 pre-existing slow-mark warning.
8. FLGT: **keep 7-series**; `hcdt_gas` / `nddc_gas` **excluded** by chart evidence.
9. Presentation-only; no Excel I/O or calc recompute in builders.
10. PP cumulative: **design ticket only** — not implemented; Production Profile still blocked.
11. Blockers remain: Production Profile (DTO), Equity CashFlow, STOIIP/GIIP, OML123, Prod_Summary #1, Analysis deferred.
12. Milestone F **partial** (data attached; plot engine deferred).
13. No full 40-chart claim; no workbook-parity claim.
14. Handoff path: `docs/phase1h/PHASE1H_CHAT_HANDOFF.md`.
15. Product scope: `docs/pems/PEMS_PRODUCT_SCOPE.md`.
