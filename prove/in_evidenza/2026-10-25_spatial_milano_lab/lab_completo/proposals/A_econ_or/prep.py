"""Step 0 - derived inputs for the A_econ_or model (read-only on mi/, istat_samples/).

Outputs (results/cache/):
  nil_hh.csv     households by size per NIL (Census 2021 sections, PF3..PF8) scaled to 2025 population
  cap_classes.csv MEF IRPEF 2024 class frequencies/amounts per CAP (reddito complessivo) + taxes
  cap_nil_w.csv  CAP x NIL address counts from OSM addr:postcode (same rule as mi/build_mi.py)
Run: PYTHONPATH=C:/Temp/pl python lab/proposals/A_econ_or/prep.py
"""
import collections, csv, io, json, os, sys, time
import numpy as np, pandas as pd, shapely, shapefile, openpyxl
from pyproj import Transformer
from shapely.geometry import Point, Polygon, shape
from shapely.strtree import STRtree

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CACHE = os.path.join(HERE, "results", "cache"); os.makedirs(CACHE, exist_ok=True)
log = lambda *a: print(f"[{time.time() - T0:6.1f}s]", *a, file=sys.stderr, flush=True)
LON0, LAT0 = 9.19, 45.465
KX, KY = 111.32 * np.cos(np.radians(LAT0)), 110.57

core = json.load(open(os.path.join(ROOT, "mi", "out", "core.json"), encoding="utf-8"))
UC = core["meta"]["unit_km"]


def poly(a, u):
    xy = np.cumsum(np.asarray(a, dtype=np.int64).reshape(-1, 2), axis=0) * u
    g = Polygon(xy)
    return g if g.is_valid else g.buffer(0)


NIL_ID = [n["id"] for n in core["nil"]]
NG = [shapely.union_all([poly(r, UC) for r in n["rings"]]) for n in core["nil"]]
tree = STRtree(NG)


def nil_at(x, y):
    p = Point(x, y)
    for i in tree.query(p):
        if NG[i].contains(p): return NIL_ID[i]
    # nearest NIL fallback (section centroids on borders)
    return NIL_ID[int(np.argmin([g.distance(p) for g in NG]))]


# ---------------------------------------------------------------- census 2021 households by size
wb = openpyxl.load_workbook(os.path.join(ROOT, "istat_samples", "census_dl", "R03_indicatori_2021_sezioni.xlsx"), read_only=True)
rows = wb[wb.sheetnames[0]].iter_rows(values_only=True)
h = next(rows); K = ("P1", "PF1", "PF3", "PF4", "PF5", "PF6", "PF7", "PF8")
ix = {k: h.index(k) for k in ("SEZ21_ID", "PROCOM") + K}
sec = {}
for r in rows:
    if r[ix["PROCOM"]] in (15146, "15146", "015146"):
        sec[int(r[ix["SEZ21_ID"]])] = [float(r[ix[k]] or 0) for k in K]
log("census sections Milano", len(sec))
UTM = Transformer.from_crs(32632, 4326, always_xy=True)
acc = collections.defaultdict(lambda: np.zeros(len(K)))
for sr in shapefile.Reader(os.path.join(ROOT, "istat_samples", "sezioni", "x", "SHP", "R03_21_WGS84")).iterShapeRecords():
    d = sr.record.as_dict()
    if d["PRO_COM"] != 15146 or int(d["SEZ21_ID"]) not in sec: continue
    g = shape(sr.shape.__geo_interface__)
    if g.is_empty: continue
    c = g.representative_point(); lon, lat = UTM.transform(c.x, c.y)
    acc[nil_at((lon - LON0) * KX, -(lat - LAT0) * KY)] += sec[int(d["SEZ21_ID"])]
H = pd.DataFrame([[i] + list(acc[i]) for i in NIL_ID], columns=["nil_id", "pop21c"] + ["hh21", "s1", "s2", "s3", "s4", "s5", "s6"])
pop25 = {n["id"]: n["ind"].get("pop") for n in core["nil"]}
H["pop25"] = H.nil_id.map(pop25)
# households 2025 = anagrafe pop 2025 / census-2021 mean household size of the NIL (assumption: size structure
# constant 2021-25). Section->NIL by centroid misallocates border sections, so counts come from pop25, shares from census.
H["msize"] = H.pop21c / H.hh21.replace(0, np.nan)
H["hh25"] = np.where(H.pop25.notna() & H.msize.notna(), H.pop25 / H.msize, H.hh21)
H["name"] = [n["n"] for n in core["nil"]]
assert abs(H[["s1", "s2", "s3", "s4", "s5", "s6"]].sum(axis=1) - H.hh21).max() < 1, "PF3..PF8 must sum to PF1"
H.to_csv(os.path.join(CACHE, "nil_hh.csv"), index=False)
log("households 2021", int(H.hh21.sum()), "2025", int(H.hh25.sum()), "pop21 census", int(H.pop21c.sum()))

# ---------------------------------------------------------------- MEF IRPEF 2024 per CAP
t = open(os.path.join(ROOT, "mi", "raw", "redditi2024.csv"), "rb").read().decode("utf-8-sig")
capv = collections.defaultdict(dict)
for r in csv.reader(io.StringIO(t), delimiter=";"):
    if r[0] == "Anno di imposta": continue
    capv[r[1]][r[2]] = float(r[3].replace(",", ".") or 0)
CL = [("le0", "Reddito complessivo minore o uguale a zero euro"), ("0_10", "Reddito complessivo da 0 a 10000 euro"),
      ("10_15", "Reddito complessivo da 10000 a 15000 euro"), ("15_26", "Reddito complessivo da 15000 a 26000 euro"),
      ("26_55", "Reddito complessivo da 26000 a 55000 euro"), ("55_75", "Reddito complessivo da 55000 a 75000 euro"),
      ("75_120", "Reddito complessivo da 75000 a 120000 euro"), ("gt120", "Reddito complessivo oltre 120000 euro")]
out = []
for cap, v in sorted(capv.items()):
    row = {"cap": cap, "taxpayers": v.get("Numero contribuenti", 0)}
    for k, lab in CL:
        row["n_" + k] = v.get(lab + " - Frequenza", 0); row["a_" + k] = v.get(lab + " - Ammontare in euro", 0)
    row["emp_n"] = v.get("Reddito da lavoro dipendente e assimilati - Frequenza", 0)
    row["pens_n"] = v.get("Reddito da pensione - Frequenza", 0)
    row["tax_irpef"] = v.get("Imposta netta - Ammontare in euro", 0)
    row["tax_reg"] = v.get("Addizionale regionale dovuta - Ammontare in euro", 0)
    row["tax_com"] = v.get("Addizionale comunale dovuta - Ammontare in euro", 0)
    row["inc_tot"] = v.get("Reddito complessivo - Ammontare in euro", 0)
    row["rc_n"] = v.get("Reddito complessivo - Frequenza", 0)
    # MEF leaves '>120k' blank in some CAPs (statistical confidentiality): impute it as the residual of the
    # reddito-complessivo total (frequency and amount) minus the published classes.
    if not row["n_gt120"]:
        row["n_gt120"] = row["rc_n"] - sum(row["n_" + k] for k, _ in CL)
        row["a_gt120"] = row["inc_tot"] - sum(row["a_" + k] for k, _ in CL)
        row["gt120_imputed"] = True
    out.append(row)
C = pd.DataFrame(out)
C.to_csv(os.path.join(CACHE, "cap_classes.csv"), index=False)
log("CAP", len(C), "taxpayers", int(C.taxpayers.sum()))

# ---------------------------------------------------------------- CAP -> NIL weights (OSM addresses)
W = collections.Counter()
for e in json.load(open(os.path.join(ROOT, "mi", "raw", "osm_postcodes.json"), encoding="utf-8"))["elements"]:
    pc = str(e.get("tags", {}).get("addr:postcode", "")).strip()[:5]
    c = e.get("center") or e
    if pc not in capv or "lat" not in c: continue
    x, y = (c["lon"] - LON0) * KX, -(c["lat"] - LAT0) * KY
    p = Point(x, y)
    for i in tree.query(p):
        if NG[i].contains(p): W[(pc, NIL_ID[i])] += 1; break
pd.DataFrame([(c, n, w) for (c, n), w in W.items()], columns=["cap", "nil_id", "addr"]).to_csv(os.path.join(CACHE, "cap_nil_w.csv"), index=False)
log("CAP-NIL pairs", len(W), "addresses", sum(W.values()))
