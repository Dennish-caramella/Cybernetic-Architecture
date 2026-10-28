"""Experiments E1-E5 for the cybernetic participation engine (Researcher B).

Usage:  PYTHONPATH=C:/Temp/pl python run.py [e1 e2 e3 e4 e5]   (default: all)
Outputs in results/. Real data: parcels.csv.gz (lab/data). SYNTHETIC: archetype
weight distributions and simulated respondents (marked SYN in outputs).
"""
import sys, json, time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import expit
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import engine as E

HERE = Path(__file__).parent
RES = HERE / "results"; RES.mkdir(exist_ok=True)
DATA = HERE.parents[1] / "data" / "parcels.csv.gz"
K = 10                       # top-k of interest
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
except ImportError:
    plt = None

# SYNTHETIC archetypes: Dirichlet(kappa * mean) over CRIT =
# [access, need, green, heat, capacity, mix, cost]. Means are plausible, literature-
# inspired (see model.md section 3), NOT measured preferences.
ARCH = {
    "young_worker": [0.30, 0.20, 0.08, 0.07, 0.10, 0.10, 0.15],
    "family_children": [0.12, 0.12, 0.25, 0.15, 0.08, 0.18, 0.10],
    "elderly": [0.25, 0.08, 0.17, 0.30, 0.05, 0.10, 0.05],
    "commuter": [0.40, 0.10, 0.05, 0.05, 0.10, 0.05, 0.25],
}
KAPPA = 40.0
M = len(E.CRIT)


def arch_sample(name, n, rng, arch=None):
    return rng.dirichlet(KAPPA * np.array((arch or ARCH)[name]), n)


def build():
    c = E.candidate_pool(DATA)
    raw, X = E.criteria_matrix(c)
    depth = E.dominance_depth(X.values)
    keep = depth < K
    R = c[keep].reset_index(drop=True)
    return c, raw, X, depth, R, X[keep].reset_index(drop=True).values, raw[keep].reset_index(drop=True)


def short(ctx):
    """SMAA short-list: parcels with P(top-10) > 0 under uniform or any archetype weights (from E1).
    Questions and rankings in E2-E5 use this list (real parcels)."""
    if not (RES / "e1_smaa_candidates.csv").exists():
        e1(ctx)
    d = pd.read_csv(RES / "e1_smaa_candidates.csv", dtype={"ref": str})
    d = d[d.filter(regex=r"^top10_(uniform|young|family|elderly|commuter)").max(axis=1) > 0].reset_index(drop=True)
    return d, d[E.CRIT].values


def label(R, i):
    return f"{R.ref[i]} ({R.nil_name[i]}, {R.raw_access[i]:.2f} km to {R.metro_nearest[i]})"

# ------------------------------------------------------------------ E1 criteria + SMAA
def e1(ctx):
    c, raw, X, depth, R, XR, rawR = ctx
    rng = np.random.default_rng(1)
    spec = {
        "pool_filter": "kind==land & area>=1000 m2 & (soft_site | max(pgt_rig,pgt_dism,pgt_tras)>0.3) & "
                       "max(pgt_srv_verde,pgt_agr,pgt_pae,dusaf_wat)<0.5 & gfa_headroom>0 & NIL rent/income known & inside city",
        "n_pool": int(len(c)), "n_reduced_depth_lt_k": int(len(R)), "k": K,
        "normalisation": "robust min-max on pool p2-p98, clipped to [0,1], cost criteria reversed",
        "criteria": {
            "access": "metro_km (parcel, km), lower better",
            "need": "nil_rent*60/nil_net_m: OMI rent of a 60 m2 flat / net monthly income per taxpayer (NIL), higher = more affordability need",
            "green": "0.5*nil_green (higher better) + 0.5*green_srv_km (parcel, lower better)",
            "heat": "nil_heatrisk, lower better",
            "capacity": "log10(gfa_headroom_m2) (assumption-based proxy), higher better",
            "mix": "nil_poor (% taxpayers <= 15k), lower better (poverty deconcentration; policy assumption)",
            "cost": "nil_price OMI EUR/m2, lower better (land cost proxy)"},
        "spearman_pool": X.corr("spearman").round(3).to_dict(),
    }
    json.dump(spec, open(RES / "criteria_spec.json", "w"), indent=1)
    out = pd.concat([R[["ref", "nil_id", "nil_name", "x", "y", "area_m2", "metro_nearest"]], rawR.add_prefix("raw_"),
                     pd.DataFrame(XR, columns=E.CRIT)], axis=1)
    out["dominance_depth"] = depth[depth < K]
    # SMAA-2 under uniform weights and each SYNTHETIC archetype
    S = 20000
    groups = {"uniform": rng.dirichlet(np.ones(M), S)} | {a: arch_sample(a, S, rng) for a in ARCH}
    topk = {}
    for g, W in groups.items():
        b, wc = E.smaa(XR, W, k=K)
        topk[g] = b.sum(1)
        out[f"b1_{g}"] = b[:, 0]
        out[f"top{K}_{g}"] = b.sum(1)
        if g == "uniform":
            out["holistic_uniform"] = b @ ((K - np.arange(K)) / K)     # meta-weights (K-r+1)/K
            for j, cr in enumerate(E.CRIT):
                out[f"wc_{cr}"] = wc[:, j]
            sel = np.where(b[:, 0] >= 0.01)[0]
            wc2 = np.full_like(wc, np.nan); wc2[sel] = wc[sel]
            out["confidence_sd05"] = E.confidence_factor(XR, wc2, 0.05, S=1000)
            bu = b
    A = np.column_stack([topk[a] for a in ARCH])
    out["top10_min_archetypes"] = A.min(1)                          # robust-for-all
    out["top10_gic_archetypes"] = np.prod((A * S + 1) / (S + 2), 1)  # Polis-style product
    out = out.sort_values("holistic_uniform", ascending=False)
    out.to_csv(RES / "e1_smaa_candidates.csv", index=False, float_format="%.4g")
    summ = {"n_pool": len(c), "n_reduced": len(R), "n_nil_reduced": int(R.nil_id.nunique()),
            "top_by_holistic_uniform": out.head(10)[["ref", "nil_name", "holistic_uniform", "b1_uniform", f"top{K}_uniform", "confidence_sd05"]].to_dict("records"),
            "top_by_min_archetype_top10": out.sort_values("top10_min_archetypes", ascending=False).head(10)[["ref", "nil_name", "top10_min_archetypes"] + [f"top{K}_{a}" for a in ARCH]].to_dict("records"),
            "n_parcels_with_b1_gt0_uniform": int((out.b1_uniform > 0).sum()),
            "overlap_top10_by_archetype": {a: int(len(set(out.nlargest(K, f"top{K}_{a}").ref) & set(out.nlargest(K, f"top{K}_uniform").ref))) for a in ARCH}}
    json.dump(summ, open(RES / "e1_summary.json", "w"), indent=1, default=float)
    if plt:
        top = out.head(15)
        fig, ax = plt.subplots(1, 2, figsize=(13, 5.5))
        b15 = bu[top.index.values]
        left = np.zeros(len(top))
        for r in range(K):
            ax[0].barh(range(len(top)), b15[:, r], left=left, color=plt.cm.viridis(r / K), label=f"rank {r+1}")
            left += b15[:, r]
        ax[0].set_yticks(range(len(top)), [f"{t.ref} {t.nil_name[:14]}" for t in top.itertuples()], fontsize=7)
        ax[0].invert_yaxis(); ax[0].set_xlabel("rank acceptability b^r (uniform weights)"); ax[0].legend(fontsize=6, ncol=2)
        hm = out.sort_values("top10_min_archetypes", ascending=False).head(20)
        im = ax[1].imshow(hm[[f"top{K}_{g}" for g in groups]].values, cmap="magma", vmin=0, vmax=1, aspect="auto")
        ax[1].set_xticks(range(len(groups)), list(groups), rotation=30, fontsize=7)
        ax[1].set_yticks(range(len(hm)), [f"{t.ref} {t.nil_name[:14]}" for t in hm.itertuples()], fontsize=7)
        ax[1].set_title("P(top-10) by weight distribution (archetypes SYNTHETIC)", fontsize=9)
        plt.colorbar(im, ax=ax[1]); fig.tight_layout(); fig.savefig(RES / "e1_smaa.png", dpi=130); plt.close(fig)
    print("E1", json.dumps({k: summ[k] for k in ["n_pool", "n_reduced", "n_nil_reduced", "n_parcels_with_b1_gt0_uniform", "overlap_top10_by_archetype"]}))

# ------------------------------------------------------------------ simulation helpers
def uniform_prior():
    return (lambda P, r: r.dirichlet(np.ones(M), P), lambda W: E.dirichlet_logpdf(W, np.ones(M)))


def pair_pool(XR, rng, n=200):
    pr = rng.integers(0, len(XR), (3 * n, 2))
    D = XR[pr[:, 0]] - XR[pr[:, 1]]
    ok = (D > 1e-9).any(1) & (D < -1e-9).any(1)          # skip Pareto-dominated pairs
    return pr[ok][:n]


def respond(w, xa, xb, beta, flip, rng):
    y = rng.random() < expit(beta * w @ (xa - xb))
    return int(y ^ (rng.random() < flip))


def metrics(wt, wh, XR):
    ut, uh = XR @ wt, XR @ wh
    tt, th = np.argsort(-ut)[:K], np.argsort(-uh)[:K]
    rng_u = ut.max() - np.median(ut)
    return dict(tv=0.5 * np.abs(wt - wh).sum(), top10=len(set(tt) & set(th)) / K,
                top1=float(tt[0] == th[0]), regret=(ut.max() - ut[th[0]]) / rng_u,
                regret10=(ut[tt].mean() - ut[th].mean()) / rng_u)


def run_participant(XR, wt, strategy, Q, beta_r, flip, rng, prior=None, P=2000, rec=True):
    ps, pl = prior or uniform_prior()
    L = E.PrefLearner(XR, ps, pl, P=P, beta=15.0, eps=0.05, rng=rng)
    rows = [metrics(wt, L.mean(), XR) | {"q": 0}] if rec else []
    for q in range(1, Q + 1):
        pr = pair_pool(XR, rng)
        a, b = pr[rng.integers(len(pr))] if strategy == "random" else pr[L.scores(pr, strategy).argmax()]
        L.update(a, b, respond(wt, XR[a], XR[b], beta_r, flip, rng))
        if rec:
            rows.append(metrics(wt, L.mean(), XR) | {"q": q})
    return L, rows

# ------------------------------------------------------------------ E2 active learning
def e2(ctx, N=32, Q=25):
    XR = short(ctx)[1]
    rng = np.random.default_rng(2)
    noise = {"low_b50": (50, 0), "mid_b15": (15, 0), "high_b5": (5, 0), "flip20_b50": (50, 0.2)}
    rows = []
    t0 = time.time()
    names = list(ARCH)
    truths = [arch_sample(names[i % 4], 1, rng)[0] for i in range(N)]   # SYNTHETIC respondents
    for nz, (br, fl) in noise.items():
        for st in ["random", "w", "top"]:
            for i, wt in enumerate(truths):
                _, r = run_participant(XR, wt, st, Q, br, fl, np.random.default_rng(1000 * i + 7))
                rows += [x | {"noise": nz, "strategy": st, "pid": i, "arch": names[i % 4]} for x in r]
    df = pd.DataFrame(rows)
    df.to_csv(RES / "e2_learning_curves_raw.csv", index=False, float_format="%.4g")
    g = df.groupby(["noise", "strategy", "q"])[["tv", "top10", "top1", "regret", "regret10"]].mean().reset_index()
    g.to_csv(RES / "e2_learning_curves_mean.csv", index=False, float_format="%.4g")
    # questions needed to reach top-10 overlap >= 0.7 and regret <= 0.05 (first q where mean crosses)
    need = []
    for (nz, st), h in g.groupby(["noise", "strategy"]):
        def first(cond):
            q = h.q[cond(h)].min(); return None if pd.isna(q) else int(q)
        need.append(dict(noise=nz, strategy=st, q_top10_ge_0_7=first(lambda h: h.top10 >= 0.7),
                         q_regret10_le_0_05=first(lambda h: h.regret10 <= 0.05), q_tv_le_0_15=first(lambda h: h.tv <= 0.15),
                         **{f"{m}_q0": float(h[h.q == 0][m].iloc[0]) for m in ["tv", "top10", "regret10"]},
                         **{f"{m}_q10": float(h[h.q == 10][m].iloc[0]) for m in ["tv", "top10", "regret", "regret10"]},
                         **{f"{m}_q25": float(h[h.q == Q][m].iloc[0]) for m in ["tv", "top10", "regret", "regret10"]}))
    se = df[df.q == Q].groupby(["noise", "strategy"])[["tv", "regret10"]].sem().add_suffix(f"_q{Q}_se").reset_index()
    need = pd.DataFrame(need).merge(se, on=["noise", "strategy"])
    pd.DataFrame(need).to_csv(RES / "e2_questions_needed.csv", index=False, float_format="%.4g")
    if plt:
        fig, ax = plt.subplots(3, 4, figsize=(15, 9), sharex=True)
        for j, nz in enumerate(noise):
            for st, col in zip(["random", "w", "top"], ["grey", "tab:blue", "tab:red"]):
                h = g[(g.noise == nz) & (g.strategy == st)]
                lab = {"random": "random pair", "w": "EIG on w (BALD)", "top": "EIG on top parcel"}[st]
                ax[0, j].plot(h.q, h.tv, color=col, label=lab); ax[1, j].plot(h.q, h.top10, color=col); ax[2, j].plot(h.q, h.regret10, color=col)
            ax[0, j].set_title(nz, fontsize=9)
        ax[0, 0].set_ylabel("weight error (TV)"); ax[1, 0].set_ylabel("top-10 overlap"); ax[2, 0].set_ylabel("top-10 utility regret")
        ax[0, 0].legend(fontsize=7); [a.set_xlabel("questions") for a in ax[2]]
        fig.suptitle(f"E2: simulated respondents (SYNTHETIC), N={N} per cell", fontsize=10)
        fig.tight_layout(); fig.savefig(RES / "e2_learning_curves.png", dpi=130); plt.close(fig)
    print(f"E2 done {time.time()-t0:.0f}s"); print(pd.DataFrame(need).to_string())

# ------------------------------------------------------------------ E3 population prior (cybernetic loop)
def pop_prior(means, mix_u=0.3, kappa=50.0):
    Mn = np.array(means)
    def sample(P, r):
        W = r.dirichlet(np.ones(M), P)
        k = r.random(P) >= mix_u
        W[k] = r.gamma(kappa * Mn[r.integers(len(Mn), size=k.sum())])
        return W / W.sum(1, keepdims=True)
    def logpdf(W):
        lu = E.dirichlet_logpdf(W, np.ones(M))
        lg = np.stack([E.dirichlet_logpdf(W, kappa * m) for m in Mn], 1)
        lg = np.logaddexp.reduce(lg, 1) - np.log(len(Mn))
        return np.logaddexp(np.log(mix_u) + lu, np.log(1 - mix_u) + lg)
    return sample, logpdf


def e3(ctx, N=50, Q=8, seeds=2, minority=0.2):
    XR = short(ctx)[1]
    rows = []
    t0 = time.time()
    for seed in range(seeds):
        rng = np.random.default_rng(300 + seed)
        is_min = rng.random(N) < minority
        truths = [arch_sample("elderly" if m else "young_worker", 1, rng)[0] for m in is_min]  # SYNTHETIC
        for mode in ["uniform", "population"]:
            means = []
            for i, wt in enumerate(truths):
                prior = pop_prior(means) if (mode == "population" and len(means) >= 5) else None
                L, r = run_participant(XR, wt, "w", Q, 15, 0, np.random.default_rng(seed * 10000 + i), prior=prior)
                means.append(L.mean())
                rows += [x | {"seed": seed, "prior": mode, "pid": i, "minority": bool(is_min[i])} for x in r if x["q"] in (0, 2, 4, 8)]
    df = pd.DataFrame(rows)
    df.to_csv(RES / "e3_population_prior_raw.csv", index=False, float_format="%.4g")
    df["late"] = df.pid >= N // 2
    s = df.groupby(["prior", "minority", "late", "q"])[["tv", "top10", "regret", "regret10"]].mean().reset_index()
    s.to_csv(RES / "e3_population_prior_summary.csv", index=False, float_format="%.4g")
    print(f"E3 done {time.time()-t0:.0f}s"); print(s[s.q.isin([4, 8])].to_string())
    if plt:
        fig, ax = plt.subplots(figsize=(6, 4))
        for (pr, mi), h in df[df.q == 4].groupby(["prior", "minority"]):
            h = h.groupby("pid").tv.mean().rolling(10, min_periods=3).mean()
            ax.plot(h.index, h.values, label=f"{pr} prior, {'minority (elderly)' if mi else 'majority (young)'}",
                    ls="-" if pr == "population" else "--", color="tab:red" if mi else "tab:blue")
        ax.set_xlabel("participant index (arrival order)"); ax.set_ylabel("TV weight error after 4 questions")
        ax.set_title("E3: learning across participants (SYNTHETIC)", fontsize=9); ax.legend(fontsize=7)
        fig.tight_layout(); fig.savefig(RES / "e3_population_prior.png", dpi=130); plt.close(fig)

# ------------------------------------------------------------------ E4 aggregation & fairness
def aggregate_all(U, Wm, XR, labels_true, rng):
    """U (N, n) learned utilities; returns dict method -> chosen set of K parcels."""
    N = len(U)
    approve = np.zeros_like(U, bool)
    np.put_along_axis(approve, np.argsort(-U, 1)[:, :K], True, 1)
    out = {"mean_weights": list(np.argsort(-(XR @ Wm.mean(0)))[:K]),
           "borda": list(np.argsort(-E.borda(U))[:K])}
    cand = np.argsort(-E.borda(U))[:20]
    out["kemeny"] = list(E.kemeny(U, cand)[:K])
    out["seq_pav"] = E.seq_pav(approve, K)
    best, lab = -1, None
    for k in range(2, 6):    # opinion groups from learned weights (Polis: PCA + k-means; here direct k-means on simplex)
        l = KMeans(k, n_init=10, random_state=0).fit_predict(Wm)
        s = silhouette_score(Wm, l)
        if s > best: best, lab = s, l
    gic, _ = E.group_informed_consensus(U, lab, K)
    out["gic"] = list(np.argsort(-gic)[:K])
    return out, lab


def fairness(S, Ut, groups, k=K):
    """Normalised satisfaction per voter: (mean u(S) - mean u) / (mean u(own top-k) - mean u)."""
    own = -np.sort(-Ut, 1)[:, :k].mean(1)
    base = Ut.mean(1)
    sat = (Ut[:, S].mean(1) - base) / (own - base)
    approve = np.zeros_like(Ut, bool); np.put_along_axis(approve, np.argsort(-Ut, 1)[:, :k], True, 1)
    return {g: float(sat[groups == g].mean()) for g in np.unique(groups)} | {
        "all": float(sat.mean()), "JR_true": E.justified_representation(approve, S, k),
        "min_group_has_own_topk": {g: int(approve[groups == g][:, S].any(1).mean() * 100) for g in np.unique(groups)}}


# E4 scenarios (SYNTHETIC): 'realistic' = archetype mix; 'polarised' = access/cost majority vs a
# green/heat-first minority, a stress test where the minority's top parcels differ from the majority's.
SCEN = {"realistic": (["young_worker", "family_children", "elderly"], {}),
        "polarised": (["commuter", "family_children", "heat_green_first"],
                      {"heat_green_first": [0.04, 0.08, 0.36, 0.36, 0.04, 0.08, 0.04]})}


def e4(ctx, N=36, Q=8, shares=(0.1, 0.2, 0.3), seeds=2):
    XR = short(ctx)[1]
    rows = []
    t0 = time.time()
    for sc, (gnames, extra) in SCEN.items():
      arch = ARCH | extra
      for s in shares:
        for seed in range(seeds):
            rng = np.random.default_rng(400 + seed + int(100 * s))
            grp = rng.choice(gnames, N, p=[0.8 - s, 0.2, s])  # SYNTHETIC population; gnames[2] = minority
            Wt = np.array([arch_sample(g, 1, rng, arch)[0] for g in grp])
            Wl = np.array([run_participant(XR, w, "top", Q, 15, 0, np.random.default_rng(seed * 1000 + i), rec=False)[0].mean()
                           for i, w in enumerate(Wt)])
            Ut = Wt @ XR.T
            for src, Wm in [("learned", Wl), ("oracle", Wt)]:
                sets, lab = aggregate_all(Wm @ XR.T, Wm, XR, grp, rng)
                for meth, S in sets.items():
                    f = fairness(S, Ut, grp)
                    gs = [f.get(g, np.nan) for g in gnames]
                    rows.append(dict(scenario=sc, minority_share=s, seed=seed, weights=src, method=meth, n_groups_found=len(set(lab)),
                                     sat_all=f["all"], sat_majority=gs[0], sat_family=gs[1], sat_minority=gs[2],
                                     worst_group=np.nanmin(gs), JR=f["JR_true"],
                                     pct_minority_with_own_topk=f["min_group_has_own_topk"].get(gnames[2], np.nan)))
    df = pd.DataFrame(rows)
    df.to_csv(RES / "e4_aggregation_raw.csv", index=False, float_format="%.4g")
    s = df.groupby(["scenario", "weights", "minority_share", "method"]).mean(numeric_only=True).drop(columns="seed").reset_index()
    s.to_csv(RES / "e4_aggregation_summary.csv", index=False, float_format="%.4g")
    print(f"E4 done {time.time()-t0:.0f}s"); print(s[s.weights == "learned"].round(3).to_string())
    if plt:
        fig, ax = plt.subplots(2, 2, figsize=(11, 7.5))
        for r, sc in enumerate(SCEN):
            for meth, h in s[(s.weights == "learned") & (s.scenario == sc)].groupby("method"):
                ax[r, 0].plot(h.minority_share, h.sat_minority, marker="o", label=meth)
                ax[r, 1].plot(h.minority_share, h.sat_all, marker="o", label=meth)
            ax[r, 0].set_title(f"{sc}: minority satisfaction", fontsize=9); ax[r, 1].set_title(f"{sc}: all-voter satisfaction", fontsize=9)
        for a in ax[1]: a.set_xlabel("minority share of participants")
        ax[0, 0].legend(fontsize=7); fig.suptitle("E4: aggregation of learned weights (SYNTHETIC population)", fontsize=10)
        fig.tight_layout(); fig.savefig(RES / "e4_fairness.png", dpi=130); plt.close(fig)

# ------------------------------------------------------------------ E5 Milan demo + teach-back
def e5(ctx, Q=12):
    R, XR = short(ctx)
    demo, learned = {}, {}
    for ai, (a, w) in enumerate(ARCH.items()):  # one prototypical SYNTHETIC participant per archetype
        wt = np.array(w)
        L, rows = run_participant(XR, wt, "top", Q, 15, 0, np.random.default_rng(500 + ai))
        learned[a] = L
        qs = [dict(a=label(R, i), b=label(R, j), answer="a" if y else "b") for i, j, y in L.hist]
        top = np.argsort(-(XR @ L.mean()))[:5]
        demo[a] = dict(true_w=dict(zip(E.CRIT, w)), learned_w=dict(zip(E.CRIT, L.mean().round(3))),
                       final=rows[-1], questions=qs, top5=[label(R, i) for i in top])
    # consensus across archetype posteriors: P_g(top-k) from each participant's posterior particles
    P = np.array([np.bincount(np.argsort(-L.U, 1)[:, :K].ravel(), weights=np.repeat(L.pi, K), minlength=len(XR))
                  for L in learned.values()])
    gic = np.prod(P, 0)
    cons = np.argsort(-gic)[:K]
    demo["_consensus_gic_top10"] = [dict(parcel=label(R, i), gic=float(gic[i]), **{a: float(P[j, i]) for j, a in enumerate(ARCH)}) for i in cons]
    # same list with at most one parcel per NIL (NIL criteria are ecological: parcels of one NIL tie on 4 of 7 criteria)
    seen, div = set(), []
    for i in np.lexsort((-P.mean(0), -gic)):   # GIC, ties (zeros) broken by mean P(top-k)
        if R.nil_id[i] not in seen:
            seen.add(R.nil_id[i]); div.append(dict(parcel=label(R, i), gic=float(gic[i]), mean_p=float(P[:, i].mean()), **{a: float(P[j, i]) for j, a in enumerate(ARCH)}))
        if len(div) == K: break
    demo["_consensus_gic_top10_one_per_nil"] = div
    # teach-back: minimal weight change flipping top-1 of each archetype vs the GIC consensus #1
    tb = []
    for a, L in learned.items():
        w = L.mean(); t1 = int(np.argmax(XR @ w))
        for other in dict.fromkeys([int(cons[0]), int(np.argsort(-(XR @ w))[1])]):
            if other == t1: continue
            l1, w2 = E.flip_l1(w, XR[t1], XR[other])
            fs = E.flip_single(w, XR[t1], XR[other])
            j = int(np.nanargmin(np.where(np.isnan(fs), np.inf, fs - w)))
            tb.append(dict(archetype=a, current_top=label(R, t1), challenger=label(R, other),
                           utility_gap=float(w @ (XR[t1] - XR[other])),
                           L1_change_points=round(100 * l1, 1),
                           weights_after=dict(zip(E.CRIT, np.round(w2, 3))) if w2 is not None else None,
                           easiest_single_criterion=E.CRIT[j], from_pct=round(100 * w[j], 1), to_pct=round(100 * fs[j], 1),
                           sentence=f"'{R.ref[other]}' would overtake '{R.ref[t1]}' if '{E.CRIT[j]}' rose from {100*w[j]:.1f}% to {100*fs[j]:.1f}% of your weight (others shrinking proportionally)."))
    demo["_teach_back"] = tb
    json.dump(demo, open(RES / "e5_milan_demo.json", "w"), indent=1, default=float)
    print("E5 consensus:", [d["parcel"] for d in demo["_consensus_gic_top10"][:5]])
    print("E5 consensus one per NIL:", [(d["parcel"], round(d["gic"], 4)) for d in div])
    for a in ARCH: print("  ", a, demo[a]["learned_w"], demo[a]["final"])
    for t in tb: print("  ", t["archetype"], t["L1_change_points"], t["sentence"])


if __name__ == "__main__":
    todo = sys.argv[1:] or ["e1", "e2", "e3", "e4", "e5"]
    t0 = time.time()
    ctx = build()
    print(f"pool {len(ctx[0])}, reduced {len(ctx[4])}, build {time.time()-t0:.0f}s")
    for e in todo:
        globals()[e](ctx)
    print(f"total {time.time()-t0:.0f}s")
