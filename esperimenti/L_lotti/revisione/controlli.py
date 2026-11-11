"""Controlli del revisore (REPORT §7). Non modifica la prova: legge il gpkg completo, la cache e riusa le funzioni di run.py.
Uso: python revisione/controlli.py [percorso lotti_v1_full.gpkg]   -> stampa i risultati (JSON) su stdout.
Seme del campione nuovo: 20261111, dichiarato prima di estrarre."""
import json, os, sys
import numpy as np, pandas as pd, geopandas as gpd, shapely

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import run  # parcels, share, dusaf_cat, rd, P

SEED_REV, N_REV, N_BASE = 20261111, 100, 300
FULL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "_cache", "L_lotti", "lotti_v1_full.gpkg")


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return dict(k=int(k), n=int(n), p=round(p, 3), ic95=[round(c - h, 3), round(c + h, 3)])


L = gpd.read_file(FULL, layer="lotti")
light = gpd.read_file(os.path.join(HERE, "..", "lotti_v1.gpkg"), layer="lotti")
du = run.rd("dusaf8.geojson"); cod = du.COD_TOT.astype(str); du["cat"] = cod.map(run.dusaf_cat)
lay = {"res": du[du.cat.isin(["resd", "resr"])],
       "nat_codice": du[du.cat.isin(["green", "agr", "wood", "wat"])],                 # come run.py (1412 escluso)
       "nat_testo": du[cod.str[0].isin(list("2345")) | cod.str.startswith("14")],       # come scritto in §1 (14x, 2xx-5xx)
       "art_codice": du[cod.str.startswith("1") & ~cod.str.startswith("14")],          # come run.py (14x escluso)
       "art_testo": du[cod.str.startswith("1")],                                         # come scritto in §1 (1xx)
       "libera": du[cod.str.startswith("13") | (cod == "1412")]}                         # [H] revisore: 13x cantieri/degrado/cave + 1412 incolte


def quote(g):
    return {k: run.share(g, v) for k, v in lay.items()}


out = {}
# 1. C3 sul file completo e sul file leggero (quello nel repo)
for nome, G in (("completo", L), ("leggero_repo", light)):
    g = G.geometry.values; i, j = shapely.STRtree(g).query(g, predicate="intersects"); k = i < j
    ov = shapely.area(shapely.intersection(g[i[k]], g[j[k]], grid_size=0.01))
    tol = np.maximum(5, 0.01 * np.minimum(shapely.area(g[i[k]]), shapely.area(g[j[k]])))
    out[f"C3_{nome}"] = dict(coppie_oltre_tol=int((ov > tol).sum()), coppie_area_pos=int((ov > 0.01).sum()), m2_max=round(float(ov.max()), 1))

# 2. C5 sul campione originale con le due letture della regola (codice / testo di §1)
camp = pd.read_csv(os.path.join(HERE, "..", "tabelle", "campione_controllo.csv"))
S = L.set_index("id").loc[camp.id]; q = quote(S.geometry); e = (S.classe == "lotto edificabile").values
out["C5a_originale_codice"] = wilson(((q["res"] <= .5) & (q["nat_codice"] <= .5))[e].sum(), e.sum())
out["C5a_originale_testo"] = wilson(((q["res"] <= .5) & (q["nat_testo"] <= .5))[e].sum(), e.sum())
out["C5b_originale_codice"] = wilson((q["art_codice"] >= .5)[~e].sum(), (~e).sum())
out["C5b_originale_testo"] = wilson((q["art_testo"] >= .5)[~e].sum(), (~e).sum())

# 3. campione nuovo di edificabili (seme 20261111, n = 100, senza reimmissione) e censimento per origine
rng = np.random.default_rng(SEED_REV)
E = L[L.classe == "lotto edificabile"].reset_index(drop=True)
qe = quote(E.geometry)
ok_c5a = (qe["res"] <= .5) & (qe["nat_codice"] <= .5); libera = qe["libera"] >= .5
sid = rng.choice(len(E), N_REV, replace=False)
out["nuovo_campione_ids"] = E.id.values[sid].tolist()
out["nuovo_C5a_regola_codice"] = wilson(ok_c5a[sid].sum(), N_REV)
out["nuovo_libera_o_dismessa_DUSAF13x_1412"] = wilson(libera[sid].sum(), N_REV)
out["nuovo_origini"] = E.origine.values[sid].tolist().count("SOFT"), E.origine.values[sid].tolist().count("ERP")
out["censimento_edificabili_per_origine"] = pd.DataFrame({"o": E.origine, "c5a": ok_c5a, "libera": libera, "res_gt_05": qe["res"] > .5}).groupby("o").agg(
    n=("c5a", "size"), c5a=("c5a", "mean"), libera=("libera", "mean"), res_gt_05=("res_gt_05", "mean")).round(3).to_dict("index")

# 4. tasso di base: la stessa regola su particelle di terreno qualsiasi (non filtrate), stesse taglie
D = run.parcels()
nil = run.rd("ds964_nil.geojson"); city = shapely.union_all(nil.geometry.values); rp = D.geometry.representative_point()
D = D[D.land & shapely.contains_xy(city, rp.x.values, rp.y.values)]
big = D[D.area_m2 >= 2286]; small = D[D.area_m2 >= 300]  # 2286 m² = area minima con 20 alloggi a FAR 1
b1 = big.iloc[rng.choice(len(big), N_BASE, replace=False)]; qb = quote(b1.geometry)
b2 = small.iloc[rng.choice(len(small), N_BASE, replace=False)]; qs = quote(b2.geometry)
out["base_C5a_regola_su_particelle_qualsiasi_ge2286"] = wilson(((qb["res"] <= .5) & (qb["nat_codice"] <= .5)).sum(), N_BASE)
out["base_C5a_solo_parte_residenziale_ge2286"] = wilson((qb["res"] <= .5).sum(), N_BASE)
out["base_C5b_regola_su_particelle_qualsiasi_ge300"] = wilson((qs["art_codice"] >= .5).sum(), N_BASE)
out["base_libera_ge2286"] = wilson((qb["libera"] >= .5).sum(), N_BASE)
# doppioni foglio+mappale tra le particelle di terreno (il join ds677 ignora allegato e sviluppo)
kk = D.foglio.astype(int).astype(str) + "/" + D.mappale.astype(int).astype(str)
out["particelle_terreno_chiave_foglio_mappale_duplicata"] = int(kk.duplicated(keep=False).sum())
out["particelle_geometria_duplicata"] = int(D.geometry.to_wkb().duplicated(keep=False).sum())

# 5. riuso: quanti in tessuto residenziale DUSAF e quanta capacità portano
R = L[L.classe == "lotto da riusare"].reset_index(drop=True); qr = quote(R.geometry)
rr = qr["res"] > .5
out["riuso_res_gt_05"] = dict(n=int(rr.sum()), su=len(R), capacita=int(R.capacita[rr].sum()), capacita_tot=int(R.capacita.sum()),
                              capacita_da_volume=int(R.capacita[R.base_capacita == "SL esistente DBT"].sum()))
out["riuso_C5b_censimento_codice"] = wilson((qr["art_codice"] >= .5).sum(), len(R))

# 6. capacità: sensibilità del conteggio a FAR e troncatura a 400
cap = lambda far: np.minimum(np.floor(0.7 * far * E.area_m2 / 80), 400)
out["edificabili_con_capacita_ge20"] = {str(f): int((cap(f) >= 20).sum()) for f in (0.5, 1.0)}
out["edificabili_troncati_a_400"] = int((np.floor(0.7 * E.area_m2 / 80) > 400).sum())
out["capacita_tot_FAR"] = {str(f): int(cap(f)[cap(f) >= 20].sum()) for f in (0.5, 1.0)}  # a FAR 2 rientrano anche i 450 siti tolti dal minimo di 20 alloggi: non ricostruibili da qui
out["proprieta_per_origine"] = pd.crosstab(L.origine, L.proprieta).to_dict("index")
print(json.dumps(out, indent=1, ensure_ascii=False, default=lambda x: x.item() if hasattr(x, "item") else str(x)))
