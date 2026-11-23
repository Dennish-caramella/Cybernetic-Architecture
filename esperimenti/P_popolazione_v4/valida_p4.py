"""P4 (margini tenuti fuori), da eseguire UNA sola volta e solo se P1-P3 passano (pre-registrazione v3 §2, v1 §6).
Unico file che legge le colonne di ds205 per NIL 'Minori' e '80 e + soli fam registrate in anagrafe'.
Uso: python3 -I valida_p4.py            -> P4 vero (una volta sola, esito a registro)
     python3 -I valida_p4.py --prova    -> prova a vuoto: copia di ds205 SENZA le due colonne, sostituite da rumore;
                                           nessun valore stampato, nessun P4c (userebbe V3), output in _cache/P_popolazione_v3/prova_vuoto/"""
import json, os, sys
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
if PROVA:
    ok = len(d) == 87 and set(s.index) <= set(q.index) and all(np.isfinite([a["spearman"], a["SRMSE"], b["spearman"], b["SRMSE"], res["appendice_quote_minori"]["spearman"]]))
    json.dump(res, open(os.path.join(dest, "P4_prova_vuoto.json"), "w"), indent=1, default=float)
    print(dict(prova_a_vuoto="OK" if ok else "NON OK", NIL_simulati=len(s), NIL_ds205=len(q), NIL_abbinati=len(d), non_abbinati=res["NIL_non_abbinati"],
               chiavi=list(res), valori_finiti=ok)); sys.exit(0 if ok else 1)
med = float(r.netto.median()); med65 = float(r[r.eta >= 2].netto.median())
res["P4c"] = dict(mediana_netta=med, banda=[0.9 * 36875, 1.5 * 36875], mediana_65=med65, banda_65=[0.8 * 27593, 1.5 * 27593],
                  passa=0.9 * 36875 <= med <= 1.5 * 36875 and 0.8 * 27593 <= med65 <= 1.5 * 27593)
res["P4_passa"] = res["P4a"]["passa"] and res["P4b"]["passa"] and res["P4c"]["passa"]
d.to_csv(os.path.join(dest, "P4_per_NIL.csv")); json.dump(res, open(os.path.join(dest, "P4_esito.json"), "w"), indent=1, default=float)
print(json.dumps(res, indent=1, default=float))
