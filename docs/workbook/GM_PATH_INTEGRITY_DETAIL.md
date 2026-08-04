# GM Path Integrity Detail — Equity Dash Focus

**Status of this document:** **HISTORICAL COMPARE EVIDENCE**  
**Final disposition (after re-freeze):** **CLOSED — NON-SUBSTANTIVE CURRENT-WORKBOOK DIFFERENCE**  
**ACTIVE GM SHA (post re-freeze):** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**PREVIOUS DOCUMENTED GM HASH — SUPERSEDED BY RE-FREEZE:** `87EF7439A8F19C52B5B948D379D1752B327144CCDBC36758A780A93EC71121FB`  
See `GM_PATH_INTEGRITY.md` and `GM_FREEZE_RECORD.md` for current authority.

**Comparison date:** 2026-08-03 (pre-alignment evidence retained)  
**Method:** Read-only openpyxl + OOXML zip inventory  
**Workbooks not modified by this comparison.**

---

## 1. Authoritative Golden Master SHA (at time of this historical compare)

**`87EF7439A8F19C52B5B948D379D1752B327144CCDBC36758A780A93EC71121FB`**  
*(now SUPERSEDED BY RE-FREEZE — do not use as active identity)*

| Field | Value |
|-------|--------|
| Path | `docs/workbook/Workbook_History/Econ_Model_PEMS_confirmed_2026-08-03.xlsx` |
| Size | 4,841,353 bytes |
| Role | Authoritative confirmed identity for catalogue / GTC / PEMS economic baseline |

---

## 2. Live workbook SHA

**`9F7257A073F37A5822EC8B71882183915E044C768696C5380DC248B98DFCF5D5`**

| Field | Value |
|-------|--------|
| Path | `docs/workbook/Econ_Model_PEMS.xlsx` |
| Size | 4,840,793 bytes |
| Role | Working copy (not byte-identical; not silently promoted) |

---

## 3. Exact differing workbook parts (OOXML)

Top size deltas (not exhaustive):

| Part | Notes |
|------|--------|
| `xl/styles.xml` | +826 B — styles/formatting |
| `customXml/itemProps*.xml` | Reordered/swapped props |
| `xl/worksheets/sheet33.xml` | +517 B — **Equity Dash** worksheet XML |
| `xl/calcChain.xml` | +168 B — calc chain residual |
| Various sheet/chart XML | Small deltas |

Byte identity: **false** (as expected for working copy).

Machine dump: `GM_PATH_INTEGRITY_DETAIL.json`

---

## 4. Equity Dash differences

### 4.1 Closed domain cells (must not reopen)

| Cell | Confirmed | Live | Match | Classification |
|------|-----------|------|-------|----------------|
| **C4** | 0.49 | 0.49 | **Yes** | **INPUT** (Company 1 share) |
| **C5** | `=C6-C4` | `=C6-C4` | **Yes** | **DERIVED** |
| **C6** | 1 | 1 | **Yes** | Project total |

### 4.2 Formatting / layout (hypothesis supported)

| Check | Result |
|-------|--------|
| Merged cells equal? | **No** |
| Merges only in confirmed | `F3:G3` |
| Merges only in live | `G3:I3`, `J3:L3` |
| Format property sample diffs (font/align/number/fill/border) | **26** cells sampled |
| Hypothesis “merged-cell / formatting work” | **Partially confirmed** |

### 4.3 Calculation-structure differences on Equity Dash (beyond pure format)

| Check | Result |
|-------|--------|
| Classic formula-string diffs (`=...` text) workbook-wide | **0** |
| ArrayFormula definitions on loan block (M4:R…) | **Ref spans differ** (e.g. confirmed `M4:M9` vs live `M4:M7` for SEQUENCE/PMT/PPMT/IPMT/SCAN arrays) |
| Loan amortization **cached values** (e.g. O5/P5/Q5/R5…) | **Material differences** (orders of magnitude) |

These are **not** explained by fonts/borders alone: array formula **spill ranges** and loan-schedule **results** differ.

---

## 5. Which differences are formatting-only

- Styles (`styles.xml`)  
- Merge layout on Equity Dash header blocks  
- Sample cell font/alignment/number-format/fill/border  
- Minor chart/customXml packaging  

---

## 6. Which differences affect values

| Area | Affects values? | Nature |
|------|-----------------|--------|
| Equity Dash C4/C5/C6 | **No change** | Share INPUT/DERIVED intact |
| Equity Dash loan amort schedule (O–R) | **Yes** | Large cached value deltas |
| RESULTS Equity K7/K8/N7 (formulas identical) | **Slight cache drift** | Same formulas; cached floats differ at ~1e-4–1e-1 scale |
| Project_NCF AU12 IRR cache | **Slight cache drift** | Formula identical; 0.3486 vs 0.3506 |
| Project_NCF AU14 | **No** | Both `#NUM!` |
| FLGT AB51 | **No** | Exact cache match |

---

## 7. Whether formulas changed

| Class | Result |
|-------|--------|
| Standard formula text (`=` strings) across all sheets | **No differences found** |
| Equity Dash ArrayFormula **ref ranges** | **Yes — changed** (local loan amortization block) |

---

## 8. Whether named ranges changed

| Check | Result |
|-------|--------|
| Defined name count | 192 = 192 |
| Names only in one file | **0** |
| Changed definitions | **0** |

---

## 9. Whether calculation dependencies changed

| Check | Result |
|-------|--------|
| Cross-sheet formula text | **No** differences detected |
| Key RESULT/NCF/FLGT formula text | **Identical** |
| Local Equity Dash array dependency span | **Changed** (loan schedule length/spill) |

---

## 10. Whether differences affect PEMS economic logic

| Concern | Assessment |
|---------|------------|
| Equity share INPUT (C4) | **Unaffected** — values and closed decision intact |
| C5 derived formula | **Unaffected** |
| Fiscal Terms LAW TABLE | **Unaffected** (not Equity Dash) |
| Core oil/gas NCF **formula definitions** | **Unaffected** (text match) |
| Equity Dash **loan amortization** local schedule | **Potentially affected** if PEMS implements that block from live copy |
| Cached KPI floats | Minor drift — **use confirmed GM cache / GTC-001** as expected baseline, not live working-copy cache |

**Post re-freeze:** PEMS must use ACTIVE confirmed GM SHA `D07560CA…BFEA` as calculation authority.  
*(Historical text below referred to then-active `87EF7439…`.)*

---

## 11. Final disposition

# **B. SUBSTANTIVE — TECHNICAL ISSUE REMAINS**

**Rationale (verified, not assumed):**

1. Formatting/merge/style differences on Equity Dash are **real** (hypothesis partially true).  
2. However, Equity Dash also shows **ArrayFormula reference-range changes** and **material loan-amortization value differences**.  
3. Therefore the live file is **not** purely a non-substantive formatting working copy for the entire Equity Dash sheet.  
4. Path integrity is **not** closed as “non-substantive.”  
5. Live file is **not** promoted; confirmed GM remains authoritative.  
6. Byte identity is **not** required; substantiveness is decided by calc structure/values evidence.

**Hypothesis status:** “Only Equity Dash presentation/formatting” → **NOT fully verified**; formatting yes, but also local calc-structure/value residuals on loan arrays.

---

## Equity domain decisions (not reopened)

| Item | Status |
|------|--------|
| C4 INPUT 0.49 | **CLOSED** |
| C5 DERIVED `=C6-C4` | **CLOSED** |
| Fiscal Terms_PIA LAW TABLE | **CLOSED** |
