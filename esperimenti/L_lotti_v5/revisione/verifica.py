"""Revisione v5 (§7): ricalcola C5 dai fogli grezzi + chiave, analisi informative, C9. Uso: python revisione/verifica.py (dalla cartella della prova)."""
import math, pandas as pd, geopandas as gpd
def w(k, n, z=1.96):
    p = k / n; c = (p + z*z/(2*n)) / (1 + z*z/n); h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n); return round(p, 3), round(c-h, 3), round(c+h, 3)
def kap(x, y):
    po = (x == y).mean(); pe = sum((x == c).mean() * (y == c).mean() for c in set(x) | set(y)); return round((po-pe)/(1-pe), 3), round(po, 3)
k = pd.read_csv("chiavi/campione_chiave.csv", dtype=str)
a, b = (pd.read_csv(f"controllo_codificatore_{i}/codifica.csv", dtype=str).fillna("") for i in (1, 2))
d = k.merge(a, on="codice").merge(b, on="codice", suffixes=("_1", "_2"))
d["o1"], d["o2"] = d.Q1_1.isin(list("LCD")), d.Q1_2.isin(list("LCD"))
lo, ba = d[d.tipo == "lotto"], d[d.tipo == "base"]
print("kappa binario", kap(d.o1, d.o2), "kappa Q1", kap(d.Q1_1, d.Q1_2))
print("C5a", round((lo.o1.sum() + lo.o2.sum()) / 240, 4), "successi", lo.o1.sum() + lo.o2.sum(), "soglia 168; cod1", w(lo.o1.sum(), 120), "cod2", w(lo.o2.sum(), 120), "entrambi", w((lo.o1 & lo.o2).sum(), 120))
print("disaccordi binari: lotti", (lo.o1 != lo.o2).sum(), "base", (ba.o1 != ba.o2).sum(), "| note non vuote identiche", ((d.nota_1 == d.nota_2) & (d.nota_1 != "")).sum())
er = lo[lo.classe != "area di attivazione"]; print("E+R (informativo)", len(er), "cod1", w(er.o1.sum(), len(er)), "cod2", w(er.o2.sum(), len(er)))
for c, g in lo.groupby("classe"): print(" ", c, len(g), w(g.o1.sum() + g.o2.sum(), 2 * len(g)))
lo = lo.assign(a=lo.area_m2.astype(float)); print("lotti < 3.000 m2", (lo.a < 3000).sum(), round(lo[lo.a < 3000][["o1", "o2"]].values.mean(), 3), "| >= 3.000", round(lo[lo.a >= 3000][["o1", "o2"]].values.mean(), 3))
nuovi = lo[(lo.o1 | lo.o2) & lo.nota_2.str.contains("s2 nuov|s2 edificat|nuove costruz", regex=True)]
s = lo.o1.sum() + lo.o2.sum() - nuovi.o1.sum() - nuovi.o2.sum()
print("successi con nota s2 'nuovo edificio' (cod2):", list(nuovi.codice), "-> C5a se contati come insuccessi", round(s / 240, 3))
c1, c2 = (pd.read_csv(f"censimento_AT/codifica_{i}.csv", dtype=str).fillna("").set_index("ambito_id") for i in (1, 2))
m = c1.join(c2, lsuffix="_1", rsuffix="_2"); dis = m[m.categoria_1 != m.categoria_2]
print("C9 accordo", (m.categoria_1 == m.categoria_2).sum(), "| disaccordi", len(dis), dis.categoria_2.value_counts().to_dict(), "| cod2 con fonte non ufficiale", (dis.fonte_ufficiale_2 != "si").sum())
L = gpd.read_file("lotti_v5.gpkg", layer="lotti")
r = L[(L.classe == "lotto da riusare") & L.residenza_2030.isin(["no", "non verificata"])]
print("lotti da riusare in ambiti senza residenza/GFU", len(r), "cap_far1", r.cap_far1.sum(), "cap_recupero", r.cap_recupero.sum())
print("capacità FAR1 edificabili AT", L[(L.classe == "lotto edificabile") & (L.lotto_at == 1)].cap_far1.sum(), "su", L[L.classe == "lotto edificabile"].cap_far1.sum())
