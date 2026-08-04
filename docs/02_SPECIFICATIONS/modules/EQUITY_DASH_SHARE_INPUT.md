# Equity Dash Share — Explicit PEMS INPUT

**Status:** Domain decision **CLOSED — INPUT**  
**Classification:** `CONFIRMED_INPUT`  
**Not:** derived value (unless a separate GM formula defines derivation)  
**GM:** Confirmed-2026-08-03 SHA `D07560CA…BFEA`  
**Authority:** `SCOPE_DECISIONS.md` §C  

**Do not modify the Golden Master.**

---

## 1. Identity

| Field | Value |
|-------|--------|
| Sheet | `Equity Dash` (visible) |
| Business meaning | Working interest / **equity holding** fraction for equity-scaled economics |
| Primary share cell (Company 1) | **`C4`** = **0.49** (literal on GM) |
| Label context | `B3` EQUITY HOLDING; `B4` Company 1 |

---

## 2. Related cells (do not confuse with INPUT)

| Cell | GM content | Classification |
|------|------------|----------------|
| **C4** | `0.49` literal | **INPUT** (Company 1 equity share) |
| **C6** | `1` (Project) | Project total holding constant on GM — not the company share input |
| **C5** | `=C6-C4` | **DERIVED** by Golden Master formula — **not** an independent INPUT |
| D4, D5, D6, … | Costs / formulas | Separate classification (not this decision) |

**Rule:** Do **not** derive Company 1 share unless a GM formula explicitly defines it. On this GM, **C4 is literal INPUT**; **C5 is formula-derived** from C6−C4.

---

## 3. Must be included in

| Area | Requirement |
|------|-------------|
| Input classification | `CONFIRMED_INPUT` |
| Input schema | Field e.g. `equity_share_company_1: float` in (0, 1] (exact bounds per validation rules) |
| Manual input UI | Editable equity share control |
| Excel import mapping | Map to Equity Dash share cell(s) / named equivalent when importing standard workbooks |
| Validation | Required; range check; consistency with any co-shares if multi-company UI added later |
| Semantic mapping | Critical path parameters |
| Module specifications | Input / scenario + equity NCF consumers |

---

## 4. Downstream consumers

Equity share scales equity NCF and RESULTS (e.g. equity-side NPV/IRR, production/revenue × share). Formula catalogue shows heavy references from equity NCF sheets and RESULTS to Equity Dash.

---

## 5. GTC-001

GTC-001 as-saved value for C4 is **0.49**. PEMS must accept this as input state for baseline regression (not recompute C4).

---

## 6. Understanding levels

| Aspect | Level |
|--------|-------|
| INPUT taxonomy | **UNDERSTOOD** (PO closed) |
| Cell C4 identity | **UNDERSTOOD** |
| Full Equity Dash (loans, ACA, etc.) | **PARTIAL** (out of this decision’s scope) |
| VALIDATED | **Not yet** |

**Do not reopen:** INPUT vs derived decision for Equity Dash Share.
