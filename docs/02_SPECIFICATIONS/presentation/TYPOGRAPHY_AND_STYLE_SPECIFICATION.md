# Typography and Style Specification

**Status:** **READY** (presentation metadata)  
**Source GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**Evidence:** `PRESENTATION_AUDIT_EXTRACT.json`  
**GM modified:** **No**

---

## 1. Font families (observed frequency, visible samples)

| Font | Approx. count | Typical role |
|------|--------------:|--------------|
| **Century Gothic** | 3311 | Dominant body / NCF / equity / many tables |
| **Calibri** | 827 | Ec_IO drivers, fiscal terms, some labels |
| **Montserrat** | 810 | Secondary branded headers/sections (where used) |
| **Arial** | 142 | RESULTS Equity KPI values |
| **Arial Narrow** | 10 | Rare |

**PEMS:** Prefer a single UI font stack for readability; map **Century Gothic / Calibri / Arial** roles rather than requiring three fonts everywhere (L3). Semantic content does not depend on font family.

---

## 2. Font sizes (observed)

| Size | Approx. count | Role |
|-----:|--------------:|------|
| **11** | 4721 | Body default |
| **10** | 346 | RESULTS KPI numbers |
| **14 / 20 / 22** | rare | Titles |
| **9 / 7** | rare | Dense labels |

---

## 3. Emphasis

| Style | Observed |
|-------|----------|
| Bold | Inputs/selectors (Ec_IO C4, G20), RESULTS KPIs, section labels |
| Italic | Not dominant in sample |
| Underline | Rare |
| Font colour | Theme/default black primarily; not a sole semantic classifier |

---

## 4. Fills (observed)

| Fill | Approx. count | Note |
|------|--------------:|------|
| none / transparent | 3840 | Majority |
| solid theme:5 | 410 | Themed section fill |
| solid theme:2 | 339 | Light themed (e.g. Ec_IO C5 sample) |
| solid theme:9 / 0 / 6 | various | Headers / bands |
| solid `FFFFFF00` (yellow) | 47 | Highlight — **do not infer INPUT solely from yellow** |

Theme colours resolve differently by Excel theme; record as **theme indices**, not assumed hex palette.

---

## 5. Representative samples

| Location | Font | Size | Bold | Fill | Role |
|----------|------|------|------|------|------|
| Ec_IO!C4 | Calibri | 11 | Yes | theme:0 solid | Analysis type (DV list) |
| Ec_IO!C15 | Calibri | 11 | No | none | Hurdle % |
| Equity Dash!C4 | Century Gothic | 11 | Yes | none | **INPUT** share |
| Equity Dash!C5 | Century Gothic | 11 | No | theme:0 solid | **DERIVED** formula |
| RESULTS!J7 | Arial | 10 | Yes | theme:0 solid | KPI NPV |
| Fiscal!W18 | Calibri | 11 | No | none | LAW rate |

---

## 6. LEVEL classification

| Aspect | Level |
|--------|-------|
| Bold on key KPIs / labels for hierarchy | L2 |
| Exact Century Gothic vs Calibri | L3 |
| Theme fill indices | L3 (unless later proven as sole input marker — **not proven**) |
