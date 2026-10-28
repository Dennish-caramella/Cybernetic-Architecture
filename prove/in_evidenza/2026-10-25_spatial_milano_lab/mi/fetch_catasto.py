"""Scarica le particelle catastali del Comune di Milano (codice F205) dal WFS INSPIRE dell'Agenzia delle Entrate (CC BY 4.0), a tasselli.
Uscita: raw/catasto/<i>_<j>.json con [[ref, [[lon,lat],...]], ...]. Uso: python fetch_catasto.py"""
import json, os, re, sys, time, urllib.parse, urllib.request

W = "https://wfs.cartografia.agenziaentrate.gov.it/inspire/wfs/owfs01.php"
LAT0, LAT1, LON0, LON1, STEP = 45.385, 45.537, 9.040, 9.279, 0.01
os.makedirs("raw/catasto", exist_ok=True)
MEM = re.compile(r"<wfs:member>(.*?)</wfs:member>", re.S)
REF = re.compile(r"<CP:NATIONALCADASTRALREFERENCE>([^<]+)<")
POS = re.compile(r"<gml:exterior>.*?<gml:posList[^>]*>([^<]+)<", re.S)


def get(url):
    for i in range(6):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "spatial-prototype/0.1"}), timeout=120).read().decode("utf-8", "replace")
        except Exception as e:
            print("retry", e, file=sys.stderr); time.sleep(5 * (i + 1))
    return ""


ni, nj = int((LAT1 - LAT0) / STEP) + 1, int((LON1 - LON0) / STEP) + 1
for i in range(ni):
    for j in range(nj):
        path = f"raw/catasto/{i}_{j}.json"
        if os.path.exists(path): continue
        a, b = LAT0 + i * STEP, LON0 + j * STEP
        bbox = f"{a:.4f},{b:.4f},{a + STEP:.4f},{b + STEP:.4f},urn:ogc:def:crs:EPSG::6706"
        out, start = [], 0
        while True:
            q = urllib.parse.urlencode({"service": "WFS", "version": "2.0.0", "request": "GetFeature", "typeNames": "CP:CadastralParcel", "count": 2000, "startIndex": start, "bbox": bbox})
            t = get(f"{W}?{q}")
            ms = MEM.findall(t)
            for m in ms:
                r, p = REF.search(m), POS.search(m)
                if not r or not p or not r.group(1).startswith("F205"): continue
                v = [float(x) for x in p.group(1).split()]
                out.append([r.group(1), [[round(v[k + 1], 7), round(v[k], 7)] for k in range(0, len(v) - 1, 2)]])
            if len(ms) < 2000: break
            start += 2000
        json.dump(out, open(path, "w"), separators=(",", ":"))
        print("tassello", i, j, len(out), file=sys.stderr, flush=True)
        time.sleep(0.3)
print("fatto", file=sys.stderr)
