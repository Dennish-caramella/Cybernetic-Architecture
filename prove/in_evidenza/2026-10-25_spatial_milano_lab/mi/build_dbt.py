"""Edifici (DBT 2020 del Comune di Milano: unita' volumetriche con altezza reale) e lotti (particelle catastali Agenzia Entrate) a tasselli di 1 km.
Uscite: out/t/<tx>_<ty>.json (caricati su richiesta), out/tiles.json (indice + indicatori per NIL). Uso: PYTHONPATH=C:/Temp/pl python build_dbt.py
Fonti: Comune di Milano DBT 2020 (volo 2020, scala 1:1000); Agenzia delle Entrate, cartografia catastale INSPIRE (CC BY 4.0)."""
import collections, glob, json, math, os, sys
import numpy as np, shapefile, shapely
from pyproj import Transformer
from shapely.geometry import Point, Polygon, shape
from shapely.strtree import STRtree

LON0, LAT0 = 9.19, 45.465
KX, KY = 111.32 * math.cos(math.radians(LAT0)), 110.57
UT = 2000  # nei tasselli 1 unita' = 0,5 m
TILE = 2.0  # km
os.makedirs("out/t", exist_ok=True)
log = lambda *a: print(*a, file=sys.stderr, flush=True)
T = Transformer.from_crs(7791, 4326, always_xy=True)


def utm(a):
    lon, lat = T.transform(a[:, 0], a[:, 1])
    return np.column_stack(((lon - LON0) * KX, -(lat - LAT0) * KY))


def enc(coords):
    out, px, py = [], 0, 0
    for x, y in coords:
        ix, iy = round(x * UT), round(y * UT); out += [ix - px, iy - py]; px, py = ix, iy
    return out


tile_of = lambda x, y: (math.floor(x / TILE), math.floor(y / TILE))

# ---------- NIL (dal core gia' costruito)
core = json.load(open("out/core.json", encoding="utf-8"))
U = core["meta"]["unit_km"]


def dec(a):
    o, x, y = [], 0, 0
    for i in range(0, len(a), 2):
        x += a[i]; y += a[i + 1]; o.append((x * U, y * U))
    return o


nils = []
for n in core["nil"]:
    rings = [Polygon(dec(r)).buffer(0) for r in n["rings"] if len(r) >= 6]
    nils.append((n["id"], shapely.union_all(rings)))
ntree = STRtree([g for _, g in nils])


def nil_at(x, y):
    p = Point(x, y)
    for i in ntree.query(p):
        if nils[i][1].contains(p): return nils[i][0]
    return None


# ---------- uso degli edifici (EDIFC -> EDIFC_USO)
USO = {}
for r in shapefile.Reader(dbf="raw/dbt/EDIFC_EDIFC_USO.dbf").iterRecords():
    USO.setdefault(r[0], r[1])
UCAT = {"01": 0, "02": 1, "03": 2, "04": 3, "05": 3, "06": 4, "07": 5, "08": 6, "09": 7, "10": 3, "11": 3, "12": 4}  # indici in USES
USES = ["Residenziale", "Amministrativo", "Servizi pubblici", "Culto, cultura e sport", "Trasporti e impianti", "Commerciale", "Industriale", "Agricolo", "Altro"]

# ---------- unita' volumetriche
vols = collections.defaultdict(list)
polys, meta = [], []
sf = shapefile.Reader("raw/dbt/UN_VOL")
skipped = collections.Counter()
for sr in sf.iterShapeRecords():
    d = sr.record.as_dict()
    if d["UN_VOL_POR"] == "02": skipped["interrato"] += 1; continue  # porzione interrata
    h = float(d["UN_VOL_AV"] or 0)
    if h <= 0.5: skipped["h0"] += 1; continue
    try:
        g = shapely.transform(shape(sr.shape.__geo_interface__), utm, include_z=False).buffer(0)
    except Exception:
        skipped["geom"] += 1; continue
    if g.is_empty: continue
    g = g if g.geom_type == "Polygon" else max(g.geoms, key=lambda q: q.area)
    s = g.simplify(0.0006)
    ring = list((s if s.geom_type == "Polygon" else g).exterior.coords)[:-1]
    if len(ring) < 3: continue
    u = UCAT.get(str(USO.get(d["CEDIUV"], "95"))[:2], 8)
    c = g.representative_point()
    polys.append(g); meta.append({"h": round(min(h, 260), 1), "q": round(float(d["UN_VOL_QE"] or 0), 1), "u": u, "ring": ring, "x": c.x, "y": c.y, "a": g.area * 1e6, "e": d["CEDIUV"]})
log("volumi", len(meta), dict(skipped))

# ---------- particelle catastali
seen, parcels = set(), []
for f in glob.glob("raw/catasto/*.json"):
    for ref, pts in json.load(open(f)):
        if ref in seen or len(pts) < 4: continue
        seen.add(ref)
        g = Polygon([((lo - LON0) * KX, -(la - LAT0) * KY) for lo, la in pts]).buffer(0)
        if g.is_empty or g.area < 2e-6: continue
        if g.geom_type != "Polygon": g = max(g.geoms, key=lambda q: q.area)
        parcels.append({"ref": ref, "g": g, "built": 0.0, "vol": 0.0})
log("particelle", len(parcels))
ptree = STRtree([p["g"] for p in parcels])
for m in meta:
    pt = Point(m["x"], m["y"])
    m["p"] = -1
    for i in ptree.query(pt):
        if parcels[i]["g"].contains(pt):
            parcels[i]["built"] += m["a"]; parcels[i]["vol"] += m["a"] * m["h"]; m["p"] = i; break

# ---------- tasselli
tiles = collections.defaultdict(lambda: {"v": [], "p": []})
for m in meta:
    k = tile_of(m["x"], m["y"])
    ref = parcels[m["p"]]["ref"].split("_", 1)[1] if m["p"] >= 0 else ""
    tiles[k]["v"].append([m["h"], m["u"], m["q"], ref] + enc(m["ring"]))
for p in parcels:
    c = p["g"].representative_point(); k = tile_of(c.x, c.y)
    a = p["g"].area * 1e6
    s = p["g"].simplify(0.0008)
    ring = list((s if s.geom_type == "Polygon" else p["g"]).exterior.coords)[:-1]
    if len(ring) < 3: continue
    tiles[k]["p"].append([p["ref"].split("_", 1)[1], round(a), round(min(1, p["built"] / a), 2), round(p["vol"] / a, 1)] + enc(ring))
index = []
for (tx, ty), t in tiles.items():
    json.dump({"u": 1 / UT, "v": t["v"], "p": t["p"]}, open(f"out/t/{tx}_{ty}.json", "w"), separators=(",", ":"))
    index.append([tx, ty, len(t["v"]), len(t["p"])])
log("tasselli", len(index), "MB", round(sum(os.path.getsize(f) for f in glob.glob("out/t/*.json")) / 1e6, 1))

# ---------- indicatori per NIL dal DBT e dal catasto
agg = collections.defaultdict(lambda: {"fa": 0.0, "vol": 0.0, "n": 0, "hs": [], "np": 0, "pa": 0.0})
for m in meta:
    i = nil_at(m["x"], m["y"])
    if i is None: continue
    a = agg[i]; a["fa"] += m["a"]; a["vol"] += m["a"] * m["h"]; a["n"] += 1; a["hs"].append((m["h"], m["a"]))
for p in parcels:
    c = p["g"].representative_point(); i = nil_at(c.x, c.y)
    if i is None: continue
    agg[i]["np"] += 1; agg[i]["pa"] += p["g"].area * 1e6
nil_ind = {}
area = {n["id"]: n["a"] * 1e6 for n in core["nil"]}
for i, a in agg.items():
    hs = sorted(a["hs"]); half = sum(w for _, w in hs) / 2; acc = 0; med = None
    for h, w in hs:
        acc += w
        if acc >= half: med = h; break
    nil_ind[i] = {"dbt_h": med, "dbt_cov": a["fa"] / area[i] * 100, "dbt_vol": a["vol"] / area[i], "dbt_n": a["n"], "lot_n": a["np"], "lot_a": a["pa"] / a["np"] if a["np"] else None,
                  "dbt_tall": sum(1 for h, _ in hs if h >= 30)}
json.dump({"tile": TILE, "index": index, "uses": USES, "nil": nil_ind}, open("out/tiles.json", "w"), separators=(",", ":"))
log("ok; esempio Duomo", nil_ind.get(1))
