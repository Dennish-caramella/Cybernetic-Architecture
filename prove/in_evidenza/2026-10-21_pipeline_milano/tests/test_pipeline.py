"""Test di correttezza dei calcoli (non dei dati). Esecuzione: python -m pytest tests -q   oppure   python tests/test_pipeline.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd
from shapely.geometry import Point, box

from milano_pipeline import accessibility as acc
from milano_pipeline import grid as gridmod
from milano_pipeline import interpolate, suitability as su


def test_extensive_intensive_conservation():
    # sorgente: un quadrato molto più grande della zona; 1000 residenti, reddito 20000 uniformi
    src = gpd.GeoDataFrame({"pop": [1000.0], "inc": [20000.0]}, geometry=[box(9.0, 45.4, 9.2, 45.5)], crs="EPSG:4326")
    bnd = gpd.GeoDataFrame(geometry=[box(9.10, 45.45, 9.11, 45.46)], crs="EPSG:4326")
    g = gridmod.build_grid(bnd, 9)
    out = interpolate.transfer(g, src, {"pop_total": {"col": "pop", "kind": "extensive"},
                                        "income_mean": {"col": "inc", "kind": "intensive"}})
    src_area = src.to_crs("EPSG:32632").area.iloc[0]
    expect = 1000.0 * g["area_m2"].sum() / src_area
    assert abs(out["pop_total"].sum() - expect) / expect < 1e-3
    assert np.allclose(out["income_mean"], 20000.0)


def test_intensive_weighted_by_population():
    # due poligoni affiancati con redditi diversi e popolazione diversa: la media pesata cade tra i due
    a = box(9.10, 45.45, 9.105, 45.46); b = box(9.105, 45.45, 9.11, 45.46)
    src = gpd.GeoDataFrame({"pop": [900.0, 100.0], "inc": [10000.0, 30000.0]}, geometry=[a, b], crs="EPSG:4326")
    bnd = gpd.GeoDataFrame(geometry=[box(9.1045, 45.455, 9.1055, 45.456)], crs="EPSG:4326")
    g = gridmod.build_grid(bnd, 9)
    out = interpolate.transfer(g, src, {"pop_total": {"col": "pop", "kind": "extensive"},
                                        "income_mean": {"col": "inc", "kind": "intensive", "peso": "pop_total"}})
    assert (out["income_mean"] >= 10000).all() and (out["income_mean"] <= 30000).all()


def test_access_times_line_graph():
    # linea di 5 nodi a 100 m l'uno dall'altro; servizio sul nodo 4; origine sul nodo 0 => 400 m
    G = nx.MultiDiGraph()
    lat0 = 45.46
    for i in range(5):
        G.add_node(i, x=9.19 + i * 100 / (111320 * np.cos(np.radians(lat0))), y=lat0)
    for i in range(4):
        G.add_edge(i, i + 1, length=100.0); G.add_edge(i + 1, i, length=100.0)
    org = gpd.GeoDataFrame({"h3": ["a"]}, geometry=[Point(G.nodes[0]["x"], lat0)], crs="EPSG:4326")
    poi = gpd.GeoDataFrame(geometry=[Point(G.nodes[4]["x"], lat0)], crs="EPSG:4326")
    t = acc.access_times(G, org, {"x": poi}, speed_kmh=6.0, tmax_min=20)   # 6 km/h = 100 m/min
    assert abs(t.loc["a", "t_x"] - 4.0) < 0.05
    t2 = acc.access_times(G, org, {"x": poi}, speed_kmh=6.0, tmax_min=3)
    assert np.isnan(t2.loc["a", "t_x"])


def test_pai_weights():
    times = pd.DataFrame({"t_a": [5, 30], "t_b": [5, 5]}, index=["x", "y"])
    pai, n = acc.compute_pai(times, {"a": {"peso": 0.6, "soglia_min": 10}, "b": {"peso": 0.4, "soglia_min": 10}})
    assert np.allclose(pai.values, [1.0, 0.4]) and list(n) == [2, 1]


def test_pareto_and_scores():
    C = pd.DataFrame({"a": [1, 0.5, 0.2, 0.9], "b": [0, 0.5, 0.2, 0.9]})
    valid = pd.Series([True] * 4, index=C.index)
    nd = su.pareto_front(C, valid)
    assert list(nd) == [True, False, False, True]        # (1,0) e (0.9,0.9) non dominati
    s = su.score(C, {"a": 1, "b": 1})
    assert np.isclose(s.iloc[3], 0.9) and np.isclose(s.iloc[0], 0.5)
    w = su.renorm({"a": 2, "b": 2, "zzz": 5}, C.columns)
    assert np.isclose(w.sum(), 1.0) and "zzz" not in w.index


def test_constraint_excludes():
    df = pd.DataFrame({"c_x": [0, 1, 0]}, index=list("abc"))
    ok = su.constraint_mask(df, ["c_x"])
    assert list(ok) == [True, False, True]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
