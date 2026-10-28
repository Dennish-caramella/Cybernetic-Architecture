"""Step 4: demand layers per NIL x scenario (A's simulator, unchanged), hex downscaling, site reach, rent erosion.

Layers (coordinator 2026-10-27):
  D_tau        A's TARGET band, tau = 0.30 (ratio OR residual-750 rule, A base)
  D_res_decent residual-income test, non-housing basket = 1.5 x ISTAT (portfolio layer when the PP layer is present)
  D_res_istat  residual test with the pure ISTAT basket -- near-empty, reported only
  D_city       city-wide search variant (rent = cheapest NIL within 5 km), scalar
The PP layer counts as present when A's purchasing_power_nil.csv exists; otherwise only D_tau is used and
pp_layer = 'missing' (re-running run.py picks it up)."""
import json, os
import numpy as np, pandas as pd, shapely
from scipy.spatial import cKDTree
from config import *
A_DEM = load_prop("A_econ_or", "demand")
import portfolio as A_PF


def pp_available():
    return os.path.exists(DEM["pp_file"])


def simulate_layers(par_over=None, n_scen=None, nh=None, seed=None, layers=None, H_override=None):
    """Returns long DataFrame nil_id x scen with hh, p_erp, D_<layer>. scen = -1 is A's unperturbed base draw."""
    n_scen = DEM["n_scen"] if n_scen is None else n_scen; nh = nh or DEM["nh"]; seed = DEM["seed"] if seed is None else seed
    par0 = {**A_DEM.BASE, "tau": DEM["tau"], **(par_over or {})}
    bm = par0.pop("basket_mult", DEM["basket_mult"])
    L = {"D_tau": dict(test="both", basket1=A_DEM.BASE["basket1"] * bm),
         "D_res_decent": dict(test="residual", basket1=DEM["decent_mult"] * DEM["nh_basket1"] * bm),
         "D_res_istat": dict(test="residual", basket1=DEM["nh_basket1"] * bm)}
    layers = layers or (list(L) if pp_available() else ["D_tau"])
    C, W, H = A_DEM.load_inputs()
    if H_override is not None: H = H_override(H)
    FIT, _ = A_DEM.fit_all(C)
    TCAL = A_DEM.tax_calibration(C, FIT, np.random.default_rng(seed))
    rows = []
    for w in range(-1, n_scen):
        r0 = np.random.default_rng(seed * 1000 + w + 1)
        pert = dict(earn_k=r0.uniform(0.8, 1.2), rho=r0.uniform(-0.2, 0.2), bk=r0.uniform(0.85, 1.15), rn=r0.uniform(0.85, 1.15)) if w >= 0 else None
        out = None
        for name in layers:
            p = {**par0, **L[name]}
            if pert:
                p.update(earn_k=p["earn_k"] * pert["earn_k"], rho=float(np.clip(p["rho"] + pert["rho"], 0, 0.9)),
                         basket1=p["basket1"] * pert["bk"], renter=p["renter"] * pert["rn"])
            d, _ = A_DEM.simulate(C, W, H, FIT, TCAL, p, np.random.default_rng(seed * 7919 + w + 2), nh=nh, perturb=w >= 0)
            if out is None: out = d[["nil_id", "hh", "p_erp"]].copy(); out["renter"] = p["renter"]
            out[name] = d.D.values
        out["scen"] = w; rows.append(out)
    return pd.concat(rows, ignore_index=True)


def city_search_variant(nh=None):
    """F-A1: D_tau with each NIL's rent replaced by the cheapest NIL rent within 5 km (~30 min transit, [A]),
    and with the city-median rent (income-only variation). Base draw only."""
    def cheapest(H):
        H = H.copy(); xy = H[["cx", "cy"]].values; t = cKDTree(xy)
        H["rent"] = [H.rent.values[n].min() for n in t.query_ball_point(xy, 5.0)]; return H
    def median(H):
        H = H.copy(); H["rent"] = float(np.average(H.rent, weights=H.hh25)); return H
    a = simulate_layers(n_scen=0, nh=nh, layers=["D_tau"], H_override=cheapest)
    b = simulate_layers(n_scen=0, nh=nh, layers=["D_tau"], H_override=median)
    return a[["nil_id", "D_tau"]].rename(columns={"D_tau": "D_city"}).merge(b[["nil_id", "D_tau"]].rename(columns={"D_tau": "D_medrent"}), on="nil_id")


# ---------------------------------------------------------------- spatial
def hex_table():
    core = json.load(open(os.path.join(MI, "out", "core.json"), encoding="utf-8"))
    Hc = np.array(core["hex"]["cells"], float)
    G = A_PF.nil_geoms(); ids = list(G)
    nid = np.full(len(Hc), -1)
    for i in ids: nid[shapely.contains_xy(G[i], Hc[:, 0], Hc[:, 1]) & (nid < 0)] = i
    miss = nid < 0
    if miss.any():
        pts = shapely.points(Hc[miss, 0], Hc[miss, 1])
        nid[miss] = [ids[int(np.argmin([G[i].distance(p) for i in ids]))] for p in pts]
    hx = pd.DataFrame(dict(x=Hc[:, 0], y=Hc[:, 1], pop=Hc[:, 2], emp=Hc[:, 3], nil_id=nid))
    hx["pop_share"] = hx["pop"] / hx.groupby("nil_id")["pop"].transform("sum").replace(0, np.nan)
    hx["pop_share"] = hx.pop_share.fillna(0)
    return hx


def site_hex_weights(S, hx, lam=None, dmax=None):
    """Sparse w_{s,h} = exp(-d/lam) 1[d <= dmax] as (s_idx, h_idx, w)."""
    lam = lam or DEM["lam_km"]; dmax = dmax or DEM["d_max"]
    t = cKDTree(hx[["x", "y"]].values)
    nb = t.query_ball_point(S[["x", "y"]].values, dmax)
    si = np.concatenate([np.full(len(n), k) for k, n in enumerate(nb)]).astype(int); hi = np.concatenate(nb).astype(int)
    d = np.hypot(S.x.values[si] - hx.x.values[hi], S.y.values[si] - hx.y.values[hi])
    return si, hi, np.exp(-d / lam)


def site_nil_weights(S, hx, ids, lam=None, dmax=None):
    """Hex-population-weighted site->NIL service weight w_{s,i} = sum_{h in i} pop_share_h w_{s,h} (replaces A's
    distance to the NIL polygon, F-A4)."""
    si, hi, w = site_hex_weights(S, hx, lam, dmax)
    pos = {n: k for k, n in enumerate(ids)}
    ni = np.array([pos.get(n, -1) for n in hx.nil_id.values[hi]])
    ok = ni >= 0
    M = pd.DataFrame(dict(s=si[ok], i=ni[ok], w=w[ok] * hx.pop_share.values[hi[ok]])).groupby(["s", "i"]).w.sum().reset_index()
    M = M[M.w > 1e-3]
    return M.s.values, M.i.values, M.w.values


def dem_reach(S, hx, Dnil, lam=None):
    """Dnil: DataFrame index nil_id, columns scen -> per site mean and p05 of sum_h w_{s,h} D_h."""
    si, hi, w = site_hex_weights(S, hx, lam)
    Dh = Dnil.reindex(hx.nil_id).fillna(0).values * hx.pop_share.values[:, None]   # (H, scen)
    R = np.zeros((len(S), Dh.shape[1])); np.add.at(R, si, w[:, None] * Dh[hi])
    return R.mean(1), np.quantile(R, 0.05, axis=1)


def A_PF_omi():
    import io
    t = open(os.path.join(MI, "raw", "omi_riepilogo.csv"), "rb").read().decode("utf-8-sig", "replace")
    o = pd.read_csv(io.StringIO(t), sep=";", dtype=str)
    o = o[(o.Cod_Tip == "20") & (o.Stato == "NORMALE")]
    for c in ("Loc_min", "Loc_max"): o[c] = pd.to_numeric(o[c].str.replace(",", "."), errors="coerce")
    o["loc"] = (o.Loc_min + o.Loc_max) / 2
    a = o[(o.Anno == "2019") & o.Periodo.str.startswith("2")].groupby("Zona").agg(Fascia=("Fascia", "first"), loc=("loc", "mean"))
    last = o[o.Anno == o.Anno.max()]; last = last[last.Periodo == last.Periodo.max()].groupby("Zona")["loc"].mean()
    j = a.join(last.rename("loc_last"), how="left")
    j["rent_g"] = j.loc_last / j["loc"] - 1
    fas = j.groupby("Fascia").rent_g.median()
    j["rent_g"] = j.rent_g.fillna(j.Fascia.map(fas))
    return j, f"{o.Anno.max()}/{o[o.Anno == o.Anno.max()].Periodo.max()}"


def rent_erosion_at(x, y):
    """Rent growth 2019->latest at points (OMI zone of the point; nearest zone if outside; fascia median if the
    zone has no 2019 match)."""
    core = json.load(open(os.path.join(MI, "out", "core.json"), encoding="utf-8")); u = core["meta"]["unit_km"]
    j, _ = A_PF_omi()
    from common import poly as c_poly
    zg = [(o["z"], shapely.union_all([g for g in (c_poly(r, u) for r in o["rings"]) if g is not None])) for o in core["omi"]]
    pts = shapely.points(np.asarray(x), np.asarray(y)); out = np.full(len(pts), np.nan)
    med = float(j.rent_g.median())
    for z, g in zg:
        m = shapely.contains(g, pts) & np.isnan(out)
        out[m] = j.rent_g.get(z, np.nan) if z in j.index else np.nan
    miss = np.isnan(out)
    for k in np.where(miss)[0]:
        z = min(zg, key=lambda q: q[1].distance(pts[k]))[0]
        out[k] = j.rent_g.get(z, med) if z in j.index else med
    return np.where(np.isnan(out), med, out)


def pp_nil():
    """NIL purchasing-power table from A (review1 §5.3 interface, adapted to A's actual columns)."""
    if not pp_available(): return None
    P = pd.read_csv(DEM["pp_file"])
    return P.rename(columns={"res_basket_med": "resid_p50", "yreal_med": "yreal_p50", "share_neg_residual": "p_neg_resid"})[
        ["nil_id", "resid_p50", "yreal_p50", "p_neg_resid", "rent_to_income_med"]]
