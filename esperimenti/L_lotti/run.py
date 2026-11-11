"""Base L v1: ricostruisce da zero i lotti candidati di Milano (edificabili e da riusare) in EPSG:32632.
Uso: python run.py            (scarica le fonti in esperimenti/_cache/L_lotti/raw se mancano, poi costruisce)
     python run.py --no-fetch (solo costruzione dai file in cache)
Uscite in questa cartella: lotti_v1.gpkg (strati lotti, metadati, cascata), tabelle/*.csv, esito_criteri.json, fig/*.png.
Filtro dei lotti edificabili = filtro condiviso del Lab (lab_completo/model/sites.py, config.py SITE/SUP), ricostruito da fonti riscaricabili."""
import glob, json, os, sys, time
import numpy as np, pandas as pd, geopandas as gpd, shapely
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from sklearn.cluster import KMeans

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "_cache", "L_lotti", "raw")
CRS = 32632
SEED = 42
T0 = time.time()
log = lambda *a: print(f"[{time.time() - T0:6.0f}s]", *a, file=sys.stderr, flush=True)

# ---------------------------------------------------------------- parametri (tutti [H], dal Lab salvo dove indicato)
P = dict(
    a_min_parcel=300.0,      # m², particella minima (Lab SITE)
    excl_share=0.5,          # quota massima di verde/agricolo/paesaggio/istruzione/acque/infrastrutture (Lab SITE)
    occ_res_share=0.5,       # particelle con volumi e quota residenziale >= 0,5 escluse: niente espulsioni (Lab SITE)
    plan_share=0.5,          # quota di AT o srv_erp che rende la particella "designata" (Lab SITE)
    storey_m=3.2,            # m, altezza di piano per SL = volume / 3,2 (Lab build_parcels)
    soft_far_ratio=0.5,      # soft site: indice < 0,5 × p75 del NIL (Lab build_parcels)
    soft_a_min=500.0,        # m², soft site minimo (Lab build_parcels)
    buffer_m=2.0,            # adiacenza per l'accorpamento in siti (Lab SITE)
    max_area_m2=60000.0,     # siti più grandi divisi con k-means pesato (Lab SITE)
    site_min_m2=1500.0,      # sito minimo (Lab SITE)
    far=1.0,                 # m² SL / m² superficie: indice ipotetico, NON l'indice del PGT (Lab SUP) [H]
    yield_=0.70,             # quota di SL utile ad alloggi (Lab SUP) [H]
    gfa_dw=80.0,             # m² SL per alloggio (Lab SUP) [H]
    m_min=20, m_max=400,     # alloggi min/max per lotto edificabile (Lab SUP) [H]
    snap_m=20.0,             # nuovo: punto di una fonte "da riusare" fuori da ogni particella -> particella più vicina entro 20 m [H]
    reuse_min_decl_m2=300.0, # nuovo: Demanio, superficie dichiarata minima (esclude appartamenti, cantine, quote) [H]
    m_min_riuso=1,           # nuovo: alloggi minimi per lotto da riusare [H]
    sample_n=30,             # controllo a campione per classe (criterio C5)
)
EXCL = ["pgt_srv_verde", "pgt_agr", "pgt_pae", "pgt_srv_ist", "dusaf_wat", "dusaf_infra", "dusaf_green", "dusaf_agr", "dusaf_wood"]  # Lab config.excl_cols
PROT = ["pgt_srv_verde", "pgt_agr", "pgt_pae", "dusaf_wat", "dusaf_infra", "dusaf_green", "dusaf_agr", "dusaf_wood"]  # Lab build_parcels.PROT

SRC = {  # fonte -> (descrizione, licenza)
    "catasto": ("Agenzia delle Entrate, cartografia catastale WFS INSPIRE (CadastralParcel, F205), scaricata 2026-11-11", "CC BY 4.0"),
    "dbt": ("Comune di Milano, DBT 2020 (ds2889): UN_VOL, EDIFC, EDIFC_USO", "CC BY 2.5 IT"),
    "dusaf": ("Regione Lombardia, DUSAF 8.0 (uso del suolo 2024), servizio ArcGIS dusaf8", "CC BY 4.0 [I: come DUSAF 7.0, licenza della 8.0 non letta]"),
    "pgt": ("Regione Lombardia, Tavola delle previsioni di piano (mosaico PGT, tav_previsioni_b), PGT Milano 2030", "[L] licenza non verificata"),
    "nil": ("Comune di Milano, NIL vigenti PGT 2030 (ds964)", "CC BY 4.0"),
    "ds503": ("Comune di Milano, Edifici e aree in degrado 2014-2017 (ds503, tav. R.10 PGT)", "CC BY 4.0"),
    "demanio": ("Agenzia del Demanio via Comune di Milano, Aree (ds2688) e Fabbricati (ds2689) del Demanio statale 2023", "CC BY 3.0 IT"),
    "ds677": ("Comune di Milano, Elenco immobili di proprietà comunale 2019 (ds677)", "CC BY 4.0"),
    "ds600": ("Città Metropolitana, Interventi di bonifica (ds600)", "CC0"),
    "ipotesi": ("Parametro o formula scelta [H] (vedi REPORT §3)", "—"),
}


def rd(name):
    g = gpd.read_file(os.path.join(RAW, name))
    return g.to_crs(CRS) if g.crs and g.crs.to_epsg() != CRS else g.set_crs(CRS, allow_override=True)


def share(geoms, layer):
    """Quota dell'area di ogni geometria coperta dallo strato (unione), 0-1."""
    if len(layer) == 0: return np.zeros(len(geoms))
    parts = np.array(shapely.get_parts(shapely.union_all(shapely.make_valid(layer.geometry.values))), dtype=object)
    parts = parts[shapely.get_type_id(parts) == 3]
    g = geoms.values if hasattr(geoms, "values") else geoms
    i, j = shapely.STRtree(parts).query(g, predicate="intersects")
    a = shapely.area(shapely.intersection(g[i], parts[j], grid_size=0.01))
    return np.clip(np.bincount(i, a, len(g)) / shapely.area(g), 0, 1)


def dusaf_cat(c):  # Lab mi/build_mi.py dusaf_cat, sul codice COD_TOT
    c = str(c)
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


# ---------------------------------------------------------------- particelle con indicatori
def parcels():
    seen, refs, rings = set(), [], []
    for f in sorted(glob.glob(os.path.join(RAW, "catasto", "*.json"))):
        for ref, pts in json.load(open(f)):
            if ref in seen or len(pts) < 4: continue
            seen.add(ref); refs.append(ref); rings.append(pts)
    g = gpd.GeoSeries(shapely.make_valid([shapely.Polygon(r) for r in rings]), crs=6706).to_crs(CRS)
    g = g.apply(lambda q: q if q.geom_type == "Polygon" else max((p for p in getattr(q, "geoms", [q]) if p.geom_type == "Polygon"), key=lambda p: p.area, default=shapely.Polygon()))
    D = gpd.GeoDataFrame({"ref": refs}, geometry=g.values, crs=CRS)
    D = D[~D.geometry.is_empty & (D.area > 1)].sort_values("ref").reset_index(drop=True)
    # il WFS è letto solo nell'anello esterno (come nel Lab): i fori (cortili con altre particelle) vanno ricostruiti
    # togliendo a ogni particella le particelle che contiene; senza questo, i lotti si sovrappongono (criterio C3)
    g = D.geometry.values
    i, j = shapely.STRtree(g).query(g, predicate="contains")
    k = (i != j) & (shapely.area(g[j]) < 0.999 * shapely.area(g[i]))  # i duplicati (stessa geometria, ref diversi) non sono fori
    holes = pd.Series(g[j[k]]).groupby(i[k]).agg(lambda v: shapely.union_all(list(v)))
    g = g.copy(); g[holes.index.values] = shapely.make_valid(shapely.difference(g[holes.index.values], holes.values))
    D["geometry"] = [q if q.geom_type in ("Polygon", "MultiPolygon") else shapely.union_all([p for p in shapely.get_parts(q) if p.geom_type == "Polygon"]) for q in g]
    D = D[~D.geometry.is_empty & (D.area > 1)].reset_index(drop=True)
    log("particelle con fori ricostruiti", len(holes))
    suf = D.ref.str.split(".").str[-1]
    D["land"] = suf.str.isdigit()
    D["foglio"] = pd.to_numeric(D.ref.str[5:9], errors="coerce")
    D["mappale"] = pd.to_numeric(suf, errors="coerce")
    D["area_m2"] = D.area
    log("particelle", len(D), "di terreno", int(D.land.sum()))
    return D


def main(fetch_first=True):
    if fetch_first:
        sys.path.insert(0, HERE); import fetch; fetch.main()
    os.makedirs(os.path.join(HERE, "tabelle"), exist_ok=True); os.makedirs(os.path.join(HERE, "fig"), exist_ok=True)
    nil = rd("ds964_nil.geojson")[["ID_NIL", "NIL", "geometry"]]
    city = shapely.union_all(nil.geometry.values)
    D = parcels()
    rp = D.geometry.representative_point()
    D["in_city"] = shapely.contains_xy(city, rp.x.values, rp.y.values)
    j = gpd.sjoin(gpd.GeoDataFrame(geometry=rp, crs=CRS), nil, predicate="within", how="left")
    D["nil_id"] = j.groupby(level=0).ID_NIL.first().reindex(D.index).values
    pt_x, pt_y = rp.x.values, rp.y.values

    # DBT 2020: volumi (fuori terra, h > 0,5 m) e uso residenziale; edifici diruti
    V = gpd.read_file(os.path.join(RAW, "dbt", "UN_VOL.shp"), columns=["UN_VOL_AV", "UN_VOL_POR", "CEDIUV"]).to_crs(CRS)
    V = V[(V.UN_VOL_POR != "02") & (V.UN_VOL_AV.astype(float) > 0.5)].copy()
    uso = gpd.read_file(os.path.join(RAW, "dbt", "EDIFC_EDIFC_USO.dbf"), ignore_geometry=True).drop_duplicates("CLASSREF").set_index("CLASSREF").EDIFC_USO
    V["vol"] = V.area * V.UN_VOL_AV.astype(float)
    V["res"] = V.CEDIUV.map(uso).fillna("95").astype(str).str.startswith("01")
    vp = gpd.GeoDataFrame(V[["vol", "res", "CEDIUV"]], geometry=V.representative_point(), crs=CRS)
    jv = gpd.sjoin(vp, D[["geometry"]][D.land], predicate="within", how="inner")
    jv = jv[~jv.index.duplicated()]
    D["n_vol"] = jv.groupby("index_right").size().reindex(D.index).fillna(0).astype(int)
    D["volume_m3"] = jv.groupby("index_right").vol.sum().reindex(D.index).fillna(0)
    rv = jv[jv.res].groupby("index_right").vol.sum().reindex(D.index).fillna(0)
    D["use_res_share"] = np.where(D.volume_m3 > 0, rv / D.volume_m3.clip(lower=1e-9), np.nan)
    log("volumi DBT", len(V), "assegnati", len(jv))

    # strati PGT (mosaico regionale) e DUSAF 8.0
    pg = {k: rd(f"pgt_{k}.geojson") for k in ("at", "servizi", "dism", "agr", "pae", "naf")}
    at = pg["at"]; pcu_poly = at[at.NOME_AMB.str.contains("PCU", na=False)]; at_np = at[~at.NOME_AMB.str.contains("PCU", na=False)]
    srv = pg["servizi"]
    lay = {"pgt_srv_verde": srv[srv.LEGENDA == "Aree a verde"], "pgt_srv_erp": srv[srv.LEGENDA == "Edilizia residenziale pubblica"],
           "pgt_srv_ist": srv[srv.LEGENDA.isin(["Istruzione", "Università e ricerca"])], "pgt_agr": pg["agr"], "pgt_pae": pg["pae"],
           "pgt_tras": at_np, "pgt_naf": pg["naf"]}
    du = rd("dusaf8.geojson"); du["cat"] = du.COD_TOT.map(dusaf_cat)
    for c in ("wat", "infra", "green", "agr", "wood"): lay[f"dusaf_{c}"] = du[du.cat == c]
    L = D.land & D.in_city
    for k, g in lay.items():
        D[k] = 0.0; D.loc[L, k] = share(D.geometry[L], g)
    log("quote PGT e DUSAF calcolate")
    D["pcu"] = shapely.contains_xy(shapely.union_all(shapely.make_valid(pcu_poly.geometry.values)), pt_x, pt_y)
    deg = pg["dism"][pg["dism"].NOTE.astype(str).str.startswith("ex AMB_DEG")]
    D["amb_deg"] = shapely.contains_xy(shapely.union_all(shapely.make_valid(deg.geometry.values)), pt_x, pt_y)
    D["at_name"] = None
    for n, g in zip(at_np.NOME_AMB, at_np.geometry):
        m = shapely.contains_xy(shapely.make_valid(g), pt_x, pt_y); D.loc[m & D.at_name.isna(), "at_name"] = n

    # soft site (Lab build_parcels)
    D["far"] = D.volume_m3 / P["storey_m"] / D.area_m2
    ref_mask = (D.area_m2 >= 200) & (D.n_vol > 0) & D.land
    D["far_nil_p75"] = D.nil_id.map(D[ref_mask].groupby("nil_id").far.quantile(0.75))
    D["far_ratio"] = D.far / D.far_nil_p75
    D["soft_site"] = (D.far_ratio < P["soft_far_ratio"]) & (D.area_m2 >= P["soft_a_min"]) & ~(D[PROT].max(axis=1) >= 0.5) & D.land

    # proprietà: ds677 (chiave catastale foglio+mappale, allegato/sviluppo ignorati [I]) e Demanio (punti)
    c677 = rd("ds677_patrimonio.geojson")
    c677_mi = c677[c677.MILANO == "SI"].copy()
    c677_mi["foglio"] = pd.to_numeric(c677_mi.FOGLIO, errors="coerce"); c677_mi["mappale"] = pd.to_numeric(c677_mi.MAPPALE, errors="coerce")
    keys = set(zip(c677_mi.foglio, c677_mi.mappale))
    D["comunale"] = [(f, m) in keys for f, m in zip(D.foglio, D.mappale)]
    dem = pd.concat([rd("ds2688_demanio_aree.geojson").assign(tipo_dem="area", sup=lambda d: d["Superficie Fondiaria area (MQ)"]),
                     rd("ds2689_demanio_fabbricati.geojson").assign(tipo_dem="fabbricato", sup=lambda d: d["Superficie Sedime (MQ)"])], ignore_index=True)
    dem["sup"] = pd.to_numeric(dem.sup.astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False), errors="coerce")
    dem = gpd.GeoDataFrame(dem, geometry="geometry", crs=CRS)

    # ------------------------------------------------------------ lotti da riusare: punto -> particella di terreno
    LP = D[D.land & D.in_city]
    tree = shapely.STRtree(LP.geometry.values)

    def to_parcel(pts):
        g = pts.geometry.values
        i, j = tree.query(g, predicate="within")
        out = np.full(len(g), -1); out[i] = LP.index.values[j]
        miss = np.where(out < 0)[0]
        if len(miss):
            k, dist = tree.query_nearest(g[miss], max_distance=P["snap_m"], return_distance=True, all_matches=False)
            out[miss[k[0]]] = LP.index.values[k[1]]
        return out

    W = []  # cascata
    R = []
    d503 = rd("ds503_degrado.geojson")
    d503["parcel"] = to_parcel(d503)
    R.append(pd.DataFrame({"parcel": d503.parcel, "fonte": "ds503", "nota": d503.TIPO_MACRO + " " + d503.INDIRIZZO}))
    W += [("riuso:ds503", "ds503 edifici e aree in degrado: righe", len(d503)), ("riuso:ds503", "ds503 associati a una particella (entro 20 m)", int((d503.parcel >= 0).sum()))]
    dd = dem[(dem["Categoria Patrimoniale"] == "PATRIMONIO DISPONIBILE")]
    W += [("riuso:demanio", "Demanio 2023 aree+fabbricati: righe", len(dem)), ("riuso:demanio", "Demanio: patrimonio disponibile", len(dd))]
    dd = dd[dd.sup >= P["reuse_min_decl_m2"]].copy()
    W += [("riuso:demanio", f"Demanio: superficie dichiarata >= {P['reuse_min_decl_m2']:.0f} m²", len(dd))]
    dd["parcel"] = to_parcel(dd)
    R.append(pd.DataFrame({"parcel": dd.parcel, "fonte": "demanio", "nota": dd.Descrizione.str[:80]}))
    W += [("riuso:demanio", "Demanio associati a una particella", int((dd.parcel >= 0).sum()))]
    al = c677_mi[c677_mi.PIANO_ALIENAZIONE == "SI"]
    kidx = D[D.land].set_index(["foglio", "mappale"]).index
    pm = pd.Series(D[D.land].index.values, index=kidx); pm = pm[~pm.index.duplicated()]
    al_parcel = [pm.get((f, m), -1) for f, m in zip(al.foglio, al.mappale)]
    R.append(pd.DataFrame({"parcel": al_parcel, "fonte": "ds677", "nota": al.TIPO + " in piano di alienazione, " + al.INDIRIZZO.astype(str)}))
    W += [("riuso:ds677", "ds677 in Milano: righe", len(c677_mi)), ("riuso:ds677", "ds677 in piano di alienazione", len(al)),
          ("riuso:ds677", "ds677 alienazione associati per foglio/mappale", int((np.array(al_parcel) >= 0).sum()))]
    ed = gpd.read_file(os.path.join(RAW, "dbt", "EDIFC.dbf"), ignore_geometry=True)
    rud = set(ed.CLASSID[ed.EDIFC_STAT == "02"])
    Vr = V[V.CEDIUV.isin(rud)]
    rp_r = gpd.GeoDataFrame(geometry=Vr.representative_point(), crs=CRS)
    rp_r["parcel"] = to_parcel(rp_r); rp_r["ed"] = Vr.CEDIUV.values
    rp_r = rp_r.drop_duplicates(["ed", "parcel"])
    R.append(pd.DataFrame({"parcel": rp_r.parcel, "fonte": "dbt_diruto", "nota": "edificio diruto/rudere (EDIFC_STAT=02) " + rp_r.ed}))
    W += [("riuso:dbt", "DBT 2020 edifici diruti/ruderi (EDIFC_STAT=02)", len(rud)), ("riuso:dbt", "DBT diruti con volume fuori terra, associati a una particella", int(rp_r.ed[rp_r.parcel >= 0].nunique()))]
    R = pd.concat(R, ignore_index=True); R = R[R.parcel >= 0]
    RG = R.groupby("parcel").agg(fonti_riuso=("fonte", lambda v: "+".join(sorted(set(v)))), nota=("nota", lambda v: " | ".join(sorted(set(map(str, v))))[:300]))
    RP = D.loc[RG.index].join(RG)
    W += [("riuso", "particelle distinte candidate al riuso", len(RP))]
    excl = (RP[EXCL] >= P["excl_share"]).any(axis=1)
    RP = RP[RP.area_m2 >= P["a_min_parcel"]]; W += [("riuso", f"particella >= {P['a_min_parcel']:.0f} m²", len(RP))]
    RP = RP[~(RP[EXCL] >= P["excl_share"]).any(axis=1)]; W += [("riuso", "non verde/agricolo/paesaggio/istruzione/acque/infrastrutture (>= 50%)", len(RP))]
    RP = RP[~RP.pcu]; W += [("riuso", "fuori dai Parchi della Campagna Urbana (PCU)", len(RP))]
    gfa = np.where(RP.volume_m3 > 0, RP.volume_m3 / P["storey_m"], P["far"] * RP.area_m2)
    RP = RP.assign(sl_base_m2=gfa, base_capacita=np.where(RP.volume_m3 > 0, "SL esistente DBT", "FAR x area"))
    RP["capacita"] = np.minimum(np.floor(P["yield_"] * RP.sl_base_m2 / P["gfa_dw"]), P["m_max"]).astype(int)
    RP = RP[RP.capacita >= P["m_min_riuso"]]; W += [("riuso", f"capacità >= {P['m_min_riuso']} alloggio", len(RP))]
    log("lotti da riusare", len(RP))

    # ------------------------------------------------------------ lotti edificabili: filtro condiviso del Lab
    E = D[D.land & D.in_city].copy()
    W += [("edificabile", "particelle di terreno nel Comune (catasto, mappale numerico)", len(E))]
    is_at = (E.pgt_tras >= P["plan_share"]) & ~E.pcu
    is_erp = E.pgt_srv_erp >= P["plan_share"]
    occ = (E.n_vol > 0) & (E.use_res_share.fillna(0) >= P["occ_res_share"])
    entry = E.soft_site | is_at | is_erp | E.amb_deg
    E["origine"] = np.select([is_at, E.amb_deg, is_erp], ["AT", "AMB_DEG", "ERP"], "SOFT")
    for lab, m in ((f"particella >= {P['a_min_parcel']:.0f} m²", E.area_m2 >= P["a_min_parcel"]),
                   ("non verde/agricolo/paesaggio/istruzione/acque/infrastrutture (>= 50%)", ~(E[EXCL] >= P["excl_share"]).any(axis=1)),
                   ("fuori dai Parchi della Campagna Urbana (PCU)", ~E.pcu),
                   ("non residenza occupata (quota residenziale del volume < 0,5)", ~occ),
                   ("ingresso: soft site, AT non PCU, srv_erp o ex AMB_DEG", entry),
                   ("non già lotto da riusare (precedenza al riuso)", ~E.ref.isin(RP.ref))):
        E = E[m.reindex(E.index)]; W += [("edificabile", lab, len(E))]
    E.loc[E.origine != "AT", "at_name"] = None
    E = E.sort_values("ref")
    # accorpamento in siti (Lab sites.build_sites): adiacenza 2 m, stessa origine, divisione k-means sopra 60.000 m², minimo 1.500 m²
    g = E.geometry.values
    a, b = shapely.STRtree(shapely.buffer(g, P["buffer_m"])).query(shapely.buffer(g, P["buffer_m"]), predicate="intersects")
    org = E.origine.values; m = (a < b) & (org[a] == org[b]); n = len(E)
    _, comp = connected_components(coo_matrix((np.ones(m.sum()), (a[m], b[m])), shape=(n, n)), directed=False)
    area = E.area_m2.values; lab_ = comp.copy(); nxt = comp.max() + 1
    cx, cy = shapely.get_x(shapely.centroid(g)), shapely.get_y(shapely.centroid(g))
    for c in np.where(np.bincount(comp, area) > P["max_area_m2"])[0]:
        idx = np.where(comp == c)[0]
        if len(idx) <= 1: continue
        k = min(int(np.ceil(area[idx].sum() / P["max_area_m2"])), len(idx))
        km = KMeans(k, n_init=4, random_state=SEED).fit(np.c_[cx[idx], cy[idx]], sample_weight=area[idx])
        lab_[idx] = nxt + km.labels_; nxt += k
    _, lab_ = np.unique(lab_, return_inverse=True)
    E["sito"] = lab_
    S = E.dissolve("sito", aggfunc={"ref": lambda v: ";".join(v), "area_m2": "sum", "volume_m3": "sum", "origine": "first",
                                    "at_name": lambda v: v.dropna().mode().iloc[0] if v.notna().any() else None})
    S["n_particelle"] = E.groupby("sito").size()
    S["area_m2"] = S.area  # area dell'unione: le particelle catastali possono sovrapporsi
    W += [("edificabile", "siti (accorpamento per adiacenza, stessa origine)", len(S))]
    S = S[S.area_m2 >= P["site_min_m2"]]; W += [("edificabile", f"sito >= {P['site_min_m2']:.0f} m²", len(S))]
    n_pre_cap = len(S)
    S["sl_base_m2"] = P["far"] * S.area_m2; S["base_capacita"] = "FAR x area"
    S["capacita"] = np.minimum(np.floor(P["yield_"] * S.sl_base_m2 / P["gfa_dw"]), P["m_max"]).astype(int)
    S = S[S.capacita >= P["m_min"]]; W += [("edificabile", f"capacità >= {P['m_min']} alloggi", len(S))]
    log("lotti edificabili", len(S))

    # ------------------------------------------------------------ tabella unica dei lotti
    RPo = RP.assign(classe="lotto da riusare", origine=RP.fonti_riuso, n_particelle=1, ambito_pgt=None)[
        ["ref", "area_m2", "volume_m3", "origine", "n_particelle", "ambito_pgt", "sl_base_m2", "base_capacita", "capacita", "nota", "classe", "geometry"]]
    So = S.reset_index(drop=True).assign(classe="lotto edificabile", nota=None).rename(columns={"at_name": "ambito_pgt"})[RPo.columns]
    Lt = gpd.GeoDataFrame(pd.concat([So, RPo], ignore_index=True), geometry="geometry", crs=CRS)
    Lt["geometry"] = shapely.make_valid(Lt.geometry.values)
    Lt["area_m2"] = Lt.area.round(1)
    rpt = Lt.geometry.representative_point()
    jn = gpd.sjoin(gpd.GeoDataFrame(geometry=rpt, crs=CRS), nil, predicate="within", how="left")
    Lt["nil_id"] = jn.groupby(level=0).ID_NIL.first().reindex(Lt.index).astype("Int64")
    Lt["nil_nome"] = jn.groupby(level=0).NIL.first().reindex(Lt.index)
    # proprietà: quota di area su particelle ds677 (chiave catastale) e punti Demanio (qualsiasi categoria) dentro il lotto
    com_area = D[D.comunale].set_index("ref").area_m2
    Lt["quota_comunale"] = [round(sum(com_area.get(r, 0) for r in refs.split(";")) / a, 3) for refs, a in zip(Lt.ref, Lt.area_m2)]
    Lt["quota_comunale"] = Lt.quota_comunale.clip(upper=1)
    dj = gpd.sjoin(dem[["Categoria Patrimoniale", "geometry"]], Lt[["geometry"]], predicate="within")
    has_dem = Lt.index.isin(dj.index_right) | Lt.origine.str.contains("demanio")
    dem_sa = set(dj.index_right[dj["Categoria Patrimoniale"] == "DEMANIO STORICO ARTISTICO"])
    is_com = (Lt.quota_comunale >= 0.5) | Lt.origine.str.contains("ds677")
    Lt["proprieta"] = np.select([has_dem, is_com], ["Demanio", "pubblico comunale"], "ignoto")
    Lt["proprieta_conflitto"] = has_dem & is_com
    # vincoli noti da dati
    bon = rd("ds600_bonifiche.geojson")
    bon_lot = set(gpd.sjoin(bon[["geometry"]], Lt[["geometry"]], predicate="within").index_right)
    dism_bon = pg["dism"][pg["dism"].BONIFICA == "SI"]
    sh = {k: share(Lt.geometry, v) for k, v in (("naf", lay["pgt_naf"]), ("pae", lay["pgt_pae"]), ("dism_bon", dism_bon))}
    vin = []
    for i in range(len(Lt)):
        v = []
        if i in bon_lot or sh["dism_bon"][i] > 0.1: v.append("bonifica (ds600 o PGT BONIFICA=SI)")
        if sh["naf"][i] > 0.1: v.append("nucleo di antica formazione PGT")
        if sh["pae"][i] > 0.1: v.append("area di valore paesaggistico PGT")
        if i in dem_sa: v.append("demanio storico-artistico")
        vin.append("; ".join(v))
    Lt["vincoli_noti"] = vin
    Lt["fonti"] = np.where(Lt.classe == "lotto edificabile", "catasto; dbt; pgt; dusaf; nil; ds677; demanio; ds600",
                           "catasto; dbt; pgt; dusaf; nil; ds677; demanio; ds600; " + Lt.origine.str.replace("+", "; ").str.replace("dbt_diruto", "dbt"))
    Lt["licenze"] = "CC BY 4.0; CC BY 2.5 IT; CC BY 3.0 IT; CC0; PGT regionale [L]"
    Lt["far_H"] = P["far"]
    Lt["cx"], Lt["cy"] = rpt.x.round(1), rpt.y.round(1)
    Lt = Lt.sort_values(["classe", "cx", "cy"]).reset_index(drop=True)
    Lt.insert(0, "id", np.where(Lt.classe == "lotto edificabile", "E", "R") + pd.Series(range(1, len(Lt) + 1)).astype(str).str.zfill(5))
    Lt["volume_m3"] = Lt.volume_m3.round(0); Lt["sl_base_m2"] = Lt.sl_base_m2.round(0)

    # ------------------------------------------------------------ criteri
    res = {}
    res["C1"] = bool(Lt.geometry.is_valid.all() and (~Lt.geometry.is_empty).all() and Lt.geom_type.isin(["Polygon", "MultiPolygon"]).all() and Lt.crs.to_epsg() == CRS)
    req = ["classe", "proprieta", "capacita", "nil_id", "fonti", "licenze"]
    res["C2"] = bool(Lt.id.is_unique and Lt[req].notna().all().all() and (Lt.area_m2 > 0).all())
    gg = Lt.geometry.values; i, j = shapely.STRtree(gg).query(gg, predicate="intersects"); k = i < j
    ov = shapely.area(shapely.intersection(gg[i[k]], gg[j[k]], grid_size=0.01))
    tol = np.maximum(5, 0.01 * np.minimum(shapely.area(gg[i[k]]), shapely.area(gg[j[k]])))
    bad = ov > tol
    res["C3_coppie_oltre_tolleranza"] = int(bad.sum()); res["C3"] = bool(bad.sum() == 0)
    res["C3_dettaglio"] = [dict(a=Lt.id[a_], b=Lt.id[b_], m2=round(float(o), 1)) for a_, b_, o in zip(i[k][bad], j[k][bad], ov[bad])][:20]
    e = Lt.classe == "lotto edificabile"
    res["C4"] = bool(Lt.capacita.between(P["m_min"], P["m_max"])[e].all() and (Lt.capacita[~e] >= P["m_min_riuso"]).all())
    # C5 controllo a campione su DUSAF 8.0
    rng = np.random.default_rng(SEED)
    sid = np.concatenate([rng.choice(Lt.index[Lt.classe == cl].values, size=min(P["sample_n"], int((Lt.classe == cl).sum())), replace=False)
                          for cl in ("lotto edificabile", "lotto da riusare")])
    sg = Lt.geometry.loc[sid].reset_index(drop=True)
    cod = du.COD_TOT.astype(str)
    q_res = share(sg, du[du.cat.isin(["resd", "resr"])]); q_nat = share(sg, du[du.cat.isin(["green", "agr", "wood", "wat"])])
    q_art = share(sg, du[cod.str.startswith("1") & ~cod.str.startswith("14")])  # suolo artificiale: DUSAF 1xx esclusi 14x (verde urbano)
    i, j = shapely.STRtree(du.geometry.values).query(sg.values, predicate="intersects")
    ia = pd.DataFrame({"i": i, "d": du.DESCRIZIONE.values[j], "a": shapely.area(shapely.intersection(sg.values[i], du.geometry.values[j]))})
    dom = ia.sort_values("a").groupby("i").d.last().reindex(range(len(sg))).fillna("nessuna classe DUSAF")
    camp = pd.DataFrame(dict(id=Lt.id[sid].values, classe=Lt.classe[sid].values, origine=Lt.origine[sid].values, area_m2=Lt.area_m2[sid].values,
                             dusaf_dominante=dom.values, quota_residenziale=q_res.round(3), quota_naturale=q_nat.round(3), quota_artificiale_1xx_no14=q_art.round(3)))
    camp["esito"] = np.where(camp.classe == "lotto edificabile", (camp.quota_residenziale <= 0.5) & (camp.quota_naturale <= 0.5), camp.quota_artificiale_1xx_no14 >= 0.5)
    pa = camp[camp.classe == "lotto edificabile"].esito.mean(); pb = camp[camp.classe == "lotto da riusare"].esito.mean()
    res["C5a_quota"], res["C5b_quota"] = round(float(pa), 3), round(float(pb), 3); res["C5"] = bool(pa >= 0.7 and pb >= 0.7)
    # diagnostica (non criterio): la regola C5a su tutti i lotti edificabili, per origine
    ge = Lt[e]
    ok_all = (share(ge.geometry, du[du.cat.isin(["resd", "resr"])]) <= 0.5) & (share(ge.geometry, du[du.cat.isin(["green", "agr", "wood", "wat"])]) <= 0.5)
    res["diag_C5a_tutti_per_origine"] = pd.Series(ok_all, index=ge.index).groupby(ge.origine).mean().round(3).to_dict()
    res["diag_C5a_tutti"] = round(float(ok_all.mean()), 3)
    tab = pd.crosstab([Lt.nil_id, Lt.nil_nome], Lt.classe).reset_index()
    res["C6"] = bool(all(tab[c].sum() == (Lt.classe == c).sum() for c in Lt.classe.unique()))
    res["C7_siti_prima_capacita"] = n_pre_cap; res["C7"] = bool(1718 <= n_pre_cap <= 2864)
    res["conteggi"] = Lt.classe.value_counts().to_dict(); res["capacita_tot"] = Lt.groupby("classe").capacita.sum().to_dict()
    res["origini"] = Lt.groupby(["classe", "origine"]).size().rename("n").reset_index().values.tolist()
    res["proprieta"] = Lt.groupby(["classe", "proprieta"]).size().rename("n").reset_index().values.tolist()
    res["proprieta_conflitti"] = int(Lt.proprieta_conflitto.sum())
    res["nil_con_lotti"] = int(Lt.nil_id.nunique()); res["parametri"] = P; res["seme"] = SEED
    res["passa"] = all(res[c] for c in ("C1", "C2", "C3", "C4", "C5", "C6"))

    # ------------------------------------------------------------ uscite
    cas = pd.DataFrame(W, columns=["classe", "passo", "rimasti"])
    cas["rimossi"] = cas.groupby("classe").rimasti.diff().mul(-1).astype("Int64")
    meta = pd.DataFrame([
        ("id", "ipotesi", "E/R + progressivo ordinato per classe e posizione"), ("geometry", "catasto", "unione delle particelle (EPSG:32632)"),
        ("classe", "ipotesi", "regole REPORT §3"), ("origine", "pgt; ds503; demanio; ds677; dbt", "edificabile: AT/AMB_DEG/ERP/SOFT; riuso: fonti del punto"),
        ("ref", "catasto", "riferimenti catastali F205_ffffas.mappale"), ("area_m2", "catasto", "area geometrica in EPSG:32632"),
        ("volume_m3", "dbt", "somma area × altezza delle unità volumetriche fuori terra"), ("ambito_pgt", "pgt", "nome AT (non PCU)"),
        ("sl_base_m2", "ipotesi; dbt", "edificabile FAR×area; riuso SL esistente = volume/3,2 m, altrimenti FAR×area"),
        ("capacita", "ipotesi", "min(floor(0,70 × SL / 80), 400)"), ("base_capacita", "ipotesi", "quale SL entra nella formula"),
        ("n_particelle", "catasto", "particelle catastali accorpate nel lotto"), ("far_H", "ipotesi", "indice ipotetico, non del PGT"),
        ("nil_id", "nil", "NIL del punto interno"), ("nil_nome", "nil", ""), ("quota_comunale", "ds677; catasto", "quota di area su particelle in ds677 (foglio+mappale)"),
        ("proprieta", "ds677; demanio; catasto", "Demanio se punto Demanio nel lotto o fonte Demanio; pubblico comunale se quota_comunale >= 0,5 o fonte ds677; altrimenti ignoto"),
        ("proprieta_conflitto", "ds677; demanio", "lotto con entrambe le evidenze"), ("vincoli_noti", "ds600; pgt; demanio", "bonifica, NAF, paesaggio, demanio storico-artistico; quota > 10%"),
        ("nota", "ds503; demanio; ds677; dbt", "descrizione della fonte del riuso"), ("cx", "catasto", "punto interno, x"), ("cy", "catasto", "punto interno, y"),
        ("fonti", "—", "chiavi delle fonti usate"), ("licenze", "—", "licenze delle fonti")], columns=["attributo", "fonte", "regola"])
    meta["fonte_estesa"] = meta.fonte.map(lambda s: " | ".join(SRC[k][0] for k in [x.strip() for x in s.split(";")] if k in SRC))
    meta["licenza"] = meta.fonte.map(lambda s: " | ".join(SRC[k][1] for k in [x.strip() for x in s.split(";")] if k in SRC)).replace("", "non applicabile (campo descrittivo)")
    out = os.path.join(HERE, "..", "_cache", "L_lotti", "lotti_v1_full.gpkg")
    for f in (out,):
        if os.path.exists(f): os.remove(f)
    Lt.drop(columns=["proprieta_conflitto"]).assign(proprieta_conflitto=Lt.proprieta_conflitto.astype(int)).to_file(out, layer="lotti", driver="GPKG")
    light = Lt.copy(); light["geometry"] = shapely.simplify(light.geometry.values, 1.0, preserve_topology=True)
    lp = os.path.join(HERE, "lotti_v1.gpkg")
    if os.path.exists(lp): os.remove(lp)
    light.assign(proprieta_conflitto=light.proprieta_conflitto.astype(int)).to_file(lp, layer="lotti", driver="GPKG")
    pyog = __import__("pyogrio")
    for name, df in (("metadati", meta), ("cascata", cas)):
        pyog.write_dataframe(df, lp, layer=name, driver="GPKG"); pyog.write_dataframe(df, out, layer=name, driver="GPKG")
    T = os.path.join(HERE, "tabelle")
    cas.to_csv(os.path.join(T, "cascata.csv"), index=False); tab.to_csv(os.path.join(T, "nil_classe.csv"), index=False)
    camp.to_csv(os.path.join(T, "campione_controllo.csv"), index=False); meta.to_csv(os.path.join(T, "metadati.csv"), index=False)
    json.dump(res, open(os.path.join(HERE, "esito_criteri.json"), "w"), indent=1, ensure_ascii=False, default=str)
    figure(Lt, nil, cas)
    log("fatto", res["conteggi"], "passa" if res["passa"] else "NON passa")
    return Lt, res


def figure(Lt, nil, cas):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 9))
    nil.boundary.plot(ax=ax, color="#bbbbbb", lw=0.4)
    for cl, col in (("lotto edificabile", "#d95f02"), ("lotto da riusare", "#1b9e77")):
        s = Lt[Lt.classe == cl]
        s.plot(ax=ax, color=col, edgecolor=col, lw=0.6, label=f"{cl} ({len(s)})")
        s.representative_point().plot(ax=ax, color=col, markersize=3)
    ax.legend(loc="lower left"); ax.set_axis_off(); ax.set_title("Base L v1: lotti candidati (EPSG:32632)")
    fig.savefig(os.path.join(HERE, "fig", "mappa_classi.png"), dpi=130, bbox_inches="tight"); plt.close(fig)
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.5))
    for ax, cl, col in zip(axs, ("edificabile", "riuso"), ("#d95f02", "#1b9e77")):
        c = cas[cas.classe.str.startswith(cl)]
        ax.barh(range(len(c))[::-1], c.rimasti, color=col); ax.set_yticks(range(len(c))[::-1]); ax.set_yticklabels([(k.split(":")[1] + ": " if ":" in k else "") + s[:55] for k, s in zip(c.classe, c.passo)], fontsize=7)
        ax.set_xscale("log"); ax.set_xlabel("unità rimaste (scala log)"); ax.set_title(f"Cascata dei filtri: {cl}")
        for y, v in zip(range(len(c))[::-1], c.rimasti): ax.text(v, y, f" {v:,}".replace(",", "."), va="center", fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig", "cascata.png"), dpi=130); plt.close(fig)


if __name__ == "__main__":
    main(fetch_first="--no-fetch" not in sys.argv)
