"""Step 7: PGT-vs-people audit (review1 §5.7). For a set G of sites built to dwellings n_s (capacity for designated
sets and null draws), compute segregation-risk and real-potential indices, and compare with R size/capacity-matched
random sets of non-designated sites (null 'size') and with sets also matched on distance-to-centre quintile
(null 'ring'). Decision rule: config.AUDIT['rule'] (pre-registered). Everything here is NIL/hex-ecological:
no household is scored."""
import numpy as np, pandas as pd
from scipy import sparse, stats
from config import *


class Auditor:
    def __init__(self, nil, site, W_si=None, cov3=None, cov1=None, hex_dem=None, hex_hh_pop=None, sigma=None):
        """nil: DataFrame (rows = NIL index 0..I-1) with hh, p_erp, poor, for_, net_m, resid, q5 (bool), kap, D (mean
        target demand). site: DataFrame with nil (row index into nil), area, cap, ring, opp, rent_g, fixed, var, hol,
        min_arch. W_si: sparse (S x I) service weights. cov3 / cov1: sparse boolean (S x H) hex within 3 km / 1 km."""
        self.N, self.S = nil.reset_index(drop=True), site.reset_index(drop=True)
        self.sigma = AUDIT["sigma"] if sigma is None else sigma
        self.W, self.cov3, self.cov1, self.hex_dem, self.hex_hh = W_si, cov3, cov1, hex_dem, hex_hh_pop
        hh, pe = self.N.hh.values, self.N.p_erp.values
        self.L0, self.O0 = hh * pe, hh * (1 - pe)
        w = hh / hh.sum()
        self.city = {c: float(np.nansum(w * self.N[c].values)) for c in ("poor", "for_", "net_m", "resid") if c in self.N}
        self.DI0, self.Iso0 = self._di(self.L0, self.O0), self._iso(self.L0, self.O0)
        self.nI = len(self.N)

    @staticmethod
    def _di(L, O): return 0.5 * np.abs(L / L.sum() - O / O.sum()).sum()

    @staticmethod
    def _iso(L, O): return float(((L / L.sum()) * (L / np.maximum(L + O, 1e-9))).sum())

    def indices(self, n):
        """n: dwellings per site (length S). Returns dict of indices."""
        n = np.asarray(n, float); tot = n.sum(); S, N = self.S, self.N
        new = np.bincount(S.nil.values, n, self.nI)
        L, O = self.L0 + self.sigma * new, self.O0 + (1 - self.sigma) * new
        nw = lambda v: float((new * v).sum() / max(tot, 1e-9))
        sw = lambda v: float((n * v).sum() / max(tot, 1e-9))
        I = dict(dDI=self._di(L, O) - self.DI0, dIso=self._iso(L, O) - self.Iso0,
                 dep_poor=nw(N.poor.values) - self.city["poor"], dep_for=nw(N.for_.values) - self.city["for_"],
                 dep_net=nw(N.net_m.values) - self.city["net_m"],
                 conc_q5=float(new[N.q5.values].sum() / max(tot, 1e-9)), n_kappa_exceed=int((new > N.kap.values + 1e-9).sum()),
                 opp=sw(S.opp.values), dwellings=float(tot))
        if "resid" in N: I["dep_resid"] = nw(N.resid.values) - self.city["resid"]
        if "q5_or" in N: I["conc_q5_or"] = float(new[N.q5_or.values].sum() / max(tot, 1e-9))   # old p_erp OR srv_erp definition
        if "rent_g" in S: I["rent_erosion"] = sw(S.rent_g.values)
        if "hol" in S: I["hol"] = sw(S.hol.values); I["min_arch"] = sw(S.min_arch.values)
        if self.W is not None:
            acc = self.W.T @ n
            served = np.minimum(N.D.values, acc).sum()
            cost = float((S.fixed.values * (n > 0)).sum() + (S["var"].values * n).sum())
            I["served"] = float(served); I["served_per_meur"] = float(served / max(cost, 1) * 1e6)
            if "D2" in N:                                   # secondary layer (D_tau), reported only
                I["served_tau"] = float(np.minimum(N.D2.values, acc).sum()); I["served_tau_per_meur"] = I["served_tau"] / max(cost, 1) * 1e6
        if self.cov3 is not None:
            on = sparse.csr_matrix((n > 0).astype(float)[None])
            h3 = np.asarray((on @ self.cov3).todense()).ravel() > 0
            h1 = np.asarray((on @ self.cov1).todense()).ravel() > 0
            I["dem_within3km"] = float(self.hex_dem[h3].sum() / self.hex_dem.sum())
            I["hh_need_cov1km"] = float(self.hex_hh[h1].sum() / max(self.hex_hh.sum(), 1))
        return I

    # ------------------------------------------------------------ nulls
    def strata(self, kind, pool):
        S = self.S
        edges = np.quantile(S.area.values[pool], np.linspace(0, 1, AUDIT["n_area_strata"] + 1)[1:-1])
        a = np.searchsorted(edges, S.area.values)
        return a if kind == "size" else a * 100 + S.ring.values

    def draw(self, G, pool, kind, R, rng, tol=None, tries=60):
        """R random index sets from `pool`, stratified like G, total capacity within +-tol of G (rejection, best of
        `tries` if never inside). Returns list of arrays and the share matched within tolerance."""
        tol = AUDIT["cap_tol"] if tol is None else tol
        st = self.strata(kind, pool); cap = self.S.cap.values
        pool_idx = np.where(pool)[0]; target = cap[G].sum()
        need = pd.Series(st[G]).value_counts()
        groups = {}
        for g, k in need.items():
            cand = pool_idx[st[pool_idx] == g]
            if len(cand) < k and kind == "ring":                     # fall back to the area stratum alone
                cand = pool_idx[(st[pool_idx] // 100) == g // 100]
            if len(cand) < k: cand = pool_idx[np.argsort(np.abs(self.S.area.values[pool_idx] - np.median(self.S.area.values[G])))[:max(3 * k, k)]]
            groups[g] = (cand, k)
        out, ok = [], 0
        for _ in range(R):
            best, bd = None, np.inf
            for _t in range(tries):
                s = np.concatenate([rng.choice(c, k, replace=len(c) < k) for c, k in groups.values()])
                d = abs(cap[s].sum() / target - 1)
                if d < bd: best, bd = s, d
                if d <= tol: break
            ok += bd <= tol; out.append(best)
        return out, ok / R

    def test(self, G, pool, kind, R=None, rng=None, keys=None, draws=None):
        R = len(draws) if draws is not None else (R or AUDIT["R"]); rng = rng or np.random.default_rng(AUDIT["seed"])
        G = np.asarray(G)
        nG = np.zeros(len(self.S)); nG[G] = self.S.cap.values[G]
        obs = self.indices(nG)
        match = 1.0
        if draws is None: draws, match = self.draw(G, pool, kind, R, rng)
        null = []
        for s in draws:
            n = np.zeros(len(self.S)); np.add.at(n, s, self.S.cap.values[s]); null.append(self.indices(n))
        null = pd.DataFrame(null)
        res = {}
        for k in (keys or obs):
            if k not in null: continue
            v = null[k].values; o = obs[k]
            sd = v.std(ddof=1)
            res[k] = dict(obs=o, mean=float(v.mean()), sd=float(sd), z=float((o - v.mean()) / sd) if sd > 0 else 0.0,
                          p_up=float((1 + (v >= o - 1e-12).sum()) / (R + 1)), p_dn=float((1 + (v <= o + 1e-12).sum()) / (R + 1)),
                          pct=float((v < o).mean() * 100), median=float(np.median(v)), p95=float(np.quantile(v, .95)))
            res[k]["p_two"] = min(1.0, 2 * min(res[k]["p_up"], res[k]["p_dn"]))
        return res, match


def block_test(A, G, pool_cap, nil_ring=None, R=4999, seed=3, keys=("dDI", "dIso", "dep_poor", "dep_resid", "conc_q5")):
    """review2 robustness (post hoc, NOT in the verdict): NIL-block permutation null. G's capacity per NIL (one block per
    NIL it touches) is re-assigned to distinct random NIL whose pool capacity can absorb the block (same centre ring if
    nil_ring is given). Effective n = number of NIL G touches, not number of sites. Returns {key: one-sided harm p}."""
    rng = np.random.default_rng(seed); S = A.S
    keys = [k for k in keys if k != "dep_resid" or "resid" in A.N]
    c = pd.Series(S.cap.values[G]).groupby(S.nil.values[G]).sum().sort_values(ascending=False)
    N = A.N
    def ind(new):                                                # same formulas as Auditor.indices, on a NIL vector
        L, O = A.L0 + A.sigma * new, A.O0 + (1 - A.sigma) * new; t = new.sum()
        I = dict(dDI=A._di(L, O) - A.DI0, dIso=A._iso(L, O) - A.Iso0, dep_poor=(new * N.poor.values).sum() / t - A.city["poor"],
                 conc_q5=new[N.q5.values].sum() / t)
        if "resid" in N: I["dep_resid"] = (new * N.resid.values).sum() / t - A.city["resid"]
        return [I[k] for k in keys]
    newG = np.bincount(c.index, c.values, A.nI); obs = np.array(ind(newG))
    sims = []
    for _ in range(R):
        used = np.zeros(A.nI, bool); new = np.zeros(A.nI)
        for j, cj in c.items():
            same = (nil_ring == nil_ring[j]) if nil_ring is not None else True
            for el in ((~used) & (pool_cap >= cj) & same, (~used) & same, ~used):
                if el.any(): break
            k = rng.choice(np.where(el)[0]); used[k] = True; new[k] = cj
        sims.append(ind(new))
    sims = np.array(sims); sgn = np.array([1 if AUDIT["bh_indices"].get(k, "+") == "+" else -1 for k in keys])
    p = (1 + ((sims - obs) * sgn >= -1e-12).sum(0)) / (R + 1)
    return {k: float(v) for k, v in zip(keys, p)}, dict(n_nil=len(c), neff=float(1 / ((c / c.sum()) ** 2).sum()))


def harm_p(r, k):
    return r[k]["p_up"] if AUDIT["bh_indices"][k] == "+" else r[k]["p_dn"]


def verdict(results, sets, family=None):
    """results[set][null] = test dict. Applies the pre-registered rule: BH over `family` (default AUDIT['sets'], the stated
    4 sets incl. RIG) x 6 indices per null, one-sided harm p; labels only for `sets`. Returns (labels, q-table)."""
    family = [g for g in (family or AUDIT["sets"]) if g in results]
    rows = []
    for null in ("size", "ring"):
        ps, keys = [], []
        for g in family:
            for k in AUDIT["bh_indices"]:
                if k in results[g][null]: ps.append(harm_p(results[g][null], k)); keys.append((g, k))
        q = stats.false_discovery_control(ps, method="bh") if ps else []
        rows += [dict(set=g, null=null, idx=k, p_harm=p, q_bh=float(qq), sig=bool(qq < AUDIT["q_fdr"])) for (g, k), p, qq in zip(keys, ps, q)]
    Q = pd.DataFrame(rows); lab = {}
    for g in sets:
        sig = lambda null, k: bool(Q[(Q.set == g) & (Q.null == null) & (Q.idx == k)].sig.any())
        risk = all(sig(n, "dDI") or sig(n, "dIso") for n in ("size", "ring"))
        pot = all(results[g][n]["served_per_meur"]["obs"] >= results[g][n]["served_per_meur"]["median"] and
                  results[g][n]["opp"]["obs"] >= results[g][n]["opp"]["median"] for n in ("size", "ring"))
        lab[g] = "both" if risk and pot else "risk" if risk else "potential" if pot else "neither"
    return lab, Q
