# DEPENDENCY GRAPH (EVIDENCE-BASED)

**Status:** Improved over pure regex inventory; **full calculation order NOT proven**.  
**Source:** Sheet-qualified references inside formulas in `formula_catalogue.csv`.  
**Artifacts:** `CROSS_SHEET_DEPENDENCY_EDGES.csv`, `SHEET_UPSTREAM_SUMMARY.csv`.

---

## 1. Method

1. Parse formulas for `Sheet!` / `'Sheet Name'!` references.  
2. Edge: `from_sheet → to_sheet` means formulas **on** `to_sheet` **reference** `from_sheet`.  
3. Count occurrences (weight).  
4. Named ranges: substring frequency in formulas (`NAMED_RANGE_USAGE_TOP100.csv`) — **not** a full name-resolution graph.  
5. Same-sheet references exist but are under-counted for dependency **order** between modules.

**Limitations**

- INDIRECT, structured table refs, incomplete name expansion → missing edges.  
- Regex false positives/negatives possible.  
- Does not prove absence of cycles.  
- Does not expand every named range to cells.

---

## 2. Strongest cross-sheet edges (top evidence)

| From | To | Approx. formula refs |
|------|-----|---------------------:|
| Block_TC | Cap_Allow | 6,636 |
| Block_TC_Gas | Cap_Allow Gas | 6,636 |
| Ec_IO | Cap_Allow / Cap_Allow Gas | 1,074 each |
| Equity Dash | HT_NCF_Oil Equity | 944 |
| CIT_NCF_Gas / Oil | Project_NCF_Con | 905 each |
| Equity Dash | CIT_NCF_* Equity | high |
| CIT_* Equity | Equity_NCF_Con | high |
| HT_NCF_Oil | HT_NCF_Oil Equity | 809 |
| FLGT | HT_NCF / CIT_* | hundreds |
| Block_Oil Data | Block_TC | 453 |
| Royalties | FLGT | 380 (via FLGT upstream) |
| Prod_Summary | ← Block_Oil/Gas, OML123, Ec_IO | see summary |

---

## 3. Domain-level flow (interpreted from edges + labels)

```text
[Inputs: Oil/Gas Input, Ec_IO, Equity Dash, Fiscal Terms_PIA]
        ↓
[STOIIP / GIIP] → [Production Profile / Block_* / OML123] → [Prod_Summary]
        ↓
[Block_TC / Block_TC_Gas] → [Cap_Allow / Cap_Allow Gas]
        ↓
[Royalties] → [FLGT]
        ↓
[CR Econ] ← FLGT, Cap_Allow, Ec_IO, Fiscal Terms, CIT_NCF_Oil
        ↓
[HT_NCF_* / CIT_NCF_* / Project_NCF_* / Equity_NCF_*]
        ↑ Equity Dash scaling
        ↓
[RESULTS Equity] ← HT_NCF_Oil Equity, Equity_NCF_Con, FLGT, Prod_Summary, Ec_IO
        ↓
[Analysis] (sensitivity; data tables)
```

---

## 4. CR Econ position

- **Upstream (referenced by CR Econ formulas):** FLGT (323), Cap_Allow (127), Ec_IO (92), Fiscal Terms_PIA (90), CIT_NCF_Oil (46).  
- **Downstream (other sheets reference CR Econ):** HT_NCF, CIT_NCF, HT_NCF_Oil, CIT_NCF_Oil/Gas, Project_NCF_*, *Equity* NCF sheets (tens to 136 refs).  

CR Econ is a **mid-stream fiscal/cost recovery bridge**, not a terminal results-only sheet.

---

## 5. Circular / unresolved dependency notes

| Issue | Evidence | Status |
|-------|----------|--------|
| Equity Dash ↔ NCF equity sheets | Equity Dash heavily referenced by equity NCF; RESULTS uses both | **Coupling** — order not fully linearized |
| Ec_IO ↔ results sheets | Ec_IO formulas also reference Prod_Summary, Project_NCF, FLGT, RESULTS | **I/O hub** — not pure input |
| Analysis ↔ Royalties/FLGT | Royalties/FLGT reference Analysis (sensitivity factors?) | **Feedback path** — needs cell-level study |
| Same-sheet NCF recurrence | Carry-forward columns (e.g. CR Econ N column) | Intra-sheet time coupling |
| Full graph proven? | No | **NOT PROVEN** |

---

## 6. Named ranges

- Defined names extracted: **192** (openpyxl); prior XML count ~230 — mismatch open.  
- Many `@Risk` / graph / MDS system names — Monte Carlo heritage; **do not invent** @Risk behaviour.  
- Business name → cell map incomplete.

---

## 7. Claim level

**Improved dependency evidence available.**  
**Full dependency order for implementation sequencing of every cell: NOT claimed.**
