"""Cybernetic participation engine (Researcher B) -- library.

Criteria matrix, SMAA-2, Bayesian pairwise preference learning with active
question selection, aggregation rules, teach-back flip explanations.
All synthetic elements (archetypes, simulated respondents) live in run.py and
are labelled there. Run `python engine.py` for the self-checks.
"""
import numpy as np
import pandas as pd
from scipy.special import gammaln, expit
from scipy.optimize import linprog, milp, LinearConstraint, Bounds

CRIT = ["access", "need", "green", "heat", "capacity", "mix", "cost"]

# ---------------------------------------------------------------- criteria
def candidate_pool(parcels_csv):
    """Hard constraints (support, Habraken) -> candidate parcels. Real data, proxy flags."""
    d = pd.read_csv(parcels_csv, dtype={"ref": str})
    pgt_share = d[["pgt_rig", "pgt_dism", "pgt_tras"]].max(axis=1)
    m = ((d.kind == "land") & (d.area_m2 >= 1000) & (d.soft_site | (pgt_share > 0.3))
         & (d[["pgt_srv_verde", "pgt_agr", "pgt_pae", "dusaf_wat"]].max(axis=1) < 0.5)
         & (d.gfa_headroom_m2 > 0) & d.nil_rent.notna() & d.nil_net_m.notna() & ~d.outside_city)
    return d[m].reset_index(drop=True)


def criteria_matrix(c):
    """Raw criteria and benefit-oriented 0-1 scores (robust min-max on p2-p98 of the pool)."""
    raw = pd.DataFrame({
        "access": c.metro_km,                                   # km to metro, lower better
        "need": c.nil_rent * 60 / c.nil_net_m,                  # OMI rent of 60 m2 / net income per taxpayer, higher = more need
        "green_nil": c.nil_green, "green_km": c.green_srv_km,   # NIL green index (higher better), km to PGT green (lower better)
        "heat": c.nil_heatrisk,                                 # lower better
        "capacity": np.log10(c.gfa_headroom_m2),                # log floor-area headroom, higher better
        "mix": c.nil_poor,                                      # % taxpayers <= 15k, lower better (deconcentration)
        "cost": c.nil_price,                                    # OMI EUR/m2, lower better
    })

    def mm(v, benefit):
        lo, hi = np.nanpercentile(v, [2, 98])
        s = np.clip((v - lo) / (hi - lo), 0, 1)
        return s if benefit else 1 - s
    X = pd.DataFrame({
        "access": mm(raw.access, False), "need": mm(raw.need, True),
        "green": 0.5 * mm(raw.green_nil, True) + 0.5 * mm(raw.green_km, False),
        "heat": mm(raw.heat, False), "capacity": mm(raw.capacity, True),
        "mix": mm(raw.mix, False), "cost": mm(raw.cost, False)})[CRIT]
    return raw, X


def dominance_depth(X, chunk=400):
    """Number of alternatives strictly Pareto-dominating each row. With non-negative
    weights an alternative dominated by >= k others can never be in the top-k, so
    filtering depth < k is exact for top-k SMAA statistics."""
    X = np.asarray(X)
    out = np.empty(len(X), int)
    for s in range(0, len(X), chunk):
        A = X[s:s + chunk, None, :]
        ge = (X[None] >= A).all(-1)
        gt = (X[None] > A).any(-1)
        out[s:s + chunk] = (ge & gt).sum(1)
    return out

# ---------------------------------------------------------------- SMAA-2
def smaa(X, W, k=10, data_sd=0.0, rng=None):
    """Rank acceptability b[i, r] (r<k), central weights, top-k acceptability.
    X: (n, m) scores, W: (S, m) weight samples. data_sd adds Gaussian noise to X
    per sample (criteria uncertainty)."""
    n, m = X.shape
    rng = rng or np.random.default_rng(0)
    b = np.zeros((n, k))
    wc = np.zeros((n, m))
    for s0 in range(0, len(W), 2000):
        Ws = W[s0:s0 + 2000]
        U = Ws @ X.T
        if data_sd:
            U = np.einsum("sm,snm->sn", Ws, X[None] + rng.normal(0, data_sd, (len(Ws), n, m)))
        order = np.argsort(-U, 1)[:, :k]
        for r in range(k):
            b[:, r] += np.bincount(order[:, r], minlength=n)
        np.add.at(wc, order[:, 0], Ws)
    first = b[:, 0].copy()
    wc = np.divide(wc, first[:, None], out=np.full_like(wc, np.nan), where=first[:, None] > 0)
    b /= len(W)
    return b, wc


def confidence_factor(X, wc, data_sd, S=2000, rng=None):
    """SMAA-2 confidence factor: P(i is first | its central weights, data noise)."""
    rng = rng or np.random.default_rng(1)
    pc = np.full(len(X), np.nan)
    for i in np.where(~np.isnan(wc[:, 0]))[0]:
        Xs = X[None] + rng.normal(0, data_sd, (S,) + X.shape)
        pc[i] = ((Xs @ wc[i]).argmax(1) == i).mean()
    return pc


def dirichlet_logpdf(w, a):
    """Vectorised log Dir(w | a); w (P, m), a (P, m) or (m,)."""
    return gammaln(a.sum(-1)) - gammaln(a).sum(-1) + ((a - 1) * np.log(w)).sum(-1)

# ---------------------------------------------------------------- learning
class PrefLearner:
    """Particle posterior over one participant's weight vector w on the simplex.

    Likelihood (Bradley-Terry / logit with lapse):
        P(a > b | w) = eps + (1 - 2 eps) * sigmoid(beta * w . (x_a - x_b))
    Prior: Dirichlet(1) or a mixture (population prior). Inference: importance
    weights + resample-move (Dirichlet random-walk Metropolis-Hastings) when ESS
    drops below P/3.
    """

    def __init__(self, X, prior_sampler, prior_logpdf, P=3000, beta=15.0, eps=0.05, rng=None):
        self.X, self.beta, self.eps = np.asarray(X), beta, eps
        self.rng = rng or np.random.default_rng()
        self.prior_logpdf = prior_logpdf
        self.W = prior_sampler(P, self.rng)
        self.logw = np.zeros(P)
        self.hist = []          # (a, b, y) with y = 1 if a preferred
        self._refresh()

    def _refresh(self):
        self.U = self.W @ self.X.T
        self.top = self.U.argmax(1)

    def lik(self, U, a, b):
        return self.eps + (1 - 2 * self.eps) * expit(self.beta * (U[:, a] - U[:, b]))

    @property
    def pi(self):
        p = np.exp(self.logw - self.logw.max())
        return p / p.sum()

    def mean(self):
        return self.pi @ self.W

    def loglik_hist(self, W):
        if not self.hist:
            return np.zeros(len(W))
        h = np.array(self.hist)
        D = self.X[h[:, 0]] - self.X[h[:, 1]]
        p = self.eps + (1 - 2 * self.eps) * expit(self.beta * W @ D.T)
        return np.where(h[:, 2] == 1, np.log(p), np.log1p(-p)).sum(1)

    def update(self, a, b, y):
        self.hist.append((a, b, y))
        p = self.lik(self.U, a, b)
        self.logw += np.log(p if y else 1 - p)
        pi = self.pi
        if 1 / (pi ** 2).sum() < len(pi) / 3:
            self._resample_move(pi)

    def _resample_move(self, pi, steps=4, c=150.0):
        idx = self.rng.choice(len(pi), len(pi), p=pi)
        W = self.W[idx]
        lp = self.prior_logpdf(W) + self.loglik_hist(W)
        for _ in range(steps):
            Wn = np.clip(self.rng.gamma(c * W), 1e-9, None)   # vectorised Dirichlet(c*W) draw
            Wn /= Wn.sum(1, keepdims=True)
            lpn = self.prior_logpdf(Wn) + self.loglik_hist(Wn)
            la = lpn - lp + dirichlet_logpdf(W, c * Wn) - dirichlet_logpdf(Wn, c * W)
            acc = np.log(self.rng.random(len(W))) < la
            W[acc], lp[acc] = Wn[acc], lpn[acc]
        self.W, self.logw = W, np.zeros(len(W))
        self._refresh()

    # ---- active question selection
    def scores(self, pairs, kind):
        """Expected information gain of each candidate pair (nats).
        kind='w'   : I(answer; w)            (BALD, Houlsby et al. 2011)
        kind='top' : I(answer; argmax parcel) (decision-focused)"""
        pi = self.pi
        Pm = self.lik(self.U, pairs[:, 0], pairs[:, 1])        # (P, Q)
        pbar = pi @ Pm

        def H(p):
            p = np.clip(p, 1e-12, 1 - 1e-12)
            return -(p * np.log(p) + (1 - p) * np.log(1 - p))
        if kind == "w":
            return H(pbar) - pi @ H(Pm)
        u, t = np.unique(self.top, return_inverse=True)
        T = np.zeros((len(pi), len(u)))
        T[np.arange(len(pi)), t] = 1

        def Hc(q):  # entropy of rows of unnormalised categorical
            z = q.sum(1, keepdims=True)
            q = np.clip(q / np.maximum(z, 1e-300), 1e-300, 1)
            return -(q * np.log(q)).sum(1)
        q1 = (Pm * pi[:, None]).T @ T
        q0 = ((1 - Pm) * pi[:, None]).T @ T
        h0 = Hc((pi @ T)[None])[0]
        return h0 - (pbar * Hc(q1) + (1 - pbar) * Hc(q0))

# ---------------------------------------------------------------- aggregation
def borda(Uind):
    """Uind (N, n) utilities per voter -> Borda scores."""
    return np.argsort(np.argsort(Uind, 1), 1).sum(0)


def kemeny(Uind, cand):
    """Exact Kemeny ranking of `cand` (indices) via ILP (scipy.milp = HiGHS)."""
    n = len(cand)
    U = Uind[:, cand]
    M = (U[:, :, None] > U[:, None, :]).sum(0)      # M[a,b] = voters preferring a to b
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
    idx = {p: i for i, p in enumerate(pairs)}
    # x_ab = 1 if a above b; cost of disagreement: x_ab*M[b,a] + (1-x_ab)*M[a,b]
    cvec = np.array([M[b, a] - M[a, b] for a, b in pairs], float)
    rows, lo, hi = [], [], []
    def var(a, b):  # returns (index, sign, const): x_ab or 1 - x_ba
        return (idx[(a, b)], 1, 0) if a < b else (idx[(b, a)], -1, 1)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if len({a, b, c}) < 3 or not (a < b and a < c):
                    continue
                for (p, q, r) in [(a, b, c), (a, c, b)]:
                    row = np.zeros(len(pairs)); const = 0
                    for (s, t) in [(p, q), (q, r), (r, p)]:
                        i, sg, k0 = var(s, t); row[i] += sg; const += k0
                    rows.append(row); lo.append(-np.inf); hi.append(2 - const)   # no 3-cycle
                    rows.append(row); lo.append(1 - const); hi.append(np.inf)    # no reverse 3-cycle
    res = milp(cvec, constraints=LinearConstraint(np.array(rows), lo, hi),
               integrality=np.ones(len(pairs)), bounds=Bounds(0, 1))
    x = np.round(res.x)
    wins = np.zeros(n)
    for (a, b), v in zip(pairs, x):
        wins[a if v else b] += 1
    return np.asarray(cand)[np.argsort(-wins)]


def seq_pav(approve, k):
    """Sequential proportional approval voting. approve (N, n) bool."""
    S, sat = [], np.zeros(len(approve))
    for _ in range(k):
        gain = (approve / (sat[:, None] + 1)).sum(0)
        gain[S] = -1
        c = int(gain.argmax()); S.append(c); sat += approve[:, c]
    return S


def group_informed_consensus(Uind, labels, k):
    """Polis-style GIC: prod over opinion groups of P_g(parcel in a member's top-k),
    Laplace-smoothed (agree+1)/(n+2) as in Polis."""
    topk = np.zeros_like(Uind, bool)
    np.put_along_axis(topk, np.argsort(-Uind, 1)[:, :k], True, 1)
    g = np.unique(labels)
    P = np.array([(topk[labels == l].sum(0) + 1) / ((labels == l).sum() + 2) for l in g])
    return np.exp(np.log(P).sum(0)), P


def justified_representation(approve, S, k):
    """JR (Aziz et al. 2017): no candidate approved by >= N/k voters with no approved winner."""
    unrep = ~approve[:, S].any(1)
    return bool((approve[unrep].sum(0) < len(approve) / k).all())

# ---------------------------------------------------------------- teach-back
def flip_l1(w, xa, xb):
    """Minimal L1 change of w on the simplex so that b scores >= a. Returns (L1, w')."""
    d = xa - xb
    if w @ d <= 0:
        return 0.0, w
    m = len(w)
    # w' = w + p - q, p,q >= 0; min sum(p+q); sum(p-q)=0; (w+p-q).d <= 0; w+p-q >= 0
    c = np.ones(2 * m)
    A_eq = np.r_[np.ones(m), -np.ones(m)][None]
    A_ub = np.vstack([np.r_[d, -d][None], np.hstack([-np.eye(m), np.eye(m)])])
    b_ub = np.r_[-w @ d, w]
    r = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[0], bounds=(0, None), method="highs")
    if r.x is None:   # a Pareto-dominates b: no weight vector flips the order
        return np.inf, None
    p, q = r.x[:m], r.x[m:]
    return r.fun, w + p - q


def flip_single(w, xa, xb):
    """For each criterion j: share t in [0,1] to move toward e_j, w(t)=(1-t)w+t e_j, so b ties a.
    Returns new weight of j (np.nan if raising j cannot flip)."""
    d = xa - xb
    g = w @ d
    out = np.full(len(w), np.nan)
    if g <= 0:
        return w.copy()
    for j in range(len(w)):
        if d[j] < 0:
            t = g / (g - d[j])
            out[j] = (1 - t) * w[j] + t
    return out

# ---------------------------------------------------------------- self-checks
if __name__ == "__main__":
    rng = np.random.default_rng(0)
    X = rng.random((30, 4))
    dd = dominance_depth(X)
    W = rng.dirichlet(np.ones(4), 3000)
    b, wc = smaa(X, W, k=3)
    assert (b[dd >= 3].sum() == 0) and np.allclose(b.sum(0), 1)
    w = np.array([.4, .3, .2, .1])
    i, j = next((i, j) for i in range(30) for j in range(30) if ((X[i] - X[j]) > 0).any() and ((X[i] - X[j]) < 0).any())
    xa, xb = X[i], X[j]
    assert flip_l1(w, X[0], X[0] - 0.1)[0] == np.inf
    if w @ (xa - xb) < 0: xa, xb = xb, xa
    L, w2 = flip_l1(w, xa, xb)
    assert abs(w2.sum() - 1) < 1e-8 and w2 @ (xa - xb) <= 1e-8 and (w2 >= -1e-9).all()
    fs = flip_single(w, xa, xb)
    j = np.nanargmin(np.abs(fs - w)); t = (fs[j] - w[j]) / (1 - w[j])
    assert abs(((1 - t) * w + t * np.eye(4)[j]) @ (xa - xb)) < 1e-9
    # Kemeny on a transitive profile must return the common order
    U = np.tile(np.arange(6)[::-1], (5, 1)).astype(float)
    assert list(kemeny(U, np.arange(6))) == list(range(6))
    # learner recovers a weight vector
    wt = np.array([.6, .2, .1, .1])
    L = PrefLearner(X, lambda P, r: r.dirichlet(np.ones(4), P),
                    lambda W: dirichlet_logpdf(W, np.ones(4)), P=2000, rng=rng)
    for _ in range(40):
        pr = rng.integers(0, 30, (200, 2)); pr = pr[pr[:, 0] != pr[:, 1]]
        a, bb = pr[L.scores(pr, "w").argmax()]
        L.update(a, bb, int(rng.random() < expit(15 * wt @ (X[a] - X[bb]))))
    assert np.abs(L.mean() - wt).sum() / 2 < 0.15, L.mean()
    print("self-checks ok", L.mean().round(2))
