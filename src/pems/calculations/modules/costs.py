"""Costs / Cap_Allow module — COSTS_PARAMETER_CONTRACT.md G1–G8.

Selected-field consolidated path for GTC parity (same pattern as Production).
Oil and gas stacks remain parallel. Units: $mm annual.
Does not re-host Fiscal Terms_PIA law rules — only CA rate surface + schedule application.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pems.domain.case_input import CaseInput


def _series_to_map(series: list[list[float]] | None) -> dict[int, float]:
    if not series:
        return {}
    out: dict[int, float] = {}
    for pair in series:
        if len(pair) < 2:
            continue
        out[int(pair[0])] = float(pair[1])
    return out


def escalate_opex(
    base_opex: float,
    year: int,
    base_year: int,
    escalation_rate: float,
) -> float:
    """Block_TC FW path: base * (1+FW3)^(year - base_year).

    GM GTC has FW3=0 → factor 1.0. Not a generic inflation CaseInput.
    """
    return float(base_opex) * (1.0 + float(escalation_rate)) ** (int(year) - int(base_year))


def apply_history_mask(
    year: int,
    value: float,
    *,
    analysis_type: str | None,
    history_year: int | None,
    history_end_year: int | None,
) -> float:
    """History filter as on Block_TC FY–GB / escalated path."""
    if analysis_type != "History":
        return value
    if history_year is not None and year < int(history_year):
        return 0.0
    if history_end_year is not None and year > int(history_end_year):
        return 0.0
    return value


def discount_factor(hurdle_rate: float, year: int, base_year: int) -> float:
    """PV factor 1/(1+r)^(year-base). Year 0 → 1."""
    return 1.0 / ((1.0 + float(hurdle_rate)) ** (int(year) - int(base_year)))


@dataclass
class StreamCostResult:
    """One of oil or gas Cap_Allow stack."""

    years: list[int] = field(default_factory=list)
    exploration: dict[int, float] = field(default_factory=dict)  # FF
    capex_wells: dict[int, float] = field(default_factory=dict)  # FG
    capex_facilities: dict[int, float] = field(default_factory=dict)  # FH
    opex: dict[int, float] = field(default_factory=dict)  # FI
    abandonment: dict[int, float] = field(default_factory=dict)
    duties: dict[int, float] = field(default_factory=dict)  # FN
    vat: dict[int, float] = field(default_factory=dict)  # FO
    expensed_capex: dict[int, float] = field(default_factory=dict)  # FP
    capitalized_costs: dict[int, float] = field(default_factory=dict)  # FQ
    disc_capex: dict[int, float] = field(default_factory=dict)  # FK
    disc_opex: dict[int, float] = field(default_factory=dict)  # FL
    sln: dict[int, float] = field(default_factory=dict)  # GX
    acq_allowance: dict[int, float] = field(default_factory=dict)  # HC

    opex_undisc_total: float = 0.0  # FI48
    opex_disc_total: float = 0.0  # FL48
    capex_disc_total: float = 0.0  # FK48
    expensed_capex_total: float = 0.0  # FP48
    capitalized_costs_total: float = 0.0  # FQ48
    sln_total: float = 0.0
    acq_allowance_total: float = 0.0


@dataclass
class CostsResult:
    oil: StreamCostResult = field(default_factory=StreamCostResult)
    gas: StreamCostResult = field(default_factory=StreamCostResult)
    ca_rates: list[float] = field(default_factory=list)
    acquisition_cost: float | None = None

    # Ec_IO cost hub G6
    pv_opex_combined: float | None = None  # N16
    undisc_opex_combined: float | None = None  # S16
    pv_capex_combined: float | None = None  # N17
    undisc_capex_combined: float | None = None  # S17
    pv_tc_combined: float | None = None  # N18
    undisc_tc_combined: float | None = None  # S18

    deferred: list[str] = field(default_factory=list)

    def cell_map(self) -> dict[tuple[str, str], Any]:
        m: dict[tuple[str, str], Any] = {
            ("Cap_Allow", "FI48"): self.oil.opex_undisc_total,
            ("Cap_Allow", "FL48"): self.oil.opex_disc_total,
            ("Cap_Allow", "FK48"): self.oil.capex_disc_total,
            ("Cap_Allow", "FP48"): self.oil.expensed_capex_total,
            ("Cap_Allow", "FQ48"): self.oil.capitalized_costs_total,
            ("Cap_Allow Gas", "FI48"): self.gas.opex_undisc_total,
            ("Cap_Allow Gas", "FL48"): self.gas.opex_disc_total,
            ("Cap_Allow Gas", "FK48"): self.gas.capex_disc_total,
            ("Cap_Allow Gas", "FP48"): self.gas.expensed_capex_total,
            ("Cap_Allow Gas", "FQ48"): self.gas.capitalized_costs_total,
            ("Ec_IO", "N16"): self.pv_opex_combined,
            ("Ec_IO", "S16"): self.undisc_opex_combined,
            ("Ec_IO", "N17"): self.pv_capex_combined,
            ("Ec_IO", "S17"): self.undisc_capex_combined,
            ("Ec_IO", "N18"): self.pv_tc_combined,
            ("Ec_IO", "S18"): self.undisc_tc_combined,
        }
        for i, rate in enumerate(self.ca_rates[:5]):
            m[("Cap_Allow", f"FR{5 + i}")] = rate
        if self.acquisition_cost is not None:
            m[("Cap_Allow", "HB")] = self.acquisition_cost
        # G8 totals for interface evidence
        m[("Cap_Allow", "GX48")] = self.oil.sln_total
        m[("Cap_Allow", "HC48")] = self.oil.acq_allowance_total
        return {k: v for k, v in m.items() if v is not None}


class CostsModule:
    name = "costs"
    contract_path = "docs/02_SPECIFICATIONS/modules/COSTS_PARAMETER_CONTRACT.md"

    DEFERRED = [
        "Full multi-field Block_TC GUI editor",
        "Transport/processing cost categories (not in GM)",
        "Generic inflation CaseInput (not evidenced)",
        "Full Cap_Allow GX/HC array-formula reimplementation body (series surface for CR/HT)",
        "FLGT / CR-NCF / RESULTS engines",
        "Ec_IO revenue hub P16–P18 and NCF KPI hub G3–G15",
    ]

    DEFAULT_CA_RATES = [0.2, 0.2, 0.2, 0.2, 0.19]

    def run(self, case: CaseInput, upstream: dict[str, Any] | None = None) -> CostsResult:
        upstream = upstream or {}
        result = CostsResult(deferred=list(self.DEFERRED))

        r = case.hurdle_rate
        if r is None:
            r = 0.0
        duties = float(case.duties_rate or 0.0)
        vat = float(case.vat_rate or 0.0)

        result.ca_rates = list(case.ca_rates) if case.ca_rates else list(self.DEFAULT_CA_RATES)
        result.acquisition_cost = case.acquisition_cost

        e28 = None
        if case.project_start_year is not None:
            e28 = int(case.project_start_year) - 1
        if upstream.get("history_end_year_e28") is not None:
            e28 = int(upstream["history_end_year_e28"])

        result.oil = self._run_stream(
            case,
            exploration=case.oil_tc_exploration,
            wells=case.oil_tc_capex_wells,
            facilities=case.oil_tc_capex_facilities,
            opex=case.oil_tc_opex,
            abandonment=case.oil_tc_abandonment,
            sln=case.oil_sln_by_year,
            acq=case.oil_acq_allowance_by_year,
            hurdle=float(r),
            duties=duties,
            vat=vat,
            history_end=e28,
        )
        result.gas = self._run_stream(
            case,
            exploration=case.gas_tc_exploration,
            wells=case.gas_tc_capex_wells,
            facilities=case.gas_tc_capex_facilities,
            opex=case.gas_tc_opex,
            abandonment=case.gas_tc_abandonment,
            sln=case.gas_sln_by_year,
            acq=case.gas_acq_allowance_by_year,
            hurdle=float(r),
            duties=duties,
            vat=vat,
            history_end=e28,
        )

        # G6 — Ec_IO N16:S18
        result.pv_opex_combined = result.oil.opex_disc_total + result.gas.opex_disc_total
        result.undisc_opex_combined = result.oil.opex_undisc_total + result.gas.opex_undisc_total
        result.pv_capex_combined = result.oil.capex_disc_total + result.gas.capex_disc_total
        result.undisc_capex_combined = (
            result.oil.expensed_capex_total
            + result.oil.capitalized_costs_total
            + result.gas.expensed_capex_total
            + result.gas.capitalized_costs_total
        )
        result.pv_tc_combined = result.pv_opex_combined + result.pv_capex_combined
        result.undisc_tc_combined = result.undisc_opex_combined + result.undisc_capex_combined
        return result

    def _run_stream(
        self,
        case: CaseInput,
        *,
        exploration: list[list[float]] | None,
        wells: list[list[float]] | None,
        facilities: list[list[float]] | None,
        opex: list[list[float]] | None,
        abandonment: list[list[float]] | None,
        sln: list[list[float]] | None,
        acq: list[list[float]] | None,
        hurdle: float,
        duties: float,
        vat: float,
        history_end: int | None,
    ) -> StreamCostResult:
        out = StreamCostResult()
        ff = _series_to_map(exploration)
        fg = _series_to_map(wells)
        fh = _series_to_map(facilities)
        fi = _series_to_map(opex)
        abd = _series_to_map(abandonment)
        sln_m = _series_to_map(sln)
        acq_m = _series_to_map(acq)

        years = sorted(set(ff) | set(fg) | set(fh) | set(fi) | set(abd) | set(sln_m) | set(acq_m))
        if not years:
            return out

        # Cap_Allow FE5 is first year of consolidated block (discount base)
        base_year = years[0]
        out.years = years

        esc_rate = float(case.opex_escalation_rate or 0.0)
        # G7: if opex series is pre-escalated from import, do not double-apply.
        # When recompute requested via extras flag:
        recompute_esc = bool(case.extras.get("recompute_opex_escalation", False))

        for y in years:
            expl = float(ff.get(y, 0.0) or 0.0)
            w = float(fg.get(y, 0.0) or 0.0)
            fac = float(fh.get(y, 0.0) or 0.0)
            op = float(fi.get(y, 0.0) or 0.0)
            ab = float(abd.get(y, 0.0) or 0.0)

            if recompute_esc:
                op = escalate_opex(op, y, base_year, esc_rate)

            expl = apply_history_mask(
                y,
                expl,
                analysis_type=case.asset_analysis_type,
                history_year=case.history_year,
                history_end_year=history_end,
            )
            w = apply_history_mask(
                y, w, analysis_type=case.asset_analysis_type, history_year=case.history_year, history_end_year=history_end
            )
            fac = apply_history_mask(
                y, fac, analysis_type=case.asset_analysis_type, history_year=case.history_year, history_end_year=history_end
            )
            op = apply_history_mask(
                y, op, analysis_type=case.asset_analysis_type, history_year=case.history_year, history_end_year=history_end
            )

            # G3 undisc
            fn = (w + fac) * duties  # FN = SUM(FG:FH)*C20
            fo = (expl + w + fac) * vat  # FO = SUM(FF:FH)*C21
            fp = expl  # FP = FF Expensed CAPEX
            fq = w + fac + fn + fo  # FQ

            # G4 discount
            df = discount_factor(hurdle, y, base_year)
            fk = (expl + w + fac) * df
            fl = op * df

            out.exploration[y] = expl
            out.capex_wells[y] = w
            out.capex_facilities[y] = fac
            out.opex[y] = op
            out.abandonment[y] = ab
            out.duties[y] = fn
            out.vat[y] = fo
            out.expensed_capex[y] = fp
            out.capitalized_costs[y] = fq
            out.disc_capex[y] = fk
            out.disc_opex[y] = fl
            out.sln[y] = float(sln_m.get(y, 0.0) or 0.0)
            out.acq_allowance[y] = float(acq_m.get(y, 0.0) or 0.0)

        # SUM ranges FI5:FI46 style — all years in FE block
        out.opex_undisc_total = sum(out.opex.values())
        out.opex_disc_total = sum(out.disc_opex.values())
        out.capex_disc_total = sum(out.disc_capex.values())
        out.expensed_capex_total = sum(out.expensed_capex.values())
        out.capitalized_costs_total = sum(out.capitalized_costs.values())
        out.sln_total = sum(out.sln.values())
        out.acq_allowance_total = sum(out.acq_allowance.values())
        return out
