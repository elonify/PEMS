# Analysis Data-Table Formulas

**Active GM SHA256:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Count:** **18**  
**Inventory:** `ANALYSIS_DATA_TABLE_FORMULAS.csv`

---

## Classification

These are Excel **`DataTableFormula`** (what-if / data table) constructs on the **Analysis** sheet.

| Question | Assessment |
|----------|------------|
| Automatic workbook **error**? | **No** (unless cached error strings appear — none required for classification as error here) |
| Affect core calc engine? | **Unlikely primary path** — sensitivity surface |
| Affect sensitivity analysis? | **Yes — likely** |
| Use as GTC expected without review? | **No** |
| PEMS requirement | If sensitivity in scope, implement via PEMS sensitivity engine + ChartDataset; **do not invent** Excel table formulas |

**Do not replace with invented formulas.**
