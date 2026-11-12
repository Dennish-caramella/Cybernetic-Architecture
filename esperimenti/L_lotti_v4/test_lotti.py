"""Invarianti di lotti_v4.gpkg (file pubblicato, non semplificato) e del rifiuto di sovrascrivere i controlli. Uso: python test_lotti.py"""
import importlib.util, json, os, tempfile
import numpy as np, pandas as pd, geopandas as gpd, pyogrio, shapely

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "lotti_v4.gpkg")
L = gpd.read_file(F, layer="lotti")
R, E, A = (L.classe == c for c in ("lotto da riusare", "lotto edificabile", "area di attivazione"))
assert L.crs.to_epsg() == 32632 and L.geometry.is_valid.all() and not L.geometry.is_empty.any()
assert L.id.is_unique and L.id.str.match(r"^[REA]\d{5}$").all() and (R | E | A).all()
assert set(L.proprieta) <= {"pubblico comunale", "Demanio", "non agganciata"} and (L.area_m2 > 0).all() and L.nil_id.notna().all()  # D7
assert L.fonti.str.len().gt(0).all() and L.licenze.str.len().gt(0).all() and L.stato_attuativo.str.len().gt(0).all()
assert (L.area_m2[E] >= 1500).all() and (L.area_m2[A] >= 500).all()
for f, c in ((0.5, "cap_far05"), (1.0, "cap_far1"), (2.0, "cap_far2")):
    assert (L[c][~A] == np.floor(0.70 * f * L.area_m2[~A] / 80)).all() and (L[c][A] == 0).all()
assert (L.cap_recupero[R] == np.floor(0.70 * L.volume_fonte_m3[R] / 3.2 / 80)).all() and L.cap_recupero[~R].isna().all()
assert (L.area_m2[R] <= L.area_v3_regola[R] + 1).all() and (L.area_intorno_5m[R] <= L.area_intorno_20m[R] + 1).all()  # G2: il lotto è dentro la regola v3
assert not L.funzione_at[E].isin(["TERZIARIO", "SERVIZI"]).any()  # D4: nessun edificabile in ambiti AT non residenziali
assert ((L.lotto_at == 1) == (L.quota_at >= 0.5)).all() and L.stato_attuativo[L.lotto_at == 0].eq("non applicabile (lotto non AT)").all()
g = L.geometry.values; i, j = shapely.STRtree(g).query(g, predicate="intersects"); k = i < j
assert (shapely.area(shapely.intersection(g[i[k]], g[j[k]], grid_size=0.01)) <= 1.0).all()  # C3
meta = pyogrio.read_dataframe(F, layer="metadati")
assert set(L.columns) - {"geometry"} <= set(meta.attributo) and meta.licenza.str.len().gt(0).all()
cas = pyogrio.read_dataframe(F, layer="cascata"); last = cas[cas.classe != "informativo"].groupby("classe").rimasti.last()
assert last["riuso"] == R.sum() and last["edificabile"] == E.sum() and last["attivazione"] == A.sum()
res = json.load(open(os.path.join(HERE, "esito_criteri.json")))
assert res["conteggi"] == L.classe.value_counts().to_dict()
cov = pd.read_csv(os.path.join(HERE, "tabelle", "copertura_ambiti.csv"))
assert len(cov) == 30 and (cov.pcu == 0).sum() == 24 and cov.coperto_quota.between(0, 1).all()  # D6: tabella completa
assert os.path.getsize(F) < 20e6

# D1: --prepara-controlli si rifiuta se un file esiste e non scrive nulla
spec = importlib.util.spec_from_file_location("run_v4", os.path.join(HERE, "run.py")); rv = importlib.util.module_from_spec(spec); spec.loader.exec_module(rv)
with tempfile.TemporaryDirectory() as t:
    rv.CTRL = {k: os.path.join(t, k) for k in rv.CTRL}; os.makedirs(rv.CTRL["controllo_codificatore_2"])
    open(os.path.join(rv.CTRL["controllo_codificatore_2"], "codifica.csv"), "w").write("codice,Q1\nC001,L\n")
    camp = pd.DataFrame({"codice": ["C001"], "classe": ["lotto edificabile"], "visto_v3": [0], "geometry": [None]})
    try:
        rv.prepara_controlli(None, camp); raise AssertionError("non si è rifiutato")
    except SystemExit:
        pass
    assert sorted(os.listdir(t)) == ["controllo_codificatore_2"] and open(os.path.join(t, "controllo_codificatore_2", "codifica.csv")).read() == "codice,Q1\nC001,L\n"
print("ok", len(L), "lotti", L.classe.value_counts().to_dict())
