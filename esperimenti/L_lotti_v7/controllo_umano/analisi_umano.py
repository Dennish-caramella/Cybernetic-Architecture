"""Analisi del controllo umano (PREREG_controllo_umano.txt §3-4): quota pesata, esito, confronto con i modelli. Uso: python3 -I analisi_umano.py"""
import numpy as np, pandas as pd
H = "."; K = pd.read_csv(f"{H}/chiave_umano.csv"); U = pd.read_csv(f"{H}/codifica_umana.csv", keep_default_na=False)
D = K.merge(U, on="codice", validate="1:1"); OK = set("LCD"); N = {"F-E": 173, "F-R": 147, "F-A": 245, "D-E": 43, "D-R": 20, "D-A": 23}; W = {h: n / 651 for h, n in N.items()}
def pw(ok, ex=None):
    d = D.assign(ok=ok); d = d[~ex] if ex is not None else d; g = d.groupby("strato").ok.agg(["sum", "count"])
    p = sum(W[h] * g.loc[h, "sum"] / g.loc[h, "count"] for h in g.index) / sum(W[h] for h in g.index)  # pesi rinormalizzati se uno strato è vuoto
    ph = (g["sum"] + 0.5) / (g["count"] + 1); se = np.sqrt(sum(W[h] ** 2 * ph[h] * (1 - ph[h]) / (g.loc[h, "count"] - 1) for h in g.index if g.loc[h, "count"] > 1))
    return p, se, g["sum"].to_dict()
ok = D.Q1.isin(OK); p, se, k = pw(ok); print(f"p (X = non successo) = {p:.3f}  SE {se:.3f}  IC95 [{p-1.96*se:.3f}; {p+1.96*se:.3f}]  successi per strato {k}")
esito = "PASSA con riscontro umano" if p >= 0.75 else ("NON PASSA" if p < 0.65 else "INCONCLUDENTE (0,65-0,75)"); print("esito pre-registrato:", esito)
print("X:", int((D.Q1 == "X").sum()), "| sensibilità X escluse: p = %.3f" % pw(ok, D.Q1 == "X")[0])
ag = D.nota.str.contains("agricol"); print("sensibilità note 'agricolo' come V (H36, H57):", D.codice[ag].tolist(), "p = %.3f" % pw(ok & ~ag)[0])
print("per classe:", D.groupby("classe").apply(lambda d: round(d.Q1.isin(OK).mean(), 2)).to_dict(), "| fuori ambito %.2f in ambito %.2f (medie semplici)" % (ok[D.strato.str[0] == "F"].mean(), ok[D.strato.str[0] == "D"].mean()))
print("distribuzione Q1:", D.Q1.value_counts().to_dict())
# confronto con i modelli sui lotti in comune (chiave v7: id -> codice C5xx)
kv = pd.read_csv("../chiavi/campione_chiave_v7.csv", dtype=str); kv = kv[kv.tipo == "lotto"].set_index("id").codice
for n, nm in ((1, "Opus"), (2, "Haiku")):
    m = pd.read_csv(f"../controllo_codificatore_{n}/codifica.csv", dtype=str).set_index("codice").Q1
    c = D[D.id.isin(kv.index)].assign(cod=lambda d: d.id.map(kv)); c = c.assign(mo=c.cod.map(m).isin(OK), um=c.Q1.isin(OK))
    a = c.um.mean(); b = c.mo.mean(); po = (c.um == c.mo).mean(); pe = a * b + (1 - a) * (1 - b)
    print(f"{nm}: {len(c)} lotti in comune | quota Dennis {a:.2f} vs {nm} {b:.2f} | accordo {po:.2f} kappa {(po-pe)/(1-pe) if pe<1 else float('nan'):.2f} | Dennis sì/{nm} no {(c.um&~c.mo).sum()}, Dennis no/{nm} sì {(~c.um&c.mo).sum()}")
