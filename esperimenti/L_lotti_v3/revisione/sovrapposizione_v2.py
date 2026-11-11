"""Revisione Base L v3: lotti del campione v3 già codificati nel campione v2 (stessa ortofoto). Dipendenza non dichiarata e test-retest di Q1.
Uso: python revisione/sovrapposizione_v2.py"""
import os, pandas as pd, geopandas as gpd, shapely
E = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
c3 = pd.read_csv(f"{E}/L_lotti_v3/tabelle/controllo_ortofoto_esito.csv"); c2 = pd.read_csv(f"{E}/L_lotti_v2/tabelle/controllo_ortofoto_esito.csv")
g3 = gpd.read_file(f"{E}/L_lotti_v3/lotti_v3.gpkg", layer="lotti").set_index("id"); g2 = gpd.read_file(f"{E}/L_lotti_v2/lotti_v2.gpkg", layer="lotti").set_index("id")
s3, s2 = g3.loc[g3.index.intersection(c3.id)], g2.loc[g2.index.intersection(c2.id)]
j = gpd.sjoin(s3[["geometry"]], s2[["geometry"]], predicate="intersects").reset_index().rename(columns={"id": "id3", "id_left": "id3", "index": "id3", "id_right": "id2"})
j["iou"] = [shapely.area(shapely.intersection(s3.geometry[a], s2.geometry[b])) / shapely.area(shapely.union(s3.geometry[a], s2.geometry[b])) for a, b in zip(j.id3, j.id2)]
j = j[j.iou > 0.5].merge(c3[["id", "classe", "origine", "Q1"]].rename(columns={"id": "id3"}), on="id3").merge(c2[["id", "classe", "Q1"]].rename(columns={"id": "id2", "classe": "classe_v2", "Q1": "Q1_v2"}), on="id2")
print(j[["id3", "id2", "iou", "classe", "origine", "classe_v2", "Q1", "Q1_v2"]].round(2).to_string(index=False))
ok = lambda s: s.isin(list("LCD")); print(f"\nlotti con IoU > 0,5: {len(j)}; Q1 identico {(j.Q1 == j.Q1_v2).sum()}; esito binario identico {(ok(j.Q1) == ok(j.Q1_v2)).sum()}")
