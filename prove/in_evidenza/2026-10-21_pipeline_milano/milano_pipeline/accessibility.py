"""Accessibilità pedonale su grafo: tempo minimo a piedi dalla cella al servizio più vicino, per categoria.

Definizione di PAI usata in questa pipeline (UNICA, per evitare le definizioni multiple dei documenti precedenti):
    PAI = sum_c peso_c * 1[ t_c <= soglia_c ]      con sum peso_c = 1, valori in [0, 1]
Non è un 2SFCA: non usa capacità dei servizi né popolazione concorrente. Il 2SFCA è una estensione possibile
quando saranno disponibili le capacità (posti scuola, ecc.).
"""
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from .io_utils import METRIC


def _to_xy(lon, lat, lat0):
    k = 111_320.0
    return np.column_stack([np.asarray(lon) * k * np.cos(np.radians(lat0)), np.asarray(lat) * k])


def _nodes_xy(G):
    ids = list(G.nodes)
    lon = np.array([G.nodes[n]["x"] for n in ids])
    lat = np.array([G.nodes[n]["y"] for n in ids])
    return ids, lon, lat


def access_times(G, origins, pois, speed_kmh, tmax_min):
    """origins: GeoDataFrame punti WGS84 con colonna 'h3'. pois: dict cat -> GeoDataFrame punti WGS84.
    Ritorna DataFrame (index h3) con t_<cat> in minuti, NaN se oltre tmax_min o servizio assente."""
    U = G.to_undirected() if G.is_directed() else G
    ids, nlon, nlat = _nodes_xy(U)
    lat0 = float(np.mean(nlat))
    tree = cKDTree(_to_xy(nlon, nlat, lat0))
    ids = np.array(ids)

    ox_, oy_ = origins.geometry.x.values, origins.geometry.y.values
    od, oi = tree.query(_to_xy(ox_, oy_, lat0))
    onode = ids[oi]
    m_per_min = speed_kmh * 1000 / 60
    cutoff = tmax_min * m_per_min
    out = pd.DataFrame(index=origins["h3"].values)
    for cat, pg in pois.items():
        if pg is None or len(pg) == 0:
            out[f"t_{cat}"] = np.nan
            continue
        pd_, pi = tree.query(_to_xy(pg.geometry.x.values, pg.geometry.y.values, lat0))
        # il tratto POI -> nodo è sommato come sovrapprezzo alla sorgente
        src = {}
        for node, extra in zip(ids[pi], pd_):
            src[node] = min(src.get(node, np.inf), float(extra))
        dist = _msd(U, src, cutoff)
        d = np.array([dist.get(n, np.inf) for n in onode]) + od
        t = d / m_per_min
        t[t > tmax_min] = np.nan
        out[f"t_{cat}"] = t
    return out


def _msd(U, src, cutoff):
    """Dijkstra multi-sorgente con distanza iniziale per sorgente (offset)."""
    import heapq

    dist = {}
    heap = [(d0, n) for n, d0 in src.items() if d0 <= cutoff]
    heapq.heapify(heap)
    best = dict((n, d0) for d0, n in heap)
    while heap:
        d, n = heapq.heappop(heap)
        if n in dist:
            continue
        dist[n] = d
        for nb, data in U[n].items():
            if nb in dist:
                continue
            w = min((e.get("length", 1.0) for e in data.values())) if U.is_multigraph() else data.get("length", 1.0)
            nd = d + w
            if nd <= cutoff and nd < best.get(nb, np.inf):
                best[nb] = nd
                heapq.heappush(heap, (nd, nb))
    return dist


def compute_pai(times, categorie):
    pai = pd.Series(0.0, index=times.index)
    n_ok = pd.Series(0, index=times.index)
    for cat, spec in categorie.items():
        col = f"t_{cat}"
        if col not in times:
            continue
        ok = (times[col] <= spec["soglia_min"]).fillna(False)
        pai += spec["peso"] * ok.astype(float)
        n_ok += ok.astype(int)
    return pai, n_ok
