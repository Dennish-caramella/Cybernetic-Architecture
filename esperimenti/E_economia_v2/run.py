"""Base E v2 (ticket #19): come v1 (esperimenti/E_economia/run.py, SHA-256 240f328a…) con le modifiche [v2] della
pre-registrazione v2 (esecuzioni/00_preregistrazione.txt, SHA-256 01d50363…, commit 34c09dc): lato cooperativa e K1 in
termini reali, vincolo r ≥ 0,5 punti, strati di r, premio del nuovo, tre scenari di valore finale, E6 per cella, E7."""
import hashlib, json, pathlib, subprocess, sys
import numpy as np, pandas as pd

H = pathlib.Path(__file__).resolve().parent
CACHE = H.parent / "_cache" / "E_economia"          # cache v1, sola lettura [v2]
LV7 = H.parent / "L_lotti_v7" / "lotti_v7.gpkg"
SHA = {"prereg": "01d503634c586138316880f8fd38ea097a40001e0617e55dd5b2278edeebe769",
       "gpkg": "5d464a3c9b3ac195c8f6a3146cff1a5619445a71250c2a9d9f11ab53768d22ac",
       "zone_omi_2025_2.geojson": "656a1e1112ac08345bfa4c166ad27654c2721f9ee4ab2764658b0f153841edc5",
       "compr.csv": "786273d162f576cb41ac405dc51e0659afe9c3c49a2454a534dba61b5c51492b",
       "loc.csv": "588850f7745bfcdb680fe9d66007728493a8db74e52e2c43d195cc40c24c48be"}
SEED, NMC = 4519, 20_000
# [v2] cubo Θ, pre-registrazione v2 §2: (centrale, basso, alto); tassi della cooperativa reali, g tolto
P = dict(eta=(0.85, 0.70, 1.00), u_p=(np.nan, 0.0, 1.0), pi_new=(0.15, 0.0, 0.40), c_new=(2000., 1600., 2600.),
         rho=(0.90, 0.60, 1.20), d=(25., 10., 50.), sigma=(0.12, 0.08, 0.16), o=(100., 62., 132.), k=(0.075, 0.05, 0.10),
         omega=(0.8, 0.4, 1.0), pi_R=(0.15, 0.10, 0.20), m_v=(0.03, 0.02, 0.04), i_c=(0.06, 0.045, 0.075),
         lam_c=(0.6, 0.5, 0.7), T_c=(3., 2., 4.), tau=(0.09, 0.04, 0.11), y_ERS=(0.045, 0.04, 0.055),
         g_m=(0.005, 0.0, 0.01), v=(0.04, 0.02, 0.06), q=(0.20, 0.15, 0.30), delta=(0.008, 0.004, 0.015),
         D=(0.70, 0.50, 0.85), i_D=(0.022, 0.014, 0.031), i_E=(-0.005, -0.020, 0.015))
FIX = dict(h=3.0, c_base=484.78, c_ERS=90.0, y_exit=0.03, r_min=0.005, r_dev=0.15)
C0 = [60., 75., 90., 110., 130.]; TT = [30, 60, 90]; ALPHA = {"ds_a0": 0.0, "ds_a05": 0.5, "ds_a08": 0.8}; VF = ["0", "s", "e"]
E6_LISTA = ["eta", "d", "sigma", "m_v", "lam_c", "T_c", "tau", "y_ERS", "g_m", "q", "delta", "D"]   # [v2] §1.7
STRATI = {"S0": (-1, 0.0), "S1": (0.0, 0.005), "S2": (0.005, 0.01), "S3": (0.01, 1)}               # [v2] §1.3, (lo, hi]
K1 = [dict(nome="Ex Palasharp", ST=18120., E=10872., S=1812., L=7248., zona="E6", bmin=3.8e6, bmax=8.6e6),
      dict(nome="San Romanello", ST=7200., E=4320., S=0., L=2880., zona="E5", bmin=0.0, bmax=0.0),
      dict(nome="Bovisasca", ST=1838., E=1103., S=0., L=735., zona="D32", bmin=0.75e6, bmax=1.5e6)]


def central():
    return {k: np.array(v[0]) for k, v in P.items()}


def sample(n, seed=SEED):
    rng = np.random.default_rng(seed)
    return {k: rng.uniform(v[1], v[2], n) for k, v in P.items()}


def price(t, lo, mid, hi):
    u = t["u_p"]
    return (1 + t["pi_new"]) * np.where(np.isnan(u), mid, lo + np.nan_to_num(u) * (hi - lo))   # [v2] premio del nuovo


def costs(t, rec=False, dem=0.0, bon=0.0):
    c = t["c_new"] * (t["rho"] if rec else 1.0)
    O = (t["o"] * FIX["h"] + t["k"] * FIX["c_base"]) * (t["omega"] if rec else 1.0)
    return c, c * (1 + t["sigma"]) + O + t["d"] * dem + bon


def vra(t, p, s_ers=0.0, rec=False, dem=0.0, bon=0.0, margine="ricavo"):
    C = costs(t, rec, dem, bon)[1]
    gdv = t["eta"] * ((1 - s_ers) * p + s_ers * FIX["c_ERS"] * (1 - t["q"]) / t["y_ERS"])
    F = t["i_c"] * t["lam_c"] * C * t["T_c"] / 2
    K = (1 + t["tau"]) * (1 + t["i_c"]) ** t["T_c"]
    if margine == "costo":
        return (gdv / (1 + t["pi_R"] / (1 - t["pi_R"])) - C - F - t["m_v"] * gdv) / K
    return (gdv * (1 - t["m_v"] - t["pi_R"]) - C - F) / K


def rate(t):
    return t["D"] * t["i_D"] + (1 - t["D"]) * t["i_E"]          # [v2] reale


def ann(r, g, T):
    """Σ_{t=1..T} (1+g)^(t-1)/(1+r)^t."""
    r, g = np.asarray(r, float), np.asarray(g, float)
    x = (1 + g) / (1 + r); z = np.abs(r - g) < 1e-12
    return np.where(z, T / (1 + r), (1 - x ** T) / np.where(z, 1, r - g))


def noi1(t, c0, rec=False, iva=0.0):
    ch = costs(t, rec)[0]
    return t["eta"] * c0 * ((1 - t["v"]) / (1 + iva) - t["q"]) - t["delta"] * ch


def lstar(t, c0, T, rec=False, dem=0.0, bon=0.0, iva=0.0, vf="0", L_acq=0.0):
    """[v2] L* reale, g = 0. vf: '0' nessuno; 's' suolo L_acq restituito; 'e' NOI_(T+1)/y_exit (solo acquisto)."""
    C = costs(t, rec, dem, bon)[1]; r = rate(t); n = noi1(t, c0, rec, iva)
    pv = n * ann(r, 0.0, T) / (1 + r) ** t["T_c"]
    if vf == "s":
        pv = pv + L_acq / (1 + r) ** (T + t["T_c"])
    elif vf == "e":
        pv = pv + n / FIX["y_exit"] / (1 + r) ** (T + t["T_c"])
    return pv - C * (1 + r * t["T_c"] / 2)


def regimi(t, Lm, A_per_SL, c0, T, vf="0", **kw):
    """[v2] ΔL per m² SL. Acquisto paga τ (m6); VF solo in acquisto (m3)."""
    La = (1 + t["tau"]) * Lm
    Ls0 = lstar(t, c0, T, **kw)
    out = {"acq": La - lstar(t, c0, T, vf=vf, L_acq=La, **kw), "ces": -Ls0}
    for k, a in ALPHA.items():
        out[k] = a * Lm + (A_per_SL if a == 0 else 0) - Ls0
    return out


def cstar(t, L, T, vf="0", L_acq=0.0, **kw):
    b = lstar(t, 0.0, T, vf=vf, L_acq=L_acq, **kw); a = lstar(t, 1.0, T, vf=vf, L_acq=L_acq, **kw) - b
    return (L - b) / a


def k1_van(t, z, prezzi, canoni, bon="atteso", lettura="a", margine_libere=False):
    """[v2] VAN reale dell'operatore Piano Casa (§3); bonifica attesa 0,25(max-min) o peggiore 0,5(max-min); K1a/K1b."""
    lo, mid, hi = prezzi[z["zona"]]; p = price(t, lo, mid, hi); cm = canoni[z["zona"]] * 12
    ch, C = costs(t); r = rate(t)
    a30, a90 = ann(r, 0.0, 30), ann(r, 0.0, 90)
    post = 0.8 * cm * (ann(r, t["g_m"], 90) - ann(r, t["g_m"], 30))
    sup = (t["eta"] if lettura == "a" else 1.0) * z["E"]
    pv_e = (sup * (90.0 * a30 + post) * ((1 - t["v"]) - t["q"]) - z["E"] * t["delta"] * ch * a90) / (1 + r) ** t["T_c"]
    lib = z["L"] * t["eta"] * p * (1 - t["m_v"] - (t["pi_R"] if margine_libere else 0)) / (1 + r) ** t["T_c"]
    b = (0.25 if bon == "atteso" else 0.5) * (z["bmax"] - z["bmin"])
    Ctot = C * (z["E"] + z["S"] + z["L"]) + b
    return pv_e + lib - Ctot * (1 + r * t["T_c"] / 2) - z["ST"] * 1.0, Ctot


# ---------------------------------------------------------------- dati (cache v1 in sola lettura)
def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def check_inputs():
    for f in ["zone_omi_2025_2.geojson", "compr.csv", "loc.csv"]:
        assert sha(CACHE / f) == SHA[f], f
    assert sha(H / "esecuzioni" / "00_preregistrazione.txt") == SHA["prereg"]
    assert sha(LV7) == SHA["gpkg"]


def omi():
    import geopandas as gpd
    rd = lambda f: pd.read_csv(CACHE / f, sep=";", decimal=",", encoding="utf-8-sig").query("Descr_Tipologia == 'Abitazioni civili'")
    c, l = rd("compr.csv"), rd("loc.csv")
    cp = c.pivot_table(index="Zona", columns="Stato", values=["Compr_min", "Compr_max"])
    lp = l.pivot_table(index="Zona", columns="Stato", values=["Loc_min", "Loc_max"])
    z = pd.DataFrame(index=cp.index)
    z["p_mid"] = (cp["Compr_min", "OTTIMO"] + cp["Compr_max", "OTTIMO"]) / 2
    z["p_lo"] = ((cp["Compr_min", "NORMALE"] + cp["Compr_max", "NORMALE"]) / 2).fillna(cp["Compr_min", "OTTIMO"])
    z["p_hi"] = cp["Compr_max", "OTTIMO"]
    z["p_min_omi"] = cp["Compr_min"].min(axis=1); z["p_max_omi"] = cp["Compr_max"].max(axis=1)
    z["canone"] = lp["Loc_max", "NORMALE"].fillna(lp["Loc_min", "OTTIMO"])
    z["can_min_omi"] = lp["Loc_min"].min(axis=1); z["can_max_omi"] = lp["Loc_max"].max(axis=1)
    g = gpd.read_file(CACHE / "zone_omi_2025_2.geojson"); g["geometry"] = g.make_valid()
    return z, g[["Zona", "Fascia", "geometry"]]


def lotti(Z):
    import geopandas as gpd
    L = gpd.read_file(LV7, layer="lotti")
    L = L[L.classe.isin(["lotto edificabile", "lotto da riusare", "edificabile per destinazione, non verificato"])].copy()
    Zp = Z.to_crs(L.crs)
    ov = gpd.overlay(L[["id", "geometry"]], Zp, how="intersection", keep_geom_type=True); ov["a"] = ov.area
    best = ov.sort_values(["id", "a"], ascending=[True, False]).drop_duplicates("id").set_index("id")
    cen = L[["id"]].copy(); cen["geometry"] = L.representative_point()
    cz = gpd.sjoin(gpd.GeoDataFrame(cen, crs=L.crs), Zp, predicate="within").drop_duplicates("id").set_index("id")
    L = L.set_index("id"); L["zona"] = best.Zona; L["fascia"] = best.Fascia; L["zona_centroide"] = cz.Zona
    return L


def lot_terms(r, f):
    if f == "R1":
        return r.volume_fonte_m3 / 3.2, True, 0.0
    SL = f * r.area_m2
    dem = float(np.nan_to_num(r.volume_fonte_m3)) / SL if r.classe == "lotto da riusare" else 0.0
    return SL, False, dem


def varianti(r):
    v = ([("R1", "R1")] if r.classe == "lotto da riusare" and r.volume_fonte_m3 and r.volume_fonte_m3 > 0 else [])
    nome = "R2" if r.classe == "lotto da riusare" else "nuovo"
    return v + [(nome, f) for f in (0.5, 1.0, 2.0)]


def taratura(th, prezzi, canoni):
    r = rate(th); star = r >= FIX["r_min"]
    def k1(**kw):
        ok = np.ones(len(r), bool); vans = []
        for z in K1:
            v, C = k1_van(th, z, prezzi, canoni, **kw); ok &= v >= -0.05 * C; vans.append((v, C))
        return ok, vans
    ok, vans = k1()
    alt = {n: k1(**kw)[0] for n, kw in [("K1b", dict(lettura="b")), ("bonifica_peggiore", dict(bon="peggiore")),
                                         ("libere_con_margine", dict(margine_libere=True))]}
    rov = np.zeros(len(r), bool)
    for v, C in vans:
        rov |= v < 0
    res = dict(n_cubo=len(r), n_Theta_star=int(star.sum()), n_Theta_cal=int(ok.sum()), n_Theta_star_cal=int((ok & star).sum()),
               n_Theta_rov_star=int((rov & star).sum()),
               varianti_K1={k: dict(n_Theta_star_cal=int((v & star).sum())) for k, v in alt.items()},
               strati_Theta_cal={s: int((ok & (r > lo) & (r <= hi)).sum()) for s, (lo, hi) in STRATI.items()},
               K1=[dict(compendio=z["nome"], zona=z["zona"], quota_Theta_star_ok=float((v >= -0.05 * C)[star].mean()),
                        VAN_su_C_q50_Theta_star=float(np.median((v / C)[star]))) for z, (v, C) in zip(K1, vans)])
    tc = central(); res["centrale_in_K1"] = bool(all(k1_van(tc, z, prezzi, canoni)[0] >= -0.05 * k1_van(tc, z, prezzi, canoni)[1] for z in K1))
    res["E4"] = bool(res["n_Theta_star_cal"] >= 1000); res["taratura_non_informativa"] = bool(res["n_Theta_star_cal"] > 0.95 * star.sum())
    masks = {"cal": ok & star, "cal_senza_vincolo": ok, "cubo": star, "rov": rov & star}
    masks.update({s: ok & (r > lo) & (r <= hi) for s, (lo, hi) in STRATI.items()})
    return res, masks


def q(x, m):
    return float((x[m] <= 0).mean()) if m.any() else np.nan


def compute(th, masks, L, prezzi, canoni):
    w = masks["cal"]; rows = []
    for lid, r in L.iterrows():
        lo, mid, hi = prezzi[r.zona]; p = price(th, lo, mid, hi); gfu = r.classe.startswith("edificabile per destinazione")
        for var, f in varianti(r):
            SL, rec, dem = lot_terms(r, f); N = int(np.floor(0.70 * SL / 80)); s_ers = 0.4 if SL >= 10000 else 0.0
            Lm = np.maximum(vra(th, p, s_ers, rec, dem), 0); Lm1 = np.maximum(vra(th, p, 0.0, rec, dem), 0)
            for T in TT:
                cs = {v_: cstar(th, (1 + th["tau"]) * Lm, T, vf=v_, L_acq=(1 + th["tau"]) * Lm, rec=rec, dem=dem) for v_ in VF}
                cs0 = cstar(th, 0.0, T, rec=rec, dem=dem)
                for c0 in C0:
                    for vf in VF:
                        dd = regimi(th, Lm, r.area_m2 / SL, c0, T, vf=vf, rec=rec, dem=dem)
                        for g_, dl in dd.items():
                            if g_ != "acq" and vf != "0":
                                continue                                  # VF = 0 in ces e ds (m3)
                            row = dict(id=lid, classe=r.classe, gfu=gfu, zona=r.zona, fascia=r.fascia, proprieta=r.proprieta,
                                       area_m2=r.area_m2, variante=var, FAR=(np.nan if f == "R1" else f), SL=SL, N=N, T=T, c0=c0,
                                       regime=g_, VF=(vf if g_ == "acq" else "0"))
                            row.update({f"quota_{k}": q(dl, m) for k, m in masks.items()})
                            if c0 == 90.0:
                                x = dl[w] * SL / r.area_m2
                                row.update(dict(zip(["dL_q05", "dL_q50", "dL_q95"], np.quantile(x, [.05, .5, .95]))))
                                if g_ == "acq":
                                    row["Lmkt_q50_SL"] = float(np.median(Lm[w]))
                                    row.update(dict(zip(["VRA_q05", "VRA_q50", "VRA_q95"], np.quantile(vra(th, p, s_ers, rec, dem)[w] * SL / r.area_m2, [.05, .5, .95]))))
                                    row.update(dict(zip(["Lstar_q05", "Lstar_q50", "Lstar_q95"], np.quantile(lstar(th, c0, T, rec=rec, dem=dem, vf=vf, L_acq=(1 + th["tau"]) * Lm)[w] * SL / r.area_m2, [.05, .5, .95]))))
                                    row.update(dict(zip(["cstar_Lmkt_q05", "cstar_Lmkt_q50", "cstar_Lmkt_q95"], np.quantile(cs[vf][w], [.05, .5, .95]))))
                                    row.update(dict(zip(["cstar_L0_q05", "cstar_L0_q50", "cstar_L0_q95"], np.quantile(cs0[w], [.05, .5, .95]))))
                                    if vf == "0":
                                        row["dL_D1_q50"] = float(np.median(((1 + th["tau"]) * Lm1 - lstar(th, c0, T, rec=rec, dem=dem))[w] * SL / r.area_m2))
                            rows.append(row)
    return pd.DataFrame(rows)


def base_point(th, m):
    b = {k: np.array(np.median(th[k][m])) for k in P}
    return b


def tornado_cell(L, base, prezzi, cls, c0, T, regime, vf):
    """Quota di lotti il cui segno di ΔL cambia per ogni parametro agli estremi (E6, §4)."""
    if cls == "edificabile":
        X = L[L.classe == "lotto edificabile"]; terms = [lot_terms(r, 1.0) for _, r in X.iterrows()]
    else:
        X = L[(L.classe == "lotto da riusare")]
        if cls == "riuso_R1":
            X = X[X.volume_fonte_m3.fillna(0) > 0]; terms = [lot_terms(r, "R1") for _, r in X.iterrows()]
        else:
            terms = [lot_terms(r, 1.0) for _, r in X.iterrows()]
    lo = np.array([prezzi[z][0] for z in X.zona]); mid = np.array([prezzi[z][1] for z in X.zona]); hi = np.array([prezzi[z][2] for z in X.zona])
    SL = np.array([t[0] for t in terms]); dem = np.array([t[2] for t in terms]); rec = terms[0][1] if terms else False
    s = np.where(SL >= 10000, 0.4, 0.0); A = X.area_m2.values

    def dl(t):
        tt = {k: np.asarray(v) for k, v in t.items()}
        Lm = np.maximum(vra(tt, price(tt, lo, mid, hi), s, rec, dem), 0)
        return regimi(tt, Lm, A / SL, c0, T, vf=vf, rec=rec, dem=dem)[regime]
    d0 = dl(base); out = {}
    for k in P:
        a_, b_ = dict(base), dict(base); a_[k] = np.array(P[k][1]); b_[k] = np.array(P[k][2])
        out[k] = float(((dl(a_) <= 0) != (dl(b_) <= 0)).mean())
    return out, float((d0 <= 0).mean()), d0 * SL / A


def prcc(X, y):
    """Correlazione di rango parziale (solo numpy)."""
    R = np.column_stack([np.argsort(np.argsort(c)) for c in X.T]).astype(float); ry = np.argsort(np.argsort(y)).astype(float)
    out = []
    for j in range(R.shape[1]):
        Z = np.column_stack([np.ones(len(ry)), np.delete(R, j, 1)])
        ex = R[:, j] - Z @ np.linalg.lstsq(Z, R[:, j], rcond=None)[0]; ey = ry - Z @ np.linalg.lstsq(Z, ry, rcond=None)[0]
        out.append(float(np.corrcoef(ex, ey)[0, 1]))
    return out


def analisi(th, masks, L, prezzi, canoni, D):
    w = masks["cal"]; base = base_point(th, w); res = {}
    # ---- E6 per cella
    cells = []
    for cls in ["edificabile", "riuso_R1", "riuso_R2"]:
        for T in TT:
            for c0 in C0:
                for regime, vf in [("acq", "0"), ("acq", "s"), ("ces", "0")]:
                    fl, regge, _ = tornado_cell(L, base, prezzi, cls, c0, T, regime, vf)
                    mx = max((fl[k], k) for k in E6_LISTA)
                    cells.append(dict(classe=cls, T=T, c0=c0, regime=regime, VF=vf, quota_lotti_regge_base=regge,
                                      max_E6=mx[0], param_max_E6=(mx[1] if mx[0] > 0 else ""), robusta=mx[0] <= 0.5,
                                      **{f"flip_{k}": v for k, v in fl.items()}))
    E6 = pd.DataFrame(cells); res["E6_celle_robuste"] = int(E6.robusta.sum()); res["E6_celle"] = len(E6)
    # ---- tornado sull'insieme e sui lotti rappresentativi (c0 = 90, T = 60, acquisto VF0)
    E = L[L.classe == "lotto edificabile"].copy(); E["gr"] = E.fascia.map({"B": "B", "C": "C+D", "D": "C+D", "E": "E"})
    rep = {gr: sorted(x.index[(x.area_m2 - x.area_m2.median()).abs() == (x.area_m2 - x.area_m2.median()).abs().min()])[0] for gr, x in E.groupby("gr")}
    res["lotti_rappresentativi"] = rep
    _, _, d0 = tornado_cell(L, base, prezzi, "edificabile", 90.0, 60, "acq", "0")
    idx = {lid: i for i, lid in enumerate(E.index)}; tor = []
    for k in list(P):
        for lab, val in [("basso", P[k][1]), ("alto", P[k][2])]:
            b = dict(base); b[k] = np.array(val)
            tt = {kk: np.asarray(vv) for kk, vv in b.items()}
            lo = np.array([prezzi[z][0] for z in E.zona]); mid = np.array([prezzi[z][1] for z in E.zona]); hi = np.array([prezzi[z][2] for z in E.zona])
            SL = E.area_m2.values * 1.0; s = np.where(SL >= 10000, 0.4, 0.0)
            dl = regimi(tt, np.maximum(vra(tt, price(tt, lo, mid, hi), s), 0), 1.0, 90.0, 60)["acq"]
            row = dict(parametro=k, estremo=lab, valore=val, insieme_mediana=float(np.median(dl)), insieme_base=float(np.median(d0)))
            row.update({f"lotto_{gr}_{lid}": float(dl[idx[lid]]) for gr, lid in rep.items()})
            tor.append(row)
    # ---- PRCC sui tre lotti rappresentativi (Θ*_cal, c0 = 90, T = 60)
    keys = [k for k in P if k != "u_p"] + ["u_p"]; X = np.column_stack([th[k][w] for k in keys]); pr = []
    for gr, lid in rep.items():
        r = L.loc[lid]; lo, mid, hi = prezzi[r.zona]; t = {k: v[w] for k, v in th.items()}
        Lm = np.maximum(vra(t, price(t, lo, mid, hi), 0.4 if r.area_m2 >= 1e4 else 0.0), 0)
        for g_ in ["acq", "ces"]:
            y = regimi(t, Lm, 1.0, 90.0, 60)[g_]
            pr.append(dict(lotto=lid, gruppo=gr, regime=g_, **dict(zip(keys, prcc(X, y)))))
    # ---- E7
    A = D[(D.classe == "lotto edificabile") & (D.regime == "acq") & (D.VF == "0") & (D.c0 == 90)]
    cellE7 = A.groupby(["fascia", "FAR", "T"]).Lmkt_q50_SL.median().reset_index()
    cellE7["non_informativo"] = cellE7.Lmkt_q50_SL <= 0
    vra_de = float(A[(A.FAR == 1.0) & A.fascia.isin(["D", "E"]) & (A["T"] == 60)].VRA_q50.median())  # €/m² area = €/m² SL a FAR 1
    res["E7"] = dict(VRA_mediano_DE_FAR1_euro_m2_SL=vra_de, rapporto_asta_678=vra_de / 678,
                     DE_tutte_non_informative=bool(vra_de / 678 < 0.5),
                     celle_DE=int(cellE7.fascia.isin(["D", "E"]).sum()),
                     celle_DE_non_informative=int(((cellE7.non_informativo) | (vra_de / 678 < 0.5))[cellE7.fascia.isin(["D", "E"])].sum()))
    # ---- bonifica 200/500 €/m² area, edificabili FAR 1, c0 = 90
    bon = []
    for b in (0, 200, 500):
        for T in (60, 90):
            qa, qc = [], []
            for lid, r in E.iterrows():
                lo, mid, hi = prezzi[r.zona]; SL = r.area_m2; bb = b * r.area_m2 / SL
                Lm = np.maximum(vra(th, price(th, lo, mid, hi), 0.4 if SL >= 1e4 else 0.0, bon=bb), 0)
                dd = regimi(th, Lm, 1.0, 90.0, T, bon=bb); qa.append(q(dd["acq"], w)); qc.append(q(dd["ces"], w))
            bon.append(dict(bonifica_euro_m2=b, T=T, quota_acq_media=float(np.mean(qa)), quota_ces_media=float(np.mean(qc))))
    # ---- DCF del developer al punto base (verifica)
    tb = {k: np.asarray(v) for k, v in base.items()}; Tc = int(round(float(tb["T_c"]))); dcf = []
    for lid, r in E.iterrows():
        lo, mid, hi = prezzi[r.zona]; s = 0.4 if r.area_m2 >= 1e4 else 0.0
        gdv = float(tb["eta"] * ((1 - s) * price(tb, lo, mid, hi) + s * FIX["c_ERS"] * (1 - tb["q"]) / tb["y_ERS"]))
        C = float(costs(tb)[1])
        pv = gdv * (1 - tb["m_v"]) / (1 + FIX["r_dev"]) ** Tc - sum(C / Tc / (1 + FIX["r_dev"]) ** t for t in range(1, Tc + 1))
        dcf.append(dict(id=lid, fascia=r.fascia, VRA_statico=float(vra(tb, price(tb, lo, mid, hi), s)), VRA_DCF=float(pv / (1 + tb["tau"]))))
    # ---- recupero per classi di ρ (c0 = 90, T = 60, cessione)
    Rr = L[(L.classe == "lotto da riusare") & (L.volume_fonte_m3.fillna(0) > 0)]
    rho_cl = {"<0,8": th["rho"] < 0.8, "0,8-1,0": (th["rho"] >= 0.8) & (th["rho"] <= 1.0), ">1,0": th["rho"] > 1.0}
    Ls = lstar(th, 90.0, 60, rec=True)
    res["recupero_per_rho"] = {k: q(-Ls, w & m) for k, m in rho_cl.items()}
    # ---- varianti al punto base: IVA, η = 0,70 (informativa)
    var = {}
    for nome, kw, et in [("base", {}, None), ("IVA 10%", dict(iva=0.10), None), ("eta 0,70", {}, 0.70)]:
        b = dict(tb)
        if et:
            b["eta"] = np.array(et)
        var[nome] = dict(cstar_L0_T60=float(cstar(b, 0.0, 60, **kw)), cstar_L0_T90=float(cstar(b, 0.0, 90, **kw)))
    res["varianti_punto_base"] = var
    res["punto_base"] = {k: float(v) for k, v in base.items()}
    return res, E6, pd.DataFrame(tor), pd.DataFrame(pr), pd.DataFrame(bon), pd.DataFrame(dcf)


def sintesi(D):
    B = D[~D.gfu].copy(); B["regge"] = B.quota_cal >= 0.5
    g = B.groupby(["classe", "variante", "FAR", "T", "c0", "regime", "VF", "fascia"], dropna=False).agg(
        lotti=("id", "size"), lotti_regge=("regge", "sum"), alloggi=("N", "sum"),
        **{f"{c}_media": (c, "mean") for c in B.columns if c.startswith("quota_")}, dL_q50_mediana=("dL_q50", "median")).reset_index()
    g.loc[g.regime.isin(["ces", "ds_a0"]), "lotti_regge"] = np.nan        # [v2] C4: conteggi degeneri soppressi
    g.insert(0, "avviso", np.where(g.regime.isin(["ces", "ds_a0", "ds_a05", "ds_a08"]),
                                   "lato cooperativa uguale in tutte le zone per m2 di SL: le differenze tra fasce non sono geografia", ""))
    p = B[B.classe == "lotto edificabile"].groupby(["proprieta", "FAR", "T", "c0", "regime", "VF"]).agg(
        lotti=("id", "size"), quota_cal_media=("quota_cal", "mean"), dL_q50_mediana=("dL_q50", "median")).reset_index()
    return g, p


TAB = ["delta_L_lotti.csv.gz", "regione_sintesi.csv", "sintesi_proprieta.csv", "E6_celle.csv", "tornado.csv", "prcc.csv",
       "bonifica.csv", "dcf_developer.csv", "lotti_omi.csv", "gfu_scenario.csv"]


def run(outdir):
    check_inputs()
    zt, Z = omi(); L = lotti(Z)
    prezzi = {z: (zt.p_lo[z], zt.p_mid[z], zt.p_hi[z]) for z in zt.index}; canoni = zt.canone.to_dict()
    th = sample(NMC); res, masks = taratura(th, prezzi, canoni)
    if not res["E4"]:
        return res, None
    D = compute(th, masks, L, prezzi, canoni)
    a, E6, tor, pr, bon, dcf = analisi(th, masks, L, prezzi, canoni, D)
    res.update(a); g, p = sintesi(D)
    S = pd.DataFrame([dict(id=lid, zona=r.zona, zona_centroide=r.zona_centroide, fascia=r.fascia, classe=r.classe,
                           p_lo=prezzi[r.zona][0], p_mid=prezzi[r.zona][1], p_hi=prezzi[r.zona][2], canone=canoni[r.zona]) for lid, r in L.iterrows()])
    res["T1"] = dict(assegnati=int(S.zona.notna().sum()), totale=len(S), quota_centroide_uguale=float((S.zona == S.zona_centroide).mean()))
    res["E3_integrita_tautologica"] = bool(all((zt.p_min_omi[z] <= prezzi[z][0]) and (prezzi[z][2] <= zt.p_max_omi[z]) and
                                               (zt.can_min_omi[z] <= canoni[z] <= zt.can_max_omi[z]) for z in S.zona.unique()))
    outdir.mkdir(parents=True, exist_ok=True)
    rnd = lambda x: x.round({c: (0 if c.startswith(("dL", "VRA", "Lstar", "Lmkt", "SL", "insieme", "lotto_")) else 4) for c in x.columns if x[c].dtype.kind == "f"})
    Dm = D.sort_values(["id", "variante", "FAR", "T", "c0", "regime", "VF"], na_position="first")
    for name, df in zip(TAB, [Dm[~Dm.gfu], g, p, E6, tor, pr, bon, dcf, S, Dm[Dm.gfu & (Dm.c0 == 90)]]):
        rnd(df).to_csv(outdir / name, index=False, compression={"method": "gzip", "mtime": 0} if name.endswith(".gz") else None)  # [v2] < 20 MB
    return res, content_hash(outdir)


def content_hash(d):
    h = hashlib.sha256()
    for f in TAB:
        h.update((d / f).read_bytes())
    return h.hexdigest()


def figure(outdir, res):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    E6 = pd.read_csv(outdir / "E6_celle.csv")
    fig, ax = plt.subplots(3, 3, figsize=(13, 10))
    for i, cls in enumerate(["edificabile", "riuso_R1", "riuso_R2"]):
        for j, (rg, vf) in enumerate([("acq", "0"), ("acq", "s"), ("ces", "0")]):
            m = E6[(E6.classe == cls) & (E6.regime == rg) & (E6.VF == vf)].pivot(index="T", columns="c0", values="max_E6")
            im = ax[i, j].imshow(m.values, vmin=0, vmax=1, cmap="RdYlGn_r")
            ax[i, j].set(xticks=range(len(m.columns)), xticklabels=[int(c) for c in m.columns], yticks=range(len(m.index)),
                         yticklabels=m.index, title=f"{cls}, {rg} VF{vf}: max cambio di segno E6", xlabel="c0", ylabel="T")
            for (a, b), v in np.ndenumerate(m.values):
                ax[i, j].text(b, a, f"{v:.2f}", ha="center", va="center", fontsize=8)
    fig.tight_layout(); (H / "fig").mkdir(exist_ok=True); fig.savefig(H / "fig" / "E6_celle.png", dpi=100); plt.close(fig)


if __name__ == "__main__":
    res, h1 = run(H / "tabelle")
    if h1 is None:
        json.dump(res, open(H / "esito_criteri.json", "w"), indent=1, ensure_ascii=False); sys.exit("E4 fallisce: arresto")
    _, h2 = run(H.parent / "_cache" / "E_economia_v2" / "ripetizione")   # [v2] E1 in processo (m1), copia fuori da git
    res["E1"] = dict(hash_1=h1, hash_2=h2, passa=h1 == h2)
    t = subprocess.run([sys.executable, str(H / "test_economia.py"), "--reali"], capture_output=True, text=True, cwd=H)
    res["E2"] = dict(passa=t.returncode == 0, uscita=t.stdout.strip().splitlines()[-14:], errore=t.stderr.strip()[-500:])
    res["E5"] = "non applicabile: nessun caso osservato utilizzabile; errore di taratura non misurato"
    res["E6_formula"] = "cella non robusta se un parametro di E6_LISTA cambia il segno di ΔL per > 50% dei lotti"
    json.dump(res, open(H / "esito_criteri.json", "w"), indent=1, default=float, ensure_ascii=False)
    figure(H / "tabelle", res)
    print("hash_contenuto", h1, "E1", h1 == h2, "E2", res["E2"]["passa"])
