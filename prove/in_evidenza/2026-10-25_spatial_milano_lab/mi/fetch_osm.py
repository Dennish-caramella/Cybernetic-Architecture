"""Scarica da OpenStreetMap (Overpass) gli edifici del Comune di Milano e gli indirizzi con CAP. Uscita: raw/osm_buildings.json, raw/osm_postcodes.json.
Dati (c) OpenStreetMap contributors, ODbL. Uso: python fetch_osm.py"""
import json, os, sys, time, urllib.parse, urllib.request

URL = "https://overpass-api.de/api/interpreter"
AREA = 'area["ref:ISTAT"="015146"]["admin_level"="8"]->.m;'
Q = {"osm_buildings": 'way(area.m)["building"];out tags geom;',
     "osm_postcodes": '(node(area.m)["addr:postcode"];way(area.m)["addr:postcode"];);out tags center;'}
for name, body in Q.items():
    path = f"raw/{name}.json"
    if os.path.exists(path): continue
    data = urllib.parse.urlencode({"data": f"[out:json][timeout:600];{AREA}{body}"}).encode()
    for i in range(8):
        try:
            out = json.load(urllib.request.urlopen(urllib.request.Request(URL, data=data, headers={"User-Agent": "spatial-prototype/0.1 (research prototype)"}), timeout=700))
            json.dump(out, open(path, "w", encoding="utf-8")); print("ok", name, len(out["elements"]), file=sys.stderr); break
        except Exception as e:
            print("retry", name, e, file=sys.stderr); time.sleep(30 * (i + 1))
