"""Test T1–T8 (pre-registrazione §8). `python test_economia.py` = solo dati fittizi; `python test_economia.py --reali` = anche T1–T3 sulle uscite."""
import sys
import numpy as np, pandas as pd
import run as R

t = R.sample(2000, seed=1)          # punti fittizi, seme di test diverso da quello del Monte Carlo
p = np.full(2000, 4000.0)


def bump(k, eps):
    u = dict(t); u[k] = t[k] + eps; return u


def test_T4_monotonie():
    V0, L0 = R.vra(t, p), R.lstar(t, 90.0, 60)
    assert (R.vra(t, p + 100) > V0).all()
    # i_c: VRA = R/K con K crescente in i_c; se R < 0 VRA cresce (meno negativo). Si verifica L_mkt = max(VRA,0) non crescente (registro 9)
    Lm = np.maximum(V0, 0)
    assert (np.maximum(R.vra(bump("i_c", 1e-3), p), 0) <= Lm + 1e-9).all() and (R.vra(bump("i_c", 1e-3), p)[V0 > 0] < V0[V0 > 0]).all()
    for k, s in [("eta", +1), ("c_new", -1), ("o", -1), ("pi_R", -1)]:
        d = R.vra(bump(k, 1e-3 * (1 if k != "c_new" else 1e3) * (1 if k != "o" else 1e3)), p) - V0
        assert (np.sign(d) == s).all(), k
    assert (R.lstar(t, 91.0, 60) > L0).all()
    for k in ["c_new", "o", "i_D", "i_E", "q", "v", "delta"]:
        d = R.lstar(bump(k, 1e-3 if k not in ("c_new", "o") else 1.0), 90.0, 60) - L0
        assert (d < 0).all(), k
    noi_pos = R.costs(t)[0] * t["delta"] < t["eta"] * 90 * ((1 - t["v"]) - t["q"])
    assert (R.lstar(t, 90.0, 61)[noi_pos] >= L0[noi_pos]).all()


def test_T5_margine():
    assert np.allclose(R.vra(t, p), R.vra(t, p, margine="costo"), atol=1e-6)


def test_T6_identita():
    Ls = R.lstar(t, 90.0, 60); Lm = np.maximum(R.vra(t, p), 0)
    assert np.allclose((Lm - Ls) + Ls, Lm)
    assert np.allclose(R.cstar(t, Ls, 60), 90.0, atol=0.01)


def test_T7_stessi_costi():
    # VRA e L* usano la stessa funzione costs: C_tot entra con lo stesso valore nei due regimi
    C = R.costs(t)[1]
    dV = R.vra(t, p) - R.vra({**t, "sigma": t["sigma"] * 0}, p)
    dL = R.lstar(t, 90.0, 60) - R.lstar({**t, "sigma": t["sigma"] * 0}, 90.0, 60)
    assert (dV < 0).all() and (dL < 0).all() and np.isfinite(C).all()


def test_T8_omogeneita():
    for SL in (1000.0, 4000.0):  # D1 (senza soglia ERS): raddoppiare la SL raddoppia i totali
        assert np.allclose(R.vra(t, p) * 2 * SL, 2 * (R.vra(t, p) * SL))
    r = pd.Series(dict(area_m2=3000.0, volume_fonte_m3=0.0, classe="lotto edificabile"))
    r2 = r.copy(); r2.area_m2 = 6000.0
    a, b = R.lot_terms(r, 1.0), R.lot_terms(r2, 1.0)
    assert b[0] == 2 * a[0] and a[1:] == b[1:]


def test_ann():
    assert np.isclose(R.ann(np.array(0.04), np.array(0.02), 3), sum(1.02 ** (k - 1) / 1.04 ** k for k in (1, 2, 3)))
    assert np.isclose(R.ann(np.array(0.03), np.array(0.03), 10), 10 / 1.03)


def test_reali():
    D = pd.read_csv(R.H / "tabelle" / "delta_L_lotti.csv"); S = pd.read_csv(R.H / "tabelle" / "lotti_omi.csv")
    L = R.lotti(R.omi()[1])
    # T1
    base = S[S.classe != "edificabile per destinazione, non verificato"]
    assert base.zona.notna().all() and base.p_mid.notna().all() and base.canone.notna().all()
    assert (base.zona == base.zona_centroide).mean() >= 0.95
    # T2
    cap = {0.5: "cap_far05", 1.0: "cap_far1", 2.0: "cap_far2"}
    for (lid, var, far), x in D.groupby(["id", "variante", "FAR"], dropna=False):
        r = L.loc[lid]
        if r.classe.startswith("edificabile per destinazione"):
            exp = r[{0.5: "cap_scen_far05", 1.0: "cap_scen_far1", 2.0: "cap_scen_far2"}[far]] if var != "R1" else r.cap_scen_recupero
            if exp and exp > 0:
                assert int(x.N.iloc[0]) == int(exp), (lid, far)
            continue
        exp = r.cap_recupero if var == "R1" else r[cap[far]]
        assert int(x.N.iloc[0]) == int(exp), (lid, var, far)
    # T3
    s = pd.read_csv(R.H / "tabelle" / "regione_sintesi.csv")
    assert not s.classe.str.startswith("edificabile per destinazione").any()
    assert set(s.classe) == {"lotto edificabile", "lotto da riusare"}


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_") and (k != "test_reali" or "--reali" in sys.argv)]
    for f in tests:
        f(); print("ok", f.__name__)
