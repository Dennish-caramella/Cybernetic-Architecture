"""Costruzione del vettore di indicatori per cella H3."""
import numpy as np
import pandas as pd

from .io_utils import METRIC


def share_of_cell(grid, polys, name, clip=True):
    """Quota di area della cella coperta dall'unione dei poligoni."""
    if polys is None or len(polys) == 0:
        return None
    from .interpolate import _overlay

    p = polys[polys.geometry.notna() & polys.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]
    if len(p) == 0:
        return None
    u = p.to_crs(METRIC).union_all()
    import geopandas as gpd

    src = gpd.GeoDataFrame(geometry=[u], crs=METRIC).to_crs(grid.crs)
    inter = _overlay(grid, src)
    ca = grid.set_index("h3")["area_m2"]
    s = (inter.groupby("h3")["ov_area"].sum() / ca).reindex(ca.index).fillna(0)
    return s.clip(0, 1).rename(name)


def sum_area_share(grid, polys, name):
    """Quota di cella coperta dalla SOMMA delle aree dei poligoni (senza unione): adatta a molti edifici."""
    if polys is None or len(polys) == 0:
        return None
    from .interpolate import _overlay

    p = polys[polys.geometry.notna() & polys.geometry.geom_type.isin(["Polygon", "MultiPolygon"])][["geometry"]]
    inter = _overlay(grid, p.reset_index(drop=True))
    ca = grid.set_index("h3")["area_m2"]
    return (inter.groupby("h3")["ov_area"].sum() / ca).reindex(ca.index).fillna(0).clip(0, 1).rename(name)


def finalize(df, cfg):
    """Indicatori derivati dai grezzi. Colonne assenti producono indicatori assenti (non inventati)."""
    out = df.copy()
    area_km2 = out["area_m2"] / 1e6
    if "pop_total" in out:
        out["pop_density"] = out["pop_total"] / area_km2
    if {"pop_over65", "pop_total"} <= set(out.columns):
        out["share_elderly"] = out["pop_over65"] / out["pop_total"].replace(0, np.nan)
    if {"omi_rent_min", "omi_rent_max"} <= set(out.columns):
        out["omi_rent_mid"] = (out["omi_rent_min"] + out["omi_rent_max"]) / 2
    if {"omi_price_min", "omi_price_max"} <= set(out.columns):
        out["omi_price_mid"] = (out["omi_price_min"] + out["omi_price_max"]) / 2
    target = cfg["obiettivo_canone"]["canone_target_eur_m2_mese"]
    if "omi_rent_mid" in out:
        out["afford_gap"] = (out["omi_rent_mid"] - target).clip(lower=0)
    # quota trasformabile: massimo tra PGT (se presente) e OSM (candidati da verificare)
    parts = [c for c in ("transformable_share_pgt", "transformable_share_osm") if c in out]
    if parts:
        out["transformable_share"] = out[parts].max(axis=1)
    return out
