# Semantic Mapping SHA Rebind Determination

**Date:** 2026-08-03  
**ACTIVE GM SHA:** `D07560CA6C1A762716E1927A130E7CA697DB0AB9BDA8E8A33C7A0ACBB6FDBFEA`  
**PREVIOUS DOCUMENTED GM HASH — SUPERSEDED BY RE-FREEZE:** `87EF7439A8F19C52B5B948D379D1752B327144CCDBC36758A780A93EC71121FB`

---

## SHA-bound artefacts (regenerated — not mere text edit)

| Artefact | Action |
|----------|--------|
| `catalogue/*` (formula/cell catalogues, extraction_summary) | **Full re-extract** from confirmed GM ACTIVE SHA |
| `Validation_Datasets/expected_outputs/*` | **Full re-extract** |
| `Validation_Datasets/scenarios/GTC-001_*` | **Full rebuild** via post-extract |
| `catalogue/ACTIVE_VS_HISTORICAL_DIFF.json` / REEXTRACT_REPORT | Regenerated with post-extract |

## SHA-referenced semantic classification (rebound after content-equivalence determination)

| Artefact | Determination | Action |
|----------|---------------|--------|
| `CRITICAL_PATH_LITERAL_CLASSIFICATION.csv` | Content-equivalent classifications; cell keys/values unchanged relative to critical-path work; 0 semantic conf/live diffs | Rebind `golden_master_sha256` column to ACTIVE SHA |
| `CRITICAL_PATH_LITERAL_REGISTER_FULL.csv` | Same | Rebind |
| `PO_CLASSIFICATION_OVERRIDES.csv` | Same | Rebind |
| `CRITICAL_PATH_LITERAL_SUMMARY.json` | Same | Rebind + superseded field |
| Header SHA lines in semantic MD maps | Citation only | Point to ACTIVE SHA; retain SUPERSEDED note where historical |

**Not regenerated from scratch:** full critical-path re-classification workshop (829 cells) — unnecessary because formula/array/semantic cell content equivalence was verified and domain closures unchanged.

**Not SHA-content-bound:** pure analysis narratives (dependency order logic, closed decisions) — SHA headers updated for identity only.
