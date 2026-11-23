"""P4 (margini tenuti fuori), da eseguire UNA sola volta e solo se P1-P3 passano (pre-registrazione v3 §2, v1 §6).
Unico file che legge le colonne di ds205 per NIL 'Minori' e '80 e + soli fam registrate in anagrafe'.
Uso: python3 -I valida_p4.py            -> P4 vero (una volta sola, esito a registro)
     python3 -I valida_p4.py --prova    -> prova a vuoto: copia di ds205 SENZA le due colonne, sostituite da rumore;
                                           nessun valore stampato, nessun P4c (userebbe V3), output in _cache/P_popolazione_v4/prova_vuoto/
[v4] P4e (cieco, V5 = mediana ISTAT dei comuni centro di area metropolitana) e P4f (informativo, Nord-ovest per componenti):
     scaricati SOLO nel ramo vero, nella stessa esecuzione che li confronta; nella prova si usano valori finti."""
import hashlib, io, json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, run
from appendice_minori import quote_minori

PROVA = "--prova" in sys.argv; V = ["Minori", "80 e + soli fam registrate in anagrafe"]
e3 = json.load(open(os.path.join(run.TAB, "P3_esito.json"))); e1 = json.load(open(os.path.join(run.TAB, "esito_base.json")))
assert e1["P1_passa"] and all(e1["P2"].values()) and e3["stesso_hash"] and e3["P1_tutti_10_semi"] and e3["P3_cv_ok"], "P1-P3 non passano: P4 resta chiuso"
t = pd.read_csv(os.path.join(run.OUT, f"nuclei_base_{run.SEME}.csv.gz"), low_memory=False); r = t[t.origine == "residente"]
if PROVA:
    cols = [c for c in pd.read_csv(run.raw("ds205.csv"), sep=";", encoding="latin1", nrows=0).columns if c not in V]
    q = pd.read_csv(run.raw("ds205.csv"), sep=";", encoding="latin1", usecols=cols)  # le due colonne non sono mai caricate
    g = np.random.default_rng(12345); q["Minori"] = g.integers(0, 10000, len(q)); q[V[1]] = g.integers(0, 3000, len(q))
    dest = os.path.join(run.OUT, "..", "prova_vuoto"); os.makedirs(dest, exist_ok=True); q.to_csv(os.path.join(dest, "ds205_rumore.csv"), sep=";", index=False)
else:
    q = pd.read_csv(run.raw("ds205.csv"), sep=";", encoding="latin1"); dest = run.TAB
q = q[q.Anno == 2024].groupby("NIL")[V + ["Totale"]].sum()
s = pd.DataFrame(dict(sim_80soli=r[(r.tip == run.MONO) & (r.eta == 3)].groupby("nil").size(), sim_minori=r.groupby("nil").minori.sum())).fillna(0)
d = s.join(q[V], how="inner")
def m(sim, obs): return dict(n=len(sim), spearman=float(pd.Series(sim).corr(pd.Series(obs), method="spearman")), SRMSE=float(np.sqrt(np.mean((sim - obs) ** 2)) / np.mean(obs)), sim_tot=float(sim.sum()), obs_tot=float(obs.sum()))
a = m(d.sim_80soli.values, d[V[1]].values); b = m(d.sim_minori.values, d.Minori.values)
res = dict(NIL_simulati=len(s), NIL_ds205=len(q), NIL_abbinati=len(d), NIL_non_abbinati=sorted(set(s.index) ^ set(q.index)),  # ds205 ha anche il NIL 8, senza famiglie in ds1441 2025: escluso dal confronto (join interno sugli 87 simulati)
           P4a=dict(**a, passa=a["spearman"] >= 0.80 and a["SRMSE"] <= 0.30), P4b=dict(**b, passa=b["spearman"] >= 0.85 and b["SRMSE"] <= 0.25),
           appendice_quote_minori=quote_minori(r, q), P4d="non applicabile (M10 [L])")
# [v4] P4e e P4f
SDMX = "https://esploradati.istat.it/SDMXWS/rest/data/IT1,32_292_DF_DCCV_REDNETFAMFONTERED_{f},1.0/"
def istat(f, key):
    b = urllib.request.urlopen(urllib.request.Request(SDMX.format(f=f) + key, headers={"User-Agent": "tesi-base-P/4.0", "Accept": "application/vnd.sdmx.data+csv;version=1.0.0"}), timeout=300).read()
    os.makedirs(os.path.join(run.OUT, "..", "p4"), exist_ok=True); open(os.path.join(run.OUT, "..", "p4", f"rednet_{f}.csv"), "wb").write(b)
    return pd.read_csv(io.BytesIO(b)), hashlib.sha256(b).hexdigest()
if PROVA:
    v5 = dict(valore=30000.0, anno="finto"); itc = pd.DataFrame(dict(NUMBER_HOUSEHOLD_COMP=["1", "2", "3", "4", "7"], OBS_VALUE=[20000.0, 30000, 35000, 40000, 40000]))
else:
    t9, h9 = istat(9, ".2.REDD_MEDIANO_FAM..2.9........"); t9 = t9[t9.REF_AREA.astype(str) == "2"]
    a9 = 2024 if (t9.TIME_PERIOD == 2024).any() else int(t9.TIME_PERIOD.max()); v5 = dict(valore=float(t9[t9.TIME_PERIOD == a9].OBS_VALUE.iloc[0]), anno=a9, sha256=h9)
    t1, h1 = istat(1, ".ITC.REDD_MEDIANO_FAM..2.9........"); t1 = t1[t1.TIME_PERIOD == a9]; itc = t1[["NUMBER_HOUSEHOLD_COMP", "OBS_VALUE"]]; v5["sha256_p4f"] = h1
med_all = float(r.netto.median())
res["P4e"] = dict(V5=v5, mediana_netta_sim=med_all, banda=[0.9 * v5["valore"], 1.5 * v5["valore"]], passa=0.9 * v5["valore"] <= med_all <= 1.5 * v5["valore"])
dimc = np.minimum(r.dim, 5).map({1: "1", 2: "2", 3: "3", 4: "4", 5: "7"}); simd = r.groupby(dimc).netto.median()
ic = itc.assign(k=itc.NUMBER_HOUSEHOLD_COMP.astype(str)).set_index("k").OBS_VALUE
res["P4f_informativo"] = {k: dict(sim=float(simd.get(k, np.nan)), ITC=float(ic.get(k, np.nan)), rapporto=float(simd.get(k, np.nan) / ic.get(k, np.nan))) for k in ["1", "2", "3", "4", "7"]}
if PROVA:
    ok = len(d) == 87 and set(s.index) <= set(q.index) and all(np.isfinite([a["spearman"], a["SRMSE"], b["spearman"], b["SRMSE"], res["appendice_quote_minori"]["spearman"]]))
    json.dump(res, open(os.path.join(dest, "P4_prova_vuoto.json"), "w"), indent=1, default=float)
    print(dict(prova_a_vuoto="OK" if ok else "NON OK", NIL_simulati=len(s), NIL_ds205=len(q), NIL_abbinati=len(d), non_abbinati=res["NIL_non_abbinati"],
               chiavi=list(res), valori_finiti=ok)); sys.exit(0 if ok else 1)
med = float(r.netto.median()); med65 = float(r[r.eta >= 2].netto.median())
res["P4c"] = dict(mediana_netta=med, banda=[0.9 * 36875, 1.5 * 36875], mediana_65=med65, banda_65=[0.8 * 27593, 1.5 * 27593],
                  passa=0.9 * 36875 <= med <= 1.5 * 36875 and 0.8 * 27593 <= med65 <= 1.5 * 27593)
res["P4_passa"] = res["P4a"]["passa"] and res["P4b"]["passa"] and res["P4c"]["passa"] and res["P4e"]["passa"]  # [v4] + P4e
d.to_csv(os.path.join(dest, "P4_per_NIL.csv")); json.dump(res, open(os.path.join(dest, "P4_esito.json"), "w"), indent=1, default=float)
print(json.dumps(res, indent=1, default=float))
