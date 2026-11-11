# Base L — versione

- Versione: **v3 candidata**, 2026-11-11, ticket #35 (revisione di v2, #34). Semi: 42 (accorpamento k-means), 3511 (campione ortofoto), 3512 (20 casi di Dennis), 3513 (codici dello screening ds503). CRS EPSG:32632.
- Stato: **non accettata, non congelata**: C5 non superato (C5a 0,58 < 0,70; C5b passa); C7 in attesa di Dennis; accordo con il secondo codificatore da calcolare (coordinatore); revisione indipendente (REPORT §7) non fatta. Regola di arresto: decide Dennis.
- Hash del contenuto (attributi + WKB 2D normalizzati, ordinati per id): `4f41a0afb50440e78ce65ef01062c7d6a2d78d3595c1dd0e93fd839055cd502a`, identico nelle esecuzioni 2026-11-11T135645Z, 140534Z e 141339Z (C8).
- Pre-registrazione: `esecuzioni/00_preregistrazione.txt`, SHA-256 `39e4c160…` registrato alle 13:09Z prima del primo pilota (13:14Z) e presente nel commit `907e0ed` (13:18Z).
- Codifiche manuali hashate prima dell'uso: screening ds503 `e92d4f2d…`, ortofoto C001-C200 `d4211b46…` (registro.txt).
- Il file pubblicato `lotti_v3.gpkg` (1,1 MB) non è semplificato: è lo stesso su cui si calcolano i criteri. Ambiente: `requirements.txt` (Python 3.13.18).
- Immagini AGEA (sola visione) non versionate: `esperimenti/_cache/L_lotti_v3/orto/`, `controllo_umano/img/`, `controllo_secondo_codificatore/img/` (rigenerate da `run.py`; i tasselli sono condivisi con v2 in `_cache/L_lotti_v2/orto/tiles`).

## SHA-256 dei file
```
22f2930e971ad3321dc3ea5950ea5801bd331d2624768e53997dbacd0d001da5  lotti_v3.gpkg
4257449a7f344d7f2e6e4bda9f600f243e38c7f48990269d2ac03f3eae228ba2  run.py
9a424be337ee982956cd29de4b7d3488a5c9bfb358d9efd6ccc929b220867a04  test_lotti.py
a9b1e995c3079bfbfd26030023d9a189fad9c875b363e209b0627f234489eada  requirements.txt
7459a7bc0f92b6983f7159d6a81ef5276bf7b68894a5d2f887ac674f2eba520e  esito_criteri.json
7b53967763fb799ad02e44610ee87036dda73ae6febf1f84a4a6e586768238e4  tabelle/campione_ortofoto.csv
fa785d6deb53050d8c53e2d890e1f26d3871fc584e2525168739363f618a998a  tabelle/cascata.csv
d4211b4697b4fc9b832000ac209752d738547fe65295ad3ce9bc6e557175f159  tabelle/codifica_ortofoto.csv
7cc202402f3acfef0bac4930e975526be2026ca08de7ff73c909414641aff922  tabelle/controllo_ortofoto_esito.csv
9fd3f8f5969eb90bbdb4c50ce05c400d488c65c75224c2aeca573db94bb8db28  tabelle/copertura_ambiti.csv
c4b62e281dede1d01804bbee92b98e6ff544a0e62aa4efa4f9813143f86bbbfb  tabelle/lotti_attributi.csv
da1d1b86082842b32253ece25f4f8fa7a71edd729c97e6ee72619b95b335bc28  tabelle/metadati.csv
3df9410c6e23581c2f51982c781e5856e739489d7b4270f9ced3ff6a37e69743  tabelle/nil_classe.csv
6fa2af74e09671ec75aea0696b87092238643a26c5dd71a6b11293abd81783fb  tabelle/screening_ds503_chiave.csv
e92d4f2df32e7ce82e9ccb59960ccedcd05f38bf14374deec41af04075318530  tabelle/screening_ds503_codifica.csv
94a84b49cdd4ce94b0b3e3e825935db7be4989974944e8ba4dd8c53444565c08  controllo_umano/chiave_da_aprire_dopo.csv
7864ddcf1c31991a2f30ca97806e58d7cc5b25d26174ac88bed7c7718fc15096  controllo_umano/modulo_dennis.csv
f578116f49db07ea11119c4845e0afd878773114aa983d057d4eefc01c0215f3  controllo_secondo_codificatore/codifica_secondo.csv
3516c8fedb9ca93efe56b79141a1641b13d55f1edba5d10c46b20368c446a765  controllo_secondo_codificatore/ISTRUZIONI.txt
39e4c160ade8c90c9e714800d5c6154afa98158ff40e83c14b55d8a1f6ce8180  esecuzioni/00_preregistrazione.txt
e8d967d3a9deec7419f3398dbba86a0d53e46f9b7e0a1bc1fe298ceedf7e696c  fig/cascata.png
aa33ce5f59a12cfd6b07942b9f48ea00dd2cd8ad008f03604f70a63f75627c1a  fig/mappa_classi.png
```
