"""FLGT / Royalties module — FLGT_ROYALTIES_CONTRACT.md R-G1…R-G5, F-G1…F-G11.

F-G12 loan AN–AP deferred. Law rates from Fiscal Terms_PIA LAW_TABLE (not CaseInput).
Authority: docs/03_IMPLEMENTATION/PHASE1D_FLGT_IMPLEMENTATION_GATE.md
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


def _map_get(m: dict[int, float], y: int, default: float = 0.0) -> float:
    return float(m.get(y, default) or 0.0)


@dataclass
class OilRoyaltyTierBand:
    """One terrain's production bands (BOPD thresholds → rates)."""

    terrain_label: str
    thresholds_bopd: list[float]  # V values as stored (e.g. 5000)
    rates: list[float]  # W rates


@dataclass
class FiscalLawParams:
    """LAW_TABLE slice for FLGT/Royalties — not CaseInput."""

    oil_tiers: list[OilRoyaltyTierBand] = field(default_factory=list)
    gas_util_dom_label: str = "In-Country (Dom Gas)"
    gas_util_out_label: str = "Out-Country"
    gas_rate_dom: float = 0.025
    gas_rate_out: float = 0.05
    price_band_low: float = 50.0  # U36
    price_band_high: float = 150.0  # U38
    price_royalty_cap: float = 0.10
    price_escalation_note: float = 0.0  # S4 on Royalties (0 on GTC)
    hcdt_rate: float = 0.03  # T72
    nddc_rate: float = 0.03  # T73
    rental_z11: float = 0.0
    rental_z12: float = 0.0

    @classmethod
    def pia_default_from_gm_gtc(cls) -> FiscalLawParams:
        """Default law parameters matching active GM as-saved (documentation values)."""
        return cls(
            oil_tiers=[
                OilRoyaltyTierBand(
                    "Onshore",
                    [5000.0, 10000.0, 10000.0],
                    [0.05, 0.075, 0.15],
                ),
                OilRoyaltyTierBand(
                    "Shallow Water (<200m water depth)",
                    [5000.0, 10000.0, 10000.0],
                    [0.05, 0.075, 0.125],
                ),
                OilRoyaltyTierBand(
                    "Deep Offshore (>200m water depth)",
                    [50000.0, 50000.0],
                    [0.05, 0.075],
                ),
                OilRoyaltyTierBand("Frontier Basin", [], [0.075]),
            ],
            gas_util_dom_label="In-Country (Dom Gas)",
            gas_util_out_label="Out-Country",
            gas_rate_dom=0.025,
            gas_rate_out=0.05,
            price_band_low=50.0,
            price_band_high=150.0,
            price_royalty_cap=0.10,
            price_escalation_note=0.0,
            hcdt_rate=0.03,
            nddc_rate=0.03,
            rental_z11=405.33,
            rental_z12=153.80841318168692,
        )


def sliding_oil_royalty_rate(daily_mbd: float, band: OilRoyaltyTierBand) -> float:
    """GM progressive average rate on daily oil (mb/d); thresholds are BOPD/1000."""
    if daily_mbd == 0 or daily_mbd is None:
        return 0.0
    b = float(daily_mbd)
    if not band.thresholds_bopd:
        # flat frontier
        return float(band.rates[0]) if band.rates else 0.0
    # convert BOPD thresholds to mb/d
    v = [t / 1000.0 for t in band.thresholds_bopd]
    w = list(band.rates)
    if len(v) >= 3 and len(w) >= 3:
        # Onshore / Shallow three-band progressive average (I5/J5 pattern)
        if b <= v[0]:
            return w[0]
        if b <= v[1]:
            return (w[0] * v[0] + (b - v[0]) * w[1]) / b
        # top band: uses V20 and W20 as in formula (third threshold index)
        return (w[0] * v[0] + (v[1] - v[0]) * w[1] + (b - v[2]) * w[2]) / b
    if len(v) >= 2 and len(w) >= 2:
        # Deep two-band
        if b <= v[0]:
            return w[0]
        return (w[0] * v[0] + (b - v[1]) * w[1]) / b
    return w[0] if w else 0.0


def gas_royalty_rate(
    daily_gas: float,
    gas_utilization: str | None,
    law: FiscalLawParams,
) -> float:
    if not daily_gas:
        return 0.0
    util = (gas_utilization or "").strip()
    # GM: IF(G21=U29 Out-Country label, U30=0.05, V30=0.025)
    # Dom gas is In-Country → V30 0.025
    if util == law.gas_util_out_label or util.startswith("Out"):
        return law.gas_rate_out
    return law.gas_rate_dom


def oil_price_path(
    year: int,
    *,
    oil_price: float,
    escalator: float,
    start_year: int,
    price_end_year: int | None,
    analysis_n12: float,
    analysis_n15: float,
    daily_oil: float,
    d29_year: int | None,
) -> tuple[float, float, float]:
    """Return (P real, Q factor, R nominal)."""
    # P: IF(AND(A<>D29, B=0), 0, C12*(1+N12))
    if d29_year is not None and year != int(d29_year) and daily_oil == 0:
        p = 0.0
    else:
        p = float(oil_price) * (1.0 + float(analysis_n12))
    # Q: ((1+C14*(1+N15))^(A-C5))*(A<D22)
    end = price_end_year if price_end_year is not None else 10**9
    if year < int(end):
        q = (1.0 + float(escalator) * (1.0 + float(analysis_n15))) ** (
            int(year) - int(start_year)
        )
    else:
        q = 0.0
    return p, q, p * q


def price_royalty_rate(
    nominal_price: float,
    year: int,
    law: FiscalLawParams,
) -> float:
    """S rate bands vs U36/U38 escalated from 2020."""
    r = float(nominal_price)
    if r <= 0:
        return 0.0
    factor = (1.0 + float(law.price_escalation_note)) ** (int(year) - 2020)
    low = law.price_band_low * factor
    high = law.price_band_high * factor
    if r <= low:
        return 0.0
    if r <= high:
        if high == low:
            return law.price_royalty_cap
        return law.price_royalty_cap * (r - low) / (high - low)
    return law.price_royalty_cap


@dataclass
class FlgtResult:
    years: list[int] = field(default_factory=list)
    # Royalties rates
    oil_rate: dict[int, float] = field(default_factory=dict)  # selected terrain rate
    oil_rate_i: dict[int, float] = field(default_factory=dict)
    oil_rate_j: dict[int, float] = field(default_factory=dict)
    oil_rate_k: dict[int, float] = field(default_factory=dict)
    oil_rate_l: dict[int, float] = field(default_factory=dict)
    gas_rate: dict[int, float] = field(default_factory=dict)
    price_real: dict[int, float] = field(default_factory=dict)
    price_q: dict[int, float] = field(default_factory=dict)
    price_nominal: dict[int, float] = field(default_factory=dict)
    price_royalty_rate: dict[int, float] = field(default_factory=dict)
    gas_price_nominal: dict[int, float] = field(default_factory=dict)
    # Volumes
    oil_daily: dict[int, float] = field(default_factory=dict)
    oil_annual: dict[int, float] = field(default_factory=dict)
    gas_daily: dict[int, float] = field(default_factory=dict)
    gas_annual: dict[int, float] = field(default_factory=dict)
    # FLGT $mm
    oil_revenue: dict[int, float] = field(default_factory=dict)  # W
    gas_revenue: dict[int, float] = field(default_factory=dict)  # X
    total_revenue: dict[int, float] = field(default_factory=dict)  # Y
    oil_royalty_mm: dict[int, float] = field(default_factory=dict)  # AB
    gas_royalty_mm: dict[int, float] = field(default_factory=dict)  # AC
    price_royalty_mm: dict[int, float] = field(default_factory=dict)  # AD
    rentals: dict[int, float] = field(default_factory=dict)  # AE
    hcdt_oil: dict[int, float] = field(default_factory=dict)  # AF
    hcdt_gas: dict[int, float] = field(default_factory=dict)  # Z
    nddc_oil: dict[int, float] = field(default_factory=dict)  # AG
    nddc_gas: dict[int, float] = field(default_factory=dict)  # AH
    bonuses: dict[int, float] = field(default_factory=dict)  # AA
    flgt_total: dict[int, float] = field(default_factory=dict)  # AI
    royalty_sum: dict[int, float] = field(default_factory=dict)  # AL
    err_annual: dict[int, float] = field(default_factory=dict)  # AM
    # Totals
    w51: float = 0.0
    x51: float = 0.0
    y51: float = 0.0
    ab51: float = 0.0
    ac51: float = 0.0
    ad51: float = 0.0
    al51: float = 0.0
    am51: float = 0.0
    ai51: float = 0.0
    z51: float = 0.0
    ae51: float = 0.0
    af51: float = 0.0
    ag51: float = 0.0
    ah51: float = 0.0
    aa51: float = 0.0
    # Sample rate cells (first production year)
    royalties_j5: float | None = None
    royalties_n5: float | None = None
    deferred: list[str] = field(default_factory=list)

    def cell_map(self) -> dict[tuple[str, str], Any]:
        m: dict[tuple[str, str], Any] = {
            ("FLGT", "W51"): self.w51,
            ("FLGT", "X51"): self.x51,
            ("FLGT", "Y51"): self.y51,
            ("FLGT", "AB51"): self.ab51,
            ("FLGT", "AC51"): self.ac51,
            ("FLGT", "AD51"): self.ad51,
            ("FLGT", "AL51"): self.al51,
            ("FLGT", "AM51"): self.am51,
            ("FLGT", "AI51"): self.ai51,
            ("FLGT", "Z51"): self.z51,
            ("FLGT", "AE51"): self.ae51,
            ("FLGT", "AF51"): self.af51,
            ("FLGT", "AG51"): self.ag51,
            ("FLGT", "AH51"): self.ah51,
            ("FLGT", "AA51"): self.aa51,
            ("Ec_IO", "G11"): self.am51,
            ("Ec_IO", "G15"): self.al51,
        }
        if self.royalties_j5 is not None:
            m[("Royalties", "J5")] = self.royalties_j5
        if self.royalties_n5 is not None:
            m[("Royalties", "N5")] = self.royalties_n5
        return m


class FlgtRoyaltiesModule:
    name = "flgt_royalties"
    contract_path = "docs/02_SPECIFICATIONS/modules/FLGT_ROYALTIES_CONTRACT.md"

    DEFERRED = [
        "F-G12 loan AN–AP (Equity Dash PPMT/IPMT)",
        "Full bonus trigger matrix beyond GTC-zero path",
        "Presentation / sensitivity UI / Monte Carlo",
        "CR/NCF and RESULTS engines",
    ]

    def run(
        self,
        case: CaseInput,
        upstream: dict[str, Any] | None = None,
        *,
        law: FiscalLawParams | None = None,
    ) -> FlgtResult:
        upstream = upstream or {}
        law = law or self._law_from_case(case)
        result = FlgtResult(deferred=list(self.DEFERRED))

        # R-G1 volumes: prefer ProductionResult maps via upstream, else CaseInput block series
        oil_daily, oil_annual, gas_daily, gas_annual = self._volumes(case, upstream)
        years = sorted(
            set(oil_daily) | set(oil_annual) | set(gas_daily) | set(gas_annual)
        )
        if not years and case.project_start_year is not None:
            years = list(range(int(case.project_start_year), int(case.project_start_year) + 42))
        result.years = years

        terrain = case.terrain or ""
        gas_util = case.gas_utilization
        oil_px = float(case.oil_price_usd_bbl or 0.0)
        gas_px = float(case.gas_price_usd_mscf or 0.0)
        esc = float(case.price_escalator or 0.0)
        start = int(case.project_start_year or (years[0] if years else 0))
        # D22 price path end (as-saved GM 2042); optional CaseInput extras
        d22 = case.extras.get("price_path_end_year")
        if d22 is None:
            # Ec_IO E29-like: start + life if known
            life = case.project_life_years
            d22 = int(start + float(life)) if life is not None else start + 15
        d29 = case.extras.get("forecast_anchor_year")
        if d29 is None:
            d29 = start  # D29 = E28+1 = start on forecast GM

        n12 = float(case.extras.get("analysis_n12", 0.0) or 0.0)
        n13 = float(case.extras.get("analysis_n13", 0.0) or 0.0)
        n15 = float(case.extras.get("analysis_n15", 0.0) or 0.0)

        # Cost bases for HCDT/NDDC
        oil_expl = _series_to_map(case.oil_tc_exploration)
        oil_wells = _series_to_map(case.oil_tc_capex_wells)
        oil_fac = _series_to_map(case.oil_tc_capex_facilities)
        oil_opex = _series_to_map(case.oil_tc_opex)
        gas_opex = _series_to_map(case.gas_tc_opex)
        gas_expl = _series_to_map(case.gas_tc_exploration)
        gas_wells = _series_to_map(case.gas_tc_capex_wells)
        gas_fac = _series_to_map(case.gas_tc_capex_facilities)

        # F-G1 lead years A5–A7 before first production year (for completeness)
        if years:
            y0 = min(years)
            lead = [y0 - 3, y0 - 2, y0 - 1]
            all_years = lead + years
        else:
            all_years = []

        band_onshore = self._band(law, "Onshore")
        band_shallow = self._band(law, "Shallow")
        band_deep = self._band(law, "Deep")
        band_frontier = self._band(law, "Frontier")
        selected_band = self._match_terrain(law, terrain)

        first_prod_year = None
        for y in years:
            b = _map_get(oil_daily, y)
            c = _map_get(oil_annual, y)
            e = _map_get(gas_daily, y)
            f = _map_get(gas_annual, y)
            result.oil_daily[y] = b
            result.oil_annual[y] = c
            result.gas_daily[y] = e
            result.gas_annual[y] = f

            # R-G2 rates all terrains
            ri = sliding_oil_royalty_rate(b, band_onshore) if band_onshore else 0.0
            rj = sliding_oil_royalty_rate(b, band_shallow) if band_shallow else 0.0
            rk = sliding_oil_royalty_rate(b, band_deep) if band_deep else 0.0
            rl = sliding_oil_royalty_rate(b, band_frontier) if band_frontier else 0.0
            if selected_band is band_onshore:
                r_oil = ri
            elif selected_band is band_shallow:
                r_oil = rj
            elif selected_band is band_deep:
                r_oil = rk
            else:
                r_oil = rl
            result.oil_rate_i[y] = ri
            result.oil_rate_j[y] = rj
            result.oil_rate_k[y] = rk
            result.oil_rate_l[y] = rl
            result.oil_rate[y] = r_oil

            # R-G3
            rg = gas_royalty_rate(e, gas_util, law)
            result.gas_rate[y] = rg

            # R-G4 / R-G5
            p, q, r_nom = oil_price_path(
                y,
                oil_price=oil_px,
                escalator=esc,
                start_year=start,
                price_end_year=int(d22),
                analysis_n12=n12,
                analysis_n15=n15,
                daily_oil=b,
                d29_year=int(d29) if d29 is not None else None,
            )
            result.price_real[y] = p
            result.price_q[y] = q
            result.price_nominal[y] = r_nom
            s_rate = price_royalty_rate(r_nom, y, law)
            result.price_royalty_rate[y] = s_rate

            # Gas price U = C17 * Q * (1+N13)  [FLGT U8 formula]
            u_nom = gas_px * q * (1.0 + n13)
            result.gas_price_nominal[y] = u_nom

            # F-G3 revenues
            w = r_nom * c
            x = u_nom * f
            result.oil_revenue[y] = w
            result.gas_revenue[y] = x
            result.total_revenue[y] = w + x

            # F-G4..G6 royalties $mm
            ab = r_oil * w
            ac = rg * x
            ad = s_rate * w
            result.oil_royalty_mm[y] = ab
            result.gas_royalty_mm[y] = ac
            result.price_royalty_mm[y] = ad
            result.royalty_sum[y] = ab + ac + ad
            if (w + x) != 0:
                result.err_annual[y] = (ab + ac + ad) / (w + x)
            else:
                result.err_annual[y] = 0.0

            if first_prod_year is None and (b > 0 or e > 0):
                first_prod_year = y

            # F-G7 rentals
            base_rent = law.rental_z12 * law.rental_z11 / 1_000_000.0
            result.rentals[y] = 0.0 if b == 0 else base_rent * q

            # F-G10 bonuses core GTC path
            result.bonuses[y] = 0.0

        # F-G8/F-G9 HCDT/NDDC need prev-year opex for AF/Z lag
        for y in years:
            ab = result.oil_royalty_mm[y]
            opex_y = _map_get(oil_opex, y)
            opex_prev = _map_get(oil_opex, y - 1)
            cost_sum = (
                _map_get(oil_expl, y)
                + _map_get(oil_wells, y)
                + _map_get(oil_fac, y)
                + opex_y
            )
            gas_fj = (
                _map_get(gas_expl, y)
                + _map_get(gas_wells, y)
                + _map_get(gas_fac, y)
                + _map_get(gas_opex, y)
            )
            gas_opex_prev = _map_get(gas_opex, y - 1)

            # AF HCDT oil: IF(AB=0,0,(prev_opex)*T72)
            result.hcdt_oil[y] = 0.0 if ab == 0 else opex_prev * law.hcdt_rate
            # AG NDDC oil
            result.nddc_oil[y] = cost_sum * law.nddc_rate
            # AH NDDC gas
            result.nddc_gas[y] = gas_fj * law.nddc_rate
            # Z HCDT gas: IF(AH=0,0, prev gas opex * T72)
            ah = result.nddc_gas[y]
            result.hcdt_gas[y] = 0.0 if ah == 0 else gas_opex_prev * law.hcdt_rate

            # F-G11 AI
            result.flgt_total[y] = (
                result.hcdt_gas[y]
                + result.bonuses[y]
                + result.oil_royalty_mm[y]
                + result.gas_royalty_mm[y]
                + result.price_royalty_mm[y]
                + result.rentals[y]
                + result.hcdt_oil[y]
                + result.nddc_oil[y]
                + result.nddc_gas[y]
            )

        # Totals SUM rows (production years in FLGT W5:W49 class)
        result.w51 = sum(result.oil_revenue.values())
        result.x51 = sum(result.gas_revenue.values())
        result.y51 = sum(result.total_revenue.values())
        result.ab51 = sum(result.oil_royalty_mm.values())
        result.ac51 = sum(result.gas_royalty_mm.values())
        result.ad51 = sum(result.price_royalty_mm.values())
        result.al51 = result.ab51 + result.ac51 + result.ad51
        result.am51 = (result.al51 / result.y51) if result.y51 else 0.0
        result.ai51 = sum(result.flgt_total.values())
        result.z51 = sum(result.hcdt_gas.values())
        result.ae51 = sum(result.rentals.values())
        result.af51 = sum(result.hcdt_oil.values())
        result.ag51 = sum(result.nddc_oil.values())
        result.ah51 = sum(result.nddc_gas.values())
        result.aa51 = sum(result.bonuses.values())

        # Sample first production year rates → Royalties J5/N5 (row5 = first Prod year)
        if first_prod_year is not None:
            result.royalties_j5 = result.oil_rate_j.get(first_prod_year, 0.0)
            result.royalties_n5 = result.gas_rate.get(first_prod_year, 0.0)
        elif years:
            y = years[0]
            result.royalties_j5 = result.oil_rate_j.get(y, 0.0)
            result.royalties_n5 = result.gas_rate.get(y, 0.0)

        return result

    def _law_from_case(self, case: CaseInput) -> FiscalLawParams:
        """Build law params from CaseInput.extras law_table if present else GM defaults."""
        raw = case.extras.get("fiscal_law")
        if isinstance(raw, FiscalLawParams):
            return raw
        if isinstance(raw, dict):
            base = FiscalLawParams.pia_default_from_gm_gtc()
            for k, v in raw.items():
                if hasattr(base, k) and k != "oil_tiers":
                    setattr(base, k, v)
            return base
        return FiscalLawParams.pia_default_from_gm_gtc()

    def _band(self, law: FiscalLawParams, key: str) -> OilRoyaltyTierBand | None:
        key_l = key.lower()
        for b in law.oil_tiers:
            if key_l in b.terrain_label.lower():
                return b
        return None

    def _match_terrain(self, law: FiscalLawParams, terrain: str) -> OilRoyaltyTierBand | None:
        t = (terrain or "").strip()
        for b in law.oil_tiers:
            if b.terrain_label == t:
                return b
        # partial match shallow
        for b in law.oil_tiers:
            if "Shallow" in b.terrain_label and "Shallow" in t:
                return b
            if "Deep" in b.terrain_label and "Deep" in t:
                return b
            if "Onshore" in b.terrain_label and "Onshore" in t:
                return b
            if "Frontier" in b.terrain_label and "Frontier" in t:
                return b
        return law.oil_tiers[1] if len(law.oil_tiers) > 1 else (law.oil_tiers[0] if law.oil_tiers else None)

    def _volumes(
        self, case: CaseInput, upstream: dict[str, Any]
    ) -> tuple[dict[int, float], dict[int, float], dict[int, float], dict[int, float]]:
        prod = upstream.get("production")
        if prod is not None:
            return (
                dict(getattr(prod, "oil_daily_series", {}) or {}),
                dict(getattr(prod, "oil_annual_series", {}) or {}),
                dict(getattr(prod, "gas_daily_series", {}) or {}),
                dict(getattr(prod, "gas_annual_series", {}) or {}),
            )
        if upstream.get("oil_daily") is not None:
            return (
                dict(upstream["oil_daily"]),
                dict(upstream.get("oil_annual") or {}),
                dict(upstream.get("gas_daily") or {}),
                dict(upstream.get("gas_annual") or {}),
            )
        return (
            _series_to_map(case.oil_block_daily),
            _series_to_map(case.oil_block_annual),
            _series_to_map(case.gas_block_daily),
            _series_to_map(case.gas_block_annual),
        )
