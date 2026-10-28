"""Uso del suolo per categorie (provincia) ed edifici + quartieri di Monza da OpenStreetMap -> detail_mb.json.
Uso: PYTHONPATH=C:/Temp/pl python build_detail_data.py   (risposte grezze in cache in ./raw_detail)
Dati (c) OpenStreetMap contributors, ODbL. Le superfici sommano i poligoni mappati: possibili sovrapposizioni e buchi."""
import json, math, os, sys, time, urllib.parse, urllib.request

from shapely.geometry import MultiPoint, Point, Polygon
from shapely.ops import voronoi_diagram

URL = "https://overpass-api.de/api/interpreter"
LON0, LAT0 = 9.27, 45.62
KX, KY = 111.32 * math.cos(math.radians(LAT0)), 110.57
U = 100
os.makedirs("raw_detail", exist_ok=True)
AREA = 'area["ISO3166-2"="IT-MB"]->.a;'
MONZA = 'area["ISO3166-2"="IT-MB"]->.a;rel(area.a)["boundary"="administrative"]["name"="Monza"]["admin_level"="8"]->.m;.m map_to_area->.ma;'


def q(name, pre, body):
    path = f"raw_detail/{name}.json"
    if os.path.exists(path): return json.load(open(path, encoding="utf-8"))
    data = urllib.parse.urlencode({"data": f"[out:json][timeout:300];{pre}{body}"}).encode()
    for i in range(4):
        try:
            req = urllib.request.Request(URL, data=data, headers={"User-Agent": "spatial-prototype/0.1 (research prototype)"})
            out = json.load(urllib.request.urlopen(req, timeout=330))
            json.dump(out, open(path, "w", encoding="utf-8"))
            print("ok", name, len(out["elements"]), file=sys.stderr); time.sleep(5)
            return out
        except Exception as e:
            print("retry", name, e, file=sys.stderr); time.sleep(30)
    raise SystemExit("overpass failed: " + name)


prj = lambda lo, la: ((lo - LON0) * KX, -(la - LAT0) * KY)


def geom(el): return [prj(g["lon"], g["lat"]) for g in el["geometry"]]


def assemble(ways):
    ways = [w[:] for w in ways if len(w) > 1]; rings = []
    while ways:
        ring = ways.pop(); grown = True
        while grown and ring[0] != ring[-1]:
            grown = False
            for i, w in enumerate(ways):
                if w[0] == ring[-1]: ring += w[1:]
                elif w[-1] == ring[-1]: ring += w[::-1][1:]
                elif w[-1] == ring[0]: ring = w[:-1] + ring
                elif w[0] == ring[0]: ring = w[::-1][:-1] + ring
                else: continue
                ways.pop(i); grown = True; break
        if ring[0] == ring[-1] and len(ring) > 3: rings.append(ring)
    return rings


def rel_rings(el):
    outer = [[(round(x, 5), round(y, 5)) for x, y in (prj(g["lon"], g["lat"]) for g in m["geometry"])] for m in el.get("members", []) if m["type"] == "way" and m.get("role") in ("outer", "") and "geometry" in m]
    return assemble(outer)


def area_km2(r): return abs(sum(r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1] for i in range(len(r) - 1))) / 2
def centroid(r): return (sum(p[0] for p in r) / len(r), sum(p[1] for p in r) / len(r))


def inside(pt, rings):
    x, y = pt; c = False
    for r in rings:
        for i in range(len(r) - 1):
            (x1, y1), (x2, y2) = r[i], r[i + 1]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c


def dp(pts, tol):
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]; dx, dy = x2 - x1, y2 - y1; n = math.hypot(dx, dy) or 1e-9
    best, k = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * (pts[i][0] - x1) - dx * (pts[i][1] - y1)) / n
        if d > best: best, k = d, i
    if best <= tol: return [pts[0], pts[-1]]
    return dp(pts[:k + 1], tol)[:-1] + dp(pts[k:], tol)


def simp(pts, tol):
    if len(pts) > 3 and pts[0] == pts[-1]:
        k = max(range(1, len(pts) - 1), key=lambda i: math.hypot(pts[i][0] - pts[0][0], pts[i][1] - pts[0][1]))
        return dp(pts[:k + 1], tol)[:-1] + dp(pts[k:], tol)
    return dp(pts, tol)


def enc(pts):
    out, px, py = [], 0, 0
    for x, y in pts:
        ix, iy = round(x * U), round(y * U); out += [ix - px, iy - py]; px, py = ix, iy
    return out


# ---- comuni (confini da OSM, gia' in cache da build_osm_data.py)
com = json.load(open("raw/comuni.json", encoding="utf-8"))["elements"]
comuni = []
for el in com:
    rings = sorted(rel_rings(el), key=area_km2, reverse=True)
    if rings and el["tags"].get("ref:ISTAT", "").startswith("108"):
        comuni.append({"id": el["tags"]["ref:ISTAT"], "n": el["tags"]["name"], "rings": rings})
which = lambda pt: next((c["id"] for c in comuni if inside(pt, c["rings"])), None)

# ---- categorie di uso del suolo: (chiave, etichetta, colore, ordine di disegno, [(nome query, filtro)])
CATS = [
    ("agr", "Agricolo", "#c9d36a", ['(way(area.a)["landuse"~"^(farmland|meadow|orchard|vineyard|farmyard|allotments)$"];rel(area.a)["landuse"~"^(farmland|meadow|orchard|vineyard)$"];);']),
    ("vac", "Vuoto e in trasformazione", "#b8b3a8", ['(way(area.a)["landuse"~"^(construction|brownfield|greenfield)$"];);']),
    ("green", "Verde e parchi", "#52b788", None),
    ("res", "Residenziale", "#f4a582", None),
    ("com", "Commerciale", "#e5484d", None),
    ("ind", "Industriale", "#b39ddb", None),
    ("edu", "Istruzione", "#5eead4", ['(way(area.a)["amenity"~"^(school|kindergarten|college|university)$"];);']),
    ("hea", "Sanità", "#22b8cf", ['(way(area.a)["amenity"~"^(hospital|clinic)$"];);']),
    ("rel", "Culto", "#74a7e0", ['(way(area.a)["amenity"="place_of_worship"];);']),
    ("trn", "Trasporti", "#d0d0d0", ['(way(area.a)["landuse"="railway"];way(area.a)["aeroway"~"^(aerodrome|runway|apron)$"];);']),
    ("wat", "Acqua", "#4cc9f0", ['(way(area.a)["natural"="water"];rel(area.a)["natural"="water"];way(area.a)["waterway"="riverbank"];);']),
]
polys = {c[0]: [] for c in CATS}


def add(cat, ring):
    ar = area_km2(ring)
    if ar >= 0.003: polys[cat].append((ar, ring))


for key, _, _, body in CATS:
    if body:
        for el in q("lu_" + key, AREA, body[0] + "out geom;")["elements"]:
            rs = rel_rings(el) if el["type"] == "relation" else ([geom(el)] if len(el.get("geometry", [])) > 3 and el["geometry"][0] == el["geometry"][-1] else [])
            for r in rs: add(key, r)
for el in json.load(open("raw/landuse.json", encoding="utf-8"))["elements"]:
    r = geom(el)
    if len(r) > 3 and r[0] == r[-1]:
        add({"residential": "res", "industrial": "ind", "commercial": "com", "retail": "com"}[el["tags"]["landuse"]], r)
for f in ("green_w", "green_r"):
    for el in json.load(open(f"raw/{f}.json", encoding="utf-8"))["elements"]:
        rs = rel_rings(el) if el["type"] == "relation" else ([geom(el)] if len(el.get("geometry", [])) > 3 and el["geometry"][0] == el["geometry"][-1] else [])
        for r in rs: add("green", r)

totals, bycom, cats_out = {}, {}, []
for key, label, color, _ in CATS:
    t = 0.0
    for ar, r in polys[key]:
        t += ar
        cid = which(centroid(r))
        if cid: bycom.setdefault(cid, {}).setdefault(key, 0.0); bycom[cid][key] += ar
    totals[key] = round(t, 2)
    keep = sorted(polys[key], key=lambda p: -p[0])
    cats_out.append({"k": key, "l": label, "c": color, "p": [enc(simp(r, 0.025)) for ar, r in keep if ar >= 0.01]})
for v in bycom.values():
    for k in v: v[k] = round(v[k], 3)
print("km2 per categoria:", totals, file=sys.stderr)

# ---- Monza: edifici e quartieri
mz = next(c for c in comuni if c["n"] == "Monza")
sub = q("monza_sub", MONZA, '(node(area.ma)["place"~"suburb|neighbourhood|quarter"];rel(area.ma)["place"~"suburb|neighbourhood|quarter"];);out tags center;')["elements"]
pts = []
for e in sub:
    lo, la = (e["lon"], e["lat"]) if e["type"] == "node" else (e["center"]["lon"], e["center"]["lat"])
    pts.append((e["tags"].get("name", "?"), prj(lo, la)))
mzpoly = Polygon(mz["rings"][0]).buffer(0)
vor = voronoi_diagram(MultiPoint([p for _, p in pts]), envelope=mzpoly.buffer(2))
districts = []
for cell in vor.geoms:
    clip = cell.intersection(mzpoly)
    if clip.is_empty: continue
    if clip.geom_type != "Polygon": clip = max(clip.geoms, key=lambda g: g.area)
    name = next((n for n, p in pts if cell.contains(Point(p))), "?")
    districts.append({"n": name, "ring": [(x, y) for x, y in clip.exterior.coords]})

bl = q("monza_buildings", MONZA, 'way(area.ma)["building"];out geom tags;')["elements"]
TYPE = {"house": "res", "detached": "res", "semidetached_house": "res", "terrace": "res", "residential": "res", "apartments": "apt", "dormitory": "apt",
        "retail": "com", "commercial": "com", "office": "com", "supermarket": "com", "hotel": "com",
        "industrial": "ind", "warehouse": "ind", "factory": "ind", "manufacture": "ind",
        "school": "pub", "hospital": "pub", "church": "pub", "chapel": "pub", "civic": "pub", "public": "pub", "university": "pub", "kindergarten": "pub", "government": "pub", "cathedral": "pub"}
DEFH = {"res": 7, "apt": 14, "com": 8, "ind": 8, "pub": 10, "oth": 4}
def hnum(v):
    try: return float(str(v).lower().replace("m", "").replace(",", ".").strip())
    except Exception: return None
bs = []
for w in bl:
    r = geom(w)
    if len(r) < 4 or r[0] != r[-1]: continue
    t = w["tags"]; ty = TYPE.get(t["building"], "oth")
    h = hnum(t.get("height")); known = 1
    if h is None:
        lv = hnum(t.get("building:levels"))
        h = lv * 3.2 if lv else None
    if h is None: h = DEFH[ty]; known = 0
    c = centroid(r); did = next((i for i, d in enumerate(districts) if inside(c, [d["ring"]])), -1)
    rr = simp(r, 0.002)
    if len(rr) < 4: continue
    bs.append([did, round(h, 1), known, ["res", "apt", "com", "ind", "pub", "oth"].index(ty), round(area_km2(r) * 1e6)] + enc(rr))
print("edifici:", len(bs), "con altezza dichiarata:", sum(b[2] for b in bs), "quartieri:", len(districts), file=sys.stderr)

out = {"source": "OpenStreetMap contributors (ODbL) via Overpass API", "unit_km": 1 / U,
       "lu": {"cats": cats_out, "totals": totals, "by": bycom},
       "monza": {"id": mz["id"], "ring": enc(simp(mz["rings"][0], 0.01)), "districts": [{"n": d["n"], "ring": enc(simp(d["ring"], 0.005))} for d in districts],
                 "types": ["Villette", "Condomini", "Commerciale", "Industriale", "Pubblico", "Altro"], "b": bs}}
json.dump(out, open("detail_mb.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
print("scritto detail_mb.json", os.path.getsize("detail_mb.json") // 1024, "KB", file=sys.stderr)
