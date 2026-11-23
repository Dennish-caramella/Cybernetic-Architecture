"""Base P v3 (ticket #18; unica modifica: titolo con arrotondamento a due vincoli, pre-registrazione v3 a2561ce8...; resto = v2; regole v2: sha256 1bf8df2a...; differenze dalla v1 marcate [v2]): popolazione sintetica dei nuclei abitativi di Milano.
Regole v1: sha256 fa0ec4f8.... Dati: scarica.py -> ../_cache/P_popolazione/raw/.
Uso:
  python3 -I run.py controlla                      # margini dal grezzo = CSV delle note (sezione 0 / regola di arresto)
  python3 -I run.py esegui [--seme S] [--pilota] [--scenario NOME] [--scrivi]
  python3 -I run.py robustezza                     # P3: seme principale due volte + 10 semi
  python3 -I run.py sensibilita                    # S1-S9
I margini tenuti fuori V1, V2 (valori per NIL di ds205) non sono usati da questo file: carica() legge tutto ds205, ma della colonna "Minori"
usa solo il totale cittadino (M6, adattato) e non usa la colonna "80 e + soli..."; il confronto per NIL lo fa solo valida_p4.py.
"""
import glob, hashlib, io, json, os, sys, zipfile
import numpy as np, pandas as pd, geopandas as gpd
from scipy.spatial import cKDTree
from scipy.stats import norm

QUI = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(QUI, "..", "_cache", "P_popolazione", "raw")  # cache v1, sola lettura (hash in dati_metadati.csv)
OUT = os.path.join(QUI, "..", "_cache", "P_popolazione_v3", "out")
TAB = os.path.join(QUI, "tabelle")
NOTE = os.path.join(QUI, "..", "..", "secondo_cervello", "ricerche", "milano_dati")
SEME = 20261122
CRS = 32632
TIP = ["Monocomponente", "Coppia sposata senza figli", "Coppia sposata con figli", "Monogenitore con uno o piu figli",
       "Monogenitore con uno o piu figli e almeno un convivente", "Capofamiglia con almeno un convivente", "In convivenza", "Altre tipologie"]
MONO, CSF, CCF, MG, MGC, CCONV, INCONV, ALTRE = range(8)
ETA = ["Meno di 35 anni", "35-64 anni", "65-79 anni", "80 anni e piu"]
DIM = ["1", "2", "3", "4", "5 e piu"]
# zeri strutturali tipologia x componenti (pre-registrazione 4.1) [H]
AMMESSI = {MONO: [1], CSF: [2], CCF: [3, 4, 5], MG: [2, 3, 4, 5], MGC: [3, 4, 5], CCONV: [2, 3, 4, 5], INCONV: [2, 3, 4, 5], ALTRE: [2, 3, 4, 5]}
MEF_CL = [("0-10k", 0, 10000, "da 0 a 10000 euro"), ("10-15k", 10000, 15000, "da 10000 a 15000 euro"),
          ("15-26k", 15000, 26000, "da 15000 a 26000 euro"), ("26-55k", 26000, 55000, "da 26000 a 55000 euro"),
          ("55-75k", 55000, 75000, "da 55000 a 75000 euro"), ("75-120k", 75000, 120000, "da 75000 a 120000 euro"),
          (">120k", 120000, np.inf, "oltre 120000 euro")]
BASE = dict(tenure="T0", studenti=70000, in_residenza=11000, canone="omi", rho_p=0.0, rho_eta=0.0, giovani_coppie="sposate",
            sap="inclusi", arrivi_dim=1.5, arrivi_shift=0.0, budget="30", q2=0.7, q_dsu=0.3)
SCENARI = {"base": {}, "S1_T1": dict(tenure="T1"), "S2_stud50k": dict(studenti=50000), "S2_stud90k": dict(studenti=90000),
           "S2_res16k": dict(in_residenza=16000), "S3_annunci": dict(canone="annunci"), "S4_rho_p05": dict(rho_p=0.5),
           "S4_rho_eta": dict(rho_eta=-0.3), "S5_conviventi": dict(giovani_coppie="+conviventi"), "S6_sap_esclusi": dict(sap="esclusi"),
           "S7_dim2": dict(arrivi_dim=2.0), "S7_shift": dict(arrivi_shift=-0.2), "S8_residuo": dict(budget="residuo"),
           "S9_q05": dict(q2=0.5), "S9_q09": dict(q2=0.9)}
CAT = ["studenti fuori sede", "famiglie con figli minorenni", "anziani soli", "giovani coppie", "giovani soli e nuovi arrivati", "nessuna categoria"]
MQ = {1: 45, 2: 60, 3: 75, 4: 85, 5: 95}  # m2; monogenitore con 1 figlio = 65 [H, 4.5]
SCALA_ISEE = {1: 1.0, 2: 1.57, 3: 2.04, 4: 2.46, 5: 2.85}  # 5: [L]
BORSA = [8248, 7172, 5857]  # fuori sede, fasce ISU 1/2/3, Bocconi 2026/27 [V nota 06]
ATENEI = {"Milano": "UNIVERSITA' DEGLI STUDI DI MILANO", "Milano Politecnico": "POLITECNICO DI MILANO",
          "Milano Cattolica": "UNIVERSITA' CATTOLICA DEL SACRO CUORE", "Milano Bicocca": "UNIVERSITA' DEGLI STUDI DI MILANO BICOCCA",
          "Milano Bocconi": "UNIVERSITA' COMMERCIALE LUIGI BOCCONI", "Milano IULM": "IULM", "Milano San Raffaele": "VITA-SALUTE SAN RAFFAELE"}

def raw(n): return os.path.join(RAW, n)
def zcsv(n, **k):
    z = zipfile.ZipFile(raw(n)); return pd.read_csv(z.open(z.namelist()[0]), **k)
def fix(s): return s.astype(str).str.replace("Ã¹", "u").str.replace("Ã ", "a").str.replace("ù", "u")
def codice(s): return s.astype(str).str.extract(r"\((\d+)\)\s*$")[0].astype(int)

# ------------------------------------------------------------------ dati (solo margini adattati)
_D = {}
def carica():
    if _D: return _D
    f = zcsv("ds1441.zip", sep=";", encoding="latin1", usecols=["Anno", "Quartiere", "Classe_eta_capofamiglia", "Numero_componenti", "Tipologia_familiare", "Famiglie"])
    y = f[f.Anno == 2025].copy()
    for c in ["Classe_eta_capofamiglia", "Numero_componenti", "Tipologia_familiare"]: y[c] = fix(y[c])
    y["n"] = codice(y.Quartiere); y["t"] = y.Tipologia_familiare.map({t: i for i, t in enumerate(TIP)})
    y["a"] = y.Classe_eta_capofamiglia.map({a: i for i, a in enumerate(ETA)}); y["d"] = y.Numero_componenti.map({d: i for i, d in enumerate(DIM)})
    assert y[["t", "a", "d"]].notna().all().all()
    NIL = np.sort(y.n.unique()); ix = {n: i for i, n in enumerate(NIL)}; y["i"] = y.n.map(ix)
    K = len(NIL)
    M1 = np.zeros((K, 8)); np.add.at(M1, (y.i, y.t), y.Famiglie)
    M2 = np.zeros((8, 4)); np.add.at(M2, (y.t, y.a), y.Famiglie)
    M3a = np.zeros(K); m = (y.t == MONO) & (y.a >= 2); np.add.at(M3a, y.i[m], y.Famiglie[m])
    M3b = np.zeros(K); m = y.a == 0; np.add.at(M3b, y.i[m], y.Famiglie[m])
    M4 = np.zeros(5); np.add.at(M4, y.d, y.Famiglie)
    M0 = np.zeros((K, 4, 8, 5)); np.add.at(M0, (y.i, y.a, y.t, y.d), y.Famiglie)  # [v2 C1] congiunta vera
    vero = dict(nta=np.zeros((K, 8, 4)), td=np.zeros((8, 5)))  # congiunte vere: solo confronto informativo
    np.add.at(vero["nta"], (y.i, y.t, y.a), y.Famiglie); np.add.at(vero["td"], (y.t, y.d), y.Famiglie)
    m = zcsv("ds139.zip", sep=";", encoding="latin1"); m.columns = [c.replace("ï»¿", "").replace("﻿", "") for c in m.columns]
    m = m[m.Anno == 2021].copy(); m["n"] = codice(m.NIL); tt = m.Tipologia_familiare.astype(str)
    g = pd.DataFrame(dict(tot=m.groupby("n").Famiglie.sum(), cm=m[tt.str.contains("minorenne")].groupby("n").Famiglie.sum(),
                          mg=m[tt == "Monogenitore con almeno un figlio minorenne"].groupby("n").Famiglie.sum())).reindex(NIL).fillna(0)
    M5 = (g.cm / g.tot).values, (g.mg / g.tot).values
    # [v2 C2] quote condizionate r^C, r^M per NIL x eta x componenti (4 e piu), ripiego se denominatore < 20
    m["i"] = m.n.map(ix); m["a"] = fix(m.Classe_eta_capofamiglia).map({"Da 18 a 34 anni": 0, "Da 35 a 64 anni": 1, "Da 65 a 79 anni": 2, "80 anni e piu": 3})
    m["s"] = fix(m.Numero_componenti).map({"1": 0, "2": 1, "3": 2, "4 e piu": 3}); assert m[["i", "a", "s"]].notna().all().all()
    def quota(num, den):
        Nm = np.zeros((K, 4, 4)); De = np.zeros((K, 4, 4))
        for arr, sel in ((Nm, tt.isin(num)), (De, tt.isin(den))): np.add.at(arr, (m.i[sel].astype(int), m.a[sel].astype(int), m.s[sel].astype(int)), m.Famiglie[sel])
        r = np.where(De >= 20, Nm / np.maximum(De, 1), np.nan); liv = np.where(De >= 20, 0, -1)
        na_, da_ = Nm.sum(2, keepdims=True), De.sum(2, keepdims=True); r2 = np.broadcast_to(np.where(da_ >= 20, na_ / np.maximum(da_, 1), np.nan), r.shape)
        nc, dc = Nm.sum(0), De.sum(0); r3 = np.broadcast_to(np.where(dc >= 20, nc / np.maximum(dc, 1), Nm.sum((0, 2))[:, None] / De.sum((0, 2))[:, None]), r.shape)
        liv = np.where(np.isnan(r), np.where(np.isnan(r2), 2, 1), 0); r = np.where(np.isnan(r), np.where(np.isnan(r2), r3, r2), r)
        return r, liv, De
    CPL = ["Coppia sposata con almeno un figlio minorenne", "Coppia convivente con almeno un figlio minorenne"]
    CPM = ["Coppia sposata con figli tutti maggiorenni", "Coppia convivente con figli tutti maggiorenni"]
    RC = quota(CPL, CPL + CPM); RM = quota(["Monogenitore con almeno un figlio minorenne"], ["Monogenitore con almeno un figlio minorenne", "Monogenitore con figli tutti maggiorenni"])
    q = pd.read_csv(raw("ds205.csv"), sep=";", encoding="latin1"); q24 = q[q.Anno == 2024]
    M6 = float(q24.Minori.sum())  # solo totale cittadino (la distribuzione per NIL e' tenuta fuori, V2)
    imm = q24.groupby("NIL").Immigrati.sum().reindex(NIL).fillna(0).values
    h = pd.read_csv(raw("istat_hudw_2021.csv")); h = h.set_index("TENURE_STATUS_HOU").OBS_VALUE
    M7 = np.array([h["RENT"], h["OWN"], h["OTH_OR"]]) / h["ALL"]  # affitto, proprieta, altro
    t = pd.read_csv(raw("ds1457_titolo.csv"), sep=";", encoding="latin1"); t.columns = ["NIL", "prop", "aff", "altro"]
    t["n"] = codice(t.NIL); t = t.groupby("n")[["aff", "prop", "altro"]].sum().reindex(NIL)
    M8seed = t.values  # NaN se NIL assente nel 2011
    c = zcsv("mef_comunale_2024.zip", sep=";", dtype=str, encoding="latin1")
    c.columns = [x.strip() for x in c.columns]; r = c[(c["Denominazione Comune"] == "MILANO") & (c["Sigla Provincia"] == "MI")].iloc[0]
    M9 = np.array([float(r[f"Reddito complessivo {lab} - Frequenza"]) for _, _, _, lab in MEF_CL])
    am = [float(r[f"Reddito complessivo {lab} - Ammontare in euro"]) for _, _, _, lab in MEF_CL]
    media_top = am[-1] / M9[-1]
    u = pd.read_csv(raw("ds752_2024_25.csv"), sep=";", encoding="latin1"); M11 = u.groupby("AteneoNOME").Isc.sum()
    mv = pd.read_csv(raw("ds71.csv"), sep=";", encoding="latin1"); M12 = float(mv[mv.iloc[:, 0] == 2024].iloc[0, 3])
    _D.update(M0=M0, RC=RC, RM=RM, NIL=NIL, M1=M1, M2=M2, M3a=M3a, M3b=M3b, M4=M4, M5=M5, M6=M6, M7=M7, M8seed=M8seed, M9=M9, media_top=media_top,
                M11=M11, M12=M12, imm=imm, vero=vero, ds139=g)
    return _D

def controlla():
    D = carica(); P = os.path.join(NOTE, "popolazioni"); err = []
    a = pd.read_csv(os.path.join(P, "famiglie_2025_per_NIL_ds1441.csv")); a["n"] = codice(a.Quartiere); a = a.set_index("n").reindex(D["NIL"])
    err += [("ds1441 totale NIL", np.abs(a.totale.values - D["M1"].sum(1)).max()), ("ds1441 soli65+", np.abs(a.soli_65piu.values - D["M3a"]).max()),
            ("ds1441 under35", np.abs(a.under35_capofam.values - D["M3b"]).max())]
    for j, t in enumerate(TIP): err.append((f"ds1441 {t[:20]}", np.abs(a[t].values - D["M1"][:, j]).max()))
    m = pd.read_csv(os.path.join(P, "famiglie_2025_milano_ds1441.csv")); ex = m[m.dimensione == "eta_x_tipologia"].modalita.str.split(" \\| ", expand=True)
    M2n = np.zeros((8, 4)); M2n[ex[1].map({t: i for i, t in enumerate(TIP)}).values, ex[0].map({x: i for i, x in enumerate(ETA)}).values] = m[m.dimensione == "eta_x_tipologia"].famiglie_2025.values
    err += [("ds1441 tipologia x eta (M2)", np.abs(M2n - D["M2"]).max()), ("ds1441 componenti (M4)", np.abs(m[m.dimensione == "Numero_componenti"].famiglie_2025.values - D["M4"]).max())]
    b = pd.read_csv(os.path.join(P, "famiglie_2021_con_minori_per_NIL_ds139.csv")); b["n"] = codice(b.NIL); b = b.set_index("n").reindex(D["NIL"])
    err += [("ds139 con_minori", np.abs(b.con_minori.values - D["ds139"].cm.values).max()), ("ds139 monogen", np.abs(b.monogen_minori.values - D["ds139"].mg.values).max()),
            ("ds139 totale", np.abs(b.totale.values - D["ds139"].tot.values).max())]
    c = pd.read_csv(os.path.join(P, "titolo_godimento_2011_per_NIL_ds1457.csv")); c["n"] = codice(c.NIL); c = c.set_index("n").reindex(D["NIL"])
    err.append(("ds1457 affitto/prop/altro", np.nanmax(np.abs(c[["affitto", "proprieta", "altro"]].values - D["M8seed"]))))
    k = pd.read_csv(os.path.join(P, "istat_famiglie_titolo_godimento_milano_2021.csv")).set_index("TENURE_STATUS_HOU").OBS_VALUE
    err.append(("ISTAT titolo 2021 quote", np.abs(np.array([k.RENT, k.OWN, k.OTH_OR]) / k.ALL - D["M7"]).max()))
    mk = pd.read_csv(os.path.join(NOTE, "mercato", "mef_milano_classi_reddito_2014_2024.csv")); mk = mk[(mk.anno == 2024) & (mk.classe != "<=0")]
    err.append(("MEF classi 2024", np.abs(mk.contribuenti.values - D["M9"]).max()))
    s = pd.read_csv(os.path.join(P, "iscritti_universita_milanesi_ds752.csv")); s = s[s.AnnoA == "2024/2025"].set_index("AteneoNOME").Isc
    err.append(("ds752 2024/25", np.abs(s.reindex(D["M11"].index).values - D["M11"].values).max()))
    mv = pd.read_csv(os.path.join(P, "movimento_anagrafico_2010_2024_ds71.csv")); err.append(("ds71 immigrati 2024", abs(mv[mv.anno == 2024].immigrati.iloc[0] - D["M12"])))
    err.append(("ds205 minori totale (nota 06: 196.577)", abs(D["M6"] - 196577)))
    M0 = D["M0"]; err += [("[v2] M0 -> M1", np.abs(M0.sum((1, 3)) - D["M1"]).max()), ("[v2] M0 -> M2", np.abs(M0.sum((0, 3)).T - D["M2"]).max()),
            ("[v2] M0 -> M4", np.abs(M0.sum((0, 1, 2)) - D["M4"]).max()), ("[v2] M0 -> M3a", np.abs(M0[:, 2:, MONO].sum((1, 2)) - D["M3a"]).max()),
            ("[v2] M0 -> M3b", np.abs(M0[:, 0].sum((1, 2)) - D["M3b"]).max()), ("[v2] quote r in [0,1]", float(max(np.nanmax(D["RC"][0]), np.nanmax(D["RM"][0])) > 1 or min(np.nanmin(D["RC"][0]), np.nanmin(D["RM"][0])) < 0))]
    ok = all(e < 1e-6 for _, e in err)
    for n, e in err: print(f"{'OK ' if e < 1e-6 else 'DIV'} {n}: scarto massimo {e}")
    print("CONTROLLO MARGINI:", "coincidono" if ok else "NON coincidono -> fermarsi"); return ok

# ------------------------------------------------------------------ strumenti
def hamilton(x, tot, rng):
    """arrotondamento a resti maggiori con spareggio casuale; conserva tot."""
    x = np.asarray(x, float); b = np.floor(x); r = x - b; k = int(round(tot - b.sum()))
    o = np.lexsort((rng.random(len(x)), -r)); b[o[:k]] += 1; return b.astype(int)

def ipf3(D, it=2000, tol=1e-8):
    K = len(D["NIL"]); T = np.ones((K, 8, 4)); conv = False
    for _ in range(it):
        T0 = T.copy()
        T *= (D["M1"] / np.maximum(T.sum(2), 1e-300))[:, :, None]
        T *= (D["M2"] / np.maximum(T.sum(0), 1e-300))[None, :, :]
        s = T[:, MONO, 2:].sum(1); T[:, MONO, 2:] *= (D["M3a"] / np.maximum(s, 1e-300))[:, None]
        s = T[:, :, 0].sum(1); T[:, :, 0] *= (D["M3b"] / np.maximum(s, 1e-300))[:, None]
        if np.nanmax(np.abs(T - T0) / np.maximum(T0, 1e-12)) < tol: conv = True; break
    return T, conv, _ + 1

def ipf2(seed, r, c, it=2000, tol=1e-10):
    T = seed.astype(float).copy()
    for _ in range(it):
        T0 = T.copy(); T *= (r / np.maximum(T.sum(1), 1e-300))[:, None]; T *= (c / np.maximum(T.sum(0), 1e-300))[None, :]
        if np.nanmax(np.abs(T - T0) / np.maximum(T0, 1e-12)) < tol: break
    return T

def netto(R, pens):
    R = np.asarray(R, float); t = 0.23 * np.minimum(R, 28000) + 0.35 * np.clip(R - 28000, 0, 22000) + 0.43 * np.maximum(R - 50000, 0)
    dd = np.select([R <= 15000, R <= 28000, R <= 50000], [1955, 1910 + 1190 * (28000 - R) / 13000, 1910 * (50000 - R) / 22000], 0) + np.where((R > 25000) & (R <= 35000), 65, 0)
    dp = np.select([R <= 8500, R <= 28000, R <= 50000], [1955, 700 + 1255 * (28000 - R) / 19500, 700 * (50000 - R) / 22000], 0) + np.where((R > 25000) & (R <= 29000), 50, 0)
    irpef = np.maximum(0, t - np.where(pens, dp, dd)); ti = np.where(~pens & (R > 8500) & (R <= 15000), 1200, 0)
    reg = 0.0123 * np.minimum(R, 15000) + 0.0158 * np.clip(R - 15000, 0, 13000) + 0.0172 * np.clip(R - 28000, 0, 22000) + 0.0173 * np.maximum(R - 50000, 0)
    com = np.where(R > 23000, 0.008 * R, 0); low = R <= 8500
    return R - irpef - np.where(low, 0, reg) - np.where(low, 0, com) + ti  # formula della nota 02 (analisi_accessibilita.py) [H]

def auu_mese(isee):
    return np.clip(199.4 - (199.4 - 57.0) * (isee - 17090.61) / (45574.96 - 17090.61), 57.0, 199.4)  # [S/H] nota 02

def lordo_da_u(u, M9, media_top):
    p = M9 / M9.sum(); cum = np.concatenate([[0], np.cumsum(p)]); k = np.clip(np.searchsorted(cum, u, side="right") - 1, 0, 6)
    w = (u - cum[k]) / p[k]; lo = np.array([c[1] for c in MEF_CL])[k]; hi = np.array([c[2] for c in MEF_CL])[k]
    alfa = media_top / (media_top - 120000)  # Pareto con media di classe [I]
    return np.where(k < 6, lo + w * np.where(np.isfinite(hi), hi - lo, 0), 120000 * (1 - np.clip(w, 0, 1 - 1e-12)) ** (-1 / alfa)), k

# ------------------------------------------------------------------ geodati
_GEO = {}
def geo():
    if _GEO: return _GEO
    r = lambda n: gpd.read_file(raw(n)).to_crs(CRS)
    nil = r("ds964_nil.geojson"); conf = r("ds2841_confine.geojson")
    civ = zcsv("ds634_civici.zip", sep=";", encoding="latin1", usecols=["ID_NIL", "LONG_WGS84", "LAT_WGS84", "DATA_SOPPRESSIONE", "STATOCIVICO", "RESIDENZIALE"])
    civ = civ[(civ.STATOCIVICO == "Applicato") & (civ.RESIDENZIALE == 1) & (civ.DATA_SOPPRESSIONE.fillna(0) == 0) & civ.LONG_WGS84.notna() & civ.ID_NIL.notna()]
    civ = gpd.GeoDataFrame(civ, geometry=gpd.points_from_xy(civ.LONG_WGS84.astype(float), civ.LAT_WGS84.astype(float)), crs=4326).to_crs(CRS)
    sez = r("ds98_sezioni2011.geojson")[["SEZ", "geometry"]]; sez["cx"] = sez.geometry.centroid.x; sez["cy"] = sez.geometry.centroid.y
    omi = r("ds3023_zone_omi.geojson")[["Zona", "geometry"]]
    q = pd.read_csv(raw("ds3024_omi_loc.csv"), sep=";", decimal=",", encoding="utf-8-sig")
    q = q[(q.Descr_Tipologia == "Abitazioni civili") & (q.Stato == "NORMALE")]; omi = omi.merge(q.assign(mid=(q.Loc_min + q.Loc_max) / 2)[["Zona", "mid"]], on="Zona", how="left")
    def pts(n, f=None):
        g = r(n); g = g[f(g)] if f is not None else g; g = g[~g.geometry.is_empty & g.geometry.notna()]; return np.c_[g.geometry.x, g.geometry.y]
    scuole = dict(nido=pts("ds47_nidi.geojson", lambda g: g.CODANNOSCOLASTICO.astype(str) == "1819"), infanzia=pts("ds3014_infanzia.geojson"),
                  primaria=pts("ds3015_primarie.geojson"), sec1=pts("ds3016_sec1.geojson"), sec2=pts("ds78_sec2.geojson"))
    mmg = gpd.read_file(raw("ds234_mmg.geojson")); mmg = mmg[mmg.attivo.astype(str) == "1"].to_crs(CRS)
    mmg = np.unique(np.c_[mmg.geometry.x, mmg.geometry.y].round(1), axis=0)
    at = gpd.read_file(raw("ds94_atenei.geojson")).to_crs(CRS); sedi = {k: np.unique(np.c_[at[at.DENOMINAZ == v].geometry.x, at[at.DENOMINAZ == v].geometry.y].round(1), axis=0) for k, v in ATENEI.items()}
    com = gpd.read_file(f"zip://{raw('istat_comuni_2024_g.zip')}!Limiti01012024_g/Com01012024_g/Com01012024_g_WGS84.shp").to_crs(CRS)
    com = dict(zip(com.COMUNE.str.upper(), zip(com.geometry.centroid.x, com.geometry.centroid.y)))
    od = zcsv("ds390.zip", sep=";", encoding="latin1"); od.columns = ["so", "mo", "nilo", "aceo", "sd", "md", "nild", "aced", "motivo", "n"]
    od = od[od.motivo == "Lavoro"].copy(); od["n"] = od.n.astype(str).str.replace(",", ".").astype(float); od["sd"] = pd.to_numeric(od.sd, errors="coerce"); od = od[od.sd.notna()]; od["sd"] = od.sd.astype(int)  # "Non determinata" (32.247 su 372.123) esclusa [registro]
    ou = zcsv("ds391.zip", sep=";", encoding="latin1"); ou.columns = ["so", "mo", "nilo", "aceo", "reg", "prov", "com", "motivo", "n"]
    ou = ou[ou.motivo == "Lavoro"]; ou["n"] = ou.n.astype(str).str.replace(",", ".").astype(float)
    _GEO.update(nil=nil, conf=conf.geometry.union_all(), civ=civ, sez=sez, omi=omi, scuole=scuole, mmg=mmg, sedi=sedi, com=com, od=od, ou=ou)
    return _GEO

# ------------------------------------------------------------------ generazione
def genera(seme=SEME, pilota=False, **par):
    P = dict(BASE, **par); D = carica(); ss = np.random.SeedSequence(seme).spawn(9); R = [np.random.default_rng(s) for s in ss]
    rep = {}
    K = len(D["NIL"]); h0 = R[0]
    # [v2 C1] scheletro = congiunta vera ds1441 2025 (NIL x eta x tipologia x componenti)
    ii, aa, tt, dd = np.nonzero(D["M0"]); rr = D["M0"][ii, aa, tt, dd].astype(int)
    n = pd.DataFrame(dict(nil_i=np.repeat(ii, rr), eta=np.repeat(aa, rr), tip=np.repeat(tt, rr), dim=np.repeat(dd + 1, rr)))
    if pilota: n = n[n.nil_i.isin([0, 1, 2])].reset_index(drop=True)
    # [v2 C4] nuovi arrivati con arrotondamento controllato; componenti dai residenti <35 dello stesso NIL (ripiego citta)
    na = int(round(D["M12"] / P["arrivi_dim"])); u35 = D["M2"][:, 0] / D["M2"][:, 0].sum(); rows = []
    kn = hamilton(na * D["imm"] / D["imm"].sum(), na, h0)
    for i in range(K):
        if kn[i] == 0 or (pilota and i > 2): continue
        kt = hamilton(kn[i] * u35, kn[i], h0)
        for t in range(8):
            if kt[t] == 0: continue
            w = D["M0"][i, 0, t]; w = w if w.sum() > 0 else D["M0"][:, 0, t].sum(0)
            kd = hamilton(kt[t] * w / w.sum(), kt[t], h0); rows.append(pd.DataFrame(dict(nil_i=i, eta=0, tip=t, dim=np.repeat(np.arange(1, 6), kd))))
    arr = pd.concat(rows, ignore_index=True)
    n["origine"] = "residente"; arr["origine"] = "nuovo arrivo"; n = pd.concat([n, arr], ignore_index=True)
    g = R[1]
    # [v2 N2] adulti: coppia senza figli con 3+ componenti = tutti adulti; In convivenza = 1 (dim 1)
    n["adulti"] = np.select([n.tip == MONO, (n.tip == CSF) & (n.dim == 2), n.tip.isin([CCF, MGC]), n.tip == MG], [1, 2, 2, 1], n.dim)
    n["figli"] = np.where(n.tip.isin([CCF, MG, MGC]), n.dim - n.adulti, 0)
    # [v2 C2] minori: quote condizionate per cella NIL x eta x componenti, arrotondamento per NIL, scelta casuale nella cella
    n["minori"] = 0; flag = np.zeros(len(n), bool); res = (n.origine == "residente").values
    sc = np.minimum(n.dim.values, 4) - 1; el = res & n.tip.isin([CCF, MG, MGC]).values
    rq = np.where(n.tip.values == MG, D["RM"][0][n.nil_i.values, n.eta.values, sc], D["RC"][0][n.nil_i.values, n.eta.values, sc])
    rq = np.where(el, rq, 0.0); tgtC = np.zeros(K); tgtM = np.zeros(K)
    np.add.at(tgtC, n.nil_i.values, rq); np.add.at(tgtM, n.nil_i.values, np.where(n.tip.values == MG, rq, 0)); rep["M5a_target"], rep["M5b_target"] = tgtC, tgtM
    cel = pd.DataFrame(dict(i=n.nil_i.values, a=n.eta.values, t=n.tip.values, s=sc, r=rq))[el]
    for i, gi in cel.groupby("i"):
        grp = gi.groupby(["a", "t", "s"]); keys = list(grp.groups); idxs = [grp.groups[k_] for k_ in keys]
        ex = np.array([gi.r.loc[ix].sum() for ix in idxs]); kk = hamilton(ex, round(ex.sum()), h0)
        for ix, k_ in zip(idxs, kk):
            if k_: flag[g.choice(np.asarray(ix), k_, replace=False)] = True
    rep["minori_quota_res"] = flag[res].mean()
    rep["ripiego_RC"] = {int(l): int(((D["RC"][1] == l) * 1).sum()) for l in (0, 1, 2)}; rep["ripiego_RM"] = {int(l): int(((D["RM"][1] == l) * 1).sum()) for l in (0, 1, 2)}
    arr_m = ~res & n.tip.isin([CCF, MG, MGC]).values; flag[arr_m] = g.random(arr_m.sum()) < (flag[el].mean())
    f = n.figli.values; lo, hi = 0.0, 1.0
    if not pilota:
        for _ in range(60):
            p = (lo + hi) / 2; e = (flag & res) @ (1 + p * (f - 1)); lo, hi = (p, hi) if e < D["M6"] else (lo, p)
    p_min = (lo + hi) / 2 if not pilota else 0.5; rep["p_minori"] = p_min
    n.loc[flag, "minori"] = 1 + g.binomial(np.maximum(f[flag] - 1, 0), p_min)
    # 4.2 titolo: quote come v2 (T0/T1); assegnazione [v3]
    g = R[2]; Nn = np.bincount(n.nil_i[res], minlength=K).astype(float)
    seed = np.nan_to_num(D["M8seed"] / np.nansum(D["M8seed"], 1, keepdims=True), nan=1 / 3) * Nn[:, None]
    TT = ipf2(seed, Nn, D["M7"] * Nn.sum()); rep["TT"] = TT
    lab = np.array(["affitto", "proprieta", "altro"]); tit = np.empty(len(n), object); tit[~res] = "affitto"
    QA = {}
    for i in np.unique(n.nil_i[res]):
        q = TT[i] / TT[i].sum()
        if P["tenure"] == "T0": QA[i] = np.tile(q, (4, 1))
        else:  # T1: odds affitto per eta (<35, 35-64, >=65) = 4, 1, 0.5 [H]; IPF (eta x titolo) dentro il NIL
            e3 = np.minimum(n.eta.values[res & (n.nil_i.values == i)], 2); Na = np.bincount(e3, minlength=3).astype(float)
            sd = np.outer(Na, q); sd[:, 0] *= np.array([4, 1, 0.5]); X = ipf2(sd, Na, TT[i]); X = X / np.maximum(X.sum(1, keepdims=True), 1e-12)
            QA[i] = np.vstack([X[0], X[1], X[2], X[2]])
    # [v3 H-N3] arrotondamento a due vincoli: totali di cella e totali NIL x titolo esatti (passi A-D)
    def sist(E):  # somme cumulate con offset u ~ U(0,1) dal flusso [0]; il totale (intero) e' rispettato esattamente
        C = np.cumsum(E); C[-1] = round(C[-1]); u = h0.random(); F = np.floor(C + u); return (F - np.r_[np.floor(u), F[:-1]]).astype(int)
    rs = pd.DataFrame(dict(i=n.nil_i.values, a=n.eta.values, t=n.tip.values, d=n.dim.values))[res]; rep["troncamenti_T1"] = 0
    for i, gi in rs.groupby("i"):
        grp = gi.groupby(["a", "t", "d"]).groups; keys = list(grp); idxs = [np.asarray(grp[k_]) for k_ in keys]
        Nc = np.array([len(x) for x in idxs], float); Q = np.array([QA[i][k_[0]] for k_ in keys])  # (celle, 3): affitto, proprieta, altro
        Ti = hamilton((Nc[:, None] * Q).sum(0), int(Nc.sum()), h0)  # passo A
        o = h0.permutation(len(keys))  # passo C1
        Ea = Nc * Q[:, 2]; Ea = Ea * Ti[2] / Ea.sum() if Ea.sum() > 0 else Ea
        tr = Ea > Nc; rep["troncamenti_T1"] += int(tr.sum()); Ea = np.minimum(Ea, Nc)
        xa = np.zeros(len(keys), int); xa[o] = sist(Ea[o]) if Ti[2] > 0 else 0  # passo C2 (altro)
        Rc = Nc - xa; w = Q[:, 0] / np.maximum(Q[:, 0] + Q[:, 1], 1e-300); Ef = Rc * w; Ef = Ef * Ti[0] / Ef.sum() if Ef.sum() > 0 else Ef
        tr = Ef > Rc; rep["troncamenti_T1"] += int(tr.sum()); Ef = np.minimum(Ef, Rc)
        xf = np.zeros(len(keys), int); xf[o] = sist(Ef[o]) if Ti[0] > 0 else 0  # passo C3 (affitto)
        xp = Rc - xf  # passo C4 (proprieta)
        for ix, a1, a0, a2 in zip(idxs, xf, xp.astype(int), xa):  # passo D
            tit[g.permutation(ix)] = np.repeat(lab, [a1, a0, a2])
    n["titolo"] = tit
    # 4.6 residenza (civico a caso nel NIL)
    G = geo(); g = R[4]; civ = G["civ"]; cx, cy = civ.geometry.x.values, civ.geometry.y.values; cid = civ.ID_NIL.values
    n["x"] = np.nan; n["y"] = np.nan; nilc = D["NIL"][n.nil_i.values]; miss = []
    for c in np.unique(nilc):
        m = nilc == c; pool = np.flatnonzero(cid == c)
        if len(pool) == 0:
            pg = G["nil"][G["nil"].ID_NIL == c].geometry; miss.append(int(c))
            n.loc[m, "x"] = pg.centroid.x.iloc[0]; n.loc[m, "y"] = pg.centroid.y.iloc[0]; continue
        k = g.choice(pool, m.sum()); n.loc[m, "x"] = cx[k]; n.loc[m, "y"] = cy[k]
    rep["nil_senza_civici"] = miss
    pt = gpd.GeoDataFrame(geometry=gpd.points_from_xy(n.x, n.y), crs=CRS)
    j = gpd.sjoin(pt, G["omi"], how="left", predicate="within"); j = j[~j.index.duplicated()]
    mid = j["mid"].to_numpy(dtype=float, copy=True); zona = j["Zona"].to_numpy(dtype=object, copy=True); nz = np.isnan(mid)
    if nz.any():  # zona senza quotazione civile/normale: zona quotata piu' vicina (dettaglio di codice, a registro)
        oq = G["omi"][G["omi"].mid.notna()]; tr = cKDTree(np.c_[oq.geometry.centroid.x, oq.geometry.centroid.y])
        _, kk = tr.query(np.c_[n.x[nz], n.y[nz]]); mid[nz] = oq.mid.values[kk]; zona[nz] = oq.Zona.values[kk]
    rep["fuori_zona_quotata"] = int(nz.sum()); n["zona_omi"] = zona
    s = gpd.sjoin(pt, G["sez"][["SEZ", "geometry"]], how="left", predicate="within"); s = s[~s.index.duplicated()]; n["sez2011"] = s.SEZ.values
    # 4.3 reddito
    g = R[3]; rows = []
    q2 = P["q2"]; e2 = n.tip.isin([CSF, CCF]) & (g.random(len(n)) < q2)
    extra = np.where(n.tip.isin([MGC, CCONV, ALTRE]), g.binomial(np.maximum(n.adulti - 1, 0), 0.5), 0)
    n["percettori"] = 1 + e2.astype(int) + extra
    rid = np.repeat(np.arange(len(n)), n.percettori); rk = np.concatenate([np.arange(k) for k in n.percettori])
    eta_p = np.where(rk <= (n.tip.isin([CSF, CCF]).values[rid]).astype(int), n.eta.values[rid], 1)  # capofamiglia e partner: stessa classe [H]
    pens = eta_p >= 2
    z = g.standard_normal(len(rid))
    if P["rho_eta"]: s_a = (eta_p - eta_p.mean()) / eta_p.std(); z = P["rho_eta"] * s_a + np.sqrt(1 - P["rho_eta"] ** 2) * z
    if P["rho_p"]:
        first = np.r_[0, np.flatnonzero(np.diff(rid)) + 1]; zf = z[first][np.searchsorted(first, np.arange(len(rid)), side="right") - 1]
        part = (rk == 1) & n.tip.isin([CSF, CCF]).values[rid]; z[part] = P["rho_p"] * zf[part] + np.sqrt(1 - P["rho_p"] ** 2) * z[part]
    u = norm.cdf(z)
    if P["arrivi_shift"]: a_ = (n.origine.values[rid] == "nuovo arrivo"); u[a_] = np.clip(u[a_] + P["arrivi_shift"], 1e-9, 1 - 1e-9)
    L, kcl = lordo_da_u(u, D["M9"], D["media_top"]); rep["M9_sim"] = np.bincount(kcl, minlength=7)
    nt = netto(L, pens); ded = np.where(pens, 0, np.minimum(0.2 * L, 3000))
    n["lordo"] = np.bincount(rid, L, len(n)); n["netto_redditi"] = np.bincount(rid, nt, len(n))
    n["ded"] = np.bincount(rid, ded, len(n)); n["pens_cf"] = n.eta >= 2
    mq = np.where((n.tip == MG) & (n.dim == 2), 65, n.dim.map(MQ)); n["mq"] = mq
    n["canone_mese"] = (mid if P["canone"] == "omi" else 23.3) * mq
    aff = n.titolo == "affitto"; isr = n.lordo - n.ded - np.where(aff, np.minimum(12 * n.canone_mese, 7000), 0)
    n["isee"] = np.maximum(isr, 0) / n.dim.map(SCALA_ISEE)
    n["netto"] = n.netto_redditi + 12 * n.minori * auu_mese(n.isee.values)
    # studenti fuori sede
    g = R[5]; ns = P["studenti"] if not pilota else 500; at = D["M11"]; atn = g.choice(at.index.values, ns, p=(at / at.sum()).values)
    st = pd.DataFrame(dict(origine="studente", tip=MONO, eta=0, dim=1, adulti=1, figli=0, minori=0, titolo="affitto", ateneo=atn, percettori=0,
                           lordo=0.0, netto=0.0, isee=np.nan, nil_i=-1))
    idon = g.random(ns) < P["q_dsu"]; fas = g.integers(0, 3, ns); st["idoneo_dsu"] = idon
    st["budget"] = np.where(idon, np.array(BORSA)[fas] / 12, np.exp(np.log(704) + 0.3 * g.standard_normal(ns)))
    st["in_residenza"] = False; st.loc[g.choice(ns, min(P["in_residenza"] if not pilota else 80, ns), replace=False), "in_residenza"] = True
    # 4.4 categorie, fascia grigia; 4.5 budget
    n["budget"] = 0.30 * n.netto / 12
    if P["budget"] == "residuo":
        ocse = 1 + 0.5 * (n.dim - n.minori - 1) + 0.3 * n.minori; n["budget"] = np.maximum(0, n.netto - 1256.37 * 12 * ocse) / 12
    gc = (n.tip == CSF) | (((n.tip == CCONV) & (n.dim == 2)) if P["giovani_coppie"] == "+conviventi" else False)  # [v2 C6]
    n["categoria"] = np.select([n.minori >= 1, (n.tip == MONO) & (n.eta >= 2), gc & (n.eta == 0), ((n.tip == MONO) & (n.eta == 0)) | (n.origine == "nuovo arrivo")],
                               CAT[1:5], CAT[5])
    n["isee_14_16"] = (n.isee >= 14000) & (n.isee <= 16000)
    n["fascia_grigia"] = (n.isee > 16000) & (12 * n.canone_mese > 0.30 * n.netto)
    for nome, c_ in (("omi", mid * mq), ("annunci", 23.3 * mq)):  # [v3, REVISIONE G1] stessa regola dello scenario S3, per entrambe le fonti dei canoni
        is_ = np.maximum(n.lordo - n.ded - np.where(aff, np.minimum(12 * c_, 7000), 0), 0) / n.dim.map(SCALA_ISEE)
        nt_ = n.netto_redditi + 12 * n.minori * auu_mese(is_.values); n[f"fascia_grigia_{nome}"] = (is_ > 16000) & (12 * c_ > 0.30 * nt_)
    st["categoria"] = CAT[0]; st["isee_14_16"] = False; st["fascia_grigia"] = False; st["fascia_grigia_omi"] = False; st["fascia_grigia_annunci"] = False
    n["sap"] = False
    if P["sap"] == "esclusi":  # 62.457 alloggi [S] tolti dagli affittuari residenti in proporzione agli affittuari del NIL [H]
        idx = np.flatnonzero(res & aff); sc = 62457 if not pilota else int(62457 * len(idx) / 231364)
        n.loc[g.choice(idx, min(sc, len(idx)), replace=False), "sap"] = True
    n["richiedente"] = ((n.titolo == "affitto") & ~n.sap) | (n.origine == "nuovo arrivo")
    st["richiedente"] = ~st.in_residenza
    n["nil"] = np.where(n.nil_i >= 0, D["NIL"][n.nil_i.clip(0)], -1)
    # 4.6 ancore
    anc = ancore(n, st, R[4], R[5])
    tutti = pd.concat([n, st], ignore_index=True); tutti.insert(0, "id", np.arange(len(tutti)))
    anc["id"] = anc.pos.map(dict(zip(range(len(tutti)), tutti.id))); anc = anc.drop(columns="pos")
    return tutti, anc, D, rep, P

def ancore(n, st, g, g2):
    G = geo(); out = []
    # lavoro: percettori non pensionati
    nl = n.percettori - np.where(n.pens_cf, np.where(n.tip.isin([CSF, CCF]), np.minimum(n.percettori, 2), 1), 0)
    nl = np.maximum(nl, 0); pos = np.repeat(np.arange(len(n)), nl); orig = n.sez2011.values[pos]
    od, ou = G["od"], G["ou"]; sz = G["sez"].set_index("SEZ"); cen = sz[["cx", "cy"]]
    oo = ou.assign(com=ou.com.str.upper()); oo = oo[oo.com.isin(G["com"])]
    tab = pd.concat([od[["so", "sd", "n"]].assign(fuori=False, com=""), oo[["so", "n", "com"]].assign(sd=-1, fuori=True)])
    tab = tab.groupby(["so", "sd", "com", "fuori"], as_index=False).n.sum()
    tutte = tab.groupby(["sd", "com", "fuori"], as_index=False).n.sum()  # margine cittadino delle destinazioni
    gr = {k: v for k, v in tab.groupby("so")}
    X = np.full(len(pos), np.nan); Y = X.copy(); F = np.zeros(len(pos), bool); arr = (n.origine.values[pos] == "nuovo arrivo")
    def sc(idx, t):
        k = g.choice(len(t), len(idx), p=(t.n / t.n.sum()).values); r = t.iloc[k]
        F[idx] = r.fuori.values; inn = ~r.fuori.values
        X[idx[inn]] = cen.cx.reindex(r.sd.values[inn]).values; Y[idx[inn]] = cen.cy.reindex(r.sd.values[inn]).values
        cc = np.array([G["com"][c] for c in r.com.values[~inn]]).reshape(-1, 2); X[idx[~inn]] = cc[:, 0]; Y[idx[~inn]] = cc[:, 1]
    df = pd.DataFrame(dict(o=orig, a=arr)); fb = []
    for o, idx in df[~df.a].groupby("o").groups.items():
        sc(np.asarray(idx), gr[o]) if o in gr else fb.append(np.asarray(idx))
    rest = np.concatenate(fb + [np.flatnonzero(arr | pd.isna(orig))]) if (fb or arr.any()) else np.array([], int)
    rest = np.unique(rest)
    if len(rest): sc(rest, tutte)  # nuovi arrivati e sezioni senza flussi: margine cittadino [H 4.6; dettaglio a registro]
    out.append(pd.DataFrame(dict(pos=pos, tipo="lavoro", x=X, y=Y, fuori_milano=F)))
    # scuola: ogni minore, servizio del livello piu' vicino
    pm = np.repeat(np.arange(len(n)), n.minori); eta_m = g.integers(0, 18, len(pm))
    liv = np.select([eta_m <= 2, eta_m <= 5, eta_m <= 10, eta_m <= 13], ["nido", "infanzia", "primaria", "sec1"], "sec2")
    for l in np.unique(liv):
        m = liv == l; _, k = cKDTree(G["scuole"][l]).query(np.c_[n.x.values[pm[m]], n.y.values[pm[m]]])
        out.append(pd.DataFrame(dict(pos=pm[m], tipo="scuola_" + l, x=G["scuole"][l][k, 0], y=G["scuole"][l][k, 1], fuori_milano=False, eta_minore=eta_m[m])))
    # cura: nuclei con capofamiglia >= 65
    pc = np.flatnonzero(n.eta.values >= 2); _, k = cKDTree(G["mmg"]).query(np.c_[n.x.values[pc], n.y.values[pc]])
    out.append(pd.DataFrame(dict(pos=pc, tipo="cura", x=G["mmg"][k, 0], y=G["mmg"][k, 1], fuori_milano=False)))
    # universita': studenti
    ps = np.arange(len(st)) + len(n); xy = np.zeros((len(st), 2))
    for a in np.unique(st.ateneo):
        m = (st.ateneo == a).values; sd = G["sedi"][a]; xy[m] = sd[g2.integers(0, len(sd), m.sum())]
    out.append(pd.DataFrame(dict(pos=ps, tipo="universita", x=xy[:, 0], y=xy[:, 1], fuori_milano=False)))
    a = pd.concat(out, ignore_index=True)  # flag dalla geometria: alcuni ambulatori MMG stanno appena fuori dal confine [registro]
    a["fuori_milano"] = a.fuori_milano.values | ~gpd.GeoSeries(gpd.points_from_xy(a.x, a.y), crs=CRS).within(G["conf"].buffer(1.0)).values
    return a

# ------------------------------------------------------------------ criteri P1, P2, P5
def err_margine(nome, sim, obi, livello):
    sim, obi = np.asarray(sim, float).ravel(), np.asarray(obi, float).ravel(); d = sim - obi; N = obi.sum()
    big = obi >= 100
    return dict(margine=nome, livello=livello, celle=len(obi), obiettivo_tot=N, TAE=np.abs(d).sum(), TAE_N=np.abs(d).sum() / N,
                err_rel_max_celle100=(np.abs(d[big]) / obi[big]).max() if big.any() else np.nan,
                err_abs_max_celle_lt100=np.abs(d[~big]).max() if (~big).any() else np.nan,
                SRMSE=np.sqrt(np.mean(d ** 2)) / obi.mean() if obi.mean() else np.nan)

def p1(t, D, rep):
    r = t[t.origine == "residente"]; K = len(D["NIL"]); out = []
    nta = np.zeros((K, 8, 4)); np.add.at(nta, (r.nil_i, r.tip, r.eta), 1)
    m0 = np.zeros((K, 4, 8, 5)); np.add.at(m0, (r.nil_i, r.eta, r.tip, r.dim - 1), 1)
    out.append(err_margine("M0 congiunta ds1441 NIL x eta x tipologia x componenti", m0, D["M0"], "NIL"))  # [v2 P1-0]
    out.append(err_margine("M1 NIL x tipologia", nta.sum(2), D["M1"], "NIL"))
    out.append(err_margine("M2 tipologia x eta", nta.sum(0), D["M2"], "citta"))
    out.append(err_margine("M3a soli >=65 per NIL", nta[:, MONO, 2:].sum(1), D["M3a"], "NIL"))
    out.append(err_margine("M3b capofamiglia <35 per NIL", nta[:, :, 0].sum(1), D["M3b"], "NIL"))
    out.append(err_margine("M4 componenti", np.bincount(r.dim - 1, minlength=5), D["M4"], "citta"))
    Nn = np.bincount(r.nil_i, minlength=K)
    out.append(err_margine("M5a con minori per NIL (quote condizionate ds139 2021)", np.bincount(r.nil_i[r.minori > 0], minlength=K), rep["M5a_target"], "NIL"))
    out.append(err_margine("M5b monogenitori con minori per NIL", np.bincount(r.nil_i[(r.minori > 0) & (r.tip == MG)], minlength=K), rep["M5b_target"], "NIL"))
    out.append(err_margine("M6 totale minori", [r.minori.sum()], [D["M6"]], "citta"))
    lab = ["affitto", "proprieta", "altro"]; ct = np.array([(r.titolo == l).sum() for l in lab])
    out.append(err_margine("M7 titolo (citta)", ct, D["M7"] * len(r), "citta"))
    tn = np.zeros((K, 3)); np.add.at(tn, (r.nil_i, r.titolo.map({l: i for i, l in enumerate(lab)})), 1)
    out.append(err_margine("M8 titolo per NIL (2011 riscalato)", tn, rep["TT"], "NIL"))
    out.append(err_margine("M9 classi MEF (percettori)", rep["M9_sim"], D["M9"] * rep["M9_sim"].sum() / D["M9"].sum(), "citta"))
    out.append(err_margine("P1c totale residenti", [len(r)], [D["M1"].sum()], "citta"))
    e = pd.DataFrame(out)
    soglia = {"M0": 0, "M2": .005, "M4": .005, "M6": .005, "M7": .005, "M9": .01, "M1": .01, "M3a": .01, "M3b": .01, "M5a": .01, "M5b": .01, "M8": .01, "P1c": 0}
    e["soglia_TAE_N"] = e.margine.str.split().str[0].map(soglia)
    e["passa"] = (e.TAE_N <= e.soglia_TAE_N + 1e-12) & ((e.livello != "NIL") | (((e.err_rel_max_celle100.fillna(0) <= .05)) & (e.err_abs_max_celle_lt100.fillna(0) <= 10)))
    return e

def p2(t, anc, tol_netto=0.0):  # tol_netto: solo per i file arrotondati a 2 decimali (test)
    G = geo(); r = t[t.origine != "studente"]; c = {}
    c["NIL valido"] = r.nil.isin(carica_nil()).all()
    c["categoria/titolo/dim"] = t.categoria.notna().all() and t.titolo.notna().all() and (t.dim >= 1).all()
    c["dim 1 <=> tipologia Monocomponente o In convivenza"] = (r.tip.isin([MONO, INCONV]) == (r.dim == 1)).all()  # [v2 P2]
    rr_ = r[r.origine == "residente"]; m0 = np.zeros_like(carica()["M0"]); np.add.at(m0, (np.searchsorted(carica_nil(), rr_.nil), rr_.eta, rr_.tip, rr_.dim - 1), 1)
    c["congiunta residenti = M0 cella per cella"] = bool((m0 == carica()["M0"]).all())
    a = r[r.categoria == CAT[2]]; c["anziani soli: dim 1, eta >= 65"] = ((a.dim == 1) & (a.eta >= 2)).all()
    f = t[t.categoria == CAT[1]]; c["famiglie con minori: >=1 minore, dim >=2"] = ((f.minori >= 1) & (f.dim >= 2)).all()
    c["minori <= dim-1"] = (t.minori <= t.dim - 1).all()
    c["netto >= 0"] = (t.netto >= 0).all(); c["isee >= 0"] = (r.isee >= 0).all()
    c["budget > 0 se reddito > 0"] = (t.budget[t.netto > tol_netto] > 0).all() and (t.budget[t.origine == "studente"] > 0).all()
    cnt = anc.groupby(["id", "tipo"]).size().unstack(fill_value=0)
    sc = cnt[[k for k in cnt.columns if k.startswith("scuola")]].sum(axis=1).reindex(t.id, fill_value=0).values
    c["minori -> >=1 ancora scuola"] = (sc[t.minori.values > 0] >= 1).all()
    c["studente -> 1 ancora universita"] = (cnt.get("universita", pd.Series(0, index=cnt.index)).reindex(t.id, fill_value=0).values[(t.origine == "studente").values] == 1).all()
    nl = cnt.get("lavoro", pd.Series(0, index=cnt.index)).reindex(t.id, fill_value=0).values
    att = (t.percettori - np.where(t.eta >= 2, np.where(t.tip.isin([CSF, CCF]), np.minimum(t.percettori, 2), 1), 0)).clip(lower=0).values
    c["percettore non pensionato -> 1 ancora lavoro"] = (nl == att).all()
    c["coordinate valide"] = anc[["x", "y"]].notna().all().all() and np.isfinite(anc[["x", "y"]].values).all()
    dentro = gpd.GeoSeries(gpd.points_from_xy(anc.x, anc.y), crs=CRS).within(G["conf"].buffer(1.0)).values
    c["ancore non 'fuori Milano' dentro il confine"] = bool(dentro[~anc.fuori_milano.values].all())
    rd = gpd.GeoSeries(gpd.points_from_xy(r.x, r.y), crs=CRS).within(G["conf"].buffer(1.0)).values; c["residenza dentro il confine"] = bool(rd.all())
    c["studenti e arrivi marcati"] = set(t.origine) <= {"residente", "nuovo arrivo", "studente"}
    c["nessun campo da LLM"] = True  # nessuna chiamata a modelli linguistici nel codice
    return {k: bool(v) for k, v in c.items()}, dict(ancore_fuori_confine=int((~dentro[~anc.fuori_milano.values]).sum()), residenze_fuori=int((~rd).sum()))

def carica_nil():
    return carica()["NIL"]

# generatori G1/G2/G3 su 5 criteri astratti e 50 lotti sintetici (non Base L) [4.7]
def generatori(t, seme=SEME, n_lotti=50, k=5):
    ss = np.random.SeedSequence(seme).spawn(9); g1, g2, g3 = (np.random.default_rng(ss[i]) for i in (6, 7, 8))
    N = len(t); Xl = np.random.default_rng(np.random.SeedSequence(seme).spawn(10)[9]).random((n_lotti, k)); s_own = np.random.default_rng(seme + 99).random(n_lotti)
    a = np.ones((N, k)); a[t.categoria.isin([CAT[1], CAT[2]]).values, 0] = 2.0  # criterio 0 = vicinanza alle ancore
    W1 = np.array([g1.dirichlet(r) for r in a]); A1 = np.exp(0.5 * g1.standard_normal(N)); L1 = np.exp(0.5 * g1.standard_normal(N))
    U1 = W1 @ Xl.T
    tipo = g2.integers(0, 5, N); W2 = g2.dirichlet(np.ones(k), N); U = W2 @ Xl.T
    kd = g2.integers(0, k, N); xk = Xl[:, kd].T
    U2 = U.copy()
    m = tipo == 0; U2[m] = 10 * np.floor(3 * xk[m]) + Xl[:, 1][None, :]  # lessicografiche (3 livelli, poi criterio 1 = budget) [H]
    m = tipo == 1; U2[m] = 0.3 * U[m] + 0.7 * s_own[None, :]  # omofile: quota della propria categoria sul lotto, non vista
    m = tipo == 2; xs = g2.uniform(0.3, 0.7, m.sum()); U2[m] = -np.abs(Xl[:, k - 1][None, :] - xs[:, None]) + 0.01 * Xl[:, 1][None, :]  # [v2 C5] punto ideale
    m = tipo == 3; thr = g2.uniform(0.3, 0.7, m.sum()); U2[m] = np.where(Xl[:, 0][None, :] < thr[:, None], -10 + U[m], U[m])  # soglia sulle ancore
    m = tipo == 4; Z = (U[m] - U[m].mean(1, keepdims=True)) / U[m].std(1, keepdims=True); U2[m] = Z + g2.standard_normal(Z.shape)  # rumore sd 1
    dich = np.clip(W2 + 0.1 * g2.standard_normal(W2.shape), 0, None); strat = g2.random(N) < 0.1
    dich[strat, W2[strat].argmax(1)] *= 2; dich /= dich.sum(1, keepdims=True)
    W3 = g3.dirichlet(np.ones(k), N); A3 = np.exp(g3.standard_normal(N)); L3 = np.exp(g3.standard_normal(N))
    S01 = W3 + 0.1 * g3.standard_normal(W3.shape); S03 = W3 + 0.3 * g3.standard_normal(W3.shape)
    return dict(Xl=Xl, U1=U1, U2=U2, tipo2=tipo, W1=W1, A1=A1, L1=L1, W2=W2, dich2=dich, strat2=strat, W3=W3, A3=A3, L3=L3, S01=S01, S03=S03)

def tau_additivo(U, Xl, chunk=20000):
    Xc = np.c_[Xl, np.ones(len(Xl))]; Pm = np.linalg.pinv(Xc); iu = np.triu_indices(len(Xl), 1); out = []
    for s in range(0, len(U), chunk):
        u = U[s:s + chunk]; fit = (Pm @ u.T).T @ Xc.T
        a = np.sign(u[:, iu[0]] - u[:, iu[1]]); b = np.sign(fit[:, iu[0]] - fit[:, iu[1]]); out.append((a * b).sum(1) / len(iu[0]))
    return np.concatenate(out)

def p5(t, seme=SEME, scrivi=False):
    r = t[t.richiedente].reset_index(drop=True); G = generatori(r, seme)
    t1 = tau_additivo(G["U1"], G["Xl"]); t2 = tau_additivo(G["U2"], G["Xl"])
    res = dict(n=len(r), G1_tau_mediana=float(np.median(t1)), P5a=bool(np.median(t1) >= 0.95), G2_quota_tau_le_080=float((t2 <= 0.80).mean()),
               P5b=bool((t2 <= 0.80).mean() >= 0.5), G2_quota_per_tipo={n_: float((t2[G["tipo2"] == i] <= .8).mean()) for i, n_ in enumerate(["lessicografiche", "omofile", "polarizzate", "soglia", "rumore"])})
    vero = pd.DataFrame(np.c_[r.id, G["W3"], G["A3"], G["L3"]], columns=["id"] + [f"w{j}" for j in range(5)] + ["alfa", "lambda"])
    b = vero.to_csv(index=False, float_format="%.10g").encode(); res["G3_sha256_veri"] = hashlib.sha256(b).hexdigest()
    res["P5c"] = bool((np.abs(G["S01"] - G["W3"]).sum(1) > 0).all() and (np.abs(G["S03"] - G["W3"]).sum(1) > 0).all())
    if scrivi:
        os.makedirs(OUT, exist_ok=True); open(os.path.join(OUT, "G3_veri_astratti.csv"), "wb").write(b)
        open(os.path.join(TAB, "G3_veri_astratti.sha256"), "w").write(res["G3_sha256_veri"] + "  G3_veri_astratti.csv (in _cache/P_popolazione/out)\n")
    return res

def hash_contenuto(t, anc):
    a = t.sort_values("id").to_csv(index=False, float_format="%.6f").encode(); b = anc.sort_values(["id", "tipo", "x", "y"]).to_csv(index=False, float_format="%.3f").encode()
    return hashlib.sha256(a + b).hexdigest()

COL = ["id", "origine", "nil", "categoria", "isee_14_16", "fascia_grigia", "richiedente", "tip", "eta", "dim", "adulti", "minori", "titolo", "sap",
       "percettori", "lordo", "netto", "isee", "canone_mese", "mq", "budget", "zona_omi", "x", "y", "ateneo", "idoneo_dsu", "in_residenza"]

EXTRA = ["fascia_grigia_omi", "fascia_grigia_annunci"]  # [v3] fuori dall'hash di contenuto (l'hash della base resta quello pre-esistente)

def riassunto(t):
    c = t.groupby("categoria").size().reindex(CAT, fill_value=0); q = t[t.richiedente].groupby("categoria").size().reindex(CAT, fill_value=0)
    rq = t[t.richiedente]
    return pd.DataFrame(dict(tutti=c, richiedenti=q, fascia_grigia_quota_rich=rq.groupby("categoria").fascia_grigia.mean().reindex(CAT),
                             isee_14_16_quota_rich=rq.groupby("categoria").isee_14_16.mean().reindex(CAT),
                             budget_mediano_rich=rq.groupby("categoria").budget.median().reindex(CAT),
                             **{f"rich_{e}": rq.groupby("categoria")[e].sum().reindex(CAT, fill_value=0) for e in EXTRA if e in t.columns}))

def esegui(seme=SEME, pilota=False, scenario="base", scrivi=False, con_hash=True):
    t, anc, D, rep, P = genera(seme, pilota, **SCENARI[scenario]); t["tip"] = t.tip.astype(int)
    t = t[[c for c in COL + EXTRA if c in t.columns]]; h = hash_contenuto(t[[c for c in COL if c in t.columns]], anc) if con_hash else None
    out = dict(seme=seme, scenario=scenario, pilota=pilota, hash_contenuto=h, n=len(t), rep={k: v for k, v in rep.items() if k not in ("TT", "M9_sim", "M5a_target", "M5b_target")})
    if not pilota:
        e = p1(t.assign(nil_i=pd.Series(np.searchsorted(D["NIL"], t.nil)).where(t.nil >= 0, -1)), D, rep); out["P1_passa"] = bool(e.passa.all())
        out["P1"] = e
    out["riassunto"] = riassunto(t)
    if scrivi:
        os.makedirs(OUT, exist_ok=True); os.makedirs(TAB, exist_ok=True)
        t.to_csv(os.path.join(OUT, f"nuclei_{scenario}_{seme}.csv.gz"), index=False, float_format="%.2f")
        anc.to_csv(os.path.join(OUT, f"ancore_{scenario}_{seme}.csv.gz"), index=False, float_format="%.1f")
        out["t"], out["anc"], out["D"], out["rep_full"] = t, anc, D, rep
    return out

def main(a):
    if a[0] == "controlla": sys.exit(0 if controlla() else 1)
    seme = int(a[a.index("--seme") + 1]) if "--seme" in a else SEME; sc = a[a.index("--scenario") + 1] if "--scenario" in a else "base"
    if a[0] == "esegui":
        o = esegui(seme, "--pilota" in a, sc, "--scrivi" in a)
        print(json.dumps({k: v for k, v in o.items() if k not in ("P1", "riassunto", "t", "anc", "D", "rep_full")}, default=str, indent=1))
        if "P1" in o: print(o["P1"].to_string())
        print(o["riassunto"].to_string())
        if "--scrivi" in a and sc == "base": completa(o)
        if "--scrivi" in a and sc != "base":  # [v3] popolazione di scenario (es. S5): richiedenti nel repo, popolazione completa in cache
            o["t"][o["t"].richiedente].to_csv(os.path.join(TAB, f"richiedenti_{sc}.csv.gz"), index=False, float_format="%.2f")
            o["riassunto"].to_csv(os.path.join(TAB, f"categorie_{sc}.csv"))
    if a[0] == "robustezza": robustezza()
    if a[0] == "sensibilita": sensibilita()

def completa(o):
    t, anc, D, rep = o["t"], o["anc"], o["D"], o["rep_full"]
    o["P1"].to_csv(os.path.join(TAB, "P1_errore_margini.csv"), index=False)
    c2, info = p2(t, anc); r5 = p5(t, o["seme"], scrivi=True)
    o["riassunto"].to_csv(os.path.join(TAB, "categorie_base.csv"))
    # [v2] informativo: quota con minori per NIL, 2025 simulato contro ds139 2021
    r = t[t.origine == "residente"]; K = len(D["NIL"]); Nn = np.bincount(np.searchsorted(D["NIL"], r.nil), minlength=K)
    q25 = np.bincount(np.searchsorted(D["NIL"], r.nil[r.minori > 0]), minlength=K) / Nn
    inf = pd.DataFrame(dict(nil=D["NIL"], famiglie_2025=Nn, quota_minori_2025_sim=q25, quota_minori_2021_ds139=D["M5"][0]))
    inf.to_csv(os.path.join(TAB, "info_minori_2025_vs_2021.csv"), index=False)
    info_vero = [dict(spearman=float(inf.quota_minori_2025_sim.corr(inf.quota_minori_2021_ds139, method="spearman")),
                      scarto_ass_max=float((inf.quota_minori_2025_sim - inf.quota_minori_2021_ds139).abs().max()), citta_2025=float((r.minori > 0).mean()),
                      ripiego_RC=rep["ripiego_RC"], ripiego_RM=rep["ripiego_RM"])]
    a_ = t[t.origine == "nuovo arrivo"]; pd.crosstab(a_.tip.map(dict(enumerate(TIP))), a_.dim).to_csv(os.path.join(TAB, "info_arrivi_tipologia_componenti.csv"))
    ric = t[t.richiedente]; ric.to_csv(os.path.join(TAB, "richiedenti_base.csv.gz"), index=False, float_format="%.2f")
    anc[anc.id.isin(ric.id)].to_csv(os.path.join(TAB, "ancore_richiedenti_base.csv.gz"), index=False, float_format="%.1f")
    esito = dict(seme=o["seme"], hash_contenuto=o["hash_contenuto"], P1_passa=o["P1_passa"], P2=c2, P2_info=info, P5=r5, rep=o["rep"],
                 info_minori=info_vero)
    json.dump(esito, open(os.path.join(TAB, "esito_base.json"), "w"), indent=1, default=str)
    print(json.dumps(esito, indent=1, default=str))

def robustezza():
    righe = []; h = []
    for s in [SEME, SEME] + [SEME + k for k in range(1, 11)]:
        o = esegui(s); h.append(o["hash_contenuto"]); rq = o["riassunto"].richiedenti
        righe.append(dict(seme=s, hash=o["hash_contenuto"], P1_passa=o["P1_passa"], P1_falliti=";".join(o["P1"][~o["P1"].passa].margine), **{f"rich_{c}": rq[c] for c in CAT}))
        print(s, o["hash_contenuto"][:12], o["P1_passa"], flush=True)
    d = pd.DataFrame(righe); d.to_csv(os.path.join(TAB, "P3_robustezza.csv"), index=False)
    r10 = d.iloc[2:]; cv = {c: float(r10[f"rich_{c}"].std() / r10[f"rich_{c}"].mean()) for c in CAT if r10[f"rich_{c}"].mean() >= 1000}
    res = dict(stesso_hash=h[0] == h[1], P1_tutti_10_semi=bool(r10.P1_passa.all()), cv=cv, P3_cv_ok=all(v <= 0.02 for v in cv.values()))
    json.dump(res, open(os.path.join(TAB, "P3_esito.json"), "w"), indent=1); print(res)

def sensibilita():
    righe = []
    for sc in SCENARI:
        o = esegui(SEME, scenario=sc, con_hash=False); r = o["riassunto"]
        for c in CAT: righe.append(dict(scenario=sc, categoria=c, **r.loc[c].to_dict()))
        print(sc, flush=True)
    d = pd.DataFrame(righe); b = d[d.scenario == "base"].set_index("categoria").richiedenti
    d["rapporto_su_base"] = d.richiedenti / d.categoria.map(b); d.to_csv(os.path.join(TAB, "P6_sensibilita.csv"), index=False)
    f = d[(d.rapporto_su_base > 2) | (d.rapporto_su_base < 0.5)]; print(f.to_string()); print(d.pivot(index="categoria", columns="scenario", values="richiedenti").to_string())

if __name__ == "__main__":
    main(sys.argv[1:])
