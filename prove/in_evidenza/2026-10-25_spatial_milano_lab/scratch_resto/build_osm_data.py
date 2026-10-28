"""Scarica da OpenStreetMap (Overpass) i dati della provincia di Monza e della Brianza e li riduce a osm_mb.json.
Uso: python build_osm_data.py   (le risposte grezze sono in cache in ./raw)
Dati (c) OpenStreetMap contributors, ODbL."""
import json, math, os, sys, time, urllib.parse, urllib.request, datetime

URL = "https://overpass-api.de/api/interpreter"
AREA = 'area["ISO3166-2"="IT-MB"]->.a;'
LON0, LAT0 = 9.27, 45.62
KX, KY = 111.32 * math.cos(math.radians(LAT0)), 110.57  # km per grado
os.makedirs("raw", exist_ok=True)


def q(name, body):
    path = f"raw/{name}.json"
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))
    data = urllib.parse.urlencode({"data": f"[out:json][timeout:300];{AREA}{body}"}).encode()
    for i in range(4):
        try:
            req = urllib.request.Request(URL, data=data, headers={"User-Agent": "spatial-prototype/0.1 (research prototype)"})
            out = json.load(urllib.request.urlopen(req, timeout=330))
            json.dump(out, open(path, "w", encoding="utf-8"))
            print("ok", name, len(out["elements"]), file=sys.stderr)
            time.sleep(5)
            return out
        except Exception as e:
            print("retry", name, e, file=sys.stderr)
            time.sleep(30)
    raise SystemExit("overpass failed: " + name)


def prj(p):  # (lon, lat) -> km
    return ((p[0] - LON0) * KX, -(p[1] - LAT0) * KY)


def geom(el):
    return [prj((g["lon"], g["lat"])) for g in el["geometry"]]


def assemble(ways):
    """unisce polilinee per estremi in anelli chiusi"""
    ways = [w[:] for w in ways if len(w) > 1]
    rings = []
    while ways:
        ring = ways.pop()
        grown = True
        while grown and ring[0] != ring[-1]:
            grown = False
            for i, w in enumerate(ways):
                if w[0] == ring[-1]: ring += w[1:]
                elif w[-1] == ring[-1]: ring += w[::-1][1:]
                elif w[-1] == ring[0]: ring = w[:-1] + ring
                elif w[0] == ring[0]: ring = w[::-1][:-1] + ring
                else: continue
                ways.pop(i); grown = True; break
        if ring[0] == ring[-1] and len(ring) > 3:
            rings.append(ring)
    return rings


def rel_rings(el):
    outer = [[prj((g["lon"], g["lat"])) for g in m["geometry"]] for m in el.get("members", []) if m["type"] == "way" and m.get("role") in ("outer", "") and "geometry" in m]
    return assemble([[(round(x, 5), round(y, 5)) for x, y in w] for w in outer])


def area_km2(r):
    return abs(sum(r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1] for i in range(len(r) - 1))) / 2


def centroid(r):
    return (sum(p[0] for p in r) / len(r), sum(p[1] for p in r) / len(r))


def inside(pt, rings):
    x, y = pt
    c = False
    for r in rings:
        for i in range(len(r) - 1):
            (x1, y1), (x2, y2) = r[i], r[i + 1]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                c = not c
    return c


def dp(pts, tol):
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy) or 1e-9
    best, k = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * (pts[i][0] - x1) - dx * (pts[i][1] - y1)) / n
        if d > best: best, k = d, i
    if best <= tol: return [pts[0], pts[-1]]
    return dp(pts[:k + 1], tol)[:-1] + dp(pts[k:], tol)


def simp(pts, tol):
    """Douglas-Peucker che non collassa gli anelli chiusi"""
    if len(pts) > 3 and pts[0] == pts[-1]:
        k = max(range(1, len(pts) - 1), key=lambda i: math.hypot(pts[i][0] - pts[0][0], pts[i][1] - pts[0][1]))
        return dp(pts[:k + 1], tol)[:-1] + dp(pts[k:], tol)
    return dp(pts, tol)


U = 100  # 1 unita = 10 m


def enc(pts):  # delta-encoding in unita da 10 m
    out, px, py = [], 0, 0
    for x, y in pts:
        ix, iy = round(x * U), round(y * U)
        out += [ix - px, iy - py]; px, py = ix, iy
    return out


def seglen(pts):
    return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))


# ---- scarico
prov = q("province", 'rel["ISO3166-2"="IT-MB"];out geom;')
com = q("comuni", 'rel(area.a)["boundary"="administrative"]["admin_level"="8"];out geom;')
roads = q("roads", 'way(area.a)["highway"~"^(motorway|trunk|primary|secondary)$"];out geom;')
rails = q("rails", 'way(area.a)["railway"="rail"][!"service"];out geom;')
stns = q("stations", 'node(area.a)["railway"~"^(station|halt)$"];out;')
pois = q("pois", '(nwr(area.a)["amenity"~"^(school|kindergarten|college|university|hospital|clinic|doctors|pharmacy)$"];nwr(area.a)["shop"];);out center tags;')
luse = q("landuse", '(way(area.a)["landuse"~"^(residential|industrial|commercial|retail)$"];);out geom;')
green_w = q("green_w", '(way(area.a)["leisure"="park"];way(area.a)["landuse"="forest"];way(area.a)["natural"="wood"];);out geom;')
green_r = q("green_r", '(rel(area.a)["leisure"="park"];rel(area.a)["landuse"="forest"];rel(area.a)["natural"="wood"];);out geom;')

# ---- provincia e comuni
prov_rings = rel_rings(prov["elements"][0])
prov_rings.sort(key=area_km2, reverse=True)
comuni = []
for el in com["elements"]:
    rings = rel_rings(el)
    if not rings: continue
    rings.sort(key=area_km2, reverse=True)
    c = centroid(rings[0])
    if not inside(c, prov_rings[:1]): continue
    t = el["tags"]
    pop = t.get("population", "").replace(".", "").replace(",", "")
    comuni.append({"n": t.get("name", "?"), "id": t.get("ref:ISTAT", ""), "pop": int(pop) if pop.isdigit() else None, "rings": rings, "c": c,
                   "a": round(sum(area_km2(r) for r in rings), 2),
                   "k": dict(school=0, higher=0, health=0, pharmacy=0, shop=0, station=0, road_km=0.0, res=0.0, ind=0.0, com=0.0, green=0.0)})
print("comuni", len(comuni), file=sys.stderr)


def which(pt):
    for i, c in enumerate(comuni):
        if inside(pt, c["rings"]): return i
    return -1


# stazioni (dedup entro 300 m)
stations = []
for n in stns["elements"]:
    p = prj((n["lon"], n["lat"]))
    if any(math.hypot(p[0] - s[0], p[1] - s[1]) < 0.3 for s in stations): continue
    stations.append((p[0], p[1], n.get("tags", {}).get("name", "")))
for s in stations:
    i = which(s[:2])
    if i >= 0: comuni[i]["k"]["station"] += 1
for c in comuni:
    c["k"]["dist_station"] = round(min(math.hypot(c["c"][0] - s[0], c["c"][1] - s[1]) for s in stations), 2)

# POI
for e in pois["elements"]:
    ctr = e.get("center") or {"lat": e.get("lat"), "lon": e.get("lon")}
    if ctr.get("lat") is None: continue
    i = which(prj((ctr["lon"], ctr["lat"])))
    if i < 0: continue
    t, k = e.get("tags", {}), comuni[i]["k"]
    a = t.get("amenity")
    if a in ("school", "kindergarten"): k["school"] += 1
    elif a in ("college", "university"): k["higher"] += 1
    elif a in ("hospital", "clinic", "doctors"): k["health"] += 1
    elif a == "pharmacy": k["pharmacy"] += 1
    elif "shop" in t: k["shop"] += 1

# strade: km di secondaria o superiore per comune (punto medio del segmento)
road_feats = []
for w in roads["elements"]:
    pts = geom(w)
    cls = {"motorway": 1, "trunk": 1, "primary": 2, "secondary": 3}[w["tags"]["highway"]]
    for i in range(len(pts) - 1):
        mid = ((pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2)
        j = which(mid)
        if j >= 0: comuni[j]["k"]["road_km"] += math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
    road_feats.append((cls, simp(pts, 0.02)))

# uso del suolo e verde (area assegnata al comune del baricentro)
for w in luse["elements"]:
    pts = geom(w)
    if len(pts) < 4: continue
    j = which(centroid(pts))
    if j < 0: continue
    key = {"residential": "res", "industrial": "ind", "commercial": "com", "retail": "com"}[w["tags"]["landuse"]]
    comuni[j]["k"][key] += area_km2(pts)
green_polys = []
for el in green_w["elements"]:
    pts = geom(el)
    if len(pts) < 4: continue
    ar = area_km2(pts); j = which(centroid(pts))
    if j >= 0: comuni[j]["k"]["green"] += ar
    if ar > 0.12: green_polys.append((ar, simp(pts, 0.03)))
for el in green_r["elements"]:
    for r in rel_rings(el):
        ar = area_km2(r); j = which(centroid(r))
        if j >= 0: comuni[j]["k"]["green"] += ar
        if ar > 0.12: green_polys.append((ar, simp(r, 0.03)))
green_polys.sort(key=lambda g: -g[0])

rail_feats = [simp(geom(w), 0.02) for w in rails["elements"] if len(w.get("geometry", [])) > 1]

out = {
    "source": "OpenStreetMap contributors (ODbL) via Overpass API",
    "fetched": datetime.date.today().isoformat(),
    "origin": {"lon": LON0, "lat": LAT0}, "unit_km": 1 / U,
    "province": [enc(simp(r, 0.03)) for r in prov_rings[:1]],
    "comuni": [{"n": c["n"], "id": c["id"], "pop": c["pop"], "a": c["a"], "c": [round(c["c"][0], 2), round(c["c"][1], 2)],
                "rings": [enc(simp(r, 0.03)) for r in c["rings"] if area_km2(r) > 0.05],
                "k": {k: (round(v, 2) if isinstance(v, float) else v) for k, v in c["k"].items()}} for c in comuni],
    "roads": [{"c": c, "p": enc(p)} for c, p in road_feats],
    "rails": [enc(p) for p in rail_feats],
    "stations": [{"x": round(s[0], 2), "y": round(s[1], 2), "n": s[2]} for s in stations],
    "green": [enc(p) for _, p in green_polys[:140]],
}
json.dump(out, open("osm_mb.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
print("scritto osm_mb.json", os.path.getsize("osm_mb.json") // 1024, "KB; comuni", len(comuni), "stazioni", len(stations), "strade", len(road_feats), file=sys.stderr)
