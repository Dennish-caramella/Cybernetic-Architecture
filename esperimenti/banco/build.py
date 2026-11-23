"""Banco di laboratorio (ticket #17): Base L v7 + NIL + Base E v2 -> banco.html (autonomo, Leaflet da cdnjs).
Uso: python build.py   (legge solo file del repo e la cache NIL; scrive solo banco.html qui)."""
import hashlib, json, os
import geopandas as gpd, numpy as np, pandas as pd

H = os.path.dirname(os.path.abspath(__file__)); E = os.path.dirname(H)
L7, E2 = os.path.join(E, "L_lotti_v7"), os.path.join(E, "E_economia_v2")
NIL = os.path.join(E, "_cache", "L_lotti", "raw", "ds964_nil.geojson")
NIL_URL = ("https://dati.comune.milano.it/dataset/e8e765fc-d882-40b8-95d8-16ff3d39eb7c/resource/"
           "9c4e0776-56fc-4f3d-8a90-f4992a3be426/download/ds964_nil_wm.geojson")
TOL_LOTTI, TOL_NIL = 1.0, 10.0  # m, semplificazione [H]
SHA = {  # VERSIONE.md Base L v7; esito_criteri.json Base E v2 (hash_tabelle_nuove); NIL: letto il 2026-11-23
    os.path.join(L7, "lotti_v7.gpkg"): "5d464a3c9b3ac195c8f6a3146cff1a5619445a71250c2a9d9f11ab53768d22ac",
    os.path.join(L7, "tabelle", "scenari_capacita.csv"): "998bf5d35b92f9b54c4093bc0ca92c04b3f6ece2ef1dbc4d966fba87779d7f97",
    os.path.join(E2, "tabelle", "c_star_per_regione.csv"): "0c44a0f4241cea068aab124d3eb84625560ef23a55ab3a8d84a176913e457d15",
    NIL: "780dfb9b3d18b11fd905e53c7faf634c2fdde76d057362da47e41505b66ccd4d",
}
E_SENZA_RIF = [os.path.join(E2, "tabelle", f) for f in ("lotti_omi.csv", "delta_L_lotti.csv.gz")]  # Base E v2 non congelata


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


if not os.path.exists(NIL):
    raise SystemExit(f"manca {NIL}: scaricarlo da {NIL_URL}")
for p, h in SHA.items():
    if sha(p) != h:
        raise SystemExit(f"SHA-256 diverso dal riferimento: {p}")
hashes = {os.path.relpath(p, E): sha(p) for p in [*SHA, *E_SENZA_RIF]}

# ---- Base L v7
L = gpd.read_file(os.path.join(L7, "lotti_v7.gpkg"), layer="lotti")
CL = {"lotto edificabile": "E", "lotto da riusare": "R", "area di attivazione": "A", "edificabile per destinazione, non verificato": "G"}
L["k"] = L.classe.map(CL)
n = L.k.value_counts().to_dict()
assert len(L) == 701 and n == {"A": 268, "E": 216, "R": 167, "G": 50}, n
cap = {k: [int(L.loc[L.k == k, c].sum()) for c in ("cap_far05", "cap_far1", "cap_far2")] for k in "ERAG"}
assert cap["E"] == [16389, 32885, 65885] and cap["R"] == [672, 1429, 2938] and cap["A"] == cap["G"] == [0, 0, 0], cap
assert int(L.cap_recupero.fillna(0)[L.k == "R"].sum()) == 2898
sc = pd.read_csv(os.path.join(L7, "tabelle", "scenari_capacita.csv"))
assert sc.iloc[0][["far05", "far1", "far2"]].tolist() == cap["E"]
gfu = sc[sc.classi == "lotti edificabili"].iloc[1:]  # scenari (ii) e (iii)
gs = [int(L.loc[(L.k == "G") & (L.classe_se_verificata == "lotto edificabile"), c].sum()) for c in ("cap_scen_far05", "cap_scen_far1", "cap_scen_far2")]
assert [a + b for a, b in zip(cap["E"], gs)] == gfu.iloc[1][["far05", "far1", "far2"]].tolist()

# ---- Base E v2 (solo lotti edificabili e da riusare; acquisto solo fasce B, C, D: REPORT E v2 §8, E7)
omi = pd.read_csv(os.path.join(E2, "tabelle", "lotti_omi.csv")).set_index("id")
D = pd.read_csv(os.path.join(E2, "tabelle", "delta_L_lotti.csv.gz"))
D = D[(D.c0 == 90) & (D.VF == "0") & ((D.FAR == 1) | (D.variante == "R1"))]
A60 = D[(D.regime == "acq") & (D["T"] == 60)]
eco = {}
for r in A60.itertuples():
    if r.fascia not in "BCD":
        continue
    eco.setdefault(r.id, {})[r.variante] = [round(r.cstar_Lmkt_q05), round(r.cstar_Lmkt_q50), round(r.cstar_Lmkt_q95), round(r.quota_cal, 3)]
ces = {}
for T in (60, 90):  # cessione, nuovo: uguale per tutti i lotti (lato cooperativa senza geografia)
    c = D[(D.regime == "ces") & (D["T"] == T) & (D.variante == "nuovo")]
    cols = ["quota_cal", "quota_rov", "quota_S0", "quota_S1", "quota_S2", "quota_S3"]
    assert (c[cols].nunique() == 1).all(), "quota di cessione non uniforme"
    ces[T] = [round(float(c[x].iloc[0]), 3) for x in cols]
cs = pd.read_csv(os.path.join(E2, "tabelle", "c_star_per_regione.csv"))
cs = cs[cs.variante == "nuovo"]
cstar = [[int(r.T), r.regione.split(" (")[0], round(r.cstar_q05), round(r.cstar_q50), round(r.cstar_q95)] for r in cs.itertuples()]

# ---- geometrie
def gj(g, tol, nd):
    g = g.to_crs(32632).simplify(tol, preserve_topology=True).to_crs(4326)
    return [json.loads(gpd.GeoSeries([x]).to_json(drop_id=True))["features"][0]["geometry"] for x in g.set_precision(10 ** -nd)]

S = lambda v: None if v is None or (isinstance(v, float) and np.isnan(v)) or v == "" else v
F = ["id", "k", "area_m2", "cap_far05", "cap_far1", "cap_far2", "cap_recupero", "cap_scen_far05", "cap_scen_far1", "cap_scen_far2",
     "cap_scen_recupero", "scenario_principale", "origine", "nota", "nil_id", "nil_nome", "ambito_pgt", "codice_pgt", "gruppo_ambito", "strumento",
     "data_ambito", "fonte_ambito", "residenza_2030", "stato_riferimento", "marca_stato_riferimento", "fonte_stato_c1", "proprieta",
     "proprieta_conflitto", "vincoli_noti", "potenziale_vuoto", "verifica_destinazione", "classe_se_verificata", "fonti", "licenze"]
lotti = []
for (_, r), g in zip(L.iterrows(), gj(L.geometry, TOL_LOTTI, 6)):
    p = {f: S(r[f].item() if hasattr(r[f], "item") else r[f]) for f in F}
    p["area_m2"] = round(p["area_m2"])
    if r.id in omi.index:
        p["omi"] = f"{omi.at[r.id, 'zona']} (fascia {omi.at[r.id, 'fascia']})"
    if r.k in "ER":
        p["eco"] = eco.get(r.id)
    lotti.append({"type": "Feature", "properties": {k: v for k, v in p.items() if v is not None}, "geometry": g})
N = gpd.read_file(NIL)
assert len(N) == 88
nil = [{"type": "Feature", "properties": {"id": int(i), "n": s}, "geometry": g} for i, s, g in zip(N.ID_NIL, N.NIL, gj(N.geometry, TOL_NIL, 5))]

data = {"lotti": {"type": "FeatureCollection", "features": lotti}, "nil": {"type": "FeatureCollection", "features": nil},
        "tot": {"n": n, "cap": cap, "cap_rec_R": 2898, "gfu_scen": gfu[["scenario", "far05", "far1", "far2"]].values.tolist()},
        "ces": ces, "cstar": cstar, "sha": hashes, "tol": [TOL_LOTTI, TOL_NIL], "nil_url": NIL_URL}
js = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
src = open(os.path.join(H, "banco.src.html"), encoding="utf-8").read()
src = src.replace("/*LEAFLET_CSS*/", open(os.path.join(H, "leaflet-1.9.4.min.css"), encoding="utf-8").read().replace("url(images/", "url(https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/"))  # il visualizzatore degli artifact blocca i fogli di stile esterni (SRI verificato al download)
open(os.path.join(H, "banco.html"), "w", encoding="utf-8").write(src.replace("/*__DATA__*/null", js))
print("banco.html", os.path.getsize(os.path.join(H, "banco.html")), "byte;", n, cap["E"])
