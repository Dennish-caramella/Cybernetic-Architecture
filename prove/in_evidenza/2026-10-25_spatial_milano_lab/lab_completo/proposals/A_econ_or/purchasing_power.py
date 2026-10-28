"""Real purchasing power of Milan households and its effect on the target band and on portfolios P2/P6.

Run: PYTHONPATH=C:/Temp/pl python lab/proposals/A_econ_or/purchasing_power.py   (~5 min; needs results/cache from prep.py
and results/demand_scenarios.csv + sites_P2.csv/sites_P6.csv from run_all.py for the comparison)
Outputs: results/purchasing_power_nil.csv, purchasing_power_hhtype.csv, purchasing_power_omi.csv,
         purchasing_power_sites_P2r.csv, purchasing_power_sites_P6r.csv, purchasing_power.json
"""
import io, json, os, sys, time
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import demand, portfolio as PF

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..")); RES = os.path.join(HERE, "results"); T0 = time.time()
log = lambda *a: print(f"[{time.time() - T0:6.1f}s]", *a, file=sys.stderr, flush=True)
TL = float(os.environ.get("A_TL", 60))

# ---------------------------------------------------------------- constants (source, status)
K = dict(
    # ISTAT absolute-poverty threshold, Lombardy, centre of metropolitan area, single adult 30-59, EUR/month.
    # Found via web search snippet of the ISTAT calculator; reference year NOT shown -> treat as 2024, to verify.
    pov_single=1256.37,
    # Same source family (Sky TG24 on ISTAT 2022): Milan single adult 1,175 EUR/month (2022) -> cross-check of order.
    pov_single_2022=1175.0,
    # ISTAT basket = food + housing (rent of adequate dwelling + utilities) + residual. Share of the rent-only
    # component for a single adult in a northern metro centre: ASSUMPTION ~40 % (from memory, to verify).
    # Non-housing basket keeps utilities (OMI rents are net of utilities, so utilities are not double counted).
    rent_share_in_threshold=0.40,
    # Spatial price level, Milan vs Italy = 1.047 (Istat-Unioncamere-Tagliacarne, 2009 data, regional capitals);
    # Cannari & Iuzzolino (Banca d'Italia QEF 49/2009): North-South gap 16-17 % incl. housing, ~10 % with actual rents.
    p_milan=1.047, p_milan_hi=1.10,
    # NIC annual average inflation, ITALY used as proxy for NIC Milano (from memory, to verify): 2020..2025
    nic={2020: -0.2, 2021: 1.9, 2022: 8.1, 2023: 5.7, 2024: 1.0, 2025: 1.7},
    # Nominal growth of mean IRPEF income 2019->2024: MEF national mean 21,800 EUR in 2019 (Il Fatto Quotidiano
    # 27/5/2021); 2024 Milan-only file in data -> growth NOT observed; scenarios +10/+15/+20 % (from memory ~+14 %).
    g_income=(0.10, 0.15, 0.20),
)
NH_BASKET1 = K["pov_single"] * (1 - K["rent_share_in_threshold"])        # ~754 EUR/month, single adult


def omi_growth():
    """OMI rent growth 2019/2 -> 2024/2 per fascia (B centre ... E/R suburbs), abitazioni civili, NORMALE. Real data."""
    t = open(os.path.join(ROOT, "mi", "raw", "omi_riepilogo.csv"), "rb").read().decode("utf-8-sig", "replace")
    o = pd.read_csv(io.StringIO(t), sep=";", dtype=str)
    o = o[(o.Cod_Tip == "20") & (o.Stato == "NORMALE")]
    for c in ("Loc_min", "Loc_max", "Compr_min", "Compr_max"): o[c] = pd.to_numeric(o[c].str.replace(",", "."), errors="coerce")
    o["loc"] = (o.Loc_min + o.Loc_max) / 2; o["prc"] = (o.Compr_min + o.Compr_max) / 2
    a = o[(o.Anno == "2019") & (o.Periodo.str.startswith("2"))].set_index("Zona")
    last = o[o.Anno == o.Anno.max()]; last = last[last.Periodo == last.Periodo.max()].set_index("Zona")
    j = a[["Fascia", "loc", "prc"]].join(last[["loc", "prc"]], rsuffix="_24", how="inner").dropna()
    j["rent_g"] = j.loc_24 / j["loc"] - 1; j["price_g"] = j.prc_24 / j.prc - 1
    g = j.groupby("Fascia").agg(zones=("rent_g", "size"), rent_g_median=("rent_g", "median"), price_g_median=("price_g", "median")).reset_index()
    g.loc[len(g)] = ["ALL", len(j), j.rent_g.median(), j.price_g.median()]
    return g, f"{o.Anno.max()}/{last.Periodo.iloc[0]}"


if __name__ == "__main__":
    # 1. erosion 2019 -> 2024/2025
    og, last = omi_growth(); og.to_csv(os.path.join(RES, "purchasing_power_omi.csv"), index=False)
    cpi_1924 = np.prod([1 + K["nic"][y] / 100 for y in range(2020, 2025)]) - 1
    cpi_1925 = np.prod([1 + K["nic"][y] / 100 for y in range(2020, 2026)]) - 1
    rg = float(og.set_index("Fascia").loc["ALL", "rent_g_median"])
    eros = [dict(g_income_nominal=g, cpi_2019_24=cpi_1924, real_income_change=(1 + g) / (1 + cpi_1924) - 1,
                 omi_rent_change=rg, income_vs_rent=(1 + g) / (1 + rg) - 1) for g in K["g_income"]]
    log("OMI rent growth", og.round(3).to_dict("records"), "CPI 2019-24", round(cpi_1924, 3))

    # 2. base (tau 30 % OR residual 750) vs residual-only with ISTAT non-housing basket (and ratio-only for reference)
    variants = {"base_tau30_or_resid750": dict(), "ratio_only_tau30": dict(test="ratio"),
                "residual_istat": dict(test="residual", basket1=NH_BASKET1),
                "residual_istat_hi_rentshare30": dict(test="residual", basket1=K["pov_single"] * 0.70),
                # A: 'decent living' basket = 1.5 x ISTAT non-housing (minimum-income-standard budgets are typically
                # well above absolute poverty; factor from memory, to verify)
                "residual_istat_x1.5": dict(test="residual", basket1=1.5 * NH_BASKET1),
                # 2019 counterfactual of the base rule: rent/income ratio back to 2019 (OMI +41 % vs income +15 %
                # nominal, mid scenario); same tax schedule and thresholds (approximation)
                "base_2019_relative_rents": dict(rent_mult=1.15 / 1.414)}
    OUT, NILS = {}, []
    for name, p in variants.items():
        R = demand.run(p, n_scen=0, nh=3000, seed=1, quiet=True)
        b, pool = R["base"], R["pool"]
        c = demand.city_stats(R); c.pop("individual_employee_check")
        OUT[name] = dict(D_total=float(b.D.sum()), share_target=c["share_target"], share_erp=c["share_erp"],
                         share_mkt_fail=c["share_mkt_fail"], target_net_p10_p50_p90=c["target_net_month_p10_p50_p90"])
        NILS.append(b[["nil_id", "D", "p_target", "p_mkt_fail"]].add_suffix("_" + name).rename(columns={"nil_id_" + name: "nil_id"}))
        if name == "base_tau30_or_resid750": POOL, H = pool, R["H"]
        log(name, round(b.D.sum()))

    # 3. per NIL real income and residuals (base draw)
    P = POOL.copy()
    P["Yreal"] = P.Y / K["p_milan"]
    P["basket"] = NH_BASKET1 * demand.OECD[P.s.values]
    P["res_rent"] = P.Y - P.R; P["res_rent_basket"] = P.Y - P.R - P.basket
    agg = lambda d: pd.Series(dict(hh=d.w.sum(), ynet_med=d.Y.median(), yreal_med=d.Yreal.median(), rent_med=d.R.median(),
                                    res_rent_med=d.res_rent.median(), res_basket_med=d.res_rent_basket.median(),
                                    share_neg_residual=(d.res_rent_basket < 0).mean(), rent_to_income_med=(d.R / d.Y.clip(lower=1)).median()))
    N = P.groupby("nil_id").apply(agg).reset_index()
    N = H[["nil_id", "name", "rent"]].merge(N, on="nil_id")
    for d in NILS: N = N.merge(d, on="nil_id")
    N["dD_resid_vs_base"] = N.D_residual_istat - N.D_base_tau30_or_resid750
    N.to_csv(os.path.join(RES, "purchasing_power_nil.csv"), index=False)
    T = P.groupby("s").apply(agg).reset_index().rename(columns={"s": "hh_size"})
    T["basket_nonhousing"] = NH_BASKET1 * demand.OECD[T.hh_size.values]
    T["fail_ratio30"] = P.groupby("s").apply(lambda d: (d.R > 0.3 * d.Y).mean()).values
    T["fail_resid_istat"] = P.groupby("s").apply(lambda d: (d.res_rent_basket < 0).mean()).values
    T.to_csv(os.path.join(RES, "purchasing_power_hhtype.csv"), index=False)

    # centre vs periphery: share of D in the 20 NIL with highest OMI rent
    top = set(H.sort_values("rent", ascending=False).nil_id.head(20))
    loc = {k: float(N[N.nil_id.isin(top)]["D_" + k].sum() / max(N["D_" + k].sum(), 1e-9)) for k in variants}

    # 4. re-solve P2 / P6 with residual-ISTAT demand (40 bootstrap scenarios)
    Rr = demand.run(dict(test="residual", basket1=NH_BASKET1), n_scen=40, nh=3000, seed=1, quiet=True)
    sp = dict(PF.SUP); M = PF.prepare(sp, Rr["S"]); port = {}
    for tag, g in (("P2r", None), ("P6r", 0.08)):
        r, site, nr = PF.solve_portfolio(M, sp, 1.0e9, gini_max=g, time_limit=TL)
        site.to_csv(os.path.join(RES, f"purchasing_power_sites_{tag}.csv"), index=False)
        old = pd.read_csv(os.path.join(RES, f"sites_{tag[:2]}.csv"), dtype={"ref": str})
        r["site_overlap_with_" + tag[:2]] = len(set(old.ref) & set(site.ref.astype(str))) / max(len(old), 1)
        r["top_nil"] = site.groupby("nil_name").dwellings.sum().sort_values(ascending=False).head(6).round().to_dict()
        port[tag] = r; log(tag, r["status"], round(r["dwellings"]), round(r["served_mean"]), round(r["gini_cov"], 3))
    tot = Rr["S"].groupby("scen").D.sum()
    js = dict(constants=K, nonhousing_basket_single=NH_BASKET1, omi_last_period=last, erosion=eros, variants=OUT,
              share_D_in_top20_rent_nil=loc, residual_istat_D_boot=[float(tot.quantile(.05)), float(tot.mean()), float(tot.quantile(.95))],
              portfolios=port, runtime_min=round((time.time() - T0) / 60, 1))
    json.dump(js, open(os.path.join(RES, "purchasing_power.json"), "w"), indent=1, default=str)
    log(json.dumps({k: v for k, v in js.items() if k != "constants"}, indent=1, default=str))
