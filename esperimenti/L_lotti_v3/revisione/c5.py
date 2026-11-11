"""Revisione indipendente Base L v3: C5 ricalcolato dalle tabelle pubblicate (codifica unita al campione), con e senza AT.
Uso: python revisione/c5.py  (legge solo tabelle/; non apre controllo_umano/ né controllo_secondo_codificatore/)."""
import os, numpy as np, pandas as pd
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tabelle")

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, c - h, c + h

def show(lab, s):
    p, lo, hi = wilson(s.sum(), len(s)); print(f"{lab:62s} {s.sum():3d}/{len(s):3d} = {p:.3f} [{lo:.3f}; {hi:.3f}]")
    return p, lo, hi

C = pd.read_csv(os.path.join(T, "controllo_ortofoto_esito.csv"), dtype=str).fillna("")
L = pd.read_csv(os.path.join(T, "lotti_attributi.csv"), dtype=str).fillna("")
C["ok"] = C.Q1.isin(list("LCD")); lo, ba = C[C.tipo == "lotto"], C[C.tipo == "base"]
at = lo.origine.str.startswith("AT"); scr = lo.id.isin(L.id[L.conferma_screening == "1"])
b = show("base (100 particelle)", ba.ok)
for lab, m in (("C5a pubblicato", lo.ok), ("senza edificabili AT", lo.ok[~(at & (lo.classe == "lotto edificabile"))]),
               ("senza ogni lotto di origine AT (anche attivazione AT/...)", lo.ok[~at]), ("senza AT e senza i 4 visti nello screening ds503", lo.ok[~at & ~scr]),
               ("solo AT (edificabili + attivazione)", lo.ok[at]), ("solo edificabili non AT", lo.ok[~at & (lo.classe == "lotto edificabile")])):
    a = show(lab, m)
    if lab != "solo AT (edificabili + attivazione)":  # Newcombe metodo 10 come run.py
        d = a[0] - b[0]; print(f"{'':62s} differenza con la base {d:.3f} [{d - np.hypot(a[0] - a[1], b[2] - b[0]):.3f}; {d + np.hypot(a[2] - a[0], b[0] - b[1]):.3f}]")
print("\nQ1 dei lotti AT nel campione:", lo[at].groupby(["classe", "Q1"]).size().to_dict())
# stima per la popolazione: post-stratificazione per classe x (AT / non AT), pesi = numerosità dei lotti in lotti_attributi
L["at"] = L.origine.str.startswith("AT"); lo = lo.assign(at=at.values)
pop = L.groupby(["classe", "at"]).size(); smp = lo.groupby(["classe", "at"]).ok.agg(["sum", "size"])
print("\nstrato (classe, AT): popolazione, campione, quota L/C/D\n", pd.concat([pop.rename("N"), smp], axis=1).assign(p=lambda d: (d["sum"] / d["size"]).round(3)))
w = pop / pop.sum(); print("stima post-stratificata, tutti i lotti:", round(float((w * smp["sum"] / smp["size"]).sum()), 3))
w2 = pop.xs(False, level="at"); w2 = w2 / w2.sum(); s2 = smp.xs(False, level="at")
print("stima post-stratificata, lotti non AT:", round(float((w2 * s2["sum"] / s2["size"]).sum()), 3))
print("quota del campione per classe vs popolazione:", (lo.classe.value_counts() / len(lo)).round(2).to_dict(), (L.classe.value_counts() / len(L)).round(2).to_dict())
