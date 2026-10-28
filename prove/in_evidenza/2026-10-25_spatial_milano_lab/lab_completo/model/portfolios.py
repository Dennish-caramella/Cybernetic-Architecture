"""Step 6: the citizens' choice set -- K diverse portfolios (integer no-good cuts) plus policy lenses (review1 §5.6).
Base model = A's robust MILP ((1-beta) mean + beta CVaR_alpha of served demand, budget, min size, NIL caps kappa,
optional demand-weighted Gini), on SITES instead of parcels, with hex-population-weighted service weights.
A's LP builder (HiGHS) and gini_w are reused unchanged."""
import numpy as np, pandas as pd
from config import *

A_PF = load_prop("A_econ_or", "portfolio")


def prepare(S, Dnil, pairs, kap, prescreen=True, k_per_nil=None, subset=None):
    """S sites (with cap, fixed_eur, var_eur, nil_id, origin); Dnil DataFrame nil_id x scen; pairs (s, i, w) over all
    sites (s = row of S); kap per NIL (aligned with Dnil.index). Returns model dict on the MILP pool."""
    k = k_per_nil or PORT["k_per_nil"]
    pool = S[(S.cap >= SUP["m_min"]) & (True if subset is None else subset)].copy()
    if prescreen:
        pool["des"] = pool.origin != "SOFT"
        pool = pool.sort_values("cost_per_dw")
        pool = pd.concat([pool.groupby(["nil_id", "des"]).head(k), pool[pool.origin.isin(["ERP", "AT", "AMB_DEG"])]])
        pool = pool[~pool.index.duplicated()]
    idx = np.sort(pool.index.values)
    pos = -np.ones(len(S), int); pos[idx] = np.arange(len(idx))
    s, i, w = pairs; m = pos[s] >= 0
    ids = list(Dnil.index)
    host = pd.Series({n: j for j, n in enumerate(ids)}).reindex(S.nil_id.values[idx]).fillna(-1).astype(int).values
    return dict(idx=idx, cap=S.cap.values[idx].astype(float), fixed=S.fixed_eur.values[idx], var=S.var_eur.values[idx],
                origin=S.origin.values[idx], ps=pos[s[m]], pi=i[m], pw=w[m], D=Dnil.values, ids=ids, host=host, kap=np.asarray(kap, float))


def solve(M, budget=None, beta=None, alpha=None, gini_max=None, allowed=None, cuts=(), fixed_y=None, time_limit=None,
          gap=None, objective="service", score=None):
    """objective='service': robust served demand. objective='score': max sum_s y_s cap_s score_s (knapsack lens),
    service evaluated afterwards with y fixed. Returns (summary dict, y bool array over M['idx'], built dwellings)."""
    budget = budget or PORT["budget"]; beta = PORT["beta"] if beta is None else beta; alpha = alpha or PORT["alpha"]
    time_limit = time_limit or PORT["time_limit"]; gap = gap or PORT["gap"]
    cap, fixed, var, ps, pi, pw, D = M["cap"], M["fixed"], M["var"], M["ps"], M["pi"], M["pw"], M["D"]
    S_, I, W = len(cap), D.shape[0], D.shape[1]
    lo_y = np.zeros(S_); hi_y = np.ones(S_)
    if allowed is not None: hi_y[~allowed] = 0
    if fixed_y is not None: lo_y = fixed_y.astype(float); hi_y = fixed_y.astype(float)
    if objective == "score":
        lp = A_PF.LP(); y = np.arange(S_)
        lp.lo, lp.hi, lp.c, lp.int_ = list(lo_y), list(hi_y), list(cap * score), [True] * S_
        lp.row(y, fixed + var * cap, hi=budget)
        for h in range(I):
            on = M["host"] == h
            if on.any(): lp.row(y[on], cap[on], hi=M["kap"][h])
        for C in cuts: lp.row(y[C], np.ones(len(C)), hi=np.floor((1 - PORT["delta"]) * len(C)))
        sol, info = lp.solve(time_limit=time_limit, gap=gap)
        ys = sol[:S_] > 0.5
        r, ys2, built = solve(M, budget, beta, alpha, None, fixed_y=ys, time_limit=time_limit, gap=gap)
        r.update(score_obj=info["obj"], score_gap=info["gap"], status_score=info["status"])
        return r, ys2, built
    lp = A_PF.LP()
    y = lp.var(S_, 0, 1, integer=True)
    lp.lo[:S_] = list(lo_y); lp.hi[:S_] = list(hi_y)
    x = lp.var(len(ps), 0, np.inf)
    u = lp.var(I * W, 0, D.T.ravel(), c=(1 - beta) / W)
    eta = lp.var(1, -np.inf, np.inf, c=beta)
    xi = lp.var(W, 0, np.inf, c=-beta / (alpha * W))
    order = np.argsort(ps, kind="stable"); bounds = np.searchsorted(ps[order], np.arange(S_ + 1))
    for s in range(S_):
        xs = x[order[bounds[s]:bounds[s + 1]]]
        lp.row(np.r_[xs, y[s]], np.r_[np.ones(len(xs)), -cap[s]], hi=0)
        if fixed_y is None: lp.row(np.r_[xs, y[s]], np.r_[np.ones(len(xs)), -SUP["m_min"]], lo=0)   # min size (not when evaluating a fixed set)
    lp.row(np.r_[y, x], np.r_[fixed, var[ps]], hi=budget)
    for i in range(I):
        on = pi == i
        lp.row(x[on], np.ones(on.sum()), hi=max(D[i].max(), 0))
        for w_ in range(W):
            lp.row(np.r_[u[w_ * I + i], x[on]], np.r_[1.0, -pw[on]], hi=0)
    hp = M["host"][ps]
    for h in range(I):
        on = hp == h
        if on.any(): lp.row(x[on], np.ones(on.sum()), hi=M["kap"][h])
    for w_ in range(W):
        lp.row(np.r_[xi[w_], eta, u[w_ * I:(w_ + 1) * I]], np.r_[1.0, -1.0, np.ones(I)], lo=0)
    for C in cuts: lp.row(y[C], np.ones(len(C)), hi=np.floor((1 - PORT["delta"]) * len(C)))
    Dbar = D.mean(1)
    if gini_max is not None:
        act = np.where(Dbar >= 1)[0]; Dt = Dbar[act].sum()
        pairs = [(a, b) for k, a in enumerate(act) for b in act[k + 1:]]
        dvar = lp.var(len(pairs), 0, np.inf)
        ub = lambda i: (u[np.arange(W) * I + i], np.full(W, 1.0 / W))
        for k, (a, b) in enumerate(pairs):
            ca, va = ub(a); cb, vb = ub(b)
            lp.row(np.r_[dvar[k], ca, cb], np.r_[1.0, -Dbar[b] * va, Dbar[a] * vb], lo=0)
            lp.row(np.r_[dvar[k], ca, cb], np.r_[1.0, Dbar[b] * va, -Dbar[a] * vb], lo=0)
        allu = np.concatenate([ub(i)[0] for i in act]); allv = np.concatenate([ub(i)[1] for i in act])
        lp.row(np.r_[dvar, allu], np.r_[np.ones(len(pairs)), -gini_max * Dt * allv], hi=0)
    sol, info = lp.solve(time_limit=time_limit, gap=gap)
    if sol.size == 0 or "nfeasible" in info["status"]:
        return dict(info, sites=0, feasible=False), np.zeros(S_, bool), np.zeros(S_)
    ys = sol[y] > 0.5; xv = sol[x]; uv = sol[u].reshape(W, I).T
    built = np.bincount(ps, weights=xv, minlength=S_)
    served = uv.sum(0); Ubar = uv.mean(1)
    cov = np.where(Dbar >= 1, np.minimum(Ubar / np.maximum(Dbar, 1e-9), 1), np.nan); a = ~np.isnan(cov)
    tail = np.sort(served)[: max(1, int(alpha * W))].mean()
    cost = fixed[ys].sum() + (var * built).sum()
    return dict(info, feasible=True, sites=int(ys.sum()), dwellings=float(built.sum()), cost_eur=float(cost),
                served_mean=float(served.mean()), served_cvar=float(tail), demand_mean=float(D.sum(0).mean()),
                gini_cov=float(A_PF.gini_w(cov[a], Dbar[a])) if a.any() else np.nan, nil_served=int((Ubar >= 1).sum()),
                served_nil=Ubar), ys, built


def overlap(a, b):
    a, b = set(np.where(a)[0]), set(np.where(b)[0])
    return len(a & b) / max(len(a), 1)


def diverse_set(M, K=None, **kw):
    """p_1 = optimum; p_k adds the no-good cut of each earlier portfolio (shares <= 70 % of its sites). Stops if served
    falls below stop_frac x p_1."""
    K = K or PORT["K"]; out, cuts = [], []
    for k in range(K):
        r, ys, built = solve(M, cuts=cuts, **kw)
        if not r.get("feasible") or r["sites"] == 0: break
        if out and r["served_mean"] < PORT["stop_frac"] * out[0][0]["served_mean"]: break
        r["max_overlap_prev"] = max([overlap(o[1], ys) for o in out], default=0.0)   # |prev ∩ new| / |prev|
        out.append((r, ys, built)); cuts.append(np.where(ys)[0])
    return out
