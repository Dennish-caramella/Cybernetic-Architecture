"""Appendice informativa a P4 (REVISIONE §7.7 punto 2): quote di minori per residente per NIL, simulato contro ds205 2024.
Nessuna soglia. Si calcola SOLO all'apertura di P4 (da valida_p4.py) o nella prova a vuoto su dati con rumore."""
import numpy as np, pandas as pd

def quote_minori(r, q):
    """r: nuclei residenti simulati (nil, dim, minori); q: ds205 2024 per NIL con colonne Totale e Minori."""
    s = pd.DataFrame(dict(sim_minori=r.groupby("nil").minori.sum(), sim_persone=r.groupby("nil").dim.sum()))
    d = s.join(q[["Totale", "Minori"]], how="inner")
    sim, obs = (d.sim_minori / d.sim_persone).values, (d.Minori / d.Totale).values
    return dict(n=len(d), spearman=float(pd.Series(sim).corr(pd.Series(obs), method="spearman")),
                SRMSE=float(np.sqrt(np.mean((sim - obs) ** 2)) / np.mean(obs)), nota="informativo, senza soglia")
