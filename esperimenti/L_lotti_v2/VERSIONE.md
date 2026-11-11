# Base L — versione

- Versione: **v2 candidata**, 2026-11-11, ticket #34. Semi: 42 (accorpamento k-means), 3411 (campione ortofoto), 3412 (20 casi di Dennis). CRS EPSG:32632.
- Stato: **non accettata, non congelata** — C5 (controllo su ortofoto) non superato; C7 in attesa di Dennis (esito_criteri.json, esecuzioni/registro.txt). Per la regola di arresto serve una decisione di Dennis; la revisione indipendente (REPORT §7) non è ancora fatta.
- Hash del contenuto (attributi + WKB 2D normalizzati, ordinati per id): `011672c66a0e9212221ba7984b847295848924c29dcdeeae7d48fded0089249b`, identico nelle esecuzioni 2026-11-11T122041Z e 122931Z (C8).
- Il file pubblicato `lotti_v2.gpkg` non è semplificato: è lo stesso su cui si calcolano i criteri. Ambiente: `requirements.txt` (Python 3.13.18).
- Le immagini di ortofoto (AGEA, licenza di sola visione) non sono nel repo: `esperimenti/_cache/L_lotti_v2/orto/` e `controllo_umano/img/` (ignorata), rigenerate da `run.py`.

## SHA-256 dei file
```
50a0c7f1761f85cb407dbc24faeb7b6ad80fdd5cef149dc1ec3d76c149c15372  lotti_v2.gpkg
3223654738f5d23bff64ba3e0d999a170e70646d48a2f2f9bf139138dee93b49  run.py
cb616a3080c622e7724d3577d8b672587c0fbdd08a1c14ff1707cca97087ef67  test_lotti.py
57fe97891722c718ecc61d11750abd7f7425b43a053fea7868a07c2d48373376  requirements.txt
891bdfd89419d35480f45f7e4882a92f2a511db4b67bc3ac82359fa3589e0209  esito_criteri.json
4927b59da319b61cb7639301497d5745e536324ff6820269ee9121addd8d8fd4  tabelle/campione_ortofoto.csv
5383de1e787983aa1fb4ecb77fc5b8cb513610503be683e16e7f1a85e00302ca  tabelle/cascata.csv
4ed06c05195ae4f992bd3eb4994888394038d54de59ed784738198d873fb450d  tabelle/codifica_ortofoto.csv
48bb36b404bca1685d774d68d7c1ef8f7353aecb846cb19e4bb89568adc7cf55  tabelle/controllo_ortofoto_esito.csv
1c9737bcd80083e8195681f03a68a55fb34d5d9c80856293c391006c814b0951  tabelle/lotti_attributi.csv
956910145209f7ee603bf665fa557a377daa5209cf2056278443bc3a49d2dc11  tabelle/metadati.csv
817aebb025026f2e9ba32a72c3d00ae22f0868a5a125efdd4a9d513050b199ee  tabelle/nil_classe.csv
9b8ec96e7177d79403513a700e3d52c222f38d0e34426d2d9110ae2fa6e722a8  controllo_umano/casi.csv
22ee79c400f39372c63f217ec445cf2669054a436c0d2d120bb75dd80d1072ef  controllo_umano/chiave_da_aprire_dopo.csv
5f672944203a4cc8d6bfac91da18ac0d22e24dba302fab48e9bfe73c6d37c9c4  esecuzioni/00_preregistrazione.txt
af854c43f99ab97a92366e793342d6db4865b793db0d0327d29bacedf651981d  fig/cascata.png
b447737a069f984b3eaf3dfd1c564216fe5fd5f34fd9951bdfa590135840ba3b  fig/mappa_classi.png
```
