"""Scarica per il Comune di Milano gli strati PGT (Tavola delle previsioni, mosaico regionale) e DUSAF 2024 dai servizi ArcGIS di Regione Lombardia.
Uscita: raw/pgt_<id>.geojson, raw/dusaf.geojson, raw/milano.geojson (WGS84). Uso: python fetch_regione.py"""
import json, os, sys, time, urllib.parse, urllib.request

T = "https://www.cartografia.servizirl.it/arcgis1/rest/services/territorio"
PGT = f"{T}/tav_previsioni_b/MapServer"
LAYERS = {12: "nuclei_antica_formazione", 13: "ambiti_trasformazione", 14: "ambiti_rigenerazione", 15: "aree_dismesse",
          18: "servizi", 19: "aree_agricole", 20: "tessuto_consolidato", 21: "valore_paesaggistico", 22: "sensibilita_paesistica", 24: "consumo_suolo"}
os.makedirs("raw", exist_ok=True)


def get(url, params, tries=5):
    q = urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url + "?" + q, headers={"User-Agent": "spatial-prototype/0.1"}), timeout=180))
        except Exception as e:
            print("retry", url[-40:], e, file=sys.stderr); time.sleep(10 * (i + 1))
    raise SystemExit("failed " + url)


def fetch(path, url, base):
    if os.path.exists(path): return
    feats, off = [], 0
    while True:
        d = get(url, {**base, "outFields": "*", "outSR": 4326, "f": "geojson", "resultOffset": off, "resultRecordCount": 1000})
        fs = d.get("features", [])
        feats += fs; off += len(fs)
        print(path, off, file=sys.stderr)
        if len(fs) < 1000 and not d.get("exceededTransferLimit"): break
        if not fs: break
    json.dump({"type": "FeatureCollection", "features": feats}, open(path, "w", encoding="utf-8"))


W = {"where": "NOME_COM='MILANO'"}
fetch("raw/milano.geojson", f"{PGT}/35/query", W)
for i, n in LAYERS.items():
    fetch(f"raw/pgt_{n}.geojson", f"{PGT}/{i}/query", W)
env = '{"xmin":9.04,"ymin":45.38,"xmax":9.28,"ymax":45.54,"spatialReference":{"wkid":4326}}'
fetch("raw/dusaf.geojson", f"{T}/dusaf8/MapServer/1/query", {"geometry": env, "geometryType": "esriGeometryEnvelope", "inSR": 4326, "spatialRel": "esriSpatialRelIntersects", "where": "1=1"})
print("fatto", file=sys.stderr)
