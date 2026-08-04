# Golden Master Freeze Record

**Event:** RE-FREEZE — accept current confirmed workbook  
**Status of freeze identity:** **ACTIVE GOLDEN MASTER** — formal PO approval **CLOSED**  
**Freeze timestamp (UTC):** 2026-08-03T18:20:00Z  
**Formal approval:** 3 August 2026, 20:57 WAT (UTC+1) — Dr Emmanuel Ifeanyichukwu Onwuka  
**Do not modify the approved Golden Master without a new versioned freeze + approval cycle.**

---

## ACTIVE GOLDEN MASTER (current — APPROVED)

| Field | Value |
|-------|--------|
| File name | `Econ_Model_PEMS_confirmed_2026-08-03.xlsx` |
| Relative path | `docs/workbook/Workbook_History/Econ_Model_PEMS_confirmed_2026-08-03.xlsx` |
| Complete SHA256 | **`D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`** |
| File size (bytes) | **4841231** |
| Sheet count | **38** |
| Version label | Confirmed-2026-08-03 |
| Status | **ACTIVE GOLDEN MASTER — FORMALLY APPROVED** |
| Formal PO approval | **CLOSED** (`GOLDEN_MASTER_APPROVAL.md`) |
| Approver | Dr Emmanuel Ifeanyichukwu Onwuka (Project Owner) |
| Policy | **READ-ONLY** for implementers; any subsequent binary change is a **new version** requiring new SHA + approval |

### Structural verification at freeze

| Check | Result |
|-------|--------|
| File readable | Yes |
| openpyxl load (formulas) | Yes |
| openpyxl load (data_only cache) | Yes |
| Sheet count | 38 |

---

## PREVIOUS DOCUMENTED GM HASH — SUPERSEDED BY RE-FREEZE

| Field | Value |
|-------|--------|
| Complete SHA256 | **`87EF7439A8F19C52B5B948D379D1752B327144CCDBC36758A780A93EC71121FB`** |
| Status | **SUPERSEDED BY RE-FREEZE** |
| Reason | Confirmed path was re-saved; prior hash no longer identifies the on-disk confirmed file |
| Restore policy | Do **not** restore unless explicitly instructed |
| Historical record | **Retain** (do not delete) |

---

## Related identities (not active GM)

| Role | Path | SHA256 | Note |
|------|------|--------|------|
| Live working copy | `docs/workbook/Econ_Model_PEMS.xlsx` | `FFADB639A0EA2FD3D1981BE11FC495D013875193F30CEEA0454CDA27827C7F0F` | Calc/semantic-equivalent to active GM; **not** byte-identical; **not** promoted |
| Historical intake | `…/Econ_Model_PEMS_intake_2026-08-01.xlsx` | `F6A1992F6A3CC27EC587779ADE6CF667B246FB1587296EFD0CD14B47A6783006` | STALE / historical only |

---

## Path integrity disposition at freeze

**CLOSED — NON-SUBSTANTIVE CURRENT-WORKBOOK DIFFERENCE**  
(calc/semantic content match between current confirmed and current live; residual packaging/CRC only)

Historical SHA drift (`87EF7439…` → `D07560CA…`) is a **governance/history** matter closed by this re-freeze, not a calculation blocker.

---

## Closed domain decisions (not reopened)

| Decision | Status |
|----------|--------|
| Equity Dash Share C4 | **INPUT** |
| C5 = C6−C4 | **DERIVED** |
| Fiscal Terms_PIA | **LAW TABLE** |
| AU14 `#NUM!` | **EXPECTED** no-sign-change IRR |
| Critical-path literals | **829/829** resolved |
| Ec_IO unresolved literals | **0** |
| Excel I/O ADR-0010 | Closed |
| Equity Dash prior substantive discrepancy | **CLOSED** |
| openpyxl 25 DataTable false positives | **CLOSED** |

---

## Catalogue / GTC binding

Catalogue and GTC-001 must be re-extracted against **ACTIVE** SHA  
`D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
(not the superseded hash). See `catalogue/extraction_summary.json` and  
`Validation_Datasets/scenarios/GTC-001_manifest.json` after re-extract.
