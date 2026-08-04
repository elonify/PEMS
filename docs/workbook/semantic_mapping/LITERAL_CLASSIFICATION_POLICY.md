# LITERAL CLASSIFICATION POLICY

**Phase:** Semantic Mapping  
**Active GM SHA256:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Register (historical full extract):** may include all sheets  
**In-scope for classification work:** **visible sheets only** (see `SCOPE_VISIBLE_SHEETS_ONLY.md`)

---

## Scope rule (mandatory)

1. **Ignore all hidden worksheets** for input/literal classification and readiness.  
2. **Literals on hidden sheets are out of scope** — do not classify them as PEMS inputs; mark scope = `OUT_OF_SCOPE_HIDDEN_SHEET` if listed.  
3. **Do not modify** hidden sheets or the Golden Master.  
4. Active extract counts: **~6,644** literals on hidden sheets (ignore); **~3,827** on visible sheets (classify).  

---

## Rules (mandatory) — visible sheets only

1. Every numeric/date/bool literal on a **visible** sheet starts as **`UNCLASSIFIED_LITERAL`**.  
2. **Do not** classify as **INPUT** merely because the cell is hard-coded.  
3. Promote a classification **only** with workbook evidence, e.g.:  
   - Explicit label “Input” / form control linkage  
   - Data validation on editable driver ranges **plus** documentation  
   - Model Map / checklist identification  
   - Project Owner decision recorded in `DECISIONS_REQUIRED.md`  
4. Non-binding **candidate hints** in the register are **not** classifications.  
5. GTC-001 may store literal values for baseline integrity without treating them as scenario drivers.

---

## Allowed classifications (future)

| Code | Meaning |
|------|---------|
| `OUT_OF_SCOPE_HIDDEN_SHEET` | On hidden sheet — **ignore** for input classification |
| `UNCLASSIFIED_LITERAL` | Default on **visible** sheet — decision required |
| `CONFIRMED_INPUT` | User/editable driver (evidence or **PO decision**) |
| `CONFIRMED_PARAMETER` | Scenario parameter (evidence required) |
| `HARDCODED_CONSTANT` | Fixed model constant (evidence required) |
| `LOOKUP_TABLE_CONSTANT` | Table entry (evidence required) |
| `LAW_TABLE` | Regulatory / fiscal law table (not ordinary user input) — **Fiscal Terms_PIA** |
| `SEED_OR_FLAG` | Zero/seed for iteration (evidence required) |
| `EXCLUDED_STRUCTURAL` | Not business-relevant (evidence required) |

### PO decisions applied (2026-08-03)

| Item | Classification |
|------|----------------|
| Equity Dash **Share** cell(s) | **`CONFIRMED_INPUT`** (user/input variable; not derived) |
| **Fiscal Terms_PIA** sheet numerics (regime tables) | **`LAW_TABLE`** (law/regulatory table; not ordinary user inputs) |

**Current state (active extract):**  
- Hidden-sheet literals: **ignore** (6,644)  
- Visible-sheet literals: **3,827** still to classify (0 promotions to CONFIRMED_*)  

---

## In-scope classification work

Priority **visible** sheets only: Ec_IO, Fiscal Terms_PIA, Equity Dash, Production Profile, STOIIP/GIIP, Block_*, Cap_Allow*, Royalties, FLGT, CR Econ, visible NCF sheets, RESULTS Equity, Analysis (if v1), Checklist/Master/START as needed.

**Do not prioritise:** Oil Input, Gas Input, YTD Budget APN (2), Model Map, OML123_Oil_S1, HT_NCF, CIT_NCF, Project_NCF_Con (all **hidden**).
