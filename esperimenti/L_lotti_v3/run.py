"""Base L v3 (ticket #35): lotti edificabili, lotti da riusare e aree di attivazione di Milano, EPSG:32632.
Parte da v2 (esperimenti/L_lotti_v2, fallimento documentato) con le sole modifiche [v3] della pre-registrazione:
AT PGT prevalgono sui filtri DUSAF di uso attuale; ds677 solo con conferma DUSAF; ds503 solo con conferma (diruto o screening).
Uso: python run.py              scarica le fonti mancanti, costruisce, campiona, prepara le immagini di ortofoto, calcola i criteri
                                (se manca tabelle/screening_ds503_codifica.csv si ferma dopo aver preparato le immagini dello screening)
     python run.py --no-fetch   solo dalla cache
     python run.py --pilota     prova su 3 NIL: uscite solo in esecuzioni/<data>_pilota/
Regole e soglie: pre-registrazione in esecuzioni/00_preregistrazione.txt (= REPORT §1). Ogni esecuzione lascia esecuzioni/<data>_<tag>/.
Riusa da v1 (esperimenti/L_lotti/run.py, congelato come fallimento documentato) le funzioni parcels, share, dusaf_cat, rd e fetch.py."""
import glob, hashlib, json, os, shutil, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
import numpy as np, pandas as pd, geopandas as gpd, shapely, pyogrio
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from sklearn.cluster import KMeans

HERE = os.path.dirname(os.path.abspath(__file__))
V1 = os.path.join(HERE, "..", "L_lotti")
sys.path.insert(0, V1)
import run as v1  # noqa: E402
CACHE = os.path.join(HERE, "..", "_cache", "L_lotti_v3")
RAW, RAW2 = v1.RAW, os.path.join(HERE, "..", "_cache", "L_lotti_v2", "raw")  # ds2813 scaricato da v2
TILES = os.path.join(HERE, "..", "_cache", "L_lotti_v2", "orto", "tiles")  # stessi tasselli AGEA di v2: cache condivisa
CRS, SEED = 32632, 42
T0 = time.time()
log = lambda *a: print(f"[{time.time() - T0:6.0f}s]", *a, file=sys.stderr, flush=True)

P = dict(  # tutti [H]; testo delle regole in REPORT §1
    a_min_parcel=300.0,      # m², particella minima (R4, E2)
    excl_share=0.5,          # quota che esclude (verde/agricolo/acque/...) o che fa entrare (AT, DUSAF 13x, 1412)
    occ_res_share=0.5,       # residenza occupata: quota residenziale del volume DBT
    free_cover_max=0.10,     # terreno comunale "libero": copertura edificata DBT < 0,10
    snap_m=20.0,             # punto ds503/Demanio -> edificio o particella più vicina entro 20 m
    buffer_m=2.0, max_area_m2=60000.0,  # accorpamento come v1/Lab
    lot_min_m2=1500.0,       # E4: lotto edificabile minimo, come area
    att_min_m2=500.0,        # A3: area di attivazione minima
    dual_min_m2=5000.0,      # A4: doppia etichetta, lotto edificabile minimo
    green_deficit_q=0.25,    # A4: NIL nel quartile inferiore dell'indice di verde ds2813
    storey_m=3.2, yield_=0.70, gfa_dw=80.0, fars=(0.5, 1.0, 2.0),  # capacità (Lab) e scenari D4
    dusaf_conf_comune=("131", "132", "133", "134", "1412"),  # [v3] conferma DUSAF dei terreni comunali (D2)
    seed_campione=3511, seed_dennis=3512, seed_screening=3513, n_alloc={"lotto edificabile": 50, "lotto da riusare": 30, "area di attivazione": 20}, n_base=100,
    orto_service="https://www.cartografia.servizirl.it/arcgis2/rest/services/BaseMap/Ortofoto2018_2019/ImageServer",
    soglia_C5a=0.70, soglia_C5b=0.25, overlap_m2=1.0,
)
TILE = dict(x0=-5120900.0, y0=9998100.0, res={9: 3.9687579375158752, 10: 2.6458386250105836, 11: 1.3229193125052918,
                                               12: 0.5291677250021167, 13: 0.26458386250105836})  # tileInfo del servizio [V]
DS2813 = ("https://dati.comune.milano.it/dataset/49d2896c-abba-44e5-9a53-c19332a275b3/resource/bbc7d511-f52d-4fe0-a7c7-aa7e5f5dceb5/"
          "download/ds2813_spotted-milan-urbangreenindex-nil-01072024_31072024.geojson")
SRC = dict(v1.SRC)
SRC["ds2813"] = ("Comune di Milano, Indice di verde urbano per NIL, luglio 2024 (ds2813, SPOTTED)", "CC BY 4.0")
SRC["orto"] = ("AGEA, Ortofoto 2018-2019, servizio Regione Lombardia BaseMap/Ortofoto2018_2019", "proprietà AGEA: visione e stampa con citazione [S]")
CL = ("lotto da riusare", "lotto edificabile", "area di attivazione")  # anche ordine di precedenza per le sovrapposizioni


def cap(area, far):
    return np.floor(P["yield_"] * far * np.asarray(area, float) / P["gfa_dw"]).astype(int)


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return dict(k=int(k), n=int(n), p=round(p, 3), ic95=[round(c - h, 3), round(c + h, 3)])


def newcombe(a, b):  # IC 95% della differenza p_a - p_b (metodo 10 di Newcombe, da due Wilson)
    d = a["p"] - b["p"]
    return round(d, 3), [round(d - np.hypot(a["p"] - a["ic95"][0], b["ic95"][1] - b["p"]), 3), round(d + np.hypot(a["ic95"][1] - a["p"], b["p"] - b["ic95"][0]), 3)]


def groups(E, key):
    """Accorpamento per adiacenza (v1/Lab): buffer 2 m, stessa chiave, k-means pesato sopra 60.000 m²."""
    E = E.sort_values("ref"); g = E.geometry.values; n = len(E)
    a, b = shapely.STRtree(shapely.buffer(g, P["buffer_m"])).query(shapely.buffer(g, P["buffer_m"]), predicate="intersects")
    k = E[key].values; m = (a < b) & (k[a] == k[b])
    _, comp = connected_components(coo_matrix((np.ones(m.sum()), (a[m], b[m])), shape=(n, n)), directed=False)
    area = E.area_m2.values; lab = comp.copy(); nxt = comp.max() + 1
    cx, cy = shapely.get_x(shapely.centroid(g)), shapely.get_y(shapely.centroid(g))
    for c in np.where(np.bincount(comp, area) > P["max_area_m2"])[0]:
        idx = np.where(comp == c)[0]
        if len(idx) <= 1: continue
        kk = min(int(np.ceil(area[idx].sum() / P["max_area_m2"])), len(idx))
        lab[idx] = nxt + KMeans(kk, n_init=4, random_state=SEED).fit(np.c_[cx[idx], cy[idx]], sample_weight=area[idx]).labels_; nxt += kk
    E = E.assign(gruppo=np.unique(lab, return_inverse=True)[1])
    S = E.dissolve("gruppo", aggfunc={"ref": ";".join, key: "first", "at_name": lambda v: v.dropna().mode().iloc[0] if v.notna().any() else None})
    S["n_particelle"] = E.groupby("gruppo").size(); S["area_m2"] = S.area
    return S.reset_index(drop=True)


# ---------------------------------------------------------------- ortofoto: tasselli in cache, immagine con contorno
def tile(level, r, c):
    p = os.path.join(TILES, str(level), f"{r}_{c}.img")
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        for i in range(5):
            try:
                b = urllib.request.urlopen(urllib.request.Request(f"{P['orto_service']}/tile/{level}/{r}/{c}", headers={"User-Agent": "tesi-base-L/3.0"}), timeout=60).read(); break
            except Exception as e:
                log("retry tassello", level, r, c, e); time.sleep(3 * (i + 1))
        else:
            raise SystemExit("tassello non scaricato")
        open(p + ".part", "wb").write(b); os.replace(p + ".part", p)
    return p


def orto_image(geom, path, px=560, extra=None):  # extra: edifici fonte, contorno giallo (screening ds503)
    from PIL import Image, ImageDraw
    x0, y0, x1, y1 = geom.bounds; m = max(x1 - x0, y1 - y0) * 0.25 + 15; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    half = max(x1 - x0, y1 - y0) / 2 + m
    X0, Y0, X1, Y1 = cx - half, cy - half, cx + half, cy + half
    level = max(l for l in TILE["res"] if 2 * half / TILE["res"][l] <= 1600 or l == 9)  # massimo dettaglio entro ~1600 px
    res = TILE["res"][level]; s = 256 * res
    c0, c1 = int((X0 - TILE["x0"]) // s), int((X1 - TILE["x0"]) // s); r0, r1 = int((TILE["y0"] - Y1) // s), int((TILE["y0"] - Y0) // s)
    rc = [(r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)]
    with ThreadPoolExecutor(6) as ex: files = list(ex.map(lambda t: tile(level, *t), rc))
    mos = Image.new("RGB", ((c1 - c0 + 1) * 256, (r1 - r0 + 1) * 256), "white")
    for (r, c), f in zip(rc, files):
        mos.paste(Image.open(f).convert("RGB"), ((c - c0) * 256, (r - r0) * 256))
    ox, oy = TILE["x0"] + c0 * s, TILE["y0"] - r0 * s  # angolo in alto a sinistra del mosaico
    box = ((X0 - ox) / res, (oy - Y1) / res, (X1 - ox) / res, (oy - Y0) / res)
    im = mos.crop(tuple(int(round(v)) for v in box)).resize((px, px)); d = ImageDraw.Draw(im); k = px / (2 * half)
    for gg, col in ((extra, (255, 230, 0)), (geom, (255, 0, 0))):
        for poly in shapely.get_parts(gg) if gg is not None else []:
            for ring in [poly.exterior, *poly.interiors]:
                d.line([((x - X0) * k, (Y1 - y) * k) for x, y in zip(*ring.xy)], fill=col, width=2)
    d.text((5, px - 14), f"{2 * half:.0f} m  AGEA 2018-2019 RL", fill=(255, 255, 0))
    im.save(path, quality=90)


# ---------------------------------------------------------------- costruzione
def build(pilota):
    nil = v1.rd("ds964_nil.geojson")[["ID_NIL", "NIL", "geometry"]]
    if pilota: nil = nil[nil.ID_NIL.isin(pilota)]
    city = shapely.union_all(nil.geometry.values)
    D = v1.parcels(); rp = D.geometry.representative_point()
    D["in_city"] = shapely.contains_xy(city, rp.x.values, rp.y.values)
    D["nil_id"] = gpd.sjoin(gpd.GeoDataFrame(geometry=rp, crs=CRS), nil, predicate="within", how="left").groupby(level=0).ID_NIL.first().reindex(D.index).values
    U = D[D.land & D.in_city].copy(); W = [("comune", "particelle di terreno nel Comune (catasto, mappale numerico)", len(U))]
    ux, uy = U.geometry.representative_point().x.values, U.geometry.representative_point().y.values
    tree = shapely.STRtree(U.geometry.values)

    def to_parcel(g):  # punto -> indice di U (particella che lo contiene o la più vicina entro snap_m), -1 se nessuna
        i, j = tree.query(g, predicate="within"); out = np.full(len(g), -1); out[i] = U.index.values[j]
        miss = np.where(out < 0)[0]
        if len(miss):
            k, _ = tree.query_nearest(g[miss], max_distance=P["snap_m"], return_distance=True, all_matches=False); out[miss[k[0]]] = U.index.values[k[1]]
        return out

    # DBT: unità volumetriche fuori terra, edifici, uso, stato
    V = gpd.read_file(os.path.join(RAW, "dbt", "UN_VOL.shp"), columns=["UN_VOL_AV", "UN_VOL_POR", "CEDIUV"]).to_crs(CRS)
    V = V[(V.UN_VOL_POR != "02") & (V.UN_VOL_AV.astype(float) > 0.5)].reset_index(drop=True)
    uso = gpd.read_file(os.path.join(RAW, "dbt", "EDIFC_EDIFC_USO.dbf"), ignore_geometry=True).drop_duplicates("CLASSREF").set_index("CLASSREF").EDIFC_USO
    stat = gpd.read_file(os.path.join(RAW, "dbt", "EDIFC.dbf"), ignore_geometry=True).set_index("CLASSID").EDIFC_STAT
    V["vol"] = V.area * V.UN_VOL_AV.astype(float); V["fp"] = V.area
    V["res"] = V.CEDIUV.map(uso).fillna("95").astype(str).str.startswith("01")
    V["parcel"] = to_parcel(V.representative_point().values)
    jv = V[V.parcel >= 0]
    U["n_vol"] = jv.groupby("parcel").size().reindex(U.index).fillna(0).astype(int)
    U["volume_m3"] = jv.groupby("parcel").vol.sum().reindex(U.index).fillna(0)
    U["cover"] = (jv.groupby("parcel").fp.sum().reindex(U.index).fillna(0) / U.area_m2).clip(upper=1)
    U["res_share"] = (jv[jv.res].groupby("parcel").vol.sum().reindex(U.index).fillna(0) / U.volume_m3.clip(lower=1e-9)).where(U.volume_m3 > 0)
    log("DBT: unità", len(V))

    # strati PGT e DUSAF
    pg = {k: v1.rd(f"pgt_{k}.geojson") for k in ("at", "servizi", "dism", "agr", "pae", "naf")}
    at = pg["at"]; is_pcu = at.NOME_AMB.str.contains("PCU", na=False); srv = pg["servizi"]
    du = v1.rd("dusaf8.geojson"); cod = du.COD_TOT.astype(str); du["cat"] = cod.map(v1.dusaf_cat)
    lay = {"pgt_srv_verde": srv[srv.LEGENDA == "Aree a verde"], "pgt_srv_ist": srv[srv.LEGENDA.isin(["Istruzione", "Università e ricerca"])],
           "pgt_agr": pg["agr"], "pgt_pae": pg["pae"], "pgt_tras": at[~is_pcu], "pgt_naf": pg["naf"],
           "dusaf_13": du[cod.isin(["133", "134"])], "dusaf_conf": du[cod.isin(P["dusaf_conf_comune"])], "dusaf_1412": du[cod == "1412"], "dusaf_cava": du[cod.isin(["131", "132"])]}
    for c in ("wat", "infra", "green", "agr", "wood"): lay[f"dusaf_{c}"] = du[du.cat == c]
    for k, g in lay.items(): U[k] = v1.share(U.geometry, g)
    U["pcu"] = shapely.contains_xy(shapely.union_all(shapely.make_valid(at[is_pcu].geometry.values)), ux, uy)
    U["is_at"] = (U.pgt_tras >= P["excl_share"]) & ~U.pcu  # [v3] particella AT: la destinazione di piano prevale sull'uso attuale DUSAF
    deg = pg["dism"][pg["dism"].NOTE.astype(str).str.startswith("ex AMB_DEG")]
    U["amb_deg"] = shapely.contains_xy(shapely.union_all(shapely.make_valid(deg.geometry.values)), ux, uy)
    U["at_name"] = None
    for n, g in zip(at[~is_pcu].NOME_AMB, at[~is_pcu].geometry):
        m = shapely.contains_xy(shapely.make_valid(g), ux, uy); U.loc[m & U.at_name.isna(), "at_name"] = n
    log("quote PGT e DUSAF")

    # proprietà
    c677 = v1.rd("ds677_patrimonio.geojson"); c677 = c677[c677.MILANO == "SI"]
    key = lambda d: list(zip(pd.to_numeric(d.FOGLIO, errors="coerce"), pd.to_numeric(d.MAPPALE, errors="coerce")))
    k_all, k_ter = set(key(c677)), set(key(c677[c677.TIPO == "TERRENO"]))
    fm = list(zip(U.foglio, U.mappale)); U["comunale"] = [x in k_all for x in fm]; U["comunale_terreno"] = [x in k_ter for x in fm]
    dem = pd.concat([v1.rd("ds2688_demanio_aree.geojson").assign(tipo_dem="area"), v1.rd("ds2689_demanio_fabbricati.geojson").assign(tipo_dem="fabbricato")], ignore_index=True)
    dem = gpd.GeoDataFrame(dem, geometry="geometry", crs=CRS); dem["parcel"] = to_parcel(dem.geometry.values)
    U["demanio"] = U.index.isin(dem.parcel); U["demanio_sa"] = U.index.isin(dem.parcel[dem["Categoria Patrimoniale"] == "DEMANIO STORICO ARTISTICO"])
    U["demanio_disp_area"] = U.index.isin(dem.parcel[(dem.tipo_dem == "area") & (dem["Categoria Patrimoniale"] == "PATRIMONIO DISPONIBILE")])

    # ------------------------------------------------------------ lotti da riusare (R1-R4)
    vt = shapely.STRtree(V.geometry.values)
    d503 = v1.rd("ds503_degrado.geojson"); g = d503.geometry.values
    i, j = vt.query(g, predicate="within"); b503 = np.full(len(g), None, dtype=object); b503[i] = V.CEDIUV.values[j]
    miss = np.array([x is None for x in b503])
    k, _ = vt.query_nearest(g[miss], max_distance=P["snap_m"], return_distance=True, all_matches=False); b503[np.where(miss)[0][k[0]]] = V.CEDIUV.values[k[1]]
    rud = set(stat.index[stat == "02"])
    src = pd.concat([pd.DataFrame({"edificio": b503, "fonte": "ds503", "nota": d503.TIPO_MACRO + " " + d503.INDIRIZZO}).dropna(subset=["edificio"]),
                     pd.DataFrame({"edificio": sorted(rud & set(V.CEDIUV)), "fonte": "dbt_diruto", "nota": "edificio diruto (EDIFC_STAT=02)"})])
    W += [("riuso:fonti", "ds503: punti", len(d503)), ("riuso:fonti", "ds503: punti con un edificio DBT entro 20 m", int((~pd.isna(b503)).sum())),
          ("riuso:fonti", "DBT diruti (EDIFC_STAT=02)", len(rud)), ("riuso:fonti", "DBT diruti con volume fuori terra", len(rud & set(V.CEDIUV))),
          ("riuso:fonti", "edifici fonte distinti", src.edificio.nunique())]
    bv = V.groupby("CEDIUV"); big = V.loc[bv.fp.idxmax()].set_index("CEDIUV")  # unità più grande dell'edificio -> particella
    E_src = src.groupby("edificio").agg(fonti_riuso=("fonte", lambda v: "+".join(sorted(set(v)))), nota=("nota", lambda v: " | ".join(sorted(set(map(str, v))))))
    E_src["parcel"] = big.parcel.reindex(E_src.index).values; E_src["vol"] = bv.vol.sum().reindex(E_src.index).values
    E_src = E_src[E_src.parcel >= 0]; W += [("riuso", "edifici fonte su una particella di terreno del Comune", len(E_src))]
    excl_plan = ["pgt_srv_verde", "pgt_agr", "pgt_pae", "pgt_srv_ist", "dusaf_wat"]; excl_use = ["dusaf_infra", "dusaf_green", "dusaf_agr", "dusaf_wood"]

    def riuso(E_src, W):  # R2-R4 come v2; [v3] filtri DUSAF di uso attuale non applicati alle particelle AT
        RP = E_src.reset_index().groupby("parcel").agg(edifici_fonte=("edificio", ";".join), fonti_riuso=("fonti_riuso", lambda v: "+".join(sorted(set("+".join(v).split("+"))))),
                                                        nota=("nota", lambda v: " | ".join(v)[:300]), volume_fonte_m3=("vol", "sum"))
        RP = U.loc[RP.index].join(RP); W += [("riuso", "particelle con edifici fonte", len(RP))]
        RP = RP[RP.area_m2 >= P["a_min_parcel"]]; W += [("riuso", f"particella >= {P['a_min_parcel']:.0f} m²", len(RP))]
        RP = RP[~(RP[excl_plan] >= P["excl_share"]).any(axis=1)]; W += [("riuso", "non verde/agricolo/paesaggio/istruzione PGT, non acque DUSAF (>= 0,5)", len(RP))]
        RP = RP[RP.is_at | ~(RP[excl_use] >= P["excl_share"]).any(axis=1)]; W += [("riuso", "non infrastrutture/verde/agricolo/boschi DUSAF (>= 0,5), salvo particelle AT", len(RP))]
        RP = RP[~RP.pcu]; W += [("riuso", "fuori dai PCU", len(RP))]
        other = V[V.parcel.isin(RP.index)]; geo = []  # R3: particella meno gli altri edifici DBT esistenti
        for p, row in RP.iterrows():
            o = other[(other.parcel == p) & ~other.CEDIUV.isin(row.edifici_fonte.split(";"))].geometry.values
            geo.append(shapely.difference(row.geometry, shapely.union_all(o)) if len(o) else row.geometry)
        return RP.set_geometry(geo, crs=CRS)

    # [v3] R1: un edificio ds503 entra solo se diruto DBT o confermato dallo screening su ortofoto (censimento dei candidati)
    cand = riuso(E_src, [])
    sid_s = E_src.index[E_src.fonti_riuso == "ds503"]  # edifici ds503 non diruti
    cand = cand[cand.edifici_fonte.map(lambda s: any(x in sid_s for x in s.split(";")))]
    scr = screening(cand, V, pilota)
    conf = set() if scr is None else set(scr.parcel[scr.Q1.eq("D") | scr.tetto.isin(["T2", "T3"])])
    W += [("riuso:fonti", "screening ds503: lotti candidati (R2-R4 passati, almeno un edificio ds503 non diruto)", len(cand)),
          ("riuso:fonti", "screening ds503: lotti confermati (Q1 = D o tetto T2/T3)", len(conf))]
    E_src = E_src[(E_src.fonti_riuso != "ds503") | E_src.parcel.isin(conf)]
    W += [("riuso", "edifici fonte confermati (diruti DBT o ds503 confermati dallo screening)", len(E_src))]
    RP = riuso(E_src, W)
    log("lotti da riusare", len(RP))

    # ------------------------------------------------------------ lotti edificabili e aree di attivazione (E1-E4, A1-A4)
    riuso_parcels = set(RP.index)
    e_at = (U.pgt_tras >= P["excl_share"]) & ~U.pcu; e_d13 = U.dusaf_13 >= P["excl_share"]
    e_com = U.comunale_terreno & (U.cover < P["free_cover_max"]) & (U.dusaf_conf >= P["excl_share"])  # [v3] D2: solo con conferma DUSAF
    entry_e = e_at | U.amb_deg | e_d13 | U.demanio_disp_area | e_com
    entry_a = (U.dusaf_1412 >= P["excl_share"]) | (U.dusaf_cava >= P["excl_share"])
    U["origine"] = np.select([e_at, U.amb_deg, e_d13, U.demanio_disp_area, e_com, U.dusaf_cava >= P["excl_share"]],
                             ["AT", "AMB_DEG", "DUSAF13", "DEMANIO", "COMUNE", "DUSAF_CAVA"], "DUSAF1412")
    A = U[entry_e | entry_a]
    W += [("edificabile+attivazione", "ingresso E1 (AT, AMB_DEG, DUSAF 133/134, Demanio disp., terreno comunale con DUSAF 131-134/1412)", int(entry_e.sum())),
          ("edificabile+attivazione", "ingresso E1 o A1 (anche DUSAF 1412, 131/132)", len(A))]
    excl_use = ["dusaf_infra", "dusaf_agr", "dusaf_wood", "dusaf_green"]
    occ = (A.n_vol > 0) & (A.res_share.fillna(0) >= P["occ_res_share"])
    for lab, m in ((f"particella >= {P['a_min_parcel']:.0f} m²", A.area_m2 >= P["a_min_parcel"]), ("fuori dai PCU", ~A.pcu),
                   ("non acque DUSAF (>= 0,5)", A.dusaf_wat < P["excl_share"]),
                   ("non infrastrutture/agricolo/boschi/verde in uso DUSAF (>= 0,5), salvo particelle AT", A.is_at | ~(A[excl_use] >= P["excl_share"]).any(axis=1)),
                   ("non agricolo/istruzione PGT (>= 0,5)", ~(A[["pgt_agr", "pgt_srv_ist"]] >= P["excl_share"]).any(axis=1)),
                   ("non residenza occupata (quota residenziale del volume < 0,5)", ~occ), ("non particella di un lotto da riusare", pd.Series(~A.index.isin(riuso_parcels), index=A.index))):
        A = A[m.reindex(A.index)]; W += [("edificabile+attivazione", lab, len(A))]
    vinc = (A.pgt_srv_verde >= P["excl_share"]) | (A.pgt_pae >= P["excl_share"])
    to_att = vinc | ~entry_e.reindex(A.index)
    A["motivo"] = np.select([A.pgt_srv_verde >= P["excl_share"], A.pgt_pae >= P["excl_share"], A.origine == "DUSAF_CAVA"],
                            ["verde di servizio PGT", "valore paesaggistico PGT", "cava o discarica DUSAF"], "area verde incolta DUSAF 1412")
    A.loc[~to_att, "at_name"] = A.loc[~to_att, "at_name"].where(A.origine[~to_att] == "AT")
    A.loc[to_att, "at_name"] = None
    Ae, Aa = A[~to_att], A[to_att].assign(origine=lambda d: d.origine + " / " + d.motivo)
    W += [("edificabile", "particelle verso l'abitazione", len(Ae)), ("attivazione", "particelle verso l'attivazione per vincolo o ingresso solo verde/cava (A2)", len(Aa))]
    Se, Sa = groups(Ae, "origine"), groups(Aa, "origine")
    W += [("edificabile", "gruppi per adiacenza (stessa origine)", len(Se)), ("attivazione", "gruppi per adiacenza (stessa origine e motivo)", len(Sa))]
    small = Se[(Se.area_m2 >= P["att_min_m2"]) & (Se.area_m2 < P["lot_min_m2"])].assign(origine=lambda d: d.origine + " / taglia < 1.500 m²", at_name=None)
    Se = Se[Se.area_m2 >= P["lot_min_m2"]]; W += [("edificabile", f"lotto >= {P['lot_min_m2']:.0f} m²", len(Se))]
    Sa = pd.concat([Sa[Sa.area_m2 >= P["att_min_m2"]], small], ignore_index=True)
    W += [("attivazione", f"gruppi >= {P['att_min_m2']:.0f} m² (A2) + gruppi edificabili 500-1.500 m² (A3)", len(Sa))]

    # ------------------------------------------------------------ tabella unica, sovrapposizioni, attributi
    RPo = RP.reset_index(drop=True).assign(classe=CL[0], origine=RP.fonti_riuso.values, n_particelle=1, at_name=None)
    Lt = gpd.GeoDataFrame(pd.concat([RPo, Se.assign(classe=CL[1]), Sa.assign(classe=CL[2])], ignore_index=True)[
        ["ref", "classe", "origine", "n_particelle", "at_name", "edifici_fonte", "fonti_riuso", "nota", "volume_fonte_m3", "geometry"]], geometry="geometry", crs=CRS)
    Lt["geometry"] = shapely.make_valid(Lt.geometry.values)
    pt = Lt.geometry.representative_point(); Lt["cx"], Lt["cy"] = pt.x.round(1), pt.y.round(1)
    Lt["_o"] = Lt.classe.map({c: i for i, c in enumerate(CL)})
    Lt = Lt.sort_values(["_o", "cx", "cy"]).reset_index(drop=True)
    Lt.insert(0, "id", Lt.classe.map({CL[0]: "R", CL[1]: "E", CL[2]: "A"}) + pd.Series(range(1, len(Lt) + 1)).astype(str).str.zfill(5))
    g = Lt.geometry.values.copy(); t = shapely.STRtree(g)
    for n in range(len(g)):  # precedenza: riuso > edificabile > attivazione, poi id (Lt è già in quest'ordine)
        prev = [m for m in t.query(g[n], predicate="intersects") if m < n]
        if prev:
            q = shapely.make_valid(shapely.difference(g[n], shapely.union_all(g[prev]), grid_size=0.01))
            g[n] = shapely.union_all([p for p in shapely.get_parts(q) if p.geom_type == "Polygon" and p.area > 0.01]) if not q.is_empty else q
    Lt["geometry"] = shapely.force_2d(g); Lt["area_m2"] = Lt.area.round(1)  # la Z ereditata dalle unità DBT varia tra esecuzioni (C8)
    keep = (~Lt.geometry.is_empty) & np.where(Lt.classe == CL[1], Lt.area_m2 >= P["lot_min_m2"], np.where(Lt.classe == CL[2], Lt.area_m2 >= P["att_min_m2"], Lt.area_m2 > 1))
    for c, kk in zip(CL, ("riuso", "edificabile", "attivazione")): W += [(kk, "dopo la rimozione delle sovrapposizioni (sopra il minimo di classe)", int((keep & (Lt.classe == c)).sum()))]
    Lt = Lt[keep].reset_index(drop=True)
    pt = Lt.geometry.representative_point(); Lt["cx"], Lt["cy"] = pt.x.round(1), pt.y.round(1)
    jn = gpd.sjoin(gpd.GeoDataFrame(geometry=pt, crs=CRS), nil, predicate="within", how="left").groupby(level=0)
    Lt["nil_id"] = jn.ID_NIL.first().reindex(Lt.index).astype("Int64"); Lt["nil_nome"] = jn.NIL.first().reindex(Lt.index)
    gv = gpd.read_file(os.path.join(RAW2, "ds2813_verde_nil.geojson"), ignore_geometry=True).set_index("ID_NIL").value
    Lt["nil_indice_verde"] = Lt.nil_id.map(gv).round(3); Lt["nil_deficit_verde"] = (Lt.nil_indice_verde <= gv.quantile(P["green_deficit_q"])).astype(int)
    r, e, a = (Lt.classe == c for c in CL)
    Lt["anche_attivazione"] = (e & (Lt.area_m2 >= P["dual_min_m2"]) & (Lt.nil_deficit_verde == 1)).astype(int)
    for f, nm in zip(P["fars"], ("cap_far05", "cap_far1", "cap_far2")): Lt[nm] = np.where(a, 0, cap(Lt.area_m2, f))
    Lt["volume_fonte_m3"] = Lt.volume_fonte_m3.round(0)
    Lt["cap_recupero"] = pd.Series(cap(Lt.volume_fonte_m3.fillna(0) / P["storey_m"], 1.0), index=Lt.index, dtype="Int64").where(r)
    Lt["scenario_principale"] = np.select([r & Lt.fonti_riuso.str.contains("dbt_diruto", na=False), r], ["demolizione e ricostruzione", "recupero"], "")
    Lt["base_scenario"] = np.where(r, "regola di default (fonte)", "")
    if scr is not None:  # [v3] scenario dallo screening ds503 (T3 -> demolizione, T1/T2 -> recupero), come per il campione
        t = scr[scr.tetto.isin(["T1", "T2", "T3"])].set_index("ref").tetto; m = r & Lt.ref.isin(t.index)
        Lt.loc[m, "scenario_principale"] = np.where(Lt.ref[m].map(t) == "T3", "demolizione e ricostruzione", "recupero"); Lt.loc[m, "base_scenario"] = "screening ds503 su ortofoto (T1-T3)"
    Lt["conferma_screening"] = (r & Lt.ref.isin(U.ref[list(conf)])).astype(int)
    # proprietà per quota di area
    ar = U.area_m2; com_a, dem_a = ar[U.comunale], ar[U.demanio]
    idx = U.reset_index().set_index("ref")["index"]
    refs = [[idx[x] for x in s.split(";") if x in idx.index] for s in Lt.ref]
    Lt["quota_comunale"] = [min(1, round(com_a.reindex(rr).fillna(0).sum() / A_, 3)) for rr, A_ in zip(refs, Lt.area_m2)]
    Lt["quota_demanio"] = [min(1, round(dem_a.reindex(rr).fillna(0).sum() / A_, 3)) for rr, A_ in zip(refs, Lt.area_m2)]
    Lt["proprieta"] = np.select([Lt.quota_demanio >= 0.5, Lt.quota_comunale >= 0.5], ["Demanio", "pubblico comunale"], "ignoto")
    Lt["proprieta_conflitto"] = ((Lt.quota_demanio >= 0.5) & (Lt.quota_comunale >= 0.5)).astype(int)
    bon = v1.rd("ds600_bonifiche.geojson"); bon_lot = set(gpd.sjoin(bon[["geometry"]], Lt[["geometry"]], predicate="within").index_right)
    sh = {k: v1.share(Lt.geometry, v) for k, v in (("naf", lay["pgt_naf"]), ("pae", lay["pgt_pae"]), ("bon", pg["dism"][pg["dism"].DBONIFICA == "SI"]))}
    dsa = set(gpd.sjoin(dem[dem["Categoria Patrimoniale"] == "DEMANIO STORICO ARTISTICO"][["geometry"]], Lt[["geometry"]], predicate="within").index_right)
    Lt["vincoli_noti"] = ["; ".join(v for v, c in (("bonifica (ds600 o PGT BONIFICA=SI)", i in bon_lot or sh["bon"][i] > 0.1), ("nucleo di antica formazione PGT", sh["naf"][i] > 0.1),
                                                  ("area di valore paesaggistico PGT", sh["pae"][i] > 0.1), ("demanio storico-artistico", i in dsa)) if c) for i in range(len(Lt))]
    base = "catasto; dbt; pgt; dusaf; nil; ds677; demanio; ds600; ds2813"
    Lt["fonti"] = np.where(r, base + "; " + Lt.fonti_riuso.fillna("").str.replace("+", "; ").str.replace("dbt_diruto", "dbt"), base)
    Lt["licenze"] = "CC BY 4.0; CC BY 2.5 IT; CC BY 3.0 IT; CC0; PGT regionale [L]"
    Lt = Lt.rename(columns={"at_name": "ambito_pgt"}).drop(columns="_o")
    log("lotti", Lt.classe.value_counts().to_dict())
    cov = copertura(at, is_pcu, Lt, U, du, pg["dism"][pg["dism"].DBONIFICA == "SI"])
    return Lt, U, nil, W, gv, cov


def copertura(at, is_pcu, Lt, U, du, bon):
    """[v3] tabelle/copertura_ambiti.csv: per ogni poligono AT, area coperta da particelle dell'universo e da lotti per classe, DUSAF della parte non coperta."""
    tu, tl, td = shapely.STRtree(U.geometry.values), shapely.STRtree(Lt.geometry.values), shapely.STRtree(du.geometry.values)
    cod = du.COD_TOT.astype(str).values; bon_u = shapely.union_all(shapely.make_valid(bon.geometry.values)); rows = []
    for oid, name, pcu, g in zip(at.OBJECTID, at.NOME_AMB, is_pcu, shapely.make_valid(at.geometry.values)):
        a = g.area; row = dict(objectid=oid, ambito=name, pcu=int(pcu), area_ha=round(a / 1e4, 2))
        row["universo_ha"] = round(shapely.intersection(g, shapely.union_all(U.geometry.values[tu.query(g, predicate="intersects")])).area / 1e4, 2)
        j = tl.query(g, predicate="intersects"); cov = shapely.union_all(Lt.geometry.values[j]) if len(j) else shapely.Polygon()
        for c, k in zip(CL, ("riuso", "edificabile", "attivazione")):
            jj = j[Lt.classe.values[j] == c]
            row[f"{k}_ha"] = round(shapely.intersection(g, shapely.union_all(Lt.geometry.values[jj])).area / 1e4, 2) if len(jj) else 0.0
            row[f"{k}_n"] = len(jj)
        row["coperto_quota"] = round(shapely.intersection(g, cov).area / a, 3)
        rest = shapely.difference(g, cov); row["non_coperto_ha"] = round(rest.area / 1e4, 2)
        k = td.query(rest, predicate="intersects")
        ar = pd.Series(shapely.area(shapely.intersection(rest, du.geometry.values[k], grid_size=0.01)), index=cod[k]).groupby(level=0).sum().sort_values(ascending=False)
        row["dusaf_non_coperto_top3"] = "; ".join(f"{c} {v / 1e4:.1f} ha" for c, v in ar.head(3).items())
        row["bonifica_pgt_quota"] = round(shapely.intersection(g, bon_u).area / a, 3)
        rows.append(row)
    return pd.DataFrame(rows).sort_values(["pcu", "ambito", "objectid"])


def fogli(d, codes):
    """Fogli 2x2 per la codifica a vista (solo immagini e codice), in d/fogli."""
    from PIL import Image, ImageDraw
    os.makedirs(os.path.join(d, "fogli"), exist_ok=True); codes = sorted(codes)
    for n in range(0, len(codes), 4):
        sheet = Image.new("RGB", (1130, 1160), "white"); dr = ImageDraw.Draw(sheet)
        for q, c in enumerate(codes[n:n + 4]):
            x, y = (q % 2) * 570, (q // 2) * 580; sheet.paste(Image.open(os.path.join(d, c + ".jpg")), (x, y + 20)); dr.text((x + 5, y + 4), c, fill=(0, 0, 0))
        sheet.save(os.path.join(d, "fogli", f"{codes[n]}_{codes[min(n + 3, len(codes) - 1)]}.jpg"), quality=88)


def screening(cand, V, pilota):
    """[v3] R1: immagini S001.. dei lotti ds503 candidati (ordine casuale, seme dichiarato) e codifica manuale cieca; None nel pilota."""
    if pilota: return None  # pilota: nessuno screening, nessun ds503 confermato
    cand = cand.sort_values("ref"); rng = np.random.default_rng(P["seed_screening"])
    key = pd.DataFrame({"codice": ["S%03d" % (i + 1) for i in np.argsort(rng.permutation(len(cand)))], "ref": cand.ref.values, "parcel": cand.index.values})
    d = os.path.join(CACHE, "orto", "screening"); os.makedirs(d, exist_ok=True)
    for c, (_, row) in zip(key.codice, cand.iterrows()):
        f = os.path.join(d, c + ".jpg")
        if not os.path.exists(f): orto_image(row.geometry, f, extra=shapely.union_all(V.geometry.values[V.CEDIUV.isin(row.edifici_fonte.split(";")).values]))
    key.to_csv(os.path.join(HERE, "tabelle", "screening_ds503_chiave.csv"), index=False)
    f = os.path.join(HERE, "tabelle", "screening_ds503_codifica.csv")
    if not os.path.exists(f):
        fogli(d, key.codice); pd.DataFrame({"codice": sorted(key.codice)}).assign(Q1="", tetto="", veg="", uso="", nota="").to_csv(f + ".vuota", index=False)
        raise SystemExit(f"screening ds503: {len(key)} immagini in {d}; compilare {f} (modello .vuota) e rieseguire")
    cod = pd.read_csv(f, dtype=str).fillna("")
    S = key.merge(cod, on="codice", how="left", validate="1:1"); assert S.Q1.isin(list("LCDUVIX")).all(), "codifica screening incompleta"
    return S


def content_hash(L):
    a = L.drop(columns="geometry").sort_values("id").to_csv(index=False, float_format="%.3f").encode()
    w = b"".join(shapely.to_wkb(shapely.normalize(shapely.set_precision(L.sort_values("id").geometry.values, 0.001))))
    return hashlib.sha256(a + w).hexdigest()


def main():
    pil = [21, 51, 72] if "--pilota" in sys.argv else None  # NIL del pilota: fissati prima [H]
    if "--no-fetch" not in sys.argv:
        import fetch; fetch.main()  # fonti di v1
        os.makedirs(RAW2, exist_ok=True); p = os.path.join(RAW2, "ds2813_verde_nil.geojson")
        if not os.path.exists(p): urllib.request.urlretrieve(DS2813, p)
    Lt, U, nil, W, gv, cov = build(pil)
    res = {"pilota": pil, "parametri": {k: v for k, v in P.items()}, "seme": SEED}
    # ---------------------------------------------------------- campione ortofoto (seme e allocazione da REPORT §1.3)
    rng = np.random.default_rng(P["seed_campione"]); alloc = dict(P["n_alloc"])
    for c in CL:
        if (Lt.classe == c).sum() < alloc[c]: alloc["lotto edificabile"] += alloc[c] - (Lt.classe == c).sum(); alloc[c] = int((Lt.classe == c).sum())
    alloc = {c: min(n, int((Lt.classe == c).sum())) for c, n in alloc.items()}  # solo il pilota ha meno lotti del campione
    sid = np.concatenate([rng.choice(Lt.index[Lt.classe == c].values, alloc[c], replace=False) for c in ("lotto edificabile", "lotto da riusare", "area di attivazione")])
    BU = U[U.area_m2 >= P["a_min_parcel"]]; bid = rng.choice(len(BU), P["n_base"], replace=False)
    camp = pd.concat([pd.DataFrame({"tipo": "lotto", "id": Lt.id[sid].values, "classe": Lt.classe[sid].values, "origine": Lt.origine[sid].values, "geometry": Lt.geometry[sid].values}),
                      pd.DataFrame({"tipo": "base", "id": BU.ref.values[bid], "classe": "particella qualsiasi", "origine": "", "geometry": BU.geometry.values[bid]})], ignore_index=True)
    camp["codice"] = ["C%03d" % (i + 1) for i in np.argsort(rng.permutation(len(camp)))]
    T = os.path.join(HERE, "tabelle"); casi = None
    if not pil:
        os.makedirs(os.path.join(CACHE, "orto", "img"), exist_ok=True)
        for cdx, gg in zip(camp.codice, camp.geometry):
            f = os.path.join(CACHE, "orto", "img", cdx + ".jpg")
            if not os.path.exists(f): orto_image(gg, f)
        log("immagini ortofoto", len(camp))
        camp.drop(columns="geometry").sort_values("codice").to_csv(os.path.join(T, "campione_ortofoto.csv"), index=False)
        secondo_codificatore(camp.codice)
        cod_f = os.path.join(T, "codifica_ortofoto.csv")
        if not os.path.exists(cod_f): fogli(os.path.join(CACHE, "orto", "img"), camp.codice)
        if os.path.exists(cod_f):
            res.update(criteri_orto(camp, pd.read_csv(cod_f, dtype=str).fillna(""), Lt)); casi = res.pop("C7_casi")
    # ---------------------------------------------------------- criteri
    r, e, a = (Lt.classe == c for c in CL)
    res["C1"] = bool(Lt.geometry.is_valid.all() and (~Lt.geometry.is_empty).all() and Lt.geom_type.isin(["Polygon", "MultiPolygon"]).all() and Lt.crs.to_epsg() == CRS)
    req = ["classe", "origine", "proprieta", "cap_far05", "cap_far1", "cap_far2", "nil_id", "fonti", "licenze"]
    res["C2"] = bool(Lt.id.is_unique and Lt[req].notna().all().all() and (Lt[["origine", "fonti", "licenze"]] != "").all().all() and (Lt.area_m2 > 0).all() and Lt.cap_recupero[r].notna().all())
    gg = Lt.geometry.values; i, j = shapely.STRtree(gg).query(gg, predicate="intersects"); k = i < j
    ov = shapely.area(shapely.intersection(gg[i[k]], gg[j[k]], grid_size=0.01)); bad = ov > P["overlap_m2"]
    res["C3_coppie_oltre_1m2"] = int(bad.sum()); res["C3_area_comune_max_m2"] = round(float(ov.max()), 3) if len(ov) else 0.0; res["C3"] = bool(bad.sum() == 0)
    res["C4"] = bool(all((Lt[nm] == np.where(a, 0, cap(Lt.area_m2, f))).all() for f, nm in zip(P["fars"], ("cap_far05", "cap_far1", "cap_far2")))
                     and (Lt.cap_recupero[r].astype(int) == cap(Lt.volume_fonte_m3[r] / P["storey_m"], 1.0)).all() and Lt.cap_recupero[~r].isna().all())
    tab = pd.crosstab([Lt.nil_id, Lt.nil_nome], Lt.classe).reset_index()
    cas = pd.DataFrame(W, columns=["classe", "passo", "rimasti"]); cas["rimossi"] = cas.groupby("classe").rimasti.diff().mul(-1).astype("Int64")
    cas.loc[cas.classe.str.endswith(":fonti") | (cas.rimossi < 0), "rimossi"] = pd.NA  # righe di fonti o di ingresso: la differenza non è un filtro
    last = cas.groupby("classe").rimasti.last()
    res["C6"] = bool(all(tab[c].sum() == (Lt.classe == c).sum() for c in Lt.classe.unique())
                     and last["riuso"] == r.sum() and last["edificabile"] == e.sum() and last["attivazione"] == a.sum())
    res["conteggi"] = Lt.classe.value_counts().to_dict()
    res["capacita"] = {c: {nm: int(Lt.loc[Lt.classe == c, nm].sum()) for nm in ("cap_far05", "cap_far1", "cap_far2")} for c in CL}
    res["capacita"][CL[0]]["cap_recupero"] = int(Lt.cap_recupero[r].sum())
    res["capacita_anche_attivazione"] = {nm: int(Lt.loc[Lt.anche_attivazione == 1, nm].sum()) for nm in ("cap_far05", "cap_far1", "cap_far2")}
    res["n_anche_attivazione"] = int(Lt.anche_attivazione.sum())
    res["edificabili_oltre_400_alloggi_far1"] = int((Lt.cap_far1[e] > 400).sum())
    res["origini"] = Lt.groupby(["classe", "origine"]).size().rename("n").reset_index().values.tolist()
    res["proprieta"] = Lt.groupby(["classe", "proprieta"]).size().rename("n").reset_index().values.tolist()
    res["area_ha"] = Lt.groupby("classe").area_m2.sum().div(1e4).round(1).to_dict()
    res["nil_con_lotti"] = int(Lt.nil_id.nunique()); res["hash_contenuto"] = content_hash(Lt)
    prev = sorted(glob.glob(os.path.join(HERE, "esecuzioni", "*_completa", "esito_criteri.json")))  # C8: confronto con l'esecuzione completa precedente
    res["C8_hash_precedente"] = json.load(open(prev[-1])).get("hash_contenuto") if prev and not pil else None
    res["C8"] = res["C8_hash_precedente"] == res["hash_contenuto"]
    res["passa"] = all(res.get(c) is True for c in ("C1", "C2", "C3", "C4", "C5", "C6", "C8"))
    # ---------------------------------------------------------- uscite
    meta = pd.DataFrame([
        ("id", "ipotesi", "R/E/A + progressivo per classe e posizione"), ("geometry", "catasto; dbt", "particelle unite; riuso: particella meno gli altri edifici DBT; senza sovrapposizioni (precedenza R > E > A)"),
        ("classe", "ipotesi", "regole REPORT §1.2"), ("origine", "pgt; dusaf; ds677; demanio; ds503; dbt", "ingresso (e motivo per l'attivazione)"),
        ("ref", "catasto", "riferimenti catastali"), ("n_particelle", "catasto", ""), ("ambito_pgt", "pgt", "nome AT non PCU"),
        ("edifici_fonte", "dbt", "CEDIUV degli edifici fonte (riuso)"), ("fonti_riuso", "ds503; dbt", ""), ("nota", "ds503; dbt", "descrizione della fonte"),
        ("volume_fonte_m3", "dbt", "volume fuori terra dei soli edifici fonte"), ("area_m2", "catasto", "area del lotto, EPSG:32632"),
        ("cx", "catasto", "punto interno x"), ("cy", "catasto", "punto interno y"), ("nil_id", "nil", ""), ("nil_nome", "nil", ""),
        ("nil_indice_verde", "ds2813", "indice di verde urbano del NIL, luglio 2024"), ("nil_deficit_verde", "ds2813; ipotesi", "1 se nel quartile inferiore degli 88 NIL"),
        ("anche_attivazione", "ds2813; ipotesi", "lotto edificabile >= 5.000 m² in NIL con deficit di verde (A4)"),
        ("cap_far05", "ipotesi", "floor(0,70 × 0,5 × area / 80); riuso: demolizione e ricostruzione; attivazione 0"),
        ("cap_far1", "ipotesi", "floor(0,70 × 1 × area / 80); come sopra"), ("cap_far2", "ipotesi", "floor(0,70 × 2 × area / 80); come sopra"),
        ("cap_recupero", "dbt; ipotesi", "riuso: floor(0,70 × volume_fonte / 3,2 / 80); altre classi vuoto"),
        ("scenario_principale", "ipotesi; orto", "riuso: T3 -> demolizione, T1/T2 -> recupero (screening ds503 o campione); altrimenti diruto -> demolizione, ds503 -> recupero"),
        ("base_scenario", "ipotesi; orto", "regola di default, screening ds503 o campione su ortofoto"),
        ("conferma_screening", "ds503; orto", "1 se il lotto da riusare contiene edifici ds503 confermati dallo screening su ortofoto (R1 v3)"),
        ("quota_comunale", "ds677; catasto", "quota di area su particelle ds677"), ("quota_demanio", "demanio; catasto", "quota di area su particelle con un punto Demanio"),
        ("proprieta", "ds677; demanio", "Demanio se quota_demanio >= 0,5; comunale se quota_comunale >= 0,5; altrimenti ignoto"),
        ("proprieta_conflitto", "ds677; demanio", "entrambe le quote >= 0,5"), ("vincoli_noti", "ds600; pgt; demanio", "quota > 10% o punto nel lotto"),
        ("fonti", "—", ""), ("licenze", "—", "")], columns=["attributo", "fonte", "regola"])
    meta["fonte_estesa"] = meta.fonte.map(lambda s: " | ".join(SRC[x.strip()][0] for x in s.split(";") if x.strip() in SRC))
    meta["licenza"] = meta.fonte.map(lambda s: " | ".join(SRC[x.strip()][1] for x in s.split(";") if x.strip() in SRC)).replace("", "non applicabile (campo descrittivo)")
    res["C2"] = res["C2"] and set(Lt.columns) - {"geometry"} <= set(meta.attributo)
    ts = time.strftime("%Y-%m-%dT%H%M%SZ", time.gmtime()); tag = "pilota" if pil else "completa"
    out = os.path.join(HERE, "esecuzioni", f"{ts}_{tag}"); os.makedirs(out)
    git = lambda *a: subprocess.run(["git", "-C", HERE, *a], capture_output=True, text=True).stdout.strip()
    res["registro"] = dict(utc=ts, commit=git("rev-parse", "HEAD"), modifiche_non_committate=git("status", "--porcelain", "--", ".").splitlines(),
                           sha256_run_py=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), python=sys.version.split()[0],
                           durata_s=round(time.time() - T0))
    js = lambda p: json.dump(res, open(p, "w"), indent=1, ensure_ascii=False, default=str)
    js(os.path.join(out, "esito_criteri.json")); cas.to_csv(os.path.join(out, "cascata.csv"), index=False); cov.to_csv(os.path.join(out, "copertura_ambiti.csv"), index=False)
    if not pil:
        lp = os.path.join(HERE, "lotti_v3.gpkg")
        if os.path.exists(lp): os.remove(lp)
        Lt.to_file(lp, layer="lotti", driver="GPKG")
        for name, df in (("metadati", meta), ("cascata", cas)): pyogrio.write_dataframe(df, lp, layer=name, driver="GPKG")
        cov.to_csv(os.path.join(T, "copertura_ambiti.csv"), index=False)
        cas.to_csv(os.path.join(T, "cascata.csv"), index=False); tab.to_csv(os.path.join(T, "nil_classe.csv"), index=False); meta.to_csv(os.path.join(T, "metadati.csv"), index=False)
        Lt.drop(columns="geometry").to_csv(os.path.join(T, "lotti_attributi.csv"), index=False)
        js(os.path.join(HERE, "esito_criteri.json")); figure(Lt, nil, cas)
        if casi is not None: controllo_umano(camp, casi)
    log("fatto", res["conteggi"], {c: res.get(c) for c in ("C1", "C2", "C3", "C4", "C5", "C6", "C8")}, res["hash_contenuto"][:12])


def criteri_orto(camp, cod, Lt):
    """C5 dalla tabella di codifica (codice, Q1, tetto, veg, uso, nota), unita al campione solo qui."""
    C = camp.drop(columns="geometry").merge(cod, on="codice", how="left", validate="1:1")
    assert C.Q1.isin(list("LCDUVIX")).all(), "codifica incompleta"
    C["ok"] = C.Q1.isin(list("LCD")); lo, ba = C[C.tipo == "lotto"], C[C.tipo == "base"]
    out = {"C5a": wilson(lo.ok.sum(), len(lo)), "C5_base": wilson(ba.ok.sum(), len(ba))}
    out["C5b_differenza"], out["C5b_ic95"] = newcombe(out["C5a"], out["C5_base"])
    out["C5"] = bool(out["C5a"]["p"] >= P["soglia_C5a"] and out["C5b_ic95"][0] >= P["soglia_C5b"])
    out["C5_per_classe"] = {c: wilson(g.ok.sum(), len(g)) for c, g in lo.groupby("classe")}
    out["C5_per_origine"] = {f"{c} | {o}": wilson(g.ok.sum(), len(g)) for (c, o), g in lo.groupby(["classe", "origine"])}
    scr_ids = set(Lt.id[Lt.conferma_screening == 1]); lo2 = lo[~lo.id.isin(scr_ids)]
    out["C5a_senza_confermati_screening"] = wilson(lo2.ok.sum(), len(lo2)); out["n_campione_confermati_screening"] = int(lo.id.isin(scr_ids).sum())
    w = Lt.classe.value_counts(normalize=True); out["C5a_pesato_per_classe"] = round(float(sum(w[c] * g.ok.mean() for c, g in lo.groupby("classe"))), 3)
    out["Q1_per_tipo"] = C.groupby(["classe", "Q1"]).size().rename("n").reset_index().values.tolist()
    rr = lo[lo.classe == "lotto da riusare"]; b = rr[rr.tetto.isin(["T1", "T2", "T3"])]
    rec = np.select([b.tetto == "T3", b.tetto == "T2", (b.tetto == "T1") & (b.veg == "V2")], ["bassa", "media", "media"], "alta")
    out["riuso_recuperabilita"] = pd.Series(rec).value_counts().to_dict(); out["riuso_uso_apparente"] = rr.uso.value_counts().to_dict()
    out["riuso_U+"] = wilson((rr.uso == "U+").sum(), len(rr)) if len(rr) else None
    # scenario principale dallo screening per i lotti da riusare nel campione
    sc = dict(zip(b.id, np.where(b.tetto == "T3", "demolizione e ricostruzione", "recupero")))
    m = Lt.id.isin(sc); Lt.loc[m, "scenario_principale"] = Lt.id[m].map(sc); Lt.loc[m, "base_scenario"] = "screening su ortofoto (T1-T3)"
    C.to_csv(os.path.join(HERE, "tabelle", "controllo_ortofoto_esito.csv"), index=False)
    # 20 casi per Dennis: 7 edificabili, 5 riuso, 3 attivazione, 5 base, seme dichiarato
    rng = np.random.default_rng(P["seed_dennis"]); pick = []
    for c, n in (("lotto edificabile", 7), ("lotto da riusare", 5), ("area di attivazione", 3), ("particella qualsiasi", 5)):
        g = C[C.classe == c]; pick += list(rng.choice(g.codice.values, min(n, len(g)), replace=False))
    out["C7"] = "in attesa di Dennis"; out["C7_casi"] = C[C.codice.isin(pick)].sort_values("codice")
    return out


def controllo_umano(camp, casi):
    """[v3] 20 casi per Dennis ricodificati D01-D20 (ordine casuale, seme 3512): immagini senza etichette, modulo vuoto, chiave a parte."""
    d = os.path.join(HERE, "controllo_umano"); os.makedirs(os.path.join(d, "img"), exist_ok=True)
    casi = casi.iloc[np.random.default_rng(P["seed_dennis"]).permutation(len(casi))].assign(caso=[f"D{i + 1:02d}" for i in range(len(casi))])
    for c, k in zip(casi.codice, casi.caso): shutil.copy(os.path.join(CACHE, "orto", "img", c + ".jpg"), os.path.join(d, "img", k + ".jpg"))
    pd.DataFrame({"caso": casi.caso, "Q1": "", "tetto": "", "veg": "", "uso": "", "nota": ""}).to_csv(os.path.join(d, "modulo_dennis.csv"), index=False)
    casi[["caso", "codice", "tipo", "id", "classe", "origine", "Q1", "tetto", "veg", "uso", "nota"]].rename(
        columns={k: "agente_" + k for k in ("Q1", "tetto", "veg", "uso", "nota")}).to_csv(os.path.join(d, "chiave_da_aprire_dopo.csv"), index=False)


def secondo_codificatore(codes):
    """[v3] 200 immagini C001-C200 + foglio vuoto + istruzioni per un secondo codificatore cieco (l'accordo lo calcola il coordinatore)."""
    d = os.path.join(HERE, "controllo_secondo_codificatore"); os.makedirs(os.path.join(d, "img"), exist_ok=True)
    for c in sorted(codes): shutil.copy(os.path.join(CACHE, "orto", "img", c + ".jpg"), os.path.join(d, "img", c + ".jpg"))
    pd.DataFrame({"codice": sorted(codes), "Q1": "", "tetto": "", "veg": "", "uso": "", "nota": ""}).to_csv(os.path.join(d, "codifica_secondo.csv"), index=False)


def figure(Lt, nil, cas):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 9)); nil.boundary.plot(ax=ax, color="#bbbbbb", lw=0.4)
    for cl, col in zip(CL, ("#1b9e77", "#d95f02", "#7570b3")):
        s = Lt[Lt.classe == cl]; s.plot(ax=ax, color=col, edgecolor=col, lw=0.6, label=f"{cl} ({len(s)})"); s.representative_point().plot(ax=ax, color=col, markersize=3)
    ax.legend(loc="lower left"); ax.set_axis_off(); ax.set_title("Base L v3 (candidata): tre classi, EPSG:32632")
    fig.savefig(os.path.join(HERE, "fig", "mappa_classi.png"), dpi=130, bbox_inches="tight"); plt.close(fig)
    ks = cas.classe.unique(); fig, axs = plt.subplots(len(ks), 1, figsize=(10, 2.2 + 0.32 * len(cas)))
    for ax, k in zip(axs, ks):
        c = cas[cas.classe == k]; y = range(len(c))[::-1]
        ax.barh(y, c.rimasti); ax.set_yticks(y); ax.set_yticklabels([s[:80] for s in c.passo], fontsize=7); ax.set_xscale("log"); ax.set_title(f"Cascata: {k}", fontsize=9)
        for yy, v in zip(y, c.rimasti): ax.text(max(v, 1), yy, f" {v:,}".replace(",", "."), va="center", fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig", "cascata.png"), dpi=120); plt.close(fig)


if __name__ == "__main__":
    main()
