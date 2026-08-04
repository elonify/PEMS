# M02 — Fiscal Terms_PIA (Semantic Map)

**Status:** **PARTIALLY MAPPED** — taxonomy **CLOSED**; formula-group depth incomplete  
**PEMS target:** FiscalRegime as **LAW_TABLE** / regulatory rule source  
**Sheet:** Fiscal Terms_PIA  

**Domain decision CLOSED — LAW TABLE** (not ordinary user inputs).  
Full rule documentation: `docs/02_SPECIFICATIONS/modules/FISCAL_TERMS_PIA_LAW_TABLE.md`

---

## Evidence of purpose

- Sheet name: **Fiscal Terms_PIA**  
- Model Map: **PIA = Petroleum Industry Act 2021**  
- Consumed by Royalties, FLGT, CR Econ, NCF  
- PO: law/regulatory table for fiscal calculation layer  

---

## Mapping fields

| Field | Content |
|-------|---------|
| Worksheet | Fiscal Terms_PIA |
| Classification | **LAW_TABLE** — not CONFIRMED_INPUT |
| Rule blocks | Rentals, oil/gas/price royalties, production allowances, dual-tier HT/CIT, PSC cost/profit oil, HCDT/NDDC/NC/EDT/cap allowance/bonus — see law-table doc |
| Formulas | Few (~5); tables are primarily labeled constants |
| Purpose | Authoritative PIA fiscal rates/thresholds/mechanisms |
| Inputs | **None ordinary** — case attributes from Ec_IO etc. **select** applicable rows |
| Outputs | Rule parameters consumed by fiscal calcs |
| Dependencies | Downstream: Royalties, FLGT, CR Econ, HT/CIT/NCF |
| Units | Rates, $/bbl, years, sqKm, mmbbls as labeled |
| Validation | Consumer outputs vs GTC-001; table identity tied to GM SHA |
| Ambiguities | Full selection logic cell-by-cell still EXTRACTED via catalogue |

**Ready for implementation:** **NO** (engine application detail incomplete) — taxonomy no longer blocks as PENDING APPROVAL
