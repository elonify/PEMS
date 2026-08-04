# PEMS Presentation Specification (Master)

**Status:** **READY**  
**Documentation type:** Level-1/2/3 presentation requirements from Golden Master audit  
**Active GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Formal GM approval:** **CLOSED**  
**Audit method:** Read-only openpyxl observation — **workbook not saved or modified**  
**Evidence extract:** `PRESENTATION_AUDIT_EXTRACT.json`  

**Sibling specs:**  
- [NUMBER_FORMAT_SPECIFICATION.md](NUMBER_FORMAT_SPECIFICATION.md)  
- [UNIT_AND_CURRENCY_SPECIFICATION.md](UNIT_AND_CURRENCY_SPECIFICATION.md)  
- [TYPOGRAPHY_AND_STYLE_SPECIFICATION.md](TYPOGRAPHY_AND_STYLE_SPECIFICATION.md)  
- [INPUT_OUTPUT_VISUAL_LANGUAGE.md](INPUT_OUTPUT_VISUAL_LANGUAGE.md)  

**Cross-refs:** module contracts (Ec_IO…RESULTS READY) · `CHART_SPECIFICATION.md` (dual-axis) · `UI_ARCHITECTURE.md` · `DATA_MODEL.md` IRR · GTC framework · `SCOPE_VISIBLE_SHEETS_ONLY.md`

---

## 1. Purpose

Specify presentation conventions so PEMS communicates the same **economic meaning** as the Excel Golden Master: editable vs derived, units/scales, KPIs, law tables, and expected unavailable results (e.g. no valid IRR).

This is **not** a mandate to pixel-clone Excel.

---

## 2. Scope

| In scope | Out of scope |
|----------|----------------|
| **30 visible sheets** presentation audit | Modifying GM |
| Reusable style / format patterns | Calculation implementation |
| Input/output visual language | Hidden-sheet UI (hidden ignored for input surface) |
| Level 1–3 classification | Invented themes not in GM |

**Visible sheets audited (30):**  
START, Checklist, Master, Fiscal Terms_PIA, Ec_IO, STOIIP, GIIP, Production Profile, Block_Oil Data, Block_Gas Data, Prod_Summary, Block_TC, Block_TC_Gas, Cap_Allow, Cap_Allow Gas, Royalties, FLGT, CR Econ, HT_NCF_Oil, CIT_NCF_Oil, CIT_NCF_Gas, Project_NCF, Analysis, END, Equity Dash, HT_NCF_Oil Equity, CIT_NCF_Oil Equity, CIT_NCF_Gas Equity, Equity_NCF_Con, RESULTS Equity.

**Hidden (8):** Oil Input, Gas Input, YTD Budget APN (2), Model Map, OML123_Oil_S1, HT_NCF, CIT_NCF, Project_NCF_Con — not user input surface; catalogue-only.

---

## 3. Three-level presentation model

| Level | Name | Must preserve? | Examples |
|------:|------|----------------|----------|
| **1** | Semantically required | **Yes** | Units, $mm vs $/bbl, % as fraction, INPUT vs DERIVED vs LAW, `NO_VALID_IRR` |
| **2** | Functionally required | **Yes for usability** | Enum dropdowns, editable fields, KPI grouping, labels+units, validation errors |
| **3** | Visual / Excel-specific | Optional polish | Exact Century Gothic, theme fills, merge headers, tab colours, print layout |

**Parity rule:** Level-3 differences are **not** calculation-parity failures.

---

## 4. Sheet purpose map (presentation)

| Sheet | User-facing purpose |
|-------|---------------------|
| START / Checklist / Master / END | Navigation / QA / labels |
| Ec_IO | Case dashboard + assumptions + KPI hub |
| Equity Dash | Equity holding INPUT + loan UI |
| Fiscal Terms_PIA | LAW TABLE reference |
| STOIIP / GIIP | Reservoir volumes (interface) |
| Production Profile / Block_* / Prod_Summary | Production schedules & summary |
| Block_TC* / Cap_Allow* | Cost schedules & allowances |
| Royalties / FLGT | Royalty rates & front-end take |
| CR Econ | Cost recovery bridge |
| HT/CIT/Project/Equity NCF | Tax & cashflow detail |
| RESULTS Equity | Executive KPI dashboard |
| Analysis | Sensitivity (deferred scope) |

---

## 5. Layout conventions

| Pattern | Observation | PEMS |
|---------|-------------|------|
| Label left, value right | Ec_IO B labels / C values; RESULTS G labels / H–N values | Standard form/KPI grid |
| Year as row axis | Block_TC A, Cap_Allow FE, NCF A, FLGT A | Time series tables |
| Category headers row 2–3 | Block_TC Exploration/CAPEX/OPEX; units `$mm` row 3 | Table headers + unit row |
| Multi-field column blocks | Block_Oil / Block_TC repeated field groups | Grid or field selector UI |
| Freeze panes | Many sheets (Ec_IO B13, Project_NCF B5, RESULTS X27, FLGT V5, …) | Sticky header/year columns where useful (L2) |
| Merges | Present on Equity Dash, dashboards | Optional (L3); don't hide semantics in merges |
| Print | Orientation/paper recorded in extract | Export concern (REPORT_SPEC) |
| Tab colour | Mostly default | Optional (L3) |

**Structural layout ≠ calculation rule.**

---

## 6. Excel-specific features classification

| Feature | Classification |
|---------|----------------|
| Number formats & units | **1 Semantic / 2 Functional** |
| Data validation enums | **2 Functional** |
| Formula vs input distinction | **1 Semantic** |
| Array formulas / data tables | **1 Semantic** (calc) / presentation of spill optional |
| Freeze panes | **2 Functional** (nice) / **3** if exact |
| Merged cells | **3** unless sole label carrier |
| Conditional formatting | **2/3** — Checklist, Production Profile, Analysis |
| Sheet protection | Rare; **2** via app permissions |
| Hidden rows/cols | Document if found; not primary |
| Print areas | **3** |
| Dual-axis charts | **1/2** — see `CHART_SPECIFICATION.md` zero alignment |
| VBA | Not relied on for presentation (no vbaProject emphasis) |

---

## 7. Format data model (conceptual)

```text
PresentationField:
  field_id
  semantic_type: INPUT | ASSUMPTION | DERIVED | FORMULA | OUTPUT | KPI | LAW_TABLE | LABEL | EXPECTED_ERROR
  editable: bool
  unit: str | null
  currency: USD | null
  scale: mm | unit | fraction | ...
  precision: int | null
  display_format: excel_format_string | pems_token
  style_class: str
  source_sheet
  source_cell
  implementation_requirement: L1 | L2 | L3
```

Manual entry and import both bind to the same `field_id` / CaseInput / Results DTO.

---

## 8. Expected error presentation

| GM | Display | PEMS |
|----|---------|------|
| Project_NCF!AU14 `#NUM!` | Excel error in cell formatted `0.0%` | **`NO_VALID_IRR` / `NO_SIGN_CHANGE`** — never invent IRR or show 0% as success |

Consistent with DATA_MODEL §4.10 and GTC EXP-001.

---

## 9. Consistency with module contracts

| Contract | Presentation link |
|----------|-------------------|
| Ec_IO | Drivers + hub KPI formats |
| Production | mb/d, mmbbls, bscf tables |
| Costs | $mm Block_TC / Cap_Allow |
| FLGT | $mm royalties, % ERR |
| CR/NCF | Accounting NCF; AU14 |
| RESULTS | KPI dashboard Arial 10 / accounting |
| Fiscal LAW | Non-editable rate tables |

No intentional contradictions introduced. Ambiguities: theme colours not hex-stable; openpyxl DV extension gaps; default `locked=True` without sheet protect.

---

## 10. Presentation readiness checklist

| Criterion | Met? |
|-----------|------|
| Visible sheets audited (30) | **Yes** |
| Typography documented | **Yes** |
| Style / fill classes documented | **Yes** |
| Number formats catalogued | **Yes** |
| Currencies catalogued | **Yes** |
| Units catalogued | **Yes** |
| Scale/precision documented | **Yes** |
| Input visual language | **Yes** |
| Derived/formula language | **Yes** |
| Output/KPI language | **Yes** |
| Expected-error presentation | **Yes** |
| Layout conventions | **Yes** |
| Conditional formatting noted | **Yes** |
| Data validation noted | **Yes** |
| Protection noted | **Yes** |
| Excel-specific features classified | **Yes** |
| L1/L2/L3 separated | **Yes** |
| Ambiguities recorded | **Yes** |
| No invented unsupported rules | **Yes** |
| Traceable GM examples | **Yes** |
| GM not modified | **Yes** |
| No calculation code | **Yes** |
| Numerical validation NOT CLAIMED | **Yes** |

# **PRESENTATION SPECIFICATION = READY**

---

## 11. Stop condition

**STOP.** Do not create GUI code, calc code, or start Phase 0 automatically.

Next gate: **final pre-implementation completeness audit** (all module contracts READY + presentation READY + GTC/traceability/architecture), then Phase 0 only when authorized.
