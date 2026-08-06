"""CR / NCF module — CR_NCF_CONTRACT.md + CR_NCF_PARAMETER_CONTRACT.md.

Groups: CR-G1…CR-G4, PN-G1…PN-G5 (via intermediates + documented AE/AF/disc/IRR), EQ-G1.
HT/CIT full engines: catalogue path — annual tax/allowable intermediates imported for GTC parity
(selected intermediate path), then Project NCF construction is computed.

AU14 #NUM! → NO_VALID_IRR (closed decision).
F-G12 loan terms: FLGT AN/AO/AP via imported Project intermediates or FLGT extras.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pems.domain.case_input import CaseInput

try:
    import numpy_financial as npf
except ImportError:  # pragma: no cover
    npf = None  # type: ignore


def _series_to_map(series: list[list[float]] | None) -> dict[int, float]:
    if not series:
        return {}
    out: dict[int, float] = {}
    for pair in series:
        if len(pair) < 2:
            continue
        out[int(pair[0])] = float(pair[1])
    return out


def _g(m: dict[int, float], y: int, default: float = 0.0) -> float:
    return float(m.get(y, default) or 0.0)


def excel_irr(cashflows: list[float]) -> float | str:
    """Excel IRR semantics; return NO_VALID_IRR when no valid root (AU14 #NUM!)."""
    # treat None as 0
    cfs = [float(x or 0.0) for x in cashflows]
    if not cfs or all(v == 0.0 for v in cfs):
        return "NO_VALID_IRR"
    # need both signs for conventional IRR
    pos = any(v > 0 for v in cfs)
    neg = any(v < 0 for v in cfs)
    if not (pos and neg):
        return "NO_VALID_IRR"
    if npf is None:
        return _irr_newton(cfs)
    try:
        r = float(npf.irr(cfs))
    except Exception:
        return "NO_VALID_IRR"
    if r != r or r == float("inf") or r == float("-inf"):  # NaN/inf
        return "NO_VALID_IRR"
    return r


def _irr_newton(cfs: list[float], guess: float = 0.1, tol: float = 1e-12, max_iter: int = 100) -> float | str:
    r = guess
    for _ in range(max_iter):
        npv = 0.0
        d = 0.0
        for t, c in enumerate(cfs):
            den = (1.0 + r) ** t
            if den == 0:
                return "NO_VALID_IRR"
            npv += c / den
            if t > 0:
                d -= t * c / ((1.0 + r) ** (t + 1))
        if abs(d) < 1e-18:
            return "NO_VALID_IRR"
        r_new = r - npv / d
        if abs(r_new - r) < tol:
            return r_new
        r = r_new
    return "NO_VALID_IRR"


@dataclass
class CrEconYear:
    year: int
    oil_rev: float = 0.0
    gas_rev: float = 0.0
    total_rev: float = 0.0
    royalties: float = 0.0
    fl_govt: float = 0.0
    expensed_capex: float = 0.0
    capex_depr: float = 0.0
    opex: float = 0.0
    eligible_adjunct: float = 0.0  # J
    eligible_total: float = 0.0  # K
    crl: float = 0.0  # L
    profit_oil: float = 0.0  # M
    cost_cf: float = 0.0  # N
    ecr: float = 0.0  # O
    project_total_oil: float = 0.0  # P
    cum_oil: float = 0.0  # Q
    hg_split: float = 0.0  # R
    contractor_split: float = 0.0  # S
    contractor_oil: float = 0.0  # T
    government_oil: float = 0.0  # U


@dataclass
class CrNcfResult:
    cr_years: list[CrEconYear] = field(default_factory=list)
    # Project annual
    years: list[int] = field(default_factory=list)
    revenue_b: dict[int, float] = field(default_factory=dict)
    host_ae: dict[int, float] = field(default_factory=dict)
    contractor_af: dict[int, float] = field(default_factory=dict)
    disc_host_ag: dict[int, float] = field(default_factory=dict)
    disc_contractor_ah: dict[int, float] = field(default_factory=dict)
    disc_cncf_ai: dict[int, float] = field(default_factory=dict)
    payout_aj: dict[int, float] = field(default_factory=dict)
    # Totals / metrics
    ag51: float = 0.0
    ah51: float = 0.0
    ae51: float = 0.0
    af51: float = 0.0
    ab51: float = 0.0
    ac51: float = 0.0
    ad51: float = 0.0
    aj51: float = 0.0
    ag58_irr: float | str = "NO_VALID_IRR"
    au12_irr: float | str = "NO_VALID_IRR"
    au14_irr: float | str = "NO_VALID_IRR"
    equity_ag51: float = 0.0
    equity_ah51: float = 0.0
    # Equity annual maps (Equity_NCF_Con AF / AH / AI) — Slice A share-homogeneous path
    equity_contractor_af: dict[int, float] = field(default_factory=dict)  # AF undisc
    equity_dncf_by_year: dict[int, float] = field(default_factory=dict)  # AH annual DNCF
    equity_cum_dncf_by_year: dict[int, float] = field(default_factory=dict)  # AI cum DNCF
    # CR samples
    cr_g8: float | None = None
    cr_h8: float | None = None
    cr_i8: float | None = None
    deferred: list[str] = field(default_factory=list)

    def cell_map(self) -> dict[tuple[str, str], Any]:
        m: dict[tuple[str, str], Any] = {
            ("Project_NCF", "AG51"): self.ag51,
            ("Project_NCF", "AH51"): self.ah51,
            ("Project_NCF", "AE51"): self.ae51,
            ("Project_NCF", "AF51"): self.af51,
            ("Project_NCF", "AB51"): self.ab51,
            ("Project_NCF", "AC51"): self.ac51,
            ("Project_NCF", "AD51"): self.ad51,
            ("Project_NCF", "AJ51"): self.aj51,
            ("Project_NCF", "AG58"): self.ag58_irr,
            ("Project_NCF", "AU12"): self.au12_irr,
            ("Project_NCF", "AU14"): self.au14_irr,
            ("Equity_NCF_Con", "AG51"): self.equity_ag51,
            ("Equity_NCF_Con", "AH51"): self.equity_ah51,
        }
        if self.cr_g8 is not None:
            m[("CR Econ", "G8")] = self.cr_g8
        if self.cr_h8 is not None:
            m[("CR Econ", "H8")] = self.cr_h8
        if self.cr_i8 is not None:
            m[("CR Econ", "I8")] = self.cr_i8
        return m


def profit_oil_hg_split(cum_oil_mmbbl: float, thresholds: list[float], rates: list[float]) -> float:
    """CR Econ R progressive average profit-oil HG split vs cum production Q."""
    q = float(cum_oil_mmbbl or 0.0)
    if q == 0:
        return 0.0
    w = thresholds
    x = rates
    if len(w) < 5 or len(x) < 6:
        return x[0] if x else 0.0
    # Mirror nested IF in CR R5 (W60…W64 thresholds, X60…X65 rates)
    if q <= w[0]:
        return x[0]
    if q <= w[1]:
        return (x[0] * w[0] + (q - w[0]) * x[1]) / q
    if q <= w[2]:
        return (x[0] * w[0] + x[1] * (w[1] - w[0]) + x[2] * (q - w[1])) / q
    if q <= w[3]:
        return (
            x[0] * w[0]
            + x[1] * (w[1] - w[0])
            + x[2] * (w[2] - w[1])
            + x[3] * (q - w[2])
        ) / q
    if q <= w[4]:
        return (
            x[0] * w[0]
            + x[1] * (w[1] - w[0])
            + x[2] * (w[2] - w[1])
            + x[3] * (w[3] - w[2])
            + x[4] * (q - w[3])
        ) / q
    return x[5]


class CrNcfModule:
    name = "cr_ncf"
    contract_path = "docs/02_SPECIFICATIONS/modules/CR_NCF_CONTRACT.md"

    DEFERRED = [
        "Full HT_NCF_Oil / CIT_NCF line-by-line engine (catalogue; intermediates imported for GTC)",
        "Hidden HT_NCF / CIT_NCF / Project_NCF_Con as primary surfaces",
        "RESULTS presentation aggregation",
        "Analysis data tables / Monte Carlo",
    ]

    DEFAULT_PO_THRESHOLDS = [50.0, 100.0, 250.0, 750.0, 1500.0]
    DEFAULT_PO_RATES = [0.05, 0.1, 0.15, 0.25, 0.35, 0.45]

    def run(self, case: CaseInput, upstream: dict[str, Any] | None = None) -> CrNcfResult:
        upstream = upstream or {}
        result = CrNcfResult(deferred=list(self.DEFERRED))

        flgt = upstream.get("flgt")
        costs = upstream.get("costs")
        prod = upstream.get("production")

        # --- CR Econ from FLGT + Costs ---
        cr_rows = self._build_cr_econ(case, flgt, costs, prod)
        result.cr_years = cr_rows
        # sample G8/H8/I8 = first year with production-aligned Cap_Allow path year 2027 often row index
        for row in cr_rows:
            if row.year == (case.project_start_year or 2027):
                result.cr_g8 = row.expensed_capex
                result.cr_h8 = row.capex_depr
                result.cr_i8 = row.opex
                break

        # --- Project NCF construction ---
        inter = case.extras.get("project_ncf_intermediates") or {}
        # inter: dict col -> {year: value} or list pairs
        inter_maps = {k: self._as_year_map(v) for k, v in inter.items()}

        years = sorted(
            set(inter_maps.get("A", {}))
            | set(inter_maps.get("B", {}))
            | {r.year for r in cr_rows}
        )
        if not years and case.project_start_year:
            years = list(range(int(case.project_start_year) - 3, int(case.project_start_year) + 45))
        result.years = years

        hurdle = float(case.hurdle_rate or 0.0)
        n14 = float(case.extras.get("analysis_n14", 0.0) or 0.0)
        start = int(case.project_start_year or (years[0] if years else 0))
        d22 = int(case.extras.get("price_path_end_year") or (start + int(case.project_life_years or 15)))
        # AF formula: Equity Dash!L(row-4) per year (acquisition schedule), not constant L4
        equity_l_by_year = self._as_year_map(case.extras.get("equity_l_by_year", {}))

        # loan terms from FLGT sheet (import) or flgt result extras
        flgt_an = self._as_year_map(case.extras.get("flgt_an", {}))
        flgt_ao = self._as_year_map(case.extras.get("flgt_ao", {}))
        flgt_ap = self._as_year_map(case.extras.get("flgt_ap", {}))

        # cost W/X from Cap_Allow when not in intermediates
        w_map = inter_maps.get("W", {})
        x_map = inter_maps.get("X", {})
        if not w_map and costs is not None:
            # FP oil+gas by year
            for y in years:
                w_map[y] = float(costs.oil.expensed_capex.get(y, 0) or 0) + float(
                    costs.gas.expensed_capex.get(y, 0) or 0
                )
                x_map[y] = float(costs.oil.capitalized_costs.get(y, 0) or 0) + float(
                    costs.gas.capitalized_costs.get(y, 0) or 0
                ) + float(case.extras.get("equity_l4", 0.0) or 0.0)

        af_list: list[float] = []
        ak_list: list[float] = []
        prev_ai = 0.0
        run_ai = 0.0

        ab_sum = ac_sum = ad_sum = 0.0

        for y in years:
            gate = 1.0 if y <= d22 else 0.0
            # Revenue B: prefer intermediate; else FLGT W+X; else CR
            if y in inter_maps.get("B", {}):
                b = _g(inter_maps["B"], y)
            elif flgt is not None:
                b = float(flgt.oil_revenue.get(y, 0) or 0) + float(flgt.gas_revenue.get(y, 0) or 0)
            else:
                b = next((r.total_rev for r in cr_rows if r.year == y), 0.0)

            e = _g(inter_maps.get("E", {}), y)
            f = _g(inter_maps.get("F", {}), y)
            g = _g(inter_maps.get("G", {}), y)
            h = _g(inter_maps.get("H", {}), y)
            i = _g(inter_maps.get("I", {}), y)
            j = _g(inter_maps.get("J", {}), y)
            o = _g(inter_maps.get("O", {}), y)
            p = _g(inter_maps.get("P", {}), y)
            q = _g(inter_maps.get("Q", {}), y)
            r = _g(inter_maps.get("R", {}), y)
            w = _g(w_map, y)
            x = _g(x_map, y)
            ab = _g(inter_maps.get("AB", {}), y)
            ac = _g(inter_maps.get("AC", {}), y)
            ad = _g(inter_maps.get("AD", {}), y)

            ab_sum += ab * gate
            ac_sum += ac * gate
            ad_sum += ad * gate

            # AE Host = (AD+AC+AB+R+Q+P+O+I+H+G+F)*gate
            ae = (ad + ac + ab + r + q + p + o + i + h + g + f) * gate
            # AF Contractor
            an = _g(flgt_an, y)
            ao = _g(flgt_ao, y)
            ap = _g(flgt_ap, y)
            eq_l = _g(equity_l_by_year, y)
            af = (b - ae - w - x - e - j - ao - ap + an - eq_l) * gate

            # Discount
            df = (1.0 + hurdle * (1.0 + n14)) ** (y - start) if gate else 1.0
            ag = (ae / df) * gate if df else 0.0
            ah = (af / df) * gate if df else 0.0

            run_ai = (run_ai + ah) if gate else run_ai
            ai = run_ai * gate
            # AJ payout fragment
            if ai < 0:
                aj = 1.0
            elif prev_ai < 0 and ai > 0:
                aj = (-prev_ai / (ai - prev_ai)) if (ai - prev_ai) != 0 else 0.0
            else:
                aj = 0.0
            prev_ai = ai if gate else prev_ai

            result.revenue_b[y] = b
            result.host_ae[y] = ae
            result.contractor_af[y] = af
            result.disc_host_ag[y] = ag
            result.disc_contractor_ah[y] = ah
            result.disc_cncf_ai[y] = ai
            result.payout_aj[y] = aj

            af_list.append(af)
            ak_list.append(_g(inter_maps.get("AK", {}), y))

        result.ag51 = sum(result.disc_host_ag.values())
        result.ah51 = sum(result.disc_contractor_ah.values())
        result.ae51 = sum(result.host_ae.values())
        result.af51 = sum(result.contractor_af.values())
        result.ab51 = ab_sum
        result.ac51 = ac_sum
        result.ad51 = ad_sum
        result.aj51 = sum(result.payout_aj.values())

        # IRR windows: AF5:AF49 and AF5:AF40 — use ordered years list length
        # Build AF vector in year order for rows corresponding to Project rows 5..49
        af_ordered = [result.contractor_af.get(y, 0.0) for y in years]
        # Pad/truncate to 45 periods if needed to match IRR(AF5:AF49)
        while len(af_ordered) < 45:
            af_ordered.append(0.0)
        af_45 = af_ordered[:45]
        af_36 = af_ordered[:36]
        result.ag58_irr = excel_irr(af_45)
        result.au12_irr = excel_irr(af_36)
        ak_ordered = [_g(inter_maps.get("AK", {}), y) for y in years]
        while len(ak_ordered) < 45:
            ak_ordered.append(0.0)
        result.au14_irr = excel_irr(ak_ordered[:45])

        eq = float(case.equity_share_company_1 or 0.0)
        # Scalar equity NPVs: preserve project-NPV × share (GTC AG51/AH51).
        result.equity_ag51 = result.ag51 * eq
        result.equity_ah51 = result.ah51 * eq

        # --- Equity year-keyed AF / AH / AI (Slice A) ---
        # GM evidence (Confirmed-2026-08-03 baseline): Equity_NCF_Con is a
        # share-homogeneous parallel of Project_NCF — cached equity AF/AH equal
        # project AF/AH × Equity Dash!C4 for all sampled years. Slice A therefore
        # derives equity maps from project contractor_af × share rather than a
        # full CIT/HT equity engine rebuild. Re-validate if equity CIT ever
        # diverges from pure C4 scaling.
        # AH discounts equity AF with the same DF as project AH.
        # AI = running SUM(AH) with strict year < D22 (Equity_NCF_Con!AI, not ≤).
        run_eq_ai = 0.0
        for y in years:
            eaf = float(result.contractor_af.get(y, 0.0) or 0.0) * eq
            gate = 1.0 if y <= d22 else 0.0
            df = (1.0 + hurdle * (1.0 + n14)) ** (y - start) if gate else 1.0
            edncf = (eaf / df) if df else 0.0
            run_eq_ai += edncf
            # Equity AI gate is strict < D22 (Project AI uses ≤).
            ecum = run_eq_ai if y < d22 else 0.0
            result.equity_contractor_af[y] = eaf
            result.equity_dncf_by_year[y] = edncf
            result.equity_cum_dncf_by_year[y] = ecum

        return result

    def _build_cr_econ(self, case, flgt, costs, prod) -> list[CrEconYear]:
        law = case.extras.get("fiscal_law") or {}
        crl_new = float(law.get("crl_new_acreage", 0.7) or 0.7)
        crl_oml = float(law.get("crl_converted_oml", 0.6) or 0.6)
        is_new = (case.licence_lease_status or "") == "New Acreage" or (
            case.licence_lease_status or ""
        ) == str(law.get("crl_new_label", "New Acreage"))
        crl_rate = crl_new if is_new else crl_oml
        psc = (case.pfs_contract_type or "") == "PSC/SC"

        po_thr = law.get("profit_oil_thresholds") or self.DEFAULT_PO_THRESHOLDS
        po_rates = law.get("profit_oil_rates") or self.DEFAULT_PO_RATES

        # year maps from flgt/costs
        if flgt is not None:
            years = sorted(
                set(flgt.oil_revenue) | set(flgt.gas_revenue) | set(getattr(flgt, "years", []) or [])
            )
        else:
            years = sorted(_series_to_map(case.oil_block_annual).keys())

        oil_fp = _series_to_map(case.oil_tc_exploration)  # FP=FF exploration as expensed on GM path
        # Better: use costs result
        oil_exp = oil_wells = oil_opex = oil_sln = oil_acq = {}
        gas_exp = gas_opex = gas_sln = gas_acq = gas_cap = {}
        if costs is not None:
            oil_exp = costs.oil.expensed_capex
            oil_opex = costs.oil.opex
            oil_sln = costs.oil.sln
            oil_acq = costs.oil.acq_allowance
            oil_cap = costs.oil.capitalized_costs
            gas_exp = costs.gas.expensed_capex
            gas_opex = costs.gas.opex
            gas_sln = costs.gas.sln
            gas_acq = costs.gas.acq_allowance
            gas_cap = costs.gas.capitalized_costs
        else:
            oil_exp = _series_to_map(case.oil_tc_exploration)
            oil_opex = _series_to_map(case.oil_tc_opex)
            oil_sln = _series_to_map(case.oil_sln_by_year)
            oil_acq = _series_to_map(case.oil_acq_allowance_by_year)
            gas_opex = _series_to_map(case.gas_tc_opex)
            gas_exp = _series_to_map(case.gas_tc_exploration)
            gas_sln = _series_to_map(case.gas_sln_by_year)
            gas_acq = _series_to_map(case.gas_acq_allowance_by_year)
            oil_cap = gas_cap = {}

        j_map = self._as_year_map(case.extras.get("cit_oil_z", {}))
        n_prev = 0.0
        rows: list[CrEconYear] = []
        cum_oil = 0.0

        for y in years:
            row = CrEconYear(year=y)
            if flgt is not None:
                row.oil_rev = float(flgt.oil_revenue.get(y, 0) or 0)
                row.gas_rev = float(flgt.gas_revenue.get(y, 0) or 0)
                row.total_rev = float(flgt.total_revenue.get(y, 0) or 0)
                row.royalties = float(flgt.royalty_sum.get(y, 0) or 0)
                row.fl_govt = (
                    float(flgt.rentals.get(y, 0) or 0)
                    + float(flgt.hcdt_oil.get(y, 0) or 0)
                    + float(flgt.nddc_oil.get(y, 0) or 0)
                    + float(flgt.nddc_gas.get(y, 0) or 0)
                    + float(flgt.hcdt_gas.get(y, 0) or 0)
                )
                cum_oil = float(flgt.oil_annual.get(y, 0) or 0) + (
                    rows[-1].cum_oil if rows else 0.0
                )
                # prefer production cum if available
                if prod is not None and getattr(prod, "oil_cum_series", None):
                    cum_oil = float(prod.oil_cum_series.get(y, cum_oil) or cum_oil)
            else:
                row.total_rev = 0.0

            row.expensed_capex = _g(oil_exp, y) + _g(gas_exp, y)
            row.capex_depr = _g(oil_sln, y) + _g(oil_acq, y) + _g(gas_sln, y) + _g(gas_acq, y)
            row.opex = _g(oil_opex, y) + _g(gas_opex, y)
            row.eligible_adjunct = _g(j_map, y)
            row.eligible_total = (
                row.fl_govt + row.capex_depr + row.opex + row.expensed_capex + row.eligible_adjunct
            )
            row.crl = crl_rate * (row.total_rev - row.royalties)
            row.profit_oil = row.total_rev - row.royalties - row.crl
            # N carry: IF(AND(G=0,D=0),0,IF(L-K+N4<0,L-K+N4,0))
            if row.expensed_capex == 0 and row.total_rev == 0:
                row.cost_cf = 0.0
            else:
                trial = row.crl - row.eligible_total + n_prev
                row.cost_cf = trial if trial < 0 else 0.0
            n_prev = row.cost_cf
            # O ECR simplified: max(0, K-L) style not fully expanded — use 0 when cost_cf path used
            row.ecr = 0.0
            row.project_total_oil = row.ecr + row.profit_oil
            row.cum_oil = cum_oil
            row.hg_split = profit_oil_hg_split(cum_oil, list(po_thr), list(po_rates))
            row.contractor_split = 0.0 if cum_oil == 0 else (1.0 - row.hg_split)
            row.contractor_oil = row.contractor_split * row.project_total_oil
            row.government_oil = (row.project_total_oil - row.contractor_oil) if psc else 0.0
            rows.append(row)
        return rows

    def _as_year_map(self, v: Any) -> dict[int, float]:
        if v is None:
            return {}
        if isinstance(v, dict):
            return {int(k): float(val or 0) for k, val in v.items()}
        if isinstance(v, list):
            return _series_to_map(v)
        return {}
