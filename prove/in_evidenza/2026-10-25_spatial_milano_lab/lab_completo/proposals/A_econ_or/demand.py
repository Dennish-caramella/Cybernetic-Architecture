"""Step 1-2 - income distributions per CAP, synthetic households per NIL, affordability band, bootstrap demand.

Model (see model.md sections 2-3):
  * per-CAP grouped-data MLE of lognormal / Singh-Maddala / Dagum on MEF IRPEF 2024 class counts; best by AIC
  * class-exact hybrid sampling: class drawn from observed shares, value inside class from the fitted truncated law
  * IRPEF 2024 + Lombardy/Milan surtaxes -> net per taxpayer, calibrated per CAP to the observed MEF tax total
  * households by size (Census 2021) x earners (1 + Binomial(s-1, p_i)), exchangeable Gaussian copula rho
  * three-way band: ERP-eligible (ISEE proxy <= 16k) / TARGET (not ERP, market fails, social rent passes) / GREY
Run: PYTHONPATH=C:/Temp/pl python lab/proposals/A_econ_or/demand.py   (writes results/demand_*.csv)
"""
import json, os, sys, time
import numpy as np, pandas as pd
from scipy import optimize, stats

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
RES, CACHE = os.path.join(HERE, "results"), os.path.join(HERE, "results", "cache")
log = lambda *a: print(f"[{time.time() - T0:6.1f}s]", *a, file=sys.stderr, flush=True)

EDGES = np.array([0, 10e3, 15e3, 26e3, 55e3, 75e3, 120e3, np.inf])
CLS = ["0_10", "10_15", "15_26", "26_55", "55_75", "75_120", "gt120"]

# ---------------------------------------------------------------- parameters (A = assumption, S = cited source)
BASE = dict(
    tau=0.30,            # S: rent/net-income convention (report sec.1); normative, varied 0.25-0.40
    basket1=750.0,       # A: non-housing monthly basket, single adult (Istat absolute-poverty values not retrieved)
    isee_erp=16000.0,    # S [from memory]: Lombardy SAP ISEE ceiling, R.R. 4/2017
    social_rent=90.0,    # S: Piano Casa bandi 2026, EUR/m2/yr max average rent (ANSA 26/3/2026)
    renter=0.30,         # A: share of households in (or entering) the rental market; Milan census tenure not in data
    earn_k=1.0,          # A: multiplier on (mean earners - 1); 1 = calibrated to taxpayers/adult
    rho=0.3,             # A: within-household earnings correlation (exchangeable Gaussian copula)
    isee_rent_ded=1.0,   # S: ISEE deducts rent paid up to 7,000 EUR/yr (DPCM 159/2013); 0 = income-only boundary
    isp=0.0,             # A: 0.2 x net assets term of ISEE (EUR/yr); assets not in data, 0 = ERP upper bound
    test="both",         # affordability rule: "both" (ratio OR residual), "ratio", "residual"
)
# A: adequate dwelling m2 by household size (DM 22/4/2008 ~1 room per member; Piano Casa examples 50/70 m2)
AREA = np.array([0, 45, 55, 70, 85, 95, 110], float)
ISEE_SCALE = np.array([0, 1.00, 1.57, 2.04, 2.46, 2.85, 3.20])        # S: DPCM 159/2013 scale (+0.35 per extra member)
OECD = np.array([0, 1.0, 1.5, 1.8, 2.1, 2.4, 2.7])                     # A: modified OECD, 2 adults + (s-2) children


# ---------------------------------------------------------------- 1. income distributions
def cdf(model, th, y):
    y = np.maximum(y, 1e-9)
    if model == "LN": return stats.norm.cdf((np.log(y) - th[0]) / th[1])
    a, b, c = th
    z = (y / b) ** a
    if model == "SM": return 1 - (1 + z) ** (-c)
    return (1 + 1 / z) ** (-c)                     # Dagum


def ppf(model, th, u):
    u = np.clip(u, 1e-12, 1 - 1e-12)
    if model == "LN": return np.exp(th[0] + th[1] * stats.norm.ppf(u))
    a, b, c = th
    if model == "SM": return b * ((1 - u) ** (-1 / c) - 1) ** (1 / a)
    return b * (u ** (-1 / c) - 1) ** (-1 / a)


def fit_cap(n):
    """Grouped multinomial MLE on positive-income classes. Returns {model: (theta, loglik, aic)}."""
    out = {}
    for m, x0 in (("LN", [np.log(25e3), 0.9]), ("SM", [2.0, 30e3, 1.0]), ("Dagum", [3.0, 30e3, 0.7])):
        def nll(lt):
            th = np.exp(lt) if m != "LN" else np.array([lt[0], np.exp(lt[1])])
            p = np.diff(cdf(m, th, EDGES))
            return -np.sum(n * np.log(np.maximum(p, 1e-300)))
        z0 = np.log(x0) if m != "LN" else np.array([x0[0], np.log(x0[1])])
        r = optimize.minimize(nll, z0, method="Nelder-Mead", options=dict(maxiter=4000, xatol=1e-7, fatol=1e-7))
        th = np.exp(r.x) if m != "LN" else np.array([r.x[0], np.exp(r.x[1])])
        out[m] = (th, -r.fun, 2 * r.fun + 2 * len(th))
    return out


def sample_income(model, th, shares, p0, u_cls, u_in, alpha=None):
    """Class-exact hybrid draw. shares: class probs (positive part); p0: mass at <= 0 income.
    alpha: Pareto index of the open top class (>120k), matched to the observed class mean."""
    cum = np.concatenate([[p0], p0 + (1 - p0) * np.cumsum(shares)])
    k = np.searchsorted(cum, u_cls, side="right") - 1            # -1 => zero income
    kk = np.clip(k, 0, len(CLS) - 1)
    Fl, Fh = cdf(model, th, EDGES[kk]), cdf(model, th, EDGES[kk + 1])
    y = ppf(model, th, Fl + u_in * (Fh - Fl))
    y = np.clip(y, EDGES[kk], np.where(np.isinf(EDGES[kk + 1]), 5e6, EDGES[kk + 1]))
    if alpha is not None:
        top = kk == len(CLS) - 1
        y[top] = EDGES[-2] * (1 - u_in[top]) ** (-1 / alpha)
    return np.where(k < 0, 0.0, y)


# ---------------------------------------------------------------- 2. gross -> net (IRPEF 2024)
def tax_2024(y):
    """IRPEF 2024 (3 brackets 23/35/43, D.Lgs. 216/2023) with employee credit (art.13 TUIR) + Lombardy regional
    surtax (1.23/1.58/1.72/1.73 %) + Milan municipal 0.8 % above a 23k exemption [from memory, unverified]."""
    g = 0.23 * np.minimum(y, 28e3) + 0.35 * np.clip(y - 28e3, 0, 22e3) + 0.43 * np.maximum(y - 50e3, 0)
    d = np.select([y <= 15e3, y <= 28e3, y <= 50e3], [1955.0, 1910 + 1190 * (28e3 - y) / 13e3, 1910 * (50e3 - y) / 22e3], 0.0)
    d = d + np.where((y > 25e3) & (y <= 35e3), 65.0, 0.0)
    irpef = np.maximum(g - d, 0)
    reg = 0.0123 * np.minimum(y, 15e3) + 0.0158 * np.clip(y - 15e3, 0, 13e3) + 0.0172 * np.clip(y - 28e3, 0, 22e3) + 0.0173 * np.maximum(y - 50e3, 0)
    com = np.where(y > 23e3, 0.008 * y, 0.0)
    due = irpef > 0                       # surtaxes only when net IRPEF is due
    return irpef + due * (reg + com)


assert tax_2024(np.array([8e3]))[0] < 1 and 9000 < tax_2024(np.array([40e3]))[0] < 12000


# ---------------------------------------------------------------- data
def load_inputs():
    C = pd.read_csv(os.path.join(CACHE, "cap_classes.csv"), dtype={"cap": str})
    W = pd.read_csv(os.path.join(CACHE, "cap_nil_w.csv"), dtype={"cap": str})
    H = pd.read_csv(os.path.join(CACHE, "nil_hh.csv"))
    N = pd.read_csv(os.path.join(ROOT, "lab", "data", "nil.csv"))
    H = H.merge(N[["nil_id", "cx", "cy", "rent", "price", "a014", "pgt_srv_erp"]], on="nil_id")
    # 6 NIL lack OMI rent/price: nearest NIL (centroid) with a value. Assumption.
    ok = H.rent.notna()
    for i in np.where(~ok)[0]:
        d = np.hypot(H.cx[ok] - H.cx[i], H.cy[ok] - H.cy[i]); j = d.idxmin()
        H.loc[i, ["rent", "price"]] = H.loc[j, ["rent", "price"]].values
    H["pop"] = H.pop25.fillna(H.pop21c)
    H = H[H.hh25 >= 1].reset_index(drop=True)
    return C, W, H


def fit_all(C):
    rows, FIT = [], {}
    for _, r in C.iterrows():
        n = r[[f"n_{k}" for k in CLS]].values.astype(float)
        f = fit_cap(n)
        best = min(f, key=lambda m: f[m][2])
        mt = r.a_gt120 / max(r.n_gt120, 1)
        alpha = mt / (mt - EDGES[-2])                 # Pareto mean = alpha*x_m/(alpha-1)
        FIT[r.cap] = (best, f[best][0], alpha)
        # validation: fitted within-class mean vs observed class mean (amount / count)
        uu = (np.arange(4000) + 0.5) / 4000
        cm = []
        for j, k in enumerate(CLS):
            Fl, Fh = cdf(best, f[best][0], EDGES[j]), cdf(best, f[best][0], EDGES[j + 1])
            cm.append(np.mean(np.minimum(ppf(best, f[best][0], Fl + uu * (Fh - Fl)), 5e6)))
        obs = r[[f"a_{k}" for k in CLS]].values / np.maximum(n, 1)
        rows.append(dict(cap=r.cap, best=best, **{f"aic_{m}": f[m][2] for m in f},
                         **{f"th{j}": v for j, v in enumerate(f[best][0])},
                         pareto_alpha=alpha, mean_err_26_55=cm[3] / obs[3] - 1, mean_err_15_26=cm[2] / obs[2] - 1,
                         mean_err_gt120_parametric=cm[6] / obs[6] - 1))
    return FIT, pd.DataFrame(rows)


def tax_calibration(C, FIT, rng):
    """Per-CAP factor so that modelled total tax = MEF (Imposta netta + addizionali)."""
    out = {}
    for _, r in C.iterrows():
        n = r[[f"n_{k}" for k in CLS]].values.astype(float); M = 40000
        m, th, al = FIT[r.cap]
        y = sample_income(m, th, n / n.sum(), 0.0, rng.random(M), rng.random(M), al)
        model_tax = tax_2024(y).mean() * n.sum()
        out[r.cap] = (r.tax_irpef + r.tax_reg + r.tax_com) / model_tax
    return out


# ---------------------------------------------------------------- 3. synthetic households + band
def simulate(C, W, H, FIT, TCAL, par, rng, nh=4000, perturb=False):
    """One scenario. Returns per-NIL DataFrame and pooled household sample (for city statistics)."""
    caps = list(C.cap); cidx = {c: j for j, c in enumerate(caps)}
    n_cls = C[[f"n_{k}" for k in CLS]].values.astype(float)
    p0 = (C.n_le0 / C.taxpayers).values
    shares = n_cls / n_cls.sum(1, keepdims=True)
    if perturb:   # Bayesian bootstrap of class shares
        shares = np.array([rng.dirichlet(n + 1) for n in n_cls])
    rent_city = np.exp(rng.normal(0, 0.07)) if perturb else 1.0          # A: OMI band ~ +-15 % (2 sd)
    tp_city = C.taxpayers.sum()
    adults = H["pop"] * (1 - H.a014 / 100)
    tp_per_adult = tp_city / adults.sum()
    rows, pool = [], []
    for i, h in H.iterrows():
        w = W[W.nil_id == h.nil_id]
        a = w.addr.values.astype(float)
        pc = rng.dirichlet(a + 0.5) if perturb else a / a.sum()
        cj = np.array([cidx[c] for c in w.cap])
        sz = h[["s1", "s2", "s3", "s4", "s5", "s6"]].values.astype(float)
        s = rng.choice(np.arange(1, 7), size=nh, p=sz / sz.sum())
        e_mean = tp_per_adult * adults[i] / h.hh25
        p_i = np.clip(par["earn_k"] * (e_mean - 1) / max((s - 1).mean(), 1e-9), 0, 1)
        k = 1 + rng.binomial(s - 1, p_i)
        hc = cj[rng.choice(len(cj), size=nh, p=pc)]                       # household CAP
        z0 = rng.standard_normal(nh)
        ygross = np.zeros(nh); ynet = np.zeros(nh); isee_ded = np.zeros(nh)
        for e in range(k.max()):
            on = k > e
            z = np.sqrt(par["rho"]) * z0 + np.sqrt(1 - par["rho"]) * rng.standard_normal(nh)
            u = stats.norm.cdf(z)
            y = np.zeros(nh)
            for j in np.unique(hc[on]):
                mk = on & (hc == j)
                m, th, al = FIT[caps[j]]
                # copula uniform drives the class draw; independent uniform places the value in the class
                y[mk] = sample_income(m, th, shares[j], p0[j], u[mk], rng.random(mk.sum()), al)
                ynet[mk] += y[mk] - tax_2024(y[mk]) * TCAL[caps[j]]
            ygross += y; isee_ded += np.where(on, np.minimum(0.2 * y, 3000), 0)
        rent_m2 = h.rent * rent_city * par.get("rent_mult", 1.0) * (np.exp(rng.normal(0, 0.05)) if perturb else 1.0)
        R = rent_m2 * AREA[s]                                             # market rent EUR/month
        Rs = par["social_rent"] / 12 * AREA[s]                            # social (Piano Casa) rent
        Y = ynet / 12
        rt = lambda r: r > par["tau"] * Y
        rs = lambda r: Y - r < par["basket1"] * OECD[s]
        fails = {"both": lambda r: rt(r) | rs(r), "ratio": rt, "residual": rs}[par["test"]]
        isee = (np.maximum(ygross - isee_ded - par["isee_rent_ded"] * np.minimum(12 * R, 7000), 0) + par["isp"]) / ISEE_SCALE[s]
        erp = isee <= par["isee_erp"]
        mkt_fail = fails(R)
        tgt = ~erp & mkt_fail & ~fails(Rs)
        grey = ~erp & mkt_fail & fails(Rs)
        gap = np.maximum(R - par["tau"] * Y, 0) * 12                      # EUR/yr ratio gap
        rows.append(dict(nil_id=h.nil_id, hh=h.hh25, p_erp=erp.mean(), p_mkt_fail=mkt_fail.mean(), p_target=tgt.mean(),
                         p_grey=grey.mean(), D=par["renter"] * h.hh25 * tgt.mean(),
                         gap_eur=par["renter"] * h.hh25 * (gap * tgt).mean(),
                         ynet_med=np.median(Y), rent_m2=rent_m2, earners=k.mean()))
        pool.append(pd.DataFrame(dict(w=h.hh25 / nh, Y=Y, s=s, tgt=tgt, erp=erp, grey=grey, mkt=mkt_fail, k=k, nil_id=h.nil_id, R=R)))
    return pd.DataFrame(rows), pd.concat(pool, ignore_index=True)


def individual_check(C, FIT, TCAL, par, rng, rent_city_m2):
    """Validation vs '37-38 % ceto medio escluso' (employees): single earner as 1-person household at city rent."""
    n_cls = C[[f"n_{k}" for k in CLS]].values.astype(float)
    wt = C.emp_n.values / C.emp_n.sum(); out = []
    for j, c in enumerate(C.cap):
        M = int(60000 * wt[j]) + 1; m, th, al = FIT[c]
        y = sample_income(m, th, n_cls[j] / n_cls[j].sum(), 0.0, rng.random(M), rng.random(M), al)
        out.append(np.c_[y, y - tax_2024(y) * TCAL[c]])
    y, yn = np.vstack(out).T
    Y = yn / 12; R = rent_city_m2 * AREA[1]
    isee = np.maximum(y - np.minimum(0.2 * y, 3000) - par["isee_rent_ded"] * min(12 * R, 7000), 0) + par["isp"]
    fails = lambda r: (r > par["tau"] * Y) | (Y - r < par["basket1"])
    return dict(share_mkt_fail=float(fails(R).mean()), share_erp=float((isee <= par["isee_erp"]).mean()),
                share_excluded_not_erp=float((fails(R) & (isee > par["isee_erp"])).mean()),
                share_target=float((fails(R) & (isee > par["isee_erp"]) & ~fails(par["social_rent"] / 12 * AREA[1])).mean()),
                share_net_1500_2500=float(((Y >= 1500) & (Y <= 2500)).mean()))


def run(par=None, n_scen=40, nh=3000, seed=1, quiet=False):
    par = {**BASE, **(par or {})}
    rng = np.random.default_rng(seed)
    C, W, H = load_inputs()
    FIT, fitdf = fit_all(C)
    TCAL = tax_calibration(C, FIT, rng)
    base, pool = simulate(C, W, H, FIT, TCAL, par, rng, nh=nh * 2)
    scen = []
    for w in range(n_scen):
        p = dict(par, earn_k=par["earn_k"] * rng.uniform(0.8, 1.2), rho=float(np.clip(par["rho"] + rng.uniform(-0.2, 0.2), 0, 0.9)),
                 basket1=par["basket1"] * rng.uniform(0.85, 1.15), renter=par["renter"] * rng.uniform(0.85, 1.15))
        d, _ = simulate(C, W, H, FIT, TCAL, p, rng, nh=nh, perturb=True)
        d["scen"] = w; scen.append(d)
        if not quiet and w % 10 == 9: log("scenario", w + 1)
    S = pd.concat(scen, ignore_index=True) if scen else None
    return dict(par=par, C=C, W=W, H=H, FIT=FIT, fitdf=fitdf, TCAL=TCAL, base=base, pool=pool, S=S)


def city_stats(R):
    pool, H = R["pool"], R["H"]; w = pool.w
    out = dict(households=float(H.hh25.sum()), share_erp=float(np.average(pool.erp, weights=w)),
               share_target=float(np.average(pool.tgt, weights=w)), share_grey=float(np.average(pool.grey, weights=w)),
               share_mkt_fail=float(np.average(pool.mkt, weights=w)), D_total_base=float(R["base"].D.sum()),
               target_net_month_p10_p50_p90=[float(np.quantile(pool.Y[pool.tgt], v)) for v in (.1, .5, .9)] if pool.tgt.any() else None,
               earners_city=float(np.average(pool.k, weights=w)))
    out["individual_employee_check"] = individual_check(R["C"], R["FIT"], R["TCAL"], R["par"], np.random.default_rng(7),
                                                        float(np.average(H.rent, weights=H.hh25)))
    return out


def main():
    R = run()
    base, S, H = R["base"], R["S"], R["H"]
    R["fitdf"].assign(tax_calib=R["fitdf"].cap.map(R["TCAL"])).to_csv(os.path.join(RES, "income_fits.csv"), index=False)
    q = S.groupby("nil_id").agg(D_mean=("D", "mean"), D_p05=("D", lambda v: v.quantile(.05)), D_p95=("D", lambda v: v.quantile(.95)),
                                gap_mean=("gap_eur", "mean"), gap_p05=("gap_eur", lambda v: v.quantile(.05)), gap_p95=("gap_eur", lambda v: v.quantile(.95)))
    out = H[["nil_id", "name", "hh25", "rent"]].merge(base, on="nil_id", suffixes=("", "_b")).merge(q, on="nil_id")
    out.to_csv(os.path.join(RES, "demand_nil.csv"), index=False)
    S.to_csv(os.path.join(RES, "demand_scenarios.csv"), index=False)
    tot = S.groupby("scen")[["D", "gap_eur"]].sum()
    city = dict(city_stats(R), D_total_mean=float(tot.D.mean()), D_total_p05=float(tot.D.quantile(.05)), D_total_p95=float(tot.D.quantile(.95)),
                gap_total_mean_eur=float(tot.gap_eur.mean()), gap_p05=float(tot.gap_eur.quantile(.05)), gap_p95=float(tot.gap_eur.quantile(.95)),
                fit_best_counts=R["fitdf"].best.value_counts().to_dict(),
                tax_calib_range=[float(min(R["TCAL"].values())), float(max(R["TCAL"].values()))], params=R["par"])
    json.dump(city, open(os.path.join(RES, "demand_city.json"), "w"), indent=1)
    log(json.dumps(city, indent=1))
    return R


if __name__ == "__main__":
    main()
