"""Invarianti P2 sull'esecuzione di base scritta da `run.py esegui --scrivi`. Uso: python3 -I test_popolazione.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, run

t = pd.read_csv(os.path.join(run.OUT, f"nuclei_base_{run.SEME}.csv.gz"), low_memory=False)
a = pd.read_csv(os.path.join(run.OUT, f"ancore_base_{run.SEME}.csv.gz"))
for c in ["richiedente", "isee_14_16", "fascia_grigia"]: t[c] = t[c].astype(bool)
c, info = run.p2(t, a, tol_netto=0.2)  # nel file budget e netto sono arrotondati al centesimo: un netto < 0,2 EUR da budget 0,00
for k, v in c.items(): print("OK " if v else "NO ", k)
print(info)
sys.exit(0 if all(c.values()) else 1)
