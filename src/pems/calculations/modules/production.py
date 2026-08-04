"""Production module — G1–G5 from PRODUCTION_PROFILE_CONTRACT.md.

G6 (local PP sensitivity) deferred. Multi-field editor deferred.
Golden Master behavioural parity only — no redesigned decline physics.
"""

from __future__ import annotations

import math
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


def _map_to_sorted_lists(m: dict[int, float]) -> tuple[list[int], list[float]]:
    years = sorted(m.keys())
    return years, [m[y] for y in years]


@dataclass
class ProductionResult:
    """Production outputs + GM cell map for GTC."""

    # G1
    pp_mode: str | None = None
    stoiip_inplace: float | None = None
    giip_inplace: float | None = None
    oil_ur: float | None = None
    gas_ur: float | None = None
    ur_target: float | None = None  # C6 = oil path UR when STOIIP

    # G2 design
    a1_buildup: float | None = None
    a3_decline: float | None = None
    t3_decline_yrs: float | None = None
    np1: float | None = None
    np2: float | None = None
    np3: float | None = None
    field_time_total: float | None = None

    # G3 PP series (calendar year → values)
    pp_rate_by_year: dict[int, float] = field(default_factory=dict)  # D (mb/d or mmscf/d /1000 scale)
    pp_annual_by_year: dict[int, float] = field(default_factory=dict)  # E
    pp_ag_rate_by_year: dict[int, float] = field(default_factory=dict)  # G
    pp_ag_annual_by_year: dict[int, float] = field(default_factory=dict)  # H

    # G4/G5 Prod_Summary series
    oil_daily_series: dict[int, float] = field(default_factory=dict)  # T
    oil_annual_series: dict[int, float] = field(default_factory=dict)  # U
    oil_cum_series: dict[int, float] = field(default_factory=dict)  # V
    gas_daily_series: dict[int, float] = field(default_factory=dict)  # W
    gas_annual_series: dict[int, float] = field(default_factory=dict)  # X
    gas_cum_series: dict[int, float] = field(default_factory=dict)  # Y

    oil_eur_or_max_cum: float | None = None  # V47
    gas_max_cum: float | None = None  # Y47
    gas_boe_factor: float | None = None  # Y48
    gas_mmboe: float | None = None  # Y49
    total_mmboe: float | None = None  # Y50
    project_life_years: float | None = None  # AF26 → Ec_IO C6
    summary_mode_flag: str | None = None  # R1
    af21_stream_flag: str | None = None  # AF21 AG/NAG

    path_used: str = "unknown"  # block_selected | analytical_pp
    deferred: list[str] = field(default_factory=list)

    def cell_map(self) -> dict[tuple[str, str], Any]:
        m: dict[tuple[str, str], Any] = {
            ("Production Profile", "B2"): self.pp_mode,
            ("Production Profile", "C2"): self.stoiip_inplace,
            ("Production Profile", "F2"): self.giip_inplace,
            ("Production Profile", "C4"): self.oil_ur,
            ("Production Profile", "F4"): self.gas_ur,
            ("Production Profile", "C6"): self.ur_target,
            ("Production Profile", "C15"): self.a1_buildup,
            ("Production Profile", "I15"): self.a3_decline,
            ("Production Profile", "I14"): self.t3_decline_yrs,
            ("Production Profile", "C16"): self.np1,
            ("Production Profile", "F16"): self.np2,
            ("Production Profile", "I16"): self.np3,
            ("Production Profile", "F17"): self.field_time_total,
            ("Prod_Summary", "R1"): self.summary_mode_flag,
            ("Prod_Summary", "AF21"): self.af21_stream_flag,
            ("Prod_Summary", "AF26"): self.project_life_years,
            ("Prod_Summary", "V47"): self.oil_eur_or_max_cum,
            ("Prod_Summary", "Y47"): self.gas_max_cum,
            ("Prod_Summary", "Y48"): self.gas_boe_factor,
            ("Prod_Summary", "Y49"): self.gas_mmboe,
            ("Prod_Summary", "Y50"): self.total_mmboe,
            ("Ec_IO", "C6"): self.project_life_years,
        }
        return {k: v for k, v in m.items() if v is not None}


class ProductionModule:
    name = "production"
    contract_path = "docs/02_SPECIFICATIONS/modules/PRODUCTION_PROFILE_CONTRACT.md"

    DEFERRED = [
        "G6 local PP sensitivity AB–AM (PRESENTATION)",
        "Full multi-field Block editor UI",
        "Hidden OML123_Oil_S1 series as editable input",
        "Reservoir STOIIP/GIIP internal engine (interface volumes only)",
    ]

    def run(self, case: CaseInput, upstream: dict[str, Any] | None = None) -> ProductionResult:
        upstream = upstream or {}
        result = ProductionResult(deferred=list(self.DEFERRED))

        mode = case.pp_mode or "STOIIP"
        result.pp_mode = mode
        result.summary_mode_flag = mode
        result.af21_stream_flag = "NAG" if mode == "GIIP" else "AG"

        stoiip = case.stoiip_inplace
        giip = case.giip_inplace
        oil_rf = case.oil_rf
        gas_rf = case.gas_rf
        result.stoiip_inplace = stoiip
        result.giip_inplace = giip

        # G1 — UR (C4 = IF(B2="STOIIP",C2*C3,F2*F3); F4 = F2*F3)
        oil_ur = None
        gas_ur = None
        if mode == "STOIIP":
            if stoiip is not None and oil_rf is not None:
                oil_ur = float(stoiip) * float(oil_rf)
        else:
            if giip is not None and gas_rf is not None:
                oil_ur = float(giip) * float(gas_rf)
        if giip is not None and gas_rf is not None:
            gas_ur = float(giip) * float(gas_rf)
        result.oil_ur = oil_ur
        result.gas_ur = gas_ur
        result.ur_target = oil_ur  # C6 = C4

        # G2 — build-up / plateau / decline design
        qi = case.qi_buildup
        qp = case.qp_plateau
        qel = case.qel_end
        t1 = case.t1_buildup_yrs
        t2 = case.t2_plateau_yrs
        days = case.pp_days_in_year
        if days is None:
            days = case.production_days_per_year
        lag = case.prod_start_lag_years
        if lag is None:
            lag = 0.0
        else:
            lag = float(lag)

        design_ok = all(
            v is not None
            for v in (
                qi,
                qp,
                qel,
                t1,
                t2,
                days,
                result.ur_target,
            )
        )
        if design_ok:
            qi_f, qp_f, qel_f = float(qi), float(qp), float(qel)  # type: ignore[arg-type]
            t1_f, t2_f, days_f = float(t1), float(t2), float(days)  # type: ignore[arg-type]
            # C15 = LN(C12/C13)/C14
            a1 = math.log(qi_f / qp_f) / t1_f if t1_f != 0 else float("nan")
            # C16 = (C12-C13)*C9/C15/1e6
            np1 = (qi_f - qp_f) * days_f / a1 / 1_000_000.0
            # F12 = C13; F16 = F12*C9*F14/1e6
            np2 = qp_f * days_f * t2_f / 1_000_000.0
            ur_for_np = float(result.ur_target)  # type: ignore[arg-type]
            np3 = ur_for_np - np1 - np2
            # I12 = F13 = F12 = qp; I15 = ((I12-I13)*C9/I16/1e6)+-LN(1-L7)*0
            a3 = (qp_f - qel_f) * days_f / np3 / 1_000_000.0 if np3 != 0 else float("nan")
            t3 = math.log(qp_f / qel_f) / a3 if a3 != 0 else float("nan")
            field_time = lag + t1_f + t2_f + t3

            result.a1_buildup = a1
            result.a3_decline = a3
            result.t3_decline_yrs = t3
            result.np1 = np1
            result.np2 = np2
            result.np3 = np3
            result.field_time_total = field_time

            year_end = case.year_end_anchor
            if year_end is not None and not math.isnan(field_time):
                result.pp_rate_by_year, result.pp_annual_by_year = self._pp_rate_series(
                    year_end=int(year_end),
                    lag=lag,
                    t1=t1_f,
                    t2=t2_f,
                    field_time=field_time,
                    qi=qi_f,
                    qp=qp_f,
                    a1=a1,
                    a3=a3,
                    days=days_f,
                )
                gor = float(case.gor_scf_bbl or 0.0)
                if mode == "GIIP":
                    result.pp_ag_rate_by_year = {y: 0.0 for y in result.pp_rate_by_year}
                    result.pp_ag_annual_by_year = {y: 0.0 for y in result.pp_annual_by_year}
                else:
                    result.pp_ag_rate_by_year = {
                        y: (r * gor) / 1000.0 for y, r in result.pp_rate_by_year.items()
                    }
                    result.pp_ag_annual_by_year = {
                        y: (gor * a) / 1000.0 for y, a in result.pp_annual_by_year.items()
                    }

        # G4/G5 — Prod_Summary from block series or analytical PP
        oil_daily = _series_to_map(case.oil_block_daily)
        oil_annual = _series_to_map(case.oil_block_annual)
        gas_daily = _series_to_map(case.gas_block_daily)
        gas_annual = _series_to_map(case.gas_block_annual)

        oil_scale = 1.0 + float(case.analysis_oil_scale or 0.0)
        gas_scale = 1.0 + float(case.analysis_gas_scale or 0.0)
        days_ann = float(days if days is not None else 365)

        if oil_daily or gas_daily:
            result.path_used = "block_selected"
            if not oil_annual and oil_daily:
                oil_annual = {y: v * days_ann / 1000.0 for y, v in oil_daily.items()}
            if not gas_annual and gas_daily:
                gas_annual = {y: v * days_ann / 1000.0 for y, v in gas_daily.items()}
            oil_daily = {y: v * oil_scale for y, v in oil_daily.items()}
            oil_annual = {y: v * oil_scale for y, v in oil_annual.items()}
            gas_daily = {y: v * gas_scale for y, v in gas_daily.items()}
            gas_annual = {y: v * gas_scale for y, v in gas_annual.items()}
        else:
            result.path_used = "analytical_pp"
            # Bridge PP rates as selected Generic Field path
            if mode == "GIIP":
                gas_daily = dict(result.pp_rate_by_year)
                gas_annual = dict(result.pp_annual_by_year)
                oil_daily = {}
                oil_annual = {}
            else:
                oil_daily = dict(result.pp_rate_by_year)
                # Block bridge annualizes daily * days/1000 (not PP E difference method)
                oil_annual = {y: v * days_ann / 1000.0 for y, v in oil_daily.items()}
                gas_daily = dict(result.pp_ag_rate_by_year)
                gas_annual = dict(result.pp_ag_annual_by_year)

        # History filter + timeline assembly (Prod_Summary T/U/W/X)
        start_year = case.project_start_year
        if start_year is None and oil_daily:
            start_year = min(oil_daily.keys())
        if start_year is None and gas_daily:
            start_year = min(gas_daily.keys())
        if start_year is None:
            start_year = case.year_end_anchor

        n_years = 48  # GM S5:S52 span class
        years: list[int] = []
        if start_year is not None:
            years = list(range(int(start_year), int(start_year) + n_years))

        hist = case.asset_analysis_type == "History"
        d28 = case.history_year
        e28 = (int(case.project_start_year) - 1) if case.project_start_year is not None else None

        def hist_mask(year: int, value: float) -> float:
            if not hist:
                return value
            if d28 is not None and year < int(d28):
                return 0.0
            if e28 is not None and year > int(e28):
                return 0.0
            return value

        oil_t: dict[int, float] = {}
        oil_u: dict[int, float] = {}
        gas_w: dict[int, float] = {}
        gas_x: dict[int, float] = {}
        for y in years:
            od = hist_mask(y, float(oil_daily.get(y, 0.0) or 0.0))
            oa = hist_mask(y, float(oil_annual.get(y, 0.0) or 0.0))
            gd = hist_mask(y, float(gas_daily.get(y, 0.0) or 0.0))
            ga = hist_mask(y, float(gas_annual.get(y, 0.0) or 0.0))
            oil_t[y] = od
            oil_u[y] = oa
            gas_w[y] = gd
            gas_x[y] = ga

        # Cum: V = IF(T=0,0,SUM(U to date)); Y similar for gas
        oil_v: dict[int, float] = {}
        gas_y: dict[int, float] = {}
        run_o = 0.0
        run_g = 0.0
        for y in years:
            if oil_t.get(y, 0.0) == 0:
                oil_v[y] = 0.0
            else:
                run_o += oil_u.get(y, 0.0)
                oil_v[y] = run_o
            if gas_w.get(y, 0.0) == 0:
                gas_y[y] = 0.0
            else:
                run_g += gas_x.get(y, 0.0)
                gas_y[y] = run_g

        result.oil_daily_series = oil_t
        result.oil_annual_series = oil_u
        result.oil_cum_series = oil_v
        result.gas_daily_series = gas_w
        result.gas_annual_series = gas_x
        result.gas_cum_series = gas_y

        # V47 = MAX(V5:V36) → first 32 years of summary table (rows 5..36)
        # Y47 = MAX(Y5:Y46) → first 42 years
        v_years = years[:32] if years else []
        y_years = years[:42] if years else []
        v47 = max((oil_v[y] for y in v_years), default=0.0) if v_years else 0.0
        y47 = max((gas_y[y] for y in y_years), default=0.0) if y_years else 0.0
        # When cum zeros for zero-rate years, max still works
        # Fix: running max of non-zero cums — MAX of series values
        if oil_v:
            v47 = max(oil_v[y] for y in (v_years or oil_v.keys()))
        if gas_y:
            y47 = max(gas_y[y] for y in (y_years or gas_y.keys()))

        boe = case.gas_boe_factor if case.gas_boe_factor is not None else 5.804
        y49 = y47 / float(boe) if boe else None
        y50 = v47 + y49 if y49 is not None else None

        result.oil_eur_or_max_cum = v47
        result.gas_max_cum = y47
        result.gas_boe_factor = float(boe)
        result.gas_mmboe = y49
        result.total_mmboe = y50

        # AF26 life: COUNTIF rates > 0 on oil if AG/Oil else gas
        if result.af21_stream_flag in ("Oil", "AG"):
            life = sum(1 for y in years if oil_t.get(y, 0.0) > 0)
        else:
            life = sum(1 for y in years if gas_w.get(y, 0.0) > 0)
        result.project_life_years = float(life)

        return result

    def _pp_rate_series(
        self,
        *,
        year_end: int,
        lag: float,
        t1: float,
        t2: float,
        field_time: float,
        qi: float,
        qp: float,
        a1: float,
        a3: float,
        days: float,
    ) -> tuple[dict[int, float], dict[int, float]]:
        """G3 rate D and annual E matching GM Production Profile formulas."""
        # Rows B23… enough years to cover field life + lag + buffer
        n = int(math.ceil(field_time + lag + 5)) + 5
        rates: dict[int, float] = {}
        annuals: dict[int, float] = {}
        prev_d = 0.0  # D22 before first row = 0
        for i in range(n):
            b_year = year_end + i  # B23 = C8
            # C23 time index
            delta = b_year - year_end
            roundup_ft = math.ceil(field_time) if field_time == int(field_time) else math.ceil(field_time)
            # Excel ROUNDUP(x,0)
            if field_time == int(field_time):
                roundup_ft = int(field_time)
            else:
                roundup_ft = math.ceil(field_time)
            if delta == roundup_ft:
                c_t = field_time
            elif delta <= field_time + 1:
                c_t = float(delta)
            else:
                c_t = 0.0

            # Rate D (before /1000 scale applied in formula — formula ends /1000)
            if c_t >= lag and c_t < (t1 + lag):
                raw = qi * math.exp(-a1 * (c_t - lag))
            elif c_t >= (t1 + lag) and c_t < (t1 + lag + t2):
                raw = qp
            elif c_t <= lag:
                raw = 0.0
            else:
                raw = qp * math.exp(-a3 * (c_t - (t1 + t2 + lag)))

            gate = 1.0 if b_year <= (year_end + lag + field_time) else 0.0
            d_rate = (raw * gate) / 1000.0  # mb/d scale

            # Annual E formula (uses previous D)
            d_prev = prev_d
            d_curr = d_rate
            if d_prev == 0:
                e_inner = 0.0
            elif d_prev > 0 and c_t <= (lag + t1):
                e_inner = (d_prev - d_curr) * days / a1 / 1_000_000.0
            elif c_t > (lag + t1) and c_t <= (lag + t1 + t2):
                e_inner = (d_curr * days) / 1_000_000.0
            else:
                e_inner = (d_prev - d_curr) * days / a3 / 1_000_000.0
            e_vol = (e_inner if e_inner > 0 else 0.0) * 1000.0

            rates[b_year] = d_rate
            annuals[b_year] = e_vol
            prev_d = d_rate

        return rates, annuals
