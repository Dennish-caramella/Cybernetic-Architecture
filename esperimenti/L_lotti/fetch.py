"""Scarica le fonti grezze della Base L in esperimenti/_cache/L_lotti/raw (ignorata da git). Riprende da dove si era fermato.
Riuso dei fetcher del Lab (prove/in_evidenza/2026-10-25_spatial_milano_lab/mi/fetch_catasto.py, fetch_regione.py), con uscita in EPSG:32632."""
import json, os, re, sys, time, urllib.parse, urllib.request, zipfile

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_cache", "L_lotti", "raw")
log = lambda *a: print(*a, file=sys.stderr, flush=True)
CKAN = "https://dati.comune.milano.it/dataset"
FILES = {  # CKAN dati.comune.milano.it: nome locale -> URL risorsa (metadati in secondo_cervello/ricerche/milano_dati/catalogo/metadati_ckan)
    "ds964_nil.geojson": f"{CKAN}/e8e765fc-d882-40b8-95d8-16ff3d39eb7c/resource/9c4e0776-56fc-4f3d-8a90-f4992a3be426/download/ds964_nil_wm.geojson",
    "ds503_degrado.geojson": f"{CKAN}/ffda4609-cd29-48f7-b501-e8bf1426dcf9/resource/4a47b39d-e64b-4a85-8115-c5f37fd94410/download/ds503_aree_edifici_degradati_abbandonati_0_final.geojson",
    "ds2688_demanio_aree.geojson": f"{CKAN}/187944ac-83b4-4030-ae99-ea2cff31da92/resource/5250928c-18ec-44d6-b350-25a29f6aa479/download/ds2688_elenco-aree-2023.geojson",
    "ds2689_demanio_fabbricati.geojson": f"{CKAN}/9f4191c6-9bcc-45a9-a62d-88ffc995078d/resource/0915324e-379e-4d50-ba80-69be66b6c984/download/ds2689_fabbricati_de_demanio_statale_2023.geojson",
    "ds677_patrimonio.geojson": f"{CKAN}/b021d942-4590-473c-9aa3-27efc4d11e2e/resource/2bf474bd-88b5-4c9e-9504-35d0cab592ec/download/patrimonio_immobiliare_2019__final.geojson",
    "ds600_bonifiche.geojson": f"{CKAN}/4c2248f9-c5b8-4f5a-b1fa-45766daf1275/resource/83475a4a-f9fa-4512-b823-70d9238e4539/download/ds600_aree_del_territorio_del__c6at-33q9_final.geojson",
    "DBT_2020.zip": "https://gisportal.comune.milano.it/download/area_download/SIT/DBT2020/DBT_2020.zip",  # ds2889, 600 MB
}
DBT_KEEP = ("UN_VOL.", "EDIFC_EDIFC_USO.dbf", "EDIFC.dbf")
T = "https://www.cartografia.servizirl.it/arcgis1/rest/services/territorio"
PGT = {12: "naf", 13: "at", 14: "rig", 15: "dism", 18: "servizi", 19: "agr", 21: "pae"}  # tav_previsioni_b (mosaico PGT regionale)
WFS = "https://wfs.cartografia.agenziaentrate.gov.it/inspire/wfs/owfs01.php"
LAT0, LAT1, LON0, LON1, STEP = 45.385, 45.537, 9.040, 9.279, 0.01


def get(url, tries=6, raw=False):
    for i in range(tries):
        try:
            b = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "tesi-base-L/1.0"}), timeout=300).read()
            return b if raw else b.decode("utf-8", "replace")
        except Exception as e:
            log("retry", url[-60:], e); time.sleep(5 * (i + 1))
    raise SystemExit("download fallito: " + url)


def files():
    for name, url in FILES.items():
        p = os.path.join(RAW, name)
        if not os.path.exists(p):
            log("scarico", name); tmp = p + ".part"; urllib.request.urlretrieve(url, tmp); os.replace(tmp, p)
    d = os.path.join(RAW, "dbt")
    if not os.path.exists(os.path.join(d, "UN_VOL.shp")):
        os.makedirs(d, exist_ok=True)
        with zipfile.ZipFile(os.path.join(RAW, "DBT_2020.zip")) as z:
            for n in z.namelist():
                if os.path.basename(n).startswith(DBT_KEEP):
                    open(os.path.join(d, os.path.basename(n)), "wb").write(z.read(n))


def arcgis(path, url, base):
    if os.path.exists(path): return
    feats, off = [], 0
    while True:
        q = urllib.parse.urlencode({**base, "outFields": "*", "outSR": 32632, "f": "geojson", "resultOffset": off, "resultRecordCount": 1000, "orderByFields": "OBJECTID"})
        fs = json.loads(get(f"{url}?{q}")).get("features", [])
        feats += fs; off += len(fs)
        if len(fs) < 1000: break
    log(os.path.basename(path), len(feats))
    # geojson con coordinate EPSG:32632 (dichiarato in crs, non standard RFC 7946 ma letto da GDAL)
    json.dump({"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::32632"}}, "features": feats},
              open(path, "w", encoding="utf-8"))


def regione():
    for i, n in PGT.items():
        arcgis(os.path.join(RAW, f"pgt_{n}.geojson"), f"{T}/tav_previsioni_b/MapServer/{i}/query", {"where": "NOME_COM='MILANO'"})
    env = '{"xmin":9.04,"ymin":45.38,"xmax":9.28,"ymax":45.54,"spatialReference":{"wkid":4326}}'
    arcgis(os.path.join(RAW, "dusaf8.geojson"), f"{T}/dusaf8/MapServer/1/query",
           {"geometry": env, "geometryType": "esriGeometryEnvelope", "inSR": 4326, "spatialRel": "esriSpatialRelIntersects", "where": "1=1"})


MEM = re.compile(r"<wfs:member>(.*?)</wfs:member>", re.S)
REF = re.compile(r"<CP:NATIONALCADASTRALREFERENCE>([^<]+)<")
POS = re.compile(r"<gml:exterior>.*?<gml:posList[^>]*>([^<]+)<", re.S)


def catasto():
    """Particelle F205 (Milano) dal WFS INSPIRE, tasselli 0,01°. Solo anello esterno (come nel Lab). Coordinate lon/lat EPSG:6706."""
    d = os.path.join(RAW, "catasto"); os.makedirs(d, exist_ok=True)
    ni, nj = int((LAT1 - LAT0) / STEP) + 1, int((LON1 - LON0) / STEP) + 1
    for i in range(ni):
        for j in range(nj):
            path = os.path.join(d, f"{i}_{j}.json")
            if os.path.exists(path): continue
            a, b = LAT0 + i * STEP, LON0 + j * STEP
            bbox = f"{a:.4f},{b:.4f},{a + STEP:.4f},{b + STEP:.4f},urn:ogc:def:crs:EPSG::6706"
            out, start = [], 0
            while True:
                q = urllib.parse.urlencode({"service": "WFS", "version": "2.0.0", "request": "GetFeature", "typeNames": "CP:CadastralParcel",
                                            "count": 2000, "startIndex": start, "bbox": bbox})
                ms = MEM.findall(get(f"{WFS}?{q}"))
                for m in ms:
                    r, p = REF.search(m), POS.search(m)
                    if not r or not p or not r.group(1).startswith("F205"): continue
                    v = [float(x) for x in p.group(1).split()]
                    out.append([r.group(1), [[round(v[k + 1], 7), round(v[k], 7)] for k in range(0, len(v) - 1, 2)]])
                if len(ms) < 2000: break
                start += 2000
            json.dump(out, open(path, "w"), separators=(",", ":"))
            log("tassello", i, j, len(out))


def main():
    os.makedirs(RAW, exist_ok=True)
    files(); regione(); catasto()


if __name__ == "__main__":
    main()
