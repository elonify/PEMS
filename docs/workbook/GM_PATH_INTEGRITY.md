# Golden Master Path Integrity

**Last updated:** 2026-08-03 — **RE-FREEZE accepted**  
**Freeze record:** `GM_FREEZE_RECORD.md`  
**Recheck artifact:** `GM_RECHECK_2026-08-03.json`  
**Prior detailed compare:** `GM_PATH_INTEGRITY_DETAIL.md` / `.json` (historical evidence)

---

## ACTIVE GOLDEN MASTER

| Field | Value |
|-------|--------|
| Path | `Workbook_History/Econ_Model_PEMS_confirmed_2026-08-03.xlsx` |
| **SHA256** | **`D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`** |
| Size | 4,841,231 bytes |
| Sheets | 38 |
| Status | **ACTIVE GOLDEN MASTER — FORMALLY APPROVED** |
| Formal PO approval | **CLOSED** — Dr Emmanuel Ifeanyichukwu Onwuka, 3 August 2026 WAT |

### PREVIOUS DOCUMENTED GM HASH — SUPERSEDED BY RE-FREEZE

| Field | Value |
|-------|--------|
| SHA256 | **`87EF7439A8F19C52B5B948D379D1752B327144CCDBC36758A780A93EC71121FB`** |
| Status | **SUPERSEDED BY RE-FREEZE** (historical only) |

---

## Live working copy

| Field | Value |
|-------|--------|
| Path | `Econ_Model_PEMS.xlsx` |
| SHA256 | `FFADB639A0EA2FD3D1981BE11FC495D013875193F30CEEA0454CDA27827C7F0F` |
| Size | 4,841,422 bytes |
| Role | Working copy — **not** the frozen GM identity |
| Byte-identical to GM | **No** (+191 bytes) |

---

## Calculation / semantic integrity (confirmed vs live)

| Check | Result |
|-------|--------|
| Sheet names (38) | Equal |
| Named ranges (192) | Equal |
| Formula strings | **0 diffs** |
| ArrayFormula ref+text | **0 diffs** |
| Semantic cell content (incl. DataTable attrs) | **0 diffs** |
| Equity Dash C4/C5/C6, loan inputs, array spans, amort | **Match** |
| Prior openpyxl “25 value diffs” | **CLOSED** — DataTableFormula object-identity false positive |
| Prior Equity Dash substantive discrepancy | **CLOSED** |

Residual binary differences: packaging / CRC / styles / calcChain (38 ZIP parts) — **non-substantive** for economics logic.

---

## Disposition

# **CLOSED — NON-SUBSTANTIVE CURRENT-WORKBOOK DIFFERENCE**

- Current confirmed vs current live: calc/semantic equivalent.  
- Historical hash change (`87EF7439…` → `D07560CA…`) is **governance/history**, closed by re-freeze acceptance.  
- **Not** a technical calculation blocker.  
- Live may remain non-identical until optionally refreshed from the **approved** GM; live is not the freeze identity.  
- **Do not** silently promote live as GM.  
- Formal PO approval of confirmed SHA `D07560CA…BFEA` is **CLOSED** (`GOLDEN_MASTER_APPROVAL.md`).

---

## Closed domain decisions (not reopened)

Equity Share INPUT · C5 DERIVED · Fiscal LAW TABLE · AU14 expected · critical-path literals 829/829 · Ec_IO unresolved 0 · ADR-0010
