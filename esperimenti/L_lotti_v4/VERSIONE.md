# Base L — versione

- Versione: **v4 candidata**, 2026-11-12, ticket #37 (revisione di v3, #35). Semi: 42 (k-means), 3513 (screening ds503 v3, riusato), 4511 (campione C5-fisico), 4512 (20 casi di Dennis). CRS EPSG:32632.
- Stato: **non accettata, non congelata**. C1–C4, C6, C8 passano; C5-fisico in attesa dei due codificatori ciechi (`controllo_codificatore_1/`, `_2/`); C9-AT in attesa del codificatore 2 e, per 12 poligoni N, di Dennis (`censimento_AT/`); C7 in attesa di Dennis (`controllo_umano/`). Revisione indipendente non fatta.
- Hash del contenuto (attributi + WKB 2D normalizzati, ordinati per id): `4de6e98855905882d8d1f547756efaeeef74200c138462accc556439f187ad31`, identico nelle esecuzioni complete 2bis, 3 e 4 (C8).
- Pre-registrazione: `esecuzioni/00_preregistrazione.txt`, SHA-256 `6bc51a3d…`, scritta alle 07:05Z prima del pilota (07:12Z); non committata (il compito vietava i commit): la precedenza si regge su registro e mtime [I].
- Correzioni dopo la prima esecuzione completa (tutte nel registro con motivo): tasselli catastali vuoti riscaricati (errore di acquisizione ereditato da v1: 34 tasselli, 17.866 particelle); screening ds503 unito per riferimento (19 candidati nuovi non confermati); un test troppo stretto.
- Censimento AT: `censimento_AT/codifica_1.csv` SHA-256 `c73c433d…` registrato prima del codificatore 2.
- Immagini AGEA (sola visione) non versionate: `_cache/L_lotti_v4/orto/img/` e cartelle `controllo_*/img/`. Catasto v4: `_cache/L_lotti_v4/raw/catasto/`.

## SHA-256 dei file
```
4f2ee3e13f18944ebdff6de41ba17f946a0d0000f79dd6eef32fae2447cfdb12  lotti_v4.gpkg
94f0a17b597020712bdfd08ad33ce07dd859d81b21df64a9c8ecda30347fd6fd  run.py
53fc3b7fa7fe086b4eed0db2f57b7148133d3654f2513a3a48978f24467b858b  test_lotti.py
eb05ec2ebd1ed165b2e8b44c9c9a68c302ede2a6bc88b05bece549b8a1e0ca29  requirements.txt
b66acd05b58e21a7a5a912041908a841c401bf798b454890a30d64369d5eb06c  esito_criteri.json
2f2b96a5acdd4d67f4f19332f9e17244b139491443ee51bc8d221179ed5f8acd  tabelle/cascata.csv
63608d28dcd7022a4281fd3c4d9a2276fa0917ca83dde4287bbf555a902a4e64  tabelle/catasto_tasselli_riscaricati.csv
b6dd89438b75ebd5fc4a795fd38bfbe266e8113e7ef64ff7782330fe7c757f4d  tabelle/copertura_ambiti.csv
e1d9b8d6e51fb069cd638d96e8c84b80314afdabc5c0c3086e299b4f0a42cfb5  tabelle/diagnosi_particelle_mancanti.csv
eb6505a81627e9c0bf090dde5140d9c05bbe6e913c98737092c78a5f894fa3ee  tabelle/lotti_attributi.csv
abe77b31573dac3addebfba857f07baa2f668c96c01356a10da8875027f1bb66  tabelle/metadati.csv
d66a358f174d5a8eaa59240d8cec61c98d749e92c9cfb57f0e365ee0aa86ec7f  tabelle/nil_classe.csv
c21cd8b7bdaa6ae571e57bd9e1ae04cfbe23a8e1e95df48a94a9b7de4abb24b3  tabelle/screening_ds503_non_codificati.csv
082cde99f491c22a5e4b8bdfec77f1b329bf3c85360f26acb3e68aefc0288275  chiavi/campione_chiave.csv
911581992fe9c83c09557eda7aa56cd39560652145cc541d31ef7481059808dc  controllo_umano/chiave_da_aprire_dopo.csv
e00af2e1acd85a15c7781431673975b06b4dc7319c1313a72e5ba2efdba164b3  controllo_umano/modulo_dennis.csv
b8190f198b836d0e4b37545e52efd440f92e01af3168c7fa0aa41ef8d0feff33  controllo_codificatore_1/codifica.csv
e5509477ecd39a4b0c58b281a21a13c44f66fa64bc750b4f94399863a130f32c  controllo_codificatore_1/ISTRUZIONI.txt
b8190f198b836d0e4b37545e52efd440f92e01af3168c7fa0aa41ef8d0feff33  controllo_codificatore_2/codifica.csv
c73c433d338dd2f7ce5c345c2d2f3aa1078aae421f99f92a6be3a057ea903e28  censimento_AT/codifica_1.csv
55ee76f5f6a3b860cf650ec0c8a18d8a81983af80921a4f0decb567bbb0bd054  censimento_AT/foglio_vuoto.csv
42bc0e0b6cc7dee6d3d3ef0ccad8912dd4c69caad059f80a044941b25f51ff55  censimento_AT/fonti_AT.csv
d2af7828b57b9ab7500522a9ce79c54b7c6a9ab098398b28f293d082fd51c512  censimento_AT/ISTRUZIONI.txt
6bc51a3d3d3d99f2ae1031fad9b43e2d5d17f74b03ca73fae3485ede041fdbeb  esecuzioni/00_preregistrazione.txt
84ad391fd3bca7c05f5f09461d53600ef3d602954a33ee42006813b9564e6b2a  fig/cascata.png
2c3ef330c5aadeac45badfa870221b27b2d66ee970d86519c4224bcce95ecb92  fig/mappa_classi.png
```
