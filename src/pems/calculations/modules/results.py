"""RESULTS Equity KPI aggregation — RESULTS_PARAMETER_CONTRACT.md.

Read-model over CR/NCF, FLGT, Production, Costs, Ec_IO identity, Equity C4.
HT BIT equity KPIs / CF series: selected intermediate path (HT engine deferred),
mirroring CR/NCF tax-intermediate pattern (A5 readiness note).

Formula groups: R-ID, R-NPV, R-IRR, R-TAKE, R-PAYOUT, R-COST, R-REV, R-UNIT,
R-ROY, R-TAX, R-PROD.

Presentation / charts / sensitivity / Monte Carlo: DEFERRED.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pems.calculations.modules.cr_ncf import excel_irr
from pems.domain.case_input import CaseInput


def _as_year_map(v: Any) -> dict[int, float]:
    if v is None:
        return {}
    if isinstance(v, dict):
        return {int(k): float(val or 0) for k, val in v.items()}
    if isinstance(v, list):
        out: dict[int, float] = {}
        for pair in v:
            if len(pair) < 2:
                continue
            out[int(pair[0])] = float(pair[1])
        return out
    return {}


def _g(m: dict[int, float], y: int, default: float = 0.0) -> float:
    return float(m.get(y, default) or 0.0)


def _equity_share_text(c4: float) -> str:
    """Excel TEXT(C4,\"0%\") → e.g. Equity Share =49%."""
    pct = int(round(float(c4) * 100))
    return f"Equity Share ={pct}%"


def _gas_bscf_text(y47: float, c4: float) -> str:
    """Excel: \"(\"&TEXT(Y47*C4,\"0.00\")&\" Bscf\"&\")\"."""
    return f"({float(y47) * float(c4):.2f} Bscf)"


def _safe_div(num: float, den: float) -> float:
    if den == 0:
        return 0.0
    return num / den


@dataclass
class ResultsResult:
    """RESULTS Equity KPI surface (semantic values; no presentation formats)."""

    # R-ID
    l2_country: str | None = None
    l3_regime: str | None = None
    l5_pfs: str | None = None
    c5_field: str | None = None
    c6_licence: str | None = None
    c7_terrain: str | None = None
    c8_equity_text: str | None = None
    h7_hurdle: float | None = None

    # R-NPV BIT / AIT
    j7_host_npv_bit: float | None = None
    k7_contractor_npv_bit: float | None = None
    m7_host_npv_ait: float | None = None
    n7_contractor_npv_ait: float | None = None

    # R-IRR / profitability
    k8_irr_bit: float | str | None = None
    n8_irr_ait: float | str | None = None
    k9_pvr_bit: float | None = None
    n9_pvr_ait: float | None = None
    k10_pi_bit: float | None = None
    n10_pi_ait: float | None = None
    k11_grr_bit: float | None = None
    n11_grr_ait: float | None = None

    # R-TAKE / R-PAYOUT / FLI
    j12_undisc_host_take_bit: float | None = None
    k12_undisc_contractor_take_bit: float | None = None
    m12_undisc_host_take_ait: float | None = None
    n12_undisc_contractor_take_ait: float | None = None
    j13_disc_host_take_bit: float | None = None
    k13_disc_contractor_take_bit: float | None = None
    m13_disc_host_take_ait: float | None = None
    n13_disc_contractor_take_ait: float | None = None
    k14_payout_bit: float | None = None
    n14_payout_ait: float | None = None
    h15_fli: float | None = None

    # R-COST / R-REV
    h16_pv_opex_eq: float | None = None
    m16_undisc_opex_eq: float | None = None
    h17_pv_capex_eq: float | None = None
    m17_undisc_capex_eq: float | None = None
    h18_pv_tc_eq: float | None = None
    m18_undisc_tc_eq: float | None = None
    j16_oil_rev_eq: float | None = None
    j17_gas_rev_eq: float | None = None
    j18_gross_rev_eq: float | None = None

    # R-UNIT (Excel order: equity_cost / Y50 / C4)
    h19_unit_pv_opex: float | None = None
    m19_unit_undisc_opex: float | None = None
    h20_unit_pv_capex: float | None = None
    m20_unit_undisc_capex: float | None = None
    h21_unit_pv_tc: float | None = None
    m21_unit_undisc_tc: float | None = None

    # R-ROY
    h22_oil_royalty_eq: float | None = None
    h23_gas_royalty_eq: float | None = None
    h24_price_royalty_eq: float | None = None
    h25_total_royalty_eq: float | None = None
    h26_err: float | None = None

    # R-TAX
    j22_ht_eq: float | None = None
    j23_cit_eq: float | None = None
    j24_etx_eq: float | None = None
    j25_total_tax_eq: float | None = None

    # R-PROD
    n22_oil_prod_eq: float | None = None
    n23_gas_mmboe_eq: float | None = None
    m23_gas_bscf_text: str | None = None
    n24_total_mmboe_eq: float | None = None

    equity_c4: float | None = None
    deferred: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def cell_map(self) -> dict[tuple[str, str], Any]:
        """Map RESULTS Equity cells for GTC compare."""
        sheet = "RESULTS Equity"
        pairs: list[tuple[str, Any]] = [
            ("L2", self.l2_country),
            ("L3", self.l3_regime),
            ("L5", self.l5_pfs),
            ("C5", self.c5_field),
            ("C6", self.c6_licence),
            ("C7", self.c7_terrain),
            ("C8", self.c8_equity_text),
            ("H7", self.h7_hurdle),
            ("J7", self.j7_host_npv_bit),
            ("K7", self.k7_contractor_npv_bit),
            ("M7", self.m7_host_npv_ait),
            ("N7", self.n7_contractor_npv_ait),
            ("K8", self.k8_irr_bit),
            ("N8", self.n8_irr_ait),
            ("K9", self.k9_pvr_bit),
            ("N9", self.n9_pvr_ait),
            ("K10", self.k10_pi_bit),
            ("N10", self.n10_pi_ait),
            ("K11", self.k11_grr_bit),
            ("N11", self.n11_grr_ait),
            ("J12", self.j12_undisc_host_take_bit),
            ("K12", self.k12_undisc_contractor_take_bit),
            ("M12", self.m12_undisc_host_take_ait),
            ("N12", self.n12_undisc_contractor_take_ait),
            ("J13", self.j13_disc_host_take_bit),
            ("K13", self.k13_disc_contractor_take_bit),
            ("M13", self.m13_disc_host_take_ait),
            ("N13", self.n13_disc_contractor_take_ait),
            ("K14", self.k14_payout_bit),
            ("N14", self.n14_payout_ait),
            ("H15", self.h15_fli),
            ("H16", self.h16_pv_opex_eq),
            ("M16", self.m16_undisc_opex_eq),
            ("H17", self.h17_pv_capex_eq),
            ("M17", self.m17_undisc_capex_eq),
            ("H18", self.h18_pv_tc_eq),
            ("M18", self.m18_undisc_tc_eq),
            ("J16", self.j16_oil_rev_eq),
            ("J17", self.j17_gas_rev_eq),
            ("J18", self.j18_gross_rev_eq),
            ("H19", self.h19_unit_pv_opex),
            ("M19", self.m19_unit_undisc_opex),
            ("H20", self.h20_unit_pv_capex),
            ("M20", self.m20_unit_undisc_capex),
            ("H21", self.h21_unit_pv_tc),
            ("M21", self.m21_unit_undisc_tc),
            ("H22", self.h22_oil_royalty_eq),
            ("H23", self.h23_gas_royalty_eq),
            ("H24", self.h24_price_royalty_eq),
            ("H25", self.h25_total_royalty_eq),
            ("H26", self.h26_err),
            ("J22", self.j22_ht_eq),
            ("J23", self.j23_cit_eq),
            ("J24", self.j24_etx_eq),
            ("J25", self.j25_total_tax_eq),
            ("N22", self.n22_oil_prod_eq),
            ("N23", self.n23_gas_mmboe_eq),
            ("M23", self.m23_gas_bscf_text),
            ("N24", self.n24_total_mmboe_eq),
        ]
        return {(sheet, cell): val for cell, val in pairs if val is not None}


class ResultsModule:
    name = "results"
    contract_path = "docs/02_SPECIFICATIONS/modules/RESULTS_PARAMETER_CONTRACT.md"

    DEFERRED = [
        "Presentation fonts/styles/colours/number formats",
        "Charts / dual-axis dashboards",
        "Sensitivity / Monte Carlo UI",
        "Full HT_NCF_Oil Equity line-by-line engine (intermediates imported for BIT path)",
        "Full CIT_NCF Equity line-by-line engine (totals via intermediates or C4 scale)",
    ]

    def run(self, case: CaseInput, upstream: dict[str, Any] | None = None) -> ResultsResult:
        upstream = upstream or {}
        r = ResultsResult(deferred=list(self.DEFERRED))
        c4 = float(case.equity_share_company_1 or 0.0)
        r.equity_c4 = c4

        prod = upstream.get("production")
        costs = upstream.get("costs")
        flgt = upstream.get("flgt")
        cr = upstream.get("cr_ncf")
        ec = upstream.get("ec_io")

        # --- R-ID identity ---
        r.l2_country = case.country
        r.l3_regime = case.fiscal_regime_label
        r.l5_pfs = case.pfs_contract_type
        # Ec_IO!I5 ← G23 ← G18 block_field_oil
        r.c5_field = case.block_field_oil
        r.c6_licence = case.licence_lease_status
        r.c7_terrain = case.terrain
        r.c8_equity_text = _equity_share_text(c4)
        r.h7_hurdle = float(case.hurdle_rate) if case.hurdle_rate is not None else None
        if ec is not None and getattr(ec, "case", None) is not None:
            # prefer ec_io resolved life/hurdle if present
            if r.h7_hurdle is None and ec.case.hurdle_rate is not None:
                r.h7_hurdle = float(ec.case.hurdle_rate)

        life = case.project_life_years
        if life is None and prod is not None and getattr(prod, "project_life_years", None) is not None:
            life = float(prod.project_life_years)
        hurdle = float(r.h7_hurdle or 0.0)

        # --- R-COST / R-REV (Ec_IO hub × C4; revenue hub = FLGT W/X) ---
        n16 = n17 = s16 = s17 = p16 = p17 = 0.0
        if costs is not None:
            n16 = float(costs.pv_opex_combined or 0.0)
            n17 = float(costs.pv_capex_combined or 0.0)
            s16 = float(costs.undisc_opex_combined or 0.0)
            s17 = float(costs.undisc_capex_combined or 0.0)
        if flgt is not None:
            p16 = float(flgt.w51 or 0.0)
            p17 = float(flgt.x51 or 0.0)

        r.h16_pv_opex_eq = n16 * c4
        r.m16_undisc_opex_eq = s16 * c4
        r.h17_pv_capex_eq = n17 * c4
        r.m17_undisc_capex_eq = s17 * c4
        r.h18_pv_tc_eq = r.h16_pv_opex_eq + r.h17_pv_capex_eq
        r.m18_undisc_tc_eq = r.m16_undisc_opex_eq + r.m17_undisc_capex_eq
        r.j16_oil_rev_eq = p16 * c4
        r.j17_gas_rev_eq = p17 * c4
        r.j18_gross_rev_eq = r.j16_oil_rev_eq + r.j17_gas_rev_eq

        # --- R-UNIT: preserve Excel order equity_num / Y50 / C4 ---
        y50 = 0.0
        y47 = 0.0
        y49 = 0.0
        v47 = 0.0
        if prod is not None:
            y50 = float(prod.total_mmboe or 0.0)
            y47 = float(prod.gas_max_cum or 0.0)
            y49 = float(prod.gas_mmboe or 0.0)
            v47 = float(prod.oil_eur_or_max_cum or 0.0)

        def unit(eq_cost: float) -> float:
            # Excel: H16/Y50/C4 == (H16/Y50)/C4
            if y50 == 0 or c4 == 0:
                return 0.0
            return (eq_cost / y50) / c4

        r.h19_unit_pv_opex = unit(r.h16_pv_opex_eq)
        r.m19_unit_undisc_opex = unit(r.m16_undisc_opex_eq)
        r.h20_unit_pv_capex = unit(r.h17_pv_capex_eq)
        r.m20_unit_undisc_capex = unit(r.m17_undisc_capex_eq)
        r.h21_unit_pv_tc = unit(r.h18_pv_tc_eq)
        r.m21_unit_undisc_tc = unit(r.m18_undisc_tc_eq)

        # --- R-ROY ---
        ab51 = ac51 = ad51 = 0.0
        if flgt is not None:
            ab51 = float(flgt.ab51 or 0.0)
            ac51 = float(flgt.ac51 or 0.0)
            ad51 = float(flgt.ad51 or 0.0)
        r.h22_oil_royalty_eq = ab51 * c4
        r.h23_gas_royalty_eq = ac51 * c4
        r.h24_price_royalty_eq = ad51 * c4
        r.h25_total_royalty_eq = r.h22_oil_royalty_eq + r.h23_gas_royalty_eq + r.h24_price_royalty_eq
        r.h26_err = _safe_div(r.h25_total_royalty_eq, r.j18_gross_rev_eq or 0.0)

        # --- R-PROD ---
        r.n22_oil_prod_eq = v47 * c4
        r.n23_gas_mmboe_eq = y49 * c4
        r.m23_gas_bscf_text = _gas_bscf_text(y47, c4)
        r.n24_total_mmboe_eq = r.n22_oil_prod_eq + r.n23_gas_mmboe_eq

        # --- R-NPV AIT from CR/NCF Equity_NCF_Con ---
        if cr is not None:
            r.m7_host_npv_ait = float(cr.equity_ag51)
            r.n7_contractor_npv_ait = float(cr.equity_ah51)
            r.n14_payout_ait = float(cr.aj51)
            # Undisc take AIT: AE/(AE+AF) scale-invariant on project totals
            ae = float(cr.ae51)
            af = float(cr.af51)
            r.m12_undisc_host_take_ait = _safe_div(ae, ae + af)
            r.n12_undisc_contractor_take_ait = 1.0 - r.m12_undisc_host_take_ait if r.m12_undisc_host_take_ait is not None else None
            # AIT IRR: Equity AF series — constant equity scale ⇒ same IRR as project AF
            years = list(cr.years) if cr.years else sorted(cr.contractor_af.keys())
            af_eq = [float(cr.contractor_af.get(y, 0.0) or 0.0) * c4 for y in years]
            while len(af_eq) < 45:
                af_eq.append(0.0)
            r.n8_irr_ait = excel_irr(af_eq[:45])

        # Disc take AIT from NPVs
        if r.m7_host_npv_ait is not None and r.n7_contractor_npv_ait is not None:
            r.m13_disc_host_take_ait = _safe_div(
                r.m7_host_npv_ait, r.m7_host_npv_ait + r.n7_contractor_npv_ait
            )
            r.n13_disc_contractor_take_ait = 1.0 - r.m13_disc_host_take_ait

        # FLI = M13/M12 - 1
        if r.m13_disc_host_take_ait is not None and r.m12_undisc_host_take_ait is not None:
            r.h15_fli = _safe_div(r.m13_disc_host_take_ait, r.m12_undisc_host_take_ait) - 1.0

        # --- BIT path: HT_NCF_Oil Equity intermediates (selected path) ---
        ht = case.extras.get("ht_ncf_oil_equity_intermediates") or {}
        if ht:
            r.j7_host_npv_bit = float(ht.get("AS51", 0.0) or 0.0)
            r.k7_contractor_npv_bit = float(ht.get("AT51", 0.0) or 0.0)
            r.j22_ht_eq = float(ht.get("AO51", 0.0) or 0.0)
            aq = float(ht.get("AQ51", 0.0) or 0.0)
            ar_tot = float(ht.get("AR51", 0.0) or 0.0)
            r.j12_undisc_host_take_bit = _safe_div(aq, aq + ar_tot)
            r.k12_undisc_contractor_take_bit = 1.0 - r.j12_undisc_host_take_bit
            r.k14_payout_bit = float(ht.get("AV51", 0.0) or 0.0)
            ar_series = _as_year_map(ht.get("AR", {}))
            years_ht = sorted(ar_series.keys()) if ar_series else []
            ar_list = [_g(ar_series, y) for y in years_ht]
            # ordered 45 periods matching AR5:AR49
            while len(ar_list) < 45:
                ar_list.append(0.0)
            r.k8_irr_bit = excel_irr(ar_list[:45])
            r.notes.append("BIT path: HT_NCF_Oil Equity intermediates")
        else:
            r.notes.append("BIT path: HT equity intermediates missing — BIT KPIs unset")

        if r.j7_host_npv_bit is not None and r.k7_contractor_npv_bit is not None:
            r.j13_disc_host_take_bit = _safe_div(
                r.j7_host_npv_bit, r.j7_host_npv_bit + r.k7_contractor_npv_bit
            )
            r.k13_disc_contractor_take_bit = 1.0 - r.j13_disc_host_take_bit

        # --- R-TAX CIT / education tax ---
        cit = case.extras.get("cit_ncf_equity_totals") or {}
        if cit:
            r.j23_cit_eq = float(cit.get("AF51", 0.0) or 0.0)
            r.j24_etx_eq = float(cit.get("AG51", 0.0) or 0.0)
            r.notes.append("CIT path: cit_ncf_equity_totals intermediates")
        elif cr is not None and case.extras.get("project_ncf_intermediates"):
            # Fallback not used for CIT (not in Project AB/AC/AD mapping alone)
            pass

        # HT tax J22 may also equal Project AD51 * C4 when intermediates absent
        if r.j22_ht_eq is None and cr is not None:
            r.j22_ht_eq = float(cr.ad51) * c4
            r.notes.append("HT tax J22 from Project AD51×C4 fallback")

        if r.j22_ht_eq is not None and r.j23_cit_eq is not None and r.j24_etx_eq is not None:
            r.j25_total_tax_eq = r.j22_ht_eq + r.j23_cit_eq + r.j24_etx_eq

        # --- PVR / PI / GRR ---
        h18 = r.h18_pv_tc_eq or 0.0
        if r.k7_contractor_npv_bit is not None and h18 != 0:
            r.k9_pvr_bit = r.k7_contractor_npv_bit / h18
            r.k10_pi_bit = 1.0 + r.k9_pvr_bit
        if r.n7_contractor_npv_ait is not None and h18 != 0:
            r.n9_pvr_ait = r.n7_contractor_npv_ait / h18
            r.n10_pi_ait = 1.0 + r.n9_pvr_ait

        # GRR = PI^(1/life)*(1+hurdle)-1  (Ec_IO C6, C15)
        if life and float(life) != 0:
            if r.k10_pi_bit is not None and r.k10_pi_bit >= 0:
                r.k11_grr_bit = (r.k10_pi_bit ** (1.0 / float(life))) * (1.0 + hurdle) - 1.0
            if r.n10_pi_ait is not None and r.n10_pi_ait >= 0:
                r.n11_grr_ait = (r.n10_pi_ait ** (1.0 / float(life))) * (1.0 + hurdle) - 1.0

        return r
