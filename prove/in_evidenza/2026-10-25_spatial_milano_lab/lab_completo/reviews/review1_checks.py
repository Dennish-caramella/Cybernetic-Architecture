"""Reviewer spot-checks for review1.md. Read-only on lab/data and lab/proposals; prints results only.
Run: PYTHONPATH=C:/Temp/pl python lab/reviews/review1_checks.py   (~30 s)
"""
import os, sys, json
import numpy as np, pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score

LAB = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PR = os.path.join(LAB, "proposals")
sys.path.insert(0, os.path.join(PR, "A_econ_or"))
from portfolio import pcu_mask  # read-only helper

P = pd.read_csv(os.path.join(LAB, "data", "parcels.csv.gz"), dtype={"ref": str})
L = P[(P.kind == "land") & ~P.outside_city].copy()
L["pcu"] = pcu_mask(L.x.values, L.y.values)
nil = pd.read_csv(os.path.join(LAB, "data", "nil.csv"))
out = {}

# --- B: are top SMAA parcels inside PCU parks / which PGT layers?
B = pd.read_csv(os.path.join(PR, "B_decision", "results", "e1_smaa_candidates.csv"), dtype={"ref": str})
Bt = B.sort_values("holistic_uniform", ascending=False).head(100).merge(L[["ref", "pcu", "pgt_tras", "pgt_rig", "soft_site", "use_dom", "dusaf_green", "dusaf_agr", "n_vol"]], on="ref", how="left")
out["B_top100_in_PCU"] = int(Bt.pcu.sum())
out["B_top100_soft_site"] = int(Bt.soft_site.sum())
out["B_top100_vacant_nvol0"] = int((Bt.n_vol == 0).sum())
out["B_top100_dusaf_agr_or_green_ge05"] = int(((Bt.dusaf_agr >= .5) | (Bt.dusaf_green >= .5)).sum())
out["B_top100_n_nil"] = int(Bt.nil_id.nunique())
out["B_top10_refs_pcu"] = Bt.head(10)[["ref", "nil_name", "pcu", "dusaf_agr", "dusaf_green"]].to_dict("records")

# --- C: direction of the univariate AUC (C reports |AUC-0.5|+0.5, sign lost)
S = pd.read_csv(os.path.join(PR, "C_ml_spatial", "results", "pu_scores.csv.gz"), dtype={"ref": str}, usecols=["ref", "label_site"])
M = L.merge(S, on="ref")
for c in ["nil_for_", "nil_poor", "nil_net_m", "nil_rent", "metro_km", "hex_pop"]:
    m = M[c].notna()
    out[f"C_signed_auc_{c}"] = round(float(roc_auc_score(M.label_site[m], M[c][m])), 3)
out["C_pos_mean_for_vs_unl"] = [round(float(M[M.label_site == 1].nil_for_.mean()), 2), round(float(M[M.label_site == 0].nil_for_.mean()), 2)]
out["C_pos_mean_poor_vs_unl"] = [round(float(M[M.label_site == 1].nil_poor.mean()), 2), round(float(M[M.label_site == 0].nil_poor.mean()), 2)]

# --- A: where do portfolios build? dwelling-weighted NIL profile vs household-weighted city
D = pd.read_csv(os.path.join(PR, "A_econ_or", "results", "demand_nil.csv"))
hh = D.set_index("nil_id").hh
city_poor = float(np.average(nil.set_index("nil_id").poor.reindex(hh.index), weights=hh))
city_for = float(np.nanmean(np.where(nil.set_index("nil_id").for_.reindex(hh.index).notna(), nil.set_index("nil_id").for_.reindex(hh.index) * hh, np.nan)) / hh.mean())
for p in ["P2", "P6"]:
    s = pd.read_csv(os.path.join(PR, "A_econ_or", "results", f"sites_{p}.csv"), dtype={"ref": str}).merge(nil[["nil_id", "poor", "for_", "rent", "metro_pop"]], on="nil_id")
    out[f"A_{p}_dw"] = round(float(s.dwellings.sum()), 1)
    out[f"A_{p}_n_nil_built"] = int(s.nil_id.nunique())
    out[f"A_{p}_dw_weighted_poor"] = round(float(np.average(s.poor, weights=s.dwellings)), 2)
    out[f"A_{p}_dw_weighted_for"] = round(float(np.average(s.for_.fillna(s.for_.mean()), weights=s.dwellings)), 2)
    out[f"A_{p}_share_public_srv_erp_dw"] = round(float(s.dwellings[s.public].sum() / s.dwellings.sum()), 3)
    top10D = set(D.sort_values("D_mean", ascending=False).head(10).nil_id)
    out[f"A_{p}_share_dw_in_top10_demand_nil"] = round(float(s.dwellings[s.nil_id.isin(top10D)].sum() / s.dwellings.sum()), 3)
out["A_city_hh_weighted_poor"] = round(city_poor, 2)
out["A_city_hh_weighted_for"] = round(city_for, 2)
out["A_top10_demand_nil_share_of_D"] = round(float(D.sort_values("D_mean", ascending=False).head(10).D_mean.sum() / D.D_mean.sum()), 3)

# --- Cross-proposal: are the three 'need' indicators the same thing? (NIL level)
X = D[["nil_id", "D_mean", "hh"]].merge(nil[["nil_id", "rent", "net_m", "poor", "for_"]], on="nil_id")
X["A_target_rate"] = X.D_mean / X.hh
X["B_need"] = X.rent * 60 / X.net_m
H = pd.read_csv(os.path.join(PR, "C_ml_spatial", "results", "hex_need.csv"))
Cn = H.groupby("nil").apply(lambda g: np.average(g.pressure, weights=g["pop"]) if g["pop"].sum() > 0 else np.nan, include_groups=False).rename("C_pressure")
X = X.merge(nil[["nil_id", "nil_name"]], on="nil_id").merge(Cn, left_on="nil_name", right_index=True, how="left")
for a, b in [("A_target_rate", "B_need"), ("A_target_rate", "C_pressure"), ("B_need", "C_pressure"), ("A_target_rate", "rent"), ("A_target_rate", "poor"), ("C_pressure", "poor")]:
    m = X[[a, b]].notna().all(1)
    out[f"rho_{a}__{b}"] = round(float(spearmanr(X[a][m], X[b][m])[0]), 3)
out["n_nil_cross"] = int(X[["A_target_rate", "B_need", "C_pressure"]].notna().all(1).sum())

# --- Segregation preview: designated land vs all land (area-weighted NIL context)
def prof(mask, name):
    g = L[mask]; w = g.area_m2
    return {"n": int(mask.sum()), "km2": round(float(w.sum() / 1e6), 2),
            "poor": round(float(np.average(g.nil_poor, weights=w)), 2),
            "for_": round(float(np.average(g.nil_for_.fillna(g.nil_for_.mean()), weights=w)), 2),
            "net_m": round(float(np.average(g.nil_net_m, weights=w)), 0),
            "metro_km": round(float(np.average(g.metro_km, weights=w)), 3)}
land = L.kind == "land"
out["SEG_all_land"] = prof(land, "all")
out["SEG_tras_nonPCU"] = prof(land & (L.pgt_tras >= .5) & ~L.pcu, "tras")
out["SEG_srv_erp"] = prof(land & (L.pgt_srv_erp >= .5), "erp")
out["SEG_rig"] = prof(land & (L.pgt_rig >= .5), "rig")
out["SEG_soft_site"] = prof(land & L.soft_site & ~L.pcu, "soft")

print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
