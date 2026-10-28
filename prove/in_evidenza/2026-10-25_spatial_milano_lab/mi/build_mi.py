"""Costruisce i dati del prototipo per il Comune di Milano a partire dai file in raw/ (vedi fetch_regione.py, fetch_osm.py e i download open data).
Uscite in out/: core.json (incorporato nella pagina), pgt.json, dusaf.json, b/<ID_NIL>.json (caricati su richiesta).
Uso: PYTHONPATH=C:/Temp/pl python build_mi.py
Unita' territoriale: i 88 NIL (Nuclei d'Identita' Locale) del PGT Milano 2030."""
import collections, csv, io, json, math, os, sys, zipfile
import numpy as np, openpyxl, shapefile, shapely
from pyproj import Transformer
from shapely.geometry import MultiPolygon, Point, Polygon, shape
from shapely.ops import unary_union
from shapely.strtree import STRtree

LON0, LAT0 = 9.19, 45.465
KX, KY = 111.32 * math.cos(math.radians(LAT0)), 110.57
U = 100  # 1 unita' = 10 m
os.makedirs("out/b", exist_ok=True)
log = lambda *a: print(*a, file=sys.stderr, flush=True)


def ll(g):  # lon/lat -> km locali
    return shapely.transform(g, lambda a: np.column_stack(((a[:, 0] - LON0) * KX, -(a[:, 1] - LAT0) * KY)))


UTM = Transformer.from_crs(32632, 4326, always_xy=True)


def utm(g):  # i file Istat 'WGS84' sono in UTM 32N
    def f(a):
        lon, lat = UTM.transform(a[:, 0], a[:, 1])
        return np.column_stack(((lon - LON0) * KX, -(lat - LAT0) * KY))
    return shapely.transform(g, f)


def enc_ring(coords):
    out, px, py = [], 0, 0
    for x, y in coords:
        ix, iy = round(x * U), round(y * U)
        out += [ix - px, iy - py]; px, py = ix, iy
    return out


def enc_geom(g, tol, holes=True, min_area=0.0):
    if g.is_empty: return []
    g = g.simplify(tol, preserve_topology=True)
    polys = [g] if g.geom_type == "Polygon" else [p for p in getattr(g, "geoms", []) if p.geom_type == "Polygon"]
    rings = []
    for p in polys:
        if p.area < min_area: continue
        rings.append(enc_ring(list(p.exterior.coords)[:-1]))
        if holes: rings += [enc_ring(list(r.coords)[:-1]) for r in p.interiors if Polygon(r).area > max(min_area, 1e-4)]
    return rings


def polyonly(g):
    if g.is_empty: return g
    if g.geom_type in ("Polygon", "MultiPolygon"): return g
    return MultiPolygon([p for p in getattr(g, "geoms", []) if p.geom_type == "Polygon"]) if hasattr(g, "geoms") else g


def num(s):
    try: return float(str(s).replace(".", "").replace(",", ".")) if "," in str(s) else float(s)
    except Exception: return None


# ---------- confine e NIL
city = ll(shape(json.load(open("raw/milano.geojson", encoding="utf-8"))["features"][0]["geometry"])).buffer(0)
nils = []
for f in json.load(open("raw/nil.geojson", encoding="utf-8"))["features"]:
    g = ll(shape(f["geometry"])).buffer(0)
    p = f["properties"]
    name = " ".join(w.capitalize() if len(w) > 2 or i == 0 else w.lower() for i, w in enumerate(p["NIL"].replace("Q.RE", "Q.re").split()))
    nils.append({"id": int(p["ID_NIL"]), "n": name, "g": g, "a": g.area, "ind": {}})
nils.sort(key=lambda n: n["id"])
NI = {n["id"]: i for i, n in enumerate(nils)}
ntree = STRtree([n["g"] for n in nils])


def nil_at(x, y):
    pt = Point(x, y)
    for i in ntree.query(pt):
        if nils[i]["g"].contains(pt): return i
    return -1


log("NIL", len(nils), "area", round(sum(n["a"] for n in nils), 1))

# ---------- popolazione per NIL (anagrafe comunale, 1999-2025)
t = zipfile.ZipFile("raw/pop_nil.zip").read("ds27_pop_sto_quartiere.csv").decode("utf-8-sig", "replace")
Y = 2025
acc = collections.defaultdict(lambda: collections.Counter())
for r in csv.DictReader(io.StringIO(t), delimiter=";"):
    y = int(r["Anno"])
    if y not in (2015, Y): continue
    i = NI.get(int(r["IdNil"]))
    if i is None: continue
    v = int(r["Residenti"]); a = r["Eta"].strip()
    age = int("".join(ch for ch in a if ch.isdigit()) or 0)
    c = acc[i]
    c[f"p{y}"] += v
    if y == Y:
        if age < 15: c["a014"] += v
        elif age >= 65: c["a65"] += v
        if age >= 80: c["a80"] += v
        if r["Cittadinanza"].strip().lower() != "italia": c["for"] += v
for i, c in acc.items():
    n = nils[i]["ind"]; p = c[f"p{Y}"]
    if not p: continue
    n.update(pop=p, dens=p / nils[i]["a"], a014=c["a014"] / p * 100, a65=c["a65"] / p * 100, a80=c["a80"] / p * 100, for_=c["for"] / p * 100,
             trend=(p / c["p2015"] - 1) * 100 if c["p2015"] else None)
log("popolazione 2025", sum(n["ind"].get("pop", 0) for n in nils))

# ---------- Censimento 2021: sezioni -> esagoni e NIL
wb = openpyxl.load_workbook("../istat_samples/census_dl/R03_indicatori_2021_sezioni.xlsx", read_only=True)
rows = wb[wb.sheetnames[0]].iter_rows(min_row=1, max_row=70000, values_only=True)
h = next(rows); ix = {k: h.index(k) for k in ("SEZ21_ID", "PROCOM", "P1", "P101", "ST1", "P90", "P86", "P87", "P88", "P89")}
ind21 = {}
for r in rows:
    if r[ix["PROCOM"]] in (15146, "15146", "015146"):
        ind21[int(r[ix["SEZ21_ID"]])] = {k: (r[ix[k]] or 0) for k in ("P101", "ST1", "P90")}
sf = shapefile.Reader("../istat_samples/sezioni/x/SHP/R03_21_WGS84")
secs = []
for sr in sf.iterShapeRecords():
    d = sr.record.as_dict()
    if d["PRO_COM"] != 15146: continue
    g = utm(shape(sr.shape.__geo_interface__)).buffer(0)
    if g.is_empty: continue
    v = ind21.get(int(d["SEZ21_ID"]), {})
    secs.append((g, {"pop": d["POP21"], "emp": v.get("P101", 0), "for": v.get("ST1", 0), "deg": v.get("P90", 0), "dw": d["ABI21"], "bld": d["EDI21"]}))
log("sezioni Milano", len(secs))
R = 0.25
minx, miny, maxx, maxy = city.bounds
w, hh = math.sqrt(3) * R, 1.5 * R
cells = []; row = 0; y = miny - R
while y < maxy + R:
    x = minx - R + (w / 2 if row % 2 else 0)
    while x < maxx + R:
        cells.append(Polygon([(x + R * math.cos(math.radians(30 + 60 * k)), y + R * math.sin(math.radians(30 + 60 * k))) for k in range(6)])); x += w
    y += hh; row += 1
ctree = STRtree(cells)
HK = ("pop", "emp", "for", "deg", "dw")
cacc = [dict.fromkeys(HK, 0.0) for _ in cells]
nc = collections.defaultdict(lambda: collections.Counter())
sec_pts = []
for g, v in secs:
    if g.area <= 0: continue
    c = g.representative_point(); i = nil_at(c.x, c.y)
    if i >= 0:
        for k in v: nc[i][k] += v[k]
    sec_pts.append((c.x, c.y, v["pop"]))
    for j in ctree.query(g):
        a = cells[j].intersection(g).area
        if a > 0:
            for k in HK: cacc[j][k] += v[k] * a / g.area
hex_cells = []
for c, a in zip(cells, cacc):
    if a["pop"] >= 1:
        hex_cells.append([round(c.centroid.x, 3), round(c.centroid.y, 3)] + [int(round(a[k])) for k in HK])
for i, c in nc.items():
    n = nils[i]["ind"]
    if c["pop"]:
        n.update(pop21=c["pop"], emp21=c["emp"], deg=c["deg"] / c["pop"] * 100, dwp=c["dw"] / c["pop"] * 100)
log("esagoni", len(hex_cells))

# ---------- redditi IRPEF 2024 per CAP -> NIL (pesi: indirizzi OSM con CAP dentro il NIL)
t = open("raw/redditi2024.csv", "rb").read().decode("utf-8-sig")
capv = collections.defaultdict(dict)
for r in csv.reader(io.StringIO(t), delimiter=";"):
    if r[0] == "Anno di imposta": continue
    capv[r[1]][r[2]] = num(r[3]) or 0


def capm(v):
    fq = lambda k: v.get(k + " - Frequenza") or 0
    am = lambda k: v.get(k + " - Ammontare in euro") or 0
    ld = "Reddito da lavoro dipendente e assimilati"; rc = "Reddito complessivo"; ri = "Reddito imponibile"
    tax = am("Imposta netta") + am("Addizionale regionale dovuta") + am("Addizionale comunale dovuta")
    rate = tax / am(ri) if am(ri) else None
    o = {"taxpayers": v.get("Numero contribuenti", 0), "inc": am(rc) / fq(rc) if fq(rc) else None, "emp_n": fq(ld),
         "wage": am(ld) / fq(ld) if fq(ld) else None, "rate": rate, "pens_share": fq("Reddito da pensione") / v.get("Numero contribuenti", 1) * 100}
    if o["wage"] is not None and rate is not None:
        o["wage_m"] = o["wage"] / 12; o["net_m"] = o["wage"] * (1 - rate) / 12
    hi = sum(fq(f"Reddito complessivo da {a} euro") for a in ("75000 a 120000", "oltre 120000"))
    o["rich"] = hi / fq(rc) * 100 if fq(rc) else None
    lo = sum(fq(f"Reddito complessivo da {a} euro") for a in ("0 a 10000", "10000 a 15000")) + fq("Reddito complessivo minore o uguale a zero euro")
    o["poor"] = lo / fq(rc) * 100 if fq(rc) else None
    return o


CAP = {c: capm(v) for c, v in capv.items()}
tot = collections.Counter()
for v in capv.values():
    for k, x in v.items(): tot[k] += x
CITY_INC = capm(tot)
pc = collections.defaultdict(collections.Counter)
for e in json.load(open("raw/osm_postcodes.json", encoding="utf-8"))["elements"]:
    pcode = str(e.get("tags", {}).get("addr:postcode", "")).strip()[:5]
    c = e.get("center") or e
    if pcode not in CAP or "lat" not in c: continue
    x, y = (c["lon"] - LON0) * KX, -(c["lat"] - LAT0) * KY
    i = nil_at(x, y)
    if i >= 0: pc[i][pcode] += 1
for i, n in enumerate(nils):
    cnt = pc.get(i)
    if not cnt:
        n["ind"]["cap"] = []; continue
    totw = sum(cnt.values())
    for k in ("inc", "wage_m", "net_m", "rate", "rich", "poor", "pens_share"):
        vals = [(CAP[c].get(k), wv) for c, wv in cnt.items() if CAP[c].get(k) is not None]
        if vals: n["ind"][k] = sum(v * wv for v, wv in vals) / sum(wv for _, wv in vals)
    n["ind"]["cap"] = [c for c, _ in cnt.most_common(3)]
log("NIL con CAP", sum(1 for n in nils if n["ind"].get("cap")))

# ---------- OMI: canoni e prezzi 2024/2 (abitazioni civili) su zone OMI
t = open("raw/omi_riepilogo.csv", "rb").read().decode("utf-8-sig", "replace")
rows = [r for r in csv.DictReader(io.StringIO(t), delimiter=";") if r["Cod_Tip"] == "20"]
last = max((r["Anno"], r["Periodo"]) for r in rows)
zv = collections.defaultdict(list)
for r in rows:
    if (r["Anno"], r["Periodo"]) != last: continue
    lo, hi, clo, chi = (num(r[k]) for k in ("Loc_min", "Loc_max", "Compr_min", "Compr_max"))
    if lo and hi: zv[r["Zona"]].append((r["Stato"], (lo + hi) / 2, (clo + chi) / 2 if clo and chi else None))
ZONE = {}
for z, vs in zv.items():
    pick = [v for v in vs if v[0] == "NORMALE"] or vs
    ZONE[z] = {"rent": sum(v[1] for v in pick) / len(pick), "price": (sum(v[2] for v in pick if v[2]) / max(1, sum(1 for v in pick if v[2]))) or None}
zones = []
for f in json.load(open("raw/zone_omi_2021_2.geojson", encoding="utf-8"))["features"]:
    z = f["properties"]["Zona"]
    g = ll(shape({"type": f["geometry"]["type"], "coordinates": json.loads(json.dumps(f["geometry"]["coordinates"]).replace(", 0.0]", "]"))})).buffer(0)
    zones.append({"z": z, "d": f["properties"]["Zona_Descr"].title(), "g": g, **ZONE.get(z, {})})
for i, n in enumerate(nils):
    wsum = rs = ps = 0
    for zo in zones:
        if "rent" not in zo: continue
        a = n["g"].intersection(zo["g"]).area
        if a > 0: wsum += a; rs += zo["rent"] * a; ps += (zo["price"] or 0) * a
    if wsum: n["ind"].update(rent=rs / wsum, price=ps / wsum)
log("OMI semestre", last, "zone con valori", len(ZONE))

# ---------- verde e calore (Spotted, luglio 2024)
for key, f in (("green", "raw/green_nil.csv"), ("heatrisk", "raw/heatrisk_nil.csv"), ("heatexp", "raw/heatexp_nil.csv")):
    for r in csv.DictReader(io.StringIO(open(f, "rb").read().decode("utf-8-sig", "replace")), delimiter=";"):
        i = NI.get(int(r["ID_NIL"]))
        if i is not None: nils[i]["ind"][key] = float(r["value"]) * (100 if key != "green" else 1)

# ---------- metropolitana: stazioni, linee, accessibilita' a 500 m
COL = {"1": "#EE3124", "2": "#00A54F", "3": "#FDB913", "4": "#0064AF", "5": "#9B5BA5"}
st = []
for f in json.load(open("raw/metro_fermate.geojson", encoding="utf-8"))["features"]:
    lo, la = f["geometry"]["coordinates"][:2]
    st.append({"x": round((lo - LON0) * KX, 3), "y": round(-(la - LAT0) * KY, 3), "n": f["properties"]["nome"].title(), "l": str(f["properties"]["linee"])})
lines = []
for f in json.load(open("raw/metro_percorsi.geojson", encoding="utf-8"))["features"]:
    g = ll(shape(f["geometry"]))
    parts = [g] if g.geom_type == "LineString" else list(g.geoms)
    lines.append({"l": f["properties"]["linea"], "c": COL.get(f["properties"]["linea"], "#ccc"), "p": [enc_ring(list(p.simplify(0.01).coords)) for p in parts]})
buf = unary_union([Point(s["x"], s["y"]).buffer(0.5) for s in st])
for i, n in enumerate(nils):
    c = n["g"].representative_point()
    n["ind"]["metro_km"] = min(math.hypot(c.x - s["x"], c.y - s["y"]) for s in st)
    n["ind"]["metro_n"] = sum(1 for s in st if n["g"].contains(Point(s["x"], s["y"])))
    n["ind"]["metro_area"] = n["g"].intersection(buf).area / n["a"] * 100
popin = collections.Counter(); poptot = collections.Counter()
for x, y, p in sec_pts:
    i = nil_at(x, y)
    if i < 0: continue
    poptot[i] += p
    if buf.contains(Point(x, y)): popin[i] += p
for i in poptot:
    if poptot[i]: nils[i]["ind"]["metro_pop"] = popin[i] / poptot[i] * 100
CITY_METRO_POP = sum(popin.values()) / max(1, sum(poptot.values())) * 100

# ---------- DUSAF 2024 (uso del suolo reale) e PGT (previsioni di piano), con quote per NIL
def dusaf_cat(desc):
    c = desc.split(" ")[0]
    if c.startswith("111"): return "resd"
    if c.startswith("112"): return "resr"
    if c in ("12111", "12112", "12123", "12125"): return "prod"
    if c in ("12121", "12122", "12124"): return "serv"
    if c.startswith("122"): return "infra"
    if c.startswith("13"): return "vac"
    if c == "1412": return "unk"
    if c.startswith("14"): return "green"
    if c.startswith("2"): return "agr"
    if c.startswith("3"): return "wood"
    if c.startswith("5") or c.startswith("4"): return "wat"
    return "unk"


DCATS = [("resd", "Residenziale denso", "#f4a582"), ("resr", "Residenziale discontinuo", "#f7c9a6"), ("prod", "Produttivo e commerciale", "#b39ddb"),
         ("serv", "Servizi e ospedali", "#22b8cf"), ("infra", "Strade e ferrovie", "#bdbdbd"), ("vac", "Cantieri e aree degradate", "#8d8577"),
         ("green", "Parchi e sport", "#52b788"), ("unk", "Verde incolto", "#a3c585"), ("agr", "Agricolo", "#d9d27a"), ("wood", "Boschi e vegetazione", "#2d6a4f"), ("wat", "Acque", "#4cc9f0")]
PCATS = [("srv_verde", "Servizi: aree a verde", "#52b788"), ("srv_erp", "Servizi: edilizia residenziale pubblica", "#f28482"), ("srv_ist", "Servizi: istruzione e università", "#5eead4"),
         ("srv_alt", "Servizi: altri", "#74a7e0"), ("rig", "Ambiti di rigenerazione", "#ffd166"), ("dism", "Aree dismesse e degradate", "#8d8577"),
         ("tras", "Ambiti di trasformazione", "#e5484d"), ("naf", "Nuclei di antica formazione", "#c08497"), ("pae", "Aree di valore paesaggistico", "#2d6a4f"), ("agr", "Aree agricole", "#d9d27a")]


def load(f):
    return json.load(open(f, encoding="utf-8"))["features"]


def collect(feats, catf):
    groups = collections.defaultdict(list)
    for f in feats:
        if not f.get("geometry"): continue
        k = catf(f["properties"])
        if not k: continue
        try: g = ll(shape(f["geometry"])).buffer(0)
        except Exception: continue
        g = polyonly(g.intersection(city))
        if not g.is_empty: groups[k].append(g)
    return {k: unary_union(v) for k, v in groups.items()}


dus = collect(load("raw/dusaf.geojson"), lambda p: dusaf_cat(p["DESCRIZIONE"]))
SRV = {"Aree a verde": "srv_verde", "Edilizia residenziale pubblica": "srv_erp", "Istruzione": "srv_ist"}
pg = {}
pg.update(collect(load("raw/pgt_servizi.geojson"), lambda p: SRV.get(p.get("LEGENDA"), "srv_ist" if "Universit" in str(p.get("LEGENDA")) else "srv_alt")))
for f, k in (("ambiti_rigenerazione", "rig"), ("aree_dismesse", "dism"), ("ambiti_trasformazione", "tras"), ("nuclei_antica_formazione", "naf"), ("valore_paesaggistico", "pae"), ("aree_agricole", "agr")):
    pg.update(collect(load(f"raw/pgt_{f}.geojson"), lambda p, k=k: k))
ATS = []
for f in load("raw/pgt_ambiti_trasformazione.geojson"):
    p = f["properties"]; g = ll(shape(f["geometry"])).buffer(0); c = g.representative_point()
    ATS.append({"n": p.get("NOME_AMB"), "f": (p.get("DFUN_PREV1") or "").capitalize(), "st": round(g.area * 100, 1), "x": round(c.x, 3), "y": round(c.y, 3), "nil": nils[nil_at(c.x, c.y)]["n"] if nil_at(c.x, c.y) >= 0 else None})
cityA = city.area
for name, groups, cats in (("dusaf", dus, DCATS), ("pgt", pg, PCATS)):
    tot = {}
    for k, _, _ in cats:
        g = groups.get(k)
        if g is None: continue
        tot[k] = round(g.area, 3)
        for n in nils:
            a = n["g"].intersection(g).area
            if a > 0: n["ind"].setdefault(name, {})[k] = round(a / n["a"] * 100, 2)
    out = {"cats": [{"k": k, "l": l, "c": c, "p": enc_geom(groups[k], 0.006, True, 0.0004) if k in groups else []} for k, l, c in cats], "totals": tot, "area": round(cityA, 2)}
    if name == "pgt": out["ats"] = ATS
    json.dump(out, open(f"out/{name}.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
    log(name, {k: round(v / cityA * 100, 1) for k, v in tot.items()}, os.path.getsize(f"out/{name}.json") // 1024, "KB")

# ---------- edifici OSM per NIL (un file per NIL)
TYPE = {"house": "res", "detached": "res", "semidetached_house": "res", "terrace": "res", "apartments": "apt", "residential": "apt", "dormitory": "apt",
        "retail": "com", "commercial": "com", "office": "com", "supermarket": "com", "hotel": "com", "industrial": "ind", "warehouse": "ind", "factory": "ind",
        "school": "pub", "hospital": "pub", "church": "pub", "chapel": "pub", "civic": "pub", "public": "pub", "university": "pub", "kindergarten": "pub", "government": "pub", "cathedral": "pub", "train_station": "pub"}
DEFH = {"res": 7, "apt": 18, "com": 14, "ind": 9, "pub": 14, "oth": 9}
TYPES = ["res", "apt", "com", "ind", "pub", "oth"]


def hnum(v):
    try: return float(str(v).lower().replace("m", "").replace(",", ".").strip())
    except Exception: return None


per = collections.defaultdict(list)
for e in json.load(open("raw/osm_buildings.json", encoding="utf-8"))["elements"]:
    gm = e.get("geometry")
    if not gm or len(gm) < 4: continue
    pts = [((q["lon"] - LON0) * KX, -(q["lat"] - LAT0) * KY) for q in gm]
    if pts[0] != pts[-1]: continue
    t = e.get("tags", {}); bt = t.get("building", "yes")
    ty = TYPE.get(bt, "oth")
    h = hnum(t.get("height")); known = 1
    if h is None:
        lv = hnum(t.get("building:levels")); h = lv * 3.2 + (1 if lv else 0) if lv else None
    if h is None:
        h = 3 if bt in ("garage", "garages", "roof", "shed", "carport") else DEFH[ty]; known = 0
    g = Polygon(pts)
    if not g.is_valid: g = g.buffer(0)
    if g.is_empty or g.geom_type != "Polygon": continue
    c = g.representative_point(); i = nil_at(c.x, c.y)
    if i < 0: continue
    s = g.simplify(0.0015)
    ring = list(s.exterior.coords)[:-1] if s.geom_type == "Polygon" else list(g.exterior.coords)[:-1]
    if len(ring) < 3: continue
    per[i].append([round(min(h, 250), 1), known, TYPES.index(ty), round(g.area * 1e6)] + enc_ring(ring))
for i, n in enumerate(nils):
    b = per.get(i, [])
    json.dump(b, open(f"out/b/{n['id']}.json", "w"), separators=(",", ":"))
    if b:
        hs = sorted(x[0] for x in b)
        n["ind"].update(bld_n=len(b), bld_h=hs[len(hs) // 2], bld_known=sum(x[1] for x in b) / len(b) * 100,
                        gfa=sum(x[3] * max(1, round(x[0] / 3.2)) for x in b) / (n["a"] * 1e6))
log("edifici", sum(len(v) for v in per.values()))

# ---------- uscita principale
def r2(v): return round(v, 2) if isinstance(v, float) else v


core = {
    "meta": {"origin": [LON0, LAT0], "unit_km": 1 / U, "omi": f"{last[0]} {last[1]}", "pop_year": Y},
    "city": {"ring": enc_geom(city, 0.01, False), "area": round(cityA, 2), "inc": {k: r2(v) for k, v in CITY_INC.items()}, "metro_pop": round(CITY_METRO_POP, 1)},
    "nil": [{"id": n["id"], "n": n["n"], "a": round(n["a"], 3), "c": [round(n["g"].representative_point().x, 3), round(n["g"].representative_point().y, 3)],
             "rings": enc_geom(n["g"], 0.008, False, 0.001),
             "ind": {k: ({kk: r2(vv) for kk, vv in v.items()} if isinstance(v, dict) else r2(v)) for k, v in n["ind"].items()}} for n in nils],
    "cap": {c: {k: r2(v) for k, v in m.items()} for c, m in CAP.items()},
    "omi": [{"z": z["z"], "d": z["d"], "rent": r2(z.get("rent")), "price": r2(z.get("price")), "rings": enc_geom(z["g"], 0.01, False)} for z in zones],
    "metro": {"st": st, "lines": lines},
    "hex": {"r": R, "keys": list(HK), "cells": hex_cells},
}
json.dump(core, open("out/core.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
log("core.json", os.path.getsize("out/core.json") // 1024, "KB")
m = next(n for n in nils if n["id"] == 1)
log("esempio", m["n"], {k: v for k, v in m["ind"].items() if not isinstance(v, dict)})
