"""Steps 3-4 - candidate supply and robust multi-objective MILP (HiGHS) for social-housing portfolios.

Inputs: lab/data/parcels.csv.gz, lab/data/nil.csv, results/demand_scenarios.csv (from demand.py), mi/out/core.json.
See model.md section 4 for the formulation. Run via run_all.py.
"""
import json, os, sys, time
import numpy as np, pandas as pd, shapely, shapely.geometry, highspy
from scipy import sparse
from shapely.geometry import Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
T0 = time.time()
log = lambda *a: print(f"[{time.time() - T0:6.1f}s]", *a, file=sys.stderr, flush=True)

SUP = dict(
    far=1.0,          # A: new gross floor area / parcel area. PGT Milano base IT 0.35 + transfers/ERS up to ~1 [unverified]
    yield_=0.70,      # S: Mill Valley realistic yield on theoretical capacity (report sec.2)
    gfa_dw=80.0,      # A: gross m2 per dwelling (avg ~65 m2 net, Piano Casa 50-70 m2 units)
    a_min=1500.0,     # A: minimum parcel area screened
    m_min=20,         # A: minimum project size (dwellings) if a site is opened
    m_max=400,        # A: maximum dwellings per site (scale / mix)
    land_inc=0.20,    # A: land incidence on OMI sale value of buildable GFA [unverified, typical 15-25 %]
    c_build=2000.0,   # S [unverified]: construction EUR/m2 GFA (report: 1,800-2,500)
    c_demo=25.0,      # A: demolition EUR/m3 of existing volume
    lam_km=1.5,       # A: distance-decay length (km) of service to demand outside the host NIL
    d_max=3.0,        # A: no service beyond 3 km from a NIL boundary
    kappa=0.03,       # A: max new social dwellings in a NIL as share of its households
    kappa_erp=0.015,  # A: tighter cap where PGT srv_erp > 5 % of NIL area (existing public-housing concentration)
    k_per_nil=12,     # pre-screen: cheapest-per-dwelling sites kept per NIL (+ all public srv_erp sites)
)


def candidates(sp):
    P = pd.read_csv(os.path.join(ROOT, "lab", "data", "parcels.csv.gz"), dtype={"ref": str})
    L = P[(P.kind == "land") & (~P.outside_city) & P.nil_price.notna()].copy()
    excl = (L[["pgt_srv_verde", "pgt_agr", "pgt_pae", "pgt_srv_ist", "dusaf_wat", "dusaf_infra", "dusaf_green", "dusaf_agr", "dusaf_wood"]] >= 0.5).any(axis=1)
    # rig/dism are zone-wide policy layers (dism ~ "ex AR_RIG", r=0.998; rig = 'rigenerazione diffusa', 36.8 km2):
    # NOT a site signal (Researcher C). Only tras (minus PCU parks) and srv_erp count as planning signals.
    pcu = pcu_mask(L.x.values, L.y.values)
    plan = ((L.pgt_tras >= 0.5) & ~pcu) | (L.pgt_srv_erp >= 0.5)
    occupied_res = (L.n_vol > 0) & (L.use_res_share >= 0.5)          # avoid displacing existing residents
    keep = (L.area_m2 >= sp["a_min"]) & ~excl & ~occupied_res & ~pcu & (L.soft_site | (plan & (L.far_ratio < 1.0)))
    if sp.get("pu_top"):                                              # sensitivity: C's PU-learning rank (top share)
        pu = pd.read_csv(os.path.join(ROOT, "lab", "proposals", "C_ml_spatial", "results", "pu_scores.csv.gz"), dtype={"ref": str}, usecols=["ref", "p_y_EN"])
        top = set(pu.ref[pu.p_y_EN >= pu.p_y_EN.quantile(1 - sp["pu_top"])])
        keep &= L.ref.isin(top)
    L = L[keep].copy()
    L["public"] = L.pgt_srv_erp >= 0.5                                 # A: srv_erp land treated as municipal (1 EUR/m2)
    L["cap"] = np.minimum(np.floor(sp["yield_"] * sp["far"] * L.area_m2 / sp["gfa_dw"]), sp["m_max"])
    L = L[L.cap >= sp["m_min"]].copy()
    gfa = L.cap * sp["gfa_dw"]
    L["fixed_eur"] = np.where(L.public, L.area_m2 * 1.0, sp["land_inc"] * L.nil_price * gfa) + sp["c_demo"] * L.volume_m3
    L["var_eur"] = sp["c_build"] * sp["gfa_dw"]
    L["cost_per_dw"] = L.fixed_eur / L.cap + L.var_eur
    L = L.sort_values("cost_per_dw")
    L = pd.concat([L.groupby("nil_id").head(sp["k_per_nil"]), L[L.public]]).drop_duplicates("ref")
    return L.reset_index(drop=True)


def pcu_mask(x, y):
    """Parcels inside the 6 'Parchi della Campagna Urbana' (PCU) transformation ambits = parks/farmland, not supply."""
    g = json.load(open(os.path.join(ROOT, "mi", "raw", "pgt_ambiti_trasformazione.geojson"), encoding="utf-8"))
    LON0, LAT0 = 9.19, 45.465; KX, KY = 111.32 * np.cos(np.radians(LAT0)), 110.57
    to_km = lambda a: np.column_stack(((a[:, 0] - LON0) * KX, -(a[:, 1] - LAT0) * KY))
    polys = [shapely.transform(shapely.geometry.shape(f["geometry"]), to_km).buffer(0)
             for f in g["features"] if "PCU" in (f["properties"].get("NOME_AMB") or "")]
    return shapely.contains_xy(shapely.union_all(polys), x, y)


def nil_geoms():
    core = json.load(open(os.path.join(ROOT, "mi", "out", "core.json"), encoding="utf-8")); u = core["meta"]["unit_km"]
    def poly(a):
        g = Polygon(np.cumsum(np.asarray(a, dtype=np.int64).reshape(-1, 2), axis=0) * u)
        return g if g.is_valid else g.buffer(0)
    return {n["id"]: shapely.union_all([poly(r) for r in n["rings"]]) for n in core["nil"]}


class LP:
    """Tiny column/row builder -> HighsLp (CSC)."""
    def __init__(s): s.lo, s.hi, s.c, s.int_, s.rows = [], [], [], [], []
    def var(s, n, lo=0.0, hi=np.inf, c=0.0, integer=False):
        i0 = len(s.lo); s.lo += [lo] * n; s.hi += list(np.broadcast_to(hi, n)); s.c += list(np.broadcast_to(c, n)); s.int_ += [integer] * n
        return np.arange(i0, i0 + n)
    def row(s, cols, vals, lo=-np.inf, hi=np.inf): s.rows.append((np.asarray(cols), np.asarray(vals, float), lo, hi))
    def solve(s, time_limit=120, gap=0.01, maximize=True):
        nr, nc = len(s.rows), len(s.lo)
        r = np.concatenate([np.full(len(c), k) for k, (c, _, _, _) in enumerate(s.rows)])
        c = np.concatenate([c for c, _, _, _ in s.rows]); v = np.concatenate([v for _, v, _, _ in s.rows])
        A = sparse.csc_matrix((v, (r, c)), shape=(nr, nc))
        lp = highspy.HighsLp(); lp.num_col_, lp.num_row_ = nc, nr
        lp.col_cost_, lp.col_lower_, lp.col_upper_ = np.array(s.c), np.array(s.lo), np.array(s.hi)
        lp.row_lower_ = np.array([x[2] for x in s.rows]); lp.row_upper_ = np.array([x[3] for x in s.rows])
        lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
        lp.a_matrix_.start_, lp.a_matrix_.index_, lp.a_matrix_.value_ = A.indptr, A.indices, A.data
        lp.integrality_ = [highspy.HighsVarType.kInteger if b else highspy.HighsVarType.kContinuous for b in s.int_]
        lp.sense_ = highspy.ObjSense.kMaximize if maximize else highspy.ObjSense.kMinimize
        h = highspy.Highs(); h.setOptionValue("output_flag", False)
        h.setOptionValue("time_limit", float(time_limit)); h.setOptionValue("mip_rel_gap", gap)
        h.passModel(lp); t = time.time(); h.run()
        info = h.getInfo()
        return np.array(h.getSolution().col_value), dict(status=h.modelStatusToString(h.getModelStatus()), obj=info.objective_function_value,
                                                        gap=info.mip_gap, sec=round(time.time() - t, 1), n_var=nc, n_row=nr)


def prepare(sp, Dscen):
    """Candidates, service pairs (site s, demand NIL i, weight w_si) and demand matrix D[i, scen]."""
    G = nil_geoms()
    Dm = Dscen.pivot(index="nil_id", columns="scen", values="D").fillna(0.0)
    L = candidates(sp); L = L[L.nil_id.isin(Dm.index)].reset_index(drop=True)
    nil = pd.read_csv(os.path.join(ROOT, "lab", "data", "nil.csv"))
    hh = pd.read_csv(os.path.join(HERE, "results", "cache", "nil_hh.csv")).set_index("nil_id").hh25
    ids = list(Dm.index); D = Dm.values
    pts = shapely.points(L.x.values, L.y.values)
    dist = np.column_stack([shapely.distance(pts, G[i]) for i in ids])          # km to NIL polygon, 0 inside
    w = np.exp(-dist / sp["lam_km"]); w[dist > sp["d_max"]] = 0
    ps, pi = np.nonzero(w); pw = w[ps, pi]
    host = L.nil_id.map({n: k for k, n in enumerate(ids)}).values
    erp_share = nil.set_index("nil_id").pgt_srv_erp.reindex(ids).fillna(0).values
    kap = np.where(erp_share > 5, sp["kappa_erp"], sp["kappa"]) * hh.reindex(ids).fillna(0).values
    return dict(L=L, ids=ids, D=D, ps=ps, pi=pi, pw=pw, host=host, kap=kap)


def solve_portfolio(M, sp, budget, beta=0.5, alpha=0.2, gini_max=None, time_limit=120):
    """max (1-beta) E[served] + beta CVaR_alpha[served]  s.t. budget, capacity, min size, NIL caps, Gini <= gini_max."""
    L, D, ps, pi, pw = M["L"], M["D"], M["ps"], M["pi"], M["pw"]
    S, I, W = len(L), D.shape[0], D.shape[1]
    lp = LP()
    y = lp.var(S, 0, 1, integer=True)
    x = lp.var(len(ps), 0, np.inf)
    u = lp.var(I * W, 0, D.T.ravel(), c=(1 - beta) / W)                      # u[w*I+i] <= D[i,w]
    eta = lp.var(1, -np.inf, np.inf, c=beta)
    xi = lp.var(W, 0, np.inf, c=-beta / (alpha * W))
    cap, fixed, var = L.cap.values, L.fixed_eur.values, L.var_eur.values
    xs = [x[ps == s] for s in range(S)]
    for s in range(S):
        lp.row(np.r_[xs[s], y[s]], np.r_[np.ones(len(xs[s])), -cap[s]], hi=0)          # capacity
        lp.row(np.r_[xs[s], y[s]], np.r_[np.ones(len(xs[s])), -sp["m_min"]], lo=0)     # min project size
    lp.row(np.r_[y, x], np.r_[fixed, var[ps]], hi=budget)                               # budget
    for i in range(I):
        on = pi == i
        lp.row(x[on], np.ones(on.sum()), hi=D[i].max())                                 # no allocation beyond worst-case demand
        for w_ in range(W):
            lp.row(np.r_[u[w_ * I + i], x[on]], np.r_[1.0, -pw[on]], hi=0)              # served <= accessible supply
    for h in range(I):                                                                  # social-mix cap by host NIL
        on = M["host"][ps] == h
        if on.any(): lp.row(x[on], np.ones(on.sum()), hi=M["kap"][h])
    for w_ in range(W):                                                                 # CVaR: xi_w >= eta - U_w
        lp.row(np.r_[xi[w_], eta, u[w_ * I:(w_ + 1) * I]], np.r_[1.0, -1.0, np.ones(I)], lo=0)
    Dbar = D.mean(1)
    if gini_max is not None:                                                            # demand-weighted Gini of coverage
        act = np.where(Dbar >= 1)[0]; Dt = Dbar[act].sum()
        # c_i = ubar_i / Dbar_i ; sum_{i<j} Di Dj |ci-cj| <= g * Dt * sum_i ubar_i   (Gini = LHS / (Dt * U))
        pairs = [(a, b) for k, a in enumerate(act) for b in act[k + 1:]]
        dvar = lp.var(len(pairs), 0, np.inf)
        ub = lambda i: (u[np.arange(W) * I + i], np.full(W, 1.0 / W))
        for k, (a, b) in enumerate(pairs):
            ca, va = ub(a); cb, vb = ub(b)
            # Da*Db*(ua/Da - ub/Db) = Db*ua - Da*ub
            lp.row(np.r_[dvar[k], ca, cb], np.r_[1.0, -Dbar[b] * va, Dbar[a] * vb], lo=0)
            lp.row(np.r_[dvar[k], ca, cb], np.r_[1.0, Dbar[b] * va, -Dbar[a] * vb], lo=0)
        allu = np.concatenate([ub(i)[0] for i in act]); allv = np.concatenate([ub(i)[1] for i in act])
        lp.row(np.r_[dvar, allu], np.r_[np.ones(len(pairs)), -gini_max * Dt * allv], hi=0)
    sol, info = lp.solve(time_limit=time_limit)
    ys = sol[y] > 0.5; xv = sol[x]; uv = sol[u].reshape(W, I).T
    built = np.bincount(ps, weights=xv, minlength=S)
    served = uv.sum(0)
    Ubar = uv.mean(1); cov = np.where(Dbar >= 1, np.minimum(Ubar / np.maximum(Dbar, 1e-9), 1), np.nan)
    a = ~np.isnan(cov); g = gini_w(cov[a], Dbar[a])
    tail = np.sort(served)[: max(1, int(alpha * W))].mean()
    cost = fixed[ys].sum() + (var * built).sum()
    res = dict(budget=budget, beta=beta, gini_max=gini_max, **info, sites=int(ys.sum()), dwellings=float(built.sum()),
               cost_eur=float(cost), served_mean=float(served.mean()), served_cvar=float(tail),
               served_p05=float(np.quantile(served, .05)), demand_mean=float(D.sum(0).mean()), gini_cov=float(g),
               nil_served_any=int((Ubar >= 1).sum()))
    site = M["L"].loc[ys, ["ref", "nil_id", "nil_name", "x", "y", "area_m2", "cap", "public", "use_dom", "metro_km", "fixed_eur", "cost_per_dw"]].copy()
    site["dwellings"] = built[ys]
    nilres = pd.DataFrame(dict(nil_id=M["ids"], D_mean=Dbar, served_mean=Ubar, coverage=cov,
                               built_in_nil=np.bincount(M["host"], weights=built, minlength=I),
                               access=np.bincount(pi, weights=pw * xv, minlength=I)))
    return res, site, nilres


def gini_w(v, w):
    """Weighted Gini = sum_ij wi wj |vi - vj| / (2 W^2 mean)."""
    W = w.sum(); m = np.sum(w * v) / W
    if m <= 0: return np.nan
    return float(np.sum(w[:, None] * w[None, :] * np.abs(v[:, None] - v[None, :])) / (2 * W * W * m))


assert abs(gini_w(np.array([1.0, 1.0]), np.array([1.0, 1.0]))) < 1e-12 and abs(gini_w(np.array([0.0, 1.0]), np.array([1.0, 1.0])) - 0.5) < 1e-12
