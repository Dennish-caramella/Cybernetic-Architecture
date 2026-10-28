"""Step 3: site criteria matrix (review1 §5.4). Benefit-oriented 0-1 scores, robust min-max on p2-p98 of the site
pool (or percentile rank where the source is only meaningful as a rank); raw values kept for teach-back.
`mix` and the PU score are deliberately NOT criteria (they go to constraints / audit)."""
import os
import numpy as np, pandas as pd
from config import *

ACC = os.path.join(PROP, "C_ml_spatial", "results", "access_parcels.csv.gz")
LABELS = {"access_metro": ("Metro access", "km to metro (lower better)"),
          "access_jobs": ("Jobs within 5 km", "work-GFA m2 within 5 km (rank)"),
          "services": ("Schools and services", "E2SFCA rank mean"),
          "green_access": ("Green access", "E2SFCA m2 green per resident (rank)"),
          "heat": ("Heat risk", "NIL heat-risk index (lower better)"),
          "demand_reach": ("People in need reached", "decay-weighted target households within 3 km"),
          "rent_burden": ("Rent burden", "NIL OMI rent of 60 m2 / net income per taxpayer"),
          "capacity": ("Capacity", "log10 dwellings"),
          "cost": ("Cost per dwelling", "EUR per dwelling (lower better)")}
BENEFIT = {"access_metro": False, "access_jobs": True, "services": True, "green_access": True, "heat": False,
           "demand_reach": True, "rent_burden": True, "capacity": True, "cost": False}
RANKED = {"access_jobs", "services", "green_access"}


def site_access(C, psite, n_sites):
    A = pd.read_csv(ACC, dtype={"ref": str}, usecols=["ref", "A_school", "A_services", "A_green", "cum_jobs_5km"])
    D = C[["ref", "area_m2"]].assign(site=psite).merge(A, on="ref", how="left")
    D = D[D.site >= 0]
    cols = ["A_school", "A_services", "A_green", "cum_jobs_5km"]
    for c in cols: D[c] = D[c].fillna(D[c].median())
    w = D.area_m2
    return pd.DataFrame({c: (D[c] * w).groupby(D.site).sum() / w.groupby(D.site).sum() for c in cols}).reindex(range(n_sites))


def mm(v, benefit):
    lo, hi = np.nanpercentile(v, [2, 98])
    s = np.clip((v - lo) / max(hi - lo, 1e-12), 0, 1)
    return s if benefit else 1 - s


def rank01(v):
    return pd.Series(v).rank(pct=True).values


def build(S, acc, dem_mean):
    raw = pd.DataFrame({
        "access_metro": S.metro_km.values,
        "access_jobs": acc.cum_jobs_5km.values,
        "services": 0.5 * (rank01(acc.A_school.values) + rank01(acc.A_services.values)),
        "green_access": np.clip(acc.A_green.values, None, np.nanpercentile(acc.A_green.values, 98)),
        "heat": S.nil_heatrisk.values,
        "demand_reach": dem_mean,
        "rent_burden": S.nil_rent.values * 60 / S.nil_net_m.values,
        "capacity": np.log10(np.maximum(S.cap.values, 1)),
        "cost": S.cost_per_dw.values,
    })[CRIT]
    X = pd.DataFrame({c: (rank01(raw[c].values) if c in RANKED else mm(raw[c].values, BENEFIT[c])) for c in CRIT})
    spec = [dict(k=c, label=LABELS[c][0], unit=LABELS[c][1], dir=1 if BENEFIT[c] else -1, rank=c in RANKED,
                 q02=float(np.nanpercentile(raw[c], 2)), q98=float(np.nanpercentile(raw[c], 98))) for c in CRIT]
    return raw, X, spec
