"""Shared loaders for proposal C. Read-only access to mi/ and lab/data/."""
import json, os, time, sys
import numpy as np, pandas as pd, shapely
from shapely.geometry import Polygon
from shapely import STRtree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MI = os.path.join(ROOT, "mi")
RES = os.path.join(HERE, "results"); os.makedirs(RES, exist_ok=True)
KX, KY = 111.32 * np.cos(np.radians(45.465)), 110.57
T0 = time.time()
log = lambda *a: print(f"[{time.time() - T0:6.1f}s]", *a, file=sys.stderr, flush=True)
load = lambda f: json.load(open(os.path.join(MI, "out", f), encoding="utf-8"))


def to_lonlat(x, y):
    return 9.19 + np.asarray(x) / KX, 45.465 - np.asarray(y) / KY


def from_lonlat(lon, lat):
    return (np.asarray(lon) - 9.19) * KX, -(np.asarray(lat) - 45.465) * KY


# Copied from lab/data/build_parcels.py (that script runs its pipeline on import).
def dec(a, u):
    return np.cumsum(np.asarray(a, dtype=np.int64).reshape(-1, 2), axis=0) * u


def poly(a, u):
    if len(a) < 6: return None
    g = Polygon(dec(a, u))
    if not g.is_valid: g = g.buffer(0)
    if g.is_empty: return None
    return g if g.geom_type == "Polygon" else max(g.geoms, key=lambda q: q.area)


def rings_to_geom(rings, u):
    ps = [p for p in (poly(r, u) for r in rings) if p is not None]
    if not ps: return []
    tree = STRtree(ps); depth = np.zeros(len(ps), int)
    rp = [p.representative_point() for p in ps]
    for i, p in enumerate(ps):
        for j in tree.query(rp[i], predicate="within"):
            if j != i and ps[j].area > p.area: depth[i] += 1
    shells = shapely.union_all([p for p, d in zip(ps, depth) if d % 2 == 0])
    holes = [p for p, d in zip(ps, depth) if d % 2 == 1]
    g = shells.difference(shapely.union_all(holes)) if holes else shells
    return [q for q in getattr(g, "geoms", [g]) if q.geom_type == "Polygon" and not q.is_empty]


def pgt_layer(k):
    P = load("pgt.json")
    c = next(c for c in P["cats"] if c["k"] == k)
    return rings_to_geom(c["p"], 0.01)


def parcels():
    d = pd.read_csv(os.path.join(ROOT, "lab", "data", "parcels.csv.gz"), dtype={"ref": str})
    return d[d.kind == "land"].reset_index(drop=True)


def save_json(obj, name):
    json.dump(obj, open(os.path.join(RES, name), "w", encoding="utf-8"), indent=1, ensure_ascii=False,
              default=lambda o: o.item() if hasattr(o, "item") else str(o))


def bh_fdr(p, q=0.05):
    """Benjamini-Hochberg: boolean mask of discoveries."""
    p = np.asarray(p); m = len(p); o = np.argsort(p)
    thr = q * np.arange(1, m + 1) / m
    ok = p[o] <= thr
    k = np.max(np.nonzero(ok)[0]) + 1 if ok.any() else 0
    mask = np.zeros(m, bool); mask[o[:k]] = True
    return mask


def morans_i(z, nbrs):
    """Global Moran's I with row-standardised binary weights; nbrs: list of index arrays."""
    z = np.asarray(z, float) - np.mean(z)
    lag = np.array([z[n].mean() if len(n) else 0.0 for n in nbrs])
    return float(len(z) / np.sum([len(n) > 0 for n in nbrs]) * (z @ lag) / (z @ z))
