"""Invarianti di lotti_v3.gpkg (il file pubblicato, non semplificato). Uso: python test_lotti.py"""
import json, os
import numpy as np, geopandas as gpd, pyogrio, shapely

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "lotti_v3.gpkg")
L = gpd.read_file(F, layer="lotti")
R, E, A = (L.classe == c for c in ("lotto da riusare", "lotto edificabile", "area di attivazione"))
assert L.crs.to_epsg() == 32632 and L.geometry.is_valid.all() and not L.geometry.is_empty.any()
assert L.id.is_unique and L.id.str.match(r"^[REA]\d{5}$").all() and (R | E | A).all()
assert set(L.proprieta) <= {"pubblico comunale", "Demanio", "ignoto"} and (L.area_m2 > 0).all() and L.nil_id.notna().all()
assert L.fonti.str.len().gt(0).all() and L.licenze.str.len().gt(0).all()
assert (L.area_m2[E] >= 1500).all() and (L.area_m2[A] >= 500).all()
for f, c in ((0.5, "cap_far05"), (1.0, "cap_far1"), (2.0, "cap_far2")):  # D4: tre scenari, formula, attivazione a zero
    assert (L[c][~A] == np.floor(0.70 * f * L.area_m2[~A] / 80)).all() and (L[c][A] == 0).all()
assert (L.cap_recupero[R] == np.floor(0.70 * L.volume_fonte_m3[R] / 3.2 / 80)).all() and L.cap_recupero[~R].isna().all()  # D3: solo edificio fonte
assert L.scenario_principale[R].isin(["recupero", "demolizione e ricostruzione"]).all()
assert (L.conferma_screening[R & ~L.fonti_riuso.str.contains("dbt_diruto")] == 1).all() and (L.conferma_screening[~R] == 0).all()  # R1 v3: ds503 solo se confermato
assert (L.anche_attivazione[~E] == 0).all() and (L.area_m2[L.anche_attivazione == 1] >= 5000).all()
g = L.geometry.values; i, j = shapely.STRtree(g).query(g, predicate="intersects"); k = i < j  # C3 sul file pubblicato
assert (shapely.area(shapely.intersection(g[i[k]], g[j[k]], grid_size=0.01)) <= 1.0).all()
meta = pyogrio.read_dataframe(F, layer="metadati")
assert set(L.columns) - {"geometry"} <= set(meta.attributo) and meta.licenza.str.len().gt(0).all()
cas = pyogrio.read_dataframe(F, layer="cascata"); last = cas.groupby("classe").rimasti.last()
assert last["riuso"] == R.sum() and last["edificabile"] == E.sum() and last["attivazione"] == A.sum()
res = json.load(open(os.path.join(HERE, "esito_criteri.json")))
assert res["conteggi"] == L.classe.value_counts().to_dict()
print("ok", len(L), "lotti", L.classe.value_counts().to_dict())
cov = __import__("pandas").read_csv(os.path.join(HERE, "tabelle", "copertura_ambiti.csv"))  # copertura: le quote stanno in [0, 1] e le aree per classe nell'ambito
assert cov.coperto_quota.between(0, 1).all() and (cov[["riuso_ha", "edificabile_ha", "attivazione_ha"]].sum(axis=1) <= cov.area_ha + 0.05).all()
assert os.path.getsize(F) < 20e6
