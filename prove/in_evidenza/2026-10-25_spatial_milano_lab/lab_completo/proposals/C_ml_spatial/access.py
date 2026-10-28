"""1. Enhanced 2SFCA (Gaussian E2SFCA, Dai 2010 kernel) accessibility for every land parcel,
compared with simple nearest-distance / cumulative measures; redundancy diagnostic (Spearman + PCA).
Output: results/access_parcels.csv.gz, results/access_summary.json, results/access_corr.csv."""
import numpy as np, pandas as pd, shapely
from scipy.spatial import cKDTree
from scipy.stats import spearmanr
from common import *

G0 = np.exp(-0.5)


def gauss(d, d0):
    """Dai (2010) Gaussian catchment kernel, 1 at d=0, 0 at d>=d0."""
    return np.where(d < d0, (np.exp(-0.5 * (d / d0) ** 2) - G0) / (1 - G0), 0.0)


def e2sfca(dem_xy, dem, sup_xy, sup, pts, d0, chunk=2000):
    """Step 1: R_j = S_j / sum_k G(d_kj) D_k.  Step 2: A_i = sum_j G(d_ij) R_j (chunked dense)."""
    tk = cKDTree(dem_xy); R = np.zeros(len(sup))
    for j, nb in enumerate(tk.query_ball_point(sup_xy, d0)):
        if nb:
            w = gauss(np.hypot(*(dem_xy[nb] - sup_xy[j]).T), d0) @ dem[nb]
            R[j] = sup[j] / w if w > 0 else 0.0
    A = np.zeros(len(pts))
    for s in range(0, len(pts), chunk):
        p = pts[s:s + chunk]
        d = np.hypot(p[:, :1] - sup_xy[:, 0], p[:, 1:] - sup_xy[:, 1])
        A[s:s + chunk] = gauss(d, d0) @ R
    return A, R


def sample_polys(parts, step=0.1):
    """Supply points: 100 m grid inside each polygon (centroid if none); polygon area (m2) split equally."""
    xy, w = [], []
    for g in parts:
        x0, y0, x1, y1 = g.bounds
        gx, gy = np.meshgrid(np.arange(x0 + step / 2, x1, step), np.arange(y0 + step / 2, y1, step))
        gx, gy = gx.ravel(), gy.ravel(); m = shapely.contains_xy(g, gx, gy)
        p = np.column_stack([gx[m], gy[m]]) if m.any() else np.array([[g.centroid.x, g.centroid.y]])
        xy.append(p); w.append(np.full(len(p), g.area * 1e6 / len(p)))
    return np.vstack(xy), np.concatenate(w)


def grid_sum(xy, w, step=0.25):
    """Aggregate point supply to a 250 m grid (keeps the dense step-2 matrix small)."""
    k = np.floor(xy / step).astype(int)
    u, inv = np.unique(k, axis=0, return_inverse=True)
    s = np.bincount(inv.ravel(), w); c = np.zeros((len(u), 2))
    np.add.at(c, inv.ravel(), xy * w[:, None]); c /= s[:, None]
    m = s > 0
    return c[m], s[m]


if __name__ == "__main__":
    D = parcels(); P = D[["x", "y"]].to_numpy()
    core = load("core.json")
    H = np.array(core["hex"]["cells"], float); hxy, hpop, hemp = H[:, :2], H[:, 2], H[:, 3]
    # children demand: hex pop x NIL share aged 0-14 (NIL of nearest parcel point; ecological assumption)
    nil_a014 = {n["id"]: n["ind"].get("a014") for n in core["nil"]}
    _, k = cKDTree(P).query(hxy)
    a014 = np.array([nil_a014.get(i) or np.nan for i in D.nil_id.to_numpy()[k]], float)
    a014 = np.where(np.isnan(a014), np.nanmedian(a014), a014)
    hkid = hpop * a014 / 100

    # jobs proxy: non-residential GFA on parcels whose dominant DBT use is a work use (assumption, see model.md)
    WORK = ["Amministrativo", "Commerciale", "Industriale", "Servizi pubblici", "Trasporti e impianti"]
    jw = np.where(D.use_dom.isin(WORK), D.gfa_m2 * (1 - D.use_res_share.fillna(0)), 0.0)
    jxy, js = grid_sum(P[jw > 0], jw[jw > 0])
    log("work-GFA proxy km2", round(jw.sum() / 1e6, 2), "grid cells", len(js))

    lay = {k: sample_polys(pgt_layer(k)) for k in ("srv_ist", "srv_alt", "srv_verde")}
    st = {}
    for s in core["metro"]["st"]: st.setdefault(s["n"], (s["x"], s["y"]))
    sxy = np.array(list(st.values()))

    # catchments (Euclidean km; assumptions): jobs 8 km ~ 30-40 min transit; walk services 1.0 km; green 0.8 km; metro 1.0 km
    spec = {"A_jobs": (hxy, hemp, jxy, js, 8.0),
            "A_school": (hxy, hkid, *lay["srv_ist"], 1.0),
            "A_services": (hxy, hpop, *lay["srv_alt"], 1.0),
            "A_green": (hxy, hpop, *lay["srv_verde"], 0.8),
            "A_metro": (hxy, hpop, sxy, np.ones(len(sxy)), 1.0)}
    out = D[["ref", "x", "y", "nil_id", "soft_site"]].copy()
    for name, (dxy, dem, sxy_, sup, d0) in spec.items():
        out[name], _ = e2sfca(dxy, dem, sxy_, sup, P, d0)
        log(name, "done; zero share", round(float((out[name] == 0).mean()), 3))
    # units: A_jobs m2 work-GFA per employed resident; A_school m2 school land per child; A_services, A_green m2 per resident
    out["A_metro"] *= 1e4     # stations per 10,000 residents

    # simple measures
    out["d_school"] = cKDTree(lay["srv_ist"][0]).query(P)[0]
    out["d_services"] = cKDTree(lay["srv_alt"][0]).query(P)[0]
    out["d_green"] = D.green_srv_km.to_numpy()
    out["d_metro"] = D.metro_km.to_numpy()
    tj = cKDTree(jxy); out["cum_jobs_5km"] = [js[n].sum() for n in tj.query_ball_point(P, 5.0)]
    out["metro_n800"] = D.metro_n800.to_numpy()
    for c in ["nil_green", "nil_heatrisk", "nil_heatexp"]: out[c] = D[c].to_numpy()
    out.round(5).to_csv(os.path.join(RES, "access_parcels.csv.gz"), index=False)

    # redundancy diagnostic (DIAGNOSTIC ONLY: never used to derive weights)
    cols = ["A_jobs", "A_school", "A_services", "A_green", "A_metro", "cum_jobs_5km", "d_school", "d_services",
            "d_green", "d_metro", "metro_n800", "nil_green", "nil_heatrisk", "nil_heatexp"]
    S = out[out.soft_site][cols].dropna()
    rho = S.rank().corr(); rho.round(3).to_csv(os.path.join(RES, "access_corr.csv"))
    Z = S.rank().to_numpy(); Z = (Z - Z.mean(0)) / Z.std(0)
    ev = np.linalg.eigvalsh(np.corrcoef(Z.T))[::-1]
    pairs = [(a, b, round(rho.loc[a, b], 3)) for i, a in enumerate(cols) for b in cols[i + 1:] if abs(rho.loc[a, b]) >= 0.7]
    summ = {"n_parcels": len(out), "n_soft_sites": int(out.soft_site.sum()),
            "catchment_km": {k: v[-1] for k, v in spec.items()},
            "describe_soft_sites": S[cols[:5]].describe(percentiles=[.05, .5, .95]).round(3).to_dict(),
            "spearman_2sfca_vs_simple": {a: round(float(rho.loc[a, b]), 3) for a, b in
                                         [("A_school", "d_school"), ("A_services", "d_services"), ("A_green", "d_green"),
                                          ("A_metro", "d_metro"), ("A_metro", "metro_n800"), ("A_jobs", "cum_jobs_5km")]},
            "pairs_abs_rho_ge_0.7": pairs,
            "pca_eigen_share": [round(float(e / ev.sum()), 3) for e in ev],
            "pca_n_eig_gt_1": int((ev > 1).sum()),
            "jobs_proxy_total_km2": round(float(jw.sum() / 1e6), 2)}
    # how much the shortlist changes: top-10% overlap when 2SFCA replaces simple distance
    def top(v, hi=True, q=0.9):
        v = np.asarray(v); return set(np.nonzero(v >= np.quantile(v, q))[0] if hi else np.nonzero(v <= np.quantile(v, 1 - q))[0])
    summ["top10pct_jaccard_2sfca_vs_simple"] = {
        a: round(len(top(S[a]) & top(S[b], hi)) / len(top(S[a]) | top(S[b], hi)), 3)
        for a, b, hi in [("A_school", "d_school", False), ("A_green", "d_green", False), ("A_metro", "d_metro", False),
                         ("A_jobs", "cum_jobs_5km", True)]}
    save_json(summ, "access_summary.json")
    log("pairs |rho|>=0.7:", pairs); log("PCA eig share:", summ["pca_eigen_share"][:5])
