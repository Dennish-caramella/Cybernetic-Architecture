# Spatial Milano Lab: recupero completato (28/10)

Base fondamentale del progetto. La sessione originale girava in una cartella di scratch del PC. Il 28/10 una sessione sul PC l'ha copiata per intero in `Desktop\TESI\spatial_milano_lab` (1024 file, sha256 in `INVENTARIO_SCRATCH.txt`, parte 4: nessun file escluso). Da lì è stato portato qui ciò che serve per leggere ed eseguire il lab. **Nessun dato è stato riscaricato da Internet**: tutto viene dallo scratch originale.

## Dove sta cosa
| Cosa | Dove | Verifica |
|---|---|---|
| Lab completo: `run.py`, modello (`config`, `criteria`, `demand`, `sites`, `portfolios`, `smaa`, `audit`, `export`, `report`, `tests`), `nil.csv`, `build_parcels.py`, risultati (`model.json`, `sites.csv`, audit, `paper.md`), revisioni, proposte A/B/C con script e risultati, prototipo (`build_proto.py`, `proto.src.html`, sito, `lab.json`, PGT, DUSAF) | `lab_completo/` (repo) | sha256 = inventario |
| Script di build e fetch di `mi/` (`build_mi.py`, `build_dbt.py`, `build_page_mi.py`, `spatial-mi.src.html`, `fetch_*.py`) | `mi/` (repo) | sha256 = inventario |
| Resto dello scratch: script di build alla radice, `*_mb.json`, prototipo `spatial-agent-prototype.html`, report e note | `scratch_resto/` (repo, senza dati grezzi) | sha256 = inventario |
| Come eseguire (ambiente, comandi, dipendenze di posizione) | `RUN_README.txt` | — |
| `parcels.csv.gz` (119.352 particelle), `base.pkl`, `sens.pkl`, `access_parcels.csv.gz`, `pu_scores.csv.gz`, 8 PNG dei risultati, 68 tasselli `site/data/t/` | cartella condivisa `spatial_milano_lab_recuperato/lab_completo/` (stessi percorsi) | sha256 = inventario |
| Dati grezzi `mi/raw/` (DBT_2020.zip 569 MB, catasto, PGT, OMI, redditi, popolazione…), `mi/out/`, `mi/site*`, `istat_samples/`, `raw*/`, `shots/` | solo PC: `Desktop\TESI\spatial_milano_lab` | sha256 in `INVENTARIO_SCRATCH.txt` |
| Copie da artifact (prima del recupero) | `recuperati_da_artifact/` | identiche ai file del lab |

Artifact: Spatial Milano Lab https://claude.ai/artifact/LHHSCseATyEEmS4g7SoTW5 · Spatial Milano (base) https://claude.ai/artifact/GaPJf4tLYL8WZTkokBZkMn · Spatial agent prototipo (Monza) https://claude.ai/artifact/MbDwdncXk3bYQNv41N7U1B

## Per eseguirlo
Sul PC, dalla cartella `spatial_milano_lab`: `$env:PYTHONPATH="C:/Temp/pl"; python lab_completo/model/run.py` (circa 23 min; `--no-sens` salta la sensibilità). Attenzione: scrive in `lab_completo/results` e `model/out`. Dal repo serve prima rimettere `parcels.csv.gz` (cartella condivisa) in `lab_completo/data/`.
`mi/build_mi.py` (righe 112 e 119) legge `../istat_samples/`: la copia sta in `scratch_resto/istat_samples` sul PC, va copiata accanto a `mi/` prima di lanciarlo.

## Limiti noti
- Nessuno script è stato eseguito dopo la copia: verificati solo import e hash.
- Le librerie in `C:\Temp\pl` non sono versionate; versioni in `RUN_README.txt`.
- La cronologia della sessione originale prima della compattazione non è recuperabile.
