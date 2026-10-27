# Spatial Milano Lab: cosa è completo e cosa manca (27/10)

Base fondamentale del progetto. Controllo fatto il 27/10 su: cartella `Desktop\TESI\spatial_milano_lab`, cartella condivisa, trascrizione della sessione "Riprogettazione con design sync" e i tre artifact pubblicati. **La sessione originale girava sul PC di Dennis, in una cartella di scratch che questo ambiente non può leggere** (richiesta di accesso rifiutata): finché non viene collegata, la ricostruzione è parziale.

## Presente (verificato)
| Cosa | Dove |
|---|---|
| Documenti: README, schema delle particelle, tre proposte A/B/C (model + summary), results.md, paper.md, review1, review2, config.py, tests.py | `lab/` |
| Report e note di ricerca (Lotti per social housing, Benghazi/ISTAT) | `secondo_cervello/ricerche/spatial_milano/` |
| **Prototipo "Spatial Milano Lab"** (pagina completa, 309 KB, include i 88 NIL) | `recuperati_da_artifact/spatial-milano-lab_prototipo_index.html` |
| Modello base protetto "Spatial Milano" (pagina, 273 KB) | `recuperati_da_artifact/spatial-milano-base_index.html` |
| **Risultati del modello** (`lab.json`: 2.291 siti, 11 portafogli, audit, persone contro PGT, modifiche post hoc, risultati per NIL) | `recuperati_da_artifact/lab.json` |
| Dati core estratti dalla pagina (88 NIL con indicatori, CAP, OMI, metro, griglia censuaria) | `recuperati_da_artifact/core.json` |
| PGT e DUSAF (poligoni) | `recuperati_da_artifact/pgt.json`, `dusaf.json` |
| Tasselli catasto + volumi DBT 2020 (68 file, ~25 MB) e prototipo Monza (1 MB) | solo cartella condivisa: `spatial_milano_lab_recuperato/` (hash in `recuperati_da_artifact/MANIFEST_sha256_file_solo_condivisa.txt`) |

Artifact: Spatial Milano Lab https://claude.ai/artifact/LHHSCseATyEEmS4g7SoTW5 · Spatial Milano (base) https://claude.ai/artifact/GaPJf4tLYL8WZTkokBZkMn · Spatial agent prototipo (Monza) https://claude.ai/artifact/MbDwdncXk3bYQNv41N7U1B

## Mancante (sta solo nella cartella di scratch del PC)
Da `ripresa_spatial_milano_lab_2026-10-27.md` e dal README del lab:
- `lab/data/parcels.csv.gz` (119.352 particelle, 78 colonne) e `nil.csv`. Dai tasselli si recuperano solo geometria, area, copertura e indice volumetrico, non le 78 colonne.
- Script del modello: `lab/model/run.py` (esecuzione ~23 min), `model.json`; script delle proposte A/B/C; `lab/prototype/build_proto.py`, `proto.src.html`; `mi/build_mi.py`, `mi/build_page_mi.py`, `mi/spatial-mi.src.html`.
- Dati grezzi `mi/raw/` (PGT/DUSAF geojson, OMI, redditi CSV, popolazione NIL 1999–2025, verde/calore, metro, catasto, DBT shapefile), `mi/out/` originale, `istat_samples/`.
- Librerie Python in `C:/Temp/pl` (numpy, scipy, scikit-learn, highspy, shapely, pyproj, pyshp, openpyxl): ricostruibili, versioni nel README.
- Cronologia della sessione prima della compattazione: la trascrizione disponibile via API contiene solo gli ultimi eventi.

## Per completarlo
Dennis deve collegare alla sessione la cartella di scratch (pulsante "Aggiungi cartella" dell'app desktop) oppure copiarla in `Desktop\TESI\spatial_milano_lab\` (cartelle `lab\` e `mi\`, salvo `mi\raw` se troppo pesante). Poi: staging in cloud, controllo checksum, commit degli script e dei dati leggeri nel repo; dati pesanti in cartella condivisa con manifest.
