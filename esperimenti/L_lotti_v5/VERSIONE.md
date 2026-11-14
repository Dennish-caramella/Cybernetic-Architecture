# Base L — versione

- Versione: **v5 candidata**, 2026-11-14, ticket #38 (revisione di v4, #37). Semi: 42 (k-means), 3513 (screening ds503 v3, riusato), 5511 (campione C5-fisico). CRS EPSG:32632.
- Unica modifica sostanziale rispetto a v4: ambiti del PGT 2030 vigente (18 PA/AS dello strato 11 del mosaico regionale, schede MA del 05/02/2020; 7 poligoni dell'AdP Scali ferroviari, decreto 754 del 01/08/2017; 4 GFU con perimetro AT 2012 sostitutivo [H]) al posto dello strato AT del PGT 2012.
- Stato: **non accettata, non congelata**. C1–C4, C6, C8 passano; C5-fisico in attesa dei due codificatori ciechi (`controllo_codificatore_1/`, `_2/`); C9 in attesa del codificatore 2 e, per 20 poligoni N, di Dennis (`censimento_AT/`). C7 non è un criterio (deciso da Dennis, #38). Revisione indipendente non fatta.
- Hash del contenuto (attributi + WKB 2D normalizzati, ordinati per id): `440bf046ea720d4a3ca0c2a3f6cf45c86d6921591c88f685cf09b7f9d68fb722`, identico nelle esecuzioni complete 2, 3 e 4 (C8).
- Pre-registrazione: `esecuzioni/00_preregistrazione.txt`, SHA-256 `5e2da4ab…`, scritta alle 10:24Z prima del pilota (10:30Z); non committata (il compito vietava i commit): la precedenza si regge su registro e mtime [I].
- Correzioni dopo la prima esecuzione completa (nel registro con motivo): una sola, di codice, per allineare il codice al testo pre-registrato 1.3 (particelle in ambito con punto interno fuori da ogni poligono); più una correzione cosmetica (centroide in EPSG:32632 per Sentinel-2).
- Censimento: `censimento_AT/codifica_1.csv` SHA-256 `a3ad9dda…` registrato prima del codificatore 2.
- Immagini (non versionate, *.jpg ignorati da git): AGEA 2018–2019 in `_cache/L_lotti_v5/orto/img/` e `controllo_*/img/`; Sentinel-2 cloudless 2025 (EOX, CC BY-NC-SA 4.0) in `_cache/L_lotti_v5/s2/` e `controllo_*/img_s2/`. Strati 2030 in `_cache/L_lotti_v5/raw/`, schede MA in `_cache/pgt2030/`.

## SHA-256 dei file
```
660ade429411c2510afa7caab6c716406daf8dc9a017aeb0828fbae26f307c97  lotti_v5.gpkg
3ace4844793239055910c41e9f128459734881f3c46e23382e425f485695e0d8  run.py
438343a26c4e550c5a6f5e265974bf69be38560f1fdc18434dc3b2c218e66539  test_lotti.py
944a8e18ef37a88a909710eac6ecc60757e8074b3b4336c95a37db7ca2abfc2d  requirements.txt
0af529f0eb66035ee36bacfeaf1d15ac4bdbc06439d5ec848b9de418a105cc51  README.md
1ae40263cd5ca837c06f3325eac30626340f97fb20f39018d60d5d9a0bcb0148  esito_criteri.json
f24f852516d0d5b9341c660b55a0a29e4055b460f67d7ec547c92802858c36c2  tabelle/ambiti_2030.csv
2bc39d1fb318289ebe9b2ab5eb9cb20f7aff89ce2883ee7dd59a7092b0e11f5b  tabelle/cascata.csv
63608d28dcd7022a4281fd3c4d9a2276fa0917ca83dde4287bbf555a902a4e64  tabelle/catasto_tasselli_riscaricati.csv
2cd3a5bf89fa13350652102725a210b63aea660771a419f764e2cbfc1aed26e6  tabelle/copertura_ambiti_2030.csv
f719a6bd649f7338c83b94bccb9433e9397934f39bdc28b38d86a07c251589d9  tabelle/diagnosi_particelle_mancanti.csv
f1b7b786edcc8c3a169ce7520d918d406fe75b478142ce356d0bd83ebd20151b  tabelle/lotti_attributi.csv
481876e5bfe6887e5a503e547cd4ef73df947d2e2384d55046ffd304e8b94b10  tabelle/metadati.csv
f8cc1fb4872b873e24719a341c8db215696c5d83fce0cf8d6ae8c6fd9a736519  tabelle/nil_classe.csv
c21cd8b7bdaa6ae571e57bd9e1ae04cfbe23a8e1e95df48a94a9b7de4abb24b3  tabelle/screening_ds503_non_codificati.csv
73811b76f99d79fb6213d83d4766128025dffa45175c350158b112a05bec0a9e  tabelle/tabella_AT_2012_2030.csv
f01c9e00a362d5eb4e8b4afb701e9d6a56dfd766bb79f73f0b7897c66679a616  tabelle/sensibilita_senza_gfu.json
d787a547e858e38150fe794837e82068870300e9dc8bba82392c58a9590da1d4  chiavi/campione_chiave.csv
ef22c48a8d82b6e75033dec3ec88ab31f4cdb6a39df99dd73e1c92b48f7f8a0e  controllo_codificatore_1/codifica.csv
7b1f1bb4ec9673578dd5904d98c508fbe14189db3a61b50608917ffb1088fd3f  controllo_codificatore_1/ISTRUZIONI.txt
ef22c48a8d82b6e75033dec3ec88ab31f4cdb6a39df99dd73e1c92b48f7f8a0e  controllo_codificatore_2/codifica.csv
58f84040a4a18ffdf327e6cd055955a7bf5df601b70df870806a28da1e25654d  controllo_codificatore_2/ISTRUZIONI.txt
ea3c2542f2163f41c92815a03ac5c5e3d72389f065ff9c8bcf22df52acd4091c  censimento_AT/ISTRUZIONI.txt
f24f852516d0d5b9341c660b55a0a29e4055b460f67d7ec547c92802858c36c2  censimento_AT/ambiti_2030.csv
a3ad9dda8ef7783f4346e5612b4d82807261f547f9bafe641adc71bdc5609475  censimento_AT/codifica_1.csv
71c9007ca104980be96924e1940b4b9885c6624541e204d8054cd999349986db  censimento_AT/foglio_vuoto.csv
62145b1ae30ddffde9c7d9dca17ec24757cbb5865e3b69e9ce5cc160b5bcf4c6  censimento_AT/fonti_AT.csv
5e2da4abf09080d2b0c251681187e9da25264e8cbce83d68a48273871b77f4cf  esecuzioni/00_preregistrazione.txt
8d342fb0603e86552175eae7818884dbd1d9e293c730b0acdbb7772c75e1de24  fig/cascata.png
2a1536026ae900fe8a32092a9d33e118d1eae3b818255729dd54d1baeca71ad6  fig/mappa_classi.png
```
