"""Prototipo del laboratorio: copia la pagina base in proto.src.html (solo la prima volta), poi costruisce
lab/prototype/site/ con la stessa struttura di mi/site/ + data/lab.json + spatial-milano-lab.html.
mi/ si legge soltanto: questo script scrive SOLO dentro lab/prototype/.
Uso: PYTHONPATH=C:/Temp/pl python lab/prototype/build_proto.py"""
import csv, json, math, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MI, LAB = os.path.join(ROOT, "mi"), os.path.join(ROOT, "lab")
SITE = os.path.join(HERE, "site")
SRC = os.path.join(HERE, "proto.src.html")
assert os.path.commonpath([SITE, MI]) != MI  # mai scrivere in mi/

if not os.path.exists(SRC):
    shutil.copy(os.path.join(MI, "spatial-mi.src.html"), SRC)

# 1. dati base (sola lettura da mi/site/data)
os.makedirs(SITE, exist_ok=True)
shutil.copytree(os.path.join(MI, "site", "data"), os.path.join(SITE, "data"), dirs_exist_ok=True)

# 2. lab.json: sottoinsieme compatto di model.json + potere d'acquisto per NIL
m = json.load(open(os.path.join(LAB, "results", "model.json"), encoding="utf-8"))


def clean(o, d=4):
    if isinstance(o, float):
        return None if not math.isfinite(o) else round(o, d)
    if isinstance(o, dict):
        return {k: clean(v, d) for k, v in o.items()}
    if isinstance(o, list):
        return [clean(v, d) for v in o]
    return o


CRIT_IT = {"access_metro": ("Accesso metro", "km dalla metro (meno è meglio)"),
           "access_jobs": ("Lavoro entro 5 km", "superficie per attività entro 5 km (rango)"),
           "services": ("Scuole e servizi", "E2SFCA, media dei ranghi"),
           "green_access": ("Accesso al verde", "E2SFCA m² di verde per residente (rango)"),
           "heat": ("Rischio calore", "indice di rischio calore del NIL (meno è meglio)"),
           "demand_reach": ("Persone nel bisogno raggiunte", "famiglie target entro 3 km, pesate per distanza"),
           "rent_burden": ("Peso dell'affitto", "affitto OMI di 60 m² / reddito netto per contribuente"),
           "capacity": ("Capacità", "log10 alloggi"),
           "cost": ("Costo per alloggio", "€ per alloggio (meno è meglio)")}
ARCH_IT = {"young_worker": "Giovane lavoratore", "family_children": "Famiglia con figli", "elderly": "Anziano", "commuter": "Pendolare"}

sites = []
for s in m["sites"]:
    a = s["acc"]
    sites.append({"id": s["id"], "o": s["o"], "at": s["at"] if isinstance(s["at"], str) else None, "nil": s["nil"],
                  "a": s["a"], "g": s["g"], "x": [round(v, 3) for v in s["x"]],
                  "dw": round(10 ** s["raw"][7]), "metro": round(s["raw"][0], 2), "dem": round(s["raw"][5], 1),
                  "cost": round(s["raw"][8]), "rb": round(s["raw"][6], 3),
                  "acc": {"top10": a["top10"], "hol": a["hol"], "b1": a["b1"], "min": a["min_arch"], **a["arch"]}})

ports = [{k: p[k] for k in ("id", "lens", "sites", "dw", "served", "gini", "cost", "gap", "status", "designated_share", "smaa", "optimal")}
         | {"audit": {k: p["audit"].get(k) for k in ("opp", "dep_poor", "dDI", "dwellings", "served_tau", "served_per_meur")}} for p in m["portfolios"]]

IDX = ("dDI", "dIso", "dep_poor", "dep_resid", "conc_q5", "opp", "served_per_meur")
audit = {}
for g, a in m["audit"].items():
    kn = a.get("key_numbers", {})
    audit[g] = {"label": a["label"], "claim_it": a["claim_it"], "caveats": a.get("caveats", []),
                "sites": kn.get("sites"), "dwellings": kn.get("dwellings"), "n_nil": kn.get("n_nil"), "eff_nil": kn.get("eff_nil"),
                "site_null": {n: {k: v for k, v in kn.get("site_null", {}).get(n, {}).items() if k in IDX} for n in ("size", "ring")},
                "block_null": kn.get("block_null"), "grid_stability": kn.get("grid_stability"), "q_dDI": kn.get("q_dDI"),
                "market_land": kn.get("market_land")}

nil = {}
for r in csv.DictReader(open(os.path.join(LAB, "proposals", "A_econ_or", "results", "purchasing_power_nil.csv"), encoding="utf-8")):
    nil[r["nil_id"]] = {k: float(r[k]) for k in ("hh", "ynet_med", "rent_med", "res_rent_med", "res_basket_med", "share_neg_residual", "rent_to_income_med")}
for r in csv.DictReader(open(os.path.join(LAB, "results", "demand_layers.csv"), encoding="utf-8")):
    nil.setdefault(r["nil_id"], {}).update({k: float(r[k + "_mean"]) for k in ("D_tau", "D_res_decent", "D_res_istat")})

meta = m["meta"]
out = clean({"meta": {"unit_km": meta["unit_km"], "params": meta["params"], "data_status": meta["data_status"], "counts": meta["counts"],
                      "demand_layer": meta["demand_layer"]},
             "criteria": [{"k": c["k"], "l": CRIT_IT[c["k"]][0], "u": CRIT_IT[c["k"]][1], "dir": c["dir"]} for c in m["criteria"]],
             "archetypes": [{"k": a["k"], "l": ARCH_IT[a["k"]], "mu": a["mu"], "synthetic": a["synthetic"]} for a in m["archetypes"]],
             "sites": sites, "portfolios": ports, "audit": audit, "people_vs_pgt": m["people_vs_pgt"],
             "posthoc_changes": m["posthoc_changes"], "rule": m["rule"], "nil": nil})
txt = json.dumps(out, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
assert "\ufffd" not in txt, "testo con caratteri corrotti"
open(os.path.join(SITE, "data", "lab.json"), "w", encoding="utf-8").write(txt)

# 3. pagina: stesso inserimento del core di mi/build_page_mi.py, ma scritto solo in lab/prototype/site
src = open(SRC, encoding="utf-8").read()
assert "/*__CORE__*/" in src
core = json.load(open(os.path.join(MI, "out", "core.json"), encoding="utf-8"))
tiles = json.load(open(os.path.join(MI, "out", "tiles.json"), encoding="utf-8"))
for n in core["nil"]:
    n["ind"].update({k: (round(v, 2) if isinstance(v, float) else v) for k, v in tiles["nil"].get(str(n["id"]), {}).items()})
core["tiles"] = {"tile": tiles["tile"], "index": tiles["index"], "uses": tiles["uses"]}
page = os.path.join(SITE, "spatial-milano-lab.html")
open(page, "w", encoding="utf-8").write(src.replace("/*__CORE__*/", json.dumps(core, separators=(",", ":"), ensure_ascii=False)))
lab_mb = os.path.getsize(os.path.join(SITE, "data", "lab.json")) / 1e6
print(f"site pronto: pagina {os.path.getsize(page) // 1024} KB, lab.json {lab_mb:.2f} MB, {len(sites)} siti, {len(ports)} portafogli, {len(nil)} NIL")
assert lab_mb < 2, "lab.json oltre 2 MB"
