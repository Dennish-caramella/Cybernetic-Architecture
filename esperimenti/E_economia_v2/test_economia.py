"""Test T1–T12 (pre-registrazione v2 §4). `python test_economia.py` = dati fittizi; `--reali` = anche T1–T3 sulle uscite."""
import importlib.util, sys
import numpy as np, pandas as pd
import run as R

t = R.sample(2000, seed=1)
p = np.full(2000, 4000.0)


def bump(k, eps):
    u = dict(t); u[k] = t[k] + eps; return u


def test_T4_monotonie():
    V0, L0 = R.vra(t, p), R.lstar(t, 90.0, 60)
    assert (R.vra(t, p + 100) > V0).all()
    Lm = np.maximum(V0, 0)   # i_c: forma corretta del registro v1 (voce 9)
    assert (np.maximum(R.vra(bump("i_c", 1e-3), p), 0) <= Lm + 1e-9).all() and (R.vra(bump("i_c", 1e-3), p)[V0 > 0] < V0[V0 > 0]).all()
    for k, s, e in [("eta", +1, 1e-3), ("c_new", -1, 1.0), ("o", -1, 1.0), ("pi_R", -1, 1e-3)]:
        assert (np.sign(R.vra(bump(k, e), p) - V0) == s).all(), k
    assert (R.lstar(t, 91.0, 60) > L0).all()
    for k, e in [("c_new", 1.0), ("o", 1.0), ("i_D", 1e-4), ("i_E", 1e-4), ("q", 1e-3), ("v", 1e-3), ("delta", 1e-4)]:
        d = R.lstar(bump(k, e), 90.0, 60) - L0
        if k in ("i_D", "i_E"):   # aumentare il tasso riduce L* solo dove il VA dei NOI è positivo
            d = d[R.noi1(t, 90.0) > 0]
        assert (d < 0).all(), k


def test_T5_margine():
    assert np.allclose(R.vra(t, p), R.vra(t, p, margine="costo"), atol=1e-6)


def test_T6_identita():
    Ls = R.lstar(t, 90.0, 60)
    assert np.allclose(R.cstar(t, Ls, 60), 90.0, atol=0.01)
    La = 500.0 * np.ones(2000)
    assert np.allclose(R.cstar(t, R.lstar(t, 90.0, 60, vf="s", L_acq=La), 60, vf="s", L_acq=La), 90.0, atol=0.01)


def test_T7_stessi_costi():
    dV = R.vra(t, p) - R.vra({**t, "sigma": t["sigma"] * 0}, p)
    dL = R.lstar(t, 90.0, 60) - R.lstar({**t, "sigma": t["sigma"] * 0}, 90.0, 60)
    assert (dV < 0).all() and (dL < 0).all()


def test_T8_omogeneita():
    r = pd.Series(dict(area_m2=3000.0, volume_fonte_m3=0.0, classe="lotto edificabile"))
    r2 = r.copy(); r2.area_m2 = 6000.0
    a, b = R.lot_terms(r, 1.0), R.lot_terms(r2, 1.0)
    assert b[0] == 2 * a[0] and a[1:] == b[1:]


def test_T9_reale():
    r = R.rate(t); n = R.noi1(t, 90.0)
    assert np.allclose(R.lstar(t, 90.0, 61) - R.lstar(t, 90.0, 60), n / (1 + r) ** (61 + t["T_c"]))


def test_T10_VF_solo_acquisto():
    Lm = np.full(2000, 800.0)
    a, b = R.regimi(t, Lm, 1.0, 90.0, 60, vf="0"), R.regimi(t, Lm, 1.0, 90.0, 60, vf="e")
    for k in ["ces", "ds_a0", "ds_a05", "ds_a08"]:
        assert np.array_equal(a[k], b[k]), k
    assert not np.allclose(a["acq"], b["acq"])


def test_T11_tau_acquisto():
    Lm = np.full(2000, 800.0)
    assert np.allclose(R.regimi(t, Lm, 1.0, 90.0, 60)["acq"], (1 + t["tau"]) * Lm - R.lstar(t, 90.0, 60))


def test_T12_v1():
    sp = importlib.util.spec_from_file_location("v1", R.H.parent / "E_economia" / "run.py")
    v1 = importlib.util.module_from_spec(sp); sp.loader.exec_module(v1)
    u = {**t, "pi_new": np.zeros(2000)}
    assert np.allclose(R.price(u, 3000, 3500, 4200), v1.price(u, 3000, 3500, 4200))
    assert np.allclose(R.vra(u, R.price(u, 3000, 3500, 4200)), v1.vra(u, v1.price(u, 3000, 3500, 4200)))


def test_ann():
    assert np.isclose(R.ann(0.03, 0.0, 10), sum(1 / 1.03 ** k for k in range(1, 11)))
    assert np.isclose(R.ann(0.0, 0.0, 10), 10.0)


def test_reali():
    D = pd.read_csv(R.H / "tabelle" / "delta_L_lotti.csv.gz"); S = pd.read_csv(R.H / "tabelle" / "lotti_omi.csv")
    L = R.lotti(R.omi()[1])
    base = S[S.classe != "edificabile per destinazione, non verificato"]
    assert base.zona.notna().all() and base.p_mid.notna().all() and base.canone.notna().all()          # T1
    assert (base.zona == base.zona_centroide).mean() >= 0.95
    cap = {0.5: "cap_far05", 1.0: "cap_far1", 2.0: "cap_far2"}
    for (lid, var, far), x in D.groupby(["id", "variante", "FAR"], dropna=False):                         # T2
        r = L.loc[lid]; exp = r.cap_recupero if var == "R1" else r[cap[far]]
        assert int(x.N.iloc[0]) == int(exp), (lid, var, far)
    assert not D.gfu.any()                                                                                 # T3
    s = pd.read_csv(R.H / "tabelle" / "regione_sintesi.csv")
    assert set(s.classe) == {"lotto edificabile", "lotto da riusare"}


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_") and (k != "test_reali" or "--reali" in sys.argv)]
    for f in tests:
        f(); print("ok", f.__name__)
