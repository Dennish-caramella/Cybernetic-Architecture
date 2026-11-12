"""Base L v4 (ticket #37): lotti edificabili, lotti da riusare e aree di attivazione di Milano, EPSG:32632.
Parte da v3 (esperimenti/L_lotti_v3, fallimento documentato) con le sole modifiche [v4] della pre-registrazione
(esecuzioni/00_preregistrazione.txt): riuso limitato a un intorno dell'edificio fonte (G2), AT non residenziali all'attivazione (D4),
proprietà "non agganciata" (D7), copertura completa degli AT con diagnosi (D6), C5-fisico sui soli lotti non AT con due codificatori
ciechi esterni (G1, D2, D3), C9-AT dal censimento dello stato attuativo, nessuna sovrascrittura dei controlli (D1).
Uso: python run.py                         scarica le fonti mancanti, costruisce, calcola i criteri (C5 e C9 se i fogli sono compilati)
     python run.py --no-fetch              solo dalla cache
     python run.py --pilota                prova su 3 NIL: uscite solo in esecuzioni/<data>_pilota/
     python run.py --no-fetch --prepara-controlli   scrive immagini, fogli vuoti e chiavi; si rifiuta ed esce se uno qualsiasi esiste già
Riusa da v1 (esperimenti/L_lotti/run.py) parcels, share, dusaf_cat, rd e fetch.py; da v3 la codifica dello screening ds503 (sola lettura)."""
import glob, hashlib, json, os, shutil, subprocess, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
import numpy as np, pandas as pd, geopandas as gpd, shapely, pyogrio
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from sklearn.cluster import KMeans

HERE = os.path.dirname(os.path.abspath(__file__))
V1, V3 = os.path.join(HERE, "..", "L_lotti"), os.path.join(HERE, "..", "L_lotti_v3")
sys.path.insert(0, V1)
import run as v1  # noqa: E402
CACHE = os.path.join(HERE, "..", "_cache", "L_lotti_v4")
RAW4 = os.path.join(CACHE, "raw")  # [v4] catasto: tasselli di v1 + tasselli vuoti riscaricati
RAW, RAW2 = v1.RAW, os.path.join(HERE, "..", "_cache", "L_lotti_v2", "raw")
TILES = os.path.join(HERE, "..", "_cache", "L_lotti_v2", "orto", "tiles")  # tasselli AGEA condivisi con v2/v3
CRS, SEED = 32632, 42
T0 = time.time()
log = lambda *a: print(f"[{time.time() - T0:6.0f}s]", *a, file=sys.stderr, flush=True)

P = dict(  # tutti [H]; testo delle regole in esecuzioni/00_preregistrazione.txt
    a_min_parcel=300.0, excl_share=0.5, occ_res_share=0.5, free_cover_max=0.10, snap_m=20.0,
    buffer_m=2.0, max_area_m2=60000.0, lot_min_m2=1500.0, att_min_m2=500.0, dual_min_m2=5000.0, green_deficit_q=0.25,
    storey_m=3.2, yield_=0.70, gfa_dw=80.0, fars=(0.5, 1.0, 2.0),
    dusaf_conf_comune=("131", "132", "133", "134", "1412"),
    riuso_intorno_m=10.0, riuso_intorno_sens=(5.0, 20.0),   # [v4] G2: intorno dell'edificio fonte (D.M. 1444/1968 art. 9 [S])
    seed_campione=4511, seed_dennis=4512, seed_screening=3513, n_lotti=120, n_base=100, px=800, lotto_grande_m2=10000.0,
    n_dennis={"lotto edificabile": 7, "lotto da riusare": 5, "area di attivazione": 3, "particella qualsiasi": 5},
    orto_service="https://www.cartografia.servizirl.it/arcgis2/rest/services/BaseMap/Ortofoto2018_2019/ImageServer",
    soglia_C5a=0.70, soglia_C5b=0.25, soglia_kappa=0.60, soglia_C7=16, soglia_C9b=20, overlap_m2=1.0,
)
TILE = dict(x0=-5120900.0, y0=9998100.0, res={9: 3.9687579375158752, 10: 2.6458386250105836, 11: 1.3229193125052918,
                                               12: 0.5291677250021167, 13: 0.26458386250105836})
DS2813 = ("https://dati.comune.milano.it/dataset/49d2896c-abba-44e5-9a53-c19332a275b3/resource/bbc7d511-f52d-4fe0-a7c7-aa7e5f5dceb5/"
          "download/ds2813_spotted-milan-urbangreenindex-nil-01072024_31072024.geojson")
SRC = dict(v1.SRC)
SRC["ds2813"] = ("Comune di Milano, Indice di verde urbano per NIL, luglio 2024 (ds2813, SPOTTED)", "CC BY 4.0")
SRC["orto"] = ("AGEA, Ortofoto 2018-2019, servizio Regione Lombardia BaseMap/Ortofoto2018_2019", "proprietà AGEA: visione e stampa con citazione [S]")
SRC["censimento"] = ("Censimento dello stato attuativo degli AT (censimento_AT/consenso.csv, fonti con URL e data per poligono)", "fonti citate per riga")
CL = ("lotto da riusare", "lotto edificabile", "area di attivazione")
CTRL = {k: os.path.join(HERE, k) for k in ("controllo_codificatore_1", "controllo_codificatore_2", "controllo_umano", "chiavi", "censimento_AT")}
LCD = set("LCD")


def cap(area, far):
    return np.floor(P["yield_"] * far * np.asarray(area, float) / P["gfa_dw"]).astype(int)


def wil(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, c - h, c + h


def wilson(k, n):
    p, lo, hi = wil(k, n); return dict(k=int(k), n=int(n), p=round(p, 3), ic95=[round(lo, 3), round(hi, 3)])


def newcombe(ka, na, kb, nb):  # IC 95% di p_a - p_b (metodo 10 di Newcombe), su p non arrotondati
    a, b = wil(ka, na), wil(kb, nb); d = a[0] - b[0]
    return round(d, 3), [round(d - np.hypot(a[0] - a[1], b[2] - b[0]), 3), round(d + np.hypot(a[2] - a[0], b[0] - b[1]), 3)]


def kappa(a, b):
    a, b = np.asarray(a), np.asarray(b); po = (a == b).mean()
    pe = sum((a == c).mean() * (b == c).mean() for c in set(a) | set(b))
    return round(float((po - pe) / (1 - pe)), 3), round(float(po), 3)


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
    S = E.dissolve("gruppo", aggfunc={"ref": ";".join, key: "first"})
    S["n_particelle"] = E.groupby("gruppo").size(); S["area_m2"] = S.area
    return S.reset_index(drop=True)


# ---------------------------------------------------------------- ortofoto (come v3)
def tile(level, r, c):
    p = os.path.join(TILES, str(level), f"{r}_{c}.img")
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        for i in range(5):
            try:
                b = urllib.request.urlopen(urllib.request.Request(f"{P['orto_service']}/tile/{level}/{r}/{c}", headers={"User-Agent": "tesi-base-L/4.0"}), timeout=60).read(); break
            except Exception as e:
                log("retry tassello", level, r, c, e); time.sleep(3 * (i + 1))
        else:
            raise SystemExit("tassello non scaricato")
        open(p + ".part", "wb").write(b); os.replace(p + ".part", p)
    return p


def orto_image(geom, path, px):
    from PIL import Image, ImageDraw
    x0, y0, x1, y1 = geom.bounds; m = max(x1 - x0, y1 - y0) * 0.25 + 15; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    half = max(x1 - x0, y1 - y0) / 2 + m
    X0, Y0, X1, Y1 = cx - half, cy - half, cx + half, cy + half
    level = max(l for l in TILE["res"] if 2 * half / TILE["res"][l] <= 1600 or l == 9)
    res = TILE["res"][level]; s = 256 * res
    c0, c1 = int((X0 - TILE["x0"]) // s), int((X1 - TILE["x0"]) // s); r0, r1 = int((TILE["y0"] - Y1) // s), int((TILE["y0"] - Y0) // s)
    rc = [(r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)]
    with ThreadPoolExecutor(6) as ex: files = list(ex.map(lambda t: tile(level, *t), rc))
    mos = Image.new("RGB", ((c1 - c0 + 1) * 256, (r1 - r0 + 1) * 256), "white")
    for (r, c), f in zip(rc, files):
        mos.paste(Image.open(f).convert("RGB"), ((c - c0) * 256, (r - r0) * 256))
    ox, oy = TILE["x0"] + c0 * s, TILE["y0"] - r0 * s
    box = ((X0 - ox) / res, (oy - Y1) / res, (X1 - ox) / res, (oy - Y0) / res)
    im = mos.crop(tuple(int(round(v)) for v in box)).resize((px, px)); d = ImageDraw.Draw(im); k = px / (2 * half)
    for poly in shapely.get_parts(geom):
        for ring in [poly.exterior, *poly.interiors]:
            d.line([((x - X0) * k, (Y1 - y) * k) for x, y in zip(*ring.xy)], fill=(255, 0, 0), width=2)
    d.text((5, px - 14), f"{2 * half:.0f} m  AGEA 2018-2019 RL", fill=(255, 255, 0))
    im.save(path, quality=90)


# ---------------------------------------------------------------- catasto [v4, correzione dei dati]
def catasto_v4():
    """v1 (fetch.tile) ha salvato come vuoti i tasselli per cui il WFS ha risposto con ServiceException ("Richiesta non valida", frequente con
    count=2000) [V, 12/11]. Qui: copia dei tasselli non vuoti di v1; i vuoti che toccano il Comune si riscaricano a riquadri,
    con più valori di count e sotto-riquadri, senza startIndex. Ritorna la tabella dei tasselli riscaricati."""
    import fetch
    d = os.path.join(RAW4, "catasto"); os.makedirs(d, exist_ok=True)
    city = shapely.union_all(gpd.read_file(os.path.join(RAW, "ds964_nil.geojson")).to_crs(6706).geometry.values); rows = []
    for f in sorted(glob.glob(os.path.join(RAW, "catasto", "*.json"))):
        out = os.path.join(d, os.path.basename(f)); i, j = map(int, os.path.basename(f)[:-5].split("_"))
        a, b = fetch.LAT0 + i * fetch.STEP, fetch.LON0 + j * fetch.STEP
        box = shapely.box(b, a, b + fetch.STEP, a + fetch.STEP); n1 = len(json.load(open(f)))
        if not os.path.exists(out):
            if n1 or not box.intersects(city): shutil.copy(f, out)
            else:
                res = {}
                def q(la, lo, st):  # [V] il WFS dà eccezioni o tronca (count-1) per certe coppie riquadro/count: prova più count, altrimenti divide
                    bbox = f"{la:.5f},{lo:.5f},{la + st:.5f},{lo + st:.5f},urn:ogc:def:crs:EPSG::6706"
                    for cnt in (5000, 3000, 2000, 1500, 500):
                        x = fetch.get(fetch.WFS + "?" + urllib.parse.urlencode({"service": "WFS", "version": "2.0.0", "request": "GetFeature", "typeNames": "CP:CadastralParcel", "count": cnt, "bbox": bbox}))
                        ms = fetch.MEM.findall(x)
                        if "ServiceException" not in x and len(ms) < cnt - 1: break
                    else:
                        if st < fetch.STEP / 16: raise SystemExit(f"tassello {i}_{j}: risposte WFS non complete")
                        return [q(la + di * st / 2, lo + dj * st / 2, st / 2) for di in (0, 1) for dj in (0, 1)]
                    for m in ms:
                        r, p = fetch.REF.search(m), fetch.POS.search(m)
                        if r and p and r.group(1).startswith("F205"):
                            v = [float(z) for z in p.group(1).split()]; res[r.group(1)] = [[round(v[k + 1], 7), round(v[k], 7)] for k in range(0, len(v) - 1, 2)]
                q(a, b, fetch.STEP); res = [[k, v] for k, v in sorted(res.items())]
                json.dump(res, open(out + ".part", "w"), separators=(",", ":")); os.replace(out + ".part", out); log("tassello riscaricato", i, j, len(res))
        if not n1 and box.intersects(city):
            rows.append(dict(tassello=f"{i}_{j}", quota_nel_comune=round(box.intersection(city).area / box.area, 3), particelle_v1=0, particelle_v4=len(json.load(open(out))),
                             scaricato_utc=time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(os.path.getmtime(out)))))
    return pd.DataFrame(rows)


def parcels():
    old = v1.RAW; v1.RAW = RAW4
    try: return v1.parcels()
    finally: v1.RAW = old


# ---------------------------------------------------------------- costruzione
def build(pilota):
    nil = v1.rd("ds964_nil.geojson")[["ID_NIL", "NIL", "geometry"]]
    if pilota: nil = nil[nil.ID_NIL.isin(pilota)]
    city = shapely.union_all(nil.geometry.values)
    D = parcels(); rp = D.geometry.representative_point()
    D["in_city"] = shapely.contains_xy(city, rp.x.values, rp.y.values)
    D["nil_id"] = gpd.sjoin(gpd.GeoDataFrame(geometry=rp, crs=CRS), nil, predicate="within", how="left").groupby(level=0).ID_NIL.first().reindex(D.index).values
    U = D[D.land & D.in_city].copy(); W = [("comune", "particelle di terreno nel Comune (catasto, mappale numerico)", len(U))]
    ux, uy = U.geometry.representative_point().x.values, U.geometry.representative_point().y.values
    tree = shapely.STRtree(U.geometry.values)

    def to_parcel(g):
        i, j = tree.query(g, predicate="within"); out = np.full(len(g), -1); out[i] = U.index.values[j]
        miss = np.where(out < 0)[0]
        if len(miss):
            k, _ = tree.query_nearest(g[miss], max_distance=P["snap_m"], return_distance=True, all_matches=False); out[miss[k[0]]] = U.index.values[k[1]]
        return out

    V = gpd.read_file(os.path.join(RAW, "dbt", "UN_VOL.shp"), columns=["UN_VOL_AV", "UN_VOL_POR", "CEDIUV"]).to_crs(CRS)
    V = V[(V.UN_VOL_POR != "02") & (V.UN_VOL_AV.astype(float) > 0.5)].reset_index(drop=True)
    V["geometry"] = shapely.force_2d(V.geometry.values)
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

    pg = {k: v1.rd(f"pgt_{k}.geojson") for k in ("at", "servizi", "dism", "agr", "pae", "naf")}
    at = pg["at"]; is_pcu = at.NOME_AMB.str.contains("PCU", na=False); srv = pg["servizi"]; atn = at[~is_pcu]
    du = v1.rd("dusaf8.geojson"); cod = du.COD_TOT.astype(str); du["cat"] = cod.map(v1.dusaf_cat)
    lay = {"pgt_srv_verde": srv[srv.LEGENDA == "Aree a verde"], "pgt_srv_ist": srv[srv.LEGENDA.isin(["Istruzione", "Università e ricerca"])],
           "pgt_agr": pg["agr"], "pgt_pae": pg["pae"], "pgt_tras": atn, "pgt_naf": pg["naf"],
           "dusaf_13": du[cod.isin(["133", "134"])], "dusaf_conf": du[cod.isin(P["dusaf_conf_comune"])], "dusaf_1412": du[cod == "1412"], "dusaf_cava": du[cod.isin(["131", "132"])]}
    for c in ("wat", "infra", "green", "agr", "wood"): lay[f"dusaf_{c}"] = du[du.cat == c]
    for k, g in lay.items(): U[k] = v1.share(U.geometry, g)
    U["pcu"] = shapely.contains_xy(shapely.union_all(shapely.make_valid(at[is_pcu].geometry.values)), ux, uy)
    U["is_at"] = (U.pgt_tras >= P["excl_share"]) & ~U.pcu
    deg = pg["dism"][pg["dism"].NOTE.astype(str).str.startswith("ex AMB_DEG")]
    U["amb_deg"] = shapely.contains_xy(shapely.union_all(shapely.make_valid(deg.geometry.values)), ux, uy)
    U["funzione_at"], U["at_nome"] = None, None  # [v4] D4: DFUN_PREV1 del poligono AT non PCU che contiene il punto interno
    for f, nm, g in zip(atn.DFUN_PREV1, atn.NOME_AMB, atn.geometry):
        m = shapely.contains_xy(shapely.make_valid(g), ux, uy) & U.funzione_at.isna(); U.loc[m, "funzione_at"] = f; U.loc[m, "at_nome"] = nm
    log("quote PGT e DUSAF")

    c677 = v1.rd("ds677_patrimonio.geojson"); c677 = c677[c677.MILANO == "SI"]
    key = lambda d: list(zip(pd.to_numeric(d.FOGLIO, errors="coerce"), pd.to_numeric(d.MAPPALE, errors="coerce")))
    k_all, k_ter = set(key(c677)), set(key(c677[c677.TIPO == "TERRENO"]))
    fm = list(zip(U.foglio, U.mappale)); U["comunale"] = [x in k_all for x in fm]; U["comunale_terreno"] = [x in k_ter for x in fm]
    sfm = set(fm); aggancio = {"chiavi_ds677": len(k_all), "agganciate": len(k_all & sfm), "quota": round(len(k_all & sfm) / len(k_all), 3),
                               "chiavi_terreno": len(k_ter), "terreno_agganciate": len(k_ter & sfm), "quota_terreno": round(len(k_ter & sfm) / len(k_ter), 3)}
    dem = pd.concat([v1.rd("ds2688_demanio_aree.geojson").assign(tipo_dem="area"), v1.rd("ds2689_demanio_fabbricati.geojson").assign(tipo_dem="fabbricato")], ignore_index=True)
    dem = gpd.GeoDataFrame(dem, geometry="geometry", crs=CRS); dem["parcel"] = to_parcel(dem.geometry.values)
    U["demanio"] = U.index.isin(dem.parcel)
    U["demanio_disp_area"] = U.index.isin(dem.parcel[(dem.tipo_dem == "area") & (dem["Categoria Patrimoniale"] == "PATRIMONIO DISPONIBILE")])

    # ------------------------------------------------------------ lotti da riusare (R1-R4; [v4] R3 con intorno)
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
    bv = V.groupby("CEDIUV"); big = V.loc[bv.fp.idxmax()].set_index("CEDIUV")
    E_src = src.groupby("edificio").agg(fonti_riuso=("fonte", lambda v: "+".join(sorted(set(v)))), nota=("nota", lambda v: " | ".join(sorted(set(map(str, v))))))
    E_src["parcel"] = big.parcel.reindex(E_src.index).values; E_src["vol"] = bv.vol.sum().reindex(E_src.index).values
    E_src = E_src[E_src.parcel >= 0]; W += [("riuso", "edifici fonte su una particella di terreno del Comune", len(E_src))]
    excl_plan = ["pgt_srv_verde", "pgt_agr", "pgt_pae", "pgt_srv_ist", "dusaf_wat"]; excl_use = ["dusaf_infra", "dusaf_green", "dusaf_agr", "dusaf_wood"]
    fp_geom = V[V.CEDIUV.isin(E_src.index)].groupby("CEDIUV").geometry.apply(lambda s: shapely.union_all(s.values))

    def riuso(E_src, W):
        RP = E_src.reset_index().groupby("parcel").agg(edifici_fonte=("edificio", ";".join), fonti_riuso=("fonti_riuso", lambda v: "+".join(sorted(set("+".join(v).split("+"))))),
                                                        nota=("nota", lambda v: " | ".join(v)[:300]), volume_fonte_m3=("vol", "sum"))
        RP = U.loc[RP.index].join(RP); W += [("riuso", "particelle con edifici fonte (aggregazione, non filtro)", len(RP))]
        RP = RP[RP.area_m2 >= P["a_min_parcel"]]; W += [("riuso", f"particella >= {P['a_min_parcel']:.0f} m²", len(RP))]
        RP = RP[~(RP[excl_plan] >= P["excl_share"]).any(axis=1)]; W += [("riuso", "non verde/agricolo/paesaggio/istruzione PGT, non acque DUSAF (>= 0,5)", len(RP))]
        RP = RP[RP.is_at | ~(RP[excl_use] >= P["excl_share"]).any(axis=1)]; W += [("riuso", "non infrastrutture/verde/agricolo/boschi DUSAF (>= 0,5), salvo particelle AT", len(RP))]
        RP = RP[~RP.pcu]; W += [("riuso", "fuori dai PCU", len(RP))]
        other = V[V.parcel.isin(RP.index)]; g3, geo, sens, fpa = [], [], [], []
        for p, row in RP.iterrows():  # v3: particella meno gli altri edifici; [v4] intersecata con impronta fonte + intorno
            ids = row.edifici_fonte.split(";")
            o = other[(other.parcel == p) & ~other.CEDIUV.isin(ids)].geometry.values
            gv3 = shapely.difference(row.geometry, shapely.union_all(o)) if len(o) else row.geometry
            fp = shapely.union_all(fp_geom.reindex(ids).dropna().values)
            g3.append(gv3); fpa.append(shapely.intersection(row.geometry, fp).area)
            geo.append(shapely.intersection(gv3, shapely.buffer(fp, P["riuso_intorno_m"])))
            sens.append([shapely.intersection(gv3, shapely.buffer(fp, d)).area for d in P["riuso_intorno_sens"]])
        RP = RP.assign(geom_v3=g3, area_v3_regola=[g.area for g in g3], impronta_fonte_m2=fpa,
                       area_intorno_5m=[s[0] for s in sens], area_intorno_20m=[s[1] for s in sens])
        return RP.set_geometry(geo, crs=CRS)

    cand = riuso(E_src, [])
    sid_s = E_src.index[E_src.fonti_riuso == "ds503"]
    cand = cand[cand.edifici_fonte.map(lambda s: any(x in sid_s for x in s.split(";")))]
    scr = screening(cand, pilota)
    conf = set() if scr is None else set(scr.parcel[scr.Q1.eq("D") | scr.tetto.isin(["T2", "T3"])])
    W += [("riuso:fonti", "screening ds503: lotti candidati", len(cand)), ("riuso:fonti", "screening ds503: lotti confermati (Q1 = D o tetto T2/T3)", len(conf))]
    E_src = E_src[(E_src.fonti_riuso != "ds503") | E_src.parcel.isin(conf)]
    W += [("riuso", "edifici fonte confermati (diruti DBT o ds503 confermati dallo screening)", len(E_src))]
    RP = riuso(E_src, W)
    rilascio = shapely.union_all([shapely.difference(a, b) for a, b in zip(RP.geom_v3, RP.geometry)])  # [v4] parte di particella liberata
    log("lotti da riusare", len(RP))

    # ------------------------------------------------------------ lotti edificabili e aree di attivazione
    e_at = U.is_at; e_d13 = U.dusaf_13 >= P["excl_share"]
    e_com = U.comunale_terreno & (U.cover < P["free_cover_max"]) & (U.dusaf_conf >= P["excl_share"])
    entry_e = e_at | U.amb_deg | e_d13 | U.demanio_disp_area | e_com
    entry_a = (U.dusaf_1412 >= P["excl_share"]) | (U.dusaf_cava >= P["excl_share"])
    U["origine"] = np.select([e_at, U.amb_deg, e_d13, U.demanio_disp_area, e_com, U.dusaf_cava >= P["excl_share"]],
                             ["AT", "AMB_DEG", "DUSAF13", "DEMANIO", "COMUNE", "DUSAF_CAVA"], "DUSAF1412")
    A = U[entry_e | entry_a]
    W += [("edificabile+attivazione", "ingresso E1 (AT, AMB_DEG, DUSAF 133/134, Demanio disp., terreno comunale con DUSAF 131-134/1412)", int(entry_e.sum())),
          ("edificabile+attivazione", "ingresso E1 o A1 (anche DUSAF 1412, 131/132)", len(A))]
    occ = (A.n_vol > 0) & (A.res_share.fillna(0) >= P["occ_res_share"])
    for lab, m in ((f"particella >= {P['a_min_parcel']:.0f} m²", A.area_m2 >= P["a_min_parcel"]), ("fuori dai PCU", ~A.pcu),
                   ("non acque DUSAF (>= 0,5)", A.dusaf_wat < P["excl_share"]),
                   ("non infrastrutture/agricolo/boschi/verde in uso DUSAF (>= 0,5), salvo particelle AT", A.is_at | ~(A[excl_use] >= P["excl_share"]).any(axis=1)),
                   ("non agricolo/istruzione PGT (>= 0,5)", ~(A[["pgt_agr", "pgt_srv_ist"]] >= P["excl_share"]).any(axis=1)),
                   ("non residenza occupata (quota residenziale del volume < 0,5)", ~occ)):
        if lab.startswith("non residenza"): d5 = A[A.is_at & occ.reindex(A.index)]  # D5: particelle AT tolte da questo filtro
        A = A[m.reindex(A.index)]; W += [("edificabile+attivazione", lab, len(A))]
    W += [("informativo", "particelle AT tolte dal filtro residenza occupata (D5)", len(d5))]
    nonres = A.is_at & A.funzione_at.notna() & (A.funzione_at != "RESIDENZIALE")  # [v4] D4
    vinc = (A.pgt_srv_verde >= P["excl_share"]) | (A.pgt_pae >= P["excl_share"])
    to_att = vinc | ~entry_e.reindex(A.index) | nonres
    A["motivo"] = np.select([A.pgt_srv_verde >= P["excl_share"], A.pgt_pae >= P["excl_share"], nonres, A.origine == "DUSAF_CAVA"],
                            ["verde di servizio PGT", "valore paesaggistico PGT", "AT a funzione prevalente non residenziale (PGT)", "cava o discarica DUSAF"], "area verde incolta DUSAF 1412")
    Ae, Aa = A[~to_att], A[to_att].assign(origine=lambda d: d.origine + " / " + d.motivo)
    W += [("edificabile", "particelle verso l'abitazione", len(Ae)), ("attivazione", "particelle verso l'attivazione (vincolo PGT, AT non residenziale [v4] o ingresso solo verde/cava)", len(Aa))]
    Se, Sa = groups(Ae, "origine"), groups(Aa, "origine")
    W += [("edificabile", "gruppi per adiacenza (aggregazione, non filtro)", len(Se)), ("attivazione", "gruppi per adiacenza (aggregazione, non filtro)", len(Sa))]
    small = Se[(Se.area_m2 >= P["att_min_m2"]) & (Se.area_m2 < P["lot_min_m2"])].assign(origine=lambda d: d.origine + " / taglia < 1.500 m²")
    Se = Se[Se.area_m2 >= P["lot_min_m2"]]; W += [("edificabile", f"lotto >= {P['lot_min_m2']:.0f} m²", len(Se))]
    Sa = pd.concat([Sa[Sa.area_m2 >= P["att_min_m2"]], small], ignore_index=True)
    W += [("attivazione", f"gruppi >= {P['att_min_m2']:.0f} m² (A2) + gruppi edificabili 500-1.500 m² (A3)", len(Sa))]

    # ------------------------------------------------------------ tabella unica, sovrapposizioni, attributi
    RPo = RP.drop(columns="geom_v3").reset_index(drop=True).assign(classe=CL[0], origine=RP.fonti_riuso.values, n_particelle=1)
    Lt = gpd.GeoDataFrame(pd.concat([RPo, Se.assign(classe=CL[1]), Sa.assign(classe=CL[2])], ignore_index=True)[
        ["ref", "classe", "origine", "n_particelle", "edifici_fonte", "fonti_riuso", "nota", "volume_fonte_m3", "area_v3_regola", "impronta_fonte_m2",
         "area_intorno_5m", "area_intorno_20m", "geometry"]], geometry="geometry", crs=CRS)
    Lt["geometry"] = shapely.make_valid(shapely.force_2d(Lt.geometry.values))
    pt = Lt.geometry.representative_point(); Lt["cx"], Lt["cy"] = pt.x.round(1), pt.y.round(1)
    Lt["_o"] = Lt.classe.map({c: i for i, c in enumerate(CL)})
    Lt = Lt.sort_values(["_o", "cx", "cy"]).reset_index(drop=True)
    Lt.insert(0, "id", Lt.classe.map({CL[0]: "R", CL[1]: "E", CL[2]: "A"}) + pd.Series(range(1, len(Lt) + 1)).astype(str).str.zfill(5))
    g = Lt.geometry.values.copy(); t = shapely.STRtree(g)
    for n in range(len(g)):  # precedenza: riuso > edificabile > attivazione, poi id
        prev = [m for m in t.query(g[n], predicate="intersects") if m < n]
        if prev:
            q = shapely.make_valid(shapely.difference(g[n], shapely.union_all(g[prev]), grid_size=0.01))
            g[n] = shapely.union_all([p for p in shapely.get_parts(q) if p.geom_type == "Polygon" and p.area > 0.01]) if not q.is_empty else q
    Lt["geometry"] = shapely.force_2d(g); Lt["area_m2"] = Lt.area.round(1)
    keep = (~Lt.geometry.is_empty) & np.where(Lt.classe == CL[1], Lt.area_m2 >= P["lot_min_m2"], np.where(Lt.classe == CL[2], Lt.area_m2 >= P["att_min_m2"], Lt.area_m2 > 1))
    for c, kk in zip(CL, ("riuso", "edificabile", "attivazione")): W += [(kk, "dopo la rimozione delle sovrapposizioni (sopra il minimo di classe)", int((keep & (Lt.classe == c)).sum()))]
    Lt = Lt[keep].reset_index(drop=True)
    pt = Lt.geometry.representative_point(); Lt["cx"], Lt["cy"] = pt.x.round(1), pt.y.round(1)
    pg_ = gpd.GeoDataFrame(geometry=pt, crs=CRS)
    jn = gpd.sjoin(pg_, nil, predicate="within", how="left").groupby(level=0)
    Lt["nil_id"] = jn.ID_NIL.first().reindex(Lt.index).astype("Int64"); Lt["nil_nome"] = jn.NIL.first().reindex(Lt.index)
    ja = gpd.sjoin(pg_, atn[["OBJECTID", "NOME_AMB", "DFUN_PREV1", "geometry"]], predicate="within", how="left").groupby(level=0)
    Lt["at_objectid"] = ja.OBJECTID.first().reindex(Lt.index).astype("Int64")
    Lt["ambito_pgt"] = ja.NOME_AMB.first().reindex(Lt.index); Lt["funzione_at"] = ja.DFUN_PREV1.first().reindex(Lt.index)
    Lt["quota_at"] = v1.share(Lt.geometry, atn).round(3); Lt["lotto_at"] = (Lt.quota_at >= P["excl_share"]).astype(int)
    gv = gpd.read_file(os.path.join(RAW2, "ds2813_verde_nil.geojson"), ignore_geometry=True).set_index("ID_NIL").value
    Lt["nil_indice_verde"] = Lt.nil_id.map(gv).round(3); Lt["nil_deficit_verde"] = (Lt.nil_indice_verde <= gv.quantile(P["green_deficit_q"])).astype(int)
    r, e, a = (Lt.classe == c for c in CL)
    Lt["anche_attivazione"] = (e & (Lt.area_m2 >= P["dual_min_m2"]) & (Lt.nil_deficit_verde == 1)).astype(int)
    for f, nm in zip(P["fars"], ("cap_far05", "cap_far1", "cap_far2")): Lt[nm] = np.where(a, 0, cap(Lt.area_m2, f))
    for c in ("volume_fonte_m3", "area_v3_regola", "impronta_fonte_m2", "area_intorno_5m", "area_intorno_20m"): Lt[c] = Lt[c].round(1)
    Lt["cap_recupero"] = pd.Series(cap(Lt.volume_fonte_m3.fillna(0) / P["storey_m"], 1.0), index=Lt.index, dtype="Int64").where(r)
    Lt["scenario_principale"] = np.select([r & Lt.fonti_riuso.str.contains("dbt_diruto", na=False), r], ["demolizione e ricostruzione", "recupero"], "")
    Lt["base_scenario"] = np.where(r, "regola di default (fonte)", "")
    if scr is not None:
        t = scr[scr.tetto.isin(["T1", "T2", "T3"])].set_index("ref").tetto; m = r & Lt.ref.isin(t.index)
        Lt.loc[m, "scenario_principale"] = np.where(Lt.ref[m].map(t) == "T3", "demolizione e ricostruzione", "recupero"); Lt.loc[m, "base_scenario"] = "screening ds503 v3 su ortofoto (T1-T3)"
    Lt["conferma_screening"] = (r & Lt.ref.isin(U.ref[list(conf)])).astype(int)
    ar = U.area_m2; com_a, dem_a = ar[U.comunale], ar[U.demanio]
    idx = U.reset_index().set_index("ref")["index"]
    refs = [[idx[x] for x in s.split(";") if x in idx.index] for s in Lt.ref]
    Lt["quota_comunale"] = [min(1, round(com_a.reindex(rr).fillna(0).sum() / A_, 3)) for rr, A_ in zip(refs, Lt.area_m2)]
    Lt["quota_demanio"] = [min(1, round(dem_a.reindex(rr).fillna(0).sum() / A_, 3)) for rr, A_ in zip(refs, Lt.area_m2)]
    Lt["proprieta"] = np.select([Lt.quota_demanio >= 0.5, Lt.quota_comunale >= 0.5], ["Demanio", "pubblico comunale"], "non agganciata")  # [v4] D7
    Lt["proprieta_conflitto"] = ((Lt.quota_demanio >= 0.5) & (Lt.quota_comunale >= 0.5)).astype(int)
    bon = v1.rd("ds600_bonifiche.geojson"); bon_lot = set(gpd.sjoin(bon[["geometry"]], Lt[["geometry"]], predicate="within").index_right)
    sh = {k: v1.share(Lt.geometry, v) for k, v in (("naf", lay["pgt_naf"]), ("pae", lay["pgt_pae"]), ("bon", pg["dism"][pg["dism"].DBONIFICA == "SI"]))}
    dsa = set(gpd.sjoin(dem[dem["Categoria Patrimoniale"] == "DEMANIO STORICO ARTISTICO"][["geometry"]], Lt[["geometry"]], predicate="within").index_right)
    Lt["vincoli_noti"] = ["; ".join(v for v, c in (("bonifica (ds600 o PGT DBONIFICA=SI)", i in bon_lot or sh["bon"][i] > 0.1), ("nucleo di antica formazione PGT", sh["naf"][i] > 0.1),
                                                  ("area di valore paesaggistico PGT", sh["pae"][i] > 0.1), ("demanio storico-artistico", i in dsa)) if c) for i in range(len(Lt))]
    stato(Lt)
    base = "catasto; dbt; pgt; dusaf; nil; ds677; demanio; ds600; ds2813"
    Lt["fonti"] = np.where(r, base + "; " + Lt.fonti_riuso.fillna("").str.replace("+", "; ").str.replace("dbt_diruto", "dbt"), base)
    Lt["licenze"] = "CC BY 4.0; CC BY 2.5 IT; CC BY 3.0 IT; CC0; PGT regionale [L]"
    Lt = Lt.drop(columns="_o")
    log("lotti", Lt.classe.value_counts().to_dict())
    cov, diag = copertura(at, is_pcu, Lt, U, D, du, pg["dism"][pg["dism"].DBONIFICA == "SI"])
    # [v4] spostamenti dovuti all'intorno del riuso (G2)
    E_u, A_u = (shapely.union_all(Lt.geometry.values[(Lt.classe == c).values]) for c in CL[1:])
    mv = {"intorno_m": P["riuso_intorno_m"], "ha_regola_v3": round(RP.area_v3_regola.sum() / 1e4, 2), "ha_intorno": round(RP.area.sum() / 1e4, 2),
          "ha_liberati": round(rilascio.area / 1e4, 2), "ha_liberati_a_edificabili": round(shapely.intersection(rilascio, E_u).area / 1e4, 2),
          "ha_liberati_a_attivazione": round(shapely.intersection(rilascio, A_u).area / 1e4, 2)}
    mv["ha_liberati_fuori_base"] = round(mv["ha_liberati"] - mv["ha_liberati_a_edificabili"] - mv["ha_liberati_a_attivazione"], 2)
    for f, nm in zip(P["fars"], ("far05", "far1", "far2")):
        mv[f"alloggi_riuso_v3_{nm}"] = int(cap(RP.area_v3_regola, f).sum()); mv[f"alloggi_riuso_v4_{nm}"] = int(cap(RP.area, f).sum())
        mv[f"alloggi_su_liberati_edificabili_{nm}_I"] = int(cap(mv["ha_liberati_a_edificabili"] * 1e4, f))
    for d, c in zip(P["riuso_intorno_sens"], ("area_intorno_5m", "area_intorno_20m")):
        mv[f"sens_{d:g}m_ha"] = round(RP[c].sum() / 1e4, 2); mv[f"sens_{d:g}m_alloggi_far1"] = int(cap(RP[c], 1.0).sum())
    rr = (RP.area / RP.impronta_fonte_m2.clip(lower=1))
    mv["rapporto_area_impronta"] = {"mediana": round(float(rr.median()), 2), "p99": round(float(rr.quantile(0.99)), 2), "max": round(float(rr.max()), 2),
                                    "v3_mediana": round(float((RP.area_v3_regola / RP.impronta_fonte_m2.clip(lower=1)).median()), 2)}
    nr = Lt[a & Lt.origine.str.contains("non residenziale")]
    mv_d4 = {"lotti": len(nr), "ha": round(nr.area_m2.sum() / 1e4, 2), "alloggi_far1_se_edificabili_I": int(cap(nr.area_m2[nr.area_m2 >= P["lot_min_m2"]], 1.0).sum()),
             "per_ambito": nr.groupby("ambito_pgt").area_m2.sum().div(1e4).round(2).to_dict()}
    extra = {"riuso_intorno": mv, "at_non_residenziali": mv_d4, "aggancio_ds677": aggancio,
             "d5_residenza_occupata_AT": {"particelle": len(d5), "ha": round(d5.area_m2.sum() / 1e4, 2), "copertura_lt_0_10": int((d5.cover < 0.10).sum()),
                                          "per_ambito": d5.groupby("at_nome").area_m2.sum().div(1e4).round(2).to_dict()}}
    return Lt, U, nil, W, cov, diag, extra


def stato(Lt):
    """[v4] stato_attuativo e disponibile_da dei lotti AT dal censimento C9 (censimento_AT/consenso.csv), se esiste."""
    f = os.path.join(CTRL["censimento_AT"], "consenso.csv"); at = Lt.lotto_at == 1
    Lt["stato_attuativo"] = np.where(at, "in attesa del censimento", "non applicabile (lotto non AT)"); Lt["fonte_stato"] = ""; Lt["disponibile_da"] = np.where(at, "da censire", "")
    if os.path.exists(f):
        c = pd.read_csv(f, dtype=str).fillna("").set_index("objectid"); o = Lt.at_objectid.astype(str)
        m = at & o.isin(c.index)
        Lt.loc[m, "stato_attuativo"] = o[m].map(c.categoria); Lt.loc[m, "fonte_stato"] = o[m].map(c.fonte_url + " (" + c.data_fonte + ")")
        Lt.loc[m, "disponibile_da"] = np.where(o[m].map(c.get("attuazione_conclusa", pd.Series(dtype=str))).eq("si"), "oggi", "dopo l'attuazione")


def copertura(at, is_pcu, Lt, U, D, du, bon):
    """Tabella per tutti i 30 poligoni AT; [v4] copertura da qualsiasi particella e diagnosi delle parti fuori dall'universo."""
    tu, td_, tl, tdu = (shapely.STRtree(x) for x in (U.geometry.values, D.geometry.values, Lt.geometry.values, du.geometry.values))
    cod = du.COD_TOT.astype(str).values; bon_u = shapely.union_all(shapely.make_valid(bon.geometry.values)); rows, diag = [], []
    for oid, name, pcu, fun, g in zip(at.OBJECTID, at.NOME_AMB, is_pcu, at.DFUN_PREV1, shapely.make_valid(at.geometry.values)):
        a = g.area; row = dict(objectid=oid, ambito=name, pcu=int(pcu), funzione=fun, area_ha=round(a / 1e4, 2))
        uu = shapely.union_all(U.geometry.values[tu.query(g, predicate="intersects")])
        jd = td_.query(g, predicate="intersects"); dd = shapely.union_all(D.geometry.values[jd])
        row["universo_ha"] = round(shapely.intersection(g, uu).area / 1e4, 2); row["catasto_qualsiasi_ha"] = round(shapely.intersection(g, dd).area / 1e4, 2)
        row["senza_particella_ha"] = round(row["area_ha"] - row["catasto_qualsiasi_ha"], 2)
        j = tl.query(g, predicate="intersects"); cov = shapely.union_all(Lt.geometry.values[j]) if len(j) else shapely.Polygon()
        for c, k in zip(CL, ("riuso", "edificabile", "attivazione")):
            jj = j[Lt.classe.values[j] == c]
            row[f"{k}_ha"] = round(shapely.intersection(g, shapely.union_all(Lt.geometry.values[jj])).area / 1e4, 2) if len(jj) else 0.0
            row[f"{k}_n"] = len(jj)
        row["coperto_quota"] = round(shapely.intersection(g, cov).area / a, 3)
        rest = shapely.difference(g, cov); row["non_coperto_ha"] = round(rest.area / 1e4, 2)
        k = tdu.query(rest, predicate="intersects")
        ar = pd.Series(shapely.area(shapely.intersection(rest, du.geometry.values[k], grid_size=0.01)), index=cod[k]).groupby(level=0).sum().sort_values(ascending=False)
        row["dusaf_non_coperto_top3"] = "; ".join(f"{c} {v / 1e4:.1f} ha" for c, v in ar.head(3).items())
        row["bonifica_pgt_quota"] = round(shapely.intersection(g, bon_u).area / a, 3)
        rows.append(row)
        if pcu: continue
        out = shapely.difference(g, uu)  # parte dell'ambito fuori dall'universo: quali particelle la coprono
        for q in jd:
            ia = shapely.intersection(out, D.geometry.values[q]).area
            if ia > 100: diag.append(dict(objectid=oid, ambito=name, ref=D.ref.values[q], suffisso=D.ref.values[q].split(".")[-1], terreno=bool(D.land.values[q]),
                                          nel_comune=bool(D.in_city.values[q]), area_particella_m2=round(D.area_m2.values[q]), area_in_ambito_fuori_universo_m2=round(ia)))
        diag.append(dict(objectid=oid, ambito=name, ref="(nessuna particella)", suffisso="", terreno=False, nel_comune=False, area_particella_m2=0,
                         area_in_ambito_fuori_universo_m2=round(shapely.difference(out, dd).area)))
    return pd.DataFrame(rows).sort_values(["pcu", "ambito", "objectid"]), pd.DataFrame(diag)


def screening(cand, pilota):
    """R1 v3: codifica dello screening ds503 di v3, in sola lettura, unita per riferimento catastale. [v4] I candidati nuovi (particelle recuperate
    dai tasselli riscaricati o cambiate) non sono stati sottoposti a screening: non confermati (come Q1 = X), elencati in tabelle/screening_ds503_non_codificati.csv."""
    if pilota: return None
    k3 = pd.read_csv(os.path.join(V3, "tabelle", "screening_ds503_chiave.csv"), dtype={"codice": str, "ref": str})
    cod = pd.read_csv(os.path.join(V3, "tabelle", "screening_ds503_codifica.csv"), dtype=str).fillna("")
    S = pd.DataFrame({"ref": cand.ref.values, "parcel": cand.index.values}).merge(k3[["codice", "ref"]].merge(cod, on="codice", validate="1:1"), on="ref", how="left", validate="1:1").fillna("")
    S.loc[S.codice == "", "Q1"] = "X"
    S[S.codice == ""][["ref"]].to_csv(os.path.join(HERE, "tabelle", "screening_ds503_non_codificati.csv"), index=False)
    log("screening ds503: candidati", len(S), "codificati in v3", int((S.codice != "").sum()), "chiavi v3 non più candidate", int((~k3.ref.isin(S.ref)).sum()))
    return S


def content_hash(L):
    a = L.drop(columns="geometry").sort_values("id").to_csv(index=False, float_format="%.3f").encode()
    w = b"".join(shapely.to_wkb(shapely.normalize(shapely.set_precision(L.sort_values("id").geometry.values, 0.001))))
    return hashlib.sha256(a + w).hexdigest()


# ---------------------------------------------------------------- campione C5-fisico e controlli
def campione(Lt, U):
    """[v4] 120 lotti non AT (allocazione proporzionale, resti più grandi) + 100 particelle qualsiasi; seme 4511; codici C001-C220."""
    rng = np.random.default_rng(P["seed_campione"]); pop = Lt[Lt.lotto_at == 0]
    cnt = pop.classe.value_counts().reindex(list(CL[1:]) + [CL[0]]).fillna(0).astype(int)  # ordine fisso: E, A, R
    q = cnt / cnt.sum() * P["n_lotti"]; alloc = np.floor(q).astype(int)
    alloc[(q - alloc).sort_values(ascending=False, kind="stable").index[:P["n_lotti"] - alloc.sum()]] += 1
    alloc = alloc.clip(upper=cnt)
    sid = np.concatenate([rng.choice(pop.index[pop.classe == c].values, alloc[c], replace=False) for c in alloc.index])
    BU = U[U.area_m2 >= P["a_min_parcel"]]; bid = rng.choice(len(BU), P["n_base"], replace=False)
    camp = pd.concat([pd.DataFrame({"tipo": "lotto", "id": Lt.id[sid].values, "classe": Lt.classe[sid].values, "origine": Lt.origine[sid].values,
                                    "area_m2": Lt.area_m2[sid].values, "geometry": Lt.geometry[sid].values}),
                      pd.DataFrame({"tipo": "base", "id": BU.ref.values[bid], "classe": "particella qualsiasi", "origine": "",
                                    "area_m2": BU.area_m2.values[bid].round(1), "geometry": BU.geometry.values[bid]})], ignore_index=True)
    camp["codice"] = ["C%03d" % (i + 1) for i in np.argsort(rng.permutation(len(camp)))]
    # lotti già visti in v3 (IoU > 0,5 con un lotto del campione v3; base: stessa particella)
    k3 = pd.read_csv(os.path.join(V3, "tabelle", "campione_ortofoto.csv"), dtype=str)
    L3 = gpd.read_file(os.path.join(V3, "lotti_v3.gpkg"), layer="lotti", columns=["id"]); g3 = L3.geometry.values[L3.id.isin(k3.id).values]
    t3 = shapely.STRtree(g3); seen = []
    for tp, i_, g in zip(camp.tipo, camp.id, camp.geometry):
        if tp == "base": seen.append(int(i_ in set(k3.id))); continue
        j = t3.query(g, predicate="intersects")
        seen.append(int(any(shapely.intersection(g, g3[x]).area / shapely.union_all([g, g3[x]]).area > 0.5 for x in j)))
    camp["visto_v3"] = seen
    return camp.sort_values("codice").reset_index(drop=True), alloc.to_dict()


ISTR = """Codificatore {n} — Base L v4 (ticket #37). Codifica cieca su ortofoto.

Materiale in questa cartella: img/C001.jpg ... img/C220.jpg (ortofoto AGEA 2018-2019, Regione Lombardia; licenza di sola visione,
non diffondere) e il foglio vuoto codifica.csv. Lavora solo con questa cartella: non aprire altri file del progetto.

Ogni immagine mostra un'area con contorno ROSSO. Codifica ciò che sta DENTRO il contorno rosso, una riga per immagine.

Q1 copertura prevalente: la categoria che occupa la parte PIÙ GRANDE dell'area dentro il contorno (anche se non supera la metà;
non la più visibile né la più interessante). Una lettera:
 L libera: suolo nudo, sterrato, prato o incolto non curato, piazzale vuoto
 C cantiere
 D edificato dismesso o degradato: tetti danneggiati o crollati, vegetazione su edifici o piazzali, nessun segno d'uso
 U edificato o area in uso (inclusi cortili, parcheggi pieni, pertinenze)
 V verde curato (parco, giardino) o agricolo coltivato
 I infrastruttura in uso (binari attivi, strade, piazzali di servizio in uso)
 X non giudicabile
LCD quota dell'area dentro il contorno che è libera, in cantiere o dismessa (L + C + D insieme):
 0 meno di 1/4   1 da 1/4 a 1/2   2 da 1/2 a 3/4   3 oltre 3/4
eterogeneo: E se nessuna categoria supera la metà dell'area, altrimenti vuoto.
Q2 solo se nel contorno ci sono edifici (altrimenti vuoto):
 tetto: T1 integro / T2 danneggiato / T3 crollato o assente / T0 non visibile
 veg: V0 nessuna vegetazione spontanea su edifici o piazzali / V1 poca / V2 molta
 uso: U+ segni d'uso (auto, manutenzione, insegne) / U- nessun segno d'uso / U? incerto
nota: facoltativa, breve, senza virgole.

Consegna: codifica.csv compilato (220 righe); annota l'ora di inizio e di fine; calcola lo SHA-256 del file e consegnalo
al coordinatore prima di qualsiasi confronto. È uno screening visivo dall'alto, non una perizia.
"""
COLS = ["Q1", "LCD", "eterogeneo", "tetto", "veg", "uso", "nota"]


def prepara_controlli(Lt, camp):
    """[v4] D1/D2: scrive pacchetti dei codificatori, controllo di Dennis e chiave; si rifiuta se uno qualsiasi dei file esiste."""
    dn = camp[camp.visto_v3 == 0]; rng = np.random.default_rng(P["seed_dennis"]); pick = []
    for c, n in P["n_dennis"].items():
        g = dn[dn.classe == c]; pick += list(rng.choice(g.codice.values, min(n, len(g)), replace=False))
    casi = camp[camp.codice.isin(pick)].sort_values("codice"); casi = casi.iloc[rng.permutation(len(casi))].assign(caso=[f"D{i + 1:02d}" for i in range(len(casi))])
    out = {os.path.join(CTRL[f"controllo_codificatore_{n}"], f): None for n in (1, 2) for f in ("ISTRUZIONI.txt", "codifica.csv", "img")}
    out.update({os.path.join(CTRL["controllo_umano"], f): None for f in ("modulo_dennis.csv", "chiave_da_aprire_dopo.csv", "img", "ISTRUZIONI.txt")})
    out[os.path.join(CTRL["chiavi"], "campione_chiave.csv")] = None
    esist = [p for p in out if os.path.exists(p)]
    if esist: raise SystemExit("--prepara-controlli: file già presenti, non sovrascrivo nulla:\n " + "\n ".join(esist))
    d = os.path.join(CACHE, "orto", "img"); os.makedirs(d, exist_ok=True)
    for c, g in zip(camp.codice, camp.geometry):
        f = os.path.join(d, c + ".jpg")
        if not os.path.exists(f): orto_image(g, f, P["px"])
    log("immagini ortofoto", len(camp))
    for n in (1, 2):
        k = CTRL[f"controllo_codificatore_{n}"]; os.makedirs(os.path.join(k, "img"))
        for c in camp.codice: shutil.copy(os.path.join(d, c + ".jpg"), os.path.join(k, "img", c + ".jpg"))
        open(os.path.join(k, "ISTRUZIONI.txt"), "w").write(ISTR.format(n=n))
        pd.DataFrame({"codice": camp.codice, **{c: "" for c in COLS}}).to_csv(os.path.join(k, "codifica.csv"), index=False)
    h = CTRL["controllo_umano"]; os.makedirs(os.path.join(h, "img"))
    for c, k in zip(casi.codice, casi.caso): shutil.copy(os.path.join(d, c + ".jpg"), os.path.join(h, "img", k + ".jpg"))
    open(os.path.join(h, "ISTRUZIONI.txt"), "w").write(ISTR.format(n="Dennis (C7)").replace("C001.jpg ... img/C220.jpg", "D01.jpg ... img/D20.jpg")
                                                       .replace("codifica.csv", "modulo_dennis.csv").replace("(220 righe)", "(20 righe), poi apri chiave_da_aprire_dopo.csv"))
    pd.DataFrame({"caso": casi.caso, **{c: "" for c in COLS}}).to_csv(os.path.join(h, "modulo_dennis.csv"), index=False)
    casi[["caso", "codice", "tipo", "id", "classe", "origine", "area_m2"]].to_csv(os.path.join(h, "chiave_da_aprire_dopo.csv"), index=False)
    os.makedirs(CTRL["chiavi"], exist_ok=True); camp.drop(columns="geometry").to_csv(os.path.join(CTRL["chiavi"], "campione_chiave.csv"), index=False)


def leggi_codifica(n):
    f = os.path.join(CTRL[f"controllo_codificatore_{n}"], "codifica.csv")
    if not os.path.exists(f): return None
    c = pd.read_csv(f, dtype=str).fillna("")
    return c if c.Q1.isin(list("LCDUVIX")).all() and len(c) else None


def criteri_orto(camp, c1, c2):
    """C5-fisico con due codificatori (pre-registrazione 2.7); scrive tabelle/controllo_ortofoto_esito.csv."""
    C = camp.drop(columns="geometry").merge(c1[["codice"] + COLS], on="codice", validate="1:1").merge(c2[["codice"] + COLS], on="codice", suffixes=("_1", "_2"), validate="1:1")
    C["ok_1"], C["ok_2"] = C.Q1_1.isin(LCD), C.Q1_2.isin(LCD)
    lo, ba = C[C.tipo == "lotto"], C[C.tipo == "base"]; n = len(lo)
    out = {"kappa_binario": kappa(C.ok_1, C.ok_2), "kappa_Q1": kappa(C.Q1_1, C.Q1_2)}
    out["C5a"] = round((lo.ok_1.sum() + lo.ok_2.sum()) / (2 * n), 3)
    for i in (1, 2):
        out[f"C5a_cod{i}"] = wilson(lo[f"ok_{i}"].sum(), n); out[f"base_cod{i}"] = wilson(ba[f"ok_{i}"].sum(), len(ba))
        out[f"C5b_cod{i}"] = newcombe(lo[f"ok_{i}"].sum(), n, ba[f"ok_{i}"].sum(), len(ba))
        out[f"C5_pesato_area_cod{i}"] = round(float((lo.area_m2 * lo[f"ok_{i}"]).sum() / lo.area_m2.sum()), 3)
        mid = pd.to_numeric(lo[f"LCD_{i}"], errors="coerce").map({0: 0.125, 1: 0.375, 2: 0.625, 3: 0.875})
        out[f"quota_libera_area_LCD_cod{i}"] = round(float((lo.area_m2 * mid).sum() / lo.area_m2[mid.notna()].sum()), 3) if mid.notna().any() else None
        g = lo[lo.area_m2 >= P["lotto_grande_m2"]]; out[f"C5_lotti_grandi_cod{i}"] = wilson(g[f"ok_{i}"].sum(), len(g)) if len(g) else None
    out["entrambi_si"] = wilson((lo.ok_1 & lo.ok_2).sum(), n)
    ok = out["kappa_binario"][0] >= P["soglia_kappa"]
    out["C5"] = bool(ok and out["C5a"] >= P["soglia_C5a"] and all(out[f"C5b_cod{i}"][1][0] >= P["soglia_C5b"] for i in (1, 2))) if ok else "non giudicabile (kappa < 0,60): ripeti"
    out["C5_per_classe"] = {c: round((g.ok_1.sum() + g.ok_2.sum()) / (2 * len(g)), 3) for c, g in lo.groupby("classe")}
    out["C5_per_origine"] = {o: [round((g.ok_1.sum() + g.ok_2.sum()) / (2 * len(g)), 3), len(g)] for o, g in lo.groupby("origine")}
    out["C5a_senza_visti_v3"] = round(float(lo[lo.visto_v3 == 0][["ok_1", "ok_2"]].values.mean()), 3); out["n_visti_v3"] = int(lo.visto_v3.sum())
    C.to_csv(os.path.join(HERE, "tabelle", "controllo_ortofoto_esito.csv"), index=False)
    return out


def criterio_c7(camp):
    h = CTRL["controllo_umano"]; f = os.path.join(h, "modulo_dennis.csv")
    if not os.path.exists(f): return "non preparato"
    m = pd.read_csv(f, dtype=str).fillna("")
    if not m.Q1.isin(list("LCDUVIX")).all(): return "in attesa di Dennis"
    k = pd.read_csv(os.path.join(h, "chiave_da_aprire_dopo.csv"), dtype=str).merge(m, on="caso")
    acc = {}
    for i in (1, 2):
        c = leggi_codifica(i)
        if c is None: return "in attesa dei codificatori"
        kk = k.merge(c[["codice", "Q1"]], on="codice", suffixes=("", "_c")); acc[i] = int((kk.Q1.isin(LCD) == kk.Q1_c.isin(LCD)).sum())
    return {"accordo_cod1": acc[1], "accordo_cod2": acc[2], "C7": all(v >= P["soglia_C7"] for v in acc.values())}


def criterio_c9():
    """C9-AT (pre-registrazione 3.5) da censimento_AT/codifica_1.csv e codifica_2.csv."""
    d = CTRL["censimento_AT"]; f = [os.path.join(d, f"codifica_{i}.csv") for i in (1, 2)]
    if not all(os.path.exists(x) for x in f): return {"C9": "in attesa del codificatore 2" if os.path.exists(f[0]) else "in attesa del censimento"}
    c = [pd.read_csv(x, dtype=str).fillna("").set_index("objectid").sort_index() for x in f]
    if not all(len(x) == 24 for x in c): return {"C9": "fogli incompleti"}
    comp = [(x.categoria.isin(list("ABCD")) & x.fonte_url.str.startswith("http") & (x.data_fonte != "") & (x.fonte_ufficiale == "si")) for x in c]
    n_ok = [int(x.sum()) for x in comp]; agree = int((c[0].categoria == c[1].categoria).sum())
    only_n = all(((x.categoria == "N") & (x.documento_da_aprire != "")).eq(~y).all() for x, y in zip(c, comp))
    c9a, c9b = all(v == 24 for v in n_ok), agree >= P["soglia_C9b"]
    esito = True if (c9a and c9b) else ("in attesa di Dennis" if (c9b and only_n) else False)
    return {"C9a_completi": n_ok, "C9b_accordo": agree, "C9": esito,
            "categorie_cod1": c[0].categoria.value_counts().to_dict(), "categorie_cod2": c[1].categoria.value_counts().to_dict()}


def main():
    pil = [21, 51, 72] if "--pilota" in sys.argv else None
    if "--no-fetch" not in sys.argv:
        import fetch; fetch.main()
        os.makedirs(RAW2, exist_ok=True); p = os.path.join(RAW2, "ds2813_verde_nil.geojson")
        if not os.path.exists(p): urllib.request.urlretrieve(DS2813, p)
    tas = catasto_v4(); log("tasselli catastali riscaricati", len(tas), int((tas.particelle_v4 == 0).sum()) if len(tas) else 0, "ancora vuoti")
    Lt, U, nil, W, cov, diag, extra = build(pil)
    extra["catasto_tasselli_riscaricati"] = {"n": len(tas), "ancora_vuoti": tas.tassello[tas.particelle_v4 == 0].tolist(), "particelle_recuperate": int(tas.particelle_v4.sum())}
    res = {"pilota": pil, "parametri": {k: v for k, v in P.items()}, "seme": SEED, **extra}
    T = os.path.join(HERE, "tabelle")
    if not pil:
        camp, alloc = campione(Lt, U); res["allocazione_C5"] = alloc; res["n_visti_v3"] = int(camp.visto_v3.sum())
        kf = os.path.join(CTRL["chiavi"], "campione_chiave.csv")
        if "--prepara-controlli" in sys.argv: prepara_controlli(Lt, camp)
        if os.path.exists(kf):
            k0 = pd.read_csv(kf, dtype=str).fillna(""); k1 = camp.drop(columns="geometry").astype(str).replace("nan", "")
            k1["area_m2"] = k1.area_m2.astype(float).astype(str); k0["area_m2"] = k0.area_m2.astype(float).astype(str)
            if not k0.equals(k1[k0.columns]): raise SystemExit("la chiave in chiavi/ non coincide con il campione ricostruito: fermo (nessuna scrittura)")
            res["sha256_chiave"] = hashlib.sha256(open(kf, "rb").read()).hexdigest()
        c1, c2 = leggi_codifica(1), leggi_codifica(2)
        res.update(criteri_orto(camp, c1, c2) if c1 is not None and c2 is not None else {"C5": "in attesa dei due codificatori"})
        res["C7"] = criterio_c7(camp)
    res.update(criterio_c9())
    r, e, a = (Lt.classe == c for c in CL)
    res["C1"] = bool(Lt.geometry.is_valid.all() and (~Lt.geometry.is_empty).all() and Lt.geom_type.isin(["Polygon", "MultiPolygon"]).all() and Lt.crs.to_epsg() == CRS)
    req = ["classe", "origine", "proprieta", "cap_far05", "cap_far1", "cap_far2", "nil_id", "fonti", "licenze", "stato_attuativo"]
    res["C2"] = bool(Lt.id.is_unique and Lt[req].notna().all().all() and (Lt[["origine", "fonti", "licenze", "stato_attuativo"]] != "").all().all() and (Lt.area_m2 > 0).all() and Lt.cap_recupero[r].notna().all())
    gg = Lt.geometry.values; i, j = shapely.STRtree(gg).query(gg, predicate="intersects"); k = i < j
    ov = shapely.area(shapely.intersection(gg[i[k]], gg[j[k]], grid_size=0.01)); bad = ov > P["overlap_m2"]
    res["C3_coppie_oltre_1m2"] = int(bad.sum()); res["C3_area_comune_max_m2"] = round(float(ov.max()), 3) if len(ov) else 0.0; res["C3"] = bool(bad.sum() == 0)
    res["C4"] = bool(all((Lt[nm] == np.where(a, 0, cap(Lt.area_m2, f))).all() for f, nm in zip(P["fars"], ("cap_far05", "cap_far1", "cap_far2")))
                     and (Lt.cap_recupero[r].astype(int) == cap(Lt.volume_fonte_m3[r] / P["storey_m"], 1.0)).all() and Lt.cap_recupero[~r].isna().all())
    tab = pd.crosstab([Lt.nil_id, Lt.nil_nome], Lt.classe).reset_index()
    cas = pd.DataFrame(W, columns=["classe", "passo", "rimasti"]); cas["rimossi"] = cas.groupby("classe").rimasti.diff().mul(-1).astype("Int64")
    cas.loc[cas.classe.str.endswith(":fonti") | cas.classe.eq("informativo") | cas.passo.str.contains("aggregazione") | (cas.rimossi < 0), "rimossi"] = pd.NA
    last = cas[cas.classe != "informativo"].groupby("classe").rimasti.last()
    res["C6"] = bool(all(tab[c].sum() == (Lt.classe == c).sum() for c in Lt.classe.unique())
                     and last["riuso"] == r.sum() and last["edificabile"] == e.sum() and last["attivazione"] == a.sum())
    res["conteggi"] = Lt.classe.value_counts().to_dict()
    res["conteggi_non_AT"] = Lt[Lt.lotto_at == 0].classe.value_counts().to_dict(); res["conteggi_AT"] = Lt[Lt.lotto_at == 1].classe.value_counts().to_dict()
    res["capacita"] = {c: {nm: int(Lt.loc[Lt.classe == c, nm].sum()) for nm in ("cap_far05", "cap_far1", "cap_far2")} for c in CL}
    res["capacita"][CL[0]]["cap_recupero"] = int(Lt.cap_recupero[r].sum())
    res["capacita_edificabili_AT"] = {nm: int(Lt.loc[e & (Lt.lotto_at == 1), nm].sum()) for nm in ("cap_far05", "cap_far1", "cap_far2")}
    res["n_anche_attivazione"] = int(Lt.anche_attivazione.sum())
    res["edificabili_oltre_400_alloggi_far1"] = int((Lt.cap_far1[e] > 400).sum())
    res["origini"] = Lt.groupby(["classe", "origine"]).size().rename("n").reset_index().values.tolist()
    res["proprieta"] = Lt.groupby(["classe", "proprieta"]).size().rename("n").reset_index().values.tolist()
    res["area_ha"] = Lt.groupby("classe").area_m2.sum().div(1e4).round(1).to_dict()
    res["scenario_riuso"] = Lt[r].scenario_principale.value_counts().to_dict()
    res["nil_con_lotti"] = int(Lt.nil_id.nunique()); res["hash_contenuto"] = content_hash(Lt)
    prev = sorted(glob.glob(os.path.join(HERE, "esecuzioni", "*_completa", "esito_criteri.json")))
    res["C8_hash_precedente"] = json.load(open(prev[-1])).get("hash_contenuto") if prev and not pil else None
    res["C8"] = res["C8_hash_precedente"] == res["hash_contenuto"]
    res["passa"] = all(res.get(c) is True for c in ("C1", "C2", "C3", "C4", "C5", "C6", "C8", "C9"))
    meta = pd.DataFrame([
        ("id", "ipotesi", "R/E/A + progressivo per classe e posizione"), ("geometry", "catasto; dbt", "particelle unite; riuso [v4]: (impronta fonte + 10 m) ∩ particella − altri edifici DBT; senza sovrapposizioni (R > E > A)"),
        ("classe", "ipotesi", "regole della pre-registrazione v4"), ("origine", "pgt; dusaf; ds677; demanio; ds503; dbt", "ingresso (e motivo per l'attivazione)"),
        ("ref", "catasto", "riferimenti catastali"), ("n_particelle", "catasto", ""),
        ("edifici_fonte", "dbt", "CEDIUV degli edifici fonte (riuso)"), ("fonti_riuso", "ds503; dbt", ""), ("nota", "ds503; dbt", "descrizione della fonte"),
        ("volume_fonte_m3", "dbt", "volume fuori terra dei soli edifici fonte"),
        ("area_v3_regola", "catasto; dbt", "[v4] riuso: area con la regola v3 (particella meno gli altri edifici), per confronto"),
        ("impronta_fonte_m2", "dbt", "[v4] riuso: impronta degli edifici fonte nella particella"),
        ("area_intorno_5m", "catasto; dbt; ipotesi", "[v4] riuso: area con intorno di 5 m (sensibilità)"), ("area_intorno_20m", "catasto; dbt; ipotesi", "[v4] riuso: area con intorno di 20 m (sensibilità)"),
        ("area_m2", "catasto", "area del lotto, EPSG:32632"), ("cx", "catasto", "punto interno x"), ("cy", "catasto", "punto interno y"),
        ("nil_id", "nil", ""), ("nil_nome", "nil", ""),
        ("at_objectid", "pgt", "[v4] OBJECTID del poligono AT non PCU che contiene il punto interno"), ("ambito_pgt", "pgt", "nome AT non PCU (punto interno)"),
        ("funzione_at", "pgt", "[v4] DFUN_PREV1 del poligono AT (D4)"), ("quota_at", "pgt", "[v4] quota dell'area in AT non PCU"), ("lotto_at", "pgt; ipotesi", "[v4] 1 se quota_at >= 0,5"),
        ("nil_indice_verde", "ds2813", "indice di verde urbano del NIL, luglio 2024"), ("nil_deficit_verde", "ds2813; ipotesi", "1 se nel quartile inferiore degli 88 NIL"),
        ("anche_attivazione", "ds2813; ipotesi", "lotto edificabile >= 5.000 m² in NIL con deficit di verde (A4)"),
        ("cap_far05", "ipotesi", "floor(0,70 × 0,5 × area / 80); riuso: demolizione e ricostruzione; attivazione 0"),
        ("cap_far1", "ipotesi", "floor(0,70 × 1 × area / 80); come sopra"), ("cap_far2", "ipotesi", "floor(0,70 × 2 × area / 80); come sopra"),
        ("cap_recupero", "dbt; ipotesi", "riuso: floor(0,70 × volume_fonte / 3,2 / 80); altre classi vuoto"),
        ("scenario_principale", "ipotesi; orto", "riuso: screening ds503 v3 (T3 demolizione, T1/T2 recupero); altrimenti diruto -> demolizione, ds503 -> recupero"),
        ("base_scenario", "ipotesi; orto", "regola di default o screening ds503 v3"),
        ("conferma_screening", "ds503; orto", "1 se il lotto da riusare contiene edifici ds503 confermati dallo screening (R1)"),
        ("quota_comunale", "ds677; catasto", "quota di area su particelle ds677"), ("quota_demanio", "demanio; catasto", "quota di area su particelle con un punto Demanio"),
        ("proprieta", "ds677; demanio", "[v4] Demanio se quota_demanio >= 0,5; pubblico comunale se quota_comunale >= 0,5; altrimenti 'non agganciata' (non significa privata)"),
        ("proprieta_conflitto", "ds677; demanio", "entrambe le quote >= 0,5"), ("vincoli_noti", "ds600; pgt; demanio", "quota > 10% o punto nel lotto"),
        ("stato_attuativo", "censimento", "[v4] categoria C9 (A/B/C/D/N) del poligono AT; 'in attesa del censimento' finché manca consenso.csv"),
        ("fonte_stato", "censimento", "[v4] URL e data della fonte dello stato attuativo"), ("disponibile_da", "censimento; ipotesi", "[v4] AT: oggi / dopo l'attuazione / da censire"),
        ("fonti", "—", ""), ("licenze", "—", "")], columns=["attributo", "fonte", "regola"])
    meta["fonte_estesa"] = meta.fonte.map(lambda s: " | ".join(SRC[x.strip()][0] for x in s.split(";") if x.strip() in SRC))
    meta["licenza"] = meta.fonte.map(lambda s: " | ".join(SRC[x.strip()][1] for x in s.split(";") if x.strip() in SRC)).replace("", "non applicabile (campo descrittivo)")
    res["C2"] = res["C2"] and set(Lt.columns) - {"geometry"} <= set(meta.attributo)
    ts = time.strftime("%Y-%m-%dT%H%M%SZ", time.gmtime()); tag = "pilota" if pil else "completa"
    out = os.path.join(HERE, "esecuzioni", f"{ts}_{tag}"); os.makedirs(out)
    git = lambda *a: subprocess.run(["git", "-C", HERE, *a], capture_output=True, text=True).stdout.strip()
    res["registro"] = dict(utc=ts, commit=git("rev-parse", "HEAD"), modifiche_non_committate=git("status", "--porcelain", "--", ".").splitlines()[:30],
                           sha256_run_py=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), python=sys.version.split()[0], durata_s=round(time.time() - T0))
    js = lambda p: json.dump(res, open(p, "w"), indent=1, ensure_ascii=False, default=str)
    js(os.path.join(out, "esito_criteri.json")); cas.to_csv(os.path.join(out, "cascata.csv"), index=False); cov.to_csv(os.path.join(out, "copertura_ambiti.csv"), index=False)
    if not pil:
        lp = os.path.join(HERE, "lotti_v4.gpkg")
        if os.path.exists(lp): os.remove(lp)
        Lt.to_file(lp, layer="lotti", driver="GPKG")
        for name, df in (("metadati", meta), ("cascata", cas)): pyogrio.write_dataframe(df, lp, layer=name, driver="GPKG")
        tas.to_csv(os.path.join(T, "catasto_tasselli_riscaricati.csv"), index=False)
        cov.to_csv(os.path.join(T, "copertura_ambiti.csv"), index=False); diag.to_csv(os.path.join(T, "diagnosi_particelle_mancanti.csv"), index=False)
        cas.to_csv(os.path.join(T, "cascata.csv"), index=False); tab.to_csv(os.path.join(T, "nil_classe.csv"), index=False); meta.to_csv(os.path.join(T, "metadati.csv"), index=False)
        Lt.drop(columns="geometry").to_csv(os.path.join(T, "lotti_attributi.csv"), index=False)
        js(os.path.join(HERE, "esito_criteri.json")); figure(Lt, nil, cas)
    log("fatto", res["conteggi"], {c: res.get(c) for c in ("C1", "C2", "C3", "C4", "C5", "C6", "C8", "C9")}, res["hash_contenuto"][:12])


def figure(Lt, nil, cas):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 9)); nil.boundary.plot(ax=ax, color="#bbbbbb", lw=0.4)
    for cl, col in zip(CL, ("#1b9e77", "#d95f02", "#7570b3")):
        s = Lt[Lt.classe == cl]; s.plot(ax=ax, color=col, edgecolor=col, lw=0.6, label=f"{cl} ({len(s)})"); s.representative_point().plot(ax=ax, color=col, markersize=3)
    Lt[Lt.lotto_at == 1].boundary.plot(ax=ax, color="black", lw=0.5, label="lotti AT (contorno)")
    ax.legend(loc="lower left"); ax.set_axis_off(); ax.set_title("Base L v4 (candidata): tre classi, EPSG:32632")
    fig.savefig(os.path.join(HERE, "fig", "mappa_classi.png"), dpi=130, bbox_inches="tight"); plt.close(fig)
    ks = [k for k in cas.classe.unique() if k != "informativo"]; fig, axs = plt.subplots(len(ks), 1, figsize=(10, 2.2 + 0.32 * len(cas)))
    for ax, k in zip(axs, ks):
        c = cas[cas.classe == k]; y = range(len(c))[::-1]
        ax.barh(y, c.rimasti); ax.set_yticks(y); ax.set_yticklabels([s[:80] for s in c.passo], fontsize=7); ax.set_xscale("log"); ax.set_title(f"Cascata: {k}", fontsize=9)
        for yy, v in zip(y, c.rimasti): ax.text(max(v, 1), yy, f" {v:,}".replace(",", "."), va="center", fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig", "cascata.png"), dpi=120); plt.close(fig)


if __name__ == "__main__":
    main()
