# CHARTS AND VBA INVENTORY

---

## 1. Charts

| Metric | Value |
|--------|------:|
| Chart XML parts in package | **41** |
| Charts via openpyxl `_charts` | **41** |
| Artifact | `CHART_INVENTORY.csv` |

### By worksheet

| Worksheet | Charts | Likely role |
|-----------|-------:|-------------|
| Analysis | 15 | Sensitivity presentation |
| Ec_IO | 6 | I/O presentation |
| STOIIP / GIIP | 4 each | Reservoir charts |
| Prod_Summary | 3 | Production presentation |
| Production Profile | 2 | Production |
| Block_TC / Block_TC_Gas | 2 / 1 | Cost |
| FLGT | 1 | Fiscal |
| Project_NCF_Con (2) / Equity_NCF_Con | 1 each | NCF presentation |

### Classification

- **Default:** **PRESENTATION** — series bound to worksheet ranges; do not implement as calculation engines.  
- Series formulas/references: see `series_preview` in CSV (partial).  
- Dual-axis zero alignment remains a **PEMS chart engine** requirement (CHART_SPECIFICATION); Excel chart objects are mapping targets, not calc authority.  
- **Do not** treat chart caches as Golden calculation truth.

---

## 2. VBA / macros

| Check | Result |
|-------|--------|
| File extension | `.xlsx` |
| `vbaProject.bin` in package | **No** |
| openpyxl `vba_archive` attribute | May report object; **no vbaProject part** |
| PrinterSettings `*.bin` | Present (print settings, **not** VBA) |

**Conclusion:** No traditional VBA project found in package.  
**Automation:** None identified as VBA macros to port.  
**@Risk named ranges** suggest historical risk-add-in settings — **not** equivalent to embedded VBA; Monte Carlo behaviour **not** reverse-engineered here.

**Policy:** Do not reproduce VBA (none found). Do not invent @Risk logic until documented.

---

## 3. Impact on PEMS

| Item | Affects calculation logic? | Action |
|------|----------------------------|--------|
| Charts | No (presentation) | Map later to ChartDataset |
| VBA | N/A (absent) | — |
| @Risk names | Possibly simulation settings only | Flag for Monte Carlo phase |
