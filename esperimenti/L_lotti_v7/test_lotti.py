"""Invarianti di lotti_v7.gpkg (file pubblicato) e del rifiuto di sovrascrivere i controlli. Uso: python test_lotti.py"""
import importlib.util, json, os, tempfile
import numpy as np, pandas as pd, geopandas as gpd, pyogrio, shapely

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "lotti_v7.gpkg")
L = gpd.read_file(F, layer="lotti"); TC = gpd.read_file(F, layer="tessuto_consolidato") if "tessuto_consolidato" in pyogrio.list_layers(F)[:, 0] else None
R, E, A, G = (L.classe == c for c in ("lotto da riusare", "lotto edificabile", "area di attivazione", "edificabile per destinazione, non verificato"))
assert L.crs.to_epsg() == 32632 and L.geometry.is_valid.all() and not L.geometry.is_empty.any()
assert L.id.is_unique and L.id.str.match(r"^[REAG]\d{5}$").all() and (R | E | A | G).all()
assert set(L.proprieta) <= {"pubblico comunale", "Demanio", "non agganciata"} and (L.area_m2 > 0).all() and L.nil_id.notna().all()
assert L.fonti.str.len().gt(0).all() and L.licenze.str.len().gt(0).all() and L.potenziale_vuoto.isin([0, 1]).all()
assert (L.area_m2[E] >= 1500).all() and (L.area_m2[A] >= 500).all()
# [v7] 1.3: classe GFU = esattamente i lotti in ambito GFU; capacita' della base 0, scenario con la formula sulla classe_se_verificata
gfu = (L.lotto_at == 1) & L.ambito_id.fillna("").str.startswith("GFU_"); sv = L.classe_se_verificata
assert (G == gfu).all() and (sv[~G] == L.classe[~G]).all() and sv[G].isin(["lotto da riusare", "lotto edificabile", "area di attivazione"]).all()
for f, c in ((0.5, "cap_far05"), (1.0, "cap_far1"), (2.0, "cap_far2")):
    base = ~A & ~G
    assert (L[c][base] == np.floor(0.70 * f * L.area_m2[base] / 80)).all() and (L[c][A | G] == 0).all()
    s = c.replace("cap_", "cap_scen_"); sg = G & (sv != "area di attivazione")
    assert (L[s][sg] == np.floor(0.70 * f * L.area_m2[sg] / 80)).all() and (L[s][~sg] == 0).all()
assert (L.cap_recupero[R] == np.floor(0.70 * L.volume_fonte_m3[R] / 3.2 / 80)).all() and L.cap_recupero[~R & ~G].isna().all() and (L.cap_recupero[G] == 0).all()
assert (L.cap_scen_recupero[G & (sv == "lotto da riusare")] == np.floor(0.70 * L.volume_fonte_m3[G & (sv == "lotto da riusare")] / 3.2 / 80)).all() and (L.cap_scen_recupero[~(G & (sv == "lotto da riusare"))] == 0).all()
assert (L.verifica_destinazione[G] != "").all() and L.verifica_destinazione[L.ambito_id == "GFU_5267"].str.startswith("da verificare").all()
assert (L.area_m2[R] <= L.area_v3_regola[R] + 1).all() and (L.area_intorno_5m[R] <= L.area_intorno_20m[R] + 1).all()
# [v6] D4 estesa ai lotti da riusare: nessun E o R, e nessuna capacita', in un ambito 2030 con residenza "no"
no = L.residenza_2030 == "no"
assert not (no & (E | R | G)).any() and (L.cap_far2[no] == 0).all()
assert ((L.lotto_at == 1) == (L.quota_at >= 0.5)).all() and L.ambito_id[L.lotto_at == 1].notna().all() and L.ambito_id.dropna().str.match(r"^(MA|ADP|GFU)_\d+$").all()
# [v6] stato come attributo: ogni lotto in ambito ha stato_c1/c2/riferimento e nessun lotto e' escluso per lo stato (D e N compresi, se presenti)
at = L.lotto_at == 1
assert (L.loc[at, ["stato_c1", "stato_c2", "stato_riferimento", "marca_stato_riferimento"]] != "").all().all() and set(L.stato_c1[at]) <= set("ABCDN")
# [v7] cantiere documentato: nessun lotto E/R/A nei poligoni della regola 1.5; il tessuto consolidato non contiene GFU
res = json.load(open(os.path.join(HERE, "esito_criteri.json"))); cs = set(res["tessuto_consolidato"]["poligoni"])
assert not (L.ambito_id.isin(cs) & at & ~G).any()
if TC is not None: assert set(TC.ambito_id) <= cs and TC.id.str.match(r"^T\d{5}$").all() and len(TC) == res["tessuto_consolidato"]["lotti"]
else: assert res["tessuto_consolidato"]["lotti"] == 0
g = L.geometry.values; i, j = shapely.STRtree(g).query(g, predicate="intersects"); k = i < j
assert (shapely.area(shapely.intersection(g[i[k]], g[j[k]], grid_size=0.01)) <= 1.0).all()
meta = pyogrio.read_dataframe(F, layer="metadati")
assert set(L.columns) - {"geometry"} <= set(meta.attributo) and meta.licenza.str.len().gt(0).all()
cas = pyogrio.read_dataframe(F, layer="cascata"); last = cas[cas.classe != "informativo"].groupby("classe").rimasti.last()
assert last["riuso"] == R.sum() and last["edificabile"] == E.sum() and last["attivazione"] == A.sum() and last["gfu"] == G.sum()
assert res["conteggi"] == L.classe.value_counts().to_dict()
amb = pd.read_csv(os.path.join(HERE, "tabelle", "ambiti_2030.csv"))
assert len(amb) == 29 and amb.ambito_id.is_unique and amb.residenza_2030.isin(["si", "no", "si [H]"]).all() and amb.fonte_ambito.str.startswith("http").all()
cov = pd.read_csv(os.path.join(HERE, "tabelle", "copertura_ambiti_2030.csv"))
assert len(cov) == len(amb) + 6 and (cov.pcu == 1).sum() == 6 and cov.coperto_quota.between(0, 1).all()
t12 = pd.read_csv(os.path.join(HERE, "tabelle", "tabella_AT_2012_2030.csv"))
assert (t12.tipo == "AT 2012").sum() == 30 and t12.esito.notna().all()
assert os.path.getsize(F) < 20e6

# D1: --prepara-controlli si rifiuta se un file esiste e non scrive nulla
spec = importlib.util.spec_from_file_location("run_v7", os.path.join(HERE, "run.py")); rv = importlib.util.module_from_spec(spec); spec.loader.exec_module(rv)
with tempfile.TemporaryDirectory() as t:
    rv.CTRL = {k: os.path.join(t, k) for k in rv.CTRL}; os.makedirs(rv.CTRL["chiavi"])
    open(os.path.join(rv.CTRL["chiavi"], "campione_chiave_v7.csv"), "w").write("codice\nC501\n")
    camp = pd.DataFrame({"codice": ["C501"], "classe": ["lotto edificabile"], "blocco": [1], "geometry": [None]})
    try:
        rv.prepara_controlli(camp); raise AssertionError("non si e' rifiutato")
    except SystemExit:
        pass
    assert sorted(os.listdir(t)) == ["chiavi"] and open(os.path.join(t, "chiavi", "campione_chiave_v7.csv")).read() == "codice\nC501\n"

# [v7] campione C5 (2.2-2.5), se preparato: niente GFU, blocchi <= 21, codici C501.. contigui, base nuova, cartelle isolate
kf = os.path.join(HERE, "chiavi", "campione_chiave_v7.csv")
if os.path.exists(kf):
    k = pd.read_csv(kf, dtype={"codice": str, "id": str}); lo = k[k.tipo == "lotto"]
    assert set(k.tipo) == {"lotto", "base"} and (k.tipo == "base").sum() == 100 and lo.id.isin(L.id[~G]).all() and lo.id.is_unique
    assert sorted(k.codice) == ["C%03d" % (501 + i) for i in range(len(k))] and k.groupby("blocco").size().max() <= 21
    k5 = pd.read_csv(os.path.join(HERE, "..", "L_lotti_v5", "chiavi", "campione_chiave.csv"), dtype=str); assert not k.id[k.tipo == "base"].isin(k5.id[k5.tipo == "base"]).any()
    st = np.where(L.lotto_at == 1, "D", "F") + "-" + L.classe.map({"lotto edificabile": "E", "lotto da riusare": "R", "area di attivazione": "A"}).fillna("G")
    assert (lo.strato.values == pd.Series(np.asarray(st), index=L.id)[lo.id].values).all()
    for n in (1, 2):
        d = os.path.join(HERE, f"controllo_codificatore_{n}")
        for b, kb in k.groupby("blocco"):
            bd = os.path.join(d, f"blocco_{b:02d}"); want = sorted(c + ".jpg" for c in kb.codice)
            assert sorted(os.listdir(bd)) == sorted(set(["ISTRUZIONI.txt", "codifica.csv", "img", "img_s2"]) | (set(os.listdir(bd)) & {"codifica.sha256"})) and sorted(os.listdir(os.path.join(bd, "img"))) == want == sorted(os.listdir(os.path.join(bd, "img_s2")))
            assert pd.read_csv(os.path.join(bd, "codifica.csv"), dtype=str).codice.tolist() == kb.codice.tolist()
    # autoverifica di criteri_c5 su fogli sintetici (lotti tutti L, base tutta U): C5a = 1, kappa = 1, C5 vero; scrive solo in una cartella temporanea
    camp = k.merge(L[["id", "geometry"]], on="id", how="left"); camp = gpd.GeoDataFrame(camp, geometry="geometry", crs=32632)
    sh = pd.DataFrame({"codice": k.codice, "Q1": np.where(k.tipo == "lotto", "L", "U")})
    NH = json.load(open(os.path.join(HERE, "esito_criteri.json")))["campione_C5"]["N_h"]
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, "tabelle")); rv.HERE = t
        o = rv.criteri_c5(camp, NH, sh, sh, L)
    assert o["C5a"] == 1.0 and o["kappa_binario"][0] == 1.0 and o["C5"] is True and set(o["info"]["in_comune"]) == {"v5", "v6"}
print("ok", len(L), "lotti", L.classe.value_counts().to_dict())
