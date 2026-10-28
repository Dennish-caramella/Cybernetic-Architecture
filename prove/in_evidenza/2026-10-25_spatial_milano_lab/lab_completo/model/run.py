"""End-to-end integrated model. Run: PYTHONPATH=C:/Temp/pl python lab/model/run.py  [--no-sens]
Writes lab/results/{model.json, sites.csv, demand_layers.csv, portfolios.csv, audit_*.csv, sensitivity.csv, results.md}
and lab/model/out/base.pkl (for tests.py). Re-running picks up A's purchasing-power layer if it appeared."""
import contextlib, copy, json, os, pickle, sys, time
import numpy as np, pandas as pd
from scipy import sparse, stats
from scipy.spatial import cKDTree
from config import *
import sites as ST, demand as DM, criteria as CR, smaa as SM, portfolios as PO, audit as AU


@contextlib.contextmanager
def override(**kw):
    """Temporarily change config parameters (dicts are shared by reference with every module)."""
    where = dict(tau=(DEM, "tau"), basket=(DEM, "basket_mult"), lam_km=(DEM, "lam_km"), kappa=(PORT, "kappa"),
                 far=(SUP, "far"), sigma=(AUDIT, "sigma"), buffer_m=(SITE, "buffer_m"), n_scen=(DEM, "n_scen"),
                 time_limit=(PORT, "time_limit"), K=(PORT, "K"))
    old = {k: where[k][0][where[k][1]] for k in kw}
    old_ke = PORT["kappa_erp"]
    try:
        for k, v in kw.items(): where[k][0][where[k][1]] = v
        if "kappa" in kw: PORT["kappa_erp"] = kw["kappa"] / 2
        yield
    finally:
        for k, v in old.items(): where[k][0][where[k][1]] = v
        PORT["kappa_erp"] = old_ke


def nil_table(Dl, ids, layer, pp):
    N = pd.read_csv(os.path.join(LAB, "data", "nil.csv")).set_index("nil_id").reindex(ids)
    base = Dl[Dl.scen == -1].set_index("nil_id").reindex(ids)
    T = pd.DataFrame(dict(nil_id=ids, name=N.nil_name.values, hh=base.hh.values, p_erp=base.p_erp.values,
                          poor=N.poor.fillna(N.poor.median()).values, for_=N.for_.fillna(N.for_.median()).values,
                          net_m=N.net_m.fillna(N.net_m.median()).values, srv_erp=N.pgt_srv_erp.fillna(0).values))
    if pp is not None:
        T = T.merge(pp, on="nil_id", how="left"); T["resid"] = T.resid_p50.fillna(T.resid_p50.median())
    T["q5_or"] = (T.p_erp >= T.p_erp.quantile(0.8)) | (T.srv_erp >= T.srv_erp.quantile(0.8))   # old definition (reported)
    # review2 household floor: NIL below hh_floor carry CAP-imputed income -> placement values set to the city mean
    T["low_hh"] = T.hh < AUDIT["hh_floor"]
    big = ~T.low_hh
    for c in [c for c in ("poor", "for_", "net_m", "resid") if c in T]:
        T[c + "_raw"] = T[c]
        T.loc[T.low_hh, c] = float(np.average(T.loc[big, c], weights=T.loc[big, "hh"]))
    T["q5"] = big & (T.p_erp >= T.p_erp[big].quantile(0.8))          # review2: p_erp only, among NIL above the floor
    T["kap"] = np.where(T.srv_erp > 5, PORT["kappa_erp"], PORT["kappa"]) * T.hh
    D = Dl[Dl.scen >= 0].pivot(index="nil_id", columns="scen", values=layer).reindex(ids).fillna(0)
    T["D"] = D.mean(1).values
    if layer != "D_tau":
        T["D2"] = Dl[Dl.scen >= 0].pivot(index="nil_id", columns="scen", values="D_tau").reindex(ids).fillna(0).mean(1).values
    return T, D


def pipeline(full=True, R=None, verbose=True, C_geo=None):
    """Runs sites -> demand -> criteria -> SMAA -> portfolios -> audit. Returns a dict of everything."""
    lg = log if verbose else (lambda *a: None)
    out = {}
    C, counts = ST.candidate_parcels() if C_geo is None else C_geo[0]
    geoms = ST.decode_geoms(C) if C_geo is None else C_geo[1]
    psite, S = ST.build_sites(C, geoms)
    S = ST.add_capacity_cost(S)
    lg("sites", len(S), S.origin.value_counts().to_dict())
    pp = DM.pp_nil(); pp_ok = pp is not None
    Dl = DM.simulate_layers()
    layer = "D_res_decent" if pp_ok else "D_tau"
    ids = sorted(Dl.nil_id.unique())
    N, Dp = nil_table(Dl, ids, layer, pp)
    Dlay = {l: Dl[Dl.scen >= 0].pivot(index="nil_id", columns="scen", values=l).reindex(ids).fillna(0)
            for l in ("D_tau", "D_res_decent", "D_res_istat") if l in Dl}
    lg("demand", {l: round(float(d.sum(0).mean())) for l, d in Dlay.items()}, "pp", pp_ok)
    if full:   # F-A1: city-wide search variant and rent/income decomposition (base draw)
        cv = DM.city_search_variant().merge(Dl[Dl.scen == -1][["nil_id", "hh", "D_tau"]], on="nil_id")
        rate = lambda c: cv[c] / cv.hh
        out["fa1"] = dict(D_tau_base=float(cv.D_tau.sum()), D_city_search=float(cv.D_city.sum()),
                          D_tau_median_rent=float(cv.D_medrent.sum()),
                          var_share_income=float(np.average((rate("D_medrent") - np.average(rate("D_medrent"), weights=cv.hh)) ** 2, weights=cv.hh)
                                                 / np.average((rate("D_tau") - np.average(rate("D_tau"), weights=cv.hh)) ** 2, weights=cv.hh)),
                          rho_rate_rent=float(stats.spearmanr(rate("D_tau"), pd.read_csv(os.path.join(LAB, "data", "nil.csv")).set_index("nil_id").rent.reindex(cv.nil_id).values, nan_policy="omit")[0]))
        lg("F-A1", out["fa1"])
    hx = DM.hex_table()
    dem_m, dem_p05 = DM.dem_reach(S, hx, Dp)
    acc = CR.site_access(C, psite, len(S))
    raw, X, cspec = CR.build(S, acc, dem_m)
    sm, Bu, keep = SM.site_smaa(X.values)
    S = pd.concat([S, sm], axis=1); S["dem_mean"], S["dem_p05"] = dem_m, dem_p05
    lg("smaa reduced", len(keep))
    rad = np.hypot(S.x.values, S.y.values)
    S["ring"] = np.searchsorted(np.quantile(rad, [.2, .4, .6, .8]), rad)
    # ---------------- portfolios
    pairs = DM.site_nil_weights(S, hx, ids)
    models = {l: PO.prepare(S, Dlay[l], pairs, N.kap.values) for l in Dlay if l != "D_res_istat"}
    M = models[layer]
    S["score"] = S.hol + 0.01 * S.eu
    P = []
    tl = dict(time_limit=PORT["time_limit_choice"], gap=PORT["gap_choice"]) if full else {}
    div = PO.diverse_set(M, K=PORT["K"] if full else 1, **tl)
    for k, (r, ys, b) in enumerate(div): P.append(dict(id=f"P{k + 1}", lens="diverse" if k else "unconstrained", r=r, y=ys, built=b))
    if full:
        org = M["origin"]
        for lid, kw in (("L_pgt", dict(allowed=org != "SOFT")), ("L_people", dict(allowed=org == "SOFT")),
                        ("L_gini", dict(gini_max=PORT["gini"])),
                        ("L_smaa", dict(objective="score", score=S.score.values[M["idx"]]))):
            r, ys, b = PO.solve(M, **kw, **tl); P.append(dict(id=lid, lens=lid[2:], r=r, y=ys, built=b)); lg(lid, r.get("status"), r.get("sites"))
        other = "D_tau" if layer != "D_tau" else None
        if other:
            Mo = models[other]; r, ys, b = PO.solve(Mo, **tl)          # same site pool order (prepare is deterministic on S)
            P.append(dict(id="L_dtau", lens="demand_tau", r=r, y=ys, built=b, layer=other))
        out["matched"] = matched_pools(S, Dlay[layer], pairs, N.kap.values, P, lg)
    # ---------------- audit context
    S["rent_g"] = DM.rent_erosion_at(S.x.values, S.y.values)
    S["opp"] = X[["access_metro", "access_jobs", "services", "green_access", "heat"]].mean(1).values
    pos = {n: j for j, n in enumerate(ids)}
    cx = cKDTree(np.c_[S.x, S.y])
    S["nil"] = [pos.get(n, -1) for n in S.nil_id]
    if (S.nil < 0).any():                      # NIL without households: nearest site's NIL
        okm = S.nil >= 0; t = cKDTree(np.c_[S.x[okm], S.y[okm]])
        S.loc[~okm, "nil"] = S.nil[okm].values[t.query(np.c_[S.x[~okm], S.y[~okm]])[1]]
    s_, i_, w_ = pairs
    W = sparse.csr_matrix((w_, (s_, i_)), shape=(len(S), len(ids)))
    th = cKDTree(hx[["x", "y"]].values)
    def covm(r):
        nb = th.query_ball_point(np.c_[S.x, S.y], r)
        rr = np.concatenate([np.full(len(n), k) for k, n in enumerate(nb)]); cc = np.concatenate(nb).astype(int)
        return sparse.csr_matrix((np.ones(len(rr)), (rr, cc)), shape=(len(S), len(hx)))
    hn = pd.read_csv(os.path.join(PROP, "C_ml_spatial", "results", "hex_need.csv"))
    hex_hh = np.where(hn.sig_fdr05 & (hn.lisa_quad == "HH"), hn["pop"], 0.0)
    hex_dem = Dp.reindex(hx.nil_id).fillna(0).values.mean(1) * hx.pop_share.values
    site_a = pd.DataFrame(dict(nil=S.nil.values, area=S.area_m2.values, cap=S.cap.values, ring=S.ring.values, opp=S.opp.values,
                               rent_g=S.rent_g.values, fixed=S.fixed_eur.values, var=S.var_eur.values, hol=S.hol.values,
                               min_arch=S.min_arch.values))
    A = AU.Auditor(N, site_a, W, covm(3.0), covm(1.0), hex_dem, hex_hh)
    sets = {"AT": S.origin.eq("AT").values, "AMB_DEG": S.origin.eq("AMB_DEG").values, "ERP": S.origin.eq("ERP").values,
            "RIG": (S.origin.eq("SOFT") & (S.pgt_rig >= 0.5)).values}
    soft = S.origin.eq("SOFT").values
    res, match = {}, {}
    for g, m in sets.items():
        pool = soft | m        # review2: permutation null over candidate land incl. G (complement pool was anti-conservative)
        res[g] = {}
        for null in ("size", "ring"):
            res[g][null], match[(g, null)] = A.test(np.where(m)[0], pool, null, R=R or AUDIT["R"], rng=np.random.default_rng(AUDIT["seed"]))
    labels, Q = AU.verdict(res, ["AT", "AMB_DEG", "ERP"])
    lg("audit labels", labels)
    # review2 robustness (post hoc, not in the verdict): NIL-block null, and ERP 'potential' with ERP land at market cost
    block = {}
    if full:
        nxy = pd.read_csv(os.path.join(LAB, "data", "nil.csv")).set_index("nil_id").reindex(ids)
        nring = np.searchsorted(np.quantile(rad, [.2, .4, .6, .8]), np.hypot(nxy.cx.values, nxy.cy.values))
        pcap = np.bincount(S.nil.values[soft], S.cap.values[soft], len(ids))
        for g in ("AT", "AMB_DEG", "ERP"):
            for null, rr in (("nil_block", None), ("nil_block_ring", nring)):
                p, info = AU.block_test(A, sets[g], pcap, rr)
                block[(g, null)] = dict(**p, **info)
        mk = SUP["land_inc"] * S.nil_price * S.cap * SUP["gfa_dw"] + SUP["c_demo"] * S.volume_m3
        Am = AU.Auditor(N, site_a.assign(fixed=np.where(S.origin.eq("ERP"), mk, S.fixed_eur)), W)
        for null in ("size", "ring"):
            r, _ = Am.test(np.where(sets["ERP"])[0], soft | sets["ERP"], null, R=R or AUDIT["R"], rng=np.random.default_rng(AUDIT["seed"]),
                           keys=["served_per_meur"])
            block[("ERP_market_land", null)] = dict(served_per_meur=r["served_per_meur"]["obs"], null_median=r["served_per_meur"]["median"])
        # AT with / without Stephenson (92 households, CAP-imputed income) and without the household floor
        st = [j for j, n in enumerate(N.name) if n == "Stephenson"]
        mS = sets["AT"] & ~np.isin(S.nil.values, st)
        for null in ("size", "ring"):
            r, _ = A.test(np.where(mS)[0], soft | mS, null, R=R or AUDIT["R"], rng=np.random.default_rng(AUDIT["seed"]))
            block[("AT_noStephenson", null)] = site_summary(r)
        for null, rr in (("nil_block", None), ("nil_block_ring", nring)):
            p, info = AU.block_test(A, mS, pcap, rr); block[("AT_noStephenson", null)] = dict(**p, **info)
        Nraw = N.copy()
        for c in ("poor", "for_", "net_m", "resid"):
            if c + "_raw" in Nraw: Nraw[c] = Nraw[c + "_raw"]
        Nraw["q5"] = Nraw.p_erp >= Nraw.p_erp.quantile(0.8)
        Araw = AU.Auditor(Nraw, site_a, W)
        for null in ("size", "ring"):
            r, _ = Araw.test(np.where(sets["AT"])[0], soft | sets["AT"], null, R=R or AUDIT["R"], rng=np.random.default_rng(AUDIT["seed"]))
            block[("AT_nofloor", null)] = site_summary(r)
        lg("block nulls", block)
    # alternatives: people's lens and top-N holistic non-designated sites matched in capacity
    alt = {}
    for g in ("AT", "AMB_DEG", "ERP"):
        Kg = S.cap[sets[g]].sum(); o = S[soft].sort_values(["hol", "eu"], ascending=False)
        sel = o.index[: int(np.searchsorted(o.cap.cumsum().values, Kg) + 1)]
        n = np.zeros(len(S)); n[sel] = S.cap[sel]; alt[f"topHol_matched_{g}"] = A.indices(n)
        n = np.zeros(len(S)); n[sets[g]] = S.cap[sets[g]]; alt[f"{g}_as_designated"] = A.indices(n)
    for p in P:
        n = np.zeros(len(S)); n[M["idx"]] = p["built"]; p["audit"] = A.indices(n)
        p["sites_idx"] = M["idx"][p["y"]]
        p["eval"] = {}
        for l, Ml in models.items():
            r, _, _ = PO.solve(Ml, fixed_y=p["y"], time_limit=30)
            p["eval"][l] = dict(served_mean=r.get("served_mean"), served_cvar=r.get("served_cvar"))
    out.update(C=C, counts=counts, psite=psite, S=S, X=X, raw=raw, cspec=cspec, Bu=Bu, keep=keep, Dl=Dl, N=N, layer=layer,
               pp_ok=pp_ok, P=P, res=res, match=match, labels=labels, Q=Q, alt=alt, ids=ids, hx=hx, M_idx=M["idx"],
               pairs=pairs, geoms=geoms, block=block)
    return out


def site_summary(r):
    """One-sided harm p and observed value per BH index from an Auditor.test result."""
    d = {}
    for k in AUDIT["bh_indices"]:
        if k in r: d[k] = AU.harm_p(r, k); d["obs_" + k] = r[k]["obs"]; d["mean_" + k] = r[k]["mean"]
    return d


def matched_pools(S, Dnil, pairs, kap, P, lg):
    """review2 Issue 5: L_pgt vs random non-designated pools with the designated MILP pool's count per area decile
    (and per centre ring), capacity within +-5 %, no cheapest-per-NIL prescreen, same MILP and budget."""
    pgt = next(p for p in P if p["id"] == "L_pgt"); ppl = next(p for p in P if p["id"] == "L_people")
    elig = (S.cap >= SUP["m_min"]).values
    des = elig & (S.origin != "SOFT").values; non = elig & (S.origin == "SOFT").values
    dec = np.searchsorted(np.quantile(S.area_m2.values[elig], np.linspace(0, 1, 11)[1:-1]), S.area_m2.values)
    target = S.cap.values[des].sum(); rng = np.random.default_rng(21)
    out = dict(pgt=pgt["r"]["served_mean"], people=ppl["r"]["served_mean"])
    for kind in ("size", "ring"):
        st = dec * 10 + (S.ring.values if kind == "ring" else 0)
        need = pd.Series(st[des]).value_counts(); vals = []
        for d in range(PORT["matched_draws"]):
            best, bd = None, np.inf
            for _ in range(200):
                sel = np.concatenate([rng.choice(np.where(non & (st == g))[0], min(k, int((non & (st == g)).sum())), replace=False)
                                      for g, k in need.items()])
                dd = abs(S.cap.values[sel].sum() / target - 1)
                if dd < bd: best, bd = sel, dd
                if dd <= 0.05: break
            m = np.zeros(len(S), bool); m[best] = True
            Mm = PO.prepare(S, Dnil, pairs, kap, prescreen=False, subset=m)
            r, _, _ = PO.solve(Mm, time_limit=PORT["matched_time_limit"], gap=PORT["gap_choice"])
            vals.append(dict(served=r.get("served_mean"), cap=float(S.cap.values[best].sum()), status=r.get("status"), gap=r.get("gap")))
        v = np.array([x["served"] for x in vals], float)
        out[kind] = dict(draws=vals, mean=float(v.mean()), lo=float(v.min()), hi=float(v.max()),
                         gain_vs_pgt=float(v.mean() / out["pgt"] - 1), pgt_beats=int((v < out["pgt"]).sum()))
        lg("matched pools", kind, round(v.mean()), "gain", round(out[kind]["gain_vs_pgt"], 3))
    out["raw_gain"] = float(out["people"] / out["pgt"] - 1)
    out["pgt_pool"] = dict(sites=int(des.sum()), cap=float(target))
    return out


def parcel_score(o):
    s = o["S"]; v = (s.hol + 1e-6 * s.eu).values
    return np.where(o["psite"] >= 0, v[np.maximum(o["psite"], 0)], np.nan)


def p1_parcels(o):
    ref = o["C"].ref.values; ps = o["psite"]
    return set(ref[np.isin(ps, o["P"][0]["sites_idx"])])


def sensitivity(base, C_geo):
    rows = []
    b_score = pd.Series(parcel_score(base), index=base["C"].ref.values); b_p1 = p1_parcels(base)
    for k, vals in SENS.items():
        for v in vals:
            t = time.time()
            with override(**{k: v}, n_scen=8, time_limit=20):
                o = pipeline(full=False, R=SENS_R, verbose=False, C_geo=C_geo)
            sc = pd.Series(parcel_score(o), index=o["C"].ref.values)
            j = pd.concat([b_score, sc], axis=1, join="inner").dropna()
            tau = stats.kendalltau(j.iloc[:, 0], j.iloc[:, 1])[0]
            p1 = p1_parcels(o)
            row = dict(param=k, value=v, kendall_tau_hol=round(float(tau), 3),
                       p1_overlap=round(len(p1 & b_p1) / max(len(b_p1), 1), 3), sites=len(o["S"]), sec=round(time.time() - t))
            for g in ("AT", "AMB_DEG", "ERP"):
                row[f"label_{g}"] = o["labels"][g]; row[f"flip_{g}"] = o["labels"][g] != base["labels"][g]
            Qs = o["Q"]
            for n in ("size", "ring"):
                row[f"q_AT_dDI_{n}"] = round(float(Qs[(Qs.set == "AT") & (Qs.null == n) & (Qs.idx == "dDI")].q_bh.iloc[0]), 4)
            rows.append(row); log("sens", row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- outputs
def write_tables(o, runtime=None, sens=None):
    S, P = o["S"], o["P"]
    cols = ["origin", "at_name", "nil_id", "n_parcels", "area_m2", "cap", "cost_per_dw", "x", "y", "dem_mean", "dem_p05",
            "b1", "top10_uniform", "hol", "min_arch", "gic_arch", "depth", "opp", "rent_g", "ring", "pgt_rig"]
    T = S[cols].copy(); T.insert(0, "site", [f"S{i:04d}" for i in range(len(S))])
    T = pd.concat([T, o["raw"].add_prefix("raw_"), o["X"].add_prefix("x_")], axis=1)
    T.round(5).to_csv(os.path.join(RES, "sites.csv"), index=False)
    D = o["Dl"]; agg = D[D.scen >= 0].groupby("nil_id")[[c for c in D if c.startswith("D_")]].agg(["mean", lambda v: v.quantile(.05)])
    agg.columns = [f"{a}_{'mean' if b == 'mean' else 'p05'}" for a, b in agg.columns]
    o["N"].merge(agg.reset_index(), on="nil_id").round(4).to_csv(os.path.join(RES, "demand_layers.csv"), index=False)
    rows = []
    for g, d in o["res"].items():
        for null, r in d.items():
            for k, v in r.items(): rows.append(dict(set=g, null=null, index=k, match_rate=o["match"][(g, null)], **v))
    pd.DataFrame(rows).round(6).to_csv(os.path.join(RES, "audit_indices.csv"), index=False)
    o["Q"].round(6).to_csv(os.path.join(RES, "audit_bh.csv"), index=False)
    if o.get("block"): pd.DataFrame([dict(set=g, null=n, **v) for (g, n), v in o["block"].items()]).round(5).to_csv(os.path.join(RES, "audit_robustness.csv"), index=False)
    pd.DataFrame(o["alt"]).T.round(5).to_csv(os.path.join(RES, "audit_alternatives.csv"))
    pr = []
    for p in P:
        r = {k: v for k, v in p["r"].items() if k not in ("served_nil",)}
        des = (S.origin.values[p["sites_idx"]] != "SOFT").mean() if len(p["sites_idx"]) else np.nan
        pr.append(dict(id=p["id"], lens=p["lens"], **r, share_sites_designated=des,
                       **{f"eval_{l}_{m}": v[m] for l, v in p["eval"].items() for m in v},
                       **{f"audit_{k}": v for k, v in p["audit"].items()}, smaa_b1=p.get("smaa_b1"), smaa_top3=p.get("smaa_top3")))
    pd.DataFrame(pr).to_csv(os.path.join(RES, "portfolios.csv"), index=False)
    if sens is not None: sens.to_csv(os.path.join(RES, "sensitivity.csv"), index=False)


def portfolio_smaa(o):
    """Portfolio-level SMAA with FIXED ranges (review2: min-max stretched CVaR noise). CVaR20 (saturated ~654 for all
    non-PGT portfolios), dDI (same ecological signal as dep_poor) and served per EUR (redundant with served at equal
    budget) are dropped. Ranges: served share of mean demand [0,1]; 1-Gini [0,1]; opportunity and rent-burden site
    scores [0,1]; dep_poor mapped from [+5, -5] pp to [0, 1]."""
    P = [p for p in o["P"] if p["r"].get("feasible", True) and len(p["sites_idx"])]
    X = o["X"]; rows = []
    for p in P:
        w = p["built"][p["y"]]; xi = X.values[p["sites_idx"]]
        mx = (xi * w[:, None]).sum(0) / max(w.sum(), 1e-9)
        r = p["r"]
        rows.append([r["served_mean"] / max(r["demand_mean"], 1e-9), 1 - r["gini_cov"], mx[[0, 1, 2, 3, 4]].mean(), mx[6],
                     np.clip((5 - p["audit"]["dep_poor"]) / 10, 0, 1)])
    b = SM.portfolio_smaa(np.clip(np.array(rows), 0, 1), k=3)
    for p, bb in zip(P, b): p["smaa_b1"], p["smaa_top3"] = float(bb[0]), float(bb.sum())
    return ["served_share", "1-gini", "opportunity", "rent_burden", "low_dep_poor"]


if __name__ == "__main__":
    t0 = time.time()
    base = pipeline(full=True)
    pcrit = portfolio_smaa(base)
    log("portfolios", [(p["id"], p["r"].get("sites"), round(p["r"].get("served_mean") or 0)) for p in base["P"]])
    pickle.dump({k: v for k, v in base.items() if k not in ("geoms",)}, open(os.path.join(OUT, "base.pkl"), "wb"))
    write_tables(base)
    import export; export.write(base, pcrit)
    sens = None
    if "--no-sens" not in sys.argv:
        sens = sensitivity(base, ((base["C"], base["counts"]), base["geoms"]))
    write_tables(base, sens=sens)
    pickle.dump(sens, open(os.path.join(OUT, "sens.pkl"), "wb"))
    rt = round((time.time() - t0) / 60, 1)
    import report; report.write(base, sens, rt)
    export.write(base, pcrit, sens=sens, runtime_min=rt)
    log("done", rt, "min")
