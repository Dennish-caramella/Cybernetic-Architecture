"""Valutazione multicriterio (WLC) con vincoli booleani, scenari di peso, analisi di sensibilità e frontiera di Pareto.

I pesi sono parametri dell'autore e degli attori, non risultati. L'analisi di sensibilità misura quanto
la classifica dipende da essi; la frontiera di Pareto mostra le celle che nessun'altra supera su tutti i criteri.
"""
import numpy as np
import pandas as pd


def normalize(df, crit_cfg, prov=None, winsor=(0.01, 0.99)):
    C = pd.DataFrame(index=df.index)
    for name, spec in crit_cfg.items():
        col = spec["colonna"]
        if col not in df or df[col].notna().sum() == 0:
            if prov is not None:
                prov.avviso(f"idoneità: criterio '{name}' escluso (colonna '{col}' assente o vuota)")
            continue
        s = df[col].astype(float)
        lo, hi = s.quantile(winsor[0]), s.quantile(winsor[1])
        s = s.clip(lo, hi)
        n = (s - lo) / (hi - lo) if hi > lo else pd.Series(0.5, index=s.index)
        n = n.fillna(n.median())
        C[name] = 1 - n if spec["direzione"] == "basso" else n
    return C


def constraint_mask(df, nomi, prov=None):
    ok = pd.Series(True, index=df.index)
    for c in nomi:
        if c in df:
            ok &= df[c].fillna(0) == 0
        else:
            if prov is not None:
                prov.data["vincoli_non_applicati"].append(c)
                prov.avviso(f"vincolo '{c}' NON applicato: dato assente")
    return ok


def renorm(weights, cols):
    w = pd.Series({k: v for k, v in weights.items() if k in cols}, dtype=float)
    return w / w.sum()


def score(C, weights):
    w = renorm(weights, C.columns)
    return (C[w.index] * w).sum(axis=1)


def sensitivity(C, valid, weights, n, conc, q, seed):
    """Frequenza con cui ogni cella cade nel quantile superiore sotto pesi perturbati (Dirichlet attorno al scenario)."""
    rng = np.random.default_rng(seed)
    w = renorm(weights, C.columns)
    draws = rng.dirichlet(conc * w.values + 1e-6, size=n)
    S = C[w.index].values @ draws.T                      # celle x estrazioni
    S = np.where(valid.values[:, None], S, -np.inf)
    freq = np.zeros(len(C))
    for j in range(S.shape[1]):
        col = S[:, j]
        v = col[np.isfinite(col)]
        t = np.quantile(v, q)
        freq += (col >= t)
    return pd.Series(freq / S.shape[1], index=C.index)


def pareto_front(C, valid):
    idx = C.index[valid.values]
    M = C.loc[idx].values
    nd = np.ones(len(M), bool)
    for i in range(len(M)):
        dom = (M >= M[i]).all(axis=1) & (M > M[i]).any(axis=1)
        if dom.any():
            nd[i] = False
    return pd.Series(False, index=C.index).where(~C.index.isin(idx[nd]), True)


def run(df, cfg, prov=None, seed=42):
    C = normalize(df, cfg["criteri"], prov)
    valid = constraint_mask(df, cfg["vincoli_booleani"], prov)
    out = C.add_prefix("crit_")
    out["valido"] = valid.astype(int)
    rep = {"criteri_usati": list(C.columns), "scenari": {}}
    for sc, w in cfg["scenari"].items():
        s = score(C, w).where(valid, 0.0)
        out[f"s_{sc}"] = s
        sens = sensitivity(C, valid, w, cfg["sensibilita"]["n_estrazioni"],
                           cfg["sensibilita"]["concentrazione"], cfg["sensibilita"]["quantile_top"], seed)
        out[f"robust_{sc}"] = sens
        rep["scenari"][sc] = {
            "pesi_dichiarati": w,
            "pesi_usati": renorm(w, C.columns).round(4).to_dict(),
            "celle_valide": int(valid.sum()),
        }
    out["pareto"] = pareto_front(C, valid).astype(int)
    rep["celle_pareto"] = int(out["pareto"].sum())
    rep["nota"] = ("La robustezza è la quota di estrazioni di pesi (Dirichlet attorno allo scenario) in cui la cella "
                   "resta nel quantile superiore. Non misura la qualità del lotto, solo la dipendenza dai pesi.")
    return out, rep
