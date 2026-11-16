"""Potenza di C5 v7 (pre-registrazione 2.5). Simulazione; non legge dati: N_h stimati da v6 [I], da ricalcolare con N_h reali prima delle codifiche.
Un solo codificatore (caso conservativo: due codificatori perfettamente correlati). Uso: python potenza_c5.py [N_FE N_FR N_FA N_DE N_DR N_DA]"""
import sys
from math import sqrt
from statistics import NormalDist
import numpy as np

rng = np.random.default_rng(20261116)  # seme della sola simulazione
H = [("F", "E"), ("F", "R"), ("F", "A"), ("D", "E"), ("D", "R"), ("D", "A")]  # F fuori ambito (lotto_at=0), D in ambito non GFU
N = dict(zip(H, map(int, sys.argv[1:7]))) if len(sys.argv) == 7 else dict(zip(H, (173, 147, 245, 43, 20, 23)))
Nt = sum(N.values()); W = {h: N[h] / Nt for h in H}


def alloc(nf, nd_max=90):
    n = {}
    for a, nn in (("F", nf), ("D", nd_max)):
        hs = [h for h in H if h[0] == a]; tot = sum(N[h] for h in hs); nn = min(nn, tot)
        raw = {h: nn * N[h] / tot for h in hs}; fl = {h: int(raw[h]) for h in hs}
        for h in sorted(hs, key=lambda h: raw[h] - fl[h], reverse=True)[: nn - sum(fl.values())]: fl[h] += 1
        n.update(fl)
    return n


def wilson(p, n, z=1.96):
    d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; m = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - m, c + m


def newcombe_low(p1, n1, p2, n2):
    l1, _ = wilson(p1, n1); _, u2 = wilson(p2, n2)
    return p1 - p2 - sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)


def sim(q, n, qb=0.16, nb=100, R=50000):
    K = {h: round(q[h] * N[h]) for h in H}; a = b = 0
    for _ in range(R):
        p = var = 0.0
        for h in H:
            qh = rng.hypergeometric(K[h], N[h] - K[h], n[h]) / n[h]
            p += W[h] * qh; var += W[h] ** 2 * qh * (1 - qh) / n[h] * ((1 - n[h] / N[h]) if n[h] < N[h] else 1)
        a += p >= 0.70
        neff = p * (1 - p) / var if var > 0 else sum(n.values())
        b += newcombe_low(p, neff, rng.binomial(nb, qb) / nb, nb) >= 0.25
    return a / R, b / R


scen = {f"{v:.2f}": {h: v for h in H} for v in (0.60, 0.65, 0.68, 0.70, 0.72, 0.75, 0.80)}
scen["v6 [I]"] = dict(zip(H, (0.703, 0.532, 0.817, 0.64, 0.64, 0.64)))
print("N_h", N, "N", Nt)
for nf in (100, 120, 150, 200):
    n = alloc(nf); print(f"\nn_fuori={nf} n_lotti={sum(n.values())} n_h={n}")
    for k, q in scen.items():
        a, b = sim(q, n); print(f"  quota {k} (p vero {sum(W[h]*q[h] for h in H):.3f}): P(C5a passa)={a:.3f}  P(C5b passa)={b:.3f}")
for nk in (286, 336):  # kappa binario, SE asintotico approssimato con pe = 0,5
    for po in (0.80, 0.85, 0.90):
        k = (po - 0.5) / 0.5; se = sqrt(po * (1 - po) / (nk * 0.25))
        print(f"kappa: n={nk} po={po} kappa={k:.2f} se={se:.3f} P(kappa>=0,60)={1 - NormalDist(k, se).cdf(0.60):.3f}")
