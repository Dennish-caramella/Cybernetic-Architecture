"""Base L v6 (ticket #39): lotti edificabili, lotti da riusare e aree di attivazione di Milano, EPSG:32632.
Parte da v5 (esperimenti/L_lotti_v5) con le modifiche [v6] della pre-registrazione (esecuzioni/00_preregistrazione.txt, SHA-256 0d83dda3...):
D4 solo dove la scheda esclude la residenza (GFU = "si [H]", estesa ai lotti da riusare); lotti in poligoni con cantiere = si (censimento v5) = tessuto consolidato;
stato di attuazione come attributo (C9 eliminato); potenziale_vuoto informativo; C5 post-stratificato (S1 = lotti identici a v5, codifiche v5 riusate; S2 = nuovi o cambiati, nuovo campione cieco).
Uso: python run.py --no-fetch                  costruisce, calcola i criteri (C5 se i fogli S2 sono compilati)
     python run.py --no-fetch --pilota         prova su 3 NIL (21, 51, 72): uscite solo in esecuzioni/<data>_pilota/
     python run.py --no-fetch --prepara-controlli   scrive immagini, fogli vuoti e chiave S2; si rifiuta se uno qualsiasi esiste
     python run.py --no-fetch --sens           sensibilita' (GFU come v5; senza Bovisa; senza regola cantiere): tabelle/sensibilita.json
Riusa da v1 parcels, share, dusaf_cat, rd e fetch.py; da v3 lo screening ds503; da v4 la cache del catasto e da v2 i tasselli AGEA (sola lettura);
da v5 (sola lettura): lotti_v5.gpkg, chiavi, codifiche C5, censimento_AT/codifica_1-2.csv, con SHA-256 verificati."""
import glob, hashlib, json, os, shutil, subprocess, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
import numpy as np, pandas as pd, geopandas as gpd, shapely, pyogrio
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from sklearn.cluster import KMeans

HERE = os.path.dirname(os.path.abspath(__file__))
V1, V3, V5 = os.path.join(HERE, "..", "L_lotti"), os.path.join(HERE, "..", "L_lotti_v3"), os.path.join(HERE, "..", "L_lotti_v5")
sys.path.insert(0, V1)
import run as v1  # noqa: E402
CACHE = os.path.join(HERE, "..", "_cache", "L_lotti_v6")  # copia degli strati 2030 e dei tasselli Sentinel-2 di v5
RAW4 = os.path.join(HERE, "..", "_cache", "L_lotti_v4", "raw")  # catasto corretto di v4 (tasselli di v1 + vuoti riscaricati): si legge
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
    seed_campione=6611, seed_screening=3513, n2_max=140, px=800, lotto_grande_m2=10000.0,   # [v6] seme del campione S2 (solo se N2 > n2_max)
    gfu_res="si [H]", pv_dusaf_min=0.5, pv_cover_max=0.10, cantiere_si="si", sim_m2=0.01,  # [v6] pre-reg. 1.3, 1.5, 1.6; sim_m2 = quota max della differenza simmetrica per S1
    orto_service="https://www.cartografia.servizirl.it/arcgis2/rest/services/BaseMap/Ortofoto2018_2019/ImageServer",
    s2_tiles="https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2025_3857/default/GoogleMapsCompatible", s2_min_m=600.0,  # [v5] solo localizzazione
    at_esito_quota=0.25,  # [v5] tabella AT 2012 -> 2030: sovrapposizione minima sull'area del poligono
    soglia_C5a=0.70, soglia_C5b=0.25, soglia_kappa=0.60, overlap_m2=1.0,  # C9b: ceil(5n/6)
)
REG = "https://www.cartografia.servizirl.it/arcgis1/rest/services/territorio"
# [v5] lettura delle 18 schede MA del Piano delle Regole PGT 2030 (pre-registrazione 1.3): COD_MOD -> codice, nome, funzione, residenza, sintesi
MA = {1: ("PA2*", "via Natta", "Verde", "no", "PA2-Sud: SL max 19.838 mq residenziale (3.667 ERS convenzionata), IF 4,5 mc/mq; poligono a funzione Verde"),
      2: ("PA1/b", "Stephenson", "Terziarie-Commerciali-Ricettive", "no", "SL max 90.000 mq funzioni urbane libere ad esclusione della residenza"),
      3: ("PA4/a", "Basmetto", "Verde", "no", "verde urbano di nuova previsione; IT 0,35 trasferibile in PA4/b previa cessione"),
      4: ("PA1/a", "Bruzzano", "Mix funzionale-Verde", "si", "SL max 76.000 mq funzioni urbane libere; 40-60% SL a servizi; permeabilità 25%"),
      5: ("PA7", "Trotto", "Mix funzionale", "si", "UT 0,35 mq/mq funzioni urbane; cessione >= 40% ST; permeabilità 30%"),
      6: ("PA6", "Caserma Mameli", "Mix Funzionale", "si", "ST 101.490 mq, IT 0,70; SL 71.043 mq di cui 35.522 ERS; cessione >= 50%; parco >= 30%"),
      7: ("AS/1", "Bellarmino", "Agricola", "no", "ambito di salvaguardia agricolo, ST 167.000 mq, acquisizione al Comune"),
      8: ("PA8", "via Novate", "Mix funzionale", "si", "ST 22.780 mq; SL 22.780 mq di cui ERS >= 20.863 (>= 50% in locazione)"),
      9: ("PA4/b", "Basmetto", "Mix funzionale", "si", "IT 0,35 mq/mq funzioni urbane libere da trasferimento da PA4/a"),
      10: ("PA2*/b", "via Natta", "Servizi-Verde", "no", "mantenimento a verde e attività sportive"),
      11: ("PA1/c", "Vaiano Valle Nord", "Mix funzionale-Verde", "si", "SL max 30.000 mq funzioni urbane libere; permeabilità 25%"),
      12: ("PA2", "via Natta", "Mix funzionale", "si", "PA2 Nord: SL 10.000 mq funzioni urbane"),
      13: ("AS/2", "Vaiano Valle Sud", "Agricola", "no", "ambito di salvaguardia agricolo, ST 294.000 mq"),
      14: ("PA1/b", "Stephenson", "Terziarie-Commerciali-Ricettive", "no", "come MA_2: residenza esclusa"),
      15: ("PA5", "piazza Lugano", "Terziarie-Commerciali-Ricettive", "no", "SL max 23.000 mq direzionali, commerciali e turistico-ricettive"),
      16: ("PA2*", "via Natta", "Mix funzionale", "si", "PA2-Sud: SL max 19.838 mq residenziale (3.667 ERS convenzionata), IF 4,5 mc/mq"),
      17: ("PA3", "viale Molise", "Mix funzionale", "si", "IT 0,35 + 68.494 mq SL da AdP Cascina Merlata; ERS >= 50%; cessione >= 30%"),
      18: ("PA2/a", "via Natta", "Verde", "no", "cessione obbligatoria per il completamento del verde di spina")}
ADP_NO = {"AREE FERROVIARIE SAN CRISTOFORO"}  # oasi naturalistica 100% (comunicato FS 22/06/2017) [V]; gli altri scali: residenza ammessa
GFU = {5263: "Piazza d'Armi", 5264: "Ronchetto", 5281: "Porto di Mare", 5267: "Bovisa-Goccia"}  # [H] perimetro AT 2012 sostitutivo
FS_CS = "https://www.fsitaliane.it/content/dam/fsitaliane/Documents/old-media-ed-eventi/comunicati-stampa-e-news/anno-2017/mese-giugno/2017_06_22_CS_Scali_ferroviari.pdf"
TILE = dict(x0=-5120900.0, y0=9998100.0, res={9: 3.9687579375158752, 10: 2.6458386250105836, 11: 1.3229193125052918,
                                               12: 0.5291677250021167, 13: 0.26458386250105836})
DS2813 = ("https://dati.comune.milano.it/dataset/49d2896c-abba-44e5-9a53-c19332a275b3/resource/bbc7d511-f52d-4fe0-a7c7-aa7e5f5dceb5/"
          "download/ds2813_spotted-milan-urbangreenindex-nil-01072024_31072024.geojson")
SRC = dict(v1.SRC)
SRC["ds2813"] = ("Comune di Milano, Indice di verde urbano per NIL, luglio 2024 (ds2813, SPOTTED)", "CC BY 4.0")
SRC["orto"] = ("AGEA, Ortofoto 2018-2019, servizio Regione Lombardia BaseMap/Ortofoto2018_2019", "proprietà AGEA: visione e stampa con citazione [S]")
SRC["censimento"] = ("Censimento dello stato attuativo degli ambiti PGT 2030 (censimento_AT/consenso.csv, fonti con URL e data per poligono)", "fonti citate per riga")
SRC["pgt2030"] = ("Regione Lombardia, mosaico PGT tav_previsioni_b strato 11 (Modalità attuative, schede MA PGT 2030 del 05/02/2020); programmi strato 1 (AdP Scali ferroviari, decreto 754 del 01/08/2017); "
                  "GFU con perimetro AT 2012 sostitutivo [H]; comunicato FS 22/06/2017", "[L] licenza non dichiarata nei servizi")
SRC["rig"] = ("Regione Lombardia, mosaico PGT tav_previsioni_b strato 14 (ambiti di rigenerazione diffusa, schede 02/07/2025)", "[L] licenza non dichiarata")
SRC["s2"] = ("EOX Sentinel-2 cloudless 2025 (dati Copernicus Sentinel 2025 modificati), solo per localizzare i lotti nei pacchetti", "CC BY-NC-SA 4.0")
CL = ("lotto da riusare", "lotto edificabile", "area di attivazione")
CTRL = {k: os.path.join(HERE, k) for k in ("controllo_codificatore_1", "controllo_codificatore_2", "chiavi")}
CENS = os.path.join(V5, "censimento_AT")  # [v6] sola lettura
H5 = {"censimento_AT/codifica_1.csv": "a3ad9dda8ef7783f4346e5612b4d82807261f547f9bafe641adc71bdc5609475", "censimento_AT/codifica_2.csv": "5eef113bc081d19dc6a7fb453e828b4b867f379e1a0a464d1e8594bcff9e4b92",
      "controllo_codificatore_1/codifica.csv": "999bf3e277c01b9dffca6c53811585bad3ad6603bc1db5e72c602bde541de5f4", "controllo_codificatore_2/codifica.csv": "7de45185fc7258f0c88ad5035380c9eca2233909f0aba171a30934a7facdeb68",
      "chiavi/campione_chiave.csv": "d787a547e858e38150fe794837e82068870300e9dc8bba82392c58a9590da1d4"}  # SHA-256 dei file v5 (pre-reg. 2.2)
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


def s2_image(geom, path, px):
    """[v5] Sentinel-2 cloudless 2025 (EOX, WMTS EPSG:3857), finestra >= 600 m sul lotto, contorno rosso: solo per localizzare."""
    from PIL import Image, ImageDraw
    g = gpd.GeoSeries([geom], crs=CRS); k = np.cos(np.radians(g.centroid.to_crs(4326).y.iloc[0])); g = g.to_crs(3857).iloc[0]
    x0, y0, x1, y1 = g.bounds; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    half = max(max(x1 - x0, y1 - y0) * 0.75 + 15 / k, P["s2_min_m"] / 2 / k); R0 = 2 * 20037508.342789
    z = max(z for z in range(12, 17) if 2 * half / (R0 / 256 / 2 ** z) <= 1600 or z == 12); res = R0 / 256 / 2 ** z
    c0, c1 = int((cx - half + R0 / 2) // (256 * res)), int((cx + half + R0 / 2) // (256 * res))
    r0, r1 = int((R0 / 2 - cy - half) // (256 * res)), int((R0 / 2 - cy + half) // (256 * res))
    def t(rc):
        p = os.path.join(CACHE, "s2", str(z), f"{rc[0]}_{rc[1]}.jpg")
        if not os.path.exists(p):
            os.makedirs(os.path.dirname(p), exist_ok=True)
            b = urllib.request.urlopen(urllib.request.Request(f"{P['s2_tiles']}/{z}/{rc[0]}/{rc[1]}.jpg", headers={"User-Agent": "tesi-base-L/5.0"}), timeout=60).read()
            open(p + ".part", "wb").write(b); os.replace(p + ".part", p)
        return p
    rc = [(r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)]
    with ThreadPoolExecutor(4) as ex: files = list(ex.map(t, rc))
    mos = Image.new("RGB", ((c1 - c0 + 1) * 256, (r1 - r0 + 1) * 256), "white")
    for (r, c), f in zip(rc, files): mos.paste(Image.open(f).convert("RGB"), ((c - c0) * 256, (r - r0) * 256))
    ox, oy = c0 * 256 * res - R0 / 2, R0 / 2 - r0 * 256 * res
    box = ((cx - half - ox) / res, (oy - cy - half) / res, (cx + half - ox) / res, (oy - cy + half) / res)
    im = mos.crop(tuple(int(round(v)) for v in box)).resize((px, px)); d = ImageDraw.Draw(im); s = px / (2 * half)
    for poly in shapely.get_parts(g):
        for ring in [poly.exterior, *poly.interiors]:
            d.line([((x - cx + half) * s, (cy + half - y) * s) for x, y in zip(*ring.xy)], fill=(255, 0, 0), width=2)
    d.text((5, px - 14), f"{2 * half * k:.0f} m  Sentinel-2 cloudless 2025 EOX, CC BY-NC-SA 4.0", fill=(255, 255, 0))
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


def ambiti_2030(at, gfu_res, drop=()):
    """[v5] Insieme degli ambiti PGT 2030 (pre-registrazione 1.2), in ordine di precedenza PA > ADP > GFU.
    PA: strato 11 del mosaico (schede MA); ADP: AdP Scali ferroviari dallo strato 1 di programmi, via identify (query non dà geometrie [V]);
    GFU: poligoni AT 2012 dello stesso nome [H]. Scarica in _cache/L_lotti_v5/raw se manca."""
    import fetch
    d = os.path.join(CACHE, "raw"); os.makedirs(d, exist_ok=True)
    pma, pad = os.path.join(d, "pgt2030_ma.geojson"), os.path.join(d, "adp_scali.json")
    fetch.arcgis(pma, f"{REG}/tav_previsioni_b/MapServer/11/query", {"where": "NOME_COM='MILANO'"})
    if not os.path.exists(pad):
        q = urllib.parse.urlencode({"geometry": '{"xmin":503000,"ymin":5023000,"xmax":525000,"ymax":5045000}', "geometryType": "esriGeometryEnvelope", "sr": 32632,
                                    "layers": "all:1", "tolerance": 0, "mapExtent": "503000,5023000,525000,5045000", "imageDisplay": "4000,4000,96",
                                    "returnGeometry": "true", "maxAllowableOffset": 0, "f": "json"})
        r = [x for x in json.loads(fetch.get(f"{REG}/programmi/MapServer/identify?{q}"))["results"] if x["attributes"]["CODICE"] == "164"]
        json.dump(r, open(pad + ".part", "w")); os.replace(pad + ".part", pad)
    ma = gpd.read_file(pma).set_crs(CRS, allow_override=True).sort_values("COD_MOD")
    rows = [dict(ambito_id=f"MA_{c}", gruppo="PA", codice_pgt=MA[c][0], ambito_pgt=MA[c][1], funzione=MA[c][2], residenza_2030=MA[c][3], sintesi=MA[c][4],
                 strumento="piano attuativo obbligatorio (PdR PGT 2030)" if MA[c][0].startswith("PA") else "ambito di salvaguardia agricola (PdR PGT 2030)",
                 data_ambito="2020-02-05 (scheda PGT 2030; PDF del 17/12/2019)", fonte_ambito=u, geometry=shapely.make_valid(g))
            for c, u, g in zip(ma.COD_MOD.astype(int), ma.SCHEDA_NEW, ma.geometry)]
    for x in sorted(json.load(open(pad)), key=lambda x: int(x["attributes"]["OBJECTID"])):
        a = x["attributes"]; rings = [shapely.LinearRing(r) for r in x["geometry"]["rings"]]
        outer = [shapely.Polygon(r) for r in rings if not r.is_ccw]; holes = [r for r in rings if r.is_ccw]  # Esri: esterni in senso orario
        geom = shapely.make_valid(shapely.MultiPolygon([shapely.Polygon(o.exterior, [h for h in holes if o.contains(shapely.Polygon(h))]) for o in outer]))
        no = a["OGGETTO"] in ADP_NO
        rows.append(dict(ambito_id=f"ADP_{a['OBJECTID']}", gruppo="ADP", codice_pgt="AdP Scali ferroviari", ambito_pgt=a["OGGETTO"].title(),
                         funzione="oasi naturalistica (100% verde)" if no else "mix (residenza e altre funzioni)", residenza_2030="no" if no else "si",
                         sintesi="comunicato FS 22/06/2017: " + ("oasi naturalistica 140.000 m², 100% della superficie" if no else "verde >= 50%; residenza sociale e convenzionata" + (", 70% non residenziale" if "GENOVA" in a["OGGETTO"] else "")),
                         strumento=f"accordo di programma (decreto {a['DECRETO APPROVAZIONE']}; stato regionale: {a['STATO']})", data_ambito="2017-08-01 (DATA DECRETO del servizio)",
                         fonte_ambito=f"{REG}/programmi/MapServer/1 (OBJECTID {a['OBJECTID']}); {FS_CS}", geometry=geom))
    if True:
        for oid, nm in GFU.items():
            if oid in drop: continue
            g = at[at.OBJECTID == oid]
            rows.append(dict(ambito_id=f"GFU_{oid}", gruppo="GFU", codice_pgt="GFU (perimetro AT 2012 sostitutivo [H])", ambito_pgt=nm, funzione="grande funzione urbana [S]",
                             residenza_2030=gfu_res, sintesi="[v6] residenza assunta [H] (area designata dal PGT come di trasformazione); destinazioni e quota residenziale non verificabili da fonti aperte [L]",
                             strumento="Documento di Piano PGT 2030 (GFU) [S]", data_ambito="[L]", fonte_ambito=g.SCHEDA_NEW.iloc[0] + " (perimetro 2012)",
                             geometry=shapely.make_valid(g.geometry.iloc[0])))
    return gpd.GeoDataFrame(rows, geometry="geometry", crs=CRS)


def tabella_at_2012_2030(at, is_pcu, amb):
    """[v5] Ogni poligono AT 2012 (30) -> ambiti 2030 sovrapposti; più gli ambiti 2030 senza AT 2012 ("nuovo"). Regola: quota >= P['at_esito_quota']."""
    rows, g2 = [], amb.geometry.values; t = shapely.STRtree(g2); hit = np.zeros(len(amb))
    for oid, nm, fun, pcu, g in zip(at.OBJECTID, at.NOME_AMB, at.DFUN_PREV1, is_pcu, shapely.make_valid(at.geometry.values)):
        j = t.query(g, predicate="intersects"); ov = shapely.area(shapely.intersection(g, g2[j]))
        q12, q30 = ov / g.area, ov / shapely.area(g2[j]); hit[j] = np.maximum(hit[j], q30)
        m = [(amb.iloc[x], a, b) for x, a, b in zip(j, q12, q30) if a >= P["at_esito_quota"] and amb.ambito_id.iloc[x] != f"GFU_{oid}"]
        if pcu: es = "PCU 2012 (parco): non è un ambito di trasformazione; filtro di esclusione mantenuto"
        elif oid in GFU: es = f"GFU 2030 {GFU[oid]} (perimetro 2012 sostitutivo [H]); residenza non verificata [L]"
        elif not m: es = "non presente negli strati 2030 raggiungibili [L]" + "".join(f"; in parte in {amb.ambito_id.iloc[x]} {amb.codice_pgt.iloc[x]} (res. {amb.residenza_2030.iloc[x]}; {a:.2f})" for x, a in zip(j, q12) if a >= 0.01)
        else:
            r30 = any(r.residenza_2030.startswith("si") for r, _, _ in m); same = r30 == (fun == "RESIDENZIALE")
            es = ("sopravvive" if same else "cambia destinazione") + f" ({'/'.join(sorted({r.gruppo for r, _, _ in m}))}; 2012 {fun} -> 2030 residenza {'si' if r30 else 'no'})"
        rows.append(dict(tipo="AT 2012", at2012_objectid=oid, at2012_nome=nm, at2012_funzione=fun, pcu=int(pcu), area_2012_ha=round(g.area / 1e4, 2),
                         ambiti_2030="; ".join(f"{r.ambito_id} {r.codice_pgt} {r.ambito_pgt} (res. {r.residenza_2030}; {a:.2f} del 2012, {b:.2f} del 2030)" for r, a, b in m),
                         sovrapposizioni_minori="; ".join(f"{amb.ambito_id.iloc[x]} {a:.2f}" for x, a in zip(j, q12) if 0.01 <= a < P["at_esito_quota"]),
                         esito=es))
    for x, r in amb.iterrows():
        if r.gruppo != "GFU" and hit[x] < P["at_esito_quota"]:
            rows.append(dict(tipo="ambito 2030", ambiti_2030=f"{r.ambito_id} {r.codice_pgt} {r.ambito_pgt} (res. {r.residenza_2030})", area_2012_ha=None,
                             esito=f"nuovo (quota massima coperta da un AT 2012: {hit[x]:.2f})"))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- costruzione
def build(pilota, gfu_res=None, cantiere=True, drop=()):
    gfu_res = gfu_res or P["gfu_res"]
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

    pg = {k: v1.rd(f"pgt_{k}.geojson") for k in ("at", "servizi", "dism", "agr", "pae", "naf", "rig")}
    at = pg["at"]; is_pcu = at.NOME_AMB.str.contains("PCU", na=False); srv = pg["servizi"]
    atn = ambiti_2030(at, gfu_res, drop)  # ambiti PGT 2030 al posto degli AT 2012 non PCU
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
    U["residenza_2030"], U["at_nome"], U["gruppo_ambito"] = None, None, None  # [v5] primo ambito 2030 (PA > ADP > GFU) che contiene il punto interno
    for f, nm, gr, g in zip(atn.residenza_2030, atn.ambito_id, atn.gruppo, atn.geometry):
        m = shapely.contains_xy(g, ux, uy) & U.residenza_2030.isna(); U.loc[m, "residenza_2030"] = f; U.loc[m, "at_nome"] = nm; U.loc[m, "gruppo_ambito"] = gr
    ta = shapely.STRtree(atn.geometry.values)  # correzione del registro (14/11): particella is_at con punto interno fuori da ogni ambito -> ambito con la sovrapposizione maggiore
    for x in U.index[U.is_at & U.residenza_2030.isna()]:
        j = ta.query(U.geometry[x], predicate="intersects"); b = atn.iloc[j[np.argmax(shapely.area(shapely.intersection(U.geometry[x], atn.geometry.values[j])))]]
        U.loc[x, ["residenza_2030", "at_nome", "gruppo_ambito"]] = [b.residenza_2030, b.ambito_id, b.gruppo]
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
    nonres = A.is_at & A.residenza_2030.notna() & ~A.residenza_2030.fillna("").str.startswith("si").astype(bool)  # [v6] D4: solo "no" (GFU "si [H]"); con gfu_res="non verificata" ricostruisce v5
    vinc = (A.pgt_srv_verde >= P["excl_share"]) | (A.pgt_pae >= P["excl_share"])
    to_att = vinc | ~entry_e.reindex(A.index) | nonres
    A["motivo"] = np.select([A.pgt_srv_verde >= P["excl_share"], A.pgt_pae >= P["excl_share"], nonres & (A.residenza_2030 == "no"), nonres, A.origine == "DUSAF_CAVA"],
                            ["verde di servizio PGT", "valore paesaggistico PGT", "ambito PGT 2030 senza residenza", "GFU 2030: residenza non verificata [L]", "cava o discarica DUSAF"],
                            "area verde incolta DUSAF 1412")
    Ae, Aa = A[~to_att], A[to_att].assign(origine=lambda d: d.origine + " / " + d.motivo)
    W += [("edificabile", "particelle verso l'abitazione", len(Ae)), ("attivazione", "particelle verso l'attivazione (vincolo PGT, ambito 2030 senza residenza o GFU [v5], ingresso solo verde/cava)", len(Aa))]
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
    ac = ["ambito_id", "ambito_pgt", "codice_pgt", "gruppo", "residenza_2030", "strumento", "data_ambito", "fonte_ambito"]
    ja = gpd.sjoin(pg_, atn[ac + ["geometry"]], predicate="within", how="left").sort_values("index_right", kind="stable").groupby(level=0)  # precedenza PA > ADP > GFU
    for c in ac: Lt[c if c != "gruppo" else "gruppo_ambito"] = ja[c].first().reindex(Lt.index)
    ta = shapely.STRtree(atn.geometry.values)  # punto interno fuori da ogni ambito: ambito con la sovrapposizione maggiore
    for x in Lt.index[Lt.ambito_id.isna()]:
        j = ta.query(Lt.geometry[x], predicate="intersects")
        if len(j):
            b = atn.iloc[j[np.argmax(shapely.area(shapely.intersection(Lt.geometry[x], atn.geometry.values[j])))]]
            for c in ac: Lt.loc[x, c if c != "gruppo" else "gruppo_ambito"] = b[c]
    Lt["quota_at"] = v1.share(Lt.geometry, atn).round(3); Lt["lotto_at"] = (Lt.quota_at >= P["excl_share"]).astype(int)
    ric = (Lt.classe == CL[0]) & (Lt.lotto_at == 1) & (Lt.residenza_2030 == "no")  # [v6] 1.2: D4 estesa ai lotti da riusare (correzione C4 della revisione v5)
    Lt.loc[ric, "classe"] = CL[2]; Lt.loc[ric, "origine"] = Lt.origine[ric] + " / ambito PGT 2030 senza residenza"
    pic = ric & (Lt.area_m2 < P["att_min_m2"]); Lt = Lt[~pic]
    W += [("riuso", "[v6] senza i lotti da riusare in ambito senza residenza (passano all'attivazione, D4)", int((Lt.classe == CL[0]).sum())),
          ("attivazione", f"[v6] più i lotti da riusare passati dall'ambito senza residenza (>= {P['att_min_m2']:.0f} m²)", int((Lt.classe == CL[2]).sum())),
          ("informativo", "[v6] lotti da riusare in ambito senza residenza (D4): totale / sotto il minimo di attivazione, fuori dalla base", int(ric.sum()))]
    Lt["quota_rig_diffusa"] = v1.share(Lt.geometry, pg["rig"]).round(3)
    gv = gpd.read_file(os.path.join(RAW2, "ds2813_verde_nil.geojson"), ignore_geometry=True).set_index("ID_NIL").value
    Lt["nil_indice_verde"] = Lt.nil_id.map(gv).round(3); Lt["nil_deficit_verde"] = (Lt.nil_indice_verde <= gv.quantile(P["green_deficit_q"])).astype(int)
    r, e, a = (Lt.classe == c for c in CL)
    Lt["anche_attivazione"] = (e & (Lt.area_m2 >= P["dual_min_m2"]) & (Lt.nil_deficit_verde == 1)).astype(int)
    caps(Lt)
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
    stato(Lt); Lt["potenziale_vuoto"] = potenziale_vuoto(Lt, V, lay["dusaf_13"])
    base = "catasto; dbt; pgt; pgt2030; rig; dusaf; nil; ds677; demanio; ds600; ds2813"
    Lt["fonti"] = np.where(r, base + "; " + Lt.fonti_riuso.fillna("").str.replace("+", "; ").str.replace("dbt_diruto", "dbt"), base)
    Lt["licenze"] = "CC BY 4.0; CC BY 2.5 IT; CC BY 3.0 IT; CC0; PGT regionale [L]"
    Lt = Lt.drop(columns="_o")
    # [v6] 1.5: lotti in poligoni con cantiere = si (codifica 1 o 2 del censimento v5) -> tessuto consolidato, non lotti
    cs = cantiere_si() if cantiere else {}
    tcm = ((Lt.lotto_at == 1) & Lt.ambito_id.isin(list(cs))).values
    tc = Lt[tcm].assign(motivo=lambda d: "cantiere = si (" + d.ambito_id.map(cs).astype(str) + ")", classe_prima=lambda d: d.classe)
    Lt = renum(Lt[~tcm]); tc = renum(tc, "T")
    r, e, a = (Lt.classe == c for c in CL)
    W += [(k, "[v6] senza i lotti in ambito con cantiere = si (tessuto urbano consolidato)", int(m.sum())) for k, m in zip(("riuso", "edificabile", "attivazione"), (r, e, a))]
    W += [("informativo", "[v6] lotti in ambito con cantiere = si, passati al tessuto consolidato", len(tc))]
    log("lotti", Lt.classe.value_counts().to_dict(), "tessuto consolidato", len(tc))
    pcu = at[is_pcu].assign(ambito_id=lambda d: "PCU_" + d.OBJECTID.astype(str), ambito_pgt=at.NOME_AMB[is_pcu], gruppo="PCU 2012 (filtro)", residenza_2030="")
    cov, diag = copertura(pd.concat([atn, pcu[["ambito_id", "ambito_pgt", "gruppo", "residenza_2030", "geometry"]]], ignore_index=True), Lt, U, D, du, pg["dism"][pg["dism"].DBONIFICA == "SI"])
    tab12 = tabella_at_2012_2030(at, is_pcu, atn)
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
    nr = Lt[a & Lt.origine.str.contains("senza residenza|GFU 2030")]
    mv_d4 = {"lotti": len(nr), "ha": round(nr.area_m2.sum() / 1e4, 2), "alloggi_far1_se_edificabili_I": int(cap(nr.area_m2[nr.area_m2 >= P["lot_min_m2"]], 1.0).sum()),
             "per_ambito": nr.groupby("ambito_id").area_m2.sum().div(1e4).round(2).to_dict(),
             "gfu_lotti": int(nr.origine.str.contains("GFU 2030").sum()), "gfu_ha": round(nr.area_m2[nr.origine.str.contains("GFU 2030")].sum() / 1e4, 2),
             "gfu_alloggi_far1_se_edificabili_I": int(cap(nr.area_m2[nr.origine.str.contains("GFU 2030") & (nr.area_m2 >= P["lot_min_m2"])], 1.0).sum())}
    extra = {"riuso_intorno": mv, "ambiti_2030_senza_residenza": mv_d4, "aggancio_ds677": aggancio,
             "d5_residenza_occupata_AT": {"particelle": len(d5), "ha": round(d5.area_m2.sum() / 1e4, 2), "copertura_lt_0_10": int((d5.cover < 0.10).sum()),
                                          "per_ambito": d5.groupby("at_nome").area_m2.sum().div(1e4).round(2).to_dict()}}
    extra["tessuto_consolidato"] = {"lotti": len(tc), "ha": round(tc.area_m2.sum() / 1e4, 2), "poligoni": cs, "per_classe": tc.classe_prima.value_counts().to_dict(),
                                    **{f"alloggi_{nm}": int(tc[nm].sum()) for nm in ("cap_far05", "cap_far1", "cap_far2")}}
    return Lt, tc, U, nil, W, cov, diag, extra, atn, tab12


def caps(L):
    r, a = L.classe == CL[0], L.classe == CL[2]
    for f, nm in zip(P["fars"], ("cap_far05", "cap_far1", "cap_far2")): L[nm] = np.where(a, 0, cap(L.area_m2, f))
    for c in ("volume_fonte_m3", "area_v3_regola", "impronta_fonte_m2", "area_intorno_5m", "area_intorno_20m"): L[c] = L[c].round(1)
    L["cap_recupero"] = pd.Series(cap(L.volume_fonte_m3.fillna(0) / P["storey_m"], 1.0), index=L.index, dtype="Int64").where(r)


def renum(L, pref=None):
    L = L.assign(_o=L.classe.map({c: i for i, c in enumerate(CL)})).sort_values(["_o", "cx", "cy"]).reset_index(drop=True)
    p = L.classe.map({CL[0]: "R", CL[1]: "E", CL[2]: "A"}) if pref is None else pref
    L["id"] = p + pd.Series(range(1, len(L) + 1)).astype(str).str.zfill(5)
    return L.drop(columns="_o")


def h5(rel):
    """SHA-256 del file v5 (sola lettura) verificato contro il valore pre-registrato; si ferma se diverso."""
    f = os.path.join(V5, rel)
    if hashlib.sha256(open(f, "rb").read()).hexdigest() != H5[rel]: raise SystemExit(f"SHA-256 diverso dal pre-registrato: {rel}")
    return f


def censimento():
    return [pd.read_csv(h5(f"censimento_AT/codifica_{i}.csv"), dtype=str).fillna("").set_index("ambito_id") for i in (1, 2)]


def cantiere_si():
    """[v6] 1.5: poligoni con cantiere = si in codifica 1 o 2 -> {ambito_id: 'codifica 1' / 'codifica 2' / 'codifiche 1 e 2'}."""
    c = censimento(); a, b = (set(x.index[x.cantiere == P["cantiere_si"]]) for x in c)
    return {k: ("codifiche 1 e 2" if k in a and k in b else "codifica 1" if k in a else "codifica 2") for k in sorted(a | b)}


def stato(Lt):
    """[v6] 1.4: stato di attuazione come attributo (nessun lotto escluso). stato_c1/c2 = categoria del censimento v5 (codifica 1 e 2), con fonte e marca di qualità;
    stato_riferimento: categoria concorde non N; oppure l'unica non N con fonte ufficiale; 'discordante'; 'non determinato [L]'. Marca = la più debole delle fonti usate."""
    c = censimento(); at = Lt.lotto_at == 1; o = Lt.ambito_id.astype(str)
    q = lambda x: np.where(x.fonte_ufficiale == "si", "ufficiale", "non ufficiale [S]")
    for i, x in ((1, c[0]), (2, c[1])):
        x = x.reindex(Lt.ambito_id.dropna().unique()).fillna("")
        Lt[f"stato_c{i}"] = np.where(at, o.map(x.categoria), ""); Lt[f"fonte_stato_c{i}"] = np.where(at, o.map(x.fonte_url), "")
        Lt[f"marca_stato_c{i}"] = np.where(at, o.map(x.marca + " / " + pd.Series(q(x), index=x.index)), "")
    s1, s2, f1, f2 = (Lt[k].astype(str) for k in ("stato_c1", "stato_c2", "marca_stato_c1", "marca_stato_c2"))
    off1, off2 = ~f1.str.contains("non uff"), ~f2.str.contains("non uff")
    ref = np.select([~at, (s1 == s2) & (s1 != "N") & (s1 != ""), (s1 == "N") & ~s2.isin(["N", ""]) & off2, (s2 == "N") & ~s1.isin(["N", ""]) & off1, ~s1.isin(["N", ""]) & ~s2.isin(["N", ""]) & (s1 != s2)],
                    ["", s1, s2, s1, "discordante"], "non determinato [L]")
    Lt["stato_riferimento"] = ref
    Lt["marca_stato_riferimento"] = np.select([~at, (ref == "discordante") | (ref == "non determinato [L]"), ref == s1, ref == s2], ["", "[L]", f1, f2], "")
    Lt.loc[at & (s1 == s2) & (ref == s1), "marca_stato_riferimento"] = np.where(off1 & off2, "ufficiale", "non ufficiale [S]")[(at & (s1 == s2) & (ref == s1)).values]


def potenziale_vuoto(L, V, d13):
    """[v6] 1.6 [H]: 1 se quota DUSAF 133/134 del lotto >= pv_dusaf_min e copertura delle impronte DBT < pv_cover_max (informativo; recinzioni non calcolabili [L])."""
    t = shapely.STRtree(V.geometry.values); cov = []
    for g in L.geometry.values:
        j = t.query(g, predicate="intersects"); cov.append(shapely.intersection(shapely.union_all(V.geometry.values[j]), g).area / g.area if len(j) else 0.0)
    return ((np.asarray(v1.share(L.geometry, d13)) >= P["pv_dusaf_min"]) & (np.array(cov) < P["pv_cover_max"])).astype(int)


def copertura(amb, Lt, U, D, du, bon):
    """[v5] Tabella per tutti gli ambiti 2030 (+ PCU 2012 marcati); copertura da qualsiasi particella e diagnosi delle parti fuori dall'universo (v4 D6)."""
    tu, td_, tl, tdu = (shapely.STRtree(x) for x in (U.geometry.values, D.geometry.values, Lt.geometry.values, du.geometry.values))
    cod = du.COD_TOT.astype(str).values; bon_u = shapely.union_all(shapely.make_valid(bon.geometry.values)); rows, diag = [], []
    for oid, name, gr, fun, g in zip(amb.ambito_id, amb.ambito_pgt, amb.gruppo, amb.residenza_2030, shapely.make_valid(amb.geometry.values)):
        pcu = gr.startswith("PCU"); a = g.area; row = dict(ambito_id=oid, ambito=name, gruppo=gr, pcu=int(pcu), residenza_2030=fun, area_ha=round(a / 1e4, 2))
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
            if ia > 100: diag.append(dict(ambito_id=oid, ambito=name, ref=D.ref.values[q], suffisso=D.ref.values[q].split(".")[-1], terreno=bool(D.land.values[q]),
                                          nel_comune=bool(D.in_city.values[q]), area_particella_m2=round(D.area_m2.values[q]), area_in_ambito_fuori_universo_m2=round(ia)))
        diag.append(dict(ambito_id=oid, ambito=name, ref="(nessuna particella)", suffisso="", terreno=False, nel_comune=False, area_particella_m2=0,
                         area_in_ambito_fuori_universo_m2=round(shapely.difference(out, dd).area)))
    return pd.DataFrame(rows), pd.DataFrame(diag)


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


# ---------------------------------------------------------------- C5-fisico post-stratificato [v6, pre-registrazione 2]
def strati(Lt):
    """[v6] 2.2: S1 = lotti con lotto_at = 0 identici (stessa classe, differenza simmetrica < sim_m2 dell'area) a un lotto v5 con lotto_at = 0; S2 = tutti gli altri lotti.
    Ritorna anche i lotti del campione v5 ancora validi e la soglia q2* (2.6)."""
    L5 = gpd.read_file(os.path.join(V5, "lotti_v5.gpkg"), layer="lotti", columns=["id", "classe", "lotto_at", "area_m2"]); g5 = L5.geometry.values; t = shapely.STRtree(g5); m5 = {}
    for i, g, c, at in zip(Lt.index, Lt.geometry.values, Lt.classe, Lt.lotto_at):
        if at: continue
        for j in t.query(g, predicate="intersects"):
            if L5.classe[j] == c and L5.lotto_at[j] == 0 and shapely.symmetric_difference(g, g5[j]).area < P["sim_m2"] * L5.area_m2[j]: m5[i] = L5.id[j]; break
    k5 = pd.read_csv(h5("chiavi/campione_chiave.csv"), dtype=str).fillna(""); lot5 = k5[k5.tipo == "lotto"]; ok5 = lot5[lot5.id.isin(set(m5.values()))]
    sh = [pd.read_csv(h5(f"controllo_codificatore_{n}/codifica.csv"), dtype=str).fillna("").set_index("codice") for n in (1, 2)]
    q1 = [float(s.Q1.reindex(ok5.codice).isin(LCD).mean()) for s in sh]
    S1 = sorted(m5); S2 = [i for i in Lt.index if i not in m5]; N1, N2 = len(S1), len(S2); q1m = float(np.mean(q1))
    qs = (P["soglia_C5a"] * (N1 + N2) - N1 * q1m) / N2 if N2 else None
    return dict(S1=S1, S2=S2, N1=N1, N2=N2, v5_campione=len(lot5), v5_ritenuti=len(ok5), v5_scartati=lot5.id[~lot5.id.isin(set(m5.values()))].tolist(), ritenuti=ok5.codice.tolist(),
                q1_cod=[round(x, 4) for x in q1], q1_media=round(q1m, 4), q2_star=None if qs is None else round(qs, 4), n2=min(N2, P["n2_max"]), censimento=N2 <= P["n2_max"])


def campione(Lt, S):
    """[v6] 2.3: S2 in censimento se N2 <= n2_max, altrimenti campione per classe (resti piu' grandi, seme 6611); codici nuovi C301...; nessuna base nuova."""
    rng = np.random.default_rng(P["seed_campione"]); pop = Lt.loc[S["S2"]]
    if S["censimento"]: sid = np.array(S["S2"])
    else:
        cnt = pop.classe.value_counts().reindex(list(CL[1:]) + [CL[0]]).fillna(0).astype(int); q = cnt / cnt.sum() * S["n2"]; alloc = np.floor(q).astype(int)
        alloc[(q - alloc).sort_values(ascending=False, kind="stable").index[:S["n2"] - alloc.sum()]] += 1; alloc = alloc.clip(upper=cnt)
        sid = np.concatenate([rng.choice(pop.index[pop.classe == c].values, alloc[c], replace=False) for c in alloc.index])
    camp = pd.DataFrame({"tipo": "lotto", "id": Lt.id[sid].values, "classe": Lt.classe[sid].values, "origine": Lt.origine[sid].values, "area_m2": Lt.area_m2[sid].values,
                         "ambito_id": Lt.ambito_id[sid].values, "strato": "S2", "geometry": Lt.geometry[sid].values})
    camp["codice"] = ["C%03d" % (301 + i) for i in np.argsort(rng.permutation(len(camp)))]
    return camp.sort_values("codice").reset_index(drop=True)


ISTR = """Codificatore {n} — Base L v6 (ticket #39). Codifica cieca su ortofoto.

Materiale in questa cartella: img/C301.jpg ... (ortofoto AGEA 2018-2019, Regione Lombardia; licenza di sola visione,
non diffondere), img_s2/C301.jpg ... (Sentinel-2 cloudless 2025 di EOX, CC BY-NC-SA 4.0, risoluzione 10 m:
stessa area vista da più lontano, solo per localizzare e per il campo s2) e il foglio vuoto codifica.csv.
Lavora solo con questa cartella: non aprire altri file del progetto.

Ogni immagine mostra un'area con contorno ROSSO. Codifica ciò che sta DENTRO il contorno rosso dell'immagine AGEA (img/), una riga per immagine.

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
s2 (informativo, dopo aver codificato Q1): confronta img_s2 con img dentro il contorno:
 S uguale (nessun cambiamento visibile)   M cambiato (nuovi edifici, cantiere, sterro, verde)   N non leggibile a 10 m
nota: facoltativa, breve, senza virgole.

Consegna: codifica.csv compilato ({n_righe} righe); annota l'ora di inizio e di fine, le interruzioni e se perdi il contesto delle immagini già viste;
calcola lo SHA-256 del file e consegnalo al coordinatore prima di qualsiasi confronto. È uno screening visivo dall'alto, non una perizia.
"""
COLS = ["Q1", "LCD", "eterogeneo", "tetto", "veg", "uso", "s2", "nota"]


def prepara_controlli(camp):
    """D1/D2: scrive i pacchetti dei due codificatori e la chiave S2; si rifiuta se uno qualsiasi dei file esiste. Nessun file di v5 o chiave dentro i pacchetti."""
    out = [os.path.join(CTRL[f"controllo_codificatore_{n}"], f) for n in (1, 2) for f in ("ISTRUZIONI.txt", "codifica.csv", "img", "img_s2")] + [os.path.join(CTRL["chiavi"], "campione_chiave_v6.csv")]
    esist = [p for p in out if os.path.exists(p)]
    if esist: raise SystemExit("--prepara-controlli: file già presenti, non sovrascrivo nulla:\n " + "\n ".join(esist))
    d, d2 = os.path.join(CACHE, "orto", "img"), os.path.join(CACHE, "s2", "img"); os.makedirs(d, exist_ok=True); os.makedirs(d2, exist_ok=True)
    for c, g in zip(camp.codice, camp.geometry):
        f, f2 = os.path.join(d, c + ".jpg"), os.path.join(d2, c + ".jpg")
        if not os.path.exists(f): orto_image(g, f, P["px"])
        if not os.path.exists(f2): s2_image(g, f2, P["px"])
    log("immagini AGEA e Sentinel-2", len(camp))
    for n in (1, 2):
        k = CTRL[f"controllo_codificatore_{n}"]
        for sub, src in (("img", d), ("img_s2", d2)):
            os.makedirs(os.path.join(k, sub))
            for c in camp.codice: shutil.copy(os.path.join(src, c + ".jpg"), os.path.join(k, sub, c + ".jpg"))
        open(os.path.join(k, "ISTRUZIONI.txt"), "w").write(ISTR.format(n=n, n_righe=len(camp)))
        pd.DataFrame({"codice": camp.codice, **{c: "" for c in COLS}}).to_csv(os.path.join(k, "codifica.csv"), index=False)
    os.makedirs(CTRL["chiavi"], exist_ok=True); camp.drop(columns="geometry").to_csv(os.path.join(CTRL["chiavi"], "campione_chiave_v6.csv"), index=False)


def leggi_codifica(n, camp):
    f = os.path.join(CTRL[f"controllo_codificatore_{n}"], "codifica.csv")
    if not os.path.exists(f): return None
    c = pd.read_csv(f, dtype=str).fillna("")
    return c if c.Q1.isin(list("LCDUVIX")).all() and set(c.codice) == set(camp.codice) else None


def criteri_c5(camp, S, c1, c2):
    """C5 v6 (pre-registrazione 2.5): kappa su tutti i casi; C5a e C5b con p_j ponderata sugli strati; IC di Wilson con numerosita' efficace dalla varianza stratificata."""
    sh = [pd.read_csv(h5(f"controllo_codificatore_{n}/codifica.csv"), dtype=str).fillna("").set_index("codice") for n in (1, 2)]
    k5 = pd.read_csv(h5("chiavi/campione_chiave.csv"), dtype=str).fillna(""); base = k5[k5.tipo == "base"].codice.tolist()
    N1, N2, n1, n2 = S["N1"], S["N2"], len(S["ritenuti"]), len(camp); N = N1 + N2
    ok = lambda s, codes: s.Q1.reindex(codes).isin(LCD).values
    c = [x.set_index("codice") for x in (c1, c2)]; out = {"N1": N1, "N2": N2, "n1_ritenuti": n1, "n2": n2}
    a1 = np.concatenate([ok(sh[0], S["ritenuti"] + base), ok(c[0], camp.codice)]); a2 = np.concatenate([ok(sh[1], S["ritenuti"] + base), ok(c[1], camp.codice)])
    out["kappa_binario"] = kappa(a1, a2)
    P_, B = [], []
    for j in (0, 1):
        q1, q2, b = ok(sh[j], S["ritenuti"]).mean(), ok(c[j], camp.codice).mean(), ok(sh[j], base)
        p = (N1 * q1 + N2 * q2) / N; var = (N1 / N) ** 2 * q1 * (1 - q1) / n1 * (1 - n1 / N1) + (N2 / N) ** 2 * q2 * (1 - q2) / n2
        neff = p * (1 - p) / var if var > 0 else 1e6
        out[f"cod{j + 1}"] = {"q_S1": round(q1, 3), "q_S2": round(q2, 3), "p": round(p, 4), "n_eff": round(neff, 1), "ic95_wilson": [round(x, 3) for x in wil(p * neff, neff)[1:]],
                              "base": wilson(b.sum(), len(b)), "C5b_newcombe": newcombe(p * neff, neff, b.sum(), len(b))}
        P_.append(p)
    out["C5a"] = round(float(np.mean(P_)), 4)
    ok_ = out["kappa_binario"][0] >= P["soglia_kappa"]
    out["C5"] = bool(ok_ and out["C5a"] >= P["soglia_C5a"] and all(out[f"cod{j}"]["C5b_newcombe"][1][0] >= P["soglia_C5b"] for j in (1, 2))) if ok_ else "non giudicabile (kappa < 0,60): ripeti"
    cc = camp.assign(ok1=ok(c[0], camp.codice), ok2=ok(c[1], camp.codice)); cc["ok"] = (cc.ok1.astype(int) + cc.ok2) / 2
    out["S2_per_classe"] = {k: [round(float(g.ok.mean()), 3), len(g)] for k, g in cc.groupby("classe")}
    out["S2_E_piu_R"] = round(float(cc.ok[cc.classe != CL[2]].mean()), 3)
    out["S2_per_gruppo_ambito"] = {k: [round(float(g.ok.mean()), 3), len(g)] for k, g in cc.groupby(cc.ambito_id.str[:3])}
    cc.drop(columns="geometry").to_csv(os.path.join(HERE, "tabelle", "controllo_ortofoto_esito_S2.csv"), index=False)
    return out


def riassunto(L, tc=None):
    """Tabella per classe e per ambito (totale / fuori / in ambito): n, ha, capacita'."""
    rows = []
    for c in CL:
        for sc, m in (("totale", L.lotto_at.notna()), ("fuori ambito 2030", L.lotto_at == 0), ("in ambito 2030", L.lotto_at == 1)):
            g = L[(L.classe == c) & m]; rows.append(dict(classe=c, ambito=sc, n=len(g), ha=round(g.area_m2.sum() / 1e4, 1), far05=int(g.cap_far05.sum()), far1=int(g.cap_far1.sum()), far2=int(g.cap_far2.sum()),
                                                        recupero=int(g.cap_recupero.sum()) if c == CL[0] else None))
    return pd.DataFrame(rows)


def confronto(Lt, tc, amb):
    """Tabella v5 / v6 (pre-reg. 1.7) e verifica Bovisa a tre definizioni (revisione v5 M3); v5 letta in sola lettura da lotti_v5.gpkg."""
    L5 = gpd.read_file(os.path.join(V5, "lotti_v5.gpkg"), layer="lotti")
    a, b = riassunto(L5), riassunto(Lt); t = a.merge(b, on=["classe", "ambito"], suffixes=("_v5", "_v6"))
    t = pd.concat([t, pd.DataFrame([dict(classe="tessuto consolidato (v6)", ambito="in ambito 2030", n_v6=len(tc), ha_v6=round(tc.area_m2.sum() / 1e4, 1), far05_v6=int(tc.cap_far05.sum()), far1_v6=int(tc.cap_far1.sum()), far2_v6=int(tc.cap_far2.sum()))])], ignore_index=True)
    t.to_csv(os.path.join(HERE, "tabelle", "confronto_v5_v6.csv"), index=False)
    pol = amb.geometry[amb.ambito_id == "GFU_5267"].iloc[0]; rows = []
    for ver, L in (("v5", L5), ("v6", Lt), ("v6 tessuto consolidato", tc)):
        if not len(L): continue
        g = L[L.ambito_id == "GFU_5267"]
        for c, x in g.groupby("classe"): rows.append(dict(versione=ver, definizione="a) lotti con ambito_id GFU_5267, per classe", voce=c, n=len(x), ha=round(x.area_m2.sum() / 1e4, 2)))
        for o, x in g.groupby("origine"): rows.append(dict(versione=ver, definizione="b) lotti con ambito_id GFU_5267, per origine/motivo", voce=o, n=len(x), ha=round(x.area_m2.sum() / 1e4, 2)))
        i = shapely.intersection(L.geometry.values, pol); rows.append(dict(versione=ver, definizione="c) area dei lotti di qualunque ambito dentro il poligono AT 2012 5267", voce="tutti", n=int((~shapely.is_empty(i)).sum()), ha=round(shapely.area(i).sum() / 1e4, 2)))
    rows.append(dict(versione="-", definizione="d) area del poligono AT 2012 5267 (perimetro GFU sostitutivo)", voce="poligono", n=1, ha=round(pol.area / 1e4, 2)))
    pd.DataFrame(rows).to_csv(os.path.join(HERE, "tabelle", "bovisa_tre_definizioni.csv"), index=False)
    return t


def content_hash2(Lt, tc):
    return hashlib.sha256((content_hash(Lt) + (content_hash(tc) if len(tc) else "")).encode()).hexdigest()


SCEN = {"gfu_come_v5": dict(gfu_res="non verificata"), "senza_bovisa": dict(drop=(5267,)), "senza_regola_cantiere": dict(cantiere=False)}


def main():
    pil = [21, 51, 72] if "--pilota" in sys.argv else None
    if "--no-fetch" not in sys.argv:
        import fetch; fetch.main()
        os.makedirs(RAW2, exist_ok=True); p = os.path.join(RAW2, "ds2813_verde_nil.geojson")
        if not os.path.exists(p): urllib.request.urlretrieve(DS2813, p)
    tas = catasto_v4(); log("tasselli catastali riscaricati", len(tas), int((tas.particelle_v4 == 0).sum()) if len(tas) else 0, "ancora vuoti")
    if "--sens" in sys.argv:  # sensibilita' informativa (pre-reg. 1.7): una per processo, nient'altro
        nome = sys.argv[sys.argv.index("--sens") + 1]; Ls, tcs = build(None, **SCEN[nome])[:2]; e_ = Ls.classe == CL[1]
        out = {"scenario": nome, "conteggi": Ls.classe.value_counts().to_dict(), "tessuto_consolidato": len(tcs), "edificabili_in_ambito": int((e_ & (Ls.lotto_at == 1)).sum()),
               "capacita_edificabili": {nm: int(Ls.loc[e_, nm].sum()) for nm in ("cap_far05", "cap_far1", "cap_far2")}, "capacita_edificabili_in_ambito_far1": int(Ls.loc[e_ & (Ls.lotto_at == 1), "cap_far1"].sum()),
               "tc_alloggi_far1": int(tcs.cap_far1.sum()), "tc_ha": round(tcs.area_m2.sum() / 1e4, 1), "area_ha": Ls.groupby("classe").area_m2.sum().div(1e4).round(1).to_dict(),
               "utc": time.strftime("%Y-%m-%dT%H%M%SZ", time.gmtime()), "sha256_run_py": hashlib.sha256(open(__file__, "rb").read()).hexdigest()}
        json.dump(out, open(os.path.join(HERE, "tabelle", f"sensibilita_{nome}.json"), "w"), indent=1, ensure_ascii=False); log("sensibilita", out); return
    Lt, tc, U, nil, W, cov, diag, extra, amb, tab12 = build(pil)
    extra["catasto_tasselli_riscaricati"] = {"n": len(tas), "ancora_vuoti": tas.tassello[tas.particelle_v4 == 0].tolist(), "particelle_recuperate": int(tas.particelle_v4.sum())}
    res = {"pilota": pil, "parametri": {k: v for k, v in P.items()}, "seme": SEED, **extra}
    T = os.path.join(HERE, "tabelle")
    if not pil:
        S = strati(Lt); res["strati_C5"] = {k: v for k, v in S.items() if k not in ("S1", "S2")}
        camp = campione(Lt, S); res["n_campione_S2"] = len(camp); res["allocazione_S2"] = camp.classe.value_counts().to_dict()
        kf = os.path.join(CTRL["chiavi"], "campione_chiave_v6.csv")
        if "--prepara-controlli" in sys.argv: prepara_controlli(camp)
        if os.path.exists(kf):
            k0 = pd.read_csv(kf, dtype=str).fillna(""); k1 = camp.drop(columns="geometry").astype(str).replace("nan", "")
            k1["area_m2"] = k1.area_m2.astype(float).astype(str); k0["area_m2"] = k0.area_m2.astype(float).astype(str)
            if not k0.equals(k1[k0.columns]): raise SystemExit("la chiave in chiavi/ non coincide con il campione ricostruito: fermo (nessuna scrittura)")
            res["sha256_chiave_v6"] = hashlib.sha256(open(kf, "rb").read()).hexdigest()
        c1, c2 = leggi_codifica(1, camp), leggi_codifica(2, camp)
        res.update({"C5_dettaglio": criteri_c5(camp, S, c1, c2)} if c1 is not None and c2 is not None else {"C5": "in attesa dei due codificatori"})
        if "C5_dettaglio" in res: res["C5"] = res["C5_dettaglio"]["C5"]
        res["C7"] = "non è un criterio (deciso da Dennis in v5)"; res["C9"] = "eliminato in v6: lo stato di attuazione è un attributo"
        confronto(Lt, tc, amb)
    r, e, a = (Lt.classe == c for c in CL)
    res["C1"] = bool(Lt.geometry.is_valid.all() and (~Lt.geometry.is_empty).all() and Lt.geom_type.isin(["Polygon", "MultiPolygon"]).all() and Lt.crs.to_epsg() == CRS)
    req = ["classe", "origine", "proprieta", "cap_far05", "cap_far1", "cap_far2", "nil_id", "fonti", "licenze", "potenziale_vuoto"]
    ina = Lt.lotto_at == 1; sk = ["stato_c1", "stato_c2", "stato_riferimento", "marca_stato_c1", "marca_stato_c2", "marca_stato_riferimento"]
    res["C2"] = bool(Lt.id.is_unique and Lt[req].notna().all().all() and (Lt[["origine", "fonti", "licenze"]] != "").all().all() and (Lt.area_m2 > 0).all() and Lt.cap_recupero[r].notna().all()
                     and Lt.ambito_id[ina].notna().all() and (Lt.loc[ina, sk] != "").all().all() and Lt.potenziale_vuoto.isin([0, 1]).all())
    gg = Lt.geometry.values; i, j = shapely.STRtree(gg).query(gg, predicate="intersects"); k = i < j
    ov = shapely.area(shapely.intersection(gg[i[k]], gg[j[k]], grid_size=0.01)); bad = ov > P["overlap_m2"]
    res["C3_coppie_oltre_1m2"] = int(bad.sum()); res["C3_area_comune_max_m2"] = round(float(ov.max()), 3) if len(ov) else 0.0; res["C3"] = bool(bad.sum() == 0)
    no_res = Lt.residenza_2030 == "no"
    res["C4"] = bool(all((Lt[nm] == np.where(a, 0, cap(Lt.area_m2, f))).all() for f, nm in zip(P["fars"], ("cap_far05", "cap_far1", "cap_far2")))
                     and (Lt.cap_recupero[r].astype(int) == cap(Lt.volume_fonte_m3[r] / P["storey_m"], 1.0)).all() and Lt.cap_recupero[~r].isna().all()
                     and not (no_res & ~a).any() and (Lt.cap_far2[no_res] == 0).all() and not (Lt.ambito_id.isin(list(extra["tessuto_consolidato"]["poligoni"])) & ina).any())
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
    res["stato_riferimento"] = Lt[ina].stato_riferimento.value_counts().to_dict(); res["potenziale_vuoto_n"] = int(Lt.potenziale_vuoto.sum())
    res["potenziale_vuoto_per_classe"] = Lt.groupby("classe").potenziale_vuoto.sum().astype(int).to_dict()
    res["nil_con_lotti"] = int(Lt.nil_id.nunique()); res["hash_contenuto"] = content_hash2(Lt, tc)
    prev = sorted(glob.glob(os.path.join(HERE, "esecuzioni", "*_completa", "esito_criteri.json")))
    res["C8_hash_precedente"] = json.load(open(prev[-1])).get("hash_contenuto") if prev and not pil else None
    res["C8"] = res["C8_hash_precedente"] == res["hash_contenuto"]
    res["passa"] = all(res.get(c) is True for c in ("C1", "C2", "C3", "C4", "C5", "C6", "C8"))
    meta = pd.DataFrame(META(), columns=["attributo", "fonte", "regola"])
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
        lp = os.path.join(HERE, "lotti_v6.gpkg")
        if os.path.exists(lp): os.remove(lp)
        Lt.to_file(lp, layer="lotti", driver="GPKG")
        for name, df in (("tessuto_consolidato", tc), ("metadati", meta), ("cascata", cas)):
            if len(df): pyogrio.write_dataframe(df, lp, layer=name, driver="GPKG")
        tas.to_csv(os.path.join(T, "catasto_tasselli_riscaricati.csv"), index=False)
        cov.to_csv(os.path.join(T, "copertura_ambiti_2030.csv"), index=False); tab12.to_csv(os.path.join(T, "tabella_AT_2012_2030.csv"), index=False)
        amb.drop(columns="geometry").assign(area_ha=(amb.area / 1e4).round(2)).to_csv(os.path.join(T, "ambiti_2030.csv"), index=False)
        diag.to_csv(os.path.join(T, "diagnosi_particelle_mancanti.csv"), index=False)
        cas.to_csv(os.path.join(T, "cascata.csv"), index=False); tab.to_csv(os.path.join(T, "nil_classe.csv"), index=False); meta.to_csv(os.path.join(T, "metadati.csv"), index=False)
        Lt.drop(columns="geometry").to_csv(os.path.join(T, "lotti_attributi.csv"), index=False); tc.drop(columns="geometry").to_csv(os.path.join(T, "tessuto_consolidato.csv"), index=False)
        js(os.path.join(HERE, "esito_criteri.json")); figure(Lt, nil, cas)
    log("fatto", res["conteggi"], {c: res.get(c) for c in ("C1", "C2", "C3", "C4", "C5", "C6", "C8")}, res["hash_contenuto"][:12])


def META():
    return [
        ("id", "ipotesi", "R/E/A + progressivo per classe e posizione"), ("geometry", "catasto; dbt", "particelle unite; riuso [v4]: (impronta fonte + 10 m) ∩ particella − altri edifici DBT; senza sovrapposizioni (R > E > A)"),
        ("classe", "ipotesi", "regole della pre-registrazione v4 e v5"), ("origine", "pgt; dusaf; ds677; demanio; ds503; dbt", "ingresso (e motivo per l'attivazione)"),
        ("ref", "catasto", "riferimenti catastali"), ("n_particelle", "catasto", ""),
        ("edifici_fonte", "dbt", "CEDIUV degli edifici fonte (riuso)"), ("fonti_riuso", "ds503; dbt", ""), ("nota", "ds503; dbt", "descrizione della fonte"),
        ("volume_fonte_m3", "dbt", "volume fuori terra dei soli edifici fonte"),
        ("area_v3_regola", "catasto; dbt", "[v4] riuso: area con la regola v3 (particella meno gli altri edifici), per confronto"),
        ("impronta_fonte_m2", "dbt", "[v4] riuso: impronta degli edifici fonte nella particella"),
        ("area_intorno_5m", "catasto; dbt; ipotesi", "[v4] riuso: area con intorno di 5 m (sensibilità)"), ("area_intorno_20m", "catasto; dbt; ipotesi", "[v4] riuso: area con intorno di 20 m (sensibilità)"),
        ("area_m2", "catasto", "area del lotto, EPSG:32632"), ("cx", "catasto", "punto interno x"), ("cy", "catasto", "punto interno y"),
        ("nil_id", "nil", ""), ("nil_nome", "nil", ""),
        ("ambito_id", "pgt2030", "[v5] ambito 2030 che contiene il punto interno (PA > ADP > GFU); se nessuno, quello con la sovrapposizione maggiore"),
        ("ambito_pgt", "pgt2030", "[v5] nome dell'ambito 2030"), ("codice_pgt", "pgt2030", "[v5] PA../AS.. (schede MA), AdP Scali, GFU"),
        ("gruppo_ambito", "pgt2030", "[v5] PA, ADP o GFU"), ("residenza_2030", "pgt2030; ipotesi", "[v6] si / si [H] (GFU) / no (pre-registrazione 1.2-1.3, D4 solo se no)"),
        ("strumento", "pgt2030", "[v5] strumento di attuazione dell'ambito"), ("data_ambito", "pgt2030", "[v5] data della scheda o del decreto"),
        ("fonte_ambito", "pgt2030", "[v5] URL della scheda o del servizio"),
        ("quota_at", "pgt2030", "[v5] quota dell'area nell'unione degli ambiti 2030"), ("lotto_at", "pgt2030; ipotesi", "1 se quota_at >= 0,5"),
        ("quota_rig_diffusa", "rig", "[v5] informativo: quota dell'area in ambiti di rigenerazione diffusa (strato 14, 2025)"),
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
        ("stato_c1", "censimento", "[v6] categoria A/B/C/D/N del poligono nella codifica 1 del censimento v5 (non esclude il lotto)"), ("stato_c2", "censimento", "[v6] come stato_c1, codifica 2"),
        ("fonte_stato_c1", "censimento", "[v6] URL della fonte della codifica 1"), ("fonte_stato_c2", "censimento", "[v6] URL della fonte della codifica 2"),
        ("marca_stato_c1", "censimento", "[v6] marca [V]/[S]/[L] e qualità (ufficiale / non ufficiale [S]) della fonte, codifica 1"), ("marca_stato_c2", "censimento", "[v6] come marca_stato_c1, codifica 2"),
        ("stato_riferimento", "censimento; ipotesi", "[v6] categoria concorde non N; o l'unica non N con fonte ufficiale; discordante; non determinato [L] (pre-reg. 1.4)"),
        ("marca_stato_riferimento", "censimento; ipotesi", "[v6] marca più debole delle fonti usate"),
        ("potenziale_vuoto", "dusaf; dbt; ipotesi", "[v6] informativo [H]: quota DUSAF 133/134 >= 0,5 e copertura impronte DBT < 0,10; recinzioni non calcolabili [L]"),
        ("fonti", "—", ""), ("licenze", "—", "")]


def figure(Lt, nil, cas):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 9)); nil.boundary.plot(ax=ax, color="#bbbbbb", lw=0.4)
    for cl, col in zip(CL, ("#1b9e77", "#d95f02", "#7570b3")):
        s = Lt[Lt.classe == cl]; s.plot(ax=ax, color=col, edgecolor=col, lw=0.6, label=f"{cl} ({len(s)})"); s.representative_point().plot(ax=ax, color=col, markersize=3)
    Lt[Lt.lotto_at == 1].boundary.plot(ax=ax, color="black", lw=0.5, label="lotti in ambiti PGT 2030 (contorno)")
    ax.legend(loc="lower left"); ax.set_axis_off(); ax.set_title("Base L v6 (candidata): tre classi, ambiti PGT 2030, EPSG:32632")
    fig.savefig(os.path.join(HERE, "fig", "mappa_classi.png"), dpi=130, bbox_inches="tight"); plt.close(fig)
    ks = [k for k in cas.classe.unique() if k != "informativo"]; fig, axs = plt.subplots(len(ks), 1, figsize=(10, 2.2 + 0.32 * len(cas)))
    for ax, k in zip(axs, ks):
        c = cas[cas.classe == k]; y = range(len(c))[::-1]
        ax.barh(y, c.rimasti); ax.set_yticks(y); ax.set_yticklabels([s[:80] for s in c.passo], fontsize=7); ax.set_xscale("log"); ax.set_title(f"Cascata: {k}", fontsize=9)
        for yy, v in zip(y, c.rimasti): ax.text(max(v, 1), yy, f" {v:,}".replace(",", "."), va="center", fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig", "cascata.png"), dpi=120); plt.close(fig)


if __name__ == "__main__":
    main()
