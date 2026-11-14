"""Invarianti di lotti_v6.gpkg (file pubblicato) e del rifiuto di sovrascrivere i controlli. Uso: python test_lotti.py"""
import importlib.util, json, os, tempfile
import numpy as np, pandas as pd, geopandas as gpd, pyogrio, shapely

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "lotti_v6.gpkg")
L = gpd.read_file(F, layer="lotti"); TC = gpd.read_file(F, layer="tessuto_consolidato") if "tessuto_consolidato" in pyogrio.list_layers(F)[:, 0] else None
R, E, A = (L.classe == c for c in ("lotto da riusare", "lotto edificabile", "area di attivazione"))
assert L.crs.to_epsg() == 32632 and L.geometry.is_valid.all() and not L.geometry.is_empty.any()
assert L.id.is_unique and L.id.str.match(r"^[REA]\d{5}$").all() and (R | E | A).all()
assert set(L.proprieta) <= {"pubblico comunale", "Demanio", "non agganciata"} and (L.area_m2 > 0).all() and L.nil_id.notna().all()
assert L.fonti.str.len().gt(0).all() and L.licenze.str.len().gt(0).all() and L.potenziale_vuoto.isin([0, 1]).all()
assert (L.area_m2[E] >= 1500).all() and (L.area_m2[A] >= 500).all()
for f, c in ((0.5, "cap_far05"), (1.0, "cap_far1"), (2.0, "cap_far2")):
    assert (L[c][~A] == np.floor(0.70 * f * L.area_m2[~A] / 80)).all() and (L[c][A] == 0).all()
assert (L.cap_recupero[R] == np.floor(0.70 * L.volume_fonte_m3[R] / 3.2 / 80)).all() and L.cap_recupero[~R].isna().all()
assert (L.area_m2[R] <= L.area_v3_regola[R] + 1).all() and (L.area_intorno_5m[R] <= L.area_intorno_20m[R] + 1).all()
# [v6] D4 estesa ai lotti da riusare: nessun E o R, e nessuna capacita', in un ambito 2030 con residenza "no"
no = L.residenza_2030 == "no"
assert not (no & (E | R)).any() and (L.cap_far2[no] == 0).all()
assert ((L.lotto_at == 1) == (L.quota_at >= 0.5)).all() and L.ambito_id[L.lotto_at == 1].notna().all() and L.ambito_id.dropna().str.match(r"^(MA|ADP|GFU)_\d+$").all()
# [v6] stato come attributo: ogni lotto in ambito ha stato_c1/c2/riferimento e nessun lotto e' escluso per lo stato (D e N compresi, se presenti)
at = L.lotto_at == 1
assert (L.loc[at, ["stato_c1", "stato_c2", "stato_riferimento", "marca_stato_riferimento"]] != "").all().all() and set(L.stato_c1[at]) <= set("ABCDN")
# [v6] cantiere: nessun lotto nei poligoni con cantiere = si; il tessuto consolidato non ha le classi E/R/A come id
res = json.load(open(os.path.join(HERE, "esito_criteri.json"))); cs = set(res["tessuto_consolidato"]["poligoni"])
assert not (L.ambito_id.isin(cs) & at).any()
if TC is not None: assert set(TC.ambito_id) <= cs and TC.id.str.match(r"^T\d{5}$").all() and len(TC) == res["tessuto_consolidato"]["lotti"]
else: assert res["tessuto_consolidato"]["lotti"] == 0
g = L.geometry.values; i, j = shapely.STRtree(g).query(g, predicate="intersects"); k = i < j
assert (shapely.area(shapely.intersection(g[i[k]], g[j[k]], grid_size=0.01)) <= 1.0).all()
meta = pyogrio.read_dataframe(F, layer="metadati")
assert set(L.columns) - {"geometry"} <= set(meta.attributo) and meta.licenza.str.len().gt(0).all()
cas = pyogrio.read_dataframe(F, layer="cascata"); last = cas[cas.classe != "informativo"].groupby("classe").rimasti.last()
assert last["riuso"] == R.sum() and last["edificabile"] == E.sum() and last["attivazione"] == A.sum()
assert res["conteggi"] == L.classe.value_counts().to_dict()
amb = pd.read_csv(os.path.join(HERE, "tabelle", "ambiti_2030.csv"))
assert len(amb) == 29 and amb.ambito_id.is_unique and amb.residenza_2030.isin(["si", "no", "si [H]"]).all() and amb.fonte_ambito.str.startswith("http").all()
cov = pd.read_csv(os.path.join(HERE, "tabelle", "copertura_ambiti_2030.csv"))
assert len(cov) == len(amb) + 6 and (cov.pcu == 1).sum() == 6 and cov.coperto_quota.between(0, 1).all()
t12 = pd.read_csv(os.path.join(HERE, "tabelle", "tabella_AT_2012_2030.csv"))
assert (t12.tipo == "AT 2012").sum() == 30 and t12.esito.notna().all()
assert os.path.getsize(F) < 20e6

# D1: --prepara-controlli si rifiuta se un file esiste e non scrive nulla
spec = importlib.util.spec_from_file_location("run_v6", os.path.join(HERE, "run.py")); rv = importlib.util.module_from_spec(spec); spec.loader.exec_module(rv)
with tempfile.TemporaryDirectory() as t:
    rv.CTRL = {k: os.path.join(t, k) for k in rv.CTRL}; os.makedirs(rv.CTRL["chiavi"])
    open(os.path.join(rv.CTRL["chiavi"], "campione_chiave_v6.csv"), "w").write("codice\nC301\n")
    camp = pd.DataFrame({"codice": ["C301"], "classe": ["lotto edificabile"], "geometry": [None]})
    try:
        rv.prepara_controlli(camp); raise AssertionError("non si e' rifiutato")
    except SystemExit:
        pass
    assert sorted(os.listdir(t)) == ["chiavi"] and open(os.path.join(t, "chiavi", "campione_chiave_v6.csv")).read() == "codice\nC301\n"
print("ok", len(L), "lotti", L.classe.value_counts().to_dict())
