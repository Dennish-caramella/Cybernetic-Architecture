# Laboratorio di ricerca — social housing partecipativo a Milano

Obiettivo: scoprire, implementare e testare un modello (matematico, economico, ML/NN) di livello di ricerca avanzata per individuare **più lotti candidati** per social housing a Milano, confrontabili dai cittadini e dal Comune, con **fattori pesati dai bisogni reali delle persone** (cibernetica + partecipazione; la "pancia della distribuzione": famiglie a reddito medio-basso escluse dal mercato).

## Regole del team
1. **Il modello base non si tocca.** `mi/` (dati, script, `mi/site/`) e l'artifact pubblicato sono la base. Lettura sì, scrittura MAI. Copia di sicurezza in `mi/site_BASE_backup/`.
2. Tutto il lavoro del team sta in `lab/`: `data/` (tabelle derivate), `proposals/` (proposte + codice + risultati), `reviews/` (revisioni paritarie), `model/` (modello integrato), `results/`.
3. Ogni affermazione quantitativa deve venire da un esperimento riproducibile (script Python in `lab/`) o da una fonte citata. Distinguere: dato reale, assunzione, dato sintetico.
4. Niente punteggi di idoneità su singole famiglie (AI Act All. III 5a). Si classificano lotti e portafogli di lotti.
5. Python: `PYTHONPATH=C:/Temp/pl python ...` (numpy 2.4, scipy 1.17, scikit-learn 1.9, highspy, shapely 2.2, pyproj, pyshp, openpyxl). Niente torch: reti neurali con scikit-learn o numpy.
6. Report di riferimento: `reports/Lotti per social housing partecipativo.md` (letteratura, verdetti sui metodi, cosa applicare/non applicare).

## Dati disponibili (sola lettura)
Coordinate locali in **km**: x = (lon − 9.19)·KX, y = −(lat − 45.465)·KY, con KX = 111.32·cos(45.465°), KY = 110.57 (y verso sud).
Geometrie codificate a **delta**: lista piatta [dx0, dy0, dx1, dy1, …] di interi; coordinata = somma cumulata × unità.

- `mi/out/core.json` — unità 0.01 km (`meta.unit_km`).
  - `nil[]`: 88 NIL con `id, n (nome), a (km²), c [x,y], rings (delta), ind {...}`. Indicatori in `ind`: pop (2025), dens, a014, a65, a80, for_ (% stranieri), trend (% 2015-25), pop21, emp21, deg (% istruzione terziaria 2021), dwp, inc (reddito complessivo medio per contribuente €/anno), wage_m (lavoro dipendente imponibile €/mese), net_m (netto stimato €/mese), rate (aliquota media IRPEF+add.), rich (% contribuenti >75k), poor (% ≤15k), pens_share, cap (CAP principali), rent (OMI 2024/2 €/m² mese), price (OMI €/m²), green (indice verde), heatrisk, heatexp, metro_km, metro_n, metro_area (% area entro 500 m da metro), metro_pop (% residenti entro 500 m), dusaf {cat: % area}, pgt {cat: % area}.
  - `cap{CAP: {taxpayers, inc, wage, wage_m, net_m, rate, rich, poor, pens_share}}` — IRPEF 2024 per CAP (lordo per contribuente, NON per nucleo).
  - `omi[]` zone OMI con rent, price, rings. `metro.st[]` fermate {x,y,n,l}; `metro.lines[]`. `hex` griglia sezioni censimento 2021 (r=0.25 km; celle [x,y,pop,emp,for,deg,dw]). `city` (ring, inc città, metro_pop).
- `mi/out/tiles.json` — indice tasselli 2 km, `nil{id: {dbt_h, dbt_cov, dbt_vol, dbt_n, lot_n, lot_a, dbt_tall}}`, `uses` (nomi usi DBT).
- `mi/out/t/<tx>_<ty>.json` — unità `u` = 0.0005 km (0,5 m). `v[]` volumi DBT 2020: [h_m, uso_idx, quota_m, ref_particella, …delta ring]. `p[]` particelle catastali: [ref, area_m2, copertura 0-1, indice_volumetrico m³/m², …delta ring]. ~231k volumi, ~120k particelle.
- `mi/out/pgt.json`, `mi/out/dusaf.json` — categorie con poligoni (unità 0.01 km); pgt cats: srv_verde, srv_erp, srv_ist, srv_alt, rig (ambiti rigenerazione), dism (aree dismesse), tras (ambiti trasformazione), naf, pae, agr; `ats[]` ambiti di trasformazione.
- Grezzi in `mi/raw/` (geojson PGT/DUSAF WGS84, OMI, redditi CSV, popolazione NIL per età 1999-2025 zip, verde/calore CSV, metro geojson, catasto tasselli, DBT shapefile in `mi/raw/dbt/`). Sezioni censimento 2021: `istat_samples/sezioni/x/SHP/R03_21_WGS84` (UTM32N), indicatori `istat_samples/census_dl/R03_indicatori_2021_sezioni.xlsx`.
- Fonti assenti: proprietà dei suoli, costi di costruzione reali, preferenze reali dei cittadini (da simulare dichiarandolo).
