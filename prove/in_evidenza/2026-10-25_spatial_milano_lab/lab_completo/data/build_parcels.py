"""Parcel-level analysis table for the whole Comune di Milano.

Inputs (read-only, mi/out/): t/*.json (cadastral parcels + DBT 2020 volumes), core.json (NIL, metro, census hex),
pgt.json, dusaf.json, tiles.json.
Outputs (lab/data/): parcels.csv.gz, nil.csv, parcels_schema.md (columns + stats + sanity checks).
Run from the project root:  PYTHONPATH=C:/Temp/pl python lab/data/build_parcels.py
Coordinates: local km, x east, y SOUTH (see lab/README.md)."""
import collections, glob, json, os, sys, time
import numpy as np, pandas as pd, shapely
from scipy.spatial import cKDTree
from shapely.geometry import Point, Polygon
from shapely.strtree import STRtree

T0 = time.time()
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MI, OUT = os.path.join(ROOT, "mi", "out"), os.path.join(ROOT, "lab", "data")
log = lambda *a: print(f"[{time.time() - T0:6.1f}s]", *a, file=sys.stderr, flush=True)
load = lambda f: json.load(open(os.path.join(MI, f), encoding="utf-8"))


def dec(a, u):
    """Delta-decoded flat int list -> [(x, y)] km. Each geometry restarts from 0 (first pair is absolute)."""
    xy = np.cumsum(np.asarray(a, dtype=np.int64).reshape(-1, 2), axis=0) * u
    return xy


def poly(a, u):
    if len(a) < 6: return None
    g = Polygon(dec(a, u))
    if not g.is_valid: g = g.buffer(0)
    if g.is_empty: return None
    return g if g.geom_type == "Polygon" else max(g.geoms, key=lambda q: q.area)


def rings_to_geom(rings, u):
    """Overlay layers store shells and holes as a flat list of rings (build_mi.enc_geom).
    Rebuild with even-odd nesting: ring depth = number of other rings containing it; odd depth = hole."""
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


# ---------------------------------------------------------------- core / NIL
core = load("core.json"); UC = core["meta"]["unit_km"]
nil_ids = [n["id"] for n in core["nil"]]
nil_geoms = [shapely.union_all([poly(r, UC) for r in n["rings"]]) for n in core["nil"]]
city = poly(core["city"]["ring"][0], UC)
assert len(nil_ids) == 88, len(nil_ids)
log("NIL", len(nil_ids), "city area km2", round(city.area, 2), "NIL union km2", round(shapely.union_all(nil_geoms).area, 2))

# ---------------------------------------------------------------- tiles: parcels + volumes
tile_files = sorted(glob.glob(os.path.join(MI, "t", "*.json")))
P, V = {}, []  # P: ref -> dict ; V: list of volumes
dup = 0
for f in tile_files:
    t = json.load(open(f)); u = t["u"]
    for rec in t["p"]:
        ref, a, cov, iv = rec[:4]; g = poly(rec[4:], u)
        if g is None: continue
        if ref in P:  # dedupe by ref: keep the larger record
            dup += 1
            if P[ref]["area_m2"] >= a: continue
        P[ref] = {"ref": ref, "area_m2": a, "src_cov": cov, "src_vi": iv, "g": g, "tile": os.path.basename(f)[:-5]}
    for rec in t["v"]:
        h, uso, q, ref = rec[:4]; g = poly(rec[4:], u)
        if g is not None: V.append((h, uso, ref, g))
# Catasto repeats identical road/water polygons under several refs (e.g. 011000.STRADA005/006/022/046):
# collapse exact geometric duplicates (same area_m2 + same ring), keep the first ref, remap the others.
alias, seen_g = {}, {}
for r in sorted(P):
    key = (P[r]["area_m2"], P[r]["g"].wkb)
    if key in seen_g: alias[r] = seen_g[key]; P[seen_g[key]]["dup_refs"] = P[seen_g[key]].get("dup_refs", 0) + 1
    else: seen_g[key] = r
for r in alias: del P[r]
refs = list(P); pg = np.array([P[r]["g"] for r in refs], dtype=object)
ref_idx = {r: i for i, r in enumerate(refs)}
ref_idx.update({r: ref_idx[k] for r, k in alias.items()})
log("geometric duplicates collapsed", len(alias))
log("tiles", len(tile_files), "parcels", len(refs), "dup refs dropped", dup, "volumes", len(V))

# ---------------------------------------------------------------- volumes -> parcels
ptree = STRtree(pg)
vg = np.array([v[3] for v in V], dtype=object)
vpar = np.array([ref_idx.get(v[2], -1) for v in V])
link_ref = int((vpar >= 0).sum())
miss = np.where(vpar < 0)[0]
if len(miss):  # fallback: representative point inside a parcel
    pts = shapely.point_on_surface(vg[miss])
    vi, pj = ptree.query(pts, predicate="within")
    vpar[miss[vi]] = pj  # if several parcels contain the point (overlaps), the last wins
link_pt = int((vpar >= 0).sum()) - link_ref
log("volumes linked by ref", link_ref, "by point", link_pt, "unlinked", int((vpar < 0).sum()))
USES = load("tiles.json")["uses"]
vh = np.array([v[0] for v in V]); vu = np.array([v[1] for v in V]); va = shapely.area(vg) * 1e6
n = len(refs); ok = vpar >= 0
built = np.bincount(vpar[ok], va[ok], n); vol = np.bincount(vpar[ok], va[ok] * vh[ok], n); nv = np.bincount(vpar[ok], minlength=n)
hmax = np.zeros(n); np.maximum.at(hmax, vpar[ok], vh[ok])
use_vol = np.zeros((n, len(USES))); np.add.at(use_vol, (vpar[ok], vu[ok]), va[ok] * vh[ok])

# ---------------------------------------------------------------- base table
cent = shapely.point_on_surface(pg)  # point-on-surface: always inside the parcel (centroid may fall outside L-shapes)
cx, cy = shapely.get_x(cent), shapely.get_y(cent)
garea = shapely.area(pg) * 1e6
D = pd.DataFrame({"ref": refs, "tile": [P[r]["tile"] for r in refs], "x": cx.round(4), "y": cy.round(4),
                  "area_m2": [P[r]["area_m2"] for r in refs], "geom_area_m2": garea.round(1)})
D["built_m2"] = built.round(1); D["coverage"] = np.minimum(1, built / D.area_m2).round(4)
D["volume_m3"] = vol.round(0); D["n_vol"] = nv
D["h_max"] = np.where(nv > 0, hmax, np.nan)
D["h_mean"] = np.where(built > 0, vol / np.maximum(built, 1e-9), np.nan).round(2)  # footprint-weighted
dom = use_vol.argmax(1)
D["use_dom"] = np.where(nv > 0, np.array(USES, dtype=object)[dom], "")
D["use_dom_share"] = np.where(vol > 0, use_vol.max(1) / np.maximum(vol, 1e-9), np.nan).round(3)
D["use_res_share"] = np.where(vol > 0, use_vol[:, 0] / np.maximum(vol, 1e-9), np.nan).round(3)
D["src_cov"] = [P[r]["src_cov"] for r in refs]; D["src_vi"] = [P[r]["src_vi"] for r in refs]
D["dup_refs"] = [P[r].get("dup_refs", 0) for r in refs]
D["ref_numeric"] = [r.split(".")[-1].isdigit() for r in refs]
D["kind"] = ["land" if r.split(".")[-1].isdigit() else "road" if "STRADA" in r else "water" if "ACQUA" in r else "letter" for r in refs]

# ---------------------------------------------------------------- NIL (point in polygon, nearest as fallback)
ntree = STRtree(nil_geoms)
pi, ni = ntree.query(cent, predicate="within")
nil_of = np.full(n, -1); nil_of[pi] = ni
out = np.where(nil_of < 0)[0]
D["nil_fallback"] = False
if len(out):
    nearest = ntree.query_nearest(cent[out], return_distance=True, all_matches=False)
    nil_of[out[nearest[0][0]]] = nearest[0][1]; D.loc[out, "nil_fallback"] = True
    D.loc[out, "nil_fallback_dist_m"] = (nearest[1] * 1000).round(1)
D["nil_id"] = np.array(nil_ids)[nil_of]
D["nil_name"] = np.array([nn["n"] for nn in core["nil"]], dtype=object)[nil_of]
D["outside_city"] = ~shapely.within(cent, city)
log("NIL assigned; fallback", len(out))

# ---------------------------------------------------------------- overlays (share of parcel area)
def overlay_share(parts, name):
    if not parts: return np.zeros(n)
    parts = np.array(parts, dtype=object); shapely.prepare(parts)
    tree = STRtree(parts)
    i, j = tree.query(pg, predicate="intersects")
    inside = shapely.contains_properly(parts[j], pg[i])
    a = np.where(inside, shapely.area(pg[i]), 0.0)
    cut = ~inside
    a[cut] = shapely.area(shapely.intersection(pg[i[cut]], parts[j[cut]], grid_size=1e-6))
    s = np.bincount(i, a, n) / garea * 1e6
    return np.clip(s, 0, 1)

layer_geoms = {}
for lay, fname in (("pgt", "pgt.json"), ("dusaf", "dusaf.json")):
    L = load(fname)
    for c in L["cats"]:
        parts = rings_to_geom(c["p"], UC); layer_geoms[(lay, c["k"])] = parts
        D[f"{lay}_{c['k']}"] = overlay_share(parts, c["k"]).round(3)
        tot = L["totals"].get(c["k"]); got = sum(p.area for p in parts)
        log(f"{lay}_{c['k']}: parts {len(parts)} area {got:.3f} km2 (source total {tot})")
D["dusaf_sum"] = D[[c for c in D if c.startswith("dusaf_") and c != "dusaf_sum"]].sum(axis=1).round(3)

# ---------------------------------------------------------------- accessibility
st = core["metro"]["st"]
st_xy = {}
for s in st: st_xy.setdefault(s["n"], (s["x"], s["y"]))  # interchanges listed once per line -> one point per name
sxy = np.array(list(st_xy.values()))
kd = cKDTree(sxy); P2 = np.column_stack([cx, cy])
d, k = kd.query(P2)
D["metro_km"] = d.round(3); D["metro_nearest"] = np.array(list(st_xy), dtype=object)[k]
D["metro_n800"] = [len(z) for z in kd.query_ball_point(P2, 0.8)]
vparts = np.array(layer_geoms[("pgt", "srv_verde")], dtype=object)
vt = STRtree(vparts); (ia, ja), dd = vt.query_nearest(cent, return_distance=True, all_matches=False)
gv = np.full(n, np.nan); gv[ia] = dd; D["green_srv_km"] = gv.round(3)  # 0 = point inside a srv_verde polygon

# ---------------------------------------------------------------- census hex (nearest cell)
H = core["hex"]; hc = np.array(H["cells"], dtype=float)
hd, hk = cKDTree(hc[:, :2]).query(P2)
for j, key in enumerate(H["keys"]): D[f"hex_{key}"] = hc[hk, 2 + j].astype(int)
D["hex_dist_km"] = hd.round(3)
D["hex_far"] = hd > H["r"]  # parcel farther than one cell radius from any populated cell centre

# ---------------------------------------------------------------- NIL context
NCOLS = ["rent", "price", "net_m", "wage_m", "inc", "poor", "rich", "dens", "a65", "for_", "green", "heatrisk", "heatexp", "metro_pop"]
nil_ind = {nn["id"]: nn["ind"] for nn in core["nil"]}
for c in NCOLS: D[f"nil_{c}"] = [nil_ind[i].get(c, np.nan) for i in D.nil_id]

# ---------------------------------------------------------------- soft-site proxy (ASSUMPTION)
STOREY = 3.2
D["gfa_m2"] = (D.volume_m3 / STOREY).round(0)
D["far"] = (D.gfa_m2 / D.area_m2).round(3)
ref_mask = (D.area_m2 >= 200) & (D.n_vol > 0) & (D.kind == "land")  # built parcels of non-trivial size define the "local norm"
p75 = D[ref_mask].groupby("nil_id")["far"].quantile(0.75)
D["far_nil_p75"] = D.nil_id.map(p75).round(3)
D["far_ratio"] = (D.far / D.far_nil_p75).round(3)
D["gfa_headroom_m2"] = ((D.far_nil_p75 - D.far).clip(lower=0) * D.area_m2).round(0)
PROT = ["pgt_srv_verde", "pgt_agr", "pgt_pae", "dusaf_wat", "dusaf_infra", "dusaf_green", "dusaf_agr", "dusaf_wood"]
protected = D[PROT].max(axis=1) >= 0.5
D["soft_site"] = (D.far_ratio < 0.5) & (D.area_m2 >= 500) & ~protected & D.ref_numeric
log("soft sites", int(D.soft_site.sum()))

# ---------------------------------------------------------------- self-checks
assert D.ref.is_unique
assert D.nil_id.notna().all()
for c in [c for c in D if c.startswith(("pgt_", "dusaf_")) and c != "dusaf_sum"]: assert D[c].between(0, 1).all(), c
assert (D.coverage.between(0, 1)).all()
assert abs(len(V) - 231000) < 20000 and abs(n - 120000) < 20000, (len(V), n)

# ---------------------------------------------------------------- sanity checks
S = []
add = lambda k, v: S.append((k, v))
city_a = 181.7
union_a = shapely.union_all(pg).area
land = (D.kind == "land").to_numpy(); union_land = shapely.union_all(pg[land]).area
add("parcels (rows)", f"{n:,}")
add("volumes decoded / linked by ref / by point / unlinked", f"{len(V):,} / {link_ref:,} / {link_pt:,} / {int((vpar < 0).sum()):,}")
add("sum parcel area_m2 (km²) vs city 181.7", f"{D.area_m2.sum() / 1e6:.2f} ({D.area_m2.sum() / 1e6 / city_a:.1%})")
add("union of decoded parcel geoms (km²); overlap = sum - union", f"{union_a:.2f}; overlap {garea.sum() / 1e6 - union_a:.3f}")
add("land parcels only: n / Σ area_m2 (km²) / overlap = sum − union (km²)", f"{land.sum():,} / {D.area_m2[land].sum() / 1e6:.2f} / {garea[land].sum() / 1e6 - union_land:.3f}")
add("by kind: n (Σ area km²)", ", ".join(f"{k} {g.size:,} ({g.sum() / 1e6:.2f})" for k, g in D.groupby("kind").area_m2))
add("geometric duplicate refs collapsed", f"{len(alias):,}")
add("decoded geom area / declared area_m2 (median, p1, p99)", "{:.3f}, {:.3f}, {:.3f}".format(*np.nanquantile(garea / D.area_m2, [.5, .01, .99])))
add("share of parcels with ≥1 volume", f"{(D.n_vol > 0).mean():.1%}")
add("built footprint total (km²) / city coverage", f"{D.built_m2.sum() / 1e6:.2f} / {D.built_m2.sum() / 1e6 / city_a:.1%}")
add("|coverage − source cov| > 0.05 (share of parcels)", f"{((D.coverage - D.src_cov).abs() > 0.05).mean():.2%}")
add("|volume/area − source vol index| > 10% (built parcels)", f"{((D.volume_m3 / D.area_m2 - D.src_vi).abs() > 0.1 * D.src_vi.clip(lower=1))[D.n_vol > 0].mean():.2%}")
add("parcel centroid outside NIL union (nearest-NIL fallback)", f"{D.nil_fallback.sum():,}")
add("parcel centroid outside city ring", f"{D.outside_city.sum():,}")
add("NIL with ≥1 parcel", f"{D.nil_id.nunique()} / 88")
add("non-numeric refs (roads/waters/letters)", f"{(~D.ref_numeric).sum():,}")
add("dusaf_sum (share covered by any DUSAF class) median / p5", f"{D.dusaf_sum.median():.3f} / {D.dusaf_sum.quantile(.05):.3f}")
add("metro stations (unique names) used", f"{len(sxy)} (of {len(st)} listed)")
add("parcels with h_max > 100 m", f"{(D.h_max > 100).sum():,}")
add("parcels with far > 10", f"{(D.far > 10).sum():,}")
add("soft_site = True", f"{D.soft_site.sum():,} parcels, {D[D.soft_site].area_m2.sum() / 1e6:.2f} km²")
for k, v in S: log("CHECK", k, "=", v)

# ---------------------------------------------------------------- write outputs
D.to_csv(os.path.join(OUT, "parcels.csv.gz"), index=False, compression="gzip")
T = load("tiles.json")["nil"]
rows = []
for nn in core["nil"]:
    r = {"nil_id": nn["id"], "nil_name": nn["n"], "area_km2": nn["a"], "cx": nn["c"][0], "cy": nn["c"][1]}
    for k, v in nn["ind"].items():
        if isinstance(v, dict): r.update({f"{k}_{kk}": vv for kk, vv in v.items()})
        elif isinstance(v, list): r[k] = ";".join(map(str, v))
        else: r[k] = v
    r.update(T.get(str(nn["id"]), {}))
    g = D[D.nil_id == nn["id"]]
    r.update({"parcels_n": len(g), "parcels_area_km2": round(g.area_m2.sum() / 1e6, 3), "far_p75": p75.get(nn["id"], np.nan), "soft_sites_n": int(g.soft_site.sum())})
    rows.append(r)
N = pd.DataFrame(rows)
for c in [c for c in N if c.startswith(("pgt_", "dusaf_"))]: N[c] = N[c].fillna(0)  # missing key = 0 % of area
N.to_csv(os.path.join(OUT, "nil.csv"), index=False)
log("nil.csv", N.shape)

# ---------------------------------------------------------------- schema doc
PG = {c["k"]: c["l"] for c in load("pgt.json")["cats"]}; DU = {c["k"]: c["l"] for c in load("dusaf.json")["cats"]}
DOC = {
    "ref": ("—", "Cadastral parcel id `foglio.particella` (tile prefix stripped by mi/build_dbt.py). Unique (deduped across tiles, larger record kept)."),
    "tile": ("—", "Source tile `tx_ty` (2 km grid)."),
    "x": ("km", "Point-on-surface of the decoded parcel polygon, local x (east)."),
    "y": ("km", "Point-on-surface, local y (**south** positive)."),
    "area_m2": ("m²", "Declared parcel area from tile (exact geometry area before simplification)."),
    "geom_area_m2": ("m²", "Area of decoded (simplified 0.8 m, 0.5 m grid) polygon; denominator of overlay shares."),
    "built_m2": ("m²", "Sum of DBT 2020 volume footprints linked to the parcel (decoded polygons)."),
    "coverage": ("0-1", "built_m2 / area_m2, capped at 1."),
    "volume_m3": ("m³", "Σ footprint × height (UN_VOL_AV, above-ground units only)."),
    "n_vol": ("count", "Number of DBT volumetric units linked."),
    "h_max": ("m", "Max height of linked volumes (NaN if none)."),
    "h_mean": ("m", "Footprint-weighted mean height = volume_m3 / built_m2."),
    "use_dom": ("cat", "Dominant DBT use (volume-weighted) among: " + ", ".join(USES) + ". Empty if no volumes."),
    "use_dom_share": ("0-1", "Volume share of the dominant use."),
    "use_res_share": ("0-1", "Volume share of Residenziale."),
    "src_cov": ("0-1", "Coverage precomputed in tile (mi/build_dbt.py, exact geometries) — kept for cross-check."),
    "src_vi": ("m³/m²", "Volumetric index precomputed in tile — cross-check."),
    "dup_refs": ("count", "Extra refs with an identical polygon collapsed into this row (catasto repeats road/water polygons)."),
    "kind": ("cat", "land = numeric particella; road = STRADA*; water = ACQUA*; letter = other lettered refs (common areas)."),
    "ref_numeric": ("bool", "Particella part is numeric. False = letter refs (typically roads, waters, common areas)."),
    "nil_fallback": ("bool", "Centroid not inside any NIL ring (0.01 km precision); NIL = nearest."),
    "nil_fallback_dist_m": ("m", "Distance to the nearest NIL for fallback rows."),
    "nil_id": ("id", "NIL (Nucleo d'Identità Locale) containing the point-on-surface (core.json)."),
    "nil_name": ("—", "NIL name."),
    "outside_city": ("bool", "Point-on-surface outside the city ring in core.json."),
    "dusaf_sum": ("0-1", "Σ DUSAF shares; < 1 where DUSAF polygons (simplified, min area 400 m²) leave gaps."),
    "metro_km": ("km", "Euclidean distance to nearest metro station (130 entries, deduped by name)."),
    "metro_nearest": ("—", "Name of that station."),
    "metro_n800": ("count", "Distinct metro stations within 800 m (Euclidean)."),
    "green_srv_km": ("km", "Distance from point-on-surface to nearest PGT srv_verde polygon (0 = inside)."),
    "hex_dist_km": ("km", "Distance to nearest census-2021 hex centre (r = 0.25 km)."),
    "hex_far": ("bool", "hex_dist_km > 0.25: parcel not covered by a populated cell; hex_* are a distant neighbour's values."),
    "gfa_m2": ("m²", "**Assumption**: gross floor area proxy = volume_m3 / 3.2 m storey height."),
    "far": ("m²/m²", "**Assumption**: floor area ratio proxy = gfa_m2 / area_m2."),
    "far_nil_p75": ("m²/m²", "**Assumption**: 75th percentile of `far` in the NIL, among land parcels ≥ 200 m² with ≥ 1 volume. Stand-in for the PGT base index (Indice di Edificabilità Territoriale), which is NOT available."),
    "far_ratio": ("ratio", "far / far_nil_p75. < 1 = built below the local norm."),
    "gfa_headroom_m2": ("m²", "**Assumption**: max(0, far_nil_p75 − far) × area_m2 — notional floor area to reach the local p75. Not a legal entitlement."),
    "soft_site": ("bool", "**Assumption**: far_ratio < 0.5 AND area_m2 ≥ 500 AND ref_numeric AND < 50 % in each of " + "/".join(PROT) + ". Includes vacant parcels (n_vol = 0). Screening flag only; ignores ownership, heritage, constraints, actual zoning."),
}
for k, l in PG.items(): DOC[f"pgt_{k}"] = ("0-1", f"Share of parcel geom area inside PGT 2030 layer '{l}' (pgt.json, 0.01 km grid, simplified 6 m).")
for k, l in DU.items(): DOC[f"dusaf_{k}"] = ("0-1", f"Share of parcel geom area inside DUSAF class '{l}' (dusaf.json, 0.01 km grid, simplified 6 m).")
for k in H["keys"]: DOC[f"hex_{k}"] = ("count", f"Census 2021 `{k}` of the nearest hex cell (core.json hex; pop=residents, emp=employed, for=foreigners, deg=tertiary-educated, dw=dwellings).")
NDOC = {"rent": "OMI 2024/2 rent €/m² month", "price": "OMI price €/m²", "net_m": "estimated net income €/month per taxpayer", "wage_m": "employee taxable wage €/month",
        "inc": "mean total income per taxpayer €/yr (IRPEF 2024)", "poor": "% taxpayers ≤ 15k", "rich": "% taxpayers > 75k", "dens": "residents per km² (2025)",
        "a65": "% aged 65+", "for_": "% foreign residents", "green": "green index", "heatrisk": "heat-risk index", "heatexp": "heat-exposure index", "metro_pop": "% residents within 500 m of metro"}
for k, v in NDOC.items(): DOC[f"nil_{k}"] = ("NIL", f"Copied from the parcel's NIL (core.json ind.{k}): {v}. NaN where the NIL lacks it.")

md = ["# parcels.csv.gz — schema, statistics, sanity checks", "",
      f"Generated by `lab/data/build_parcels.py` ({time.strftime('%Y-%m-%d %H:%M')}). One row per cadastral parcel, {n:,} rows × {D.shape[1]} columns. "
      "Read with `pd.read_csv('lab/data/parcels.csv.gz', dtype={'ref': str})`.", "",
      "Data status (lab rule 3): parcel/volume/overlay/census/NIL columns are **real data** (derived); `gfa_m2`, `far`, `far_nil_p75`, `far_ratio`, `gfa_headroom_m2`, `soft_site` are **assumption-based proxies**.", "",
      "## Columns", "", "| column | unit | description |", "|---|---|---|"]
for c in D.columns: u_, d_ = DOC.get(c, ("", "")); md.append(f"| `{c}` | {u_} | {d_} |")
md += ["", "## Geometry handling", "",
       "- Tiles: delta-encoded rings, unit `u` = 0.0005 km per tile; each geometry restarts accumulation from 0. Decoded with `cumsum`; invalid rings repaired with `buffer(0)`, largest part kept.",
       "- PGT/DUSAF: unit 0.01 km (10 m grid), simplified at 6 m, parts < 400 m² and holes < 100 m² dropped upstream. Shells and holes are a flat ring list; rebuilt by even-odd nesting depth. "
       "Shares are therefore accurate to roughly ±10 m at polygon edges — treat small shares (< 0.1) on small parcels as noise.",
       "- NIL: point-on-surface of parcel in NIL rings (0.01 km grid); nearest NIL if outside any ring.",
       "- Volumes link to parcels via `ref` (assigned upstream by representative point of the exact footprint); unreferenced ones via point-on-surface-in-parcel. A volume straddling two parcels counts fully in one.",
       "- Distances are Euclidean in the local km frame (KX/KY scaling ≈ isotropic, error < 0.5 %).", "",
       "## Sanity checks", "", "| check | value |", "|---|---|"] + [f"| {k} | {v} |" for k, v in S]
num = D.select_dtypes("number")
q = num.quantile([0, .05, .25, .5, .75, .95, 1]).T
md += ["", "## Summary statistics (numeric)", "", "| column | non-null | mean | min | p5 | p25 | p50 | p75 | p95 | max |", "|---|---|---|---|---|---|---|---|---|---|"]
f_ = lambda v: "" if pd.isna(v) else f"{v:.4g}"
for c in num.columns: md.append(f"| `{c}` | {num[c].notna().sum():,} | {f_(num[c].mean())} | " + " | ".join(f_(v) for v in q.loc[c]) + " |")
md += ["", "## Categorical", "", "use_dom counts: " + ", ".join(f"{k or '(none)'} {v:,}" for k, v in D.use_dom.value_counts().items()), "",
       "## Known data problems", "",
       "- No PGT base index (IT), ownership, listed-building or constraint layers: `soft_site` is a screening proxy only.",
       "- Storey height 3.2 m is a single assumption for all uses; industrial/commercial sheds inflate GFA.",
       "- DBT 2020 heights (UN_VOL_AV) of above-ground units; underground units dropped upstream; heights capped at 260 m upstream.",
       "- Catasto includes road (STRADA) and water (ACQUA) polygons, some repeated under several refs (collapsed, see `dup_refs`); they overlap land parcels, so Σ area ≠ city area. Filter `kind == 'land'` for lot analysis.",
       "- ~8 % of DBT volumes have no parcel (empty `ref` upstream, point not inside any parcel): mostly on road/rail land or catasto gaps; not counted in any parcel.",
       "- NIL 40 Ronchetto delle Rane (0.19 km²) receives no parcel point-on-surface.",
       "- Overlay layers are generalised (10 m grid); NIL context is an ecological (area) attribute, identical for all parcels in a NIL.",
       "- Census hex holds only populated cells; parcels in parks/industrial zones get a distant cell (`hex_far`).",
       "- 5 NIL lack demographics (pop/dens/a65/for_…) and 1 lacks rent/price → NaN in `nil_*`.",
       "", "## nil.csv", "", f"{len(N)} rows × {N.shape[1]} columns: all `core.json` `ind` fields flattened (`dusaf_*`, `pgt_*` = % of NIL area, missing = 0; `cap` joined by `;`), "
       "plus tiles.json DBT aggregates (`dbt_h` median height m, `dbt_cov` % coverage, `dbt_vol` m³/m², `dbt_n`, `lot_n`, `lot_a` m², `dbt_tall` n ≥ 30 m) and from this script `parcels_n`, `parcels_area_km2`, `far_p75`, `soft_sites_n`."]
open(os.path.join(OUT, "parcels_schema.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
log("done", D.shape)
