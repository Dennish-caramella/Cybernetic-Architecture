"""Revisione indipendente Base L v3: controlli strutturali che richiedono la ricostruzione (R3, residenza occupata negli AT,
funzione prevalente degli AT, aggancio della proprietà ds677). Uso: python revisione/strutturale.py [cartella_con_run.py]
Attenzione: build() riscrive tabelle/screening_ds503_chiave.csv (contenuto deterministico) nella cartella indicata; eseguirlo su una copia."""
import os, sys, numpy as np, pandas as pd, geopandas as gpd, shapely
D = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, D); import importlib.util
spec = importlib.util.spec_from_file_location("run3", os.path.join(D, "run.py")); r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
Lt, U, nil, W, gv, cov = r.build(None); P = r.P
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30)

# 1. R3: lotti da riusare = particella intera meno gli altri edifici; rapporto area lotto / impronta degli edifici fonte
V = gpd.read_file(os.path.join(r.RAW, "dbt", "UN_VOL.shp"), columns=["UN_VOL_AV", "UN_VOL_POR", "CEDIUV"]).to_crs(r.CRS)
V = V[(V.UN_VOL_POR != "02") & (V.UN_VOL_AV.astype(float) > 0.5)]; fp = V.assign(a=V.area).groupby("CEDIUV").a.sum()
R = Lt[Lt.classe == "lotto da riusare"].copy()
R["impronta_fonte_m2"] = R.edifici_fonte.map(lambda s: fp.reindex(s.split(";")).sum()); R["rapporto"] = R.area_m2 / R.impronta_fonte_m2.clip(lower=1)
ref2i = U.reset_index().set_index("ref")["index"]; Ui = U.loc[ref2i[R.ref].values]
R["is_at"] = Ui.is_at.values; R["dusaf_infra"] = Ui.dusaf_infra.round(2).values; R["at_name"] = Ui.at_name.values
print("\n[R3] lotti da riusare: rapporto area/impronta fonte, quantili", R.rapporto.quantile([.5, .9, .99]).round(1).to_dict())
for t in (10, 50):
    m = R.rapporto > t; print(f"  rapporto > {t}: {m.sum()} lotti, {R.area_m2[m].sum() / 1e4:.1f} ha su {R.area_m2.sum() / 1e4:.1f}; cap_far1 {R.cap_far1[m].sum()} su {R.cap_far1.sum()}")
print("  in particelle AT:", int(R.is_at.sum()), "lotti,", round(R.area_m2[R.is_at].sum() / 1e4, 1), "ha; con DUSAF infrastrutture >= 0,5:", int((R.dusaf_infra >= .5).sum()))
print(R.sort_values("area_m2", ascending=False)[["id", "ref", "area_m2", "impronta_fonte_m2", "rapporto", "fonti_riuso", "is_at", "at_name", "dusaf_infra", "cap_far1", "cap_recupero", "scenario_principale"]].head(10).round(1).to_string())

# 2. residenza occupata negli AT: particelle AT tolte da quel filtro (dopo i filtri precedenti della cascata)
A = U[(U.pgt_tras >= P["excl_share"]) & ~U.pcu & (U.area_m2 >= P["a_min_parcel"]) & (U.dusaf_wat < P["excl_share"]) & ~(U[["pgt_agr", "pgt_srv_ist"]] >= P["excl_share"]).any(axis=1)]
occ = (A.n_vol > 0) & (A.res_share.fillna(0) >= P["occ_res_share"])
print(f"\n[occ] particelle AT dopo i filtri precedenti: {len(A)}, tolte come residenza occupata: {occ.sum()} ({A.area_m2[occ].sum() / 1e4:.1f} ha, volume res. {A.volume_m3[occ].sum():,.0f} m³)")
print("  per ambito (ha):", A[occ].groupby("at_name").area_m2.sum().div(1e4).round(2).to_dict())
print("  di cui con copertura edificata < 0,10 (residenziale per quota di volume ma quasi libera):", int((occ & (A.cover < 0.10)).sum()))

# 3. AT con funzione prevalente non residenziale (mosaico PGT, DFUN_PREV1) e capacità abitativa attribuita
at = r.v1.rd("pgt_at.geojson"); fun = at.drop_duplicates("NOME_AMB").set_index("NOME_AMB").DFUN_PREV1
E = Lt[Lt.classe == "lotto edificabile"]; e_at = E[E.origine == "AT"]
print("\n[funzione] DFUN_PREV1 per poligono AT:", at.groupby("DFUN_PREV1").NOME_AMB.apply(lambda v: sorted(set(v))).to_dict())
nr = at[at.DFUN_PREV1 != "RESIDENZIALE"]; pt = e_at.geometry.representative_point()
inn = np.zeros(len(e_at), bool)
for g in shapely.make_valid(nr.geometry.values): inn |= shapely.contains_xy(g, pt.x.values, pt.y.values)
print(f"  lotti edificabili AT con punto interno in un AT non residenziale: {inn.sum()} ({e_at.area_m2[inn].sum() / 1e4:.1f} ha), cap_far1 {e_at.cap_far1[inn].sum()} su {E.cap_far1.sum()} degli edificabili")
print("  SL del mosaico / area del poligono (se ~1, SL non è un indice):", (at.SL / at.geometry.area).round(3).describe()[["min", "50%", "max"]].to_dict(), "; DSTR_ATT:", at.DSTR_ATT.unique().tolist())

# 4. proprietà: aggancio ds677 per foglio+mappale
c = r.v1.rd("ds677_patrimonio.geojson"); c = c[c.MILANO == "SI"]
k = set(zip(pd.to_numeric(c.FOGLIO, errors="coerce"), pd.to_numeric(c.MAPPALE, errors="coerce"))); kt = set(zip(pd.to_numeric(c[c.TIPO == "TERRENO"].FOGLIO, errors="coerce"), pd.to_numeric(c[c.TIPO == "TERRENO"].MAPPALE, errors="coerce")))
uk = set(zip(U.foglio, U.mappale)); print(f"\n[proprietà] chiavi ds677 (MILANO=SI): {len(k)}, trovate fra le particelle di terreno: {len(k & uk)} ({len(k & uk) / len(k):.2f}); TERRENO: {len(kt & uk)}/{len(kt)}")
print("  ref -> foglio (esempi):", U[["ref", "foglio", "mappale"]].head(3).values.tolist(), "; chiavi duplicate (stesso foglio+mappale su più particelle):", int(U.duplicated(["foglio", "mappale"]).sum()))
# punto ds677 dentro la particella agganciata? (controllo spaziale indipendente dalla chiave)
cg = c[c.geometry.notna() & ~c.geometry.is_empty].to_crs(r.CRS) if c.crs else None
if cg is not None and len(cg):
    j = gpd.sjoin(cg[["FOGLIO", "MAPPALE", "geometry"]], U[["foglio", "mappale", "geometry"]], predicate="within", how="inner")
    same = (pd.to_numeric(j.FOGLIO, errors="coerce") == j.foglio) & (pd.to_numeric(j.MAPPALE, errors="coerce") == j.mappale)
    print(f"  punti ds677 dentro una particella di terreno: {len(j)}; con foglio+mappale coincidenti: {same.mean():.2f}")
