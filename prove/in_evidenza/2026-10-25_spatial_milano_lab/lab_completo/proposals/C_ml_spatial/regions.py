"""3. Spatial need regions on census-2021 hex cells (r = 0.25 km):
affordability-pressure index -> LISA with conditional permutation + Benjamini-Hochberg FDR -> max-p regionalisation
(simple Duque-Anselin-Rey 2012 heuristic: randomised growth + enclave assignment + boundary-swap local search).
Labels are neutral ids (R01..). Outputs: results/hex_need.csv, regions_summary.json, regions_map.png."""
import numpy as np, pandas as pd, shapely
from collections import deque
from scipy.spatial import cKDTree
from sklearn.metrics import adjusted_rand_score
from common import *

RNG = np.random.default_rng(1)
POP_MIN = 5000      # max-p floor: residents per region (assumption; NIL mean is ~16k)
FLAT_M2 = 50        # notional flat size for the rent-to-income index (assumption)


def build_index():
    core = load("core.json"); H = np.array(core["hex"]["cells"], float)
    xy, pop, deg = H[:, :2], H[:, 2], H[:, 5]
    nil = core["nil"]; ng = [shapely.union_all([poly(r, 0.01) for r in n["rings"]]) for n in nil]
    nid = np.full(len(H), -1)
    for i, g in enumerate(ng): nid[shapely.contains_xy(g, xy[:, 0], xy[:, 1])] = i
    miss = nid < 0
    if miss.any():  # nearest NIL centroid for cells on ring edges
        cxy = np.array([[g.centroid.x, g.centroid.y] for g in ng]); nid[miss] = cKDTree(cxy).query(xy[miss])[1]
    omi = core["omi"]; og = [shapely.union_all([poly(r, 0.01) for r in o["rings"]]) for o in omi]
    rent = np.full(len(H), np.nan)
    for g, o in zip(og, omi): rent[shapely.contains_xy(g, xy[:, 0], xy[:, 1]) & np.isnan(rent)] = o["rent"]
    m = np.isnan(rent); ok = ~m
    rent[m] = rent[ok][cKDTree(xy[ok]).query(xy[m])[1]]
    # small-area income: NIL net income downscaled by the hex tertiary-education share, slope fitted across NIL
    share = deg / np.maximum(pop, 1)
    net = np.array([n["ind"].get("net_m") or np.nan for n in nil], float)
    nil_share = np.array([deg[nid == i].sum() / max(pop[nid == i].sum(), 1) for i in range(len(nil))])
    have = ~np.isnan(net) & (np.bincount(nid, pop, len(nil)) > 1000)
    b, a = np.polyfit(nil_share[have], np.log(net[have]), 1)
    r2 = np.corrcoef(nil_share[have], np.log(net[have]))[0, 1] ** 2
    # shrink tiny-population cells toward their NIL share (empirical-Bayes style, prior weight 200 residents)
    share = (deg + 200 * nil_share[nid]) / (pop + 200)
    net_nil = np.where(np.isnan(net), np.nanmedian(net), net)[nid]
    inc = net_nil * np.exp(b * (share - nil_share[nid]))
    press = rent * FLAT_M2 / inc
    df = pd.DataFrame({"x": xy[:, 0], "y": xy[:, 1], "pop": pop, "nil": [nil[i]["n"] for i in nid], "nil_idx": nid,
                       "rent_omi": rent, "deg_share": share.round(4), "net_m_est": inc.round(0), "pressure": press.round(4)})
    return df, {"slope_log_net_on_deg_share": round(float(b), 3), "r2_across_nil": round(float(r2), 3), "n_nil_fit": int(have.sum())}


def neighbours(xy):
    t = cKDTree(xy); nb = [np.array([j for j in t.query_ball_point(p, 0.45) if j != i]) for i, p in enumerate(xy)]
    # make the graph connected (needed by max-p enclave assignment): link each minor component to the main one
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    while True:
        r = np.concatenate([np.full(len(n), i) for i, n in enumerate(nb)]); c = np.concatenate(nb).astype(int)
        k, comp = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(len(xy),) * 2), directed=False)
        if k == 1: break
        main = np.bincount(comp).argmax(); tm = cKDTree(xy[comp == main]); idx_main = np.nonzero(comp == main)[0]
        for cc in set(range(k)) - {main}:
            mem = np.nonzero(comp == cc)[0]; d, j = tm.query(xy[mem]); i = mem[d.argmin()]; j = idx_main[j[d.argmin()]]
            nb[i] = np.append(nb[i], j); nb[j] = np.append(nb[j], i)
    return [n.astype(int) for n in nb]


def lisa(z, nb, perms=9999):
    z = (z - z.mean()) / z.std(); n = len(z)
    lag = np.array([z[k].mean() for k in nb]); I = z * lag
    p = np.zeros(n)
    for i in range(n):  # conditional permutation: hold z_i, redraw its |N_i| neighbours from the other cells
        k = len(nb[i]); others = np.delete(np.arange(n), i)
        sim = z[RNG.choice(others, (perms, k))].mean(1) * z[i]
        p[i] = (min((sim >= I[i]).sum(), (sim <= I[i]).sum()) + 1) / (perms + 1)
    quad = np.where(z > 0, np.where(lag > 0, "HH", "HL"), np.where(lag > 0, "LH", "LL"))
    return I, p, quad


def connected(cells, nb):
    cells = set(cells)
    if not cells: return True
    s = next(iter(cells)); seen = {s}; q = deque([s])
    while q:
        for j in nb[q.popleft()]:
            if j in cells and j not in seen: seen.add(j); q.append(j)
    return len(seen) == len(cells)


def maxp_construct(z, pop, nb):
    n = len(z); lab = np.full(n, -1); r = 0
    for s in RNG.permutation(n):
        if lab[s] != -1: continue
        reg = [s]; lab[s] = r; P = pop[s]
        while P < POP_MIN:
            front = {j for i in reg for j in nb[i] if lab[j] == -1}
            if not front: break
            mu = z[reg].mean(); j = min(front, key=lambda j: abs(z[j] - mu))
            reg.append(j); lab[j] = r; P += pop[j]
        if P < POP_MIN: lab[reg] = -2  # enclave, assigned later
        else: r += 1
    while (lab == -2).any():  # enclaves -> most similar adjacent region
        for i in np.nonzero(lab == -2)[0]:
            cand = {lab[j] for j in nb[i] if lab[j] >= 0}
            if cand:
                lab[i] = min(cand, key=lambda c: abs(z[i] - z[lab == c].mean()))
    return lab, r


def ssd(z, lab):
    return float(sum(((z[lab == c] - z[lab == c].mean()) ** 2).sum() for c in np.unique(lab)))


def local_search(z, pop, nb, lab, passes=4):
    """Move boundary cells to a neighbouring region when within-SSD drops, keeping floor and contiguity."""
    rp = pd.Series(pop).groupby(lab).sum().to_dict()
    members = {c: set(np.nonzero(lab == c)[0]) for c in np.unique(lab)}
    for _ in range(passes):
        moved = 0
        for i in RNG.permutation(len(z)):
            a = lab[i]
            if rp[a] - pop[i] < POP_MIN or len(members[a]) == 1: continue
            for b in {lab[j] for j in nb[i]} - {a}:
                A, B = list(members[a]), list(members[b])
                ma, mb = z[A].mean(), z[B].mean()
                na, nb_ = len(A), len(B)
                # exact SSD change of removing i from A and adding to B
                d = -(na / (na - 1)) * (z[i] - ma) ** 2 + (nb_ / (nb_ + 1)) * (z[i] - mb) ** 2
                if d < -1e-12 and connected(members[a] - {i}, nb):
                    members[a].discard(i); members[b].add(i); lab[i] = b
                    rp[a] -= pop[i]; rp[b] += pop[i]; moved += 1; break
        if not moved: break
    return lab


if __name__ == "__main__":
    df, fit = build_index(); log("index built", fit)
    xy = df[["x", "y"]].to_numpy(); z_raw = df.pressure.to_numpy(); pop = df["pop"].to_numpy()
    nb = neighbours(xy)
    I, p, quad = lisa(z_raw, nb)
    q_fdr = bh_fdr(p, 0.05)
    df["lisa_I"], df["lisa_p"], df["lisa_quad"] = I.round(4), p, quad
    df["sig_raw05"], df["sig_fdr05"] = p <= 0.05, q_fdr
    log("LISA sig raw", int((p <= .05).sum()), "FDR", int(q_fdr.sum()))

    z = (z_raw - z_raw.mean()) / z_raw.std()
    sols = []
    for it in range(60):
        lab, r = maxp_construct(z, pop, nb); sols.append((r, ssd(z, lab), lab.copy()))
    pmax = max(s[0] for s in sols); best = sorted([s for s in sols if s[0] == pmax], key=lambda s: s[1])
    lab = local_search(z, pop, nb, best[0][2].copy())
    assert pd.Series(pop).groupby(lab).sum().min() >= POP_MIN
    assert all(connected(set(np.nonzero(lab == c)[0]), nb) for c in np.unique(lab))
    # stability: ARI among the 10 best constructions (after the same local search)
    top = [local_search(z, pop, nb, s[2].copy(), passes=2) for s in sorted(sols, key=lambda s: (-s[0], s[1]))[:10]]
    ari = [adjusted_rand_score(top[i], top[j]) for i in range(10) for j in range(i + 1, 10)]
    ids = {c: f"R{k + 1:02d}" for k, c in enumerate(np.unique(lab))}
    df["region"] = [ids[c] for c in lab]
    sst = float(((z - z.mean()) ** 2).sum())
    nil_lab = df.nil_idx.to_numpy()
    # hidden pockets: FDR-significant HH cells whose NIL (aggregated) pressure is at or below the median NIL
    nil_press = df.groupby("nil_idx").apply(lambda g: np.average(g.pressure, weights=np.maximum(g["pop"], 1)), include_groups=False)
    hh = df[(df.lisa_quad == "HH") & df.sig_fdr05]
    hidden = hh[hh.nil_idx.map(nil_press) <= nil_press.median()]
    summ = {"n_hex": len(df), "pop_total": int(pop.sum()), "income_downscaling": fit, "flat_m2": FLAT_M2, "pop_min_region": POP_MIN,
            "pressure_quantiles": {q: round(float(np.quantile(z_raw, q)), 3) for q in (0.05, 0.25, 0.5, 0.75, 0.95)},
            "moran_I_global": round(morans_i(z_raw, nb), 3),
            "lisa": {"sig_raw_p05": int((p <= .05).sum()), "sig_fdr_q05": int(q_fdr.sum()),
                     "fdr_by_quadrant": df[df.sig_fdr05].lisa_quad.value_counts().to_dict(),
                     "fdr_HH_pop": int(hh["pop"].sum()), "fdr_HH_in_nil_at_or_below_median": int(len(hidden)),
                     "nils_with_hidden_HH": sorted(hidden.nil.unique().tolist())},
            "maxp": {"p_regions": int(len(ids)), "constructions": len(sols), "constructions_reaching_pmax": len(best),
                     "r2_maxp": round(1 - ssd(z, lab) / sst, 3), "r2_nil_partition_88": round(1 - ssd(z, nil_lab) / sst, 3),
                     "region_pop_min_median_max": [int(v) for v in np.percentile(pd.Series(pop).groupby(lab).sum(), [0, 50, 100])],
                     "ari_top10_mean": round(float(np.mean(ari)), 3), "ari_top10_min": round(float(np.min(ari)), 3),
                     "regions_crossing_nil_borders": int(sum(df[lab == c].nil_idx.nunique() > 1 for c in np.unique(lab)))}}
    df.drop(columns=["nil_idx"]).to_csv(os.path.join(RES, "hex_need.csv"), index=False)
    save_json(summ, "regions_summary.json"); log(summ["lisa"], summ["maxp"])
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 3, figsize=(16, 5.5))
        sc = ax[0].scatter(df.x, -df.y, c=df.pressure, s=9, marker="h", cmap="viridis"); fig.colorbar(sc, ax=ax[0], shrink=.7)
        ax[0].set_title("Rent-to-income index (50 m², est. net income)")
        col = {"HH": "#c0392b", "LL": "#2e86c1", "HL": "#f5b041", "LH": "#85c1e9"}
        ax[1].scatter(df.x, -df.y, c="#dddddd", s=9, marker="h")
        for qd, cc in col.items():
            m = (df.lisa_quad == qd) & df.sig_fdr05; ax[1].scatter(df.x[m], -df.y[m], c=cc, s=9, marker="h", label=f"{qd} ({m.sum()})")
        ax[1].legend(fontsize=8); ax[1].set_title("LISA, FDR q=0.05")
        perm = RNG.permutation(len(ids)); codes = np.array([perm[list(ids).index(c)] for c in lab])
        ax[2].scatter(df.x, -df.y, c=codes, s=9, marker="h", cmap="tab20"); ax[2].set_title(f"max-p regions (p={len(ids)}, pop ≥ {POP_MIN})")
        for a in ax: a.set_aspect("equal"); a.set_xticks([]); a.set_yticks([])
        fig.tight_layout(); fig.savefig(os.path.join(RES, "regions_map.png"), dpi=110)
    except ImportError:
        log("matplotlib missing: no chart")
