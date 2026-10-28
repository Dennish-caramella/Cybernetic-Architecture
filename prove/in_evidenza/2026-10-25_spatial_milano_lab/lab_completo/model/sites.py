"""Step 1-2: parcels -> candidate parcels (shared filter, review1 §5.2) -> adjacency sites.
Sites never mix origins (AT / AMB_DEG / ERP / SOFT), so the audit can compare designated and non-designated land."""
import json, os
import numpy as np, pandas as pd, shapely
from shapely.geometry import shape
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from sklearn.cluster import KMeans
from config import *
A_PF = load_prop("A_econ_or", "portfolio")
from common import poly as c_poly, from_lonlat   # C's tile decoder

WAVG = ["metro_km", "nil_heatrisk", "nil_rent", "nil_net_m", "nil_poor", "nil_for_", "pgt_rig", "pgt_srv_erp", "pgt_tras",
        "far_ratio", "coverage"]


def _to_km(g):
    return shapely.transform(g, lambda c: np.column_stack(from_lonlat(c[:, 0], c[:, 1])))


def designation_layers():
    F = json.load(open(os.path.join(MI, "raw", "pgt_ambiti_trasformazione.geojson"), encoding="utf-8"))["features"]
    at = [(f["properties"]["NOME_AMB"], _to_km(shape(f["geometry"])).buffer(0)) for f in F if "PCU" not in (f["properties"].get("NOME_AMB") or "")]
    G = json.load(open(os.path.join(MI, "raw", "pgt_aree_dismesse.geojson"), encoding="utf-8"))["features"]
    deg = shapely.union_all([_to_km(shape(f["geometry"])).buffer(0) for f in G if str(f["properties"].get("NOTE", "")).startswith("ex AMB_DEG")])
    return at, deg


def candidate_parcels(P=None):
    """Shared filter. Returns candidate land parcels with `origin` and `at_name`, plus counts per exclusion."""
    P = pd.read_csv(os.path.join(LAB, "data", "parcels.csv.gz"), dtype={"ref": str}) if P is None else P
    L = P[(P.kind == "land") & ~P.outside_city].copy()
    x, y = L.x.values, L.y.values
    L["pcu"] = A_PF.pcu_mask(x, y)
    at, deg = designation_layers()
    L["at_name"] = None
    for n, g in at:
        m = shapely.contains_xy(g, x, y); L.loc[m, "at_name"] = n
    L["amb_deg"] = shapely.contains_xy(deg, x, y)
    s = SITE["plan_share"]
    is_at = (L.pgt_tras >= s) & ~L.pcu
    is_erp = L.pgt_srv_erp >= s
    excl = (L[SITE["excl_cols"]] >= SITE["excl_share"]).any(axis=1)
    occ = (L.n_vol > 0) & (L.use_res_share.fillna(0) >= SITE["occ_res_share"])
    entry = L.soft_site | is_at | is_erp | L.amb_deg
    keep = (L.area_m2 >= SITE["a_min_parcel"]) & ~excl & ~L.pcu & ~occ & entry
    counts = dict(land=len(L), small=int((L.area_m2 < SITE["a_min_parcel"]).sum()), green_agri_excl=int(excl.sum()),
                  pcu=int(L.pcu.sum()), occupied_housing=int(occ.sum()), no_entry=int((~entry).sum()), kept=int(keep.sum()))
    L["origin"] = np.select([is_at, L.amb_deg, is_erp], ["AT", "AMB_DEG", "ERP"], "SOFT")
    L.loc[L.origin != "AT", "at_name"] = None
    C = L[keep].reset_index(drop=True)
    C["nil_price"] = C.nil_price.fillna(C.nil_price.median())                 # [A] 1 NIL lacks OMI price
    for c in ("nil_rent", "nil_net_m", "nil_poor", "nil_for_", "nil_heatrisk"): C[c] = C[c].fillna(C[c].median())
    return C, counts


def decode_geoms(C):
    """Parcel polygons (km) from mi/out/t tiles."""
    out = {}
    for t, grp in C.groupby("tile"):
        T = json.load(open(os.path.join(MI, "out", "t", t + ".json"))); u = T["u"]; want = set(grp.ref)
        for rec in T["p"]:
            r = rec[0]
            if r in want:
                g = c_poly(rec[4:], u)
                if g is not None and (r not in out or g.area > out[r].area): out[r] = g
    g = [out.get(r) for r in C.ref]
    # fallback: square of the declared area around the point (rare: undecodable ring)
    return np.array([gi if gi is not None else shapely.box(x - (a ** .5) / 2e3, y - (a ** .5) / 2e3, x + (a ** .5) / 2e3, y + (a ** .5) / 2e3)
                     for gi, x, y, a in zip(g, C.x, C.y, C.area_m2)], dtype=object)


def build_sites(C, geoms, buffer_m=None, seed=0):
    """Adjacency aggregation within each origin class. Returns (parcel->site index array, sites DataFrame, site geoms)."""
    buffer_m = SITE["buffer_m"] if buffer_m is None else buffer_m
    gb = shapely.buffer(geoms, buffer_m / 1000.0) if buffer_m > 0 else geoms
    tree = shapely.STRtree(gb)
    a, b = tree.query(gb, predicate="intersects")
    org = C.origin.values
    m = (a < b) & (org[a] == org[b])
    n = len(C)
    _, comp = connected_components(coo_matrix((np.ones(m.sum()), (a[m], b[m])), shape=(n, n)), directed=False)
    area = C.area_m2.values
    lab = comp.copy(); nxt = comp.max() + 1
    carea = np.bincount(comp, area)
    for c in np.where(carea > SITE["max_area_m2"])[0]:
        idx = np.where(comp == c)[0]; k = int(np.ceil(carea[c] / SITE["max_area_m2"]))
        if len(idx) <= 1: continue
        k = min(k, len(idx))
        km = KMeans(k, n_init=4, random_state=seed).fit(np.c_[C.x.values[idx], C.y.values[idx]], sample_weight=area[idx])
        lab[idx] = nxt + km.labels_; nxt += k
    _, lab = np.unique(lab, return_inverse=True)
    sarea = np.bincount(lab, area)
    ok = sarea >= SITE["site_min_m2"]
    keepmap = -np.ones(len(sarea), int); keepmap[ok] = np.arange(ok.sum())
    psite = keepmap[lab]                                          # -1 = parcel dropped (site too small)
    S = site_table(C, psite, geoms)
    return psite, S


def site_table(C, psite, geoms):
    m = psite >= 0; D = C[m].copy(); D["site"] = psite[m]; g = geoms[m]
    w = D.area_m2
    agg = {c: (D[c] * w).groupby(D.site).sum() / w.groupby(D.site).sum() for c in WAVG}
    S = pd.DataFrame(agg)
    S["area_m2"] = w.groupby(D.site).sum()
    S["n_parcels"] = D.groupby("site").size()
    S["volume_m3"] = D.groupby("site").volume_m3.sum()
    S["origin"] = D.groupby("site").origin.first()
    S["at_name"] = D.groupby("site").at_name.agg(lambda v: v.dropna().mode().iloc[0] if v.notna().any() else None)
    S["nil_id"] = D.loc[D.groupby("site").area_m2.idxmax(), ["site", "nil_id"]].set_index("site").nil_id
    S["nil_price"] = (D.nil_price * w).groupby(D.site).sum() / w.groupby(D.site).sum()
    S["soft_share"] = (D.soft_site * w).groupby(D.site).sum() / w.groupby(D.site).sum()
    S["geom"] = pd.Series(list(g), index=D.index).groupby(D.site).agg(lambda v: shapely.union_all(list(v)))
    S["x"] = [q.centroid.x for q in S.geom]; S["y"] = [q.centroid.y for q in S.geom]
    S = S.sort_index().reset_index(drop=True)
    return add_capacity_cost(S)


def add_capacity_cost(S, far=None):
    far = SUP["far"] if far is None else far
    S = S.copy()
    S["public"] = S.origin.eq("ERP")                                # [A] srv_erp land treated as municipal (A)
    S["cap"] = np.minimum(np.floor(SUP["yield_"] * far * S.area_m2 / SUP["gfa_dw"]), SUP["m_max"])
    gfa = S.cap * SUP["gfa_dw"]
    S["fixed_eur"] = np.where(S.public, S.area_m2 * 1.0, SUP["land_inc"] * S.nil_price * gfa) + SUP["c_demo"] * S.volume_m3
    S["var_eur"] = SUP["c_build"] * SUP["gfa_dw"]
    S["cost_per_dw"] = S.fixed_eur / np.maximum(S.cap, 1) + S.var_eur
    return S


if __name__ == "__main__":
    C, cnt = candidate_parcels(); log("candidate parcels", cnt, C.origin.value_counts().to_dict())
    g = decode_geoms(C); log("decoded")
    ps, S = build_sites(C, g); log("sites", len(S), S.origin.value_counts().to_dict(), "cap", int(S.cap.sum()))
