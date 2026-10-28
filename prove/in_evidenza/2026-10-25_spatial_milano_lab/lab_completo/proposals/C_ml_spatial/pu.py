"""2. Positive-unlabelled learning of 'designated-site likeness' with spatial block CV.
Positives (planner labels): parcels whose point-on-surface lies in a PGT Ambito di Trasformazione EXCEPT the
'PCU' (Parchi della Campagna Urbana: agricultural/park ambiti, not redevelopment sites), or in one of the
59 'ex AMB_DEG' degraded-area polygons of the PGT aree_dismesse layer. Secondary target: Ambiti di rigenerazione (pgt_rig).
Outputs: results/pu_metrics.json, pu_ablation.csv, pu_top_sites.csv/.geojson, pu_scores.csv.gz, pu_reliability.csv."""
import json, numpy as np, pandas as pd, shapely
from shapely.geometry import shape
from scipy.spatial import cKDTree
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold, KFold
from sklearn.metrics import average_precision_score, roc_auc_score
from common import *

RNG = np.random.default_rng(0)


def to_km(geom):
    return shapely.transform(shape(geom), lambda c: np.column_stack(from_lonlat(c[:, 0], c[:, 1])))


def at_objects():
    """Ambiti di Trasformazione (km frame), split into redevelopment ATs and PCU park ambiti."""
    F = json.load(open(os.path.join(MI, "raw", "pgt_ambiti_trasformazione.geojson"), encoding="utf-8"))["features"]
    return [(f["properties"]["NOME_AMB"], to_km(f["geometry"]), "(PCU" in f["properties"]["NOME_AMB"]) for f in F]


def amb_deg_mask(D):
    g = json.load(open(os.path.join(MI, "raw", "pgt_aree_dismesse.geojson"), encoding="utf-8"))["features"]
    polys = []
    for f in g:
        if not str(f["properties"].get("NOTE", "")).startswith("ex AMB_DEG"): continue
        geom = shape(f["geometry"])
        polys.append(shapely.transform(geom, lambda c: np.column_stack(from_lonlat(c[:, 0], c[:, 1]))))
    u = shapely.union_all(polys)
    return shapely.contains_xy(u, D.x.to_numpy(), D.y.to_numpy()), len(polys)


def features(D):
    X = pd.DataFrame(index=D.index)
    phys = {"log_area": np.log10(D.area_m2), "coverage": D.coverage, "far": D.far.clip(0, 15),
            "far_ratio": D.far_ratio.clip(0, 5), "h_max": D.h_max.fillna(0), "h_mean": D.h_mean.fillna(0),
            "log_nvol": np.log1p(D.n_vol), "use_res_share": D.use_res_share.fillna(0), "use_dom_share": D.use_dom_share.fillna(0)}
    for u in ["Residenziale", "Altro", "Industriale", "Commerciale", "Servizi pubblici", "Trasporti e impianti", "Agricolo"]:
        phys[f"use_{u[:6]}"] = (D.use_dom == u).astype(float)
    X = X.assign(**phys); groups = {"physical": list(phys)}
    # neighbourhood morphology from the 30 nearest land parcels (context, no labels)
    P = D[["x", "y"]].to_numpy(); _, nb = cKDTree(P).query(P, 31); nb = nb[:, 1:]
    ctx = {"nb_coverage": D.coverage.to_numpy()[nb].mean(1), "nb_far": D.far.clip(0, 15).to_numpy()[nb].mean(1),
           "nb_industrial": (D.use_dom == "Industriale").to_numpy()[nb].mean(1),
           "nb_vacant": (D.n_vol == 0).to_numpy()[nb].mean(1), "nb_log_area": np.log10(D.area_m2.to_numpy())[nb].mean(1),
           "metro_km": D.metro_km, "metro_n800": D.metro_n800, "green_srv_km": D.green_srv_km,
           "hex_pop": D.hex_pop, "hex_emp": D.hex_emp, "hex_dw": D.hex_dw, "hex_far": D.hex_far.astype(float),
           "dist_centre": np.hypot(D.x, D.y)}
    X = X.assign(**ctx); groups["context"] = list(ctx)
    nil = ["nil_rent", "nil_price", "nil_net_m", "nil_dens", "nil_for_", "nil_poor", "nil_a65"]
    X = X.assign(**{c: D[c] for c in nil}); groups["nil"] = nil
    dus = [c for c in D if c.startswith("dusaf_") and c != "dusaf_sum"]
    X = X.assign(**{c: D[c] for c in dus}); groups["dusaf"] = dus
    return X, groups


def blocks(D, km):
    t = D.tile.str.split("_", expand=True).astype(int)  # 2 km tiles
    f = km // 2
    return (t[0] // f).astype(str) + "_" + (t[1] // f).astype(str)


def hgb():
    return HistGradientBoostingClassifier(max_iter=300, learning_rate=0.06, max_leaf_nodes=31, min_samples_leaf=40,
                                          l2_regularization=1.0, random_state=0)


def oof(X, s, cv, model=hgb, bag=0):
    """Out-of-fold g(x)=P(s=1|x) and per-fold Elkan-Noto c = mean g over held-out labelled positives.
    bag>0: PU bagging (Mordelet & Vert 2014) - each bag trains on all train positives vs an equal-size unlabelled sample."""
    g = np.zeros(len(s)); cs = []
    for tr, te in cv:
        if bag:
            P_, U_ = tr[s[tr] == 1], tr[s[tr] == 0]; acc = np.zeros(len(te))
            for b in range(bag):
                idx = np.concatenate([P_, RNG.choice(U_, len(P_), replace=False)])
                acc += model().fit(X[idx], s[idx]).predict_proba(X[te])[:, 1]
            g[te] = acc / bag
        else:
            g[te] = model().fit(X[tr], s[tr]).predict_proba(X[te])[:, 1]
        if s[te].sum(): cs.append(float(g[te][s[te] == 1].mean()))
    return g, cs


def metrics(s, g):
    o = np.argsort(-g); n = len(s)
    rec = {f"recall@{q}%": round(float(s[o[:int(n * q / 100)]].sum() / s.sum()), 3) for q in (1, 5, 10)}
    return {"pr_auc": round(float(average_precision_score(s, g)), 3), "base_rate": round(float(s.mean()), 4),
            "roc_auc": round(float(roc_auc_score(s, g)), 3), **rec}


if __name__ == "__main__":
    D = parcels()
    deg, n_deg = amb_deg_mask(D)
    ATS = at_objects(); xs, ys = D.x.to_numpy(), D.y.to_numpy()
    in_at = np.zeros(len(D), bool); in_pcu = np.zeros(len(D), bool)
    for nm, geom, pcu in ATS:
        m = shapely.contains_xy(geom, xs, ys)
        if pcu: in_pcu |= m
        else: in_at |= m
    s_site = (in_at | deg).astype(int)
    log("parcels in redevelopment ATs", in_at.sum(), "in PCU park ambiti (left unlabelled, never candidates)", in_pcu.sum())
    s_zone = (D.pgt_rig >= 0.5).to_numpy().astype(int)
    log("positives site", s_site.sum(), "(tras", int((D.pgt_tras >= .5).sum()), "amb_deg pts", int(deg.sum()), "polys", n_deg, ") zone", s_zone.sum())
    Xdf, groups = features(D); X = Xdf.to_numpy(float)
    P = D[["x", "y"]].to_numpy(); _, knn = cKDTree(P).query(P, 9); nbrs = list(knn[:, 1:])
    B2, B4 = blocks(D, 2), blocks(D, 4)
    cvs = {"random": list(KFold(5, shuffle=True, random_state=0).split(X)),
           "block2km": list(GroupKFold(5).split(X, groups=B2)),
           "block4km": list(GroupKFold(5).split(X, groups=B4))}
    res = {"n": len(D), "positives_site": int(s_site.sum()), "parcels_in_redev_AT": int(in_at.sum()), "parcels_in_PCU_unlabelled": int(in_pcu.sum()), "amb_deg_polygons": n_deg,
           "positives_zone_rig": int(s_zone.sum()), "n_blocks": {"2km": int(B2.nunique()), "4km": int(B4.nunique())},
           "features": groups, "runs": {}}

    def run(name, s, cv, cols=None, **kw):
        Xs = X if cols is None else Xdf[cols].to_numpy(float)
        g, cs = oof(Xs, s, cvs[cv], **kw)
        m = metrics(s, g); m["c_folds"] = [round(c, 3) for c in cs]
        m["moran_I_residual"] = round(morans_i(s - g, nbrs), 3)
        res["runs"][name] = m; log(name, m); return g

    res["moran_I_label_site"] = round(morans_i(s_site, nbrs), 3)
    res["moran_I_label_zone"] = round(morans_i(s_zone, nbrs), 3)
    # baselines: crude FAR rule and low far_ratio as scores
    res["runs"]["baseline_soft_site_rule"] = metrics(s_site, D.soft_site.to_numpy().astype(float) + 1e-9 * RNG.random(len(D)))
    res["runs"]["baseline_1_minus_far_ratio"] = metrics(s_site, -D.far_ratio.clip(0, 5).to_numpy())
    logit = lambda: make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=1.0))
    Xn = np.nan_to_num(X, nan=0.0)
    g_l, cs = oof(Xn, s_site, cvs["block4km"], model=logit)
    res["runs"]["site_logit_block4km"] = {**metrics(s_site, g_l), "c_folds": [round(c, 3) for c in cs]}

    for cv in ("random", "block2km", "block4km"):
        g = run(f"site_hgb_{cv}", s_site, cv)
        if cv == "block4km": g_site = g
    run("site_pubag10_block4km", s_site, "block4km", bag=10)
    for cv in ("random", "block4km"): run(f"zone_rig_hgb_{cv}", s_zone, cv)

    # ablation (block 4 km): which feature groups carry the signal; DUSAF 2024 is post-designation (leakage risk)
    abl = []
    for name, gs in [("physical", ["physical"]), ("physical+context", ["physical", "context"]),
                     ("physical+context+nil", ["physical", "context", "nil"]), ("all(+dusaf2024)", ["physical", "context", "nil", "dusaf"]),
                     ("context+nil only (no parcel physics)", ["context", "nil"])]:
        cols = sum((groups[k] for k in gs), [])
        g, cs = oof(Xdf[cols].to_numpy(float), s_site, cvs["block4km"])
        abl.append({"features": name, **metrics(s_site, g), "c_mean": round(float(np.mean(cs)), 3)})
        log("ablation", abl[-1])
        if name == "physical+context": g_main, c_main = g, float(np.mean(cs))
    pd.DataFrame(abl).to_csv(os.path.join(RES, "pu_ablation.csv"), index=False)

    # main model = physical+context, block-4km OOF (every parcel scored by a model that never saw its 4 km block).
    # NIL socio-economics excluded on purpose: they would flag sites because of WHO lives nearby (income, % foreign).
    res["main_model"] = "HGB, physical+context (no NIL socio-economics), block4km OOF"; res["c_elkan_noto_main"] = round(c_main, 3)
    res["est_prior_pi_EN"] = round(float(g_main.mean() / c_main), 4)  # Elkan-Noto: pi = E[g]/c
    res["main_metrics"] = next(a for a in abl if a["features"] == "physical+context")
    # object-level recall: positives are ~89 planning objects, not 7k independent parcels
    top10 = g_main >= np.quantile(g_main, 0.9); objs = []
    for nm, geom, pcu in ATS:
        m = shapely.contains_xy(geom, xs, ys) & (s_site == 1)
        if m.any() and not pcu: objs.append({"AT": nm, "n_parcels": int(m.sum()),
                                 "area_share_top10": round(float(D.area_m2[m & top10].sum() / D.area_m2[m].sum()), 3)})
    objs = pd.DataFrame(objs); objs.to_csv(os.path.join(RES, "pu_object_recall.csv"), index=False)
    res["object_recall_AT"] = {"n_AT": len(objs), "AT_with_>=50pct_area_in_top10": int((objs.area_share_top10 >= .5).sum()),
                               "median_area_share_top10": float(objs.area_share_top10.median())}
    res["main_moran_I_residual"] = round(morans_i(s_site - g_main, nbrs), 3)
    bins = np.quantile(g_main, np.linspace(0, 1, 11)); k = np.clip(np.searchsorted(bins, g_main, side="right") - 1, 0, 9)
    rel = pd.DataFrame({"decile": range(10), "mean_g": [g_main[k == i].mean() for i in range(10)],
                        "observed_s": [s_site[k == i].mean() for i in range(10)]})
    rel.round(4).to_csv(os.path.join(RES, "pu_reliability.csv"), index=False)
    res["brier_g"] = round(float(np.mean((g_main - s_site) ** 2)), 4)
    # permutation importance would need refits per fold; report HGB-free proxy: univariate AUC of each feature
    res["univariate_auc_top"] = sorted(((c, round(abs(roc_auc_score(s_site, np.nan_to_num(Xdf[c].to_numpy(float))) - .5) + .5, 3))
                                        for c in Xdf.columns), key=lambda t: -t[1])[:12]

    # detected 'soft sites beyond the FAR rule': unlabelled, >= 2000 m2, not protected/green/water/service land
    PROT = ["pgt_srv_verde", "pgt_agr", "pgt_pae", "pgt_srv_ist", "pgt_srv_alt", "dusaf_wat", "dusaf_infra", "dusaf_green", "dusaf_agr", "dusaf_wood"]
    ok = (s_site == 0) & ~in_pcu & (D.pgt_tras < 0.5).to_numpy() & (D.area_m2 >= 2000).to_numpy() & (D[PROT].max(axis=1) < 0.5).to_numpy()
    sc = D[["ref", "x", "y", "nil_name", "area_m2", "use_dom", "coverage", "far", "far_ratio", "h_max", "soft_site", "pgt_rig", "pgt_srv_erp", "dusaf_prod", "dusaf_vac"]].copy()
    sc["g"] = g_main; sc["p_y_EN"] = np.minimum(1, g_main / c_main); sc["label_site"] = s_site
    sc["lon"], sc["lat"] = to_lonlat(sc.x, sc.y)
    sc.round(5).to_csv(os.path.join(RES, "pu_scores.csv.gz"), index=False)
    top = sc[ok].sort_values("g", ascending=False).head(200).round(5)
    top.to_csv(os.path.join(RES, "pu_top_sites.csv"), index=False)
    fc = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [r.lon, r.lat]},
         "properties": {k: (None if pd.isna(v) else v) for k, v in r.drop(["lon", "lat"]).items()}} for _, r in top.iterrows()]}
    json.dump(fc, open(os.path.join(RES, "pu_top_sites.geojson"), "w", encoding="utf-8"), default=lambda o: o.item() if hasattr(o, "item") else str(o))
    res["top200"] = {"eligible_unlabelled": int(ok.sum()), "share_soft_site_rule": round(float(top.soft_site.mean()), 3),
                     "share_in_rig": round(float((top.pgt_rig >= .5).mean()), 3),
                     "use_dom": top.use_dom.fillna("(none)").value_counts().to_dict(),
                     "median_area_m2": float(top.area_m2.median()), "total_area_ha": round(float(top.area_m2.sum() / 1e4), 1),
                     "n_nil": int(top.nil_name.nunique()), "g_range": [float(top.g.min()), float(top.g.max())],
                     "overlap_with_soft_site_rule_eligible": int((ok & D.soft_site.to_numpy()).sum())}
    save_json(res, "pu_metrics.json")
    log("done", res["top200"])
