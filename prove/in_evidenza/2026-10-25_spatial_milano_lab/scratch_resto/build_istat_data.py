"""Scarica da ISTAT (SDMX) e MEF gli indicatori per i 55 comuni di Monza e Brianza e li riduce a istat_mb.json.
Uso: python build_istat_data.py   (risposte in cache in ./raw_istat). Il server ISTAT e' lento: ci sono i retry.
Fonti: Istat (CC BY 4.0), MEF Dipartimento Finanze (CC BY 3.0 IT). Nessun CORS: i dati vanno incorporati nella pagina."""
import csv, io, json, os, sys, time, urllib.request, zipfile

BASE = "https://esploradati.istat.it/SDMXWS/rest/data/IT1,{flow},1.0/{key}?lastNObservations=1"
CODES = [str(108000 + i) for i in range(1, 56)]
os.makedirs("raw_istat", exist_ok=True)


def get(url, accept=None, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "spatial-prototype/0.1", **({"Accept": accept} if accept else {})})
            return urllib.request.urlopen(req, timeout=180).read()
        except Exception as e:
            print("retry", url[:110], e, file=sys.stderr)
            if "400" in str(e): return None
            time.sleep(15)
    raise SystemExit("fallito: " + url)


def sdmx(name, flow, ndims, fixed):
    """fixed: {posizione: valore}; la posizione 1 e' REF_AREA (riempita a blocchi da 25 comuni)"""
    path = f"raw_istat/{name}.csv"
    if os.path.exists(path):
        return list(csv.DictReader(open(path, encoding="utf-8")))
    rows = []
    for i in range(0, 55, 25):
        parts = [""] * ndims
        parts[0] = "A"
        parts[1] = "+".join(CODES[i:i + 25])
        for k, v in fixed.items(): parts[k] = v
        raw = get(BASE.format(flow=flow, key=".".join(parts)), "application/vnd.sdmx.data+csv;version=1.0.0")
        if raw is None: return None
        rows += list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
        time.sleep(2)
    if rows:
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    return rows


def sdmx_probe(name, flow, dims_candidates, fixed):
    for n in dims_candidates:
        r = sdmx(name, flow, n, fixed)
        if r is not None: return r
    raise SystemExit("nessuna chiave valida per " + flow)


out = {c: {} for c in CODES}
num = lambda v: float(v) if v not in ("", None) else None

# 1) popolazione residente per eta' (1 gennaio, ultimo anno disponibile)
rows = sdmx("pop", "22_289_DF_DCIS_POPRES1_6", 6, {2: "JAN", 3: "9", 5: "99"})
for c in CODES:
    ages = {r["AGE"]: float(r["OBS_VALUE"]) for r in rows if r["REF_AREA"] == c}
    if "TOTAL" not in ages: continue
    y = lambda a, b: sum(ages.get(f"Y{k}", 0) for k in range(a, b + 1))
    tot = ages["TOTAL"]
    o = out[c]
    o.update(pop=int(tot), pop_year=[r["TIME_PERIOD"] for r in rows if r["REF_AREA"] == c][0],
             a0_14=round(y(0, 14) / tot * 100, 1), a15_64=round(y(15, 64) / tot * 100, 1),
             a65=round((y(65, 99) + ages.get("Y_GE100", 0)) / tot * 100, 1),
             old_age_index=round((y(65, 99) + ages.get("Y_GE100", 0)) / max(y(0, 14), 1) * 100))

# 2) stranieri residenti
rows = sdmx_probe("foreign", "29_7_DF_DCIS_POPSTRRES1_23", (5, 6), {})
print("foreign SEX/AGE esempio:", sorted({(r["SEX"], r["AGE"]) for r in rows})[:6], file=sys.stderr)
for c in CODES:
    v = [r for r in rows if r["REF_AREA"] == c and r["AGE"] == "TOTAL" and r["SEX"] in ("9", "T")]
    if not v:  # somma dei sessi
        v1 = [float(r["OBS_VALUE"]) for r in rows if r["REF_AREA"] == c and r["AGE"] == "TOTAL" and r["SEX"] in ("1", "2")]
        tot = sum(v1) if v1 else None
    else: tot = float(v[0]["OBS_VALUE"])
    if tot is not None and out[c].get("pop"): out[c].update(foreign=int(tot), foreign_pct=round(tot / out[c]["pop"] * 100, 1))

# 3) occupati e disoccupati (censimento permanente 2024)
rows = sdmx("work", "DF_DCSS_ISTR_LAV_PEN_2_TV_3", 10, {2: "RESPOP_AV", 3: "T", 4: "Y_GE15"})
for c in CODES:
    v = {r["CUR_ACT_STAT"]: float(r["OBS_VALUE"]) for r in rows if r["REF_AREA"] == c and r["GENDER"] == "T" and r["AGE_NOCLASS"] == "Y_GE15"}
    if {"1", "12", "22", "99"} <= v.keys():
        out[c].update(emp_rate=round(v["1"] / v["99"] * 100, 1), unemp_rate=round(v["12"] / v["22"] * 100, 1), work_year=2024)

# 4) unita' locali e addetti (ASIA 2024)
rows = sdmx("asia", "183_1163_DF_DICA_ASIAULP_TERRIFDATA_3", 5, {3: "0010", 4: "TOTAL"})
for c in CODES:
    for r in rows:
        if r["REF_AREA"] != c: continue
        if r["DATA_TYPE"] == "LU": out[c]["lu"] = int(float(r["OBS_VALUE"]))
        if r["DATA_TYPE"] == "LUEMPDAA": out[c]["empl"] = int(round(float(r["OBS_VALUE"])))

# 5) famiglie e abitazioni
rows = sdmx("fam", "DF_DCSS_FAM_POP_TV_1", 3, {})
for c in CODES:
    v = {r["INDICATOR"]: float(r["OBS_VALUE"]) for r in rows if r["REF_AREA"] == c}
    if "NPHH_AV" in v: out[c].update(households=int(v["NPHH_AV"]), hh_size=round(v["POPHH_AV"] / v["NPHH_AV"], 2))
rows = sdmx("dw", "DF_DCSS_ABITAZIONI_TV_1", 9, {2: "NUM_DW_AV+NUM_OCC_DW_AV+NUM_UNOCC_DW_AV", 3: "ALL", 4: "TOT"})
for c in CODES:
    v = {r["INDICATOR"]: float(r["OBS_VALUE"]) for r in rows if r["REF_AREA"] == c and r["TYPE_OF_BUILDING"] == "TOTAL" and r["ACCESS_BUILDING"] == "TOTAL"}
    if "NUM_DW_AV" in v: out[c].update(dwellings=int(v["NUM_DW_AV"]), unocc_pct=round(v.get("NUM_UNOCC_DW_AV", 0) / v["NUM_DW_AV"] * 100, 1))

# 6) redditi IRPEF (MEF, anno d'imposta 2024)
zpath = "raw_istat/irpef2024.zip"
if not os.path.exists(zpath):
    open(zpath, "wb").write(get("https://www1.finanze.gov.it/finanze/analisi_stat/public/v_4_0_0/contenuti/Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2024.zip?d=1615465800"))
z = zipfile.ZipFile(zpath)
text = z.read([n for n in z.namelist() if n.lower().endswith(".csv")][0]).decode("latin-1")
for r in csv.DictReader(io.StringIO(text), delimiter=";"):
    c = r["Codice Istat Comune"].strip().zfill(6)
    if c in out:
        n = num(r["Reddito complessivo - Frequenza"]); a = num(r["Reddito complessivo - Ammontare in euro"])
        if n and a: out[c].update(income=int(round(a / n)), taxpayers=int(num(r["Numero contribuenti"])), income_year=2024)

json.dump(out, open("istat_mb.json", "w", encoding="utf-8"), separators=(",", ":"))
miss = {k: sum(1 for c in CODES if k not in out[c]) for k in ["pop", "foreign_pct", "emp_rate", "lu", "households", "dwellings", "income"]}
print("scritto istat_mb.json; comuni senza dato:", miss, file=sys.stderr)
print("esempio Monza:", out["108033"], file=sys.stderr)
