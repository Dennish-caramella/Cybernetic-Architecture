#!/usr/bin/env python3
"""Cerca dataset sui portali CKAN (es. open data del Comune di Milano) senza inventare URL.

Uso:  python tools/discover_opendata.py --base <URL_BASE_DEL_PORTALE> "NIL" "PGT" "edifici" ...

NON TESTATO: la sessione che ha scritto questo script non poteva raggiungere i portali. Assume un portale CKAN
(endpoint /api/3/action/package_search). Se il portale usa un'altra tecnologia, lo script lo dice e si ferma.
Stampa titolo, id, licenza, formati e URL delle risorse: sceglili tu e scarica a mano in data_raw/.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("--base", required=True, help="URL base del portale, es. https://dati.comune.milano.it")
ap.add_argument("termini", nargs="+")
a = ap.parse_args()

for t in a.termini:
    url = f"{a.base.rstrip('/')}/api/3/action/package_search?q={urllib.parse.quote(t)}&rows=10"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            d = json.load(r)
    except Exception as e:
        sys.exit(f"Errore su {url}: {e}\n(Forse il portale non è CKAN o la rete è bloccata.)")
    print(f"\n=== '{t}': {d['result']['count']} risultati (prime 10) ===")
    for p in d["result"]["results"]:
        print(f"- {p.get('title')}  [{p.get('name')}]  licenza: {p.get('license_title')}  aggiornato: {p.get('metadata_modified')}")
        for res in p.get("resources", []):
            print(f"    {res.get('format')}: {res.get('url')}")
