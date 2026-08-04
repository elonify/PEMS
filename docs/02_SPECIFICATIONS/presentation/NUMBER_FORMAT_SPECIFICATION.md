# Number Format Specification

**Status:** **READY** (presentation metadata)  
**Source GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Evidence:** `PRESENTATION_AUDIT_EXTRACT.json` (read-only openpyxl sample)  
**GM modified:** **No**

---

## 1. Observed Excel format strings (high frequency)

| Excel format string | Approx. sample count | Typical use |
|---------------------|---------------------:|-------------|
| `General` | 1953 | Labels, years, free text, many drivers |
| `_-* #,##0.00_-;\-* #,##0.00_-;_-* "-"??_-;_-@_-` | 1765 | Accounting $mm cashflow / NCF |
| `_(* #,##0.00_);_(* \(#,##0.00\);_(* "-"??_);_(@_)` | 515 | Accounting with parens for negatives |
| `0.00%` | 204 | Rates, IRR, ERR, hurdle |
| `0%` | 162 | Whole-percent rates / equity share |
| `0.0%` | 130 | One-decimal percent (e.g. AU14 format) |
| `0.00` | 101 | Ratios PVR/PI |
| `_-* #,##0_-;\-* #,##0_-;_-* "-"??_-;_-@_-` | 63 | Integer accounting |
| `[$$-409]#,##0.00_ ;[Red]\-[$$-409]#,##0.00\ ` | 54 | Currency $ with red negatives |
| `_("$"* #,##0.00_);_("$"* \(#,##0.00\);_("$"* "-"??_);_(@_)` | 52 | Explicit `$` accounting (RESULTS costs/revenues) |
| `#,##0.00_);[Red](#,##0.00)` | 30 | Red negative decimals |
| `_(* #,##0.000_);_(* \(#,##0.000\);_(* "-"??_);_(@_)` | 14 | Three-decimal accounting |

Counts from visible-sheet nonempty samples (not full workbook census).

---

## 2. Traceable examples (sheet!cell)

| Cell | Semantic | Stored value (formula mode) | Excel format | Display intent |
|------|----------|-----------------------------|--------------|----------------|
| Ec_IO!C15 | Hurdle rate | 0.15 | `0.00%` | 15.00% |
| Ec_IO!C12 | Oil price | 50 | `General` | 50 |
| Equity Dash!C4 | Equity INPUT | 0.49 | `0%` | 49% |
| Equity Dash!C5 | DERIVED | `=C6-C4` | `0%` | 51% |
| Fiscal Terms_PIA!W18 | Oil royalty rate (law) | 0.05 | `0.00%` | 5.00% |
| Fiscal Terms_PIA!T72 | HCDT rate | 0.03 | `0%` | 3% |
| RESULTS Equity!H7 | Hurdle display | `=Ec_IO!C15` | `0.00%` | 15.00% |
| RESULTS Equity!J7 | Host BIT NPV | formula | `_-* #,##0.00_-;…` | 37.21 accounting |
| RESULTS Equity!N8 | AIT IRR | IRR formula | `0.00%` | 34.86% |
| RESULTS Equity!H26 | ERR | formula | `0.00%` | 5.43% |
| Project_NCF!AG58 | Project IRR | IRR | `0.00%` | ~34.86% |
| Project_NCF!AU14 | IRR no-sign-change | IRR → `#NUM!` | `0.0%` | Excel error display |

---

## 3. PEMS presentation behaviour

| Kind | Store | Display |
|------|-------|---------|
| Percentage / rate | Fraction 0–1 | Match format class: `0%`, `0.0%`, or `0.00%` |
| Money $mm series | Numeric $mm | Accounting 2 dp; zero as `-` where Excel does |
| Money with `$` prefix | Numeric | RESULTS-style `$` accounting |
| Ratios PVR/PI | Numeric | 2 dp `0.00` |
| Years / counts | Numeric | General or integer accounting |
| Expected no-IRR | `NO_VALID_IRR` semantic | Do **not** format as 0%; show unavailable/error state |

**Precision materiality:** Use GM format precision for UI; GTC numeric compare still uses validation float policy (1e-9) for underlying values.
