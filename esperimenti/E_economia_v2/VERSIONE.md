# Base E v2 — congelata il 2026-11-23 (decisione di Dennis)

Ticket #19. Revisione indipendente: passa con correzioni (fatte nel REPORT). Scelte H1–H19 confermate da Dennis il 23/11.

**Uscita principale**: canone di pareggio con suolo gratuito (`tabelle/c_star_per_regione.csv`), da riportare sempre nelle tre regioni (tarata / cubo / bandi deserti): a 60 anni 130 / 148 / 172 €/m²/anno. Formulazioni ammesse: F-a (B, C, D), F-c, F-d, F-e, F-f del REPORT; F-b non ammessa.

**Hash di contenuto delle tabelle**: `024ac9ea2a2b50314dab71a6afc200416c3be7346b188f5f6e788b4ece725454`.

**File e SHA-256**
- 45cccede184e79c4bd83cf196ee26361ad085d63472ceb5bad47d2198d6d25fe  run.py
- aecfa9819f3ac5606128f02c661052acb4520ea727c5333b68a999710c31c366  test_economia.py
- 689ea5523965fb101a77f7756dbf5a4e544fb1625378005fa99686b41d716424  esito_criteri.json
- 01d503634c586138316880f8fd38ea097a40001e0617e55dd5b2278edeebe769  esecuzioni/00_preregistrazione.txt
- 3566d11fc0859dcd822ca47f7bd352b6884d9c881832271ae5c0b75ed43ebac4  tabelle/E6_celle.csv
- 51c19019df296c02174bb09136ee1c5f4b59fc0950e5df9e1867e31a4aac6a4e  tabelle/E6_fuori_elenco.csv
- 00c5d36cce45e2fc992f4201bef40775a1c60e16e682eef7883e6ef14c20743c  tabelle/bonifica.csv
- 0c44a0f4241cea068aab124d3eb84625560ef23a55ab3a8d84a176913e457d15  tabelle/c_star_per_regione.csv
- e5b35556fafa7cacca6afa59913f62fe2363d077543c2b026a46d66ed36d9b7c  tabelle/dcf_developer.csv
- c562c640ac26a6f9eba51fa3eb3819e1d8e4f3763f908903bd5e58f04612ed2a  tabelle/gfu_scenario.csv
- 135d2fef9ab634b11473d89e0401dd54ac650751fb70c03a15255d24d2d46102  tabelle/lotti_omi.csv
- 4c114b1e6b1853268b88cfe3898e9a0a89d8ff403ad6ede639b666197ed2faf3  tabelle/prcc.csv
- b28e0706d79373ca65705443e67362e989527f0b75c2cadd6821dadd73b291ec  tabelle/regione_sintesi.csv
- 7960bf47a3c4e5dd7782b797be715bde8bb959a95a0331ebb660d790ba27a86f  tabelle/sintesi_proprieta.csv
- 889ad165d6e2c738e7a61a2b5d4992742c7108f0bc3682499f63b36203e1eba0  tabelle/tornado.csv
- 97a129ceab96c8536bdfffcab7b36010a29cb2c0974aa12496ab01bdabc7f883  tabelle/delta_L_lotti.csv.gz

**Avvertenze per le prove successive**: non usarla come vincolo di fattibilità per lotto nei metodi B0–B6; quote = quote della regione dei parametri, non probabilità; errore di taratura non misurato (E5); η senza fonte; ramo developer non tarato su compravendite; rifare la taratura K1 quando ci sarà un'aggiudicazione del Piano Casa con corrispettivo da fonte istituzionale.
