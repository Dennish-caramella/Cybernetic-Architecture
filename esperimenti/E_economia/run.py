"""Base E v1 (ticket #19): valore residuo del developer, prezzo del suolo sostenibile della cooperativa (canone a costo),
gap fondiario ΔL per lotto della Base L v7; taratura K1 (DG 365/2026), Monte Carlo, tornado, mappe 2D.
Pre-registrazione: esecuzioni/00_preregistrazione.txt (SHA-256 ce059fd6…, commit b3b0df6). Tutto per m² di SL, poi × SL."""
import hashlib, json, pathlib, sys
import numpy as np, pandas as pd

H = pathlib.Path(__file__).resolve().parent
CACHE = H.parent / "_cache" / "E_economia"
LV7 = H.parent / "L_lotti_v7" / "lotti_v7.gpkg"
SHA = {"prereg": "ce059fd669941b4aa6a5505c2b30886391519b3cc87d934098d0a2144455c065",
       "gpkg": "5d464a3c9b3ac195c8f6a3146cff1a5619445a71250c2a9d9f11ab53768d22ac",
       "zone_omi_2025_2.geojson": "656a1e1112ac08345bfa4c166ad27654c2721f9ee4ab2764658b0f153841edc5",
       "compr.csv": "786273d162f576cb41ac405dc51e0659afe9c3c49a2454a534dba61b5c51492b",
       "loc.csv": "588850f7745bfcdb680fe9d66007728493a8db74e52e2c43d195cc40c24c48be"}
URL = {"zone_omi_2025_2.geojson": "https://dati.comune.milano.it/dataset/02d8344e-9d79-4048-99bc-a5fbbd68e846/resource/ad93f018-fa80-4b6f-844f-e07936db1b94/download/zone_omi_2025_2.geojson",
       "compr.csv": "https://dati.comune.milano.it/dataset/b4ff0e85-9137-413c-9a70-0a857d08a2aa/resource/a2ffc245-c05b-4867-97ef-1a527219d71e/download/quotazioni_omi_compravendita_2025_2.csv",
       "loc.csv": "https://dati.comune.milano.it/dataset/cac75735-6fee-4e46-813f-dc1a43c02b8e/resource/2b37b0fc-e7b5-4ba2-bd8b-073c987f19bf/download/quotazioni_omi_locazione_2025_2.csv"}
SEED, NMC = 4519, 20_000
# parametri del cubo Θ: (centrale, basso, alto) — pre-registrazione §5
P = dict(eta=(0.85, 0.75, 0.95), u_p=(np.nan, 0.0, 1.0), c_new=(2000., 1600., 2600.), rho=(0.80, 0.55, 1.00),
         d=(25., 10., 50.), sigma=(0.12, 0.08, 0.16), o=(100., 62., 132.), k=(0.075, 0.05, 0.10), omega=(0.8, 0.4, 1.0),
         pi_R=(0.15, 0.10, 0.20), m_v=(0.03, 0.02, 0.04), i_c=(0.06, 0.045, 0.075), lam_c=(0.6, 0.5, 0.7),
         T_c=(3., 2., 4.), tau=(0.09, 0.04, 0.11), y_ERS=(0.045, 0.04, 0.055), g=(0.02, 0.01, 0.03),
         v=(0.04, 0.02, 0.06), q=(0.20, 0.15, 0.30), delta=(0.008, 0.004, 0.015), D=(0.70, 0.50, 0.85),
         i_D=(0.04, 0.025, 0.055), i_E=(0.015, 0.0, 0.035))
FIX = dict(h=3.0, c_base=484.78, c_ERS=90.0)
C0 = [60., 75., 90., 110., 130.]; TT = [30, 60, 90]; ALPHA = {"ds_a0": 0.0, "ds_a05": 0.5, "ds_a08": 0.8}
SENZA_FONTE = ["eta", "rho", "d", "sigma", "m_v", "lam_c", "T_c", "tau", "y_ERS", "g", "v", "q", "delta", "D"]  # registro 8e
# K1, DG 365/2026 [V F1]: ST, SL ERSC, SAP, libere; zona OMI (registro 6); bonifica a carico operatore (registro 8a)
K1 = [dict(nome="Ex Palasharp", ST=18120., E=10872., S=1812., L=7248., zona="E6", bon=0.5 * (8.6e6 - 3.8e6)),
      dict(nome="San Romanello", ST=7200., E=4320., S=0., L=2880., zona="E5", bon=0.0),
      dict(nome="Bovisasca", ST=1838., E=1103., S=0., L=735., zona="D32", bon=0.5 * (1.5e6 - 0.75e6))]


def central():
    return {k: np.array(v[0]) for k, v in P.items()}


def sample(n, seed=SEED):
    rng = np.random.default_rng(seed)
    return {k: rng.uniform(v[1], v[2], n) for k, v in P.items()}


def price(t, lo, mid, hi):
    u = t["u_p"]
    return np.where(np.isnan(u), mid, lo + np.nan_to_num(u) * (hi - lo))


def costs(t, rec=False, dem=0.0, bon=0.0):
    """(costo di costruzione, C_tot) per m² SL; dem = volume_fonte/SL (m³ per m² SL), bon = € per m² SL. Stessi nei due regimi."""
    c = t["c_new"] * (t["rho"] if rec else 1.0)
    O = (t["o"] * FIX["h"] + t["k"] * FIX["c_base"]) * (t["omega"] if rec else 1.0)
    return c, c * (1 + t["sigma"]) + O + t["d"] * dem + bon


def vra(t, p, s_ers=0.0, rec=False, dem=0.0, bon=0.0, margine="ricavo"):
    """Valore residuo del suolo per m² SL (RICS statico). margine='costo' usa π_C = π_R/(1-π_R) su tutti i costi (test T5)."""
    C = costs(t, rec, dem, bon)[1]
    gdv = t["eta"] * ((1 - s_ers) * p + s_ers * FIX["c_ERS"] * (1 - t["q"]) / t["y_ERS"])
    F = t["i_c"] * t["lam_c"] * C * t["T_c"] / 2
    K = (1 + t["tau"]) * (1 + t["i_c"]) ** t["T_c"]
    if margine == "costo":
        return (gdv / (1 + t["pi_R"] / (1 - t["pi_R"])) - C - F - t["m_v"] * gdv) / K
    return (gdv * (1 - t["m_v"] - t["pi_R"]) - C - F) / K


def rate(t):
    return t["D"] * t["i_D"] + (1 - t["D"]) * t["i_E"]


def ann(r, g, T):
    """Σ_{t=1..T} (1+g)^(t-1)/(1+r)^t."""
    x = (1 + g) / (1 + r)
    return np.where(np.abs(r - g) < 1e-12, T / (1 + r), (1 - x ** T) / np.where(np.abs(r - g) < 1e-12, 1, r - g))


def lstar(t, c0, T, rec=False, dem=0.0, bon=0.0, iva=0.0, y_exit=None):
    """Prezzo del suolo sostenibile per la cooperativa per m² SL (DCF del canone a costo, §4.3)."""
    ch, C = costs(t, rec, dem, bon)
    r, g = rate(t), t["g"]
    noi1 = t["eta"] * c0 * ((1 - t["v"]) / (1 + iva) - t["q"]) - t["delta"] * ch
    pv = noi1 * ann(r, g, T) / (1 + r) ** t["T_c"]
    if y_exit:  # variante VF = NOI_(T+1)/y_exit in acquisto
        pv = pv + noi1 * (1 + g) ** T / y_exit / (1 + r) ** (T + t["T_c"])
    return pv - C * (1 + r * t["T_c"] / 2)


def cstar(t, L, T, **kw):
    """Canone di pareggio: L* è lineare in c0 → forma chiusa."""
    b = lstar(t, 0.0, T, **kw); a = lstar(t, 1.0, T, **kw) - b
    return (L - b) / a


def k1_van(t, z, prezzi, canoni):
    """VAN dell'operatore Piano Casa per un compendio (§6.1, registro 8a). Restituisce (VAN, C_tot)."""
    lo, mid, hi = prezzi[z["zona"]]; p = price(t, lo, mid, hi); cm = canoni[z["zona"]] * 12
    ch, C = costs(t)
    r, g = rate(t), t["g"]
    a30, a90 = ann(r, g, 30), ann(r, g, 90)
    rent = 90.0 * a30 + 0.8 * cm * (a90 - a30)
    pv_e = z["E"] * (t["eta"] * rent * ((1 - t["v"]) - t["q"]) - t["delta"] * ch * a90) / (1 + r) ** t["T_c"]
    lib = z["L"] * t["eta"] * p * (1 - t["m_v"]) / (1 + r) ** t["T_c"]
    Ctot = C * (z["E"] + z["S"] + z["L"]) + z["bon"]
    return pv_e + lib - Ctot * (1 + r * t["T_c"] / 2) - z["ST"] * 1.0, Ctot


# ---------------------------------------------------------------- dati
def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def fetch():
    import urllib.request
    CACHE.mkdir(parents=True, exist_ok=True)
    for f, u in URL.items():
        if not (CACHE / f).exists():
            urllib.request.urlretrieve(u, CACHE / f)
        assert sha(CACHE / f) == SHA[f], f"hash diverso: {f}"


def omi():
    import geopandas as gpd
    rd = lambda f: pd.read_csv(CACHE / f, sep=";", decimal=",", encoding="utf-8-sig").query("Descr_Tipologia == 'Abitazioni civili'")
    c, l = rd("compr.csv"), rd("loc.csv")
    cp = c.pivot_table(index="Zona", columns="Stato", values=["Compr_min", "Compr_max"])
    lp = l.pivot_table(index="Zona", columns="Stato", values=["Loc_min", "Loc_max"])
    z = pd.DataFrame(index=cp.index)
    z["p_mid"] = (cp["Compr_min", "OTTIMO"] + cp["Compr_max", "OTTIMO"]) / 2
    z["p_lo"] = ((cp["Compr_min", "NORMALE"] + cp["Compr_max", "NORMALE"]) / 2).fillna(cp["Compr_min", "OTTIMO"])  # registro 4
    z["p_hi"] = cp["Compr_max", "OTTIMO"]
    z["p_min_omi"] = cp["Compr_min"].min(axis=1); z["p_max_omi"] = cp["Compr_max"].max(axis=1)
    z["canone"] = lp["Loc_max", "NORMALE"].fillna(lp["Loc_min", "OTTIMO"])
    z["can_min_omi"] = lp["Loc_min"].min(axis=1); z["can_max_omi"] = lp["Loc_max"].max(axis=1)
    g = gpd.read_file(CACHE / "zone_omi_2025_2.geojson"); g["geometry"] = g.make_valid()  # registro 3
    return z, g[["Zona", "Fascia", "geometry"]]


def lotti(Z):
    import geopandas as gpd
    L = gpd.read_file(LV7, layer="lotti")
    L = L[L.classe.isin(["lotto edificabile", "lotto da riusare", "edificabile per destinazione, non verificato"])].copy()
    Zp = Z.to_crs(L.crs)
    ov = gpd.overlay(L[["id", "geometry"]], Zp, how="intersection", keep_geom_type=True)
    ov["a"] = ov.area
    best = ov.sort_values(["id", "a"], ascending=[True, False]).drop_duplicates("id").set_index("id")
    cen = L[["id"]].copy(); cen["geometry"] = L.representative_point()
    cz = gpd.sjoin(gpd.GeoDataFrame(cen, crs=L.crs), Zp, predicate="within").drop_duplicates("id").set_index("id")
    L = L.set_index("id")
    L["zona"] = best.Zona; L["fascia"] = best.Fascia; L["zona_centroide"] = cz.Zona
    return L


# ---------------------------------------------------------------- calcolo
def lot_terms(r, f):
    """SL, rec, dem per un lotto e una variante: f = FAR (R2/edificabile) o 'R1' (recupero)."""
    if f == "R1":
        return r.volume_fonte_m3 / 3.2, True, 0.0
    SL = f * r.area_m2
    dem = float(np.nan_to_num(r.volume_fonte_m3)) / SL if r.classe == "lotto da riusare" else 0.0
    return SL, False, dem


def run(seed=SEED, nmc=NMC, out=True, eta_fisso=None):
    fetch()
    assert sha(H / "esecuzioni" / "00_preregistrazione.txt") == SHA["prereg"]
    assert sha(LV7) == SHA["gpkg"]
    zt, Z = omi(); L = lotti(Z)
    prezzi = {z: (zt.p_lo[z], zt.p_mid[z], zt.p_hi[z]) for z in zt.index}; canoni = zt.canone.to_dict()
    th = sample(nmc, seed)
    if eta_fisso is not None:
        th["eta"] = np.full(nmc, eta_fisso)
    tc = central()
    res = {}
    # ---- taratura K1
    ok = np.ones(nmc, bool); k1rows = []
    for z in K1:
        van, Ct = k1_van(th, z, prezzi, canoni); vc, Cc = k1_van(tc, z, prezzi, canoni)
        cond = van >= -0.05 * Ct; ok &= cond
        k1rows.append(dict(compendio=z["nome"], zona=z["zona"], VAN_centrale=float(vc), Ctot_centrale=float(Cc),
                           VAN_su_Ctot_centrale=float(vc / Cc), quota_cubo_ok=float(cond.mean()),
                           VAN_q05=float(np.quantile(van, .05)), VAN_q50=float(np.median(van)), VAN_q95=float(np.quantile(van, .95))))
    ncal = int(ok.sum()); res["K1"] = k1rows; res["n_Theta_cal"] = ncal; res["quota_Theta_cal"] = ncal / nmc
    cen_ok = all(k1_van(tc, z, prezzi, canoni)[0] >= -0.05 * k1_van(tc, z, prezzi, canoni)[1] for z in K1)
    res["centrale_in_Theta_cal"] = bool(cen_ok)
    ks = {}
    for k in P:
        if ncal == 0:
            break
        x = np.sort((th[k][ok] - P[k][1]) / (P[k][2] - P[k][1]))
        ks[k] = float(np.max(np.abs(np.arange(1, len(x) + 1) / len(x) - x)))
    res["KS_marginali"] = ks
    res["E4"] = bool(ncal >= 1000)
    res["taratura_non_informativa"] = bool(ncal > 19000)
    base = tc if cen_ok or ncal == 0 else {k: np.array(np.median(th[k][ok])) for k in P}  # registro 8e
    if not cen_ok and ncal:
        base["u_p"] = np.array(np.median(th["u_p"][ok]))
    res["punto_base_tornado"] = "centrale" if cen_ok else "mediana di Theta_cal"
    w = ok if ncal else np.ones(nmc, bool)
    # ---- per lotto
    rows, stats = [], []
    for lid, r in L.iterrows():
        lo, mid, hi = prezzi[r.zona]; p = price(th, lo, mid, hi)
        gfu = r.classe.startswith("edificabile per destinazione")
        varianti = ["R1"] + [0.5, 1.0, 2.0] if r.classe == "lotto da riusare" else [0.5, 1.0, 2.0]
        for f in varianti:
            if f == "R1" and not (r.volume_fonte_m3 and r.volume_fonte_m3 > 0):
                continue
            SL, rec, dem = lot_terms(r, f)
            N = int(np.floor(0.70 * SL / 80))
            s_ers = 0.4 if SL >= 10000 else 0.0
            V = vra(th, p, s_ers, rec, dem) * SL; Lm = np.maximum(V, 0)
            V1 = vra(th, p, 0.0, rec, dem) * SL
            for T in TT:
                for c0 in C0:
                    Ls = lstar(th, c0, T, rec, dem) * SL
                    reg = {"acq": Lm - Ls, "ces": -Ls, **{k: a * Lm + (r.area_m2 if a == 0 else 0) - Ls for k, a in ALPHA.items()}}
                    for g_, dl in reg.items():
                        row = dict(id=lid, classe=r.classe, gfu=gfu, zona=r.zona, fascia=r.fascia, proprieta=r.proprieta,
                                   area_m2=r.area_m2, variante=("R1" if f == "R1" else ("R2" if r.classe == "lotto da riusare" else "nuovo")),
                                   FAR=(np.nan if f == "R1" else f), SL=SL, N=N, T=T, c0=c0, regime=g_,
                                   quota_cal=float((dl[w] <= 0).mean()), quota_cubo=float((dl <= 0).mean()))
                        if c0 == 90.0:
                            q = np.quantile(dl[w], [.05, .5, .95]) / r.area_m2
                            row.update(dL_q05=q[0], dL_q50=q[1], dL_q95=q[2])
                        if c0 == 90.0 and g_ == "acq":
                            row.update(VRA_q50=float(np.median(V[w]) / r.area_m2), VRA_D1_q50=float(np.median(V1[w]) / r.area_m2),
                                       Lstar_q50=float(np.median(Ls[w]) / r.area_m2), VRA_q50_SL=float(np.median(V[w]) / SL),
                                       cstar_L0_q50=float(np.median(cstar(th, 0.0, T, rec=rec, dem=dem)[w])),
                                       cstar_Lmkt_q50=float(np.median(cstar(th, Lm / SL, T, rec=rec, dem=dem)[w])))
                        rows.append(row)
        stats.append(dict(id=lid, zona=r.zona, zona_centroide=r.zona_centroide, fascia=r.fascia, classe=r.classe,
                          p_lo=lo, p_mid=mid, p_hi=hi, canone=canoni[r.zona]))
    D = pd.DataFrame(rows); S = pd.DataFrame(stats)
    res["T1"] = dict(assegnati=int(S.zona.notna().sum()), totale=len(S), quota_centroide_uguale=float((S.zona == S.zona_centroide).mean()))
    res["E3"] = bool(all((zt.p_min_omi[z] <= prezzi[z][0]) and (prezzi[z][2] <= zt.p_max_omi[z]) and
                         (zt.can_min_omi[z] <= canoni[z] <= zt.can_max_omi[z]) for z in S.zona.unique()))
    # ---- tornado e E6
    tor, e6 = tornado(L, base, prezzi)
    res["E6"] = e6
    res["informativi"] = informativi(base, D, L, prezzi)
    if out:
        write(D, S, res, tor, th, ok, L, base, prezzi)
    return D, S, res, tor


def tornado(L, base, prezzi):
    E = L[(L.classe == "lotto edificabile")]
    p_lo = np.array([prezzi[z][0] for z in E.zona]); p_mid = np.array([prezzi[z][1] for z in E.zona]); p_hi = np.array([prezzi[z][2] for z in E.zona])
    SL = E.area_m2.values * 1.0; s = np.where(SL >= 10000, 0.4, 0.0)
    def dl(t):
        tt = {k: np.asarray(v) for k, v in t.items()}
        V = vra(tt, price(tt, p_lo, p_mid, p_hi), s) * SL
        return np.maximum(V, 0) - lstar(tt, 90.0, 60) * SL
    d0 = dl(base); rows, e6 = [], {}
    for k in P:
        lo_, hi_ = dict(base), dict(base); lo_[k] = np.array(P[k][1]); hi_[k] = np.array(P[k][2])
        a, b = dl(lo_), dl(hi_)
        flip = float(((a <= 0) != (b <= 0)).mean())
        rows.append(dict(parametro=k, basso=P[k][1], alto=P[k][2], dL_med_base=float(np.median(d0 / E.area_m2)),
                         dL_med_basso=float(np.median(a / E.area_m2)), dL_med_alto=float(np.median(b / E.area_m2)),
                         quota_lotti_segno_cambia=flip, senza_fonte=k in SENZA_FONTE))
        e6[k] = flip
    tt = {k: np.asarray(v) for k, v in base.items()}
    V = np.maximum(vra(tt, price(tt, p_lo, p_mid, p_hi), s) * SL, 0)
    a, b = V - lstar(tt, 90.0, 30) * SL, V - lstar(tt, 90.0, 90) * SL
    rows.append(dict(parametro="T (durata, non nel cubo)", basso=30, alto=90, dL_med_base=float(np.median(d0 / E.area_m2)),
                     dL_med_basso=float(np.median(a / E.area_m2)), dL_med_alto=float(np.median(b / E.area_m2)),
                     quota_lotti_segno_cambia=float(((a <= 0) != (b <= 0)).mean()), senza_fonte=False))
    return pd.DataFrame(rows), e6


SACC = [("via Cascella 5", 28, 2964504.00), ("P.le Cooperazione 1 (LUM)", 14, 1387400.70), ("P.le Cooperazione 1 (Solidarnosc)", 14, 1387067.10),
        ("via Castellammare 16 (9)", 9, 1647062.80), ("via Castellammare 16 (5)", 5, 1252281.19), ("via Castellammare 16 (1)", 1, 234481.00)]


def informativi(base, D, L, prezzi):
    """Controlli informativi, fuori dai criteri: K2(b) SACC, asta diritti edificatori, varianti IVA e VF (punto base, FAR 1, c0 = 90, T = 60)."""
    t = {k: np.asarray(v) for k, v in base.items()}
    cost_all = float(80 / t["eta"] * t["c_new"] * (1 + t["sigma"]))  # 80 m² commerciali per alloggio [H], prezzi 2025
    sacc = [dict(caso=c, alloggi=n, inv_per_alloggio=i / n, inv_2025=i / n * 110.7 / 96.6, modello=cost_all,
                 rapporto=cost_all / (i / n * 110.7 / 96.6)) for c, n, i in SACC]
    E = D[(D.classe == "lotto edificabile") & (D.FAR == 1.0) & (D.c0 == 90) & (D["T"] == 60) & (D.regime == "acq")]
    dir_ = float(E[E.fascia.isin(["D", "E"])].VRA_q50_SL.median())
    ed = L[L.classe == "lotto edificabile"]; var = {}
    for nome, kw in [("base", {}), ("IVA 10% sul godimento", dict(iva=0.10)), ("VF con y_exit 4,5% (solo acquisto)", dict(y_exit=0.045))]:
        acq = ces = 0
        for lid, r in ed.iterrows():
            lo, mid, hi = prezzi[r.zona]; SL = r.area_m2
            Lm = max(float(vra(t, price(t, lo, mid, hi), 0.4 if SL >= 1e4 else 0.0)), 0.0)
            Ls = float(lstar(t, 90.0, 60, **kw))
            acq += Lm - Ls <= 0; ces += -Ls <= 0
        var[nome] = dict(lotti=len(ed), regge_acquisto=int(acq), regge_cessione=int(ces))
    return dict(SACC_K2b=sacc, diritti_edificatori=dict(prezzo_asta_2023_euro_m2_SL=678, VRA_mediana_D_E_FAR1_euro_m2_SL=dir_),
                varianti_punto_base=var)


def write(D, S, res, tor, th, ok, L, base, prezzi):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    (H / "tabelle").mkdir(exist_ok=True); (H / "fig").mkdir(exist_ok=True)
    D = D.sort_values(["id", "variante", "FAR", "T", "c0", "regime"], na_position="first")
    rnd = {c: 4 for c in ["quota_cal", "quota_cubo", "FAR"]} | {c: 0 for c in D.columns if c.startswith(("dL_", "VRA", "Lstar", "SL"))} | {c: 2 for c in D.columns if c.startswith("cstar")}
    D.round(rnd).to_csv(H / "tabelle" / "delta_L_lotti.csv", index=False)
    S.to_csv(H / "tabelle" / "lotti_omi.csv", index=False)
    pd.DataFrame(res["K1"]).round(4).to_csv(H / "tabelle" / "taratura_K1.csv", index=False)
    tor.round(4).to_csv(H / "tabelle" / "tornado.csv", index=False)
    # sintesi della regione: lotti con quota_cal >= 0,5 (fuori GFU), per FAR/variante/regime/c0/T/fascia
    B = D[~D.gfu]
    g = B.assign(regge=B.quota_cal >= 0.5, N_regge=lambda x: x.N * x.regge).groupby(
        ["classe", "variante", "FAR", "T", "c0", "regime", "fascia"], dropna=False).agg(
        lotti=("id", "size"), lotti_regge=("regge", "sum"), alloggi=("N", "sum"), alloggi_regge=("N_regge", "sum"),
        quota_cal_media=("quota_cal", "mean"), dL_q50_mediana=("dL_q50", "median")).reset_index()
    g.round(4).to_csv(H / "tabelle" / "regione_sintesi.csv", index=False)
    D[D.gfu].round(rnd).to_csv(H / "tabelle" / "gfu_scenario.csv", index=False)
    # mappe 2D per i tre lotti rappresentativi (registro 8f)
    E = L[L.classe == "lotto edificabile"].copy(); E["gr"] = E.fascia.map({"B": "B", "C": "C+D", "D": "C+D", "E": "E"})
    rep = {}
    for gr, x in E.groupby("gr"):
        m = x.area_m2.median()
        rep[gr] = sorted(x.index[(x.area_m2 - m).abs() == (x.area_m2 - m).abs().min()])[0]
    res["lotti_rappresentativi"] = rep
    fig, ax = plt.subplots(3, 3, figsize=(13, 11))
    for i, (gr, lid) in enumerate(rep.items()):
        r = L.loc[lid]; lo, mid, hi = prezzi[r.zona]; SL = r.area_m2
        t0 = {k: np.asarray(v) for k, v in base.items()}
        Lm = max(float(vra(t0, price(t0, lo, mid, hi), 0.4 if SL >= 1e4 else 0.0)), 0.0)
        # (a) prezzo del suolo × canone
        cc, LL = np.meshgrid(np.linspace(40, 160, 121), np.linspace(0, max(1500, 1.5 * Lm), 121))
        Z = lstar(t0, cc, 60) - LL
        ax[i, 0].contourf(cc, LL, Z >= 0, levels=[-.5, .5, 1.5], colors=["#e8b4b4", "#b4d8b4"]); ax[i, 0].axhline(Lm, ls="--", c="k")
        ax[i, 0].set(xlabel="canone c0 €/m²/anno", ylabel="prezzo suolo €/m² SL", title=f"{lid} ({gr}, zona {r.zona}): verde = coop regge, T=60")
        # (b) costo × tasso i_D, suolo = L_mkt
        for j, (kx, ky, xs, ys) in enumerate([("c_new", "i_D", np.linspace(1600, 2600, 101), np.linspace(.025, .055, 101)),
                                               ("T", "i_D", np.arange(20, 91), np.linspace(.025, .055, 101))]):
            X, Y = np.meshgrid(xs, ys); t = dict(t0); t["i_D"] = Y
            if kx == "c_new":
                t["c_new"] = X; Lmk = np.maximum(vra(t, price(t, lo, mid, hi), 0.4 if SL >= 1e4 else 0.0), 0); Zm = lstar(t, 90.0, 60) - Lmk
            else:
                Zm = lstar(t, 90.0, X) - Lm
            ax[i, j + 1].contourf(X, Y, Zm >= 0, levels=[-.5, .5, 1.5], colors=["#e8b4b4", "#b4d8b4"])
            ax[i, j + 1].set(xlabel=kx, ylabel="i_D", title=f"acquisto a L_mkt, c0=90")
    fig.tight_layout(); fig.savefig(H / "fig" / "mappe_2d.png", dpi=110); plt.close(fig)
    json.dump(res, open(H / "esito_criteri.json", "w"), indent=1, default=float, ensure_ascii=False)


def content_hash():
    h = hashlib.sha256()
    for f in ["delta_L_lotti.csv", "regione_sintesi.csv", "taratura_K1.csv", "tornado.csv", "lotti_omi.csv", "gfu_scenario.csv"]:
        h.update((H / "tabelle" / f).read_bytes())
    return h.hexdigest()


if __name__ == "__main__":
    D, S, res, tor = run()
    print(json.dumps({k: res[k] for k in ["n_Theta_cal", "quota_Theta_cal", "centrale_in_Theta_cal", "T1", "E3"]}, default=float))
    print("hash_contenuto", content_hash())
