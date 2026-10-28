"""PCA e K-Means con validazione. Nessuna etichetta funzionale è imposta ai cluster:
i cluster sono descritti dai loro profili e interpretati dall'autore."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler


def prepare(df, cfg, prov=None):
    feats = [f for f in cfg["feature"] if f in df.columns]
    missing = [f for f in cfg["feature"] if f not in df.columns]
    if prov is not None:
        prov.data["feature_assenti"] = missing
        if missing:
            prov.avviso(f"clustering: feature assenti, non usate: {missing}")
    X = df[feats].copy()
    drop = [c for c in X if X[c].isna().mean() > 0.5]
    if drop:
        if prov is not None:
            prov.avviso(f"clustering: feature con >50% valori mancanti, escluse: {drop}")
        X = X.drop(columns=drop)
    for c in X:
        if X[c].isna().any():
            if prov is not None:
                prov.avviso(f"clustering: '{c}' ha {int(X[c].isna().sum())} mancanti, imputati con la mediana")
            X[c] = X[c].fillna(X[c].median())
    for c in cfg.get("log1p", []):
        if c in X:
            X[c] = np.log1p(X[c].clip(lower=0))
    lo, hi = cfg["winsor"]
    for c in X:
        a, b = X[c].quantile([lo, hi])
        X[c] = X[c].clip(a, b)
    keep = [c for c in X if X[c].std() > 1e-12]
    return X[keep]


def run(df, cfg, prov=None):
    X = prepare(df, cfg, prov)
    if X.shape[1] < 2:
        raise ValueError(f"Servono almeno 2 feature utilizzabili per PCA/K-Means, trovate: {list(X.columns)}")
    Z = StandardScaler().fit_transform(X)
    ncomp = min(cfg["n_componenti"], X.shape[1])
    pca = PCA(n_components=ncomp, random_state=cfg["seed"]).fit(Z)
    PC = pca.transform(Z)
    loadings = pd.DataFrame(pca.components_.T, index=X.columns, columns=[f"PC{i+1}" for i in range(ncomp)])

    k0, k1 = cfg["k_range"]
    sel = []
    for k in range(k0, min(k1, len(X) - 1) + 1):
        km = KMeans(n_clusters=k, n_init=20, random_state=cfg["seed"]).fit(PC)
        sel.append({
            "k": k,
            "silhouette": float(silhouette_score(PC, km.labels_)),
            "davies_bouldin": float(davies_bouldin_score(PC, km.labels_)),
            "calinski_harabasz": float(calinski_harabasz_score(PC, km.labels_)),
            "inerzia": float(km.inertia_),
        })
    k = cfg["k_forzato"] or max(sel, key=lambda r: r["silhouette"])["k"]
    km = KMeans(n_clusters=k, n_init=50, random_state=cfg["seed"]).fit(PC)
    # ordine stabile dei cluster: per media di PC1 crescente
    order = np.argsort([PC[km.labels_ == i, 0].mean() for i in range(k)])
    remap = {int(old): int(new) for new, old in enumerate(order)}
    labels = np.array([remap[int(l)] for l in km.labels_])

    rng = np.random.default_rng(cfg["seed"])
    aris = []
    for _ in range(cfg["n_bootstrap"]):
        idx = rng.choice(len(PC), size=int(0.8 * len(PC)), replace=False)
        kb = KMeans(n_clusters=k, n_init=10, random_state=int(rng.integers(1e9))).fit(PC[idx])
        aris.append(adjusted_rand_score(km.labels_, kb.predict(PC)))

    prof_raw = df.loc[X.index, [c for c in df.columns if c in cfg["feature"]]].groupby(labels).mean()
    z = (X - X.mean()) / X.std()
    z_prof = z.groupby(labels).mean()
    tratti = {}
    for cl in z_prof.index:
        r = z_prof.loc[cl].sort_values()
        tratti[int(cl)] = {
            "alto": [f"{n} ({v:+.2f})" for n, v in r[::-1].head(3).items() if v > 0.25],
            "basso": [f"{n} ({v:+.2f})" for n, v in r.head(3).items() if v < -0.25],
            "n_celle": int((labels == cl).sum()),
        }
    report = {
        "feature_usate": list(X.columns),
        "varianza_spiegata": [float(v) for v in pca.explained_variance_ratio_],
        "varianza_cumulata": float(pca.explained_variance_ratio_.sum()),
        "caricamenti": loadings.round(4).to_dict(),
        "selezione_k": sel,
        "k_scelto": int(k),
        "k_forzato": bool(cfg["k_forzato"]),
        "stabilita_bootstrap_ari_media": float(np.mean(aris)),
        "stabilita_bootstrap_ari_min": float(np.min(aris)),
        "profili_medi_grezzi": prof_raw.round(3).to_dict(orient="index"),
        "tratti_distintivi": tratti,
        "nota_k": "La silhouette tende a preferire K piccoli: valutare anche K maggiori con interpretabilità e stabilità (k_forzato).",
        "nota": "I cluster non hanno etichette funzionali: l'interpretazione (es. quali cluster siano adatti a quale uso) spetta all'autore.",
    }
    scores = pd.DataFrame(PC, index=X.index, columns=[f"PC{i+1}" for i in range(ncomp)])
    scores["cluster"] = labels
    return scores, report
