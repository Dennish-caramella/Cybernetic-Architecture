"""Lotti candidati: poligoni dismessi/trasformabili (PGT se disponibile, altrimenti OSM) valutati con gli stessi criteri.

Un lotto candidato è un'IPOTESI da verificare (proprietà, bonifica, vincoli, indici reali): qui si misura solo
dove convergono i criteri dichiarati.
"""
import geopandas as gpd
import numpy as np
import pandas as pd

from .accessibility import access_times, compute_pai
from .interpolate import _overlay
from .io_utils import METRIC, WGS84
from . import suitability as su


def build_lots(src, min_area_m2, boundary=None):
    s = src[src.geometry.notna() & src.geometry.geom_type.isin(["Polygon", "MultiPolygon"])].to_crs(METRIC)
    if len(s) == 0:
        return gpd.GeoDataFrame({"geometry": []}, crs=METRIC)
    if boundary is not None:
        s = s.clip(boundary.to_crs(METRIC).union_all())
        s = s[~s.geometry.is_empty]
    merged = s.geometry.make_valid().union_all()
    g = gpd.GeoDataFrame(geometry=gpd.GeoSeries([merged], crs=METRIC).explode(index_parts=False).reset_index(drop=True), crs=METRIC)
    g["area_m2"] = g.area
    g = g[g["area_m2"] >= min_area_m2].reset_index(drop=True)
    g["lot_id"] = [f"L{i:04d}" for i in range(len(g))]
    return g


def evaluate(lots, cells, crit, G, pois, cfg, prov=None):
    """cells: GeoDataFrame con index h3 e colonne valido/crit_*; crit: DataFrame crit_*."""
    if len(lots) == 0:
        return lots.to_crs(WGS84)
    grid = cells.reset_index()[["h3", "geometry"]].copy()
    grid["area_m2"] = grid.to_crs(METRIC).area
    inter = _overlay(grid, lots[["lot_id", "geometry"]])
    inter = inter.merge(cells.drop(columns="geometry")[["valido"] + [c for c in cells.columns if c.startswith("crit_")]],
                        left_on="h3", right_index=True, how="left")
    w = inter["ov_area"]
    res = pd.DataFrame(index=lots["lot_id"])
    nocell = set(lots["lot_id"]) - set(inter["lot_id"])
    if nocell and prov is not None:
        prov.avviso(f"lotti senza sovrapposizione con la griglia, scartati: {len(nocell)}")
    lots = lots[~lots["lot_id"].isin(nocell)].reset_index(drop=True)
    res = res.loc[lots["lot_id"]]
    for c in [c for c in inter.columns if c.startswith("crit_")]:
        res[c] = (inter[c] * w).groupby(inter["lot_id"]).sum() / w.groupby(inter["lot_id"]).sum()
    res["quota_vincolata"] = ((1 - inter["valido"].fillna(1)) * w).groupby(inter["lot_id"]).sum() / w.groupby(inter["lot_id"]).sum()
    # accessibilità dal centroide del lotto (più fine della media di cella)
    cent = lots.copy()
    cent["geometry"] = cent.geometry.representative_point()
    cent = cent.to_crs(WGS84)
    cent["h3"] = cent["lot_id"]
    times = access_times(G, cent[["h3", "geometry"]], pois, cfg["accessibilita"]["velocita_kmh"], cfg["accessibilita"]["tempo_max_min"])
    pai, nok = compute_pai(times, cfg["accessibilita"]["categorie"])
    res = res.join(times).assign(pai_lotto=pai, servizi_raggiunti=nok)
    if "crit_access" in res:
        res["crit_access"] = res["pai_lotto"]          # sostituisce la media di cella con il valore al lotto
    res["crit_transform"] = 1.0                           # per costruzione: il lotto è già un'area trasformabile
    C = res[[c for c in res.columns if c.startswith("crit_")]].rename(columns=lambda c: c[5:])
    valid = res["quota_vincolata"].fillna(0) < 0.5
    top_n = cfg["lotti"]["top_n"]
    for sc, wts in cfg["idoneita"]["scenari"].items():
        s = su.score(C, wts).where(valid, 0.0)
        res[f"s_{sc}"] = s
        res[f"rank_{sc}"] = s.rank(ascending=False, method="min")
        # robustezza: quota di estrazioni di pesi in cui il lotto sta nei primi top_n
        rng = np.random.default_rng(cfg["clustering"]["seed"])
        ww = su.renorm(wts, C.columns)
        draws = rng.dirichlet(cfg["idoneita"]["sensibilita"]["concentrazione"] * ww.values + 1e-6,
                              size=cfg["idoneita"]["sensibilita"]["n_estrazioni"])
        S = np.where(valid.values[:, None], C[ww.index].values @ draws.T, -np.inf)
        k = min(top_n, len(res))
        rank_pos = (-S).argsort(axis=0).argsort(axis=0)
        res[f"robust_{sc}"] = (rank_pos < k).mean(axis=1)
    res["area_m2"] = lots.set_index("lot_id")["area_m2"]
    f = cfg["lotti"].get("indice_if_m2_m2")
    if f:
        res["slp_stimata_m2"] = res["area_m2"] * f
    out = lots.set_index("lot_id").join(res.drop(columns="area_m2")).reset_index()
    return out.to_crs(WGS84)
