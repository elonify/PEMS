# CHART_SPECIFICATION.md

**Project:** Elonify Petroleum Economics Modeling System (PEMS)  
**Documentation Baseline:** v2.1  
**Status:** Chart engine specification  

---

## 1. Purpose

Specifies chart architecture, data flow, dynamic behaviour, and **mandatory dual-axis zero alignment**.

Charts must not depend on Excel VBA. Charts consume **ChartDataset** domain objects only.

---

## 2. Architecture

```text
RunResult / domain series
        ↓
  ChartDataset builder (application/services)
        ↓
  ChartFactory  →  ChartBuilder  →  ChartRenderer  →  ChartExporter
```

| Component | Responsibility |
|-----------|----------------|
| ChartFactory | Select template by chart type |
| ChartBuilder | Bind series, axes, titles, units, legends |
| ChartRenderer | Draw via chosen library (ADR-0008) |
| ChartExporter | PNG, SVG, embed in reports |

---

## 3. Chart Families

Production, cash flow, revenue, fiscal take, NPV, IRR, economic limit, sensitivity, Monte Carlo distributions, tornado, spider, waterfall — as required by Golden Master and product roadmap.

Each Excel chart maps to one PEMS chart template (WORKBOOK_MAPPING).

---

## 4. ChartDataset Contract (minimum)

| Field | Description |
|-------|-------------|
| chart_type | enum/string |
| title | string |
| x_axis | label, categories or numeric x |
| series[] | name, values[], axis_role (`primary` \| `secondary`), style hints |
| units | per series |
| options | stacked, legend, etc. |

---

## 5. Dynamic Chart Behaviour

Charts **must** recompute layout when data changes:

- Recompute series extents from current data  
- Recompute tick marks and labels  
- Recompute dual-axis ranges using §6 algorithm  
- Update legend and tooltips  
- Support zoom/pan where enabled without permanently corrupting zero alignment policy (reset restores policy)  

Dynamic scaling is mandatory (PROJECT_ROADMAP / IMPLEMENTATION_SEQUENCE).

---

## 6. Dual-Axis Zero Alignment (mandatory)

### 6.1 Requirement

When a chart has **primary** and **secondary** Y-axes, and **both axes logically contain zero**, the rendered chart **must** align:

- zero on the primary Y-axis  
- with zero on the secondary Y-axis  

This must hold **dynamically** for changing datasets. It must **not** depend on VBA macros.

### 6.2 When alignment applies

Apply when all are true:

1. Chart uses two Y-axes.  
2. Primary axis data range requires display of both positive and negative values **or** zero is within the chosen padded range that includes data min/max.  
3. Secondary axis likewise.  
4. Product policy for that chart type requests zero visibility (default: **yes** when data straddles or touches zero; always for cash-flow-like series unless template overrides).  

If an axis is strictly positive (or strictly negative) and template sets `force_zero=false`, alignment rules still apply if zero is included in the axis range; if zero is not included, dual-zero alignment is **not** required for that axis pair.

### 6.3 Algorithm (normative)

Goal: choose primary range `[Pmin, Pmax]` and secondary range `[Smin, Smax]` such that the pixel/normalized position of 0 is identical on both axes.

**Step A — Data extents**

For primary series: `p_raw_min`, `p_raw_max`  
For secondary series: `s_raw_min`, `s_raw_max`

**Step B — Include zero when required**

If primary must show zero:  
`p_min0 = min(p_raw_min, 0)`, `p_max0 = max(p_raw_max, 0)`  
Else use raw min/max.  
Same for secondary → `s_min0`, `s_max0`.

**Step C — Padding**

Apply symmetric or proportional padding factor `pad` (configurable, default e.g. 5%):

```text
p_span = p_max0 - p_min0  (if 0, use library minimum span)
Pmin = p_min0 - pad * p_span
Pmax = p_max0 + pad * p_span
```

Same for secondary → `Smin`, `Smax`. Re-include zero after padding if policy requires zero in view:

```text
Pmin = min(Pmin, 0); Pmax = max(Pmax, 0)   # if force_zero
Smin = min(Smin, 0); Smax = max(Smax, 0)
```

**Step D — Zero fraction**

```text
# Guard zero-length ranges
fp = (0 - Pmin) / (Pmax - Pmin)   # fraction from bottom; 0 at bottom, 1 at top
fs = (0 - Smin) / (Smax - Smin)
```

If either denominator is 0, expand that axis by a minimum epsilon defined in chart config.

**Step E — Align fractions**

If `|fp - fs| <= epsilon_align` (default 1e-6), done.

Otherwise expand one or both axes so that `fp == fs == f*` for a chosen target.

**Recommended method — expand about data while locking zero position:**

1. Choose target zero fraction `f*`:

   - Option **midpoint**: `f* = 0.5` only if both sides need balanced view (optional template flag).  
   - Option **preserve primary** (default): `f* = fp` after Step D on primary; adjust secondary only.  
   - Option **max headroom**: choose `f*` to minimise total expansion (optional optimisation).

2. **Default policy for PEMS: preserve primary zero fraction; expand secondary** so `fs = fp`.

   Given `f* = fp`, secondary range must satisfy:

   ```text
   (0 - Smin') / (Smax' - Smin') = f*
   ```

   Keep secondary data inside range with padding:

   ```text
   # Let secondary data bounds after pad be s_lo, s_hi (must satisfy s_lo <= min data, s_hi >= max data, and 0 in range if required)
   # Expand so zero at f*:
   # 0 = Smin' + f* * (Smax' - Smin')
   # Smin' = -f* * Span'
   # Smax' = (1 - f*) * Span'
   # Choose Span' large enough that Smin' <= s_lo and Smax' >= s_hi
   Span_needed_lo = (s_lo < 0) ? (-s_lo / f*) : 0          # if f* > 0
   Span_needed_hi = (s_hi > 0) ? (s_hi / (1 - f*)) : 0     # if f* < 1
   Span' = max(Span_needed_lo, Span_needed_hi, min_span)
   Smin' = -f* * Span'
   Smax' = (1 - f*) * Span'
   ```

   Handle edge cases `f* ≈ 0` or `f* ≈ 1` (zero on axis end): use minimum opposite headroom so labels remain readable.

3. Optionally **expand both** axes to a common `f*` if secondary expansion alone would be extreme (threshold configurable); document choice in chart template.

**Step F — Apply to renderer**

Set axis limits explicitly; disable chart-library auto-scale that would break alignment, or re-run algorithm after library suggestions.

### 6.4 Edge cases

| Case | Behaviour |
|------|-----------|
| All primary values > 0, secondary straddles 0 | If primary force_zero, include 0 on primary then align; else align only if both include 0 |
| Empty series | Do not render axes; show placeholder |
| Single point | Synthetic span from config |
| Very large magnitude ratio | Expand axes; scientific tick formatting |
| Log scale | Dual-axis zero alignment **N/A** (zero not on log scale); templates must not request log dual-zero |
| Secondary unused | Single axis; no alignment routine |

### 6.5 Validation approach

- Unit tests for pure function `compute_aligned_axis_limits(primary_minmax, secondary_minmax, policy) -> ranges`  
- Property: normalized zero position equal within epsilon when both ranges contain 0  
- Property: all data points remain within ranges  
- Golden visual tests optional; numeric limit tests mandatory  
- Regression fixtures with changing datasets proving dynamic recompute  

---

## 7. Interaction

Zoom, pan, interactive legends, export — per IMPLEMENTATION_SEQUENCE Phase 12. Zoom may temporarily decouple axes only if UI offers “Reset axes” restoring §6 policy.

---

## 8. Theming

Theme support via configuration; colours must remain readable; do not encode data only by colour when avoidable.

---

## 9. Non-Goals

- Excel chart object model parity pixel-for-pixel  
- VBA macro execution  
- Calculating economics inside chart code  

---

## 10. Traceability

Excel chart → Chart template → ChartDataset builder → Renderer → Validation tests for series values and axis policy.
