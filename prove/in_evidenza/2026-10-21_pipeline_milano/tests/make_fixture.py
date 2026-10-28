"""Genera DATI SINTETICI di collaudo in data_test/. Non rappresentano Milano: servono solo a provare il codice
(forma dei file, adattatori, calcoli). Ogni risultato ottenuto da questi dati è privo di significato urbano."""
import sys
from pathlib import Path

import geopandas as gpd
import networkx as nx
import numpy as np
import osmnx as ox
from shapely.geometry import Point, Polygon, box
from shapely.ops import voronoi_diagram

root = Path(__file__).resolve().parent.parent
D = root / "data_test"
C = D / "osm_cache"
C.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(7)
LAT0, LON0 = 45.464, 9.19
KX, KY = 111320 * np.cos(np.radians(LAT0)), 111320


def ll(x, y):
    return LON0 + x / KX, LAT0 + y / KY


def gdf(geoms, **cols):
    return gpd.GeoDataFrame(cols, geometry=geoms, crs="EPSG:4326")


# confine ellittico
t = np.linspace(0, 2 * np.pi, 80, endpoint=False)
bx, by = 7000 * np.cos(t), 6000 * np.sin(t)
boundary = Polygon([ll(x, y) for x, y in zip(bx, by)])
gdf([boundary]).to_file(C / "confine.gpkg", driver="GPKG")

# rete pedonale a maglia irregolare
xs, ys = np.arange(-7000, 7001, 150), np.arange(-6000, 6001, 150)
G = nx.MultiDiGraph(crs="EPSG:4326")
pos = {}
for i, x in enumerate(xs):
    for j, y in enumerate(ys):
        if (x / 7000) ** 2 + (y / 6000) ** 2 <= 1.0:
            xx, yy = x + rng.normal(0, 15), y + rng.normal(0, 15)
            lon, lat = ll(xx, yy)
            pos[(i, j)] = (len(pos), xx, yy)
            G.add_node(len(pos) - 1, x=lon, y=lat)
for (i, j), (n, x, y) in pos.items():
    for di, dj in ((1, 0), (0, 1)):
        k = pos.get((i + di, j + dj))
        if k and rng.random() > 0.08:  # alcune maglie mancanti
            L = float(np.hypot(k[1] - x, k[2] - y))
            G.add_edge(n, k[0], length=L)
            G.add_edge(k[0], n, length=L)
ox.save_graphml(G, C / "walk.graphml")

# servizi: più densi al centro
def pts(n, scale):
    r = np.abs(rng.normal(0, scale, n)); a = rng.uniform(0, 2 * np.pi, n)
    return [Point(*ll(min(r_ * np.cos(a_), 6900), min(r_ * np.sin(a_), 5900))) for r_, a_ in zip(r, a)]
for cat, n, sc in [("metro", 40, 3500), ("scuola", 180, 4500), ("asilo", 150, 4500), ("sanita", 120, 4500),
                   ("farmacia", 200, 4500), ("verde", 160, 5000), ("commercio", 300, 4500)]:
    gdf(pts(n, sc)).to_file(C / f"poi_{cat}.gpkg", driver="GPKG")

# edifici (quadrati piccoli), più densi al centro
bl = []
for p in pts(15000, 4200):
    s = rng.uniform(8, 25) / 111320
    bl.append(box(p.x - s, p.y - s, p.x + s, p.y + s))
gdf(bl, building=["yes"] * len(bl)).to_file(C / "edifici.gpkg", driver="GPKG")

# aree dismesse (sintetiche)
tr = []
for _ in range(60):
    cx, cy = rng.uniform(-6000, 6000), rng.uniform(-5000, 5000)
    w, h = rng.uniform(60, 500), rng.uniform(60, 400)
    tr.append(Polygon([ll(cx, cy), ll(cx + w, cy), ll(cx + w, cy + h), ll(cx, cy + h)]))
gdf(tr, landuse=["brownfield"] * len(tr)).to_file(C / "landuse_dismessi.gpkg", driver="GPKG")
prot = Polygon([ll(-3000, -6000), ll(3000, -6000), ll(3000, -4300), ll(-3000, -4300)])
gdf([prot], boundary=["protected_area"]).to_file(C / "protette.gpkg", driver="GPKG")
gdf([g for g in [__import__("shapely.geometry", fromlist=["LineString"]).LineString([ll(-7000, 0), ll(7000, 0)]),
                 __import__("shapely.geometry", fromlist=["LineString"]).LineString([ll(0, -6000), ll(0, 6000)])]]
    ).to_file(C / "strade_principali.gpkg", driver="GPKG")

# fonti "ufficiali" sintetiche
from shapely.geometry import MultiPoint
seeds = MultiPoint([Point(rng.uniform(-7000, 7000), rng.uniform(-6000, 6000)) for _ in range(90)])
vor = voronoi_diagram(seeds, envelope=box(-8000, -7000, 8000, 7000))
cells = [g for g in vor.geoms]
rows = []
for g in cells:
    c = g.centroid
    d = np.hypot(c.x / 7000, c.y / 6000)
    area_km2 = g.area / 1e6
    dens = (14000 * np.exp(-1.6 * d) + 1500) * rng.uniform(0.8, 1.2)
    pop = dens * area_km2
    rows.append(dict(
        pop_tot=pop, pop_65=pop * rng.uniform(0.15, 0.30), famiglie=pop / 2.1,
        reddito=24000 + 9000 * np.exp(-3 * (d - 0.15) ** 2) + rng.normal(0, 2500)))
pop_g = gdf([Polygon([ll(x, y) for x, y in g.exterior.coords]) for g in cells],
            **{k: [r[k] for r in rows] for k in rows[0]})
pop_g.to_file(D / "popolazione.gpkg", driver="GPKG")

rings = []
for k, rad in enumerate([1500, 3000, 4500, 6000, 9000]):
    t = np.linspace(0, 2 * np.pi, 60, endpoint=False)
    rings.append(Polygon([ll(1.17 * rad * np.cos(a), rad * np.sin(a)) for a in t]))
zones, prev = [], None
for k, r in enumerate(rings):
    z = r if prev is None else r.difference(prev)
    zones.append(z); prev = r
affitto = [22, 17, 14, 11.5, 10]
prezzo = [6500, 4200, 3200, 2600, 2300]
gdf(zones, aff_min=[a * 0.85 for a in affitto], aff_max=[a * 1.15 for a in affitto],
    pr_min=[p * 0.85 for p in prezzo], pr_max=[p * 1.15 for p in prezzo]).to_file(D / "omi.gpkg", driver="GPKG")
pg = [Polygon([ll(cx, cy), ll(cx + 500, cy), ll(cx + 500, cy + 400), ll(cx, cy + 400)])
      for cx, cy in [(-4500, 1000), (2500, -3000), (4000, 3500), (-1000, 4200), (500, -1500)]]
gdf(pg, nome=["ambito_%d" % i for i in range(len(pg))]).to_file(D / "pgt_ambiti.gpkg", driver="GPKG")
print("fixture sintetica scritta in", D)
