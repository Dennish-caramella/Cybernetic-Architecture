"""P4 (margini tenuti fuori), da eseguire UNA sola volta e solo se P1-P3 passano (pre-registrazione v3 §2, v1 §6).
Unico file che legge le colonne di ds205 per NIL 'Minori' e '80 e + soli fam registrate in anagrafe'. Uso: python3 -I valida_p4.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, run

e3 = json.load(open(os.path.join(run.TAB, "P3_esito.json"))); e1 = json.load(open(os.path.join(run.TAB, "esito_base.json")))
assert e1["P1_passa"] and all(e1["P2"].values()) and e3["stesso_hash"] and e3["P1_tutti_10_semi"] and e3["P3_cv_ok"], "P1-P3 non passano: P4 resta chiuso"
t = pd.read_csv(os.path.join(run.OUT, f"nuclei_base_{run.SEME}.csv.gz"), low_memory=False); r = t[t.origine == "residente"]
q = pd.read_csv(run.raw("ds205.csv"), sep=";", encoding="latin1"); q = q[q.Anno == 2024].groupby("NIL")[["Minori", "80 e + soli fam registrate in anagrafe"]].sum()
s = pd.DataFrame(dict(sim_80soli=r[(r.tip == run.MONO) & (r.eta == 3)].groupby("nil").size(), sim_minori=r.groupby("nil").minori.sum())).fillna(0)
d = s.join(q, how="inner")
def m(sim, obs): return dict(n=len(sim), spearman=float(pd.Series(sim).corr(pd.Series(obs), method="spearman")), SRMSE=float(np.sqrt(np.mean((sim - obs) ** 2)) / np.mean(obs)), sim_tot=float(sim.sum()), obs_tot=float(obs.sum()))
a = m(d.sim_80soli.values, d["80 e + soli fam registrate in anagrafe"].values); b = m(d.sim_minori.values, d.Minori.values)
med = float(r.netto.median()); med65 = float(r[r.eta >= 2].netto.median())
res = dict(NIL_non_abbinati=sorted(set(s.index) ^ set(q.index)),
           P4a=dict(**a, passa=a["spearman"] >= 0.80 and a["SRMSE"] <= 0.30), P4b=dict(**b, passa=b["spearman"] >= 0.85 and b["SRMSE"] <= 0.25),
           P4c=dict(mediana_netta=med, banda=[0.9 * 36875, 1.5 * 36875], mediana_65=med65, banda_65=[0.8 * 27593, 1.5 * 27593],
                    passa=0.9 * 36875 <= med <= 1.5 * 36875 and 0.8 * 27593 <= med65 <= 1.5 * 27593), P4d="non applicabile (M10 [L])")
res["P4_passa"] = res["P4a"]["passa"] and res["P4b"]["passa"] and res["P4c"]["passa"]
d.to_csv(os.path.join(run.TAB, "P4_per_NIL.csv")); json.dump(res, open(os.path.join(run.TAB, "P4_esito.json"), "w"), indent=1, default=float)
print(json.dumps(res, indent=1, default=float))
