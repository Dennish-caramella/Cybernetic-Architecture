"""Banco di laboratorio (ticket #17): pagina dello Spatial Milano Lab + lotti della Base L v7 + Base E v2 -> banco.html (autonoma).
Uso: python build.py   (legge solo file del repo; scrive solo banco.html qui). Versione Leaflet precedente in archivio/."""
import hashlib, json, math, os
import geopandas as gpd, numpy as np, pandas as pd

H = os.path.dirname(os.path.abspath(__file__)); E = os.path.dirname(H); R = os.path.dirname(E)
LAB = os.path.join(R, "prove", "in_evidenza", "2026-10-25_spatial_milano_lab")
L7, E2 = os.path.join(E, "L_lotti_v7"), os.path.join(E, "E_economia_v2")
PAGE = os.path.join(LAB, "lab_completo", "prototype", "site", "spatial-milano-lab.html")
TOL = 1.0  # m, semplificazione dei lotti [H]
SHA = {  # Lab: INVENTARIO_SCRATCH.txt; Base L v7 e Base E v2: VERSIONE.md
    PAGE: "ec22113278077d3035b473099776459d68acd390f9dbf8b924d33f38577cd188",
    os.path.join(LAB, "recuperati_da_artifact", "dusaf.json"): "3a0a12ecce1cc12313068f94bfadf08f4e4827ae93dd6a720e2d3a2912386c58",
    os.path.join(LAB, "recuperati_da_artifact", "pgt.json"): "6a2826113a1673f75addefc6e2f14d4fd2faf9af94bbfa1cc0b831e408641d81",
    os.path.join(L7, "lotti_v7.gpkg"): "5d464a3c9b3ac195c8f6a3146cff1a5619445a71250c2a9d9f11ab53768d22ac",
    os.path.join(L7, "tabelle", "scenari_capacita.csv"): "998bf5d35b92f9b54c4093bc0ca92c04b3f6ece2ef1dbc4d966fba87779d7f97",
    os.path.join(E2, "tabelle", "c_star_per_regione.csv"): "0c44a0f4241cea068aab124d3eb84625560ef23a55ab3a8d84a176913e457d15",
    os.path.join(E2, "tabelle", "lotti_omi.csv"): "135d2fef9ab634b11473d89e0401dd54ac650751fb70c03a15255d24d2d46102",
    os.path.join(E2, "tabelle", "delta_L_lotti.csv.gz"): "97a129ceab96c8536bdfffcab7b36010a29cb2c0974aa12496ab01bdabc7f883",
}
for p, h in SHA.items():
    if hashlib.sha256(open(p, "rb").read()).hexdigest() != h:
        raise SystemExit(f"SHA-256 diverso dal riferimento: {p}")

# ---- Base L v7
L = gpd.read_file(os.path.join(L7, "lotti_v7.gpkg"), layer="lotti")
L["k"] = L.classe.map({"lotto edificabile": "E", "lotto da riusare": "R", "area di attivazione": "A", "edificabile per destinazione, non verificato": "G"})
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

# ---- Base E v2 (lotti edificabili e da riusare; acquisto solo fasce B, C, D: REPORT E v2 §8, E7)
omi = pd.read_csv(os.path.join(E2, "tabelle", "lotti_omi.csv")).set_index("id")
D = pd.read_csv(os.path.join(E2, "tabelle", "delta_L_lotti.csv.gz"))
D = D[(D.c0 == 90) & (D.VF == "0") & ((D.FAR == 1) | (D.variante == "R1"))]
eco = {}
for r in D[(D.regime == "acq") & (D["T"] == 60)].itertuples():
    if r.fascia in "BCD":
        eco.setdefault(r.id, {})[r.variante] = [round(r.cstar_Lmkt_q05), round(r.cstar_Lmkt_q50), round(r.cstar_Lmkt_q95), round(r.quota_cal, 3)]
ces, cols = {}, ["quota_cal", "quota_rov", "quota_S0", "quota_S1", "quota_S2", "quota_S3"]
for T in (60, 90):  # cessione, nuovo: uguale per tutti i lotti (lato cooperativa senza geografia)
    c = D[(D.regime == "ces") & (D["T"] == T) & (D.variante == "nuovo")]
    assert (c[cols].nunique() == 1).all(), "quota di cessione non uniforme"
    ces[T] = [round(float(c[x].iloc[0]), 3) for x in cols]
cs = pd.read_csv(os.path.join(E2, "tabelle", "c_star_per_regione.csv"))
cstar = [[int(r.T), r.regione.split(" (")[0], round(r.cstar_q05), round(r.cstar_q50), round(r.cstar_q95)] for r in cs[cs.variante == "nuovo"].itertuples()]

# ---- geometrie nel sistema del Lab (mi/build_mi.py: km locali da 9,19 E 45,465 N), codifica a delta come enc_ring, passo 1 m
LON0, LAT0 = 9.19, 45.465
KX, KY = 111.32 * math.cos(math.radians(LAT0)), 110.57
def enc(g):
    out = []
    for p in getattr(g, "geoms", [g]):
        for ring in [p.exterior, *p.interiors]:
            o, px, py = [], 0, 0
            for lon, lat in list(ring.coords)[:-1]:
                ix, iy = round((lon - LON0) * KX * 1000), round(-(lat - LAT0) * KY * 1000)
                o += [ix - px, iy - py]; px, py = ix, iy
            out.append(o)
    return out
G4 = L.geometry.simplify(TOL, preserve_topology=True).to_crs(4326)
S = lambda v: None if v is None or (isinstance(v, float) and np.isnan(v)) or v == "" else (v.item() if hasattr(v, "item") else v)
F = ["id", "k", "area_m2", "cap_far05", "cap_far1", "cap_far2", "cap_recupero", "cap_scen_far05", "cap_scen_far1", "cap_scen_far2",
     "cap_scen_recupero", "scenario_principale", "origine", "nota", "nil_id", "nil_nome", "ambito_pgt", "codice_pgt", "gruppo_ambito", "strumento",
     "data_ambito", "fonte_ambito", "residenza_2030", "stato_riferimento", "marca_stato_riferimento", "fonte_stato_c1", "proprieta",
     "proprieta_conflitto", "vincoli_noti", "potenziale_vuoto", "verifica_destinazione", "classe_se_verificata", "fonti", "licenze"]
lotti = []
for (_, r), g in zip(L.iterrows(), G4):
    p = {f: S(r[f]) for f in F}; p["area_m2"] = round(p["area_m2"])
    if r.id in omi.index: p["omi"] = f"{omi.at[r.id, 'zona']} (fascia {omi.at[r.id, 'fascia']})"
    if r.k in "ER" and r.id in eco: p["eco"] = eco[r.id]
    lotti.append({"p": {k: v for k, v in p.items() if v is not None}, "r": enc(g)})
BL = {"lotti": lotti, "tot": {"n": n, "cap": cap, "cap_rec_R": 2898, "gfu_scen": gfu[["scenario", "far05", "far1", "far2"]].values.tolist()},
      "ces": ces, "cstar": cstar, "tol": TOL, "sha": {os.path.relpath(p, R): h for p, h in SHA.items()}}
js = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))

# ---- pagina del Lab: sostituzioni puntuali (ognuna deve comparire una sola volta)
page = open(PAGE, encoding="utf-8").read()
lay = {k: json.load(open(os.path.join(LAB, "recuperati_da_artifact", f"{k}.json"), encoding="utf-8")) for k in ("dusaf", "pgt")}
CSS = open(os.path.join(H, "banco.css"), encoding="utf-8").read()
PATCH = [
    ("<title>Spatial Milano Lab</title>", "<title>Banco di laboratorio — Spatial Milano Lab + Base L v7</title>"),
    ("</style>", CSS + "</style>"),
    ('<g id="labsites" class="lyr off" aria-label="Siti candidati per social housing"></g>',
     '<g id="labsites" class="lyr off" aria-label="Siti candidati per social housing"></g>\n      <g id="lotti" class="lyr off" aria-label="Lotti della Base L v7"></g>'),
    ('<div class="lab" id="bLab" hidden></div>', '<div class="lab" id="bLab" hidden></div>\n        <div class="lab" id="bLotti" hidden></div>'),
    ("const MLAB = {", 'delete D.city; delete D.lab; delete D.pp; // fuori: edifici 3D (tasselli DBT non nel repo), modelli di analisi del Lab (DECISIONI 09/11)\n'
     'D.lotti = { t: "Base L v7: lotti", mode: "lotti", m: ["lcl"], lay: [] };\nconst LAYDATA = ' + js(lay) + ';\nconst MLAB = { lcl: "Classi",'),
    ('const LAYERS = { metro: "Metro", omi: "Zone OMI" };', 'const LAYERS = { metro: "Metro", omi: "Zone OMI", lotti: "Lotti Base L v7" };'),
    ("const lay = { metro: false, omi: false };", "const lay = { metro: false, omi: false, lotti: false };"),
    ("const d = await (await fetch(LAYERS_META[k].file)).json();", "const d = LAYDATA[k];"),
    ('labMode = mode === "lab";', 'labMode = mode === "lab", lotMode = mode === "lotti";'),
    ("const flat = choro || catMode || labMode,", "const flat = choro || catMode || labMode || lotMode,"),
    ('map.classList.toggle("lab-w", labMode);', 'map.classList.toggle("lab-w", labMode || lotMode);'),
    ('catMode || labMode ? "var(--land)"', 'catMode || labMode || lotMode ? "var(--land)"'),
    ('on("labsites", labMode);', 'on("labsites", labMode); on("lotti", lotMode || lay.lotti); show("bLotti", lotMode);'),
    ("else if (labMode) renderLab();", "else if (labMode) renderLab();\n  else if (lotMode) renderLotti();"),
    ('$("cityBtn").hidden = !(flat && sel >= 0);', '$("cityBtn").hidden = true;'),
    ("const TOOLS = () => [", "const TOOLS = () => TOOLS0().filter((t) => !/^(show_buildings|get_lab_audit|get_portfolio|get_site)$/.test(t.name));\nconst TOOLS0 = () => ["),
    ("In più c'è il <b>laboratorio</b> sui lotti per social housing e sul potere d'acquisto reale.",
     "In più c'è il <b>banco di laboratorio</b>: i lotti della Base L v7 con schede, filtri e Base E v2."),
    ("/* ---------- UI ---------- */", open(os.path.join(H, "lotti.js"), encoding="utf-8").read().replace("/*__BL__*/null", js(BL)) + "\n/* ---------- UI ---------- */"),
    ("\nreset();\n", '\nif (matchMedia("(prefers-color-scheme: light)").matches) { map.dataset.base = "light"; $("base").textContent = "LIGHT"; }\nreset();\ngo(9, null, null, true);\n'),
]
for a, b in PATCH:
    assert page.count(a) == 1, f"sostituzione non univoca: {a[:60]}"
    page = page.replace(a, b)
# righe del chat: niente strumenti né fasi del Lab rimossi
import re
page, k1 = re.subn(r"\nLaboratorio \(dashboard lab[^\n]*", "\nBase L v7 (dashboard lotti): 701 lotti in quattro classi; capacità come forbice; GFU non verificate; la Base E v2 non è un vincolo.", page)
page, k2 = re.subn(r" Per gli edifici di un quartiere usa show_buildings[^.]*\.", "", page)
page, k3 = re.subn(r"const lab = want \|\| [^\n]*", "const lab = /lott|base l|edificabil|riusa|attivazione|gfu|laborator|social housing/.test(lc) ? 9 : 0;", page)
page, k4 = re.subn(r"const want = [^\n]*", "const want = null;", page)
page, k5 = re.subn(r"const i = /edific\|altezz\|3d\.\*quart\|scendi/\.test\(lc\) \? 9 :", "const i = /edific|altezz|3d.*quart|scendi/.test(lc) ? 8 :", page)
assert (k1, k2, k3, k4, k5) == (1, 1, 1, 1, 1), (k1, k2, k3, k4, k5)
assert "fetch(" not in page.replace('fetch(`data/t/', "").replace('fetch("data/lab.json")', ""), "fetch inattesi"
out = os.path.join(H, "banco.html")
open(out, "w", encoding="utf-8").write(page)
print("banco.html", os.path.getsize(out), "byte;", n, cap["E"])
