# Input / Output Visual Language

**Status:** **READY** (presentation + interaction semantics)  
**Source GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**GM modified:** **No**

Cross-reference semantic truth: module contracts + `SCOPE_VISIBLE_SHEETS_ONLY.md` + closed domain decisions.  
**Colour alone is not semantic classification.**

---

## 1. Taxonomy (semantic classes for PEMS UI)

| Class | Meaning | How known | Visual cues (observed, non-authoritative alone) |
|-------|---------|-----------|--------------------------------------------------|
| **INPUT** | User/scenario editable | Semantic register / contracts (e.g. Equity C4) | Sometimes bold; DV dropdown; unlocked when sheet protected (rare) |
| **ASSUMPTION** | Scenario driver | Contracts / labels | Often adjacent unit label; % or General format |
| **DEFAULT / STRUCTURAL** | Seed / structural | Register | May look like input — **do not promote to INPUT without contract** |
| **DERIVED** | Formula from inputs | Formula present | Formula bar; sometimes filled cell (Equity C5) |
| **FORMULA / INTERMEDIATE** | Calculation | Formula | Accounting formats on NCF |
| **OUTPUT / KPI** | Result display | RESULTS / hubs | Bold Arial 10 on RESULTS; accounting / % formats |
| **LAW TABLE** | Regulatory reference | Fiscal Terms_PIA decision | Plain rates `0%`/`0.00%`; **not editable as scenario** |
| **EXPECTED ERROR** | No valid result | AU14 `#NUM!` | Excel error string; PEMS `NO_VALID_IRR` |
| **HEADER / LABEL** | Structure | Text | Labels left of values; merged titles |
| **NOTE** | Guidance | Text cells | Smaller/rarer fonts |

---

## 2. Closed decision visual mapping

| Decision | Presentation requirement |
|----------|--------------------------|
| Equity Dash!C4 = **INPUT** | Editable control; format `0%`; bold Century Gothic on GM; show as 49% for GTC |
| Equity Dash!C5 = **DERIVED** | Read-only; show formula result; do not expose as independent input |
| Fiscal Terms_PIA = **LAW TABLE** | Read-only reference browser; rates as %; not CaseInput forms |
| AU14 `#NUM!` | Display **NO_VALID_IRR** / unavailable — not 0% |

---

## 3. Input visual language (PEMS must preserve meaning)

| Mechanism | GM evidence | PEMS |
|-----------|-------------|------|
| Adjacent labels | Ec_IO B-column labels | Field labels required |
| Units in labels | `$/bbl`, `$/Mscf`, `$mm` | Unit chip or suffix |
| Data validation lists | Ec_IO C4 History/Forecast/Complete; G24 R/T vs PSC/SC | Dropdown / enum |
| Percentage formats | C15 `0.00%`, C4 equity `0%` | Percent editors |
| Protection | Sheet protection rare (YTD, OML123 hidden-related); default cell locked flag **not** reliable alone | Use app-level editable flags from contracts |

**Manual vs import:** same CaseInput model; presentation differs only by entry path (form vs import review).

---

## 4. Output / KPI visual language

| Pattern | GM evidence | PEMS |
|---------|-------------|------|
| KPI block with left labels | RESULTS G7–G26 labels, H/J/K/M/N values | Label | value | unit layout |
| BIT vs AIT columns | Host/Contractor BIT $MM vs AIT $MM headers | Column groups |
| Accounting money | `#,##0.00` with `-` for zero | Match |
| Percent KPIs | IRR, take, ERR `0.00%` / `0.0%` | Match |
| Identity strip | Country, PIA, field, equity text | Context header |

---

## 5. Data validation presentation (visible)

| Sheet | Evidence (audit) | Notes |
|-------|------------------|-------|
| Ec_IO | 3 validations (incl. C4 list, G24 list) | Primary CaseInput enums |
| Equity Dash | 2 validations | |
| Cap_Allow / Cap_Allow Gas | 1 each | |
| FLGT, Production Profile, Block_TC, Analysis, HT/CIT oil, START | 1 each | |
| openpyxl warning | “Data Validation extension not supported” | Some DV may be incomplete in extract — **catalogue/data_validations.csv** is co-authority |

---

## 6. Conditional formatting

Material CF present on **Checklist**, **Production Profile**, **Analysis** (audit).  
Treat as **L2/L3** unless a rule encodes a threshold that changes interpretation — document when implementing those sheets’ UI.

---

## 7. Protection

| Sheet | Sheet protection |
|-------|------------------|
| Most visible | **Unprotected** |
| YTD Budget APN (2), OML123_Oil_S1 | Protected (hidden/out of input scope) |

PEMS should lock **DERIVED/LAW/OUTPUT** and unlock **INPUT/ASSUMPTION** per contracts, independent of Excel lock bits.
