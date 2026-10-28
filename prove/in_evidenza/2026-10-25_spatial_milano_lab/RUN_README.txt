RUN_README - come eseguire lab e mi (2026-10-28)
Verificato: solo import delle librerie e lettura dei sorgenti. NESSUNO script e' stato eseguito.

1. AMBIENTE
Python: 3.11.9 (C:\Users\Caredda Dennis\AppData\Local\Programs\Python\Python311\python.exe, e' il "python" di default).
Librerie in C:\Temp\pl (da usare via PYTHONPATH; non copiate qui):
  numpy 2.4.6, scipy 1.17.1, scikit-learn 1.9.1, joblib 1.6.0, threadpoolctl 3.7.0,
  shapely 2.2.0, pyproj 3.7.2, pyshp 3.1.6 (modulo "shapefile"), openpyxl 3.1.5, et_xmlfile 2.0.0,
  highspy 1.15.1, narwhals 2.27.1, cloudpickle 3.1.2, certifi 2026.10.23
Librerie nel python di sistema (non in C:\Temp\pl): pandas 3.0.6, matplotlib 3.11.2 (numpy 2.4.6 e openpyxl 3.1.5 anche li').
Import verificato con PYTHONPATH=C:/Temp/pl: numpy, scipy, sklearn, shapely, pyproj, shapefile, openpyxl, highspy.
Moduli standard usati dagli script: json, csv, zipfile, glob, pickle, os, sys, shutil, io, collections, itertools, contextlib.

2. COMANDI (PowerShell; dalla cartella spatial_milano_lab)
  $env:PYTHONPATH="C:/Temp/pl"
  python lab_completo/model/run.py            # aggiungi --no-sens per saltare la sensibilita'
  python lab_completo/model/tests.py          # test
Nota: la docstring dice "python lab/model/run.py" (nome originale della cartella); con la copia il percorso e' lab_completo/...

Build mi (ESEGUIRE DENTRO mi/: i percorsi sono relativi alla cartella corrente):
  cd mi
  python build_mi.py        # raw/ -> out/core.json, pgt.json, dusaf.json, b/*.json
  python build_dbt.py       # raw/dbt, raw/catasto -> out/t/*.json, out/tiles.json (richiede out/core.json)
  python build_page_mi.py   # spatial-mi.src.html + out -> site/spatial-milano.html, site/data/
(fetch_*.py scaricano dati da Internet: non servono per rigenerare.)
Altri: lab_completo/data/build_parcels.py, lab_completo/prototype/build_proto.py (docstring: da root, "python lab/..."), proposals/*/run*.py.

3. PERCORSI ASSOLUTI / DIPENDENZE DI POSIZIONE
- Nessun .py in lab_completo e mi contiene percorsi assoluti reali nel codice (grep su C:\, /c/Users, /tmp). "C:/Temp/pl" compare solo nelle docstring come PYTHONPATH.
- lab/model/config.py: percorsi derivati da __file__ (LAB=cartella sopra model; ROOT=cartella sopra LAB = spatial_milano_lab; MI=ROOT/mi; PROP=LAB/proposals; OUT=model/out; RES=LAB/results). Funziona anche con il nome lab_completo, purche' mi/ stia accanto (spatial_milano_lab/mi: ok).
- run.py legge: LAB/data/nil.csv, proposals/C_ml_spatial/results/hex_need.csv; scrive model/out/*.pkl e LAB/results.
  ATTENZIONE: scrivendo in lab_completo/results e model/out sovrascrive le copie (non toccare la cartella lab originale gia' presente).
- mi/*.py: percorsi relativi alla cartella corrente (raw/, out/, site/, spatial-mi.src.html): serve cwd = mi.
- mi/build_mi.py righe 112 e 119 usano ../istat_samples/census_dl/R03_indicatori_2021_sezioni.xlsx e ../istat_samples/sezioni/x/SHP/R03_21_WGS84,
  cioe' spatial_milano_lab/istat_samples/. La copia e' in spatial_milano_lab/scratch_resto/istat_samples/. Per far girare build_mi.py:
  copiare (o linkare) scratch_resto/istat_samples in spatial_milano_lab/istat_samples. NON fatto, per non alterare la struttura.
- mi/raw/DBT_2020.zip (569 MB) e' stato copiato; build_dbt.py legge raw/dbt/ (gia' estratto, presente).
