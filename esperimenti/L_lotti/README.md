Base L v1 (ticket #16): lotti candidati di Milano, edificabili e da riusare, in EPSG:32632; esito e regole in `REPORT.md`, versione in `VERSIONE.md`.
Rifare tutto: `python run.py` (scarica le fonti in `esperimenti/_cache/L_lotti/raw`, ~1 h la prima volta; poi ~8 min), quindi `python test_lotti.py`; servono geopandas, pyogrio, shapely, scipy, scikit-learn, matplotlib.
