"""Autocontrollo degli invarianti di lotti_v1.gpkg. Uso: python test_lotti.py"""
import os
import geopandas as gpd, pyogrio

HERE = os.path.dirname(os.path.abspath(__file__))
L = gpd.read_file(os.path.join(HERE, "lotti_v1.gpkg"), layer="lotti")
assert L.crs.to_epsg() == 32632
assert L.geometry.is_valid.all() and not L.geometry.is_empty.any()
assert L.id.is_unique and L.id.str.match(r"^[ER]\d{5}$").all()
assert set(L.classe) == {"lotto edificabile", "lotto da riusare"}
assert set(L.proprieta) <= {"pubblico comunale", "Demanio", "ignoto"}
assert (L.area_m2 > 0).all() and L.nil_id.notna().all() and L.fonti.str.len().gt(0).all() and L.licenze.str.len().gt(0).all()
e = L.classe == "lotto edificabile"
assert L.capacita[e].between(20, 400).all() and (L.capacita[~e] >= 1).all() and (L.capacita <= 400).all()
assert (L.capacita[e] <= (0.70 * L.far_H[e] * L.area_m2[e] / 80).astype(int)).all()  # capacità coerente con la formula
meta = pyogrio.read_dataframe(os.path.join(HERE, "lotti_v1.gpkg"), layer="metadati")
assert set(L.columns) - {"geometry"} <= set(meta.attributo), set(L.columns) - set(meta.attributo)
assert meta.licenza.str.len().gt(0).all()
cas = pyogrio.read_dataframe(os.path.join(HERE, "lotti_v1.gpkg"), layer="cascata")
assert cas[cas.classe == "edificabile"].rimasti.iloc[-1] == e.sum() and cas[cas.classe == "riuso"].rimasti.iloc[-1] == (~e).sum()
print("ok", len(L), "lotti")
