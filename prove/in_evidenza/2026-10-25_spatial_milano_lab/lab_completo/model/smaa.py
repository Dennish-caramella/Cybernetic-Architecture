"""Step 5: SMAA-2 on sites and portfolios with B's engine (unchanged). Archetypes are SYNTHETIC (B)."""
import numpy as np, pandas as pd
from config import *

E = load_prop("B_decision", "engine")


def weight_groups(S=None, seed=None, m=len(CRIT)):
    S = S or SMAA["S"]; rng = np.random.default_rng(SMAA["seed"] if seed is None else seed)
    G = {"uniform": rng.dirichlet(np.ones(m), S)}
    if m == len(CRIT):
        for k, mu in arch_means().items(): G[k] = rng.dirichlet(SMAA["kappa"] * np.array(mu), S)
    return G


def site_smaa(X, K=None, S=None):
    """X (n, m) benefit scores. Returns DataFrame with b1, top10, hol (uniform), top10_<arch>, min_arch, gic_arch,
    depth; plus the uniform rank-acceptability matrix of the reduced set (for the invariant test)."""
    K = K or SMAA["K"]; X = np.asarray(X, float); n = len(X)
    depth = E.dominance_depth(X); keep = np.where(depth < K)[0]
    G = weight_groups(S); out = pd.DataFrame(dict(depth=depth))
    for g, W in G.items():
        b, _ = E.smaa(X[keep], W, k=K)
        t = np.zeros(n); t[keep] = b.sum(1); out[f"top10_{g}"] = t
        if g == "uniform":
            b1 = np.zeros(n); b1[keep] = b[:, 0]; out["b1"] = b1
            h = np.zeros(n); h[keep] = b @ ((K - np.arange(K)) / K); out["hol"] = h
            B_uniform = b
    arch = [g for g in G if g != "uniform"]
    A = out[[f"top10_{a}" for a in arch]].values
    out["min_arch"] = A.min(1)
    Sn = len(G["uniform"]); out["gic_arch"] = np.prod((A * Sn + 1) / (Sn + 2), 1)
    # continuous holistic score for ranking outside the top-K reduced set: expected utility under uniform weights
    out["eu"] = X.mean(1)
    return out, B_uniform, keep


def portfolio_smaa(Xp, k=3, S=20000, seed=3):
    W = np.random.default_rng(seed).dirichlet(np.ones(Xp.shape[1]), S)
    b, _ = E.smaa(np.asarray(Xp, float), W, k=min(k, len(Xp)))
    return b
