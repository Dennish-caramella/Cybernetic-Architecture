"""Tests of review1 §5.9. Run: PYTHONPATH=C:/Temp/pl python lab/model/tests.py
1-3 and 5 are synthetic (SYNTHETIC data, labelled); 4 checks invariants on lab/model/out/base.pkl + lab/results/model.json
(run run.py first); 6 summarises lab/results/sensitivity.csv. Writes lab/results/tests.json."""
import itertools, json, os, pickle, time
import numpy as np, pandas as pd
from scipy import stats, optimize
from scipy.special import expit
from config import *
import audit as AU, portfolios as PO, smaa as SM, export as EX

R_ = {}


def record(name, ok, **kw):
    R_[name] = dict(ok=bool(ok), **kw); print(("PASS " if ok else "FAIL ") + name, kw, flush=True)


# ---------------------------------------------------------------- synthetic city (SYNTHETIC)
def synth_city(rng, I=40, S=400):
    p = np.sort(rng.uniform(0.05, 0.40, I))                       # low-income share by NIL
    N = pd.DataFrame(dict(hh=rng.uniform(3000, 15000, I), p_erp=p, poor=20 + 40 * p + rng.normal(0, 1, I),
                          for_=10 + 50 * p, net_m=2600 - 2000 * p, q5=p >= np.quantile(p, 0.8)))
    N["kap"] = 0.03 * N.hh
    site = pd.DataFrame(dict(nil=rng.integers(0, I, S), area=rng.lognormal(8.5, 0.6, S), ring=rng.integers(0, 5, S),
                             opp=rng.random(S)))
    site["cap"] = np.minimum(np.floor(0.7 * site.area / 80), 400)
    return N, site


def test_audit_recovery():
    rng = np.random.default_rng(11)
    N, site = synth_city(rng)
    poorest = np.argsort(-N.p_erp.values)[:8]                    # 20 % poorest NIL
    G = rng.choice(np.where(np.isin(site.nil, poorest))[0], 15, replace=False)
    A = AU.Auditor(N, site)
    pool = ~np.isin(np.arange(len(site)), G)
    res = {k: A.test(G, pool, k, R=999, rng=np.random.default_rng(1))[0]["dDI"] for k in ("size", "ring")}
    ok = all(r["p_up"] < 0.01 and r["obs"] > r["p95"] for r in res.values())
    record("1a_planted_segregation_detected", ok, p_size=res["size"]["p_up"], p_ring=res["ring"]["p_up"],
           z_size=round(res["size"]["z"], 2))
    # review2: G is a random draw from ALL sites, so the exchangeable (permutation) null draws from all sites incl. G.
    # The old complement pool was anti-conservative: 0.061 [0.051, 0.072] over 2000 reps vs 0.042 [0.034, 0.052] here.
    # 1000 reps (spec: 50) so the rate is estimated to +-1.4 pp; pass = spec bound <= 0.10 AND exact CI covers or is below 0.05.
    fp = []
    for k in range(1000):
        r2 = np.random.default_rng(100 + k); N2, s2 = synth_city(r2)
        G2 = r2.choice(len(s2), 15, replace=False); pool2 = np.ones(len(s2), bool)
        fp.append(AU.Auditor(N2, s2).test(G2, pool2, "size", R=99, rng=r2)[0]["dDI"]["p_up"] < 0.05)
    fp = np.array(fp); ci = stats.binomtest(int(fp.sum()), len(fp)).proportion_ci(method="exact")
    record("1b_false_positive_rate", fp.mean() <= 0.10 and ci.low <= 0.05, fp_rate_1000=float(fp.mean()),
           ci95=[round(ci.low, 3), round(ci.high, 3)], fp_rate_first50=float(fp[:50].mean()))


def test_clustered_h0(reps=1000):
    """review2: designated sets concentrated in few NIL under H0 (k = 3 random NIL, no planted effect). FP rate of the
    site-level size null and of the NIL-block null at nominal 0.05 (one-sided dDI), exact 95 % CIs. Pass: the block null
    is calibrated (rate <= 0.10 and CI lower bound <= 0.05). The site-level rate is reported (expected anti-conservative)."""
    site_fp, blk_fp = [], []
    for k in range(reps):
        r = np.random.default_rng(5000 + k); N, s = synth_city(r)
        nils = r.choice(len(N), 3, replace=False)
        cand = np.where(np.isin(s.nil.values, nils))[0]
        G = r.choice(cand, min(15, len(cand)), replace=False)
        A = AU.Auditor(N, s); allp = np.ones(len(s), bool)
        site_fp.append(A.test(G, allp, "size", R=99, rng=r, keys=["dDI"])[0]["dDI"]["p_up"] < 0.05)
        m = np.zeros(len(s), bool); m[G] = True
        pcap = np.bincount(s.nil.values, s.cap.values, len(N))
        p, _ = AU.block_test(A, m, pcap, None, R=99, seed=int(r.integers(1e9)), keys=("dDI",))
        blk_fp.append(p["dDI"] < 0.05)
    out = {}
    for name, v in (("site_null", site_fp), ("nil_block_null", blk_fp)):
        v = np.array(v); ci = stats.binomtest(int(v.sum()), len(v)).proportion_ci(method="exact")
        out[name] = dict(fp=float(v.mean()), ci95=[round(ci.low, 3), round(ci.high, 3)])
    b = out["nil_block_null"]
    record("1c_clustered_h0_false_positive", b["fp"] <= 0.10 and b["ci95"][0] <= 0.05, reps=reps, nil_per_set=3, **out)


def test_null_calibration():
    rng = np.random.default_rng(5)
    N, site = synth_city(rng); A = AU.Auditor(N, site)
    allp = np.ones(len(site), bool); G0 = rng.choice(len(site), 12, replace=False)
    ps = []
    for k in range(200):
        # exact exchangeability: the 'designated' set is one more draw of the same null generator (same target)
        d, _ = A.draw(G0, allp, "size", 200, rng)
        r = A.test(d[0], allp, "size", draws=d[1:])[0]["dDI"]
        ps.append(r["p_up"] - rng.uniform(0, 1 / 200))               # randomised p (removes the 1/(R+1) grid)
    ks = stats.kstest(ps, "uniform")
    record("5_null_pvalues_uniform", ks.pvalue > 0.05, ks_p=round(float(ks.pvalue), 3), mean_p=round(float(np.mean(ps)), 3))


# ---------------------------------------------------------------- MILP vs brute force (SYNTHETIC toy)
def toy():
    rng = np.random.default_rng(3)
    Sn, I, W = 5, 3, 4
    M = dict(idx=np.arange(Sn), cap=np.array([60, 45, 80, 30, 50.]), fixed=rng.uniform(1e6, 4e6, Sn), var=np.full(Sn, 1.6e5),
             origin=np.array(["SOFT"] * Sn), D=rng.uniform(20, 70, (I, W)), ids=[0, 1, 2], host=np.array([0, 0, 1, 2, 2]),
             kap=np.array([70., 60, 70]))
    ps, pi = np.meshgrid(np.arange(Sn), np.arange(I), indexing="ij"); ps, pi = ps.ravel(), pi.ravel()
    pw = np.where(M["host"][ps] == pi, 1.0, 0.4)
    M.update(ps=ps, pi=pi, pw=pw)
    return M


def brute(M, budget, beta=0.5, alpha=0.2):
    """Independent formulation: enumerate y, solve the LP in (x, u, eta, xi) with scipy linprog."""
    cap, fixed, var, ps, pi, pw, D = M["cap"], M["fixed"], M["var"], M["ps"], M["pi"], M["pw"], M["D"]
    Sn, P = len(cap), len(ps); I, W = D.shape; best = -np.inf
    for y in itertools.product([0, 1], repeat=Sn):
        y = np.array(y)
        if (fixed * y).sum() > budget: continue
        nx, nu = P, I * W; n = nx + nu + 1 + W
        c = np.zeros(n); c[nx:nx + nu] = -(1 - beta) / W; c[nx + nu] = -beta; c[nx + nu + 1:] = beta / (alpha * W)
        A, b = [], []
        def row(d, rhs):
            r = np.zeros(n)
            for k, v in d: r[k] += v
            A.append(r); b.append(rhs)
        for s in range(Sn):
            on = np.where(ps == s)[0]
            row([(k, 1) for k in on], cap[s] * y[s]); row([(k, -1) for k in on], -SUP["m_min"] * y[s])
        row([(k, var[ps[k]]) for k in range(P)], budget - (fixed * y).sum())
        for i in range(I):
            on = np.where(pi == i)[0]; row([(k, 1) for k in on], D[i].max())
            for w in range(W): row([(nx + w * I + i, 1)] + [(k, -pw[k]) for k in on], 0)
        for h in range(I):
            on = np.where(M["host"][ps] == h)[0]; row([(k, 1) for k in on], M["kap"][h])
        for w in range(W): row([(nx + nu + 1 + w, -1), (nx + nu, 1)] + [(nx + w * I + i, -1) for i in range(I)], 0)
        bounds = [(0, None)] * nx + [(0, D[i, w]) for w in range(W) for i in range(I)] + [(None, None)] + [(0, None)] * W
        r = optimize.linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=bounds, method="highs")
        if r.status == 0: best = max(best, -r.fun)
    return best


def test_milp():
    M = toy(); budget = 2.6e7
    r, ys, _ = PO.solve(M, budget=budget, gap=1e-9, time_limit=30)
    bf = brute(M, budget)
    record("2a_milp_equals_bruteforce", abs(r["obj"] - bf) < 1e-4 * max(1, abs(bf)), milp=round(r["obj"], 4), brute=round(bf, 4))
    out = PO.diverse_set(M, K=3, budget=budget, gap=1e-9)
    ov = [o[0]["max_overlap_prev"] for o in out[1:]]
    record("2b_diversity_cuts_overlap_le_70pct", all(v <= 0.7 + 1e-9 for v in ov), n=len(out), overlaps=[round(v, 2) for v in ov])


# ---------------------------------------------------------------- learning (B's learner on the real site matrix)
def test_learning(base):
    X = base["X"].values; keep = base["keep"]
    rng = np.random.default_rng(4)
    XR = X[keep][np.argsort(-base["S"].hol.values[keep])[:300]]
    m = XR.shape[1]; tvs = []
    for p in range(8):
        wt = rng.dirichlet(np.ones(m))
        L = SM.E.PrefLearner(XR, lambda P, r: r.dirichlet(np.ones(m), P), lambda W: SM.E.dirichlet_logpdf(W, np.ones(m)),
                             P=3000, beta=15.0, eps=0.05, rng=rng)
        for q in range(25):
            pr = rng.integers(0, len(XR), (600, 2)); Dd = XR[pr[:, 0]] - XR[pr[:, 1]]
            pr = pr[(Dd > 1e-9).any(1) & (Dd < -1e-9).any(1)][:200]
            a, b = pr[L.scores(pr, "w").argmax()]
            L.update(a, b, int(rng.random() < expit(50 * wt @ (XR[a] - XR[b]))))
        tvs.append(0.5 * np.abs(L.mean() - wt).sum())
    record("3_weight_recovery_tv", np.mean(tvs) < 0.15, tv_mean=round(float(np.mean(tvs)), 3), tv_max=round(float(np.max(tvs)), 3), criteria=m, questions=25)


# ---------------------------------------------------------------- invariants (real run)
def test_invariants(base):
    C, ps, S = base["C"], base["psite"], base["S"]
    inn = ps >= 0
    ex = (C.loc[inn, SITE["excl_cols"]] >= SITE["excl_share"]).any(axis=1).sum()
    record("4a_no_pcu_no_green_in_sites", int(C.pcu[inn].sum()) == 0 and ex == 0, pcu=int(C.pcu[inn].sum()), green=int(ex))
    record("4b_parcel_in_one_site", C.ref.is_unique and ps.ndim == 1, parcels_in_sites=int(inn.sum()))
    d = abs(S.area_m2.sum() / C.area_m2[inn].sum() - 1)
    record("4c_site_area_equals_parcel_sum", d <= 0.001, rel_diff=d)
    N = base["N"]; kap = N.set_index("nil_id").kap
    viol_serv = viol_kap = viol_bud = 0
    for p in base["P"]:
        r = p["r"]
        if not r.get("feasible", True): continue
        Dl = base["Dl"]; lay = p.get("layer", base["layer"])
        Dbar = Dl[Dl.scen >= 0].pivot(index="nil_id", columns="scen", values=lay).reindex(base["ids"]).fillna(0).mean(1).values
        viol_serv += int((r["served_nil"] > Dbar + 1e-6).sum())
        host = S.nil_id.values[base["M_idx"]]
        b = pd.Series(p["built"]).groupby(host).sum()
        viol_kap += int((b > kap.reindex(b.index).fillna(np.inf) + 1e-6).sum())
        viol_bud += int(r["cost_eur"] > PORT["budget"] * (1 + 1e-9))
    record("4d_served_le_demand", viol_serv == 0, violations=viol_serv, note="mean over scenarios; per-scenario u<=D is a variable bound")
    record("4e_kappa_respected", viol_kap == 0, violations=viol_kap)
    record("4f_budget_respected", viol_bud == 0, violations=viol_bud)
    B = base["Bu"]
    record("4g_acceptability_columns_sum_to_1", np.allclose(B.sum(0), 1), max_dev=float(np.abs(B.sum(0) - 1).max()))
    dom = S.depth >= SMAA["K"]
    record("4h_dominated_sites_zero_topk", float(S.top10_uniform[dom].sum()) == 0, n_dominated=int(dom.sum()))
    J = json.load(open(os.path.join(RES, "model.json"), encoding="utf-8"))
    errs = []
    for s, g in zip(J["sites"], S.geom):
        a = EX.dec_geom(s["g"]).area
        errs.append(abs(a / g.area - 1))
    errs = np.array(errs)
    record("4i_export_geometry_area_within_2pct", (errs <= 0.02).mean() >= 0.99, share_within=round(float((errs <= 0.02).mean()), 4),
           p99=round(float(np.quantile(errs, .99)), 4), max=round(float(errs.max()), 4))
    bad = {"household", "households_list", "Y", "ynet", "isee", "pool", "hh_id", "person"}
    keys = set()
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items(): keys.add(k); walk(v)
        elif isinstance(o, list):
            for v in o[:50]: walk(v)
    walk(J)
    size = os.path.getsize(os.path.join(RES, "model.json")) / 1e6
    record("4j_no_household_records_in_export", not (keys & bad), forbidden_keys_found=sorted(keys & bad), size_mb=round(size, 2))


def test_sensitivity():
    f = os.path.join(RES, "sensitivity.csv")
    if not os.path.exists(f): record("6_sensitivity_summary", False, note="sensitivity.csv missing"); return
    T = pd.read_csv(f); out = {}
    for g in ("AT", "AMB_DEG", "ERP"):
        out[g] = round(1 - T[f"flip_{g}"].mean(), 3)
    stable = {g: v >= 2 / 3 for g, v in out.items()}
    R_["6_sensitivity_summary"] = dict(ok=None, reported=True, label_stability=out, stable_ge_2_3=stable,
                                      kendall_tau_median=float(T.kendall_tau_hol.median()), p1_overlap_median=float(T.p1_overlap.median()))
    print("INFO 6_sensitivity_summary", R_["6_sensitivity_summary"])


if __name__ == "__main__":
    t = time.time()
    test_milp(); test_audit_recovery(); test_clustered_h0(); test_null_calibration()
    base = pickle.load(open(os.path.join(OUT, "base.pkl"), "rb"))
    test_learning(base); test_invariants(base); test_sensitivity()
    R_["_runtime_s"] = round(time.time() - t, 1)
    json.dump(R_, open(os.path.join(RES, "tests.json"), "w"), indent=1, default=lambda v: v.item() if hasattr(v, "item") else str(v))
    n_fail = sum(1 for k, v in R_.items() if isinstance(v, dict) and v.get("ok") is False)
    print(f"{n_fail} failed, runtime {R_['_runtime_s']} s")
