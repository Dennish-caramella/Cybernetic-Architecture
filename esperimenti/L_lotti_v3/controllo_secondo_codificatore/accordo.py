"""Accordo tra primo codificatore (esecutore) e secondo codificatore cieco, e C5 ricalcolato. Uso: python accordo.py"""
import json, math, pandas as pd

LIB = set("LCD")  # libera o dismessa, come da pre-registrazione

def kappa(a, b):
    cats = sorted(set(a) | set(b)); n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((list(a).count(c) / n) * (list(b).count(c) / n) for c in cats)
    return (po - pe) / (1 - pe), po

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(p, 3), [round(c - h, 3), round(c + h, 3)]

e = pd.read_csv("../tabelle/controllo_ortofoto_esito.csv")            # chiave + primo codificatore
s = pd.read_csv("codifica_secondo.csv").rename(columns={"Q1": "Q1_2"})[["codice", "Q1_2"]]
m = e.merge(s, on="codice", validate="1:1")
assert len(m) == 200, len(m)
b1, b2 = m.Q1.isin(LIB), m.Q1_2.isin(LIB)

k7, po7 = kappa(m.Q1, m.Q1_2); kb, pob = kappa(b1.astype(int), b2.astype(int))
lot, base = m.tipo == "lotto", m.tipo != "lotto"
out = {
    "n": 200,
    "accordo_Q1_7_categorie": {"accordo": round(po7, 3), "kappa": round(k7, 3)},
    "accordo_binario_libera_o_dismessa": {"accordo": round(pob, 3), "kappa": round(kb, 3)},
    "C5a_lotti": {"primo": wilson(b1[lot].sum(), lot.sum()), "secondo": wilson(b2[lot].sum(), lot.sum()),
                  "entrambi_concordi_si": wilson((b1 & b2)[lot].sum(), lot.sum())},
    "base_particelle": {"primo": wilson(b1[base].sum(), base.sum()), "secondo": wilson(b2[base].sum(), base.sum())},
    "per_classe_secondo": {c: wilson(b2[lot & (m.classe == c)].sum(), (lot & (m.classe == c)).sum()) for c in m.classe[lot].unique()},
    "per_origine_secondo": {o: wilson(b2[lot & (m.origine == o)].sum(), (lot & (m.origine == o)).sum()) for o in m.origine[lot].unique()},
    "matrice_Q1": pd.crosstab(m.Q1, m.Q1_2).to_dict(),
}
json.dump(out, open("accordo.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: v for k, v in out.items() if k != "matrice_Q1"}, indent=1, ensure_ascii=False))
print(pd.crosstab(m.Q1, m.Q1_2, margins=True))
